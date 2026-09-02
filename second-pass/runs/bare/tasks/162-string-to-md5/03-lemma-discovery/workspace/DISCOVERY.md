# Trust-boundary discovery

The canonical inventory identifies three rules, in module `VERIFICATION`, and
all three are classified as `DEFINITION`.

- `rule-94c25ab8fa55e4a32d6644c52fa3be49b288dadeb7d44eed8cd9c05847112219`
  defines `solutionBody` by expanding it to the exact translated body
  constructor tree.
- `rule-355c7965a40e332089142b46c25dec21f1db8e383c1fc3f20a6de02381621f97`
  defines `solutionProgram` by expanding it to the translated module
  constructor tree.
- `rule-0e35f967958921b2696228779a3b13e82321fcfb461b86b6c3cbbee2e6ddf007`
  defines the named `expectedMd5` proof summary in terms of `md5String`.

No inventoried rule is an ordinary execution or observation rule, so the
`OPERATIONAL_RULE` set is empty. The launcher inventory is exhaustive for this
classification task; rules outside it, including rules in other Stage 1
modules, are therefore not added or classified here.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles `verification.k` as module
`VERIFICATION`, which already contains all three inventoried rules. It then
runs the program exercises and finally invokes:

```text
kprove spec.k --definition verification-kompiled
```

There is no earlier proof command against a module lacking any of these rules,
no later insertion of an exactly corresponding rule, and no prove-then-reuse
ordering. Consequently, none meets the evidence requirement for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas and simplification rules

The domain-lemma set is empty.

All three inventory entries have an empty attribute list, so none carries the
`simplification` attribute. Their equations are structural expansions or a
named mathematical summary, and thus belong under `DEFINITION` rather than
`DOMAIN_LEMMA`.
