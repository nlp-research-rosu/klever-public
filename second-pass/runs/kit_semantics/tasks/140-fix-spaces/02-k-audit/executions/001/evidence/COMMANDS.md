# Auditor command record

All build/proof commands below ran from
`/tmp/audit-work/candidate-src`. Logs are bounded captures with their actual
exit code in the final `COMMAND_EXIT_CODE` line.

## Integrity and generation records

```bash
python3 /audit-output/evidence/integrity_check.py
# exit 0; evidence: 01-integrity-v4.log

python3 /audit-output/evidence/trace_inspect.py
# exit 0; parsed all 273 JSONL records; evidence: 01-trace-summary.log
```

## Translation and differential

```bash
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/candidate-src/solution.regenerated.mpy
cmp -s \
  /tmp/audit-work/candidate-src/solution.regenerated.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
# translator exit 0, cmp exit 0; both SHA-256
# 1bc0cbde9674e4357b29b5a38b64910e147af495f58944d6c1533afd7c488e44
# evidence: 02-translation.log

python3 /audit-output/evidence/differential_test.py
# exit 1 because generated-vs-trusted-canonical mismatches were deliberately
# surfaced; 10,366 inputs, 285 canonical mismatches, 0 prompt-contract
# mismatches; evidence: 02-differential.log and 02-differential-inputs.jsonl
```

## Clean K builds and positive proofs

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
# exit 0; evidence: 03-kompile-haskell.log

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
# exit 0, #Top; evidence: 03-kprove-loop-invariant.log

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
# exit 0, #Top; evidence: 03-kprove-all-claims.log

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
# exit 0; evidence: 03-kompile-llvm.log

/audit-output/evidence/translate_concrete.sh
# exit 0; evidence: 03-concrete-translation-v2.log

krun concrete_cases.mpy --definition audit-runtime-kompiled
# exit 0, final .K / NoExc / exit-code 0;
# evidence: 03-krun-concrete-v2.log
```

## Pinning, witness, and inventory checks

```bash
krun solution.regenerated.mpy --definition audit-runtime-kompiled
# exit 0; final module state contains the exact closure body and exact target
# pre-state; evidence: 04-krun-module-load.log

kprove pinning-compare.k \
  --definition audit-verification-kompiled \
  --spec-module PINNING-COMPARE
# exit 0, #Top; the frontend simplified both exact constructor equalities;
# evidence: 04-kprove-pinning-compare-v2.log

kprove ground-witness.k \
  --definition audit-verification-kompiled \
  --spec-module GROUND-WITNESS
# exit 0, #Top for empty, 1/2/3-space, and interior-2-space witnesses;
# evidence: 04-kprove-ground-witnesses.log

python3 /audit-output/evidence/k_rule_inventory.py
# exit 0; evidence: 04-rule-inventory-v2.log and 04-rule-inventory.tsv
```

An initial reviewer-only pinning probe used functional claims without a
configuration. The frontend reported that functional claims were unsupported
and the backend exited 113 (`04-kprove-pinning-compare.log`). It was replaced
by the configuration claims above. This parser/backend diagnostic is not used
as proof, pinning, or mutation evidence.

## Fresh negative checks

```bash
kprove audit-false-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-MUTATION
# expected exit 1, WarnStuckClaimState; reached "__", demanded "_";
# evidence: 06-kprove-false-mutation.log

kprove audit-body-sensitivity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-BODY-SENSITIVITY
# expected exit 1, WarnStuckClaimState; reached "X", demanded "";
# evidence: 06-kprove-body-sensitivity.log
```
