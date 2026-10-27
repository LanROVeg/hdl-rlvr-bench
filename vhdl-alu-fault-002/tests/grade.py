#!/usr/bin/env python3
import json, os, random, subprocess, tempfile

WORKSPACE_VHD = "/workspace/alu_8b.vhd"

def compute_expected(a: int, b: int, sel: int):
    v, c = 0, 0
    if sel == 0:
        full = a + b
        res = full & 0xFF
        c = 1 if full > 0xFF else 0
        sa, sb, sr = (a >> 7) & 1, (b >> 7) & 1, (res >> 7) & 1
        v = 1 if ((sa == sb) and (sr != sa)) else 0
    elif sel == 1:
        res = (a - b) & 0xFF
        c = 1 if a < b else 0
        sa, sb, sr = (a >> 7) & 1, (b >> 7) & 1, (res >> 7) & 1
        v = 1 if ((sa != sb) and (sr != sa)) else 0
    elif sel == 2: res = a & b
    elif sel == 3: res = a | b
    elif sel == 4: res = a ^ b
    elif sel == 5:
        c = (a >> 7) & 1
        res = (a << 1) & 0xFF
    elif sel == 6:
        c = a & 1
        res = (a >> 1) & 0xFF
    else: res = a

    n = (res >> 7) & 1
    z = 1 if res == 0 else 0
    nzvc = (n << 3) | (z << 2) | (v << 1) | c
    return res, nzvc

def generate_vhdl_tb(vectors):
    stim = []
    for (a, b, sel, exp_res, exp_nzvc) in vectors:
        stim.append(f"""
        A <= "{a:08b}"; B <= "{b:08b}"; ALU_Sel <= "{sel:03b}";
        wait for 10 ns;
        if Result = "{exp_res:08b}" then res_pass := res_pass + 1; end if;
        if Result = "{exp_res:08b}" and NZVC = "{exp_nzvc:04b}" then flag_pass := flag_pass + 1; end if;""")
    return f"""
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
entity alu_tb_eval is end alu_tb_eval;
architecture sim of alu_tb_eval is
    signal A, B, Result : std_logic_vector(7 downto 0) := (others => '0');
    signal ALU_Sel : std_logic_vector(2 downto 0) := (others => '0');
    signal NZVC : std_logic_vector(3 downto 0) := (others => '0');
begin
    uut: entity work.alu_8b port map (A => A, B => B, ALU_Sel => ALU_Sel, Result => Result, NZVC => NZVC);
    process
        variable res_pass, flag_pass : integer := 0;
    begin
        {"".join(stim)}
        report "SCORE_DATA:" & integer'image(res_pass) & ":" & integer'image(flag_pass);
        wait;
    end process;
end sim;
"""

def grade():
    reward = 0.0
    details = {}
    with tempfile.TemporaryDirectory() as tmpdir:
        comp = subprocess.run(["ghdl", "-a", "--std=08", f"--workdir={tmpdir}", WORKSPACE_VHD], capture_output=True, text=True)
        if comp.returncode != 0:
            print(json.dumps({"reward": 0.0, "stage": "compile_failed", "stderr": comp.stderr}))
            return
        reward += 0.20
        rng = random.Random(20261026)
        raw_cases = [(127,1,0), (128,1,1), (255,1,0), (5,10,1), (0x80,0,5), (0x01,0,6)]
        for _ in range(54):
            raw_cases.append((rng.randint(0,255), rng.randint(0,255), rng.randint(0,7)))
        vectors = [(a, b, s, *compute_expected(a, b, s)) for (a, b, s) in raw_cases]
        tb_path = os.path.join(tmpdir, "alu_tb_eval.vhd")
        with open(tb_path, "w") as f: f.write(generate_vhdl_tb(vectors))
        subprocess.run(["ghdl", "-a", "--std=08", f"--workdir={tmpdir}", tb_path], check=True)
        subprocess.run(["ghdl", "-e", "--std=08", f"--workdir={tmpdir}", "alu_tb_eval"], check=True)
        sim = subprocess.run(["ghdl", "-r", "--std=08", f"--workdir={tmpdir}", "alu_tb_eval"], capture_output=True, text=True)
        total = len(vectors)
        for line in (sim.stdout + sim.stderr).splitlines():
            if "SCORE_DATA:" in line:
                res_p, flag_p = map(int, line.split("SCORE_DATA:")[1].strip().split(":"))
                reward += 0.40 * (res_p / total) + 0.40 * (flag_p / total)
                details = {"res_passed": f"{res_p}/{total}", "flags_passed": f"{flag_p}/{total}"}
    print(json.dumps({"reward": round(reward, 4), "details": details}))

if __name__ == "__main__":
    grade()
