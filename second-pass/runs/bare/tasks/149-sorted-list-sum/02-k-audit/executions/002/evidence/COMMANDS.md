# Audit command ledger

All commands were run from `/audit-output` unless a different working
directory is shown. `script -q -e -c ... LOG` was used to preserve bounded
stdout/stderr; each log footer records `COMMAND_EXIT_CODE`.

| Purpose | Exact command (inside the recorder) | Working directory | Exit |
|---|---|---|---:|
| Toolchain | `kompile --version && kprove --version && krun --version && python3 --version` | `/audit-output` | 0 |
| Provenance | `python3 evidence/provenance_check.py` | `/audit-output` | 0 |
| Translation/program generation identity | `python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy && cmp regenerated-solution.mpy solution.mpy && python3 make_solution_k.py > regenerated-solution-program.k && cmp regenerated-solution-program.k solution-program.k && sha256sum solution.py solution.mpy regenerated-solution.mpy solution-program.k regenerated-solution-program.k` | `/tmp/audit-work/reconstruction` | 0 |
| Python differential | `python3 /audit-output/evidence/differential_test.py` | `/tmp/audit-work/reconstruction` | 0 |
| Fresh LLVM build | `kompile semantic.k --main-module MPY-SEMANTIC --syntax-module MPY-SYNTAX --backend llvm --output-definition concrete-kompiled -w none` | `/tmp/audit-work/reconstruction` | 0 |
| Fresh Haskell proof build | `kompile verification.k --main-module SORTED-LIST-VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition proof-kompiled -w none` | `/tmp/audit-work/reconstruction` | 0 |
| Concrete ASCII/boundary executions | `bash /audit-output/evidence/concrete_semantics_tests.sh` | `/tmp/audit-work/reconstruction` | 0 |
| Every positive claim separately | `bash /audit-output/evidence/prove_each_claim.sh` | `/tmp/audit-work/reconstruction` | 0 |
| Satisfying claim witnesses | `python3 evidence/claim_witnesses.py` | `/audit-output` | 0 |
| Constructor-level pinning | `python3 evidence/program_pinning.py` | `/audit-output` | 0 |
| Unicode semantic witnesses (both backends) | `bash /audit-output/evidence/unicode_semantics_mismatch.sh` | `/audit-output` | 0 (confirmed expected discrepancies) |
| Body sensitivity | `bash /audit-output/evidence/body_sensitivity_test.sh` | `/audit-output` | 0 wrapper; mutation build 0; mutated proof 1 as expected |
| Fresh false-result mutation | `bash /audit-output/evidence/nonvacuity_test.sh` | `/audit-output` | 0 wrapper; dry run 0; mutated proof 1 as expected |
| Source inventory | `python3 evidence/k_source_inventory.py` | `/audit-output` | 0 |

The positive-claim script invoked, once each:

```text
kprove spec.k --definition /tmp/audit-work/reconstruction/proof-kompiled
  --spec-module SPEC --claims <LABEL> --output pretty -w none
```

for `universal-correctness`, `base`, `symbolic-two`,
`symbolic-two-reverse`, `symbolic-three`, `prompt-example-one`, and
`prompt-example-two`. Every invocation exited 0 and printed exactly `#Top`.

The non-vacuity dry-run and proof commands were:

```text
kprove /audit-output/evidence/spec-vacuity-audit.k
  --definition /tmp/audit-work/reconstruction/proof-kompiled
  --spec-module SPEC-VACUITY-AUDIT --dry-run
  -I /tmp/audit-work/reconstruction -w none

kprove /audit-output/evidence/spec-vacuity-audit.k
  --definition /tmp/audit-work/reconstruction/proof-kompiled
  --spec-module SPEC-VACUITY-AUDIT --output pretty
  -I /tmp/audit-work/reconstruction -w none
```
