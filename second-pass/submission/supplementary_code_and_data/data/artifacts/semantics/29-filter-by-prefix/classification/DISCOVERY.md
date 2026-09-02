# K proof trust-boundary discovery

The canonical inventory has nine rules, all from the Stage 1 `VERIFICATION`
module. Each is classified exactly once and in canonical inventory order in
`trust-boundary.json`.

## Classification basis

- `filterByPrefixDef` is a `DEFINITION`: it is a macro equation naming the
  exact translated function AST used by the proof.
- The empty and nonempty `stringList` iterator rules are
  `OPERATIONAL_RULE`s. They define verification-model execution steps in the
  `<k>` cell: termination for an empty iterator, and head emission plus a
  residual iterator for a nonempty one.
- The three `prefixFilter` simplification rules are `DEFINITION`s. Together
  they are the base case and two guarded recursive cases of the mathematical
  result summary. Their `simplification` attributes do not turn these defining
  equations into lemmas.
- The returned-list `#checkFilter` rule is an `OPERATIONAL_RULE`: it observes a
  heap-allocated result and reduces the check to structural K equality.
- The right-identity and associativity rules for `valSeqConcat` are
  `DOMAIN_LEMMA`s. They add mathematical facts beyond the supplied
  first-argument recurrence for `valSeqConcat` and are trusted simplifiers in
  the proof definition.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` compiles `verification.k` into
`verification-kompiled` before invoking:

```sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module FILTER-BY-PREFIX-SPEC
```

Consequently, both `valSeqConcat` rules are already present while the loop and
end-to-end claims are proved. Stage 1 does not first prove either exact rule
against a module that excludes it, so the successful `kprove` run is not
separate derived-lemma evidence. No other inventory rule has such prior,
exact-statement proof evidence either.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

- `rule-656b75764c3203134f266be9408944fcc82d61f11a51b6ca12049b4e0fddc5cb`
  — right identity, `valSeqConcat(VS, .ValSeq) => VS`.
- `rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97`
  — associativity of `valSeqConcat`.

All five rules carrying the `simplification` attribute are therefore
classified as required: the three `prefixFilter` equations are
`DEFINITION`s, and the two additional concatenation facts are
`DOMAIN_LEMMA`s.
