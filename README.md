# HDL & SPICE RLVR Benchmark Suite (`hdl-rlvr-bench`)

Containerized, deterministic evaluation environments for **Digital Logic (VHDL / GHDL)** and **Analog Circuit Analysis (Ngspice)** following the Harbor / Terminal-Bench verifier specification.

## Architecture
Each task environment is packaged as an isolated Ubuntu 24.04 container with a locked verification entrypoint (`/tests/test.sh` -> `/logs/verifier/reward.json`) providing dense, multi-stage process rewards (`0.00` to `1.00`) and anti-cheat randomized testbench synthesis.

## Verified Tasks
| Task ID | Subdomain | Tooling | NOP Baseline | Oracle Score | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `vhdl-alu-flags-001` | Digital Logic (VHDL-2008) | `ghdl-mcode` | `0.2467` | `1.0000` | 8-Bit Combinational ALU with Two's Complement `NZVC` status flags and dynamic 60-vector verification. |
| `vhdl-alu-fault-002` | RTL Bug Triage (VHDL-2008) | `ghdl-mcode` | `0.7133` | `1.0000` | Pre-populated 8-Bit ALU injected with 3 datapath and flag-generation bugs requiring diagnosis and patching. |
| `spice-rc-phase-003` | Analog AC Analysis | `ngspice` | `0.4000` | `1.0000` | Single-pole RC low-pass filter tuning for exact $-3\text{ dB}$ magnitude ($0.7071\text{ V/V}$) and $-45^\circ$ phase shift at $1\text{ kHz}$. |
