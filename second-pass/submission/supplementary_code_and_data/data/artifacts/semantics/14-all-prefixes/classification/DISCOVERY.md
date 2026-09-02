# Trust-boundary discovery

The canonical inventory contains seven rules, all from the `VERIFICATION`
module. Every rule is classified as `DEFINITION`.

The first two rules are the recursive and terminating equations of
`prefixesAcc`, the mathematical fold used to summarize the source loop. The
third rule defines `allPrefixes` by choosing the initial accumulator and the
range bounds corresponding to every nonempty string prefix.

The remaining four rules expand named proof terms:
`allPrefixesLoopBody`, `allPrefixesBody`, `allPrefixesDef`, and
`solutionModule`. They package the translated constructor syntax so that the
claims can refer to the exact program structure readably. They do not add
execution behavior or mathematical facts.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` compiles
`verification.k`—including all seven inventory rules—into
`verification-kompiled` before running `kprove spec.k`. It contains no earlier
proof against a module omitting any inventory rule, and therefore provides no
evidence of the required prove-before-add ordering or exact correspondence for
a reusable derived rule.

The claims in `spec.k` prove the loop invariant and end-to-end result, but
claims are not rules in the canonical local verification-module inventory.

## Other classifications

There are no `OPERATIONAL_RULE` entries: none of the seven rules specifies an
ordinary configuration transition or observation in the verification model.

The `DOMAIN_LEMMA` set is empty. No inventory rule asserts an additional
trusted mathematical fact, and the inventory contains no rule carrying the
`simplification` attribute.
