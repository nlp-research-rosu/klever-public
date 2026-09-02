# Audit evidence

Each `.log` file records shell tracing (`+ command`), combined standard output/error, and relevant exit-status checks for the independently rerun audit command named by the file. JSON evidence is emitted directly by the trusted checker or by a read-only inspection command recorded in the adjacent log.

Authoritative successful reruns are:

- Stage 3: `reconstructed-inventory.json`, `inventory-bijection.log`, and `independent-classification.md`.
- Stage 4: `producer-authentication-corrected.log`, `check-generation-proc-compat.log`, `independent-generation-audit.log`, and `mathematical-obligation-review.md`.
- Stage 5: `fresh-copy-corrected.log`, `lake-clean.log`, `lake-build.log`, `candidate-integrity-check.log`, `print-axioms-direct.log`, `axiom-reconciliation.log`, `operational-adversarial-tests.log`, and `operational-bridge-review.md`.

Earlier Stage 4 app-path experiments and the first `check-generation.log` are deliberately retained as raw diagnostics. They document the container `/proc/<pid>/exe` incompatibility and are superseded by the pinned-toolchain `/proc/self/exe` compatibility rerun. Likewise, `stage5/fresh-copy.log` records a first copy that nested `generated/` under the candidate's pre-existing empty `Base`; `fresh-copy-corrected.log` is the exact corrected copy. `print-axioms.log` records why `lake env` reordering masked the compatibility library; `print-axioms-direct.log` is the exact successful Lean run with Lake's resolved paths. No read-only mounted artifact was modified.
