# Trust-boundary rule discovery

## Canonical scope

The exhaustive canonical inventory is
`/reference/rule-inventory.json`. It identifies `VERIFICATION` as the local
verification module, records inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and contains zero rule entries.

The mounted `verification.k` is consistent with that inventory: its
`VERIFICATION` module imports the supplied `MPY` semantics but declares no
rules of its own. Because the launcher inventory is authoritative, imported
reference-semantics rules are not added to or reclassified in this result.

## Classification result

All canonical rules have been classified exactly once in inventory order.
Since the canonical rule array is empty, the result array is also empty:

| Classification | Count |
|---|---:|
| `DEFINITION` | 0 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |
| **Total canonical rules** | **0** |

There are no canonical rules carrying the `simplification` attribute, so the
special classification restriction for such rules is satisfied vacuously.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` builds the rule-free `VERIFICATION` module, proves the
two target claims individually and together, and runs expected-failure
vacuity and body-mutation probes. It does not first prove the exact statement
of any reusable rule against a module lacking that rule and then install that
rule. The Stage 1 `PROOF.md` likewise records that there are no proof-local
functions, equations, simplification rules, ordinary rewrites, operational
bridges, or auxiliary circularities.

Accordingly, there is no Stage 1 proof evidence satisfying the required
ordering and exact-correspondence test for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty.

Stage 1 discusses trusted components of the frozen reference semantics,
including the opaque MD5 primitive and string-encoding model, but those are
not rules in the canonical local verification-module inventory. No additional
mathematical fact was installed in `VERIFICATION` to close the proof.
