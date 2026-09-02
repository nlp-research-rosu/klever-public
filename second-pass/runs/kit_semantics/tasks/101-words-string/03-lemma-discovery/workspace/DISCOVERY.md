# Trust-boundary discovery

## Canonical scope

`/reference/rule-inventory.json` is the exhaustive canonical inventory for the
local verification-module closure. It names only `VERIFICATION` in
`verification_modules`, gives inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and contains zero rule records.

Accordingly, `trust-boundary.json` contains an empty `rules` array. This
classifies every canonical rule exactly once in inventory order because the
canonical rule set is empty. Rules from the imported, supplied `MPY` reference
semantics are not added: they are outside the launcher-defined local inventory
and expanding the scope would contradict the canonical inventory.

The mounted `verification.k` corroborates that scope: module `VERIFICATION`
imports `MPY` but declares no local rules, functions, equations,
simplification rules, macros, or structural helpers. The claims in `spec.k`
and the two negative-probe specs are proof obligations, not canonical rule
records.

## Classification results

There are no entries to classify as `DEFINITION`, `OPERATIONAL_RULE`,
`PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`. In particular, the canonical
inventory contains no rule carrying the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` compiles `verification.k`, proves the target claim in
`spec.k`, and runs two expected-failure validation probes. It does not first
prove any reusable rule against a module omitting that rule and then add the
exact rule to the verification closure. This agrees with the empty canonical
inventory and with Stage 1 `PROOF.md`, whose proof-extension inventory is
explicitly empty.

## Domain lemmas

The domain-lemma set is empty.
