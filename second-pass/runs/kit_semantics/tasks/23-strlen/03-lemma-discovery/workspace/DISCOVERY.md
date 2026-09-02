# Trust-boundary discovery

## Canonical inventory

`/reference/rule-inventory.json` is the exhaustive canonical inventory for the
local verification-module closure. It has schema version 2, inventory SHA-256
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`,
and an empty `rules` array.

Accordingly, there are zero canonical rules to classify. The output preserves
that hash and inventory order with an empty `rules` array. Every canonical
`source_rule_id` is therefore classified exactly once, vacuously, and no rule
outside the canonical inventory has been added.

## Stage 1 confirmation

The mounted `/reference/k-proof/verification.k` contains only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

It declares no equation, recurrence, macro, structural helper, execution rule,
observation rule, simplification rule, or reusable mathematical lemma. This
agrees with the canonical inventory's `verification_modules` value of
`["VERIFICATION"]` and its zero-rule result.

The reachability claim `SPEC.strlen` is in `/reference/k-proof/spec.k`, not a
rule in the canonical verification-module inventory. The rules in the supplied
reference semantics are likewise not canonical `source_rule_id` entries for
this discovery task, so they are not added to or reformulated in
`trust-boundary.json`.

## Classification results

The counts are:

- `DEFINITION`: 0
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

There are no rules carrying the `simplification` attribute, so the special
classification restriction for simplification rules is satisfied.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1's `/reference/k-proof/prove.sh` compiles the import-only
`verification.k` and proves the target reachability claim in `spec.k`. It also
runs expected-failure postcondition and body-mutation probes. It does not first
prove the exact statement of any reusable rule against a module omitting that
rule, and it does not subsequently install such a rule. The `#Top` recorded in
`/reference/k-proof/proof-run.log` is evidence for `SPEC.strlen`, not evidence
for a `PROVED_DERIVED_LEMMA` classification.

## Domain-lemma set

The domain-lemma set is empty. No additional mathematical fact is present in
the canonical inventory or trusted locally to close the Stage 1 proof.
