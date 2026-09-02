# K proof trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory
SHA-256 `9a12ebca3aee6e4628fbfba1dc7335ab4e3079d3c32cdc1cace0d9ad4f3a4fd7`.
It contains 11 rules, all in `VERIFICATION`. Every inventory rule is classified
exactly once and in canonical order in `trust-boundary.json`.

## Classification basis

- The two `#iterNext(list(intVals(...)))` rules are `OPERATIONAL_RULE`s. They
  give the verification model's symbolic integer-list representation its
  ordinary empty and yield iterator transitions.
- `scopeMap` and the four `addAccSpec` equations are `DEFINITION`s. They are,
  respectively, a structural projection and the complete mathematical
  recurrence used as the result summary.
- `addLoopBody`, `addFunctionBody`, and `solutionModule` are `DEFINITION`s.
  Their productions carry the `macro` attribute, and these rules expand the
  corresponding named proof terms.
- Rule
  `rule-97c5ca34b9b50dc1f2c9ed9ae56ea870fa5fc9060599752a28635a1372be2589`
  is a `DOMAIN_LEMMA`. It bypasses an arbitrary symbolic loop at function entry
  and replaces its result with `addAccSpec(INPUT, false, 0)`. That is an
  additional mathematical summary rather than an ordinary small-step
  execution transition.

No inventory rule carries the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

Stage 1's `prove.sh` first compiles `verification.k` into
`verification-kompiled`. At that point the loop-summary rule above is already
part of the proof definition. The script then proves the
`SPEC.loop-invariant-bound` and `SPEC.add-correct` claims against that compiled
definition. Neither claim is the exact statement of the loop-summary rule, and
there is no earlier compilation or proof against a module that omits the rule.
Consequently, the comment calling it an instance of the proved invariant does
not satisfy the required proof-before-installation ordering or exact
correspondence.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

- `rule-97c5ca34b9b50dc1f2c9ed9ae56ea870fa5fc9060599752a28635a1372be2589`
