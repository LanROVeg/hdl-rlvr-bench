# HDL and SPICE verification exercises

[![Checks](https://github.com/LanROVeg/hdl-rlvr-bench/actions/workflows/checks.yml/badge.svg)](https://github.com/LanROVeg/hdl-rlvr-bench/actions/workflows/checks.yml)

Three small EE exercises with automated grading:

- **ALU design:** implement an 8-bit combinational ALU with NZVC flags.
- **ALU debugging:** fix a different starter against the same ALU specification.
- **RC filter:** choose a resistor for a 1 kHz low-pass filter with a fixed 100 nF capacitor.

The VHDL tasks use GHDL. The circuit task uses Ngspice. Python handles grading,
Docker provides the environments, and Harbor 0.25.0 runs the tasks end to end.

## Run the checks

Use Linux or WSL2 with Python 3.12+, Docker Engine, and Docker Compose.

```bash
bash run_all_checks.sh

# Also run the tasks through the pinned Harbor runner.
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
bash run_all_checks.sh --harbor
```

The runner builds each task image, checks the starters and reference solutions,
and tries broken and invalid submissions. No model API key is needed. Results go
in the ignored `check-results/` directory; CI uploads the same results.

## How grading works

The ALU verifier synthesizes the submitted RTL and checks the resulting netlist
against all **524,288 binary A/B/opcode combinations**. Clocked logic and feedback
are rejected. Flags earn credit only when the result is also correct. Reports
printed by a submission do not supply scores.

The RC verifier reads the allowed component values and builds its own circuit.
It checks true DC gain, magnitude at 1 kHz, and phase at 1 kHz. Submitted SPICE
control commands are not executed.

Harbor transfers only the declared source file into a separate verifier container.
`reward.json` and `reward.txt` contain the score; `details.json` explains the result.
Each task's `instruction.md` gives the exact interface, restrictions, and scoring.

Reference solutions score **1.0**. The starter scores are **0.206569**, **0.699216**,
and **0.4** for tasks 001, 002, and 003. See [verification notes](docs/verification.md)
for the reproduced runs, negative cases, and limits of these checks.

This is an undergraduate learning project. Exhaustive binary simulation does not
establish FPGA timing or board operation, and the grader is not a general sandbox
for arbitrary HDL or SPICE programs. The tasks have not been used to measure model
difficulty. AI tools helped with development and verification; the
[learning guide](docs/learning-guide.md) explains the underlying concepts.

There is also a [synchronous counter practice example](examples/synchronous-counter),
separate from the three tasks.

MIT license; see [LICENSE](LICENSE).
