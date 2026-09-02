# Trust-boundary discovery

The canonical source is `/reference/rule-inventory.json`, with inventory hash
`1066209b71a607b520f502ba2fce41fc9fb386169ed80067c8bcb7576819bf34`.
It lists 23 rules, all in the local `VERIFICATION` module. Every canonical
`source_rule_id` is classified exactly once and in canonical order in
`trust-boundary.json`.

## Classification summary

| Classification | Count | Basis |
|---|---:|---|
| `DEFINITION` | 18 | Equations defining proof-local predicates, the named integer projection term, or structurally recursive mathematical summaries. |
| `OPERATIONAL_RULE` | 0 | The inventory contains no ordinary non-simplification execution or observation rule added to the verification model. |
| `PROVED_DERIVED_LEMMA` | 0 | Stage 1 contains no rule-free proof followed by installation of the exact proved rule. |
| `DOMAIN_LEMMA` | 5 | Unproved simplification facts about the partial-cast domain and guarded dispatch through existing operator symbols. |

The `isIntVal` and `definedProjectInt` equations define proof-local predicates.
The guarded cast orientations, collapse, and nested-projection normalization
define and normalize the new `projectIntTotal` proof term. The `allPositive`,
`frequencyOf`, `updateAnswer`, and `searchSummary` cases are base, guarded, or
recursive equations defining mathematical summaries.

The five domain lemmas are:

1. `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`,
   the simplification characterization of when the existing partial
   `Val`-to-`Int` cast is defined.
2. `rule-884f162b67149e88e7eecc28af46f50766a05e73cff70c9f7e167c33b1409e7d`,
   guarded dynamic-`Val` dispatch for integer equality.
3. `rule-ffcf407de56764af73a323c60852665b87709ae760e0a275c8dacf75d96c5f02`,
   guarded dynamic-`Val` dispatch for integer greater-than-or-equal.
4. `rule-3e1ce8e4b12d8d2bae33238dc22c1575ab618c72afa918828d490765e79c8c2c`,
   guarded dynamic-`Val` dispatch for integer greater-than.
5. `rule-45c3bb147f4e28b3f60623a84ce2306b2a8b697607e4388f59b32c4585d29c66`,
   guarded dynamic-`Val` dispatch for integer addition.

These rules carry `simplification`, alter pre-existing cast or operator
reasoning, and are not definitions of those pre-existing symbols. They are
therefore trusted domain facts under the requested taxonomy. Stage 1's concrete
and differential tests support their intended use but do not universally prove
their exact K statements.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical rule inventory.

The Stage 1 `prove.sh` first compiles `verification.k`—including all 23
inventory rules—into `verification-kompiled`, and only then invokes `kprove` on
`spec.k`. It never proves an inventory rule against a module omitting that rule,
nor does it subsequently install a rule whose exact statement corresponds to
such a proof. The successful `kprove.log`, LLVM tests, differential tests, and
negative mutation probes consequently do not satisfy the required ordering for
`PROVED_DERIVED_LEMMA`.

The `inner-loop` and `outer-loop` reachability claims are machine-checked
circularities and are discussed as derived reachability lemmas in Stage 1
`PROOF.md`, but they are claims in `spec.k`, not rules in the canonical local
verification-module inventory. They therefore receive no entry in
`trust-boundary.json`.

## Domain-lemma result

The domain-lemma set is **not empty**. It contains exactly the five
`source_rule_id` values listed above.
