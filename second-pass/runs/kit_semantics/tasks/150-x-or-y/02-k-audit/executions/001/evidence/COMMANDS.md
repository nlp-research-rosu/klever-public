# Audit command record

All paths are container paths. Logs named below were captured with `script -q
-e -c`; each log footer records `COMMAND_EXIT_CODE`.

## Stage 1

- CWD `/audit-output`:
  `python3 /audit-output/evidence/stage1/inspect_provenance.py`
  — exit 0; log `stage1/inspect-provenance-final.log`.
- CWD `/audit-output`:
  `sha256sum /audit-input.json /audit-campaign-lock.json /run.json /task.json /generation-result.json /reference/canonical.py /reference/prompt.py /reference/py2mpy.py /generation-evidence/invocation.json /generation-evidence/metrics.json /generation-evidence/runtime-metrics.json /generation-evidence/usage.json /generation-evidence/codex-last.txt /generation-evidence/codex-output.log /generation-evidence/prompt.txt /generation-evidence/codex-trace/2026/07/25/*.jsonl`
  — exit 0; log `stage1/hash-and-compare.log`.
- CWD `/audit-output`:
  `diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics`
  — exit 0; same log.

An initial optional `jq` display attempt exited 127 because `jq` is absent;
`stage1/launcher-records.log` preserves it. The records were then read with
`sed` and parsed with Python; this did not affect any audit gate.

## Stage 2

- CWD `/tmp/audit-work/reconstruction`:
  `python3 py2mpy.py solution.py > solution.regenerated.mpy`
  — exit 0.
- Same CWD: `cmp -l solution.mpy solution.regenerated.mpy`
  — exit 0; both commands are in `stage2/translation-identity.log`.
- Same CWD:
  `python3 /audit-output/evidence/stage2/differential.py`
  — exit 0; log `stage2/differential.log`.

## Stage 3

- CWD `/tmp/audit-work/reconstruction`:
  `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION-SYNTAX --output-definition verification-audit-kompiled`
  — exit 0; log `stage3/kompile-verification.log`.
- Same CWD:
  `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.trial-loop`
  — exit 0, `#Top`; log `stage3/kprove-trial-loop.log`.
- Same CWD:
  `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC`
  — exit 0, `#Top`; log `stage3/kprove-complete-spec.log`.
- Same CWD:
  `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled`
  — exit 0; log `stage3/kompile-runtime.log`.
- Same CWD:
  `python3 py2mpy.py /audit-output/evidence/stage3/concrete_probe.py > concrete_probe.mpy`
  — exit 0.
- Same CWD:
  `krun concrete_probe.mpy --definition runtime-audit-kompiled`
  — exit 0 with final `.K`, `NoExc`, and modeled exit code 0; both commands are
  in `stage3/krun-concrete-probe.log`.

A diagnostic run selecting only `SPEC.x-or-y` was interrupted with exit 130
after it excluded the helper circularity and began unrolling the symbolic loop;
`stage3/kprove-x-or-y.log` preserves this non-target diagnostic. The required
complete-spec command includes both the helper and entry claims and closes.

## Stage 4

- CWD `/tmp/audit-work/reconstruction`:
  `python3 /audit-output/evidence/stage4/pinning_check.py`
  — exit 0; log `stage4/pinning-check-v2.log`. The script records its two exact
  `kast` commands, both exit 0.
- Same CWD:
  `python3 /audit-output/evidence/stage4/ground_witnesses.py`
  — exit 0; log `stage4/ground-witnesses.log`.
- Same CWD:
  `python3 /audit-output/evidence/stage4/make_body_mutation.py`
  — exit 0; log `stage4/body-mutation-generate.log`.
- Same CWD:
  `kprove spec-audit-body-mutation.k --definition verification-audit-kompiled --spec-module SPEC-AUDIT-BODY-MUTATION --dry-run`
  — exit 0; log `stage4/body-mutation-dry-run.log`.
- Same CWD:
  `kprove spec-audit-body-mutation.k --definition verification-audit-kompiled --spec-module SPEC-AUDIT-BODY-MUTATION`
  — expected exit 1 with `WarnStuckClaimState` and residual value 20; log
  `stage4/body-mutation-kprove.log`.

## Stage 5

- CWD `/tmp/audit-work/reconstruction`:
  `python3 /audit-output/evidence/stage5/inventory_k.py`
  — exit 0.
- Same CWD:
  `python3 /audit-output/evidence/stage5/disposition_inventory.py`
  — exit 0; final combined log
  `stage5/inventory-and-dispositions-v3.log`.
- Same CWD:
  `rg -n "\[(?:[^]]*)(simplification|priority|concrete|symbolic|anywhere|owise|no-evaluators|hook)" verification.k spec.k`
  — exit 1 because there are no matches; recorded as the expected absence in
  `stage5/attribute-absence.log`.

## Stage 6

- CWD `/tmp/audit-work/reconstruction`:
  `kprove spec-audit-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-AUDIT-VACUITY --dry-run`
  — exit 0; log `stage6/mutation-dry-run.log`.
- Same CWD:
  `kprove spec-audit-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-AUDIT-VACUITY`
  — expected exit 1 with `WarnStuckClaimState` and residual value 10; log
  `stage6/mutation-kprove.log`.
