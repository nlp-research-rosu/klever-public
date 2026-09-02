# Trust-boundary discovery

The canonical inventory contains one rule from the local verification-module
closure.

## Classification

`rule-421e63465e293edfd877e4482b1842e53422f4b5589c6d1a5f54e9d264066aa8`
is classified as `DEFINITION`. It defines the named proof-harness term
`#callAdd(X, Y)` by expanding it to the loading of the exact `add` AST and a
call with the two symbolic integer arguments. This is a named proof-term
expansion, not a separately asserted mathematical property and not an
additional arithmetic fact. The rule has no `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1's `prove.sh` first
compiles `verification.k` as `ADD-VERIFICATION` and then proves the claim in
`spec.k` against that compiled definition. Thus the inventoried `#callAdd`
rule is already present in the definition used by `kprove`; there is no
earlier proof of that rule's exact statement against a module omitting it.
No inventory rule therefore meets the evidence requirement for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. The sole inventoried rule only constructs the
execution term used by the target claim and supplies no trusted mathematical
fact.
