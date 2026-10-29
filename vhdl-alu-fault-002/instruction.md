# Task: RTL Silicon Bug Triage — 8-Bit ALU (NZVC)

The existing VHDL implementation in `/workspace/alu_8b.vhd` compiles cleanly in GHDL, but fails functional verification across several opcodes and status flags (`NZVC`).

Audit `/workspace/alu_8b.vhd` against the specification below, identify all functional and flag-generation bugs, and patch the file in-place.

## Target Specification
- `ALU_Sel = "000"`: `A + B` with signed two's complement overflow (`V = NZVC(1)`) and unsigned carry (`C = NZVC(0)`).
- `ALU_Sel = "001"`: `A - B` with signed two's complement overflow (`V`) and unsigned borrow (`C = '1'` when `unsigned(A) < unsigned(B)`).
- `ALU_Sel = "010"`: Bitwise `A and B` (`V = '0', C = '0'`).
- `ALU_Sel = "011"`: Bitwise `A or B` (`V = '0', C = '0'`).
- `ALU_Sel = "100"`: Bitwise `A xor B` (`V = '0', C = '0'`).
- `ALU_Sel = "101"`: Logical Shift Left `A` by 1 bit (`C = A(7)`).
- `ALU_Sel = "110"`: Logical Shift Right `A` by 1 bit (`C = A(0)`).
- `ALU_Sel = "111"`: Pass `A` unchanged (`V = '0', C = '0'`).
- `N = NZVC(3)`: Always equals `Result(7)`.
- `Z = NZVC(2)`: `'1'` if and only if `Result = x"00"`.


## Submission and verification contract
Submit one self-contained `alu_8b` entity in `/workspace/alu_8b.vhd` (maximum 64 KiB).
Use only `ieee.std_logic_1164.all` and optionally `ieee.numeric_std.all`.
The design must synthesize in GHDL without inferred latches and be purely combinational.
File I/O, foreign interfaces, external names, configurations, and additional entities are
outside this task. The verifier synthesizes the source and simulates only the resulting
combinational netlist. It checks all 524,288 binary A/B/opcode combinations.
Score: 0.20 for an accepted synthesized design, 0.40 for correct result values, and
0.40 for correct flags gated on a correct result. Invalid or incomplete runs receive zero.
