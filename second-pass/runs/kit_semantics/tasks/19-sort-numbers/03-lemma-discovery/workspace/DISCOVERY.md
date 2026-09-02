# Trust-boundary discovery

## Inventory basis

The exhaustive source is `/reference/rule-inventory.json`, with canonical
inventory SHA-256:

```text
20c8738205fc5ef28c7bbff6183179d6c8d11652f47801ab429697222a78de1b
```

It identifies one local verification module, `VERIFICATION`, and six rules.
All six `source_rule_id` values are unique. `trust-boundary.json` preserves
their inventory order and classifies each exactly once.

None of the six canonical rules carries the `simplification` attribute.

## Classifications

All six canonical rules are `DEFINITION`:

1. `rule-e16b3241b5675fa807f7287fd8db8e3e71b24e7b7b130da84250149d7e166ca8`
   expands the macro name `numberKeyClosure` to the exact translated helper
   closure.
2. `rule-5692cca793a2159c984323ca422a6e908349e27acd9f001a5718828b318b0c67`
   expands the macro name `sortNumbersClosure` to the exact translated target
   closure.
3. `rule-9b835db36ee25ad7bebed412bf86771e90764ac448f5b8c18671f2ffdbd65747`
   defines the total predicate `isNumberWord` by the ten permitted string
   values.
4. `rule-e47e06c71c6d44b8fb7a5471bbd23d7a1afd8a6499d2077f4bfcae6064ac294c`
   is the empty-sequence defining case of `allNumberWords`.
5. `rule-fde315ba45836b08d40df28f6a9f608e17b9e5b5a70d717c5ecc140209f4ba29`
   is the structurally recursive defining case of `allNumberWords`.
6. `rule-ea52da411b9ddcd44409f34ea1ec779091c47f11ec46ca66f711f60bd835a10b`
   defines `expectedSortNumbers` as a name for the symbolic
   split/keyed-sort/join result.

The first two are macro expansions. The next three are equations of total
domain predicates, with the recursive rule descending on the `ValSeq` tail.
The last is a nonrecursive result abbreviation. None matches a `<k>` cell or
another execution configuration, observes operational state, or redirects a
program computation, so the canonical set contains no `OPERATIONAL_RULE`.

The occurrence of the supplied `sortKeyVS` symbol on the right-hand side of
the final definition does not turn that naming equation into a domain lemma.
Stage 1 records the semantics' `sortKeyVS` contract as an external trust
boundary, but rules from the supplied reference semantics are outside this
canonical local-rule inventory and are therefore not added to or reformulated
in `trust-boundary.json`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1's `/reference/k-proof/prove.sh` first compiles `verification.k`—with
all six canonical rules already present—into `verification-kompiled`. It then
runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.sort-numbers
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

`/reference/k-proof/prove.out` records `#Top` for both positive runs. Those
runs prove the reachability claims under a definition already containing all
six rules. They do not first prove the exact statement of any canonical rule
against a module that omits that rule, and `prove.sh` has no later step that
installs such a proved statement as a reusable rule. Consequently, the Stage 1
ordering and exact-correspondence requirement for
`PROVED_DERIVED_LEMMA` is not met by any inventory entry.

The ten `_number_key` claims in `spec.k` are separately checked reachability
claims, but they are not rules in the canonical inventory and are not
classified or added to the JSON.

## Domain lemmas

The domain-lemma set is empty.

No canonical rule asserts an additional mathematical fact used to close the
proof. The predicates and result term are introduced by defining equations,
and no local simplification or other trusted mathematical rule appears in the
inventory.
