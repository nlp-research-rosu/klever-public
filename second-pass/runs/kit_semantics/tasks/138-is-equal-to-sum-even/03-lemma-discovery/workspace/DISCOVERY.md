# Trust-boundary classification

The exhaustive canonical inventory at
`/reference/rule-inventory.json` has schema version 2, inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and an empty `rules` array. Consequently, there are no canonical
`source_rule_id` values to classify. The `DEFINITION`, `OPERATIONAL_RULE`,
`PROVED_DERIVED_LEMMA`, and `DOMAIN_LEMMA` sets are all empty. The restriction
on rules carrying the `simplification` attribute is therefore satisfied
vacuously.

This agrees with the mounted Stage 1 artifacts:
`/reference/k-proof/verification.k` contains only the `VERIFICATION` module and
an import of the supplied `MPY` semantics; it declares no rules. The sole
positive `kprove` command in `/reference/k-proof/prove.sh` proves the target
reachability claim from `/reference/k-proof/spec.k`. It does not first prove
the exact statement of any reusable rule against a rule-free module and then
install that rule.

## Separately proved derived lemmas

There are no separately proved derived lemmas. The Stage 1 evidence contains
no canonical rule statement for which the ordering and exact-correspondence
requirements of `PROVED_DERIVED_LEMMA` could be demonstrated.

## Domain lemmas

The domain-lemma set is empty. Stage 1 adds no mathematical rule to the local
verification-module closure.
