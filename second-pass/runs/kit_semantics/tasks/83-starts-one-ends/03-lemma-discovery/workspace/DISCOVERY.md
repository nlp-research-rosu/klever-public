# Trust-boundary discovery

## Canonical inventory

The launcher-generated `/reference/rule-inventory.json` is the exhaustive
canonical inventory for this classification. It has schema version `2`,
inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and an empty `rules` array.

Accordingly, there are no canonical `source_rule_id` values to classify.
`trust-boundary.json` preserves the canonical order and classifies every
inventoried rule exactly once: vacuously, because the inventory contains zero
rules.

## Classification results

| Classification | Count | Explanation |
|---|---:|---|
| `DEFINITION` | 0 | No equation, recurrence, macro expansion, or structural helper appears in the canonical inventory. |
| `OPERATIONAL_RULE` | 0 | No local verification-model execution or observation rule appears in the canonical inventory. |
| `PROVED_DERIVED_LEMMA` | 0 | No reusable rule is separately proved before being included in the verification module. |
| `DOMAIN_LEMMA` | 0 | No additional mathematical rule is trusted to close the proof. |

There are no inventoried rules carrying the `simplification` attribute.

## Separately proved derived lemmas

The separately proved derived-lemma set is empty.

The mounted Stage 1 `verification.k` contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

It declares no rule. The mounted Stage 1 `prove.sh` compiles that module and
proves the two target reachability claims in `spec.k`, both individually and
together. It also runs expected-failure body-sensitivity and false-result
probes. It does not first prove the exact statement of any reusable rule
against a module that omits that rule, and it has no later compilation phase
that adds such a rule. Therefore there is no Stage 1 evidence meeting the
required ordering and exact-correspondence test for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No canonical rule contributes an additional
trusted mathematical fact to target-proof closure.

The Stage 1 `PROOF.md` separately gives an informal inclusion-exclusion
argument connecting the returned formula to the HumanEval counting intent.
That prose is not a K rule in the canonical inventory and is therefore not a
`DOMAIN_LEMMA` entry in `trust-boundary.json`.

## Boundary conclusion

There are no local verification rules to add to the rule-level trust boundary.
The target claims close using the imported reference execution semantics
without any inventoried local definition, operational rule, proved derived
lemma, or domain lemma.
