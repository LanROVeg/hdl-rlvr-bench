#!/usr/bin/env python3
"""Read a constrained passive topology; simulate a verifier-owned reconstruction."""
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile

SOURCE=Path('/workspace/filter.cir')
NUMBER=r'([+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)(meg|[tgkmunpf])?(?:ohm|f)?'
SCALE={'':1.,'t':1e12,'g':1e9,'meg':1e6,'k':1e3,'m':1e-3,'u':1e-6,'n':1e-9,'p':1e-12,'f':1e-15}

def value(token):
    m=re.fullmatch(NUMBER,token,re.I)
    if not m:
        raise ValueError('Expected a positive literal SPICE component value')
    v=float(m[1])*SCALE[(m[2] or '').lower()]
    if not math.isfinite(v) or v<=0:
        raise ValueError('Value must be finite and positive')
    return v

def components():
    if not SOURCE.is_file() or SOURCE.is_symlink() or SOURCE.stat().st_size>16384:
        raise ValueError('Missing, oversized, or linked input')
    found={}; ended=False
    for raw in SOURCE.read_text().splitlines():
        line=raw.strip()
        if not line or line.startswith('*'):
            continue
        if ended:
            raise ValueError('Content after .end is not allowed')
        parts=line.split(); tag=parts[0].lower()
        if tag in {'v1','r1','c1'}:
            if tag in found:
                raise ValueError('Duplicate component')
            required={'v1':['v1','in','0','ac'],'r1':['r1','in','out'],'c1':['c1','out','0']}[tag]
            if [s.lower() for s in parts[:-1]]!=required:
                raise ValueError('Topology must remain V1, R1, C1 as specified')
            found[tag]=value(parts[-1])
        elif line.lower() in {'.ac dec 10 10 100k','.print ac vm(out) vp(out)'}:
            continue
        elif line.lower()=='.end':
            ended=True
        else:
            raise ValueError('Unsupported directive or component; .control/.include are not allowed')
    if not ended or set(found)!={'v1','r1','c1'}:
        raise ValueError('Expected V1, R1, C1 and .end')
    if not math.isclose(found['v1'],1.,rel_tol=1e-12):
        raise ValueError('V1 must stay AC 1.0')
    if not math.isclose(found['c1'],100e-9,rel_tol=1e-12):
        raise ValueError('C1 must stay 100nF')
    if not 1<=found['r1']<=1e9:
        raise ValueError('R1 must be between 1 ohm and 1 Gohm')
    return found

def measure(tmp,r,c,ac):
    analysis='.ac lin 1 1000 1000\n.print ac vr(out) vi(out)' if ac else '.dc V1 1 1 1\n.print dc v(out)'
    netlist=f'Verifier-owned RC measurement\nV1 in 0 DC 1 AC 1\nR1 in out {r:.17g}\nC1 out 0 {c:.17g}\n{analysis}\n.end\n'
    p=tmp/('ac.cir' if ac else 'dc.cir'); p.write_text(netlist)
    result=subprocess.run(['ngspice','-n','-b',str(p)],cwd=tmp,capture_output=True,text=True,
                          timeout=10,env={'PATH':'/usr/bin:/bin','HOME':str(tmp)})
    if result.returncode:
        raise RuntimeError('Trusted ngspice measurement failed: '+result.stderr[-1000:])
    rows=[]
    for line in result.stdout.splitlines():
        fields=line.split()
        if len(fields)==(4 if ac else 3) and fields[0]=='0':
            row=[float(v) for v in fields[1:]]
            if all(math.isfinite(v) for v in row): rows.append(row)
    if len(rows)!=1 or not math.isclose(rows[0][0],1000 if ac else 1,abs_tol=1e-6):
        raise RuntimeError('Expected one finite measurement at specified operating point')
    return rows[0][1:]

def grade():
    try:
        values=components()
    except ValueError as exc:
        return 0.,{'stage':'invalid_submission','error':str(exc)}
    with tempfile.TemporaryDirectory(prefix='rc-verifier-') as name:
        dc=measure(Path(name),values['r1'],values['c1'],False)[0]
        real,imag=measure(Path(name),values['r1'],values['c1'],True)
    dc_db=20*math.log10(abs(dc)) if dc else -math.inf
    mag_db=20*math.log10(math.hypot(real,imag))
    phase=math.degrees(math.atan2(imag,real))
    score=.2
    score+=.2 if abs(dc_db)<=.1 else 0
    score+=.3 if abs(mag_db-(-3.01029995664))<=.1 else 0
    score+=.3 if abs(phase+45.)<=2. else 0
    return round(score,6),{'stage':'complete','r_ohm':values['r1'],'dc_gain_db':dc_db,
                         'gain_db_1khz':mag_db,'phase_deg_1khz':phase}

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
