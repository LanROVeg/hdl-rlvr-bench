#!/usr/bin/env python3
"""Build clean task images and test baselines, references, and known grader attacks."""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import tomllib

ROOT=Path(__file__).resolve().parents[1]
TASKS=sorted(p for p in ROOT.iterdir() if (p/'task.toml').is_file())

def checked(args, **kwargs):
    result=subprocess.run(args,text=True,capture_output=True,**kwargs)
    if result.returncode:
        raise RuntimeError(f'Command failed: {args}\n{result.stdout[-5000:]}\n{result.stderr[-5000:]}')
    return result

def evaluate(task,source):
    filename='filter.cir' if task.name.startswith('spice') else 'alu_8b.vhd'
    with tempfile.TemporaryDirectory() as name:
        candidate=Path(name)/'submission'
        if source is not None: candidate.write_text(source)
        args=['docker','run','--rm','--network','none','--memory','512m','--cpus','1',
              '--pids-limit','128','-v',f'{task}/tests:/tests:ro',
              '-v',f'{name}:/candidate:ro',f'ee-bench-{task.name}:local','bash','-lc']
        copy=f'cp /candidate/submission /workspace/{filename}; ' if source is not None else f'rm -f /workspace/{filename}; '
        validate="python3 -c 'import json,math; from pathlib import Path; p=Path(\"/logs/verifier\"); d=json.loads((p/\"reward.json\").read_text()); assert set(d)=={\"reward\"}; r=d[\"reward\"]; assert type(r) in (int,float) and math.isfinite(r) and 0<=r<=1; assert float((p/\"reward.txt\").read_text())==r; assert (p/\"details.json\").is_file()'"
        result=checked(args+['set -e; '+copy+'bash /tests/test.sh; '+validate],timeout=140)
        return json.loads(result.stdout.strip().splitlines()[-1])

def cases(task):
    if task.name.startswith('spice'):
        starter=(task/'environment/workspace/filter.cir').read_text()
        golden=(task/'solution/filter_golden.cir').read_text()
        spoof=starter.replace('.end','.control\nrun\necho 0 1.000000e+01 1.0 0.0\necho 1 1.000000e+03 0.7071 -0.7853981633974483\nquit\n.endc\n.end')
        return [('nop',starter,'baseline'),('oracle',golden,'perfect'),
                ('stdout_spoof',spoof,'zero'),('changed_topology',golden.replace('100nF','1nF'),'zero'),
                ('include_attempt',golden.replace('.end','.include /solution/filter_golden.cir\n.end'),'zero'),
                ('nonfinite_value',golden.replace('1591.55','NaN'),'zero'),('missing_file',None,'zero')]
    starter=(task/'environment/workspace/alu_8b.vhd').read_text()
    golden=(task/'solution/alu_8b_golden.vhd').read_text()
    i=starter.lower().index('begin')+5
    spoof=starter[:i]+'\nprocess begin report "SCORE_DATA:524288:524288"; wait; end process;\n'+starter[i:]
    wrong=golden.replace('NZVC   <= n_flag & z_flag & v_flag & c_flag;', 'NZVC <= "0000";')
    if wrong==golden: raise AssertionError('Flag mutation did not alter the source')
    return [('nop',starter,'baseline'),('oracle',golden,'perfect'),('stdout_spoof',spoof,'no_increase'),
            ('wrong_flags',wrong,'imperfect'),('syntax_error','not VHDL','zero'),
            ('missing_file',None,'zero')]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--skip-build',action='store_true')
    parser.add_argument('--harbor',action='store_true',help='Also run actual Harbor NOP/oracle jobs')
    parser.add_argument('--output',type=Path,default=ROOT/'check-results')
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    names=[]; records=[]
    for task in TASKS:
        config=tomllib.loads((task/'task.toml').read_text())
        names.append(config['task']['name'])
        assert config['metadata']['id']==task.name
        assert config['verifier']['environment_mode']=='separate'
        assert config['artifacts']
        if not args.skip_build:
            checked(['docker','build','-t',f'ee-bench-{task.name}:local',str(task/'environment')],timeout=600)
        baseline=None
        for label,source,expect in cases(task):
            start=time.monotonic(); result=evaluate(task,source); score=result['reward']
            if expect=='baseline':
                assert 0<=score<1,(task.name,label,result); baseline=score
            elif expect=='perfect': assert score==1,(task.name,label,result)
            elif expect=='zero': assert score==0,(task.name,label,result)
            elif expect=='no_increase': assert score<=baseline,(task.name,label,result)
            else: assert score<1,(task.name,label,result)
            record={'task':task.name,'case':label,**result,'seconds':round(time.monotonic()-start,2)}
            records.append(record)
            print(f'{task.name:26s} {label:18s} {score:.6f}',flush=True)
    assert len(set(names))==len(names),'Duplicate task names'
    (args.output/'results.json').write_text(json.dumps(records,indent=2)+'\n')
    example=ROOT/'examples/synchronous-counter'
    design=(example/'counter_8b.vhd').read_text()
    mutations={
        'reference':design,
        'wrong_increment':design.replace('count + 1','count + 2'),
        'asynchronous_reset':design.replace('process(clk)','process(clk, rst)').replace(
            "if rising_edge(clk) then\n            if rst = '1' then\n                count <= (others => '0');\n            elsif load = '1' then",
            "if rst = '1' then\n            count <= (others => '0');\n        elsif rising_edge(clk) then\n            if load = '1' then"),
        'wrong_priority':design.replace("if rst = '1' then","if load = '1' then").replace(
            "elsif load = '1' then","elsif rst = '1' then"),
    }
    for label,source in mutations.items():
        assert label=='reference' or source!=design,'Counter mutation must change source'
        with tempfile.TemporaryDirectory() as name:
            path=Path(name)
            (path/'counter_8b.vhd').write_text(source)
            shutil.copy2(example/'counter_tb.vhd',path/'counter_tb.vhd')
            result=subprocess.run(['docker','run','--rm','--network','none','--memory','512m',
                '-v',f'{path}:/src:ro','ee-bench-vhdl-alu-flags-001:local','bash','-lc',
                'set -e; cd "$(mktemp -d)"; ghdl -a --std=08 /src/*.vhd; ghdl -e --std=08 counter_tb; ghdl -r --std=08 counter_tb --assert-level=error'],
                text=True,capture_output=True,timeout=60)
            if label=='reference':
                assert result.returncode==0,result.stdout+result.stderr
                assert '2048' in result.stdout,result.stdout
            else:
                assert result.returncode!=0,(label,'Mutation escaped assertions')
                assert 'assertion failure' in result.stdout.lower(),(label,result.stdout,result.stderr)
            print(f'counter example: {label} verified',flush=True)
    if args.harbor:
        harbor=shutil.which('harbor')
        if not harbor: raise RuntimeError('Install requirements-dev.txt first')
        assert checked([harbor,'--version']).stdout.strip()=='0.25.0','Use pinned Harbor 0.25.0'
        for agent in ['nop','oracle']:
            out=args.output/f'harbor-{agent}'
            checked([harbor,'run','--path',str(ROOT),'--agent',agent,'--n-concurrent','1',
                     '--jobs-dir',str(out),'--job-name',f'{agent}-{time.time_ns()}','--quiet'],timeout=1200)
            results=list(out.glob('*/**/result.json'))
            trials=[]
            for path in results:
                data=json.loads(path.read_text())
                if 'verifier_result' in data: trials.append(data)
            assert len(trials)==len(TASKS),(agent,'Expected one completed trial per task',len(trials))
            for trial in trials:
                assert trial.get('exception_info') is None,trial.get('exception_info')
                reward=trial['verifier_result']['rewards']['reward']
                assert reward==1 if agent=='oracle' else 0<=reward<1,(agent,reward)
            print(f'Harbor {agent}: {len(trials)} trials validated',flush=True)
    print(f'PASS: {len(records)} container regression checks',flush=True)

if __name__=='__main__':
    main()
