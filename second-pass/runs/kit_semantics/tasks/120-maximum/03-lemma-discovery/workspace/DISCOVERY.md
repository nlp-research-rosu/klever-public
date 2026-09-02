# Lemma Discovery

## Canonical inventory

The exhaustive canonical inventory is
`/reference/rule-inventory.json`, with inventory SHA-256:

```text
a5c14e04fab2c20c7620b8979b4cc4b4eb2232e21babb1d076942b24e60bf083
```

It contains one rule. `trust-boundary.json` preserves that sole
`source_rule_id` in inventory order and classifies it exactly once.

## Classification

### `rule-fbc012b3ef8f9433c0af203532037974f8c0298dcbdd8c0b25f3729ff47074f9`

Classification: `DEFINITION`.

This is the unconditional equation at
`/reference/k-proof/verification.k:9` for the `[function, total]` symbol
`maximumResult(ValSeq, Int)`. It expands the named result summary to:

```k
doSlice(
  list(sortVS(VS)),
  someB(vsLen(VS) -Int K),
  noB,
  noB)
```

The rule is nonrecursive and defines a proof term. It does not match a
configuration cell, execute or observe a program step, or assert an additional
mathematical property of the terms on its right-hand side. Stage 1 also
describes it as the sole definitional summary in `PROOF.md` and records that
there are no proof-local derived lemmas, simplification rules, or operational
bridges.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The ordering required for that classification is absent: Stage 1 `prove.sh`
first compiles `verification.k`, including the `maximumResult` equation, at
lines 23–26 and then runs `kprove` against that compiled definition at lines
28–30. It does not first prove the equation's exact statement against a module
that omits the rule. The later vacuity and body-mutation commands import the
same compiled definition and are negative probes, not proofs of this equation.

## Domain lemmas

The domain-lemma set is empty.

The canonical inventory contains no rule that contributes an additional
trusted mathematical fact and no rule carrying the `simplification` attribute.
The Stage 1 report separately identifies the supplied semantics' opaque
`sortVS` contract as an external trust boundary, but `sortVS` contributes no
rule to this canonical local verification-module inventory and therefore has
no entry to classify here.

## Coverage

Classification totals:

- `DEFINITION`: 1
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

Total classified rules: 1 of 1, with no duplicates or omissions.
