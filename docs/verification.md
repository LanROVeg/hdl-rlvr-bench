# Verification contract and regression coverage

Validated runner: `harbor==0.25.0`; task schema: 1.3. The task configurations declare
unique registry names, explicit source artifacts, no-network execution, resource limits,
and separate verifier containers. This avoids inheriting modified tools from the agent.

Run `bash run_all_checks.sh` for clean environment-context builds and container checks.
Add `--harbor` after installing `requirements-dev.txt` for actual NOP/oracle jobs. This
uses local Docker and the built-in NOP/oracle agents; it does not invoke a paid model.

## Required regression outcomes

- Every reference gets 1.0 and every starter stays below 1.0.
- VHDL score-report injection cannot increase the starter's score. The behavior is
  synthesized before simulation, and counts come only from the trusted generated bench.
- An incorrect flag implementation loses functional credit.
- Inferred latches and clocked designs get zero. Synthesized signal dependencies
  must be acyclic, including dependencies in selected-assignment selectors.
- Missing or malformed source gets zero, and score files contain finite bounded numbers.
- SPICE fabricated measurements, include directives, nonfinite values, and changed fixed
  topology get zero. Only verifier-owned simulation data is measured.
- The clocked-counter reference passes; wrong increment, asynchronous reset, and wrong
  priority must fail with assertions. There are 2,048 state/control transitions.

## Reproduced on October 29, 2026

The 19 task-level regression cases passed. All three actual Harbor NOP trials and all
three actual Harbor oracle trials completed without exceptions. Oracle rewards were all
1.0; NOP rewards were 0.206569, 0.699216, and 0.4 for tasks 001, 002, and 003 respectively.
The counter reference and its three negative mutations also passed their expected checks.

## Reproduced on November 1, 2026

All 38 task-level regression cases passed, plus the counter reference and three negative
mutations. The six actual Harbor trials also passed with the same NOP and oracle rewards
listed above. Previous job results were left in the output directories during this run;
the runner correctly validated only the newly created jobs.

The RC cases cover engineering suffixes, scientific notation, wrong resistance, fabricated
output, changed topology, includes, nonfinite/overflow/negative values, duplicate components,
oversized source, and a missing file. Each VHDL task checks its starter and reference,
`process(all)`, a forged count report, wrong flags, wrong shift carry, an inferred variable
latch, a clocked design, an extra entity, oversized source, syntax errors, and a missing file.

The variable-latch case exposed a real gap: GHDL can express storage as feedback between
concurrent assignments, with no process block in its output. The verifier now rejects such
cycles. It accepts basic identifiers in the synthesized netlist and fails closed on extended
identifiers, rather than guessing how to parse them.

## Limitations

The ALU test space is exhaustive for binary inputs **after synthesis**. It is not a claim
of exhaustive analog timing, unknown-value semantics, or synthesis equivalence under every
possible behavioral construct. Accepted submissions are self-contained, synthesizable
numeric_std RTL within the prompt's restrictions. Unsupported source constructs fail closed.

The RC exercise intentionally restricts the topology; it does not accept arbitrary SPICE
programs or evaluate transistor-level analog design. A separate verifier and allowlisted
reconstruction reduce known reward-hacking paths; they do not establish universal security.

The base Ubuntu digest and Harbor version are pinned. Ubuntu repository dependencies are
installed at build time and are not a full immutable package snapshot. Save image digests
and logs if exact archival reproduction is required. CI results are available on GitHub
Actions; local detailed logs live under ignored `check-results/`.
