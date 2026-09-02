# Trust-boundary discovery

The canonical inventory has SHA-256
`f7fc1515a39252cfcad99c9b36688221f5ff9a464dcfddb5f89cd67042f72ed7`
and contains one rule in the local `VERIFICATION` module closure.

## Classification

`rule-59290db9e488b423436a4d0f01b5a3d6d709fdc7ff06097440b03b279b42ecfd`
is classified as `DEFINITION`. It expands the named proof-harness term
`#isEqualToSumEven(N)` into a `Call` of the closure whose parameter and body
correspond to the translated function in `solution.mpy`. The resulting call,
argument binding, expression evaluation, return, and frame cleanup are handled
by the imported reference semantics. The rule is therefore a definition of a
named proof term, not an additional arithmetic fact or an independent
execution rule in the Python model.

There are no canonical rules classified as `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1's `prove.sh` compiles
`verification.k` into `verification-kompiled` before invoking `kprove` on
`spec.k`; consequently, the sole inventory rule is already present in the
module used to prove the claims. Stage 1 contains no earlier proof of that
rule's exact statement against a module omitting it, so it is not classified
as `PROVED_DERIVED_LEMMA`. The four claims in `spec.k` are proof targets, not
rules in the canonical inventory.

## Domain lemmas

The domain-lemma set is empty. The sole rule adds no trusted mathematical fact,
and the canonical inventory contains no rule with the `simplification`
attribute.
