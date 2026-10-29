# Clocked counter practice reference

An AI-assisted learning example added alongside the combinational benchmark tasks.
It is not a completed microprocessor or a separate commercial benchmark task.

The 8-bit register changes on rising clock edges only. Priority is synchronous reset,
then parallel load, then increment when enabled, otherwise hold. Incrementing 255 wraps
to zero. Power-on state is intentionally unspecified; apply reset before use.

`counter_tb.vhd` checks all 256 prior states and all eight reset/load/enable combinations
(2,048 transitions), with loads varied across that space. Assertions also check load
seeding, stable outputs before a rising edge, and no change on a falling edge. This is
systematic transition coverage, not every possible input history or FPGA timing proof.

The root `run_all_checks.sh` runs this example and negative mutations that break
reset synchronization, control priority, and increment behavior.

Before presenting this as a skill, explain why omitting the last `else` inside this
clocked process creates a register hold, whereas an incomplete combinational process
can infer a latch. Then change the width or priority and update the verification.
