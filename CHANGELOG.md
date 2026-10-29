# Changes

## October 29, 2026 — verification and portfolio cleanup

- Replaced score-message parsing with exhaustive checks of synthesized ALU netlists.
- Reconstructed the RC circuit from allowed values instead of executing submitted programs.
- Matched prompt and grader tolerances; separated numeric reward files from diagnostics.
- Moved starter assets inside real environment/ build contexts and removed duplicate roots.
- Adopted Harbor 0.25.0/schema 1.3 with separate verifier containers and explicit artifacts.
- Added regression checks, CI, an AI-assisted clocked-counter practice reference, and a
  concept guide. Corrected published baseline values using reproduced runs.
- Removed personal planning material from the current published tree and added MIT licensing.

Removing a file from the current tree does not erase earlier Git history. This release
does not rewrite history or claim that material previously published has become private.
