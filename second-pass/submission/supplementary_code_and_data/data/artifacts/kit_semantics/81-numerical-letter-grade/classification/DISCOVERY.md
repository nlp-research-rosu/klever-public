# Trust-boundary discovery

The canonical source is `/reference/rule-inventory.json`, with inventory SHA-256:

```text
00b871c4197f4e4b8c563bbbfd4e2d0186e6f8ce8b19b803de1e23228bec6727
```

It contains 16 rules, all in the local `VERIFICATION` module closure. Every
canonical `source_rule_id` is classified exactly once and retained in canonical
inventory order in `trust-boundary.json`.

## Classification summary

| Classification | Count |
|---|---:|
| `DEFINITION` | 14 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 2 |

The 14 definitions are:

- the `GRADE-STEP` and `GRADE-PROGRAM` compile-time macro expansions;
- `isGradeNumber` and the two equations defining `allGradeNumbers`;
- the three exhaustive equations for `gradeEq`;
- the three exhaustive equations for `gradeGt`;
- the grading-table equation for `gradeValue`; and
- the base and recursive equations for `gradeAcc`.

These rules introduce or recursively define named syntax, predicates, and
mathematical summaries. They do not add standalone mathematical facts about an
already defined symbol.

No inventoried rule is an `OPERATIONAL_RULE`. The inventory is limited to the
local verification module, and its rules are macros, proof helpers, summary
equations, or simplifications; the ordinary MPY execution model is imported
from the read-only reference semantics and is not present in this canonical
local inventory.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1 `prove.sh` first compiles `verification.k` as module `VERIFICATION`, so
all 16 inventoried rules are already present in `verification-kompiled`. It then
runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

That command proves the reachability claims under the theory containing the
inventoried rules. It does not first prove the exact statement of any reusable
inventoried rule against a module from which that rule is absent.

The false-postcondition probe in `spec-vacuity.k` and the body-sensitivity probe
in `spec-body-mutation.k` are negative validation evidence. Neither is a
positive, rule-free proof of an inventoried rule's exact statement. The KAST
comparison proves macro expansion identity as an artifact check, but it is not
a `kprove` proof establishing a reusable rule before that rule is introduced.
Therefore the `PROVED_DERIVED_LEMMA` set is empty.

## Domain lemmas

The domain-lemma set is not empty. It contains exactly these two simplification
rules:

1. `rule-bb0819476c6343e9119c99a78b2ae8eb72ebad42dbc170a9eaa3c4af6f39f115`
   rewrites guarded dynamic `applyCmp("==", V, F)` to `gradeEq(V, F)`.
2. `rule-79c1c8d9ff74acff507b7b4a319ee7d9d034df3550afdf9196f29291297713c8`
   rewrites guarded dynamic `applyCmp(">", V, F)` to `gradeGt(V, F)`.

Both rules carry the `simplification` attribute. They state additional guarded
facts about the pre-existing operational `applyCmp` symbol and are used to
connect symbolic dynamic `Val` operands to the newly defined comparison
summaries. Stage 1 comments and `PROOF.md` describe them as guarded dispatch
restatements, but the required evidence ordering for
`PROVED_DERIVED_LEMMA` is absent: the rules are included in the module used by
the positive target proof. Under the requested taxonomy, they are consequently
trusted `DOMAIN_LEMMA` entries.

All simplification-attributed inventory rules are thus classified as
`DOMAIN_LEMMA`; none is classified as `OPERATIONAL_RULE` or
`PROVED_DERIVED_LEMMA`.
