# Rule classification discovery

The canonical inventory at `/reference/rule-inventory.json` has schema version
2, inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and an empty `rules` array. Because the launcher-generated inventory is
exhaustive and canonical, there are no local verification-module rules to
classify as `DEFINITION`, `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or
`DOMAIN_LEMMA`.

The mounted Stage 1 `verification.k` confirms this result: module
`VERIFICATION` only imports `MPY` and contains no rule declarations. Rules in
the supplied reference semantics are not canonical inventory entries and
therefore are not added to `trust-boundary.json`.

## Separately proved derived lemmas

There are no separately proved derived lemmas. The Stage 1 `prove.sh` compiles
`VERIFICATION` and proves the target claims in `spec.k`; it does not first
prove an exact reusable rule against a rule-free module and then introduce that
rule. Accordingly, no entry can be classified as `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No additional mathematical fact appears in the
canonical local rule inventory, including no rule carrying the
`simplification` attribute.
