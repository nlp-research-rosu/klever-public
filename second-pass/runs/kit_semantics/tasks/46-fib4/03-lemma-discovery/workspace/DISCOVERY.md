# Trust-boundary discovery

## Canonical scope

The sole rule source for this classification is
`/reference/rule-inventory.json`, whose canonical `inventory_sha256` is
`551c2ad2e058ea51404c32413dec9df6da2982ef848827af03a8fbd7d13181d9`.
It contains five rules, all in the local `VERIFICATION` module. The JSON output
preserves their inventory order and includes each `source_rule_id` exactly once.

The mounted Stage 1 `verification.k`, `spec.k`, and `prove.sh` were inspected
read-only to determine semantic role and proof ordering. Imported MPY semantics
rules are outside the launcher-declared canonical inventory and therefore are
not added to this classification.

## Rule classifications

| Inventory position | Source rule | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-293fdb8b1d4095ddc8eddd99c97d4c5b4818a9cdd792bb6b4caad600ddbaf296` | `DEFINITION` | Defines the totalized `fib4Spec` value as zero when `N <= 0`. |
| 2 | `rule-aefe9a8e0afe275fcdfc27000ccbac76a17a6ee88013c84c8f5f1b5213f62614` | `DEFINITION` | Defines the `fib4Spec(1)` base value. |
| 3 | `rule-b63d3b98fbeab97d51b6a9f210a585da08c78b0dba0660d7aa24fe8f9b52ac46` | `DEFINITION` | Defines the `fib4Spec(2)` base value. |
| 4 | `rule-ae0f386ab9647cf6bacccb9eec146bdadc0897e261591027a72b14b464abe92c` | `DEFINITION` | Defines the `fib4Spec(3)` base value. |
| 5 | `rule-d44d71dd060859619764bc0fe005a75f61253b9f2ffa46e35b48b4b028aaeca1` | `DEFINITION` | Defines the guarded four-term recurrence for `N >= 4`; recursive indices strictly decrease. |

Together these rules define one total mathematical summary. Their cases are
exhaustive over K integers and pairwise disjoint: `N <= 0`, the exact values
`1`, `2`, and `3`, and `N >= 4`. None matches a configuration cell or a program
term, so none is an `OPERATIONAL_RULE`.

The inventory reports no `simplification` attribute on any rule. No rule needs
the special simplification-rule restriction.

## Separately proved derived lemmas

There are no separately proved derived rules in the canonical inventory.

Stage 1 `prove.sh` first kompiles `verification.k`, which already contains all
five inventory rules, and only afterward runs `kprove`. It never proves the
exact statement of one of these rules against a module that omits that rule and
then imports the proved statement as a reusable rule. Consequently, none meets
the required evidence ordering for `PROVED_DERIVED_LEMMA`.

`prove.sh` does separately run the `SPEC.loop-invariant` reachability claim
before running the complete spec, and that focused command reports `#Top` in
the Stage 1 record. That object is a claim in `spec.k`, not a reusable rule in
the canonical verification-module rule inventory. Moreover, its proof module
imports the already compiled five definitions. It therefore does not cause any
canonical rule to be classified as `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. The inventory has no additional mathematical
fact layered over an independently defined summary: every canonical rule is
part of the base-case or recurrence definition of `fib4Spec`.

## Classification counts

- `DEFINITION`: 5
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0
