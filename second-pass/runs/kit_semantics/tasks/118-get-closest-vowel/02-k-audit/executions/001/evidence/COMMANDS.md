# Audit command index

All commands below were run from `/tmp/audit-work/reconstruction` unless a
different working directory is stated. The linked `script(1)` transcripts
contain bounded command output and `COMMAND_EXIT_CODE`. Expected-negative
wrappers print the actual inner `kprove_exit=1` and themselves exit 0 only
after checking that the inner status is nonzero.

## Integrity and fidelity

```sh
# cwd /audit-output
python3 /audit-output/evidence/stage1_integrity.py
# exit 0
```

Transcript: `stage1_integrity.log`.

```sh
python3 /reference/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
cmp /tmp/audit-work/reconstruction/solution.regenerated.mpy \
    /tmp/audit-work/reconstruction/solution.mpy
sha256sum /tmp/audit-work/reconstruction/solution.regenerated.mpy \
          /tmp/audit-work/reconstruction/solution.mpy
# exit 0; both SHA-256 values:
# 45fd803cabebf8892d50d4a04cbcbb7e74a90c01f88713aa140f006d671a6d5d
```

Transcript: `translation_identity.log`.

```sh
# cwd /audit-output
python3 /audit-output/evidence/differential.py
# exit 0; total_cases=508306; mismatch_count=0
```

Transcript: `differential.log`.

## Fresh builds and positive claims

```sh
kompile --backend haskell foundation.k \
  --main-module FOUNDATION \
  --syntax-module FOUNDATION-SYNTAX \
  --output-definition fresh-connection-kompiled
# exit 0

kprove connection-spec.k \
  --definition fresh-connection-kompiled \
  --spec-module CONNECTION-SPEC \
  --claims CONNECTION-SPEC.helper-vowel
# exit 0; #Top

kprove connection-spec.k \
  --definition fresh-connection-kompiled \
  --spec-module CONNECTION-SPEC \
  --claims CONNECTION-SPEC.helper-consonant
# exit 0; #Top
```

Transcripts: `build_connection.log`, `prove_helper_vowel.log`,
`prove_helper_consonant.log`.

```sh
kompile --backend haskell helper-verification.k \
  --main-module HELPER-VERIFICATION \
  --syntax-module HELPER-VERIFICATION-SYNTAX \
  --output-definition fresh-loop-kompiled
# exit 0

kprove loop-connection-spec.k \
  --definition fresh-loop-kompiled \
  --spec-module LOOP-CONNECTION-SPEC \
  --claims LOOP-CONNECTION-SPEC.loop-invariant
# exit 0; #Top
```

Transcripts: `build_loop.log`, `prove_loop_invariant.log`.

```sh
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition fresh-verification-kompiled
# exit 0

kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.entry
# exit 0; #Top
```

Transcripts: `build_verification.log`, `prove_entry.log`.

```sh
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
# exit 0

krun concrete-tests.mpy --definition fresh-runtime-kompiled
# exit 0
```

Transcripts: `build_runtime.log`, `krun_concrete_tests.log`.

## Pinning, ground instances, and operational sensitivity

```sh
kast --definition fresh-verification-kompiled \
  --module VERIFICATION-SYNTAX --sort Module \
  --expression getClosestProgram --expand-macros --output kore \
  > /tmp/audit-work/reconstruction/proof-program.kore
kast --definition fresh-verification-kompiled \
  --module VERIFICATION-SYNTAX --sort Module \
  solution.mpy --expand-macros --output kore \
  > /tmp/audit-work/reconstruction/solution-program.kore
cmp /tmp/audit-work/reconstruction/proof-program.kore \
    /tmp/audit-work/reconstruction/solution-program.kore
# exit 0; each file 21104 bytes and
# SHA-256 f916e371483de3235cc4a6e84f189aa1bd9c2b79900443ab0dbce028b0f67372
```

Transcript: `program_pinning.log`.

```sh
kprove summary-instance-spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SUMMARY-INSTANCE-SPEC
# exit 0; #Top for "bab", "yogurt", "", and "quick"
```

Artifact/transcript: `summary-instance-spec.k`,
`prove_summary_instances.log`.

```sh
kprove helper-body-mutation-spec.k \
  --definition fresh-connection-kompiled \
  --spec-module HELPER-BODY-MUTATION-SPEC
# actual exit 1; WarnStuckClaimState; residual false

kprove loop-body-mutation-spec.k \
  --definition fresh-verification-kompiled \
  --spec-module LOOP-BODY-MUTATION-SPEC
# actual exit 1; WarnStuckClaimState; residual empty string

kprove continuation-mutation-spec.k \
  --definition fresh-verification-kompiled \
  --spec-module CONTINUATION-MUTATION-SPEC
# actual exit 1; WarnStuckClaimState; residual "x"
```

Transcripts: `helper_body_sensitivity.log`, `loop_body_sensitivity.log`,
`continuation_sensitivity.log`.

## Static inventory

```sh
# cwd /audit-output
python3 /audit-output/evidence/inventory_rules.py \
  > /audit-output/evidence/rule_inventory.txt
# exit 0
```

Artifacts: `inventory_rules.py`, `rule_inventory.txt`,
`rule_inventory_command.log`, `local_rule_review.md`,
`used_construct_map.md`.

## Fresh reviewer mutation

```sh
kprove reviewer-false-spec.k \
  --definition fresh-verification-kompiled \
  --spec-module REVIEWER-FALSE-SPEC \
  --dry-run \
  > /tmp/audit-work/reconstruction/reviewer-false-spec.kore
# exit 0; generated KORE size 330 bytes

kprove reviewer-false-spec.k \
  --definition fresh-verification-kompiled \
  --spec-module REVIEWER-FALSE-SPEC
# actual exit 1; WarnStuckClaimState; residual str(iCons(97,.IntSeq))
```

Artifact/transcripts: `reviewer-false-spec.k`,
`reviewer_false_build.log`, `reviewer_false_proof.log`.
