# Filtered entry-only diagnostic note

Command:

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.sum-squares
```

The reviewer started this command from
`/tmp/audit-work/142-sum-squares`. It kept `kore-exec` CPU-active for 756
seconds without emitting a result because selecting only the entry claim also
removes the loop-invariant circularity from the proof set. The reviewer
interrupted the enclosing execution session; the session reported exit status
130. The interruption occurred before `run_logged.sh` finalized its log, so
this note records the experiment explicitly.

This is not treated as a failed positive claim. The bounded reproduction in
`11-kprove-entry-filtered-depth80.log` exits 1 at the second symbolic loop
iteration and exhibits the missing circularity. The actual target is the
two-claim proof set: `10-kprove-loop-invariant.log` closes the invariant
individually, and `12-kprove-all-targets.log` closes the complete set with
`#Top` and exit 0.
