# HDL and SPICE verification exercises

[![Verify benchmark tasks](https://github.com/LanROVeg/hdl-rlvr-bench/actions/workflows/checks.yml/badge.svg)](https://github.com/LanROVeg/hdl-rlvr-bench/actions/workflows/checks.yml)

An undergraduate EE portfolio project combining VHDL, circuit simulation, Python, Docker,
and machine-readable grading. Three introductory exercises are packaged for **Harbor
0.25.0**, with fresh verifier containers and explicit submission artifacts.

This is a small educational suite, not a validated commercial dataset or a claim about
frontier-model difficulty. Development, verification improvements, and documentation use
substantial AI assistance. The goal is to make each specification and check inspectable.

## Exercises and reproduced scores

- **vhdl-alu-flags-001**: implement an 8-bit combinational ALU with NZVC flags.
  Unmodified starter: **0.206569**; reference: **1.000000**.
- **vhdl-alu-fault-002**: repair swapped logic operations, a shift/carry defect, and an
  incorrect zero flag. Unmodified starter: **0.699216**; reference: **1.000000**.
- **spice-rc-phase-003**: choose R1 for a passive RC low-pass cutoff at 1 kHz with fixed
  100 nF capacitance. Unmodified starter: **0.400000**; reference: **1.000000**.

Scores above were reproduced in manual Docker checks and actual Harbor 0.25.0 NOP/oracle
trials on October 29, 2026. All six Harbor trials completed without exceptions. A starter
can earn partial credit; only a score of 1.0 means all specified functional checks passed.

## Run locally

Use Linux or WSL2 with Python 3.12+, Docker Engine, and Docker Compose available.
No commercial EDA software, GPU, model API key, or paid model run is needed.

```bash
# Build images from their actual environment/ contexts and run regression checks.
bash run_all_checks.sh

# Optional: also validate with the pinned Harbor runner.
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
bash run_all_checks.sh --harbor
```

The check runner verifies all three baselines and references, numeric reward artifacts,
known output-spoofing attempts, broken flags, malformed/missing inputs, and prohibited
SPICE constructs. It also tests the clocked-counter practice example and three behavioral
mutations. Detailed local results go to ignored `check-results/`; CI uploads its results.

## What the verifiers trust

**VHDL:** GHDL synthesizes the submitted self-contained RTL. The verifier simulates the
resulting combinational netlist against a verifier-owned bench across **all 524,288 binary
A/B/opcode combinations**. It never runs the original behavioral source as a testbench or
adds credit from arbitrary submitted report messages. Synthesis and simulation have time
limits; invalid/incomplete runs fail closed. The score is 0.20 synthesis, 0.40 result
accuracy, and 0.40 correct flags gated on a correct result.

**SPICE:** a small allowlisted parser accepts the specified V1/R1/C1 topology and literal
component values. The verifier constructs and runs a fresh circuit for true DC gain and
complex response at 1 kHz. Submitted `.control`, `.include`, expressions, and fabricated
measurements cannot supply scores. Prompt and verifier use the same gain/phase tolerances.

**Harbor:** only declared source artifacts cross into a fresh verifier container. Tests,
solutions, or modified agent-side executables do not transfer. `reward.json` contains one
numeric metric, `reward.txt` the same score, and diagnostics live separately in `details.json`.

These checks address the documented attacks; they are not a proof against every compiler,
simulator, container, or host vulnerability. Binary functional coverage does not establish
physical timing, FPGA operation, or all unknown/high-impedance input behavior. Package
versions from Ubuntu repositories can change even though the base image digest is pinned.

## Sequential-logic practice

[Synchronous counter example](examples/synchronous-counter) adds an 8-bit register with
reset/load/enable/hold priority and 2,048 systematically checked state/control transitions.
It is an AI-assisted learning reference, separate from the three Harbor tasks.

See [the learning guide](docs/learning-guide.md) for the concepts to understand and
[verification notes](docs/verification.md) for the runner and regression coverage.

## Layout

Each task has `instruction.md`, `task.toml`, `environment/Dockerfile`,
`environment/workspace/`, `solution/solve.sh`, and `tests/test.sh` plus its grader.
The Docker build context is `environment/`. Solutions and tests are kept out of that
context. Personal planning files are not part of the published portfolio.

## License

MIT; see [LICENSE](LICENSE). Third-party simulators retain their respective licenses.
