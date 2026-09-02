# `Proof.final` axiom accounting

The exact `#print axioms Proof.final` output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The output is preserved verbatim in `08-print-axioms.log`.

- `propext` is Lean's foundational propositional-extensionality axiom.
- `Classical.choice` is Lean's standard classical-choice axiom; it is reached
  by the candidate's classical equality decision on generated `SortKItem`.
- `Quot.sound` is Lean's foundational quotient-soundness axiom.

These are declarations in the pinned Lean foundation, not declarations added
by the candidate or generated project.  `trust-inventory.json` inventories 50
generated trust-boundary declarations.  None of those 50 declarations occurs
in the dependency output, so the final proof does not consume any generated
hook axiom or opaque declaration.  There is no `sorryAx` and no unrecorded
candidate or generated proof escape.  The three foundational dependencies are
therefore reconciled with the inventory as dependencies outside its stated
generated-declaration scope.

Clean axiom accounting does not repair the empty-sort/vacuity or operational
bridge failures.
