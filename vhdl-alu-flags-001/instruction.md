# Task: 8-Bit Combinational ALU with Status Flags (NZVC)

Complete the synthesizable VHDL entity `alu_8b` located in `/workspace/alu_8b.vhd`.

## Port Specification
- `A` : `in std_logic_vector(7 downto 0)`
- `B` : `in std_logic_vector(7 downto 0)`
- `ALU_Sel` : `in std_logic_vector(2 downto 0)`
- `Result` : `out std_logic_vector(7 downto 0)`
- `NZVC` : `out std_logic_vector(3 downto 0)` — Mapped as `NZVC(3) = N`, `NZVC(2) = Z`, `NZVC(1) = V`, `NZVC(0) = C`

## Required Operations (`ALU_Sel`)
| `ALU_Sel` | Operation | `V` (Signed Overflow) | `C` (Carry / Borrow Flag) |
| :--- | :--- | :--- | :--- |
| `"000"` | `A + B` | `'1'` if signed 2's complement overflow occurs, else `'0'` | `'1'` if unsigned carry out of bit 7 occurs, else `'0'` |
| `"001"` | `A - B` | `'1'` if signed 2's complement overflow occurs, else `'0'` | `'1'` if unsigned borrow occurs (`unsigned(A) < unsigned(B)`), else `'0'` |
| `"010"` | `A and B` | `'0'` | `'0'` |
| `"011"` | `A or B` | `'0'` | `'0'` |
| `"100"` | `A xor B` | `'0'` | `'0'` |
| `"101"` | Logical Shift Left `A` by 1 (`A(6 downto 0) & '0'`) | `'0'` | `A(7)` |
| `"110"` | Logical Shift Right `A` by 1 (`'0' & A(7 downto 1)`) | `'0'` | `A(0)` |
| `"111"` | Pass `A` unchanged | `'0'` | `'0'` |

## Flag Rules (All Operations)
- `N` (`NZVC(3)`): Always equals MSB of the computed result (`Result(7)`).
- `Z` (`NZVC(2)`): `'1'` when `Result = x"00"`, else `'0'`.
- Purely combinational logic required (no clock, no inferred latches).
- You may use `ieee.numeric_std.all` and `ghdl -a --std=08 alu_8b.vhd` to test compilation.

## Submission and verification contract
Submit one self-contained `alu_8b` entity in `/workspace/alu_8b.vhd` (maximum 64 KiB).
Use only `ieee.std_logic_1164.all` and optionally `ieee.numeric_std.all`.
The design must synthesize in GHDL without inferred latches and be purely combinational.
File I/O, foreign interfaces, external names, configurations, and additional entities are
outside this task. The verifier synthesizes the source and simulates only the resulting
combinational netlist. It checks all 524,288 binary A/B/opcode combinations.
Score: 0.20 for an accepted synthesized design, 0.40 for correct result values, and
0.40 for correct flags gated on a correct result. Invalid or incomplete runs receive zero.
