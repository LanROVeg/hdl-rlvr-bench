#!/usr/bin/env python3
"""Synthesize submitted RTL and exhaustively test its combinational netlist."""
import json
from pathlib import Path
import re
import resource
import subprocess
import tempfile

SOURCE = Path('/workspace/alu_8b.vhd')
TOTAL = 8 * 256 * 256
TB = '''library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;
entity verifier_tb is end;
architecture test of verifier_tb is
  signal a, b, result : std_logic_vector(7 downto 0);
  signal op : std_logic_vector(2 downto 0);
  signal flags : std_logic_vector(3 downto 0);
begin
  dut: entity work.alu_8b port map(a, b, op, result, flags);
  process
    variable r, full, sa, sb, signed_result : integer;
    variable expected : std_logic_vector(3 downto 0);
    variable data_pass, flags_pass : integer := 0;
  begin
    for s in 0 to 7 loop
      for x in 0 to 255 loop
        for y in 0 to 255 loop
          a <= std_logic_vector(to_unsigned(x, 8));
          b <= std_logic_vector(to_unsigned(y, 8));
          op <= std_logic_vector(to_unsigned(s, 3));
          expected := "0000";
          sa := x; if x >= 128 then sa := x - 256; end if;
          sb := y; if y >= 128 then sb := y - 256; end if;
          case s is
            when 0 =>
              full := x + y; r := full mod 256;
              if full > 255 then expected(0) := '1'; end if;
              signed_result := sa + sb;
              if signed_result < -128 or signed_result > 127 then expected(1) := '1'; end if;
            when 1 =>
              r := (x - y) mod 256;
              if x < y then expected(0) := '1'; end if;
              signed_result := sa - sb;
              if signed_result < -128 or signed_result > 127 then expected(1) := '1'; end if;
            when 2 => r := to_integer(to_unsigned(x,8) and to_unsigned(y,8));
            when 3 => r := to_integer(to_unsigned(x,8) or to_unsigned(y,8));
            when 4 => r := to_integer(to_unsigned(x,8) xor to_unsigned(y,8));
            when 5 =>
              r := (x * 2) mod 256;
              if x >= 128 then expected(0) := '1'; end if;
            when 6 =>
              r := x / 2;
              if x mod 2 = 1 then expected(0) := '1'; end if;
            when others => r := x;
          end case;
          if r >= 128 then expected(3) := '1'; end if;
          if r = 0 then expected(2) := '1'; end if;
          wait for 1 ns;
          if result = std_logic_vector(to_unsigned(r,8)) then
            data_pass := data_pass + 1;
            if flags = expected then flags_pass := flags_pass + 1; end if;
          end if;
        end loop;
      end loop;
    end loop;
    report "VERIFIER_COUNTS:" & integer'image(data_pass) & ":" & integer'image(flags_pass);
    finish;
  end process;
end;
'''

def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (25, 25))
    resource.setrlimit(resource.RLIMIT_FSIZE, (8*1024*1024, 8*1024*1024))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

def run(args, cwd):
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        p = subprocess.run(args, cwd=cwd, stdout=out, stderr=err, timeout=30,
                           preexec_fn=limits, env={'PATH':'/usr/bin:/bin','HOME':str(cwd)})
        out.seek(0); err.seek(0)
        return p.returncode, out.read().decode(errors='replace'), err.read().decode(errors='replace')

def grade():
    if not SOURCE.is_file() or SOURCE.is_symlink() or SOURCE.stat().st_size > 65536:
        return 0., {'stage':'invalid_source'}
    text = SOURCE.read_text()
    clean = re.sub(r'--[^\n]*', '', text)
    if re.search(r'\b(file|textio|foreign|external|configuration)\b|<<|>>', clean, re.I):
        return 0., {'stage':'unsupported_source_construct'}
    uses = re.findall(r'\buse\s+([^;]+);', clean, re.I)
    if any(u.strip().lower() not in {'ieee.std_logic_1164.all','ieee.numeric_std.all'} for u in uses):
        return 0., {'stage':'unsupported_library'}
    if [e.lower() for e in re.findall(r'\bentity\s+(\w+)\s+is\b',clean,re.I)] != ['alu_8b']:
        return 0., {'stage':'expected_one_alu_entity'}
    with tempfile.TemporaryDirectory(prefix='alu-verifier-') as name:
        tmp = Path(name)
        (tmp/'candidate.vhd').write_text(text)
        rc, netlist, err = run(['ghdl','--synth','--std=08','--out=vhdl','candidate.vhd','-e','alu_8b'],tmp)
        if rc:
            return 0., {'stage':'synthesis_failed','stderr':err[-3000:]}
        netlist = re.sub(r'--[^\n]*','',netlist)
        if re.search(r'\b(process|wait|report|assert|file|foreign)\b',netlist,re.I):
            return 0., {'stage':'not_combinational_netlist'}
        (tmp/'netlist.vhd').write_text(netlist)
        (tmp/'verifier_tb.vhd').write_text(TB)
        for args in [['ghdl','-a','--std=08','netlist.vhd','verifier_tb.vhd'],
                     ['ghdl','-e','--std=08','verifier_tb']]:
            rc, _, err = run(args,tmp)
            if rc:
                return 0., {'stage':'verifier_compile_failed','stderr':err[-3000:]}
        rc, out, err = run(['ghdl','-r','--std=08','verifier_tb','--assert-level=error','--stop-time=1ms'],tmp)
        matches = re.findall(r'VERIFIER_COUNTS:(\d+):(\d+)\s*$',out+err,re.M)
        if rc or len(matches)!=1:
            return 0., {'stage':'simulation_failed_or_incomplete','stderr':err[-3000:]}
        data, flags = map(int,matches[0])
        if not 0 <= flags <= data <= TOTAL:
            return 0., {'stage':'invalid_counts'}
        return round(.2+.4*data/TOTAL+.4*flags/TOTAL,6), {
            'stage':'complete','vectors':TOTAL,'datapath_passed':data,'flags_passed':flags}

def main():
    logs=Path('/logs/verifier'); logs.mkdir(parents=True,exist_ok=True)
    try:
        score,details=grade()
    except subprocess.TimeoutExpired:
        score,details=0.,{'stage':'timeout'}
    except Exception as exc:
        score,details=0.,{'stage':'verifier_error','error':str(exc)}
    (logs/'details.json').write_text(json.dumps(details,indent=2)+'\n')
    (logs/'reward.json').write_text(json.dumps({'reward':score},allow_nan=False)+'\n')
    (logs/'reward.txt').write_text(f'{score}\n')
    print(json.dumps({'reward':score,'details':details}))

if __name__=='__main__':
    main()
