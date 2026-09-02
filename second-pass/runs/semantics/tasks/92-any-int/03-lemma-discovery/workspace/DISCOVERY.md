# Trust-boundary discovery

The canonical inventory identifies three rules in the local
`ANY-INT-VERIFICATION` module closure. Each is classified exactly once and in
inventory order in `trust-boundary.json`.

## Classifications

- `rule-2448470f8e791bc970ea500cb0eab8f2f171b687e742dc9dd620c3fe599983ae`
  is a `DEFINITION`. It expands the named `anyIntBody` term into the translated
  function body.
- `rule-20a4c6b1a1a6ebf18f4619214bf9a06e19c1ded1a4237df4613d473cbbd128eb`
  is an `OPERATIONAL_RULE`. It is the `<k>`-cell transition that constructs the
  function closure and applies it to the supplied arguments.
- `rule-da3bd6ef60a4c93d6ad5fcaf71497b30730636aeefceca70e5216a0ee566f547`
  is a `DEFINITION`. It defines the `sumCondition` mathematical summary used
  as the integer-case postcondition.

None of the inventoried rules carries the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications. Stage 1's `prove.sh`
first compiles `verification.k` as `ANY-INT-VERIFICATION`, including all three
inventoried rules, and then invokes `kprove` on `spec.k` against that compiled
definition. It contains no earlier proof command against a module omitting one
of these rules and no later inclusion of an exactly corresponding proved rule.
Consequently, the mounted Stage 1 evidence establishes no separately proved
derived lemma.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule asserts an additional
trusted mathematical fact: the two equations are definitions and the
remaining rule is operational.
