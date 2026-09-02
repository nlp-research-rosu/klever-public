# Trust-boundary discovery

## Scope and method

`/reference/rule-inventory.json` is treated as the exhaustive canonical
inventory of the local verification-module closure. It contains nine rules, all
from `VERIFICATION`; this report neither adds rules from the supplied reference
semantics nor treats the reachability claims in `spec.k` as inventory rules.
The output preserves the canonical rule order and
`inventory_sha256` value.

Each rule was checked against the mounted `verification.k`, `prove.sh`,
`spec.k`, and Stage 1 proof report. Equations that introduce and recursively
define proof-local summaries are `DEFINITION`. A rule about an existing
semantic operation is not a definition merely because a comment calls it
derived. `PROVED_DERIVED_LEMMA` requires Stage 1 to first prove the exact rule
against a module that omits that rule.

## Rule classifications

| Inventory order | `source_rule_id` | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-d67f74749887fbf3e482ab3b5e009e306d6afabeb7e2bc1483cdcc5bc5d801aa` | `DEFINITION` | Defines `stringCodes(str(S))` as the contained `IntSeq`. |
| 2 | `rule-fd0940a4d6054e1358229d8416d82d1fdbd9fc9b81a95171ac29cc004419b996` | `DEFINITION` | Supplies the `owise` fallback completing the total proof-local `stringCodes` projection. |
| 3 | `rule-dcec90ae81b6468389e91083acc95d81ead6981ccababa579f6172a0a877a7e3` | `DEFINITION` | Base equation for the `isStringSeq` predicate. |
| 4 | `rule-7a72869f4d1d964b627bb3b06d70211a5e2d1d60583ce2a867ccbb8d7b284747` | `DEFINITION` | Structural cons recurrence for `isStringSeq`. |
| 5 | `rule-caaa68653c6b00f190e89bd450eb4b1da239abda96d0efd431698e876453410d` | `DEFINITION` | Empty-tail base equation for the `concatFrom` summary. |
| 6 | `rule-164607b7d03894ef15a07854149cb03c9b9031a6e6187bd89611899d0aaac54e` | `DEFINITION` | Guarded structural recurrence for `concatFrom`. |
| 7 | `rule-2bc2a66c772aae97380ca3ab3abdcf702833b825027b9f8fc0da1fe4878d02ac` | `DEFINITION` | Empty-tail base equation for the `lastFrom` summary. |
| 8 | `rule-8d075e2e7a462abce866779cfe5fc6c30b077acc04bc848e0e0bb58c1da430da` | `DEFINITION` | Guarded structural recurrence for `lastFrom`. |
| 9 | `rule-d77f984813dd200ec980ca7e00225a96be53f3a6ed10be91093061eb9e528506` | `DOMAIN_LEMMA` | Adds a simplification fact for the already-defined MPY `applyBin` operation. It is not a defining equation for a new proof-local term and is not separately proved before use. |

No canonical rule is classified as `OPERATIONAL_RULE`: none of the nine rules
is an ordinary execution or observation rule added to the verification model.
The operational Python rules are supplied by imported MPY modules and are
outside this canonical local-rule inventory.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

Stage 1 `prove.sh` first compiles `verification.k` as module `VERIFICATION`.
That compilation already contains all nine canonical rules. It then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The later `kprove` commands target `spec-vacuity.k` and
`spec-body-mutation.k` as expected-failure validation probes. No Stage 1
command constructs a module without the `applyBin` simplification rule and
proves that rule's exact statement before adding it. Consequently, neither the
comment “Derived symbolic normalization” nor the successful target proof is
evidence for the stricter `PROVED_DERIVED_LEMMA` classification.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

```text
rule-d77f984813dd200ec980ca7e00225a96be53f3a6ed10be91093061eb9e528506
```

This is the guarded `[simplification]` rule for
`applyBin("+", str(A), V)`. Stage 1 argues that its guard makes it agree with
the fixed concrete-string addition equation, but the rule itself is present in
the compiled positive-proof module and has no separate earlier proof. Under
the required taxonomy, it is therefore a trusted `DOMAIN_LEMMA`.
