# Audit evidence index

All executions used the source-only scratch tree at
`/tmp/audit-work/review-45-triangle-area-20260724`. Each `.log` begins with the
exact command and working directory and ends with `EXIT_STATUS`.

- `stage1-integrity.log`, `artifact-manifest.log`: provenance/type/hash checks
  and recursive supplied-semantics comparison.
- `cache-discard.log`: removal of copied candidate bytecode before import tests.
- `translation-regeneration.log`, `smoke-translation.log`: trusted-translator
  regeneration and byte comparisons.
- `program-fidelity.log`: source diff and AST dumps.
- `differential_triangle_area.py`, `differential.log`: 500-case independent
  canonical/generated differential; one preserved mismatch.
- `kompile-runtime.log`, `krun-smoke.log`,
  `krun-reviewer-cases.log`: clean LLVM build and concrete checks.
- `kompile-verification.log`, `kprove-positive.log`: clean Haskell build and
  the required positive proof (`#Top`, exit 0).
- `ground_witness_compare.py`, `ground-witness-compare.log`: satisfying
  substitution `A=5,H=3`.
- `spec-ground-witness.k`, `kprove-ground-witness.log`: optional ground
  specialization; it exposes the Haskell backend's unsupported concrete
  `Int2Float` hook and is not used as proof-success evidence.
- `inventory_k.py`, `k-rule-inventory.md`, `static-path-analysis.md`:
  exhaustive declaration/rule inventory and reachable-path assessment.
- `spec-vacuity-audit.k`, `vacuity-build.log`, `vacuity-proof.log`: fresh
  false-result mutation, successful dry build, and expected stuck proof.
- `concrete_huge_boundary.py`, `concrete_huge_boundary.mpy`,
  `python-huge-boundary.log`, `krun-huge-boundary.log`: Python exception versus
  normal K completion.
- `concrete_division_scaling_boundary.py`,
  `concrete_division_scaling_boundary.mpy`,
  `python-division-scaling-boundary.log`,
  `krun-division-scaling-boundary.log`: generated Python finite result versus
  supplied-semantics assertion failure at a large integer admitted by the
  claim.
- `run_logged.sh`: command/status capture helper.
