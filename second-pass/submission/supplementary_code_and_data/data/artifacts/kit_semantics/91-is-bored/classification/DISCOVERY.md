# Trust-boundary discovery

## Canonical scope

`/reference/rule-inventory.json` is the canonical inventory used for this
classification. Its `inventory_sha256` is
`c52fa2a5b96c79c46b9f6eea4cc8d3d034a6a20c005da213b247fb8b3b3d5577`.
It contains exactly one rule, and `trust-boundary.json` preserves that rule's
inventory position and `source_rule_id`.

The sole rule has the attribute `priority(40)`. It has no `simplification`
attribute, so the special restriction on simplification rules is satisfied
vacuously.

## Classification

`rule-202b06d05541325e5aaf0e76d47ae510afce49eaa2aabb95863e7e1250b712ef`
is classified as `PROVED_DERIVED_LEMMA`.

Behaviorally, the rule is an operational loop summary: it replaces the exact
`#loop` execution and its fixed continuation with `scanResult`, while updating
the environment, scopes, scope location, stack, and return-related cells.
It qualifies for the more specific proved-derived classification because its
entire accepted configuration and rewrite was machine-proved before the rule
was added to the compiled verification module.

It is not a `DEFINITION`: it rewrites an active MPY configuration rather than
defining a mathematical helper. It is not an unproved `OPERATIONAL_RULE`,
because the exact operational rewrite has prior proof evidence. It is not a
`DOMAIN_LEMMA`, because no additional mathematical fact is assumed to admit
the rewrite.

## Separately proved derived lemmas and evidence

There is exactly one separately proved derived lemma in the canonical
inventory: the loop rule identified above.

The mounted Stage 1 evidence is:

1. `loop-spec.k` declares `LOOP-SPEC.loop` over the same 43-line configuration
   and rewrite payload as the rule in `verification.k`. The rule's
   `priority(40)` attribute affects rule application order but is not an
   additional logical premise or conclusion.
2. `LOOP-SPEC` imports `VERIFICATION-BASE`. `verification-base.k` imports the
   supplied `MPY` semantics and does not import `VERIFICATION`, mention the
   inventoried `source_rule_id`, or contain the inventoried rule text.
3. In `prove.sh`, lines 30–33 compile `verification-base.k`; lines 34–37 run
   `kprove loop-spec.k --definition verification-base-kompiled --spec-module
   LOOP-SPEC`; and only afterward, at lines 39–42, is `verification.k`
   compiled with the derived rule present.
4. The mounted `loop-proof.out` contains `#Top`. Because `prove.sh` uses
   `set -euo pipefail`, this positive proof is part of the successful ordered
   Stage 1 run documented in `PROOF.md`.

The earlier `CONNECTION-SPEC` proof concerns rules outside the canonical
inventory supplied for this task, so it contributes supporting Stage 1
evidence but creates no additional `source_rule_id` to classify here.

## Domain-lemma set

The domain-lemma set is empty. No canonical rule is an unproved mathematical
fact trusted to close the finalized K proof.
