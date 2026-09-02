# Audit command ledger

All commands were run against source copied to
`/tmp/audit-work/63-fibfib`; no candidate-built definition was used.

## Toolchain and provenance

```sh
kompile --version
kprove --version
krun --version
kast --version
python3 --version
```

Exit 0; K v7.1.293 and Python 3.10.12
(`00-tool-versions.log`).

```sh
python3 /audit-output/evidence/check_provenance.py
```

Exit 0; `PROVENANCE_CHECK_PASS` (`01-provenance.log`). The script records
every required file/type/hash comparison and validates all 181 structured trace
records.

## Translation and Python differential

```sh
python3 /tmp/audit-work/63-fibfib/reference/py2mpy.py \
  /tmp/audit-work/63-fibfib/candidate/solution.py \
  > /tmp/audit-work/63-fibfib/regenerated-solution.mpy
cmp -l /tmp/audit-work/63-fibfib/candidate/solution.mpy \
  /tmp/audit-work/63-fibfib/regenerated-solution.mpy
```

Both exit 0; both files have SHA-256
`4ae5eadda2bc9e05737c549a4ae38413d20a0bd9a520a71bf1100855124657f0`
(`02-translation-cmp.log`).

```sh
python3 /audit-output/evidence/differential_test.py
```

Exit 0; zero mismatches for all `n=0..20` and the larger indices
25, 50, 100, and 250 (`02-differential.log`).

## Clean concrete and proof reconstruction

```sh
kompile semantic.k --backend llvm \
  --syntax-module FIBFIB-SYNTAX --main-module FIBFIB \
  --output-definition /tmp/audit-work/63-fibfib/build/concrete-kompiled
```

Exit 0 (`03-kompile-llvm.log`).

```sh
python3 /audit-output/evidence/run_concrete_cases.py
```

The first reviewer-script run exited 1 solely because the parser regex
contained literal backslashes; every displayed `krun` command itself exited 0
and displayed the expected result (`03-concrete-cases.log`). After correcting
that evidence parser:

```sh
python3 /audit-output/evidence/run_concrete_cases.py
```

Exit 0; all nine K/Python comparisons matched
(`03-concrete-cases-fixed.log`). The script records each exact `krun` command:

```sh
krun /tmp/audit-work/63-fibfib/candidate/solution.mpy -cN=<N> \
  --definition /tmp/audit-work/63-fibfib/build/concrete-kompiled
```

for `N = 0,1,2,3,4,5,8,10,25`; every invocation exited 0.

```sh
kompile semantic.k --backend haskell \
  --syntax-module FIBFIB-SYNTAX --main-module FIBFIB \
  --output-definition /tmp/audit-work/63-fibfib/build/proof-kompiled
```

Exit 0 (`03-kompile-haskell.log`).

```sh
kprove spec.k \
  --definition /tmp/audit-work/63-fibfib/build/proof-kompiled \
  --spec-module FIBFIB-SPEC -w none
```

Exit 0, output exactly `#Top` (`03-kprove-all-claims.log`).

```sh
kprove spec.k \
  --definition /tmp/audit-work/63-fibfib/build/proof-kompiled \
  --spec-module FIBFIB-SPEC \
  --claims FIBFIB-SPEC.loop-invariant
```

Exit 0, output `#Top` (`03-kprove-loop-invariant.log`).

An initial diagnostic tried the analogous `--claims
FIBFIB-SPEC.program-correct`. Claim filtering removed the helper loop claim,
so `kore-exec` kept unrolling at about 97% CPU. It was interrupted after about
ten minutes (exit 130; empty buffered log
`03-kprove-program-correct.log`). This is not the valid positive target
command.

For independent compositional entry closure, the exact separately proved loop
claim was marked `[trusted]` only in the reviewer spec
`spec-entry-composed.k`, leaving the exact entry claim as the obligation:

```sh
kprove /audit-output/evidence/spec-entry-composed.k \
  --definition /tmp/audit-work/63-fibfib/build/proof-kompiled \
  --spec-module FIBFIB-SPEC-ENTRY-COMPOSED
```

The first three authoring attempts exited 113 because `[trusted]` was placed in
the label bracket; their parser logs are preserved. With the valid trailing
attribute syntax the command exited 0 and printed `#Top`
(`03-kprove-program-composed-attr-final.log`).

## Pinning, witnesses, and body sensitivity

```sh
kast solution.mpy \
  --definition /tmp/audit-work/63-fibfib/build/proof-kompiled \
  --module FIBFIB-SYNTAX --sort Pgm --expand-macros --output json \
  > /tmp/audit-work/63-fibfib/source-term.json
kast --expression fibfibProgram \
  --definition /tmp/audit-work/63-fibfib/build/proof-kompiled \
  --module FIBFIB-VERIFICATION --sort Pgm --expand-macros --output json \
  > /tmp/audit-work/63-fibfib/claim-term.json
cmp -s /tmp/audit-work/63-fibfib/source-term.json \
  /tmp/audit-work/63-fibfib/claim-term.json
```

All exit 0; both JSON terms have SHA-256
`b0536e0b2937b5e6163a8115597630d51d47fc9483611d513e6fcfc5c594d236`
(`04-program-pinning.log`).

```sh
python3 /audit-output/evidence/claim_witnesses.py
```

Exit 0; concrete entry and loop states satisfy their preconditions and the
claimed values agree with both Python implementations
(`04-claim-witnesses.log`).

The body mutation changes the executed macro term from `return a` to
`return b` and changes only the helper's continuation to follow that actual
mutated body (`04-body-mutation.diff`):

```sh
kompile semantic.k --backend haskell \
  --syntax-module FIBFIB-SYNTAX --main-module FIBFIB \
  --output-definition /tmp/audit-work/63-fibfib/build/body-mutation-kompiled
kprove spec.k \
  --definition /tmp/audit-work/63-fibfib/build/body-mutation-kompiled \
  --spec-module FIBFIB-SPEC
```

Build exit 0; proof exit 1 with `WarnStuckClaimState` and the unmet equality
`fibfibMath(N+1)=fibfibMath(N)` (`04-body-mutation-*.log`).

## Fresh non-vacuity mutation

```sh
kprove /audit-output/evidence/spec-vacuity.k \
  --definition /tmp/audit-work/63-fibfib/build/proof-kompiled \
  --spec-module FIBFIB-SPEC-VACUITY --dry-run
```

Exit 0, demonstrating successful parsing/build
(`06-vacuity-dry-run.log`).

```sh
kprove /audit-output/evidence/spec-vacuity.k \
  --definition /tmp/audit-work/63-fibfib/build/proof-kompiled \
  --spec-module FIBFIB-SPEC-VACUITY
```

Exit 1 with `WarnStuckClaimState` and exactly the unmet equality
`fibfibMath(N)+1=fibfibMath(N)` (`06-vacuity-kprove.log`). `N=0` is a
satisfying concrete witness: the real result is 0 and the mutated destination
requires 1.
