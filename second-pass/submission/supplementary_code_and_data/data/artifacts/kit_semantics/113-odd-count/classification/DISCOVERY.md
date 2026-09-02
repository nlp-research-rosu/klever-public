# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`
`84c56c6d77a6c8573f9c1eff1b9d516b8e8f84abb998ce1cf8f36e219de6f41a`.
It contains 12 rules from the local `VERIFICATION` closure. Every canonical
`source_rule_id` appears exactly once and in canonical order in
`trust-boundary.json`.

## Classification method

The audit used the canonical rule text and attributes, then checked the mounted
Stage 1 `verification.k`, `prove.sh`, `projection-spec.k`, `spec.k`, and proof
outputs. Comments and the earlier prose inventory were not treated as proof of
a rule.

Eleven rules are `DEFINITION`:

- `ODD-COUNT-BODY` and `ODD-COUNT-LOOP-BODY` are macro expansions naming exact
  statement trees.
- The two `isStringVal` equations define a total constructor predicate.
- `stringCodes(str(CS)) => CS [simplification]` defines the new guarded
  projection symbol on its reducing constructor case. Its `simplification`
  attribute does not turn the constructor projection into an additional
  theorem.
- The empty and cons equations define the recursive `allDigitStrings`
  predicate.
- `oddDigitCount` and `oddLine` define the per-string mathematical summaries.
- The empty and cons equations define the accumulator recurrence
  `oddLinesAcc`.

None of those rules extends a pre-existing operational symbol with an
additional mathematical fact; each expands a macro or defines a proof-local
symbol by equations or structural recursion.

## Domain lemma

The domain-lemma set is **not empty**. It contains exactly:

```text
rule-9c06989c16c7a097c03e07267ceaa4fc5afd44c87f6099c4345fad7d4fc52617
```

This is the simplifying rule:

```k
applyMethod(V:Val, "count", str(PATTERN:IntSeq), .Vals)
  => cntSub(stringCodes(V), PATTERN)
requires isStringVal(V)
[simplification]
```

It does not define a new symbol: it adds a guarded equation for the existing
semantic symbol `applyMethod`, allowing a dynamically sorted `Val` receiver to
use the string-count result. It is therefore an additional mathematical fact
trusted by the target proof and is classified `DOMAIN_LEMMA`, as required for
an unproved rule carrying `simplification`.

## Separately proved derived lemmas

There are **no** `PROVED_DERIVED_LEMMA` rules in the canonical inventory.

Stage 1 does contain a prior auxiliary proof:

```bash
kprove projection-spec.k \
  --definition reference-proof-kompiled \
  --spec-module PROJECTION-SPEC
```

`prove.sh` compiles `reference-proof-kompiled` from the reference semantics
before compiling `verification.k`, so the auxiliary proof does run against a
module that omits all local verification rules. `projection-proof.out` contains
`#Top`.

However, the proved claim is:

```k
applyMethod(str(CODES:IntSeq), "count", str(PATTERN:IntSeq), .Vals)
  => cntSub(CODES, PATTERN)
```

That is the reference semantics' statically typed string equation. It is not
the exact canonical guarded supersort rule: it does not quantify `V:Val`, does
not assume `isStringVal(V)`, and does not conclude through
`stringCodes(V)`. Consequently, the Stage 1 evidence does not satisfy the
required exact-statement correspondence for
`PROVED_DERIVED_LEMMA`. The ground wrong-count mutation and differential tests
are validation evidence, not a prior universal proof of the canonical rule.

## Operational rules

No canonical rule is classified `OPERATIONAL_RULE`. The inventory contains
only macro/summary definitions and the one additional simplifying domain
fact. The ordinary Python execution, call, loop, lookup, heap, and method rules
come from the mounted reference semantics and are outside this local
verification-module inventory.
