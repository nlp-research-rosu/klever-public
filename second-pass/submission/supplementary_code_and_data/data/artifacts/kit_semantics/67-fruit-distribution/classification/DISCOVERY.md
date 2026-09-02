# Trust-boundary discovery

## Canonical inventory

The exhaustive canonical inventory is
`/reference/rule-inventory.json`. It has schema version 2, inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and an empty `rules` array. Its local verification-module closure contains only
`VERIFICATION`.

The mounted `/reference/k-proof/verification.k` confirms why the inventory is
empty: `VERIFICATION` imports the supplied `MPY` semantics but declares no
local rules. Because the launcher inventory is authoritative, imported
reference-semantics rules outside that local closure are not added here.

## Classification result

There are zero canonical rules to classify. Accordingly,
`trust-boundary.json` preserves inventory order with an empty `rules` array.
Every allowed classification has count zero:

- `DEFINITION`: 0
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

No simplification-attributed rule appears in the canonical inventory.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` compiles `verification.k` and proves the target claim in
`spec.k`; it also runs two expected-failure mutation claims. It does not first
prove an exact reusable rule against a module lacking that rule and then admit
the corresponding rule into `VERIFICATION`. This agrees with the Stage 1
`PROOF.md`, which records that `verification.k` declares no functions,
equations, simplifications, ordinary rewrites, operational bridges, trusted
primitives, or auxiliary claims. The positive Stage 1 evidence is
`proof-target.log`, whose proof result is `#Top`, but that target claim is not a
derived rule in the canonical inventory.

## Domain lemmas

The domain-lemma set is empty.

No additional mathematical fact is present as a local verification rule, so
there is no `DOMAIN_LEMMA` trust assumption to report for this inventory.
