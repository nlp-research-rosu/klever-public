# Trust-boundary discovery

The canonical inventory contains seven rules, all from
`REMOVE-DUPLICATES-VERIFICATION`. Every inventory rule is classified exactly
once and remains in canonical inventory order.

## Classification basis

The two `allInts` rules are `DEFINITION` because they are the base and
recursive equations for the structural `List[int]` precondition.

The three `keepSinglesAcc` rules are `DEFINITION` because together they define
the mathematical output summary: the empty-input base case, the
singleton-occurrence retain case, and the repeated-occurrence discard case.
All three rules carrying the `simplification` attribute are therefore
definitions, not independently trusted mathematical facts.

The `#removeDuplicatesBody` and `#removeDuplicatesClosure` rules are
`DEFINITION` because they are macro expansions naming the exact translated
program terms used in the proof.

There are no canonical `OPERATIONAL_RULE` entries. The local verification
module adds no execution or observation behavior; execution comes from the
imported reference semantics, while the inventoried program macros are
structural definitions.

## Separately proved derived lemma

Stage 1 separately proves one reusable claim:
`REMOVE-DUPLICATES-SPEC.loop-invariant`.

The evidence is the ordered pair of commands in the mounted `prove.sh`:

1. After compiling `verification.k`, the first `kprove` invocation selects
   only `REMOVE-DUPLICATES-SPEC.loop-invariant` with `--claims`. The compiled
   verification module contains the seven canonical definitional rules and
   does not contain the loop-invariant claim as a rule.
2. The following `kprove` invocation names that exact same claim label with
   `--trusted`, reusing the already-proved invariant as a lemma while proving
   the exhaustive entry claims.

The exact statement being proved and reused is the single labeled claim in
the mounted `spec.k`; the identical fully qualified label appears in both
commands. This claim is not a rule in the canonical verification inventory,
so no inventory entry is classified `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule asserts an additional
mathematical fact beyond the definitions and macro expansions above.
