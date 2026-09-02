# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256` `20b6358e762781800f25ce55eb5c0c191044c9e9a1b81cb80bf453a3cadc4c53`.
It contains 21 rules, all from the Stage 1 `VERIFICATION` module.

## Classification summary

- `DEFINITION`: 19 rules.
- `OPERATIONAL_RULE`: 2 rules.
- `PROVED_DERIVED_LEMMA`: 0 rules.
- `DOMAIN_LEMMA`: 0 rules.

The two operational rules are the priority-40 `#iterNext` rules for the typed
`wordVals` verification input. They specify the observable iterator behavior
used by symbolic execution: completion for the empty sequence and yielding a
string plus the remaining sequence for a nonempty sequence.

All other rules are definitional:

- The two `wordVals` equations define the typed input encoding.
- `findMaxLoopBody` and `findMaxFunctionBody` expand named proof terms to the
  exact translated program fragments.
- The five `findMaxWords` equations define the mathematical accumulator by
  cases.
- `bestWord` and `bestScore` define the two structural projections.
- The eight rules with the `simplification` attribute are specialized
  projection-unfolding equations for those same accumulator cases. Although
  the Stage 1 comment calls them projection lemmas, their role and form are
  definitional: they expose an existing accumulator equation beneath a named
  projection and add no independent ordering, cardinality, or string fact.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles `verification.k` as module
`VERIFICATION`, with all 21 inventoried rules already present, and then runs:

```text
kprove spec.k --definition verification-kompiled
```

`spec.k` contains the `find-max-loop-invariant` and `find-max-contract`
claims. Neither is an exact statement of an inventoried rule, and Stage 1 has
no preceding proof command or alternate module that proves any inventoried
rule before adding it to the verification definition. Consequently, the
required ordering and exact-correspondence evidence for
`PROVED_DERIVED_LEMMA` is absent for every rule.

## Domain lemmas

The domain-lemma set is empty. No verification rule supplies an additional
trusted mathematical fact beyond the definitions and operational input
adapter described above.
