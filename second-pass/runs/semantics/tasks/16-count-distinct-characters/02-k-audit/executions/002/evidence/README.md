# Reviewer evidence index

Every `stage*.log` was produced by `run_logged.sh`. Its first line is the
shell-escaped exact command and its final line is `EXIT_STATUS: N`.

## Stage 1

- `stage1-provenance.log`: required-record checks, launcher/hash checks,
  candidate/trusted prompt and translator identity, recursive supplied-semantics
  identity, generation evidence hashes, and full structured-record parsing.
- `stage1-trace-inventory.log`: bounded inventory of all 99 structured trace
  records, including tool calls and outputs.
- `provenance_check.py`, `trace_inventory.py`: reviewer-authored checkers.

## Stage 2

- `stage2-translation.log`: trusted translation and byte comparison.
- `stage2-differential.log`: 4,624-case independent CPython differential run.
- `differential_test.py`, `differential-cases.json`: executable oracle and
  complete deterministic input corpus.

## Stage 3

- `stage3-clean-check.log`: confirms no pre-existing kompiled directories.
- `stage3-kompile-llvm.log`, `stage3-kompile-proof.log`: fresh source builds.
- `stage3-concrete-translation.log`, `stage3-krun-candidate-tests.log`: trusted
  concrete-test regeneration and execution.
- `stage3-kprove-all.log`: unmodified candidate specification.
- `stage3-kprove-load.log`, `stage3-kprove-call.log`: each candidate claim
  independently replayed via claim-identical reviewer modules.
- `spec-load-only.k`, `spec-call-only.k`: those split modules.

## Stage 4

- `stage4-pinning-extract-v2.log`, `stage4-pinning-kast-v2.log`: extracts both
  proof-executed function terms and proves their parsed KORE bytes equal the
  trusted regenerated `solution.mpy` term.
- `extract_pinned_program.py`, `pinned-*.mpy`: checker and extracted terms.
- `stage4-ground-kprove.log`, `spec-ground.k`: concrete satisfying theorem
  instances, including Unicode code sequences.
- `stage4-adequacy-witness.log`, `adequacy_witness.py`: compares those K results
  with both Python implementations and exhibits two Unicode counterexamples.
- `stage4-body-mutation-*.log`, `verification-body-mutation.k`: a material
  mutation of the closure body; it builds, then the original result obligation
  is stuck as expected.

## Stage 5

- `k-inventory-v2.json`: all 1,094 local K sentences, including full text,
  locations, hashes, and attributes.
- `k-classification-v2.json`: a decision for every inventoried sentence.
- `stage5-inventory-v2-command.log`,
  `stage5-classification-v2-command.log`: exact generation commands.
- `k_full_inventory.py`, `classify_k_inventory.py`: reviewer-authored scripts.
- `superseded/`: retained first-pass parser output and the expected failed
  program-mode parse before `.Exprs` unit normalization; neither is relied on.

## Stage 6

- `spec-vacuity.k`: false “correct result plus one” mutation, false at the
  satisfying empty input.
- `stage6-vacuity-dry-run.log`: successful parsing/KORE generation.
- `stage6-vacuity-kprove.log`: expected `WarnStuckClaimState` and exit 1.
