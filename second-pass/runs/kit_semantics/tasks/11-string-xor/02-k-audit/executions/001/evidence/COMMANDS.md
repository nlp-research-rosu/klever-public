# Reviewer command record

All mutation/build work used `/tmp/audit-work/reconstruction`; all candidate
compiled directories and caches were excluded. Logs linked below contain actual
bounded output and an explicit exit status.

| Purpose | Working directory | Exact command | Result |
|---|---|---|---|
| Toolchain | `/audit-output` | `kompile --version; kprove --version; krun --version; python3 --version` | K `7.1.293`, Python `3.10.12`, exit 0; `00-toolchain.log` |
| Provenance | `/audit-output` | `python3 /audit-output/evidence/provenance_check.py` | exit 0; `01-provenance.log` |
| Pipeline tree hashes | `/audit-output` | `python3 /audit-output/evidence/pipeline_tree_hash_check.py` | exit 0; `01-pipeline-tree-hashes.log` |
| Generation-record read/summary | `/audit-output` | `python3 /audit-output/evidence/generation_record_summary.py` | exit 0; `01-generation-record-summary.log` |
| Trusted translation | `/tmp/audit-work/reconstruction` | `python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/solution.regenerated.mpy` then `cmp -l solution.mpy solution.regenerated.mpy` | translator 0, `cmp` 0; `02-translation-identity.log` |
| Differential test | `/audit-output` | `python3 /audit-output/evidence/differential_test.py` | 66,036 checks, 0 mismatches, exit 0; `02-differential.log` |
| Concrete definition | `/tmp/audit-work/reconstruction` | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-fresh-kompiled` | exit 0; `03-kompile-runtime.log` |
| Bridge-free definition | `/tmp/audit-work/reconstruction` | `kompile verification.k --backend haskell --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition verification-base-fresh-kompiled` | exit 0; `03-kompile-verification-base.log` |
| Bridge-enabled definition | `/tmp/audit-work/reconstruction` | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-fresh-kompiled` | exit 0; `03-kompile-verification.log` |
| Bridge-free target proof | `/tmp/audit-work/reconstruction` | `kprove spec.k --definition verification-base-fresh-kompiled --spec-module LOOP-SPEC --claims LOOP-SPEC.loop-invariant` | `#Top`, exit 0; `03-kprove-loop.log` |
| Entry target proof | `/tmp/audit-work/reconstruction` | `kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC --claims SPEC.string-xor` | `#Top`, exit 0; `03-kprove-entry.log` |
| Concrete harness preparation | `/tmp/audit-work/reconstruction` | `python3 /reference/py2mpy.py /audit-output/evidence/reviewer_concrete.py > /tmp/audit-work/reconstruction/reviewer_concrete.mpy` plus AST identity check | exit 0; `03-concrete-harness-prep.log` |
| Fixed concrete execution | `/tmp/audit-work/reconstruction` | `krun reviewer_concrete.mpy --definition runtime-fresh-kompiled --output none` | exit 0; `03-krun-runtime-concrete.log` |
| Bridge concrete execution | `/tmp/audit-work/reconstruction` | `krun reviewer_concrete.mpy --definition verification-fresh-kompiled --output none` | exit 0; `03-krun-verification-concrete.log` |
| Ground witnesses | `/tmp/audit-work/reconstruction` | `kprove spec-ground.k --definition verification-fresh-kompiled --spec-module SPEC-GROUND` | `#Top`, exit 0; `04-kprove-ground.log` |
| Body sensitivity | `/tmp/audit-work/reconstruction` | `kprove spec-body-mutation.k --definition verification-base-fresh-kompiled --spec-module LOOP-SPEC-BODY-MUTATION` | expected `WarnStuckClaimState`, kprove exit 1; `04-kprove-body-sensitivity.log` |
| Constructor/bridge identity | `/tmp/audit-work/reconstruction` | `python3 /audit-output/evidence/static_artifact_checks.py` | exit 0; `04-static-artifact-checks.log` |
| Full K inventory | `/tmp/audit-work/reconstruction` | `python3 /audit-output/evidence/k_inventory.py` | 1,120 entries, exit 0; `05-k-inventory.log`, `k-rule-inventory.tsv` |
| Fixed continuation sensitivity | `/tmp/audit-work/reconstruction` | `kprove spec-continuation.k --definition verification-base-fresh-kompiled --spec-module CONTINUATION-SPEC-BASE` | `#Top`, exit 0; `05-continuation-base.log` |
| Bridge continuation sensitivity | `/tmp/audit-work/reconstruction` | `kprove spec-continuation.k --definition verification-fresh-kompiled --spec-module CONTINUATION-SPEC-BRIDGE` | `#Top`, exit 0; `05-continuation-bridge.log` |
| Fresh false-result mutation | `/tmp/audit-work/reconstruction` | `kprove spec-fresh-vacuity.k --definition verification-fresh-kompiled --spec-module SPEC-FRESH-VACUITY` | expected `WarnStuckClaimState`, kprove exit 1; audit check exit 0; `06-fresh-vacuity.log` |
