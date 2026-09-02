# Axiom reconciliation

The exact command and output are in `07_print_axioms.sh` and
`07_print_axioms.out`:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

- `sorryAx` is absent.
- `11_candidate_structure.out` finds no candidate `axiom` or `opaque`
  declaration and no `sorry`, `admit`, or `unsafe` token.
- `trust-inventory.json` contains 57 generated declarations. None appears in
  the transitive axiom list of `Proof.final`; therefore the proof does not rely
  on any of the generated hook/projection axioms in that allowlist.
- `propext`, `Classical.choice`, and `Quot.sound` are the pinned Lean 4 core
  axioms, not candidate-created or generated declarations. `Classical.choice`
  is induced by the candidate's `classical` decidable equality helpers;
  `propext` and `Quot.sound` arise through simplification/library definitions.
  They are part of the normal Lean kernel trust boundary, not an unrecorded
  proof escape.

This axiom accounting is clean. It does not cure the independent operational
bridge failure: the Float-max conjunct is proved by definitional equality, so
the incorrect helper does not need to be unfolded and contributes no axiom to
the list.
