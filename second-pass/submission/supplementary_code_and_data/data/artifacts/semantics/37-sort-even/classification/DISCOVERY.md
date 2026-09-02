# Trust-boundary discovery

The canonical inventory contains 17 rules from `VERIFICATION`. Every
`source_rule_id` is classified exactly once and remains in canonical inventory
order in `trust-boundary.json`.

## Classification basis

- **DEFINITION (11 rules):** `loopBody`, `sortEvenBody`, and
  `sortEvenClosure` name constructor-level proof terms. `evenIndices`,
  `oddIndices`, `pairedVS`, `advancedIndex`, `evenSuffix`, and
  `assembledEvenSort` are equations or recurrences defining the mathematical
  summaries used by the claims.
- **OPERATIONAL_RULE (3 rules):** the specialized `#bindP` rule performs
  ordinary function-parameter binding. The two `#observeResult` rules are
  verification-model observation behavior for heap references and direct
  values.
- **DOMAIN_LEMMA (3 rules):** the right-identity and associativity rules for
  `valSeqConcat`, plus the `"$cells" in_keys(...)` map simplification, add
  mathematical facts about existing operations. All three carry the
  `simplification` attribute. They are already in `verification.k` when the
  Haskell definition is compiled, and `prove.sh` contains no earlier proof of
  their exact statements.
- **PROVED_DERIVED_LEMMA (0 rules):** no canonical inventory rule satisfies
  the required prove-before-introduction ordering.

## Separately proved Stage 1 lemma

Stage 1 does separately prove the `SPEC.loop-correct` reachability claim in
`spec.k` lines 9–49. In `prove.sh` lines 21–26, `verification.k` is first
compiled with all 17 inventoried rules. Lines 29–33 then run `kprove` on
`SPEC.loop-correct`. Lines 37–42 prove the entry claim while selecting both
claims and marking `SPEC.loop-correct` trusted for reuse.

This is valid evidence that the loop claim was independently proved before it
was reused by the entry proof. It does not classify any canonical rule as
`PROVED_DERIVED_LEMMA`: the loop claim is in `spec.k`, is not a rule in the
canonical verification-module inventory, and none of the 17 inventoried rule
statements is first proved against a module that omits that rule.

## Domain-lemma set

The domain-lemma set is **not empty**. It consists of exactly these three
canonical rules:

1. `rule-656b75764c3203134f266be9408944fcc82d61f11a51b6ca12049b4e0fddc5cb`
   — right identity of `valSeqConcat`.
2. `rule-654c2f49cd7e7e59ab81408e4712d1a42c74c6bd59416f943395163de8bed937`
   — associativity of `valSeqConcat`.
3. `rule-e4098f840641d982cc071ea690be2438850392507ef1b3d1e9de094705d06500`
   — removal of five known non-`"$cells"` local keys from the map-membership
   query.
