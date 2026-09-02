# Auditor evidence index

- `audit_integrity.py`, `stage1-integrity.log`: launcher records, hashes,
  campaign equality, regular-file/type checks, recursive semantics identity,
  candidate workspace binding, and complete JSONL parsing.
- `generation_record_summary.py`, `generation-record-summary.log`: full
  structured-record read and untrusted generation claim/tool summary.
- `source_fidelity.py`, `source-fidelity.log`: canonical/candidate signature
  and behavior-AST identity after removing the canonical docstring.
- `translation.log`: trusted regeneration and byte comparison with submitted
  `solution.mpy`.
- `differential_test.py`, `differential-test.log`,
  `differential-results.json`: 259 deterministic canonical comparisons with
  complete input/output records.
- `toolchain.log`, `llvm-build.log`, `haskell-build.log`: observed K 7.1.293
  and fresh source builds.
- `runtime_cases.py`, `krun-solution.log`, `krun-runtime-cases.log`: fresh
  concrete executions.
- `kprove-target.log`: independent run of the sole required positive claim.
- `solution.kast.json`, `spec-claims.json`, `spec-dry-run.log`,
  `program_pinning_check.py`, `program-pinning.log`: parsed constructor-level
  program identity and claim metadata.
- `concrete-substitution.k`, `concrete-substitution.log`: satisfiable
  precondition witness `CS=[65]`, K result `[97]`, and both Python results.
- `body-sensitivity.k`, `body-sensitivity.log`: actual executed-body mutation,
  successful dry build, and expected proof rejection.
- `rule_inventory.py`, `rule-inventory.tsv`, `rule-inventory-summary.txt`,
  `rule-inventory.log`, `static-soundness-analysis.md`,
  `proof-definition-slice.log`: exhaustive declaration/rule inventory and
  theorem-slice soundness review.
- `spec-auditor-vacuity.k`, `non-vacuity.log`: fresh false-result mutation,
  successful dry build, and stuck residual at the true result.
- `model-gap-witness.k`, `kprove-model-gap.log`,
  `model-gap-cpython-result.k`, `model_gap_python.py`,
  `model-gap-comparison.log`: independent supplied-model/CPython divergence
  witnesses.
- `scratch-copy.log`: bounded inventory of source-only scratch inputs.
