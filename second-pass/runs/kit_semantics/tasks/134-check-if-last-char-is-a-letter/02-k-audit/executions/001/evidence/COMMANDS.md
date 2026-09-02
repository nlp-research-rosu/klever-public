# Reviewer command record

All mutable work used `/tmp/audit-work/134-check-last-char`; all durable logs
and reviewer-authored sources are under `/audit-output/evidence`.

## Stage 1

```bash
python3 /audit-output/evidence/stage1_integrity.py
```

Exit 0. Full output: `stage1_integrity.log`.

```bash
python3 /audit-output/evidence/summarize_generation_trace.py
```

Exit 0. It parsed 345 JSONL events with zero parse errors. Full indexed output:
`stage1_generation_trace_summary.log`.

The source-only scratch tree was prepared with:

```bash
mkdir -p /tmp/audit-work/134-check-last-char/reference-semantics
cp -a /reference/reference-semantics/. /tmp/audit-work/134-check-last-char/reference-semantics/
cp /reference/canonical.py /reference/prompt.py /reference/py2mpy.py /tmp/audit-work/134-check-last-char/
cp /candidate/solution.py /candidate/solution.mpy /candidate/verification.k /candidate/spec.k /candidate/spec-model-boundary.k /candidate/spec-vacuity.k /candidate/spec-body-mutation.k /tmp/audit-work/134-check-last-char/
```

Candidate `runtime-kompiled/`, `verification-kompiled/`, bytecode, and other
caches were not copied or used.

## Stage 2

```bash
python3 py2mpy.py solution.py > solution.regenerated.mpy
sha256sum solution.py solution.mpy solution.regenerated.mpy
cmp -l solution.mpy solution.regenerated.mpy
```

Translator exit 0; `cmp` exit 0. Log: `stage2_translation.log`.

```bash
python3 /audit-output/evidence/stage2_differential.py --inputs-only > /audit-output/evidence/stage2_inputs.json
python3 /audit-output/evidence/stage2_differential.py
```

Both exits 0. The test ran 9,354 distinct strings. Log:
`stage2_differential.log`; full corpus: `stage2_inputs.json`.

## Stage 3

```bash
python3 py2mpy.py stage3_smoke.py > stage3_smoke.mpy
```

Exit 0. Log: `stage3_smoke_translation.log`.

```bash
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
krun stage3_smoke.mpy --definition audit-runtime-kompiled
```

Both exits 0. Logs: `stage3_kompile_llvm.log`, `stage3_krun_smoke.log`.

```bash
kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.target-empty
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.target-nonalpha
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.target-alpha
kprove spec-model-boundary.k --definition audit-verification-kompiled --spec-module SPEC-MODEL-BOUNDARY
```

Every command exited 0; every `kprove` printed `#Top`. Logs:
`stage3_kompile_haskell.log`, `stage3_kprove_all_targets.log`,
`stage3_kprove_target_empty.log`, `stage3_kprove_target_nonalpha.log`,
`stage3_kprove_target_alpha.log`, and `stage3_kprove_model_boundary.log`.

## Stage 4

```bash
python3 /audit-output/evidence/stage4_pinning.py
```

Exit 0. Log: `stage4_pinning.log`.

```bash
kprove stage4_body_sensitivity.k --definition audit-verification-kompiled --spec-module AUDIT-BODY-SENSITIVITY
```

Exit 1 as expected, with `WarnStuckClaimState` and `<k> true ~> .K </k>`.
The surrounding validation wrapper exited 0. Log:
`stage4_body_sensitivity.log`.

## Stage 5

```bash
python3 /audit-output/evidence/stage5_inventory.py > /audit-output/evidence/stage5_rule_inventory.md
rg -n '\[(?:[^]]*\b(?:priority|simplification|concrete|function|functional|total|no-evaluators|owise)\b[^]]*)\]' \
  /tmp/audit-work/134-check-last-char/reference-semantics/semantics.k \
  /tmp/audit-work/134-check-last-char/reference-semantics/semantics/*.k \
  /tmp/audit-work/134-check-last-char/verification.k \
  > /audit-output/evidence/stage5_attribute_index.txt
```

Both exits 0. The inventory contains 1,021 entries.

## Stage 6

```bash
kprove stage6_false_result.k --definition audit-verification-kompiled --spec-module AUDIT-FALSE-RESULT
```

Exit 1 as expected, with `WarnStuckClaimState` and the reachable residual
`<k> true ~> .K </k>` against destination `false`. The surrounding validation
wrapper exited 0. Log: `stage6_false_result.log`.
