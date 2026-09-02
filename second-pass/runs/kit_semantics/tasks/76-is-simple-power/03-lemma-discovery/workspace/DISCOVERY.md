# Trust-boundary discovery

## Canonical scope

`/reference/rule-inventory.json` is the exhaustive inventory used for this
classification. It identifies one local verification module, `VERIFICATION`,
and nine rules. The copied inventory identifier is
`d2933cd1014ec18a12e3f519fc18739b2c3d87ab2b3a6ac648eeaf11c68ae48d`.
Every inventory rule appears exactly once and in canonical order in
`trust-boundary.json`.

## Classification result

The first seven rules are `DEFINITION`. Together they define the total
`simplePower(Int, Int)` summary:

- `rule-146fed052167b079e1650450e1ce639924212da85a65b3aba6d9be3d6e53c7e3`
  is the `X = 1` base equation.
- `rule-60585bbb6d312b6f4f8499ebbf464f74ddf2e2181ec92b0e8af660b2838bc868`
  defines the guarded base-0 case.
- `rule-896a8a4fcf1778edbc32f433cc5724feec0edb677d9dea32a3e484bb2aecf746`
  defines the guarded base-1 case.
- `rule-3ecd89403379532a7e0ba4d1d0747278594ded6e9d59f9925bdee477f6b5ddc3`
  defines the guarded base-minus-one case.
- `rule-e5a3d5202919810bbe675a2a77fceecdb470e4b5c07f803b5b3ecbed8f59041b`
  defines the zero-input case for bases whose magnitude is at least two.
- `rule-d19d1bda5d0346f529812d8ff45415af253ed73e3bc020870bf8b1750eb773b9`
  is the exact-factor recurrence.
- `rule-775415705833fb882b7bb2633fea60ea3123195b617f4a19ad0450c43e3dd4ae`
  is the terminal nondivisible equation.

None of these rules matches a `<k>` cell or another execution configuration,
so none is an `OPERATIONAL_RULE`.

The remaining two rules carry the `simplification` attribute and are
`DOMAIN_LEMMA`:

- `rule-8464b0da61f140807ea0bf9d284978c8e9beca854f787960b68d619fb825f1ee`
  supplies the nondivisible loop-base simplification.
- `rule-03216b3b471d3a9d3f64484ebc0ff5a8d18bceade6710b43811706d8d0373c9b`
  supplies factor folding in the integer-division normal form reached by the
  operational semantics.

They are additional mathematical facts rather than necessary cases of the
already complete seven-rule summary definition. Both are present in
`verification.k` before the Haskell definition is compiled, and both are
available to every positive proof command. They therefore remain inside the
trusted mathematical boundary.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1's `prove.sh` compiles `verification.k` with all nine inventory rules
already present, then proves `SPEC.loop-invariant` and the complete `SPEC`
claim set. It never compiles a predecessor module without either
simplification rule, never proves either exact rule statement there, and never
rebuilds the final verification module only after such a proof. The two
`#Top` results consequently establish the reachability claims under those
rules; they do not separately prove the rules themselves. The expected-failure
result and body mutations test discrimination and body sensitivity, not the
exact statements of either simplification rule.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly the two
`simplification` rules listed above.

There are no `OPERATIONAL_RULE` entries in the local verification-module
inventory and no separately proved derived lemmas.
