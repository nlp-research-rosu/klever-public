The diagnostic command recorded in `stage3-kprove-entry.log` selected only
`SPEC.intersperse-correct`. Doing so removes `SPEC.loop-invariant` from the
specification, so the entry proof loses its required circularity and keeps
unrolling the symbolic list. The reviewer interrupted that diagnostic after
about 60 seconds; it was not a candidate target-proof command and is not used
as either positive or negative evidence.

The actual candidate target command was the unfiltered
`kprove spec.k --definition reviewer-verification-kompiled --spec-module SPEC`.
It retained both claims, printed `#Top`, and exited 0, as recorded in
`stage3-kprove-all.log`. The loop circularity was also selected and proved
separately in `stage3-kprove-loop-invariant.log`.
