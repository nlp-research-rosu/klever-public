# Entry-only claim-selection diagnostic

Command:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.entry
```

This diagnostic was intentionally interrupted by the reviewer with `Ctrl-C`
after approximately 34 minutes of active `kore-exec` CPU use. Its partial log
is `prove-entry.log`; no exit status was produced because the wrapper itself
received the interrupt.

This is not the submitted positive target command. Filtering the specification
to `SPEC.entry` removes `SPEC.loop-invariant` from the simultaneous claim set,
so the entry execution cannot apply the loop circularity and keeps unrolling.
The intact submitted command (`kprove spec.k ... --spec-module SPEC`) retained
both claims and independently closed with `#Top`, exit 0, in `prove-all.log`.
The loop claim also closed under its own selection in `prove-loop.log`.
