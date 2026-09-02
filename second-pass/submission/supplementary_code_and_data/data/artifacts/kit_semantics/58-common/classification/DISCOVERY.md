# Trust-boundary discovery

The canonical inventory has SHA-256
`87f56ae659ac675f0785aa4bb001dad4a3f0f76ab2231c11d8dd28eaf505e6f6`
and contains seven rules, all from the `VERIFICATION` module. Every canonical
`source_rule_id` is classified exactly once and in inventory order in
`trust-boundary.json`.

## Classification results

Six rules are `DEFINITION`:

- the empty and cons equations for the total `commonMember` summary;
- the empty and cons equations for the total `commonAcc` summary; and
- the `commonLoopBody()` and `commonBody()` macro expansions.

The four summary equations are base/recursive clauses defining named
mathematical summaries. The two macros are structural definitions of named
proof terms containing the exact translated program fragments. None is an
ordinary execution rule or an added mathematical fact about pre-existing
symbols.

The guarded rule at `verification.k:14-16` is a `DOMAIN_LEMMA`. It has the
`simplification` attribute and rewrites an expression built from the
pre-existing K equality and `orBool` operations. It therefore supplies an
additional Boolean fact used by simplification rather than defining
`commonMember`, `commonAcc`, or another new proof symbol.

No inventory rule is an `OPERATIONAL_RULE`: none implements an execution or
observation step in the local verification model. The operational Python rules
come from the supplied `MPY` semantics and are outside the canonical local
verification-module inventory.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1's `prove.sh` first compiles `verification.k`—including all seven
canonical rules—into `verification-kompiled`, then runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

That run proves the claims in `spec.k` under a theory that already contains the
guarded simplification rule. The `member-fold` claim is not a prior proof of
that rule's exact statement, and no Stage 1 command proves the exact
simplification statement against a module from which the rule is absent.
The negative mutation probes also use the same compiled definition. Therefore
Stage 1 supplies no ordering or exact-correspondence evidence that would permit
classifying any canonical rule as a separately proved derived lemma.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

- `rule-cd11c71e1459d61e91176cc439f01696c9d8116dd9313d8d67eb714d1144a5b0`,
  the guarded `simplification` rule at `verification.k:14-16`.
