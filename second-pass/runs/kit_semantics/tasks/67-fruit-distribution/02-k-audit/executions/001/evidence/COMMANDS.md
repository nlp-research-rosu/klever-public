# Reviewer command record

All build/proof commands used source copies under `/tmp/audit-work/fruit67`;
no candidate-provided compiled directory or cache was used.

| Working directory | Exact command | Exit | Preserved output |
|---|---|---:|---|
| `/audit-output` | `/usr/bin/python3 /audit-output/evidence/stage1_integrity.py` | 0 | `stage1_integrity.log`: `STAGE1_INTEGRITY=PASS` |
| `/audit-output` | `/usr/bin/python3 /audit-output/evidence/trace_inventory.py` | 0 | `trace_inventory.log`: 212 JSONL records and all 43 tool calls inventoried |
| `/audit-output` | `/usr/bin/python3 /tmp/audit-work/fruit67/py2mpy.py /tmp/audit-work/fruit67/solution.py > /tmp/audit-work/fruit67/solution.regenerated.mpy` | 0 | `translation_regeneration.log` |
| `/audit-output` | `cmp -s /tmp/audit-work/fruit67/solution.regenerated.mpy /candidate/solution.mpy` | 0 | Both SHA-256 values are `280a1b9812a03c3679da3bf6dd8dc7be48f2c78769ec1a5ce6ff7b1ba73a5902` |
| `/audit-output` | `/usr/bin/python3 /audit-output/evidence/differential_test.py` | 0 | `differential_test.log`: 163 total cases, 0 in-domain mismatches, 5 excluded-probe divergences |
| `/tmp/audit-work/fruit67` | `/usr/bin/python3 py2mpy.py /audit-output/evidence/concrete_audit.py > concrete_audit.mpy` | 0 | Generated reviewer smoke program |
| `/tmp/audit-work/fruit67` | `kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition concrete-kompiled` | 0 | `kompile_llvm.log` |
| `/tmp/audit-work/fruit67` | `krun concrete_audit.mpy --definition concrete-kompiled` | 0 | `krun_concrete.log`: `.K`, `NoExc`, exit code 0 |
| `/tmp/audit-work/fruit67` | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | 0 | `kompile_haskell.log` |
| `/tmp/audit-work/fruit67` | `rg -n '^\s*claim\b' spec.k` | 0 | `positive_claim_inventory.log`: exactly one target claim |
| `/tmp/audit-work/fruit67` | `kprove spec.k --definition verification-kompiled --spec-module SPEC` | 0 | `kprove_positive.log`: `#Top` |
| `/audit-output` | `/usr/bin/python3 /audit-output/evidence/program_term_compare.py` | 0 | `program_term_compare.log`: identical normalized constructor trees |
| `/audit-output` | `/usr/bin/python3 /audit-output/evidence/precondition_witness.py` | 0 | `precondition_witness.log`: every guard true and both Python results 8 |
| `/tmp/audit-work/fruit67` | `kprove ground-witness.k --definition verification-kompiled --spec-module GROUND-WITNESS` | 0 | `kprove_ground_witness.log`: `#Top` |
| `/audit-output` | `/usr/bin/python3 /audit-output/evidence/rule_inventory.py` | 0 | `rule_inventory.tsv`: 929 inventoried/disposed sentences |
| `/tmp/audit-work/fruit67` | `kprove false-result.k --definition verification-kompiled --spec-module FALSE-RESULT --dry-run` | 0 | `false_result_dry_run.log`: successful parse/build command |
| `/tmp/audit-work/fruit67` | `kprove false-result.k --definition verification-kompiled --spec-module FALSE-RESULT` | 1 (expected) | `kprove_false_result.log`: `WarnStuckClaimState`, actual `<k> 8`, prover error |
| `/tmp/audit-work/fruit67` | `kprove body-sensitivity.k --definition verification-kompiled --spec-module BODY-SENSITIVITY` | 1 (expected) | `kprove_body_sensitivity.log`: `WarnStuckClaimState`, changed body returns `<k> 20` |

Tool versions in `tool_versions.log`: K `v7.1.293` for `kompile`, `krun`,
and `kprove`.
