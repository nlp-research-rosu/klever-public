# Reviewer diagnostic: isolated entry-claim selection

This was a reviewer-authored diagnostic, not the candidate's submitted proof
command and not a reconstruction gate.

Command:

```text
kprove spec.k --definition review-verification-kompiled --spec-module SPEC --claims SPEC.pairs-sum-to-zero
```

The command was started after the loop-invariant claim had independently closed.
Selecting only `SPEC.pairs-sum-to-zero` also removes the auxiliary circularity
from the active specification, so K began unrolling the symbolic loop rather
than applying the submitted invariant. Once that selection effect was
recognized, the process was interrupted by the reviewer (shell status 130).
The corresponding `03_kprove_entry.log` is empty because the interrupted
process had not flushed bounded output.

The valid target reconstruction instead used the submitted aggregate
specification, with both claims active:

```text
kprove spec.k --definition review-verification-kompiled --spec-module SPEC
```

That command exited 0 and printed `#Top`; its output is preserved in
`03_kprove_all_target_claims.log`.
