# Diagnostic-only filtered entry run

Command:

```text
kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC --claims SPEC.is-sorted
```

This filter removed `SPEC.loop-invariant`, the circularity required by the
entry proof. `kore-exec` remained active (about 83% CPU) for approximately
30 minutes without a residual or success result. The reviewer interrupted it;
the execution session returned status 130. Its contemporaneous output is in
`stage3-diagnostic-entry-without-invariant.log`.

This is not a positive target-proof result and is not used for the verdict.
The correct full-spec command, which includes both the entry claim and its
auxiliary invariant, is preserved in `stage3-kprove-full-spec.log`; it printed
`#Top` and exited 0. The invariant was also selected and proved separately in
`stage3-kprove-loop-invariant.log`.
