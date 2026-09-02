# Trust-boundary rule discovery

## Scope and canonical source

This classification uses `/reference/rule-inventory.json` as the exhaustive
canonical inventory of the local verification-module closure. Its copied
inventory digest is
`f0ac74e960f507aef4fa9453b392fd9c8075bd1ed5b645532becd82a9e24645f`.
The inventory contains 16 rules, all in `VERIFICATION`; every canonical
`source_rule_id` appears exactly once and in inventory order in
`trust-boundary.json`.

The mounted Stage 1 files under `/reference/k-proof` were read only. No Stage 1
artifact was edited or copied.

## Classification result

- `DEFINITION`: 16 rules.
- `OPERATIONAL_RULE`: 0 rules.
- `PROVED_DERIVED_LEMMA`: 0 rules.
- `DOMAIN_LEMMA`: 0 rules.

All 16 rules are equations or structural recurrences defining declared
proof-local functions:

- `parenCodes` defines the parenthesis-code input predicate.
- `nextBalance` and `scanBalance` define the balance fold.
- `nextMinimum` and `scanMinimum` define the minimum-prefix fold.
- `scanLast` defines the final persistent loop-target value.
- `goodParens`, `possibleMatch`, and `matchAnswer` define the named result
  predicates and answer.

None of the canonical rules matches a `<k>` cell or another execution-state
cell, observes a program operation, or advances execution. Consequently none
is an `OPERATIONAL_RULE`.

The two rules carrying the `simplification` attribute are the guarded
`nextBalance` cases. Their guards (`C ==Int 40` and `C =/=Int 40`) are
complementary, and their right-hand sides are the defining cases of the
`nextBalance` function. They are therefore classified as `DEFINITION`, not as
trusted mathematical facts.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical rule inventory.

Stage 1 `prove.sh` compiles `verification.k` with all 16 inventory rules already
present and then runs:

```text
kprove spec.k ... --claims SPEC.loop-first
kprove spec.k ... --claims SPEC.loop-second
kprove spec.k ... --spec-module SPEC
```

The first two commands separately prove reachability claims in `spec.k`; those
claims are not rules in the canonical inventory and are not exact statements
of any inventory rule. The full-spec command proves the target claims under the
already compiled verification module. No Stage 1 command first proves an
inventory rule against a module that omits that rule and then imports the exact
proved statement. The mutation probes likewise establish expected failure, not
a reusable rule. Therefore no rule meets the required
`PROVED_DERIVED_LEMMA` evidence ordering.

## Domain-lemma set

The domain-lemma set is empty. No canonical rule adds a mathematical fact
beyond the equations defining the named summaries and predicates.
