# Trust-boundary rule discovery

## Canonical inventory

The exhaustive launcher-generated inventory at
`/reference/rule-inventory.json` has schema version 2, inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and zero rules. Its verification-module closure contains only `VERIFICATION`.

The mounted `verification.k` confirms why the inventory is empty:
`VERIFICATION` imports the supplied `MPY` reference semantics but declares no
rules of its own. The imported reference-semantics rules are part of the fixed
verification model and are outside the canonical local-rule inventory; they
were therefore not added to or classified in `trust-boundary.json`.

## Classification result

Every canonical rule is classified exactly once. Because the canonical
inventory contains no rules, the `rules` array is empty and the classification
counts are:

- `DEFINITION`: 0
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

There are no inventoried rules carrying the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1 `prove.sh` compiles `verification.k` and proves the target reachability
claim in `spec.k`. It does not first prove the exact statement of any reusable
rule against a module lacking that rule and then install that rule into the
verification-module closure. The negative vacuity and body-mutation probes are
validation evidence, not proofs of reusable derived rules. Accordingly, no
entry is classified as `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. The local verification-module closure adds no
mathematical facts trusted to close the K proof.
