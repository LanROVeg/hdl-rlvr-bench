# Tune a passive RC low-pass filter

Change **R1 only** in `/workspace/filter.cir` so the passive single-pole low-pass filter
has its cutoff at 1 kHz. Keep `V1 in 0 AC 1.0`, `R1 in out <value>` and
`C1 out 0 100nF`; finish the netlist with `.end`.

Acceptance criteria, each measured by the verifier:

- DC voltage gain: 0 dB +/-0.1 dB (a true DC operating-point sweep, not a 10 Hz proxy).
- Gain at 1,000 Hz: -3.01029995664 dB +/-0.1 dB.
- Phase at 1,000 Hz: -45 degrees +/-2 degrees.

R1 must be a finite positive literal between 1 ohm and 1 Gohm. Decimal, scientific
notation, and SPICE engineering suffixes are accepted (for example `1591.55` or
`1.59155k`). C1 stays 100 nF and the AC source stays 1 V. Blank lines and `*` comments
are allowed. The starter's `.ac dec 10 10 100k` and `.print ac vm(out) vp(out)` lines
may stay or be omitted. Other directives, components, expressions, `.control`, `.include`,
and file access are outside the task. Maximum input size: 16 KiB.

The verifier reads the allowed values and reconstructs its own circuit; it never executes
submitted control commands or trusts submitted measurement text. Score: 0.20 for a valid
submission and successful simulations, 0.20 for DC gain, 0.30 for cutoff gain, 0.30 for phase.
