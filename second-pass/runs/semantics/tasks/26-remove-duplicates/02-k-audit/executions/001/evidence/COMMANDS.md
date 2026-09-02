# Reviewer command ledger

Unless a block says otherwise, commands ran from
`/tmp/audit-work/26-remove-duplicates/candidate`. Full bounded output is in the
named log.

## Integrity and provenance

From `/audit-output`:

```bash
find /reference -maxdepth 3 -printf "%y %p -> %l\n" | sort
find /candidate -maxdepth 4 -printf "%y %p -> %l\n" | sort
test -d /reference/reference-semantics
find /candidate/reference-semantics -type l -print
diff --no-dereference -r /reference/reference-semantics /candidate/reference-semantics
kompile --version
kprove --version
krun --version
```

Status: trusted-semantics directory 0; symlink search empty; recursive diff 0;
all version commands 0. Log:
`01-inventory-and-mode-rerun.log`.

```bash
diff -u /reference/prompt.py /candidate/prompt.py
diff -u /reference/py2mpy.py /candidate/py2mpy.py
sha256sum /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py /candidate/solution.py /candidate/solution.mpy \
  /candidate/spec.k /candidate/verification.k /candidate/prove.sh
```

Status: both diffs 0; `sha256sum` 0. Log:
`02-provenance-and-sources.log`.

The superseded first wrapper was:

```bash
script -q -e -c 'set -o pipefail; ...' \
  /audit-output/evidence/01-inventory-and-mode.log
```

Status: 2 before checks because `script` invoked `sh`, which rejected
`pipefail`. The corrected Bash run above is the operative evidence.

## Translation and differential test

From `/audit-output`:

```bash
python3 /tmp/audit-work/26-remove-duplicates/trusted/py2mpy.py \
  /tmp/audit-work/26-remove-duplicates/candidate/solution.py \
  > /tmp/audit-work/26-remove-duplicates/regenerated-solution.mpy
cmp -s /tmp/audit-work/26-remove-duplicates/regenerated-solution.mpy \
  /tmp/audit-work/26-remove-duplicates/candidate/solution.mpy
python3 -m py_compile /audit-output/evidence/03-differential.py
python3 /audit-output/evidence/03-differential.py
```

Statuses: 0, 0, 0, 0. Log:
`03-translation-and-differential.log`.

## Clean definitions and concrete run

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Status: 0. Log: `04-kompile-llvm.log`.

```bash
krun concrete-tests.mpy --definition runtime-kompiled --output none
```

Status: 0. Log: `04-krun-concrete.log`.

```bash
kompile verification.k \
  --backend haskell \
  --main-module REMOVE-DUPLICATES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Status: 0. Log: `04-kompile-haskell.log`.

## Positive proof targets

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC \
  --claims REMOVE-DUPLICATES-SPEC.loop-invariant \
  --output pretty
```

Status: 0 and `#Top`. Log: `05-kprove-loop-invariant.log`.

The empty case used:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC \
  --claims REMOVE-DUPLICATES-SPEC.entry-empty \
  --trusted REMOVE-DUPLICATES-SPEC.loop-invariant \
  --output pretty
```

Status: 0 and `#Top`. Log: `05-kprove-entry-empty.log`. The loop claim is not
reached on the empty case.

For each `CLAIM` in `entry-keep` and `entry-drop`, the corrected independent
command retained both the proved lemma and selected target:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC \
  --claims REMOVE-DUPLICATES-SPEC.loop-invariant,REMOVE-DUPLICATES-SPEC.CLAIM \
  --trusted REMOVE-DUPLICATES-SPEC.loop-invariant \
  --output pretty
```

Statuses: both 0 and `#Top`. Logs: `05-kprove-entry-keep.log` and
`05-kprove-entry-drop.log`.

Superseded reviewer diagnostics used the following incorrect selector shape:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC \
  --claims REMOVE-DUPLICATES-SPEC.CLAIM \
  --trusted REMOVE-DUPLICATES-SPEC.loop-invariant \
  --output pretty
```

Because `--claims` retained only the entry, it filtered the loop claim out of
the emitted spec before the trusted marking could make it available. Those
open-ended symbolic-unrolling runs are not proof evidence. Their renamed logs
are `05-superseded-entry-keep-filtered-without-loop.log` and
`05-superseded-entry-drop-filtered-without-loop.log`. The exact-PID termination
attempt could not cross sibling PID namespaces; its status 1 is recorded in
`05-superseded-filtered-runs-termination.log`.

## Static inventory and adequacy checks

From `/audit-output`:

```bash
/audit-output/evidence/06-build-rule-inventory.sh
```

Status: 0. Logs: `06-inventory-command-rerun.log`,
`06-rule-inventory.txt`, and `06-full-numbered-k-sources.txt`.

```bash
python3 -m py_compile /audit-output/evidence/07-kast-program-pinning.py
python3 /audit-output/evidence/07-kast-program-pinning.py
python3 -m py_compile /audit-output/evidence/07-claim-witnesses.py
python3 /audit-output/evidence/07-claim-witnesses.py
```

Statuses: 0, 0, 0, 0. Logs: `07-kast-program-pinning.log` and
`07-claim-witnesses.log`.

## Fresh false-result mutation

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC-VACUITY \
  --dry-run \
  --output pretty
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module REMOVE-DUPLICATES-SPEC-VACUITY \
  --output pretty
```

Statuses: dry-run 0; proof 1 with `WarnStuckClaimState` at the false heap
obligation. The audit harness required exactly those statuses and exited 0.
Log: `08-vacuity-build-and-proof.log`.
