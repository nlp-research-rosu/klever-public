# Auditor command ledger

All commands below ran against read-only mounts or scratch copies. The stated
directory is the working directory for the command. Terminal logs preserve the
bounded stdout/stderr and their `COMMAND_EXIT_CODE`.

| Purpose | Working directory | Exact command | Exit | Log/artifact |
|---|---|---|---:|---|
| Provenance/integrity | `/audit-output` | `python3 /audit-output/evidence/provenance_check.py` | 0 | `provenance-check.log` |
| Trusted regeneration | `/audit-output` | `python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/reconstruction/regenerated-solution.mpy; translator_exit=$?; cmp /tmp/audit-work/reconstruction/regenerated-solution.mpy /candidate/solution.mpy; cmp_exit=$?; sha256sum /tmp/audit-work/reconstruction/regenerated-solution.mpy /candidate/solution.mpy; printf "translator_exit=%s cmp_exit=%s\n" "$translator_exit" "$cmp_exit"; test "$translator_exit" -eq 0 -a "$cmp_exit" -eq 0` | 0 | `translation-identity.log`, `regenerated-solution.mpy` |
| Differential test | `/audit-output` | `python3 /audit-output/evidence/differential_test.py` | 0 | `differential-test.log` |
| Tool versions | `/audit-output` | `command -v kup; kup_status=$?; command -v kompile; command -v krun; command -v kprove; kompile --version; kompile_status=$?; kprove --version; kprove_status=$?; printf "kup_status=%s kompile_status=%s kprove_status=%s\n" "$kup_status" "$kompile_status" "$kprove_status"; test "$kompile_status" -eq 0 -a "$kprove_status" -eq 0` | 0 | `toolchain-version.log` |
| Auditor concrete translation | `/tmp/audit-work/reconstruction` | `python3 py2mpy.py auditor_concrete.py > auditor_concrete.mpy` | 0 | `auditor_concrete.py`, `auditor_concrete.mpy` |
| Clean LLVM build | `/tmp/audit-work/reconstruction` | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition auditor-runtime-kompiled` | 0 | `llvm-kompile.log` |
| Concrete execution | `/tmp/audit-work/reconstruction` | `krun auditor_concrete.mpy --definition auditor-runtime-kompiled --output pretty` | 0 | `llvm-concrete-with-ground-witness.log` |
| Clean Haskell build | `/tmp/audit-work/reconstruction` | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition auditor-verification-kompiled -I .` | 0 | `haskell-kompile.log` |
| All positive claims | `/tmp/audit-work/reconstruction` | `kprove spec.k --definition auditor-verification-kompiled --spec-module SPEC --output pretty` | 0, `#Top` | `kprove-all-positive.log` |
| Explicit both-label selection | `/tmp/audit-work/reconstruction` | `kprove spec.k --definition auditor-verification-kompiled --spec-module SPEC --claims SPEC.incr-loop,SPEC.incr-list --output pretty` | 0, `#Top` | `kprove-both-labeled.log` |
| Loop claim selection | `/tmp/audit-work/reconstruction` | `kprove spec.k --definition auditor-verification-kompiled --spec-module SPEC --claims SPEC.incr-loop --output pretty` | 0, `#Top` | `kprove-incr-loop.log` |
| Ground satisfying witness | `/tmp/audit-work/reconstruction` | `kprove ground-witness.k --definition auditor-verification-kompiled --spec-module GROUND-WITNESS --output pretty` | 0, `#Top` | `kprove-ground-witness.log`, `ground-witness.k` |
| Constructor identity, first syntax attempt | `/tmp/audit-work/reconstruction` | `kprove program-identity.k --definition auditor-verification-kompiled --spec-module PROGRAM-IDENTITY --output pretty` | 113, parser error | `kprove-program-identity.log` |
| Constructor identity, unsupported functional-claim attempt | `/tmp/audit-work/reconstruction` | `kprove program-identity.k --definition auditor-verification-kompiled --spec-module PROGRAM-IDENTITY --output pretty` | 113, no backend claim | `kprove-program-identity-rerun.log` |
| Constructor identity, configuration form | `/tmp/audit-work/reconstruction` | `kprove program-identity.k --definition auditor-verification-kompiled --spec-module PROGRAM-IDENTITY --output pretty` | 0, `#Top` | `kprove-program-identity-config.log`, `program-identity.k` |
| Body mutation build | `/tmp/audit-work/body-mutation` | `diff -u /tmp/audit-work/reconstruction/verification.k verification.k; diff_status=$?; printf "expected_diff_status=%s\n" "$diff_status"; kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutated-kompiled -I .` | 0 (expected `diff` status 1, build 0) | `body-mutation-build.log`, `body-mutated-verification.k` |
| Body sensitivity | `/tmp/audit-work/body-mutation` | `kprove spec.k --definition body-mutated-kompiled --spec-module SPEC --output pretty` | 1, expected stuck claim | `body-mutation-kprove.log` |
| Directive inventory | `/audit-output` | `python3 /audit-output/evidence/rule_inventory.py` | 0 | `rule-inventory.log` |
| False mutation dry run | `/tmp/audit-work/reconstruction` | `kprove spec-vacuity.k --definition auditor-verification-kompiled --spec-module SPEC-VACUITY --dry-run --output pretty` | 0 | `vacuity-dry-run.log`, `spec-vacuity.k` |
| False mutation proof | `/tmp/audit-work/reconstruction` | `kprove spec-vacuity.k --definition auditor-verification-kompiled --spec-module SPEC-VACUITY --output pretty` | 1, expected stuck claim | `vacuity-kprove.log` |

Exploratory identity attempts that were rejected by the frontend/backend were
not treated as evidence. The final configuration-form identity claim is the
successful mechanical check. Selecting `SPEC.incr-list` alone was also abandoned
because that filter removes its declared `incr-loop` dependency; the complete
and explicit two-label runs above are the valid target-proof commands.
