# Trust-boundary discovery

The canonical inventory contains eight rules, all from the `VERIFICATION`
module. They are exactly the equations defining four mathematical summaries:
`noFactor`, `isPrime`, `primesFrom`, and `primesBelow`. Accordingly, every
inventory rule is classified as `DEFINITION`.

The three `noFactor` rules are the base, divisor-found, and recursive
nondivisor cases of the bounded divisor search. The two `isPrime` rules define
the below-two case and reduce the remaining domain to `noFactor`. The two
`primesFrom` rules define the empty interval and recursive conditional-cons
cases. The final rule defines `primesBelow` as `primesFrom(2, N)`.

No inventory rule has the `simplification` attribute. No inventory rule is an
execution or observation transition, so the canonical inventory has no
`OPERATIONAL_RULE` entries. The operational `scan`, `trial`, `prependIf`, AST
lowering, and return rules are in Stage 1's `MPY` semantics, but they are not
members of the launcher-provided canonical inventory and therefore are not
added to this classification file.

## Proved-derived-lemma audit

There are no separately proved derived lemmas in the canonical inventory.
Stage 1 `prove.sh` line 19 compiles `verification.k`—already containing all
eight inventoried rules—into `verification-kompiled`. Line 20 then invokes one
`kprove` command against that definition. Thus no inventoried rule is first
proved against a module that omits it and subsequently installed as an
exactly corresponding reusable rule.

Stage 1 `spec.k` contains the claims `trial-correct`, `scan-correct`, and
`count-up-to-correct`, and the single `kprove` invocation proves those claims.
They are claims rather than rules in the canonical inventory, and the Stage 1
artifacts show no separate prove-then-add ordering for an exact rule
corresponding to any of them. Consequently, no inventory entry is classified
as `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. The inventory introduces no additional
mathematical fact beyond the defining recurrences and aliases described
above.
