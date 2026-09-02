# Trust-boundary discovery

The canonical inventory has two rules, both in `ROUNDED-AVG-VERIFICATION`.
Each is classified exactly once and in canonical inventory order in
`trust-boundary.json`.

## Definitions

- `rule-07b2e76171363735048d516894c0106df978020141671339aaa271a5d5e0d8e7`
  is a `DEFINITION`. It expands the total, nullary `roundedAvgBody` helper into
  the statement AST translated from `solution.mpy`. This is a structural
  representation of the program body.

- `rule-5e130f83335a10b2992b3283bceb5cbf4e9d208c0b150ab3918d09173e3f7ad7`
  is a `DEFINITION`. It expands the total `roundedAvgCall(N, M)` helper into
  the closure call used as the initial proof term. This is a named proof
  harness.

Neither inventory rule has the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications. Stage 1 `prove.sh`
compiles `verification.k`—already containing both inventory rules—into
`verification-kompiled` and then invokes `kprove spec.k` against that
definition. It contains no earlier proof command against a module omitting
either rule, so Stage 1 provides no required ordering evidence for a
separately proved derived lemma.

The four items in `spec.k` are reachability claims about the program behavior,
not reusable rules in the canonical verification-module rule inventory.

## Domain lemmas and operational rules

The domain-lemma set is empty. Neither rule supplies an additional
mathematical fact: both only expand named proof terms. The operational-rule
set is also empty because the execution and observation rules come from the
imported reference semantics, while the canonical local inventory contains
only the two proof-term definitions above.
