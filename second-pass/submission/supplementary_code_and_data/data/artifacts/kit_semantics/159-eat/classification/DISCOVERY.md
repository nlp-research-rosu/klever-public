# Rule trust-boundary discovery

## Canonical inventory

The exhaustive canonical inventory is
`/reference/rule-inventory.json`. It identifies `VERIFICATION` as the sole
local verification module and contains zero rules. Its ordered `rules` array
serializes canonically to SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
which is copied unchanged into `trust-boundary.json`.

The mounted `/reference/k-proof/verification.k` contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

Its SHA-256 is
`ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`,
matching the inventory's `verification_sha256`. This independently confirms
that the local verification module declares no rules.

## Classification result

Because the canonical inventory is empty, `trust-boundary.json` has an empty
`rules` array. Every canonical `source_rule_id` is therefore included exactly
once in inventory order, vacuously.

| Classification | Count | Reason |
|---|---:|---|
| `DEFINITION` | 0 | No local equation, recurrence, macro, structural helper, or named proof-term rule is inventoried. |
| `OPERATIONAL_RULE` | 0 | No local execution or observation rule is inventoried. |
| `PROVED_DERIVED_LEMMA` | 0 | No reusable local rule is inventoried, so no rule can qualify through separate prior proof. |
| `DOMAIN_LEMMA` | 0 | No additional local mathematical rule is inventoried. |

There are also zero inventoried rules carrying the `simplification`
attribute, so the special classification restriction for simplification rules
is satisfied without any entries.

Imported rules from the supplied `MPY` reference semantics are not added:
the launcher-generated inventory is explicitly exhaustive for the local
verification-module closure and lists only `VERIFICATION`. Likewise, the
reachability claims in `spec.k` and the negative probes are not canonical rule
entries and are not assigned invented `source_rule_id` values.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The mounted Stage 1 `prove.sh` compiles `verification.k` and proves the target
claims in `spec.k`, but it contains no earlier proof command for a reusable
rule followed by a build that introduces that exact rule. The mounted Stage 1
`PROOF.md` also reports an empty proof-extension inventory and states that
`verification.k` adds no equation, simplification rule, ordinary rewrite, or
auxiliary claim. Consequently, there is no Stage 1 ordering-and-correspondence
evidence that could justify a `PROVED_DERIVED_LEMMA` classification.

## Domain-lemma set

The domain-lemma set is empty.

No additional mathematical fact is present in the canonical local rule
inventory. The finalized proof relies on ordinary execution under the
imported, supplied reference semantics rather than on local trusted domain
lemmas.
