# Trust-boundary rule discovery

The canonical inventory contains exactly three rules, in one verification
module. Each rule is classified exactly once and retained in canonical
inventory order in `trust-boundary.json`.

## Classification result

All three rules are `DEFINITION` entries. Together they are the guarded cases
of the proof-local `factorAcc(ValSeq, Int, Int)` recurrence:

- `rule-dbfc0d4c3175b4500c8cf75aa233cec5e0c9c3cee743890140512a0182f4cafa`
  is its base equation.
- `rule-a835c97bf031675f196bffdf44a60757b87fcba3d1c37ef34f793bef42ba0e65`
  is its divisible-case recursive equation.
- `rule-5fab523961a49385350dd07993fa3e83246b724eb1f40138964ce039d42a8f55`
  is its non-divisible-case recursive equation.

These equations define the named mathematical sequence summary. Their
left-hand sides are pure `factorAcc` terms: they do not match a `<k>` cell,
program syntax, continuation, environment, heap, or other execution state.
They therefore are not `OPERATIONAL_RULE` entries.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical rule inventory.

The mounted Stage 1 `prove.sh` compiles `verification.k`—with all three
`factorAcc` rules already present—before running:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It does not first prove the exact statement of any inventory rule against a
module from which that rule is absent. Consequently, none meets the required
ordering or exact-correspondence test for `PROVED_DERIVED_LEMMA`.

`SPEC.factor-loop` is machine-checked Stage 1 evidence connecting fixed program
execution to the recurrence, but it is a reachability claim in `spec.k`, not a
rule in the canonical inventory. It does not change the classification of the
three recurrence equations.

## Domain lemmas

The domain-lemma set is empty. No canonical rule states an additional trusted
mathematical fact, and no canonical rule carries the `simplification`
attribute.
