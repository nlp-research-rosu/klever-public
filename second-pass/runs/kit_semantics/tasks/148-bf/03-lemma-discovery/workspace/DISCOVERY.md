# Trust-boundary discovery

## Canonical source

This classification uses `/reference/rule-inventory.json` as the exhaustive
canonical inventory for the local verification-module closure. Its copied
`inventory_sha256` is:

```text
16428e5ee7ce644b84ef8ad08e4e7f58213de2531a5bd36080bafebea24f7093
```

The inventory contains 17 rules, all from module `VERIFICATION`. Each
`source_rule_id` appears exactly once in `trust-boundary.json`, in canonical
inventory order.

## Classification result

| Classification | Count |
|---|---:|
| `DEFINITION` | 17 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

All 17 rules are definitions:

- `bfBody`, `bfModule`, and `bfCall` are macro expansions defining named MPY
  program terms. They expand to ordinary syntax that the imported reference
  semantics executes; they are not local execution rules.
- `planetValues` defines the ordered mathematical sequence of planet values.
- The nine `planetIndex` equations are the eight singleton name cases plus the
  exact complementary invalid-name case. Together they define the total
  summary function.
- `betweenPlanets` defines the composition of the two index lookups with
  `betweenIndices`.
- The three `betweenIndices` equations define the invalid, forward, and
  reverse-or-equal cases of the result sequence. Their guards partition the
  index cases used by the summary.

No canonical rule carries the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The mounted Stage 1 `prove.sh` first compiles `verification.k` as module
`VERIFICATION`, with every canonical local rule already present, and then runs:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.bf-correct
```

That command proves the target reachability claim; it does not first prove the
exact statement of any reusable inventory rule against a module omitting that
rule. The other two `kprove` invocations are expected-failure
false-postcondition and changed-body probes. They also do not establish any
inventory rule before admission. Therefore none of the 17 rules qualifies as
`PROVED_DERIVED_LEMMA`.

## Operational-rule boundary

The canonical local closure contains no ordinary execution or observation
rules, so the `OPERATIONAL_RULE` set is empty. Execution is supplied by the
imported `MPY` reference semantics, but its rules are not entries in the
launcher-generated canonical inventory and are not added to this
classification.

## Domain-lemma boundary

The domain-lemma set is empty. No local rule asserts an additional trusted
mathematical fact beyond the macro and summary definitions described above.
