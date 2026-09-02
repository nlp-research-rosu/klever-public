# Trust-boundary discovery

## Canonical scope and coverage

The sole classification source is
`/reference/rule-inventory.json`. Its copied inventory digest is
`d0fdf03a9d036db3e9b0732707b1c26876c4455cf0bffb60046d153ec2797da8`.
It contains seven rules, all in module `VERIFICATION`.

`trust-boundary.json` preserves those seven `source_rule_id` values in
canonical inventory order and classifies each exactly once. Rules in imported
`projection.k` are outside this launcher-generated canonical inventory and
were not added.

Classification totals:

- `DEFINITION`: 5
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 2

## Definitions

The following rules are equations or structural recurrences that define named
mathematical summaries:

- `rule-8348557acb9f13893399c872ddae569bc70937b7abc79fbe39494743b080aa93`
  defines `hasInverse` in terms of fixed-semantics occurrence counting.
- `rule-2ebe172a962d634da4247333469c7c769941308cbaa1ffb0733ad2c17efc3b87`
  and
  `rule-f0f2741daac7483fe012897d489038765088adda53a780fb059bfe91cd605192`
  are the base and cons equations for `anyInverse`.
- `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08`
  and
  `rule-d25e64ac0656cbce08dd6ef3cd864d49a4614f3e415d6533ea1c726c4a025b1a`
  are the base and cons equations for `allInts`.

These rules introduce and define proof-local summary symbols; they do not add
standalone mathematical facts about an already-defined operation.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-4f41076b3b0eb2c1c718d3792b1c9158f8ae7d86ca361684ad8670d999140def`
- `rule-23e1a62d70fda3f264b9738a91911fc3875dc654e5e8dbd9c9e70004aee7e7b5`

Both carry the `simplification` attribute, so the required classification
constraint permits only `DEFINITION` or `DOMAIN_LEMMA`. They rewrite existing
`MPY` operation symbols (`applyCmp` and `applyUn`) rather than defining new
summary symbols. They are therefore additional guarded mathematical facts used
to recover integer behavior from a value held at sort `Val`, and are classified
as `DOMAIN_LEMMA`.

They are not ordinary model execution/observation rules, so
`OPERATIONAL_RULE` would not describe their proof-local role.

## Separately proved derived lemmas and Stage 1 evidence

Stage 1 separately proved two auxiliary connection claims:

- `CONNECTION-SPEC.int-equality` at
  `/reference/k-proof/connection-spec.k:6`
- `CONNECTION-SPEC.int-unary-minus` at
  `/reference/k-proof/connection-spec.k:9`

The evidence and ordering are:

1. `/reference/k-proof/connection-definition.k` imports
   `INT-PROJECTION` and does not import `VERIFICATION`.
2. `/reference/k-proof/prove.sh:38-45` compiles
   `CONNECTION-DEFINITION` and runs both connection claims.
3. Only afterward,
   `/reference/k-proof/prove.sh:47-50` compiles `VERIFICATION`, which contains
   the two simplification rules.
4. `/reference/k-proof/prove.out:157-160` records both connection claims as
   proven and prints `#Top`.

This demonstrates bridge-free, proof-before-use evidence for the two auxiliary
connection claims. It does **not** make either canonical simplification rule a
`PROVED_DERIVED_LEMMA` under this benchmark's exact-statement criterion:

- the connection claims quantify operands directly at sort `Int`;
- the inventory rules instead match a `Val` operand under an `isInt` guard;
- the inventory rules are simplification rules, which the benchmark explicitly
  requires to be classified only as `DEFINITION` or `DOMAIN_LEMMA`.

Consequently, no canonical inventory rule qualifies as
`PROVED_DERIVED_LEMMA`, even though the related connection claims provide
Stage 1 support for the intended sort-recovery facts.

## Resulting trust boundary

Within the canonical local verification-module inventory, the trusted
additional mathematical boundary consists precisely of the two guarded
simplification rules listed above. The remaining five rules are definitions.
There are no canonical ordinary operational rules and no canonical rules whose
exact statements satisfy the proved-derived-lemma classification.
