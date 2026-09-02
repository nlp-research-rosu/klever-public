# Audit command and status index

All candidate artifacts were read only. Builds and mutations ran in
`/tmp/audit-work/87-get-row`; reviewer artifacts and bounded logs are in this
directory. `script -q -e -c '<command>' <log>` was used to preserve output and
the command exit status in each log footer.

| Evidence | Working directory | Exact inner command | Exit | Relevant result |
|---|---|---|---:|---|
| `00_toolchain.log` | `/audit-output` | `kompile --version && kprove --version && python3 --version` | 0 | K 7.1.337; Python 3.10.12 |
| `01_provenance_check.log` | `/audit-output` | `bash /audit-output/evidence/01_provenance_check.sh` | 0 | prompt, translator, and supplied-semantics tree identical; four generation metadata files absent |
| `02_retranslation_check.log` | `/audit-output` | `bash /audit-output/evidence/02_retranslation_check.sh` | 0 | trusted retranslation byte-identical |
| `03_differential_test.log` | `/audit-output` | `python3 /audit-output/evidence/03_differential_test.py` | 0 | 13,914 cases, zero mismatches |
| `04_concrete_translate.log` | `/tmp/audit-work/87-get-row` | `python3 /reference/py2mpy.py reviewer-concrete-tests.py > reviewer-concrete-tests.mpy` | 0 | reviewer K smoke program generated |
| `05_llvm_build.log` | `/tmp/audit-work/87-get-row` | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition reviewer-runtime-kompiled` | 0 | fresh concrete definition |
| `06_k_concrete_run.log` | `/tmp/audit-work/87-get-row` | `krun reviewer-concrete-tests.mpy --definition reviewer-runtime-kompiled` | 0 | `.K`, `NoExc`, exit-code 0 |
| `07_haskell_build.log` | `/tmp/audit-work/87-get-row` | `kompile verification.k --backend haskell --main-module GET-ROW-VERIFICATION --syntax-module MPY-SYNTAX --output-definition reviewer-verification-kompiled` | 0 | fresh proof definition |
| `08_prove_empty.log` | `/tmp/audit-work/87-get-row` | `kprove spec-labeled.k --definition reviewer-verification-kompiled --spec-module GET-ROW-SPEC --claims GET-ROW-SPEC.empty` | 113 | auditor used the wrong label qualification; unused-filter diagnostic |
| `08b_prove_empty.log` | `/tmp/audit-work/87-get-row` | `kprove spec-labeled.k --definition reviewer-verification-kompiled --spec-module GET-ROW-SPEC --claims empty` | 0 | `#Top` |
| `09_prove_ragged.log` | `/tmp/audit-work/87-get-row` | `kprove spec-labeled.k --definition reviewer-verification-kompiled --spec-module GET-ROW-SPEC --claims ragged` | 0 | `#Top` |
| `10_prove_submitted_spec.log` | `/tmp/audit-work/87-get-row` | `kprove spec.k --definition reviewer-verification-kompiled --spec-module GET-ROW-SPEC` | 0 | `#Top` |
| `11_claim_ground_witnesses.log` | `/audit-output` | `python3 /audit-output/evidence/11_claim_ground_witnesses.py` | 0 | four ground witnesses; claimed/canonical/generated values identical |
| `12_body_mutant_haskell_build.log` | `/tmp/audit-work/87-get-row` | `kompile verification.k --backend haskell --main-module GET-ROW-VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutant-verification-kompiled` | 0 | fresh proof build while `solution.mpy` had `Return(Int(999))` |
| `13_body_mutant_proof.log` | `/tmp/audit-work/87-get-row` | `kprove spec.k --definition body-mutant-verification-kompiled --spec-module GET-ROW-SPEC` | 0 | still `#Top` |
| `13a_body_mutant_concrete_run.log` | `/tmp/audit-work/87-get-row` | `python3 /reference/py2mpy.py reviewer-body-mutant-test.py > reviewer-body-mutant-test.mpy && python3 reviewer-body-mutant-test.py && krun reviewer-body-mutant-test.mpy --definition reviewer-runtime-kompiled --output none` | 0 | Python and K execute the mutation as return value 999 |
| `13b_body_sensitivity.log` | `/audit-output` | `bash /audit-output/evidence/13b_body_sensitivity.sh` | 0 | combined hash/build/proof record: active mutant SHA-256, fresh build exit 0, proof `#Top` exit 0 |
| `14_static_inventory_final.log` | `/audit-output` | `python3 /audit-output/evidence/14_static_inventory.py > /audit-output/evidence/14_rule_inventory.md && sha256sum /audit-output/evidence/14_rule_inventory.md` | 0 | exhaustive lexical inventory; final inventory SHA-256 `60beac214e5f9ecc3cdd8e5f38f3a9219d1fa6d64da300797bf62a7522e56f69` |
| `15_vacuity_dry_run.log` | `/tmp/audit-work/87-get-row` | `kprove spec-vacuity.k --definition reviewer-verification-kompiled --spec-module GET-ROW-SPEC-VACUITY --dry-run` | 0 | false mutation builds successfully |
| `16_vacuity_proof_failure.log` | `/tmp/audit-work/87-get-row` | `kprove spec-vacuity.k --definition reviewer-verification-kompiled --spec-module GET-ROW-SPEC-VACUITY` | 1 | expected `WarnStuckClaimState`; actual heap has empty result instead of `[(0,0)]` |

The first body-mutation build/proof pair is retained separately for redundancy;
`13b_body_sensitivity.log` is the self-contained causal record that installs
the preserved mutant at the active `solution.mpy` path, hashes it, rebuilds, and
proves before restoring the original.
