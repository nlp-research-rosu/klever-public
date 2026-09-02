# Trust-boundary discovery

The canonical inventory has SHA-256
`bbad9df4e70598a94f0400994f8887fa6499ad74a9bcf8b430d656fa4f69683a`
and contains one rule in the local `VERIFICATION` module closure.

## Classification

`rule-9f2dfdab6d05b03a483926083949b77353f4d59ab6455390118d3ed077036f67`
is classified as `DEFINITION`. In `verification.k`, it expands
`solutionProgram` into the `Module` AST containing the translated
`truncate_number` function. The associated `solutionProgram` syntax
production carries the `macro` attribute. The rule therefore names and
unfolds the program term used by the proof; it does not model an execution
step and does not assert an independent mathematical property.

There are no `OPERATIONAL_RULE` entries in the canonical inventory.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1's `prove.sh` compiles
`verification.k` and then proves the reachability claim in `spec.k`; it does
not first prove the exact statement of any reusable inventory rule against a
module that omits that rule. Accordingly, no rule is classified as
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. The sole inventory rule is a program-term
definition, and the verification module adds no trusted mathematical fact.
