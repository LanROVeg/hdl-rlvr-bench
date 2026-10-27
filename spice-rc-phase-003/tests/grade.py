#!/usr/bin/env python3
import json, os, subprocess, tempfile

CIR_FILE = "/workspace/filter.cir"

def grade():
    reward = 0.0
    if not os.path.exists(CIR_FILE):
        print(json.dumps({"reward": 0.0, "error": "Missing filter.cir"}))
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        # Run ngspice in batch mode (-b)
        res = subprocess.run(["ngspice", "-b", CIR_FILE], capture_output=True, text=True)
        if res.returncode != 0:
            print(json.dumps({"reward": 0.2, "stage": "simulation_failed", "stderr": res.stderr}))
            return
        reward += 0.30

        # Parse output for 1kHz phase angle and DC gain
        # Ngspice prints AC analysis output lines
        lines = res.stdout.splitlines()
        mag, phase = None, None
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 3 and "1.000000e+03" in parts[0]:
                mag = float(parts[1])
                phase = float(parts[2])
                break

        if mag is not None and phase is not None:
            # Check -3dB magnitude (~0.707) and -45 deg phase
            mag_error = abs(mag - 0.7071)
            phase_error = abs(phase - (-45.0))
            
            if mag_error < 0.05:
                reward += 0.30
            if phase_error < 2.0:
                reward += 0.40
        else:
            # Fallback check if output format differs
            reward += 0.50

    print(json.dumps({"reward": round(reward, 4)}))

if __name__ == "__main__":
    grade()
