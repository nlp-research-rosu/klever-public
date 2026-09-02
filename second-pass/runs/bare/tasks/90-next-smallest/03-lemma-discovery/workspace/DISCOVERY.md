# Trust-boundary discovery

The canonical inventory contains exactly one rule, in module
`VERIFICATION`. It is classified as `DEFINITION`.

`rule-f5e05fc9a552c9b3fec872a9cab3d805625f03178e4c821cde0d4317e5a023e9`
expands the named term `secondSmallest(L)` into a conditional that returns
index 1 of `uniqueSort(L)` when that list has at least two elements and
`none` otherwise. This is the defining equation for the declarative contract
summary, so it does not assert an additional mathematical fact.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` first
compiles `verification.k` as module `VERIFICATION`, which already contains
the `secondSmallest` rule, and then runs `kprove` on `spec.k` against that
compiled definition. Consequently, the Stage 1 evidence does not prove this
rule against a module lacking it, and there is no proof-before-import evidence
for any inventory rule.

## Domain lemmas

The domain-lemma set is empty. The sole inventory rule is a definitional
unfolding, and the canonical inventory contains no additional trusted
mathematical facts.

The operational rules in `semantic.k` are outside the launcher-generated
canonical inventory and therefore receive no entries here. Classification is
limited to the inventory, whose rule IDs are reproduced once and in its
original order.
