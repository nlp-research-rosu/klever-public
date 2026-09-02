# Trust-boundary discovery

## Canonical input

The classification uses `/reference/rule-inventory.json` as the exhaustive
inventory of the finalized local verification-module closure. Its
`inventory_sha256` is:

```text
6b7cc9b5eb3dab9e078c1ec848cbe95c1df8a055e1a23922684aa8ed53edc950
```

The inventory contains six rules, all from module `VERIFICATION`, and every
one carries the `simplification` attribute. Each canonical `source_rule_id`
appears exactly once in `trust-boundary.json`, in inventory order.

## Classification

All six rules are `DEFINITION`.

The first three equations define the total proof summary
`baseAcc(Int, Int, IntSeq)`:

1. A nonpositive remaining magnitude returns the accumulator.
2. A positive magnitude with an out-of-domain base below 2 returns the
   accumulator as an off-target totalization case.
3. A positive magnitude with base at least 2 recursively advances by the
   semantics' quotient/remainder step and prepends the corresponding digit
   code.

These are base, totalization, and recursive equations for a named mathematical
summary. They do not observe or rewrite the K configuration and do not state
independent arithmetic facts.

The final three equations define the total signed representation summary
`changeBaseCodes(Int, Int)`:

1. Zero is represented by code 48.
2. Positive integers initialize `baseAcc` with an empty accumulator.
3. Negative integers prefix code 45 and convert their positive magnitude.

These cases are likewise equations defining the named proof term, rather than
execution rules or facts imported to make the proof close.

## Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty.

Stage 1's `/reference/k-proof/prove.sh` first compiles `verification.k` into
`verification-kompiled`; that compiled module already contains all six
canonical rules. Its later `kprove` commands therefore do not prove any one of
those exact rule statements against a module from which that rule is absent.

The command

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
```

is evidence for the separate reachability claim `SPEC.loop-invariant`, as
recorded in Stage 1's `PROOF.md`. That claim is not a rule in the canonical
inventory and does not establish any canonical simplification rule before
that rule is introduced. Consequently, it supplies no
`PROVED_DERIVED_LEMMA` classification here.

## Other classification sets

The `OPERATIONAL_RULE` set is empty. None of the six rules matches `<k>`, a
configuration cell, a call, or an observable execution step; each rewrites
only a proof-summary symbol. This also follows the required restriction that a
rule carrying `simplification` must be either `DEFINITION` or `DOMAIN_LEMMA`.

The `DOMAIN_LEMMA` set is explicitly empty. The verification closure adds no
trusted mathematical identity beyond the defining cases of `baseAcc` and
`changeBaseCodes`; arithmetic obligations are handled by the imported
semantics and backend rather than by additional local rules.
