# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with inventory
SHA-256:

```text
9eaebbd4fb6dd63f68a3e126ff644a5f975c58ce19f8951223c1ce18c21c72c8
```

All 16 canonical rules are classified exactly once and remain in canonical
inventory order in `trust-boundary.json`.

## Classification method

Rules 1–4 in inventory order are macro expansions. `innerBody`, `outerBody`,
`countBody`, and the validation-only `countBodyStart3` define named AST proof
terms. The requested classification definition expressly includes macro
expansions, so all four are `DEFINITION`.

Rules 5–14 are the guarded equations for `noDivisors`, `primesBetween`, and
`primesBelow`. They supply base cases, recursive cases, totalization, and the
prime/non-prime case split for mathematical summaries. They do not match a K
configuration cell or add an execution/observation step. All ten are
`DEFINITION`.

Rules 15–16 are the two rules with the `simplification` attribute:

- `rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97`
  states associativity of `valSeqConcat`.
- `rule-1bc30aceb4ec6e423c8f79079ea7b1c195de5d88396229aa8ee74794085384fa`
  states that `.ValSeq` is a right identity for `valSeqConcat`.

These rules add reusable mathematical facts about the already-defined
`valSeqConcat` operation; they are not equations defining a new summary
symbol. Both are therefore `DOMAIN_LEMMA`.

No canonical rule matches execution cells or defines a step of the
verification model, so the `OPERATIONAL_RULE` set is empty.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications.

Stage 1's `prove.sh` kompiles `verification.k` directly, with both
`valSeqConcat` simplification rules already present, and then runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

It does not first prove either exact simplification statement against a module
that omits that rule. The comments in `verification.k` and `PROOF.md` describe
a structural-induction justification, but that prose is not the required
separate Stage 1 K proof evidence and cannot support
`PROVED_DERIVED_LEMMA`.

## Domain-lemma boundary

The domain-lemma set is **not empty**. It contains exactly the two
`valSeqConcat` simplification rules listed above. These are the only canonical
rules that the finalized proof trusts as additional mathematical facts.
