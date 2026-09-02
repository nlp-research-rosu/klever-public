# Auditor command manifest

All commands ran from `/tmp/audit-work/37-sort-even` unless noted. The linked
logs contain bounded stdout/stderr. Status is the status of the substantive
command, not an `expected failure` wrapper.

| Stage | Exact command | Status | Relevant result/log |
|---|---|---:|---|
| 1 | `python3 /audit-output/evidence/integrity_check.py` | 0 | All required records/hashes and recursive supplied-semantics comparison passed; `stage1-integrity.log`. |
| 1 | `python3 /audit-output/evidence/inspect_generation_records.py` | 0 | All JSON/text/trace records were read; trace had 672 valid JSONL records and no parse errors; `stage1-generation-records.log`. |
| 2 | `python3 py2mpy.py solution.py > regenerated-solution.mpy` | 0 | Trusted regeneration succeeded; `stage2-regeneration.log`. |
| 2 | `cmp -s regenerated-solution.mpy solution.mpy` | 0 | Byte identity; both SHA-256 values `c25e5d64b696017be3aa254ddf81cecdb15f4ddf770c164a9c197e2773535280`; `stage2-regeneration.log`. |
| 2 | `python3 /audit-output/evidence/differential_test.py` | 0 | 24,543 cases, zero mismatches; `stage2-differential.log`. |
| 3 | `kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | 0 | Fresh concrete definition; `stage3-kompile-llvm.log`. |
| 3 | `krun audit-smoke.mpy --definition runtime-kompiled` | 0 | `.K`, `NoExc`, exit code 0 after six explicit assertions; `stage3-krun-smoke.log`. |
| 3 | `kompile --backend haskell verification.k --main-module VERIFICATION-NO-BRIDGE --syntax-module MPY-SYNTAX --output-definition verification-no-bridge-kompiled` | 0 | Fresh bridge-free definition; `stage3-kompile-no-bridge.log`. |
| 3 | `kprove spec-connection.k --definition verification-no-bridge-kompiled --spec-module SPEC-CONNECTION` | 0 | `#Top`; `stage3-kprove-connection.log`. |
| 3 | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | 0 | Fresh proof definition; `stage3-kompile-verification.log`. |
| 3 | `kprove spec.k --definition verification-kompiled --spec-module SPEC` | 0 | `#Top`, proving both target claims together; `stage3-kprove-target-all.log`. |
| 3 | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.loop-inv` | 0 | `#Top` for the selected loop claim; `stage3-kprove-loop-inv.log`. |
| 4 | `python3 /audit-output/evidence/program_identity.py` | 0 | Trusted byte identity plus constructor-level function/body identity; `stage4-program-identity.log`. |
| 4 | `kprove audit-witness.k --definition verification-kompiled --spec-module AUDIT-WITNESS` | 0 | `#Top` for explicit `[5,6,3,4] -> [3,6,5,4]`; `stage4-kprove-witness.log`. |
| 4 | `kompile --backend haskell verification-body-mutated.k --main-module VERIFICATION-NO-BRIDGE --syntax-module MPY-SYNTAX --output-definition verification-body-mutated-kompiled` | 0 | Mutated definition built; `stage4-kompile-body-mutation.log`. |
| 4 | `kprove audit-body-connection.k --definition verification-body-mutated-kompiled --spec-module AUDIT-BODY-CONNECTION` | 1 (expected) | `WarnStuckClaimState`; residual contrasts writes at `2*I+1` and `2*I`; `stage4-kprove-body-mutation.log`. |
| 5 | `python3 /audit-output/evidence/rule_inventory.py` | 0 | Generated `rule-inventory.md`: 232 syntax declarations and 702 rules, plus contexts/configuration/claims. |
| 5 | `python3 /audit-output/evidence/bridge_context_check.py` | 0 | Complete bridge/theorem region identity and no-bridge import isolation; `stage5-bridge-context.log`. |
| 5 | `krun audit-k-differential.mpy --definition runtime-kompiled --output none` | 0 | 26 explicit-oracle K cases, zero failed assertions; `stage5-k-differential.log`. |
| 5 | same K differential command with a superseded 134-assertion input | 137 | Parser process was killed by the 8 GB limit before execution; retained as `stage5-k-differential-oversized.log` and not treated as candidate evidence. |
| 6 | `kprove audit-false-result.k --definition verification-kompiled --spec-module AUDIT-FALSE-RESULT --dry-run` | 0 | Fresh mutation parses/builds; `stage6-false-mutation-build.log`. |
| 6 | `kprove audit-false-result.k --definition verification-kompiled --spec-module AUDIT-FALSE-RESULT` | 1 (expected) | `WarnStuckClaimState`; residual heap contains `[3,8,9]`, not demanded `[9,8,3]`; `stage6-false-mutation-proof.log`. |
