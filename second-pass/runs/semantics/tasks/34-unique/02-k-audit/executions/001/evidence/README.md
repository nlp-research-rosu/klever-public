# Audit evidence index

All commands ran against source copies in `/tmp/audit-work/34-unique`. Candidate
compiled output and caches were not used.

- `00-tool-versions.log`: K tool paths and versions.
- `01-provenance-integrity.log`: candidate/reference inventories, required-file
  presence, prompt/translator hashes, recursive supplied-semantics diff, and
  symlink check.
- `02-translator-regeneration.log`: trusted translator regeneration and byte
  identity check for `solution.mpy`.
- `differential_unique.py`, `differential-inputs.json`, and
  `03-python-differential.log`: independent canonical-versus-generated Python
  differential, exact corpus, and zero-mismatch result.
- `k_concrete_tests.py`, `04-k-test-translation.log`,
  `05-kompile-concrete.log`, and `06-krun-concrete.log`: reviewer-authored
  concrete K assertions and fresh LLVM execution.
- `07-kompile-proof.log`: fresh Haskell proof-definition build.
- `08-kprove-member-summary.log`, `11-kprove-loop-with-dependency.log`,
  `12-kprove-entry-with-dependencies.log`, and `13-kprove-all-claims.log`:
  dependency-preserving positive proof runs.
- `09-kprove-unique-loop.log`: explicitly excluded dependency-stripped
  diagnostic; its annotation records why it was interrupted.
- `inventory_k.py` and `10-k-rule-inventory.md`: exhaustive, line-bounded
  inventory of every syntax declaration, configuration, context, rule, and
  claim in the supplied K tree plus candidate proof files.
- `spec-vacuity.k`, `14-vacuity-dry-run.log`, and `15-vacuity-proof.log`:
  reviewer-authored false-result mutation; it builds and fails on `[1]`.
- `spec-ground-witnesses.k`, `17-ground-witnesses-dry-run.log`,
  `18-ground-member.log`, `19-ground-loop.log`, and
  `20-ground-literal-entry.log`: satisfying ground witnesses, including a
  literal submitted-AST entry execution. `16-ground-witnesses-dry-run.log`
  preserves an initial reviewer syntax error that was corrected before use.
- `spec-operational-sensitivity.k`, `21-operational-sensitivity-dry-run.log`,
  and `22-operational-sensitivity-proof.log`: body-sensitivity mutation; the
  mutated append-always loop reaches `[1,1]` and is rejected.
- `23-scratch-source-manifest.log`: scratch/candidate source identities,
  trusted-semantics scratch diff, and ignored cache inventory.
- `24-review-validation.log`: mechanical checks for all seven headings,
  positive `#Top`/exit signals, expected negative residuals, and exact terminal
  verdict markers.
- `25-evidence-checksums.log`: SHA-256 manifest for the completed review and
  preceding evidence artifacts.
- `run_logged.sh`: command wrapper that records work directory, shell-escaped
  command, output, and exit status.
