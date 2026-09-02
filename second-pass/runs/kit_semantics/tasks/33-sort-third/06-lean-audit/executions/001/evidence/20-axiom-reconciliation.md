# `Proof.final` axiom reconciliation

The exact Lean output is:

```text
'Proof.final' depends on axioms: [propext]
```

There is no `sorryAx`. None of the 45 generated declarations in
`trust-inventory.json`'s allowlist occurs in the dependency list. `propext` is
Lean's standard foundational proposition-extensionality axiom supplied by the
pinned Lean 4.22 toolchain, not a declaration added by the generated project or
candidate; the generated trust inventory inventories generated declarations,
so this is an intrinsic kernel trust dependency rather than an unrecorded
candidate escape.
