# Trust-boundary discovery

The canonical inventory contains exactly one rule, in module
`MAXIMUM-VERIFICATION`.

`rule-b232439c4babf099ec2603b1993e6927d97e11d5b79e2ca4eed6caaae5c767bd`
is classified as `DEFINITION`. Its left-hand side is the named mathematical
summary `maximumSpec(L, K)`, and its right-hand side directly defines that
summary as the suffix obtained by sorting the input and dropping
`size(L) - K` elements. It is an equation defining a proof term, not an
operational execution rule or an additional mathematical fact.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1's `prove.sh` first
compiles `verification.k` as module `MAXIMUM-VERIFICATION`, which already
contains the `maximumSpec` rule, and then runs `kprove spec.k` against that
compiled definition. Thus the Stage 1 proof uses the rule; it does not first
prove the rule's exact statement against a module from which the rule is
absent. No inventory rule satisfies the required proof-before-inclusion
ordering.

## Domain lemmas

The domain-lemma set is empty. The sole inventory rule is definitional, has no
`simplification` attribute, and introduces no separately trusted mathematical
fact.
