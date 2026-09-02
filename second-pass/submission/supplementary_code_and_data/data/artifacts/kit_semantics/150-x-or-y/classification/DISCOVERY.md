# Trust-boundary discovery

## Canonical scope

The exhaustive source for this classification is
`/reference/rule-inventory.json`, whose recorded inventory SHA-256 is
`246b3d350a4a29f82f499272a975210b22fa01970cdb82b8256b92534fc98419`.
It contains five rules in inventory order, all from module `VERIFICATION`.
Each canonical `source_rule_id` appears exactly once in
`trust-boundary.json`.

The inventory reports no `simplification` attributes. No rule in the
canonical closure matches a `<k>` cell or another execution configuration.

## Classification

All five rules are `DEFINITION`:

1. `rule-cfb2314df4ea697cded9cf0262c9f9148799f41b14471c7e9e6718139a0df7cb`
   is the guarded base equation for `trialChoice`.
2. `rule-7877c000c080d739794dbb3915705fc950212640a5d2b537a5a03a482090b6b0`
   is the zero-remainder recurrence case for `trialChoice`.
3. `rule-8c56ab5c7a8fcd164fb0d555a596cba2218ac3044885d21f8baf67a9b169c995`
   is the nonzero-remainder recurrence case for `trialChoice`.
4. `rule-a0b42dd3540472c0a1673da37721faef739d8c78131d66bce39a209f91709162`
   is the below-two case of the `xOrYSpec` definition.
5. `rule-9fda901ff7675dee4a02c075bdb95e6d8c069630f55a40d4ecadca1361519e44`
   is the at-least-two case of the `xOrYSpec` definition.

The first three rules collectively define a guarded recurrence for a named
mathematical summary. The last two are disjoint, exhaustive cases defining the
total entry summary. They do not intercept Python/MPY execution constructs and
do not state standalone facts about pre-existing mathematical operations.
Accordingly, none is an `OPERATIONAL_RULE` or `DOMAIN_LEMMA`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries in the canonical rule inventory.
Stage 1 compiles `verification.k`, already containing all five inventory rules,
before it runs any proof command. Its `prove.sh` does not first prove the exact
statement of any one of these rules against a module from which that rule is
absent.

Stage 1 does separately prove the reachability claim `SPEC.trial-loop` with:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.trial-loop
```

`/reference/k-proof/PROOF.md` records `#Top` and exit status `0` for that
focused command, and `prove.sh` runs it before the complete-spec proof. This is
evidence for the loop circularity in `spec.k`; it is not evidence that an exact
canonical inventory rule was proved before admission. `SPEC.trial-loop` is a
claim, is absent from the canonical rule inventory, and therefore receives no
entry in `trust-boundary.json`.

## Domain-lemma set

The domain-lemma set is empty.
