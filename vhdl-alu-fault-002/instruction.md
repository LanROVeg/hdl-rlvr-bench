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
