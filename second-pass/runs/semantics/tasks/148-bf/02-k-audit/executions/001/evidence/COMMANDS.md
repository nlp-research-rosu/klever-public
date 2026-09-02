# Reviewer command index

All commands ran from `/tmp/audit-work/148-bf-audit` unless the command uses
absolute paths. The referenced `script(1)` logs are bounded transcripts whose
footer records `COMMAND_EXIT_CODE`.

## Toolchain

```bash
bash -o pipefail -lc "kompile --version && kprove --version && krun --version && python3 --version"
```

Exit 0. Log: `stage0-toolchain.log`.

## Stage 1: provenance

```bash
python3 /audit-output/evidence/provenance_check.py
```

The first run exited 1 because the reviewer script compared the launcher-added
embedded `config` key with `/task.json`; log: `stage1-provenance.log`. After
correcting that reviewer-only comparison, the same command exited 0 and printed
`INTEGRITY_CHECKS=PASS`; log: `stage1-provenance-final.log`.

## Stage 2: fidelity

```bash
python3 /audit-output/evidence/differential_test.py
```

The first run exited 1 because the reviewer's independent oracle mishandled
equal valid names; log: `stage2-differential.log`. The corrected command exited
0 over 939 unique cases with zero mismatches; log:
`stage2-differential-final.log`.

```bash
bash -o pipefail -lc "python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/148-bf-audit/solution.regenerated.mpy && cmp -s /candidate/solution.mpy /tmp/audit-work/148-bf-audit/solution.regenerated.mpy && sha256sum /candidate/solution.mpy /tmp/audit-work/148-bf-audit/solution.regenerated.mpy"
```

Exit 0; both files hash to
`3f657ffd4d066c0d77ca1927b490720f80cac27830b713caaf4bdf9cfee6a7fa`.
Log: `stage2-regeneration.log`. An earlier reviewer CLI attempt used an
unsupported `--output` option and exited 2 before the correct shell-redirection
command; it is preserved as `stage2-translate-attempt.log`.

## Stage 3: clean reconstruction

```bash
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition reviewer-runtime-kompiled
```

Exit 0. Log: `stage3-kompile-llvm.log`.

```bash
kompile verification.k --backend haskell --main-module BF-VERIFICATION --syntax-module BF-VERIFICATION --output-definition reviewer-verification-kompiled
```

Exit 0. Log: `stage3-kompile-haskell.log`.

```bash
kprove spec.k --definition reviewer-verification-kompiled --spec-module BF-SPEC
```

Exit 0 and `#Top`. Log: `stage3-kprove-all.log`.

```bash
bash -o pipefail -lc "python3 concrete-tests.py && python3 py2mpy.py concrete-tests.py > concrete-tests.mpy && krun concrete-tests.mpy --definition reviewer-runtime-kompiled --output none"
```

Exit 0. Log: `stage3-concrete-tests.log`.

## Stage 4: pinning, witnesses, and body sensitivity

```bash
bash -o pipefail -lc "python3 /audit-output/evidence/extract_translated_body.py > body-from-solution.mpy && kast body-from-solution.mpy --definition reviewer-verification-kompiled --module BF-VERIFICATION --sort Stmts --expand-macros --output kore --output-file body-from-solution.kore && kast --expression bfBody --definition reviewer-verification-kompiled --module BF-VERIFICATION --sort Stmts --expand-macros --output kore --output-file body-from-macro.kore && cmp -s body-from-solution.kore body-from-macro.kore && sha256sum body-from-solution.mpy body-from-solution.kore body-from-macro.kore"
```

Exit 0; both expanded KORE bodies hash to
`644ce421a13ba7d711e970a2448745204080a98b6c33ca4a964b00488bb61d7d`.
Log: `stage4-body-pinning.log`.

```bash
kprove spec-ground-witnesses.k --definition reviewer-verification-kompiled --spec-module BF-SPEC-GROUND-WITNESSES
```

Exit 0 and `#Top`. Log: `stage4-ground-witnesses.log`.

The reviewer changed the executed body's `"Earth"` literal to `"EarthX"` in
`verification-body-mutated.k`, leaving the expected sequence unchanged:

```bash
kompile verification-body-mutated.k --backend haskell --main-module BF-VERIFICATION-BODY-MUTATED --syntax-module BF-VERIFICATION-BODY-MUTATED --output-definition reviewer-body-mutated-kompiled
kprove spec-body-mutated.k --definition reviewer-body-mutated-kompiled --spec-module BF-SPEC-BODY-MUTATED
```

Compilation exited 0. The proof exited 1 with `WarnStuckClaimState`,
`AssertionError`, and exit code 1 in the residual. Logs:
`stage4-body-mutation-kompile.log` and `stage4-body-mutation-proof.log`.

## Stage 5: exhaustive inventory

```bash
python3 /audit-output/evidence/rule_inventory.py
```

Exit 0; it emitted 970 entries. Log: `stage5-rule-inventory.log`; outputs:
`rule-inventory.tsv` and `rule-inventory-summary.txt`.

```bash
python3 /audit-output/evidence/proof_local_checks.py
```

The first reviewer-script run exited 1 because a comment contained the word
`claim`; log: `stage5-proof-local-checks.log`. The comment-stripped final
version exited 0; log: `stage5-proof-local-checks-final2.log`.

## Stage 6: fresh non-vacuity mutation

```bash
kprove spec-vacuity-reviewer.k --definition reviewer-verification-kompiled --spec-module BF-SPEC-VACUITY-REVIEWER --dry-run
```

Exit 0. Log: `stage6-vacuity-dry-run.log`.

```bash
kprove spec-vacuity-reviewer.k --definition reviewer-verification-kompiled --spec-module BF-SPEC-VACUITY-REVIEWER
```

Expected exit 1 with `WarnStuckClaimState`; the residual is the actual six-item
Mercury-to-Neptune result against the false empty-tuple target. Log:
`stage6-vacuity-proof.log`.
