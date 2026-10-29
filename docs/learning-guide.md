# Explain the work before presenting it

This is a study guide, not interview answers to read during an assessment. Follow each
platform's rules on tools and outside assistance. The reference examples and verification
code were developed with AI assistance; work through the questions and changes yourself.

## Combinational ALU

- A combinational output depends on current inputs, without stored clocked state.
- Unsigned carry and signed overflow answer different questions. Work through 255+1,
  127+1, 128-1, and 5-10 using both number interpretations.
- This benchmark defines subtraction C as **borrow**, meaning A < B. Other architectures
  can define C differently, so read the specification.
- Explain why shift-left C uses the old most-significant bit and shift-right C the old
  least-significant bit. Explain why flags depend on the computed result.
- Incomplete combinational assignments can infer latches. The verifier requires a GHDL
  synthesized combinational netlist and rejects runtime constructs in that netlist.
- Explain what exhaustive binary testing covers and what it leaves out: unknown values,
  physical propagation delay, routed timing, and arbitrary malicious tool vulnerabilities.

Practice: change one carry or overflow rule in a temporary copy, run the checks, and explain
which inputs expose the defect. The two VHDL tasks share a contract but different starters;
they are not two independent demonstrations of algorithmic complexity.

## Clocked counter

Read `examples/synchronous-counter/`. Sketch the next count for reset, load, increment,
and hold. Explain why reset is synchronous and why changing reset between rising edges
must not immediately change q. Explain how the testbench catches an asynchronous reset.

Practice: change priority deliberately or increment by two, then predict the failure
before running the test. Extend the counter width yourself and update ports and tests.
Do not call the unfinished coursework microprocessor a working CPU.

## RC response

For the passive low-pass, H(jw) = 1/(1+jwRC) and fc = 1/(2*pi*R*C). With C=100 nF and
fc=1 kHz, R is approximately 1591.55 ohms. At cutoff the magnitude is 1/sqrt(2), or
-3.0103 dB, and phase is -45 degrees. Explain why the DC gain is one and why 10 Hz is
only an approximation to DC. Explain 20*log10(voltage ratio) versus 10*log10(power ratio).

Practice: halve R and predict the cutoff and response at 1 kHz. Describe why a verifier
must reconstruct the circuit instead of believing measurement rows printed by a submission.

## Reproducibility and honest scope

Explain environment versus verifier containers, explicit artifact transfer, NOP versus
oracle checks, and why a reference score of one does not measure frontier-model difficulty.
Be able to run the checks and find `reward.json`, `reward.txt`, and separate diagnostics.

Use AI for learning and development where permitted. An asynchronous assignment is not
permission to automate its work or send private task content to external tools. Read the
specific project's rules before using tools, tracking time, or accepting work.
