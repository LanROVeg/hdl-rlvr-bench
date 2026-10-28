#!/usr/bin/env python3
import json, math, os, subprocess

CIR_FILE = "/workspace/filter.cir"

def grade():
    if not os.path.exists(CIR_FILE):
        print(json.dumps({"reward": 0.0, "error": "Missing filter.cir"}))
        return

    res = subprocess.run(["ngspice", "-b", CIR_FILE], capture_output=True, text=True)
    if res.returncode != 0:
        print(json.dumps({"reward": 0.0, "stage": "simulation_failed"}))
        return

    reward = 0.20  # Stage 1: Valid SPICE syntax & simulation
    dc_mag, fc_mag, fc_phase_deg = None, None, None

    for line in res.stdout.splitlines():
        parts = line.strip().split()
        if len(parts) >= 4 and parts[0].isdigit():
            try:
                freq = float(parts[1])
                mag = float(parts[2])
                phase_deg = math.degrees(float(parts[3]))
                if abs(freq - 10.0) < 0.1:
                    dc_mag = mag
                elif abs(freq - 1000.0) < 1.0:
                    fc_mag = mag
                    fc_phase_deg = phase_deg
            except ValueError:
                continue

    if dc_mag is not None and abs(dc_mag - 1.0) <= 0.02:
        reward += 0.20  # Stage 2: Passband gain ~0 dB (1.0 V/V)
    if fc_mag is not None and abs(fc_mag - 0.7071) <= 0.02:
        reward += 0.30  # Stage 3: -3dB cutoff magnitude at 1 kHz
    if fc_phase_deg is not None and abs(fc_phase_deg - (-45.0)) <= 1.5:
        reward += 0.30  # Stage 4: -45 deg phase angle at 1 kHz

    print(json.dumps({
        "reward": round(reward, 4),
        "details": {"dc_mag": dc_mag, "fc_mag_1khz": fc_mag, "fc_phase_deg_1khz": fc_phase_deg}
    }))

if __name__ == "__main__":
    grade()
