# Trust-boundary discovery

## Canonical source

The exhaustive source is `/reference/rule-inventory.json`, with
`inventory_sha256`:

```text
36b7269f531b8499a3ecc5033b85b9cbd19024d07da31b455cd99ab6ca61e21c
```

It contains 13 rules from the local `VERIFICATION-SYNTAX`/`VERIFICATION`
closure. `trust-boundary.json` preserves their canonical order and classifies
each `source_rule_id` exactly once.

## Classification result

| Canonical inventory positions | Classification | Reason |
|---|---|---|
| 1–3 | `DEFINITION` | Structural equations defining `allInts` and `definedProjectInt`. |
| 4 | `DOMAIN_LEMMA` | Additional `#Ceil` characterization of the existing partial Val-to-Int cast. |
| 5–8 | `DEFINITION` | Guarded defining and canonicalization equations for the new named proof term `projectIntTotal`. |
| 9–10 | `DOMAIN_LEMMA` | Additional guarded simplification facts about the existing MPY `applyBin` operations `%` and `+`. |
| 11–13 | `DEFINITION` | Structural recurrence defining the mathematical result summary `addSummary`. |

The rules defining `allInts` and `addSummary` are exhaustive structural
recurrences. `definedProjectInt` and the `projectIntTotal` equations introduce
and normalize named proof terms, so they are definitions rather than claims of
separate Stage 1 theorems.

The three `DOMAIN_LEMMA` rules instead assert facts about constructs already
owned by K or MPY:

- `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
  characterizes `#Ceil` for the existing partial cast.
- `rule-2dd919bc012c069b3c8fffc3cbdb9c9070068f0c8eca42acdc492a3b3db5315a`
  widens MPY integer remainder dispatch to an `isInt`-guarded `Val`.
- `rule-573796c5ae90b21570a38c51e4cd10a1610683b2a2b51c68ff466ef5277fc7fc`
  widens MPY integer addition dispatch to an `isInt`-guarded `Val`.

All seven rules carrying a `simplification` attribute are classified as either
`DEFINITION` or `DOMAIN_LEMMA`, as required.

No canonical rule is an `OPERATIONAL_RULE`. The inventory contains proof-local
equations and simplifications, not an ordinary K-cell execution or observation
rule. In particular, the `%` and `+` twins carry `simplification`, so the
required taxonomy places their unproved mathematical correspondence in
`DOMAIN_LEMMA`, not `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 evidence establishes this directly:

1. `/reference/k-proof/prove.sh` first kompiles `verification.k` as module
   `VERIFICATION`, so all 13 canonical rules are already present in
   `verification-kompiled`.
2. It then proves `SPEC.add-loop` and the complete `SPEC` against that compiled
   definition.
3. The vacuity and body-mutation probes also import and use the same complete
   `VERIFICATION` module.
4. No Stage 1 module omits an inventory rule and proves that rule's exact
   statement before the rule is admitted.

Consequently, target-proof `#Top` results, negative mutation probes, comments
calling rules “lemmas,” and differential tests do not meet the required
ordering for `PROVED_DERIVED_LEMMA`. The `PROVED_DERIVED_LEMMA` set is empty.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly the three canonical
rules listed above: the partial-cast `#Ceil` characterization and the guarded
`applyBin` facts for `%` and `+`.
