# Trust-boundary discovery

## Inventory and classification

The canonical inventory hash is
`577e90b3e2ba59231529bb8ba7f67b95a7969f86d0f9e22e335605619797a3f9`.
It contains 11 rules, all in the local `VERIFICATION` module. The mounted
`verification.k` SHA-256 is
`a54766e74afa56d501e8880c29aacebec2884555ba27c801af7a1bbb614859db`,
which matches the canonical inventory metadata.

All 11 inventory rules are classified as `DEFINITION`:

- Four rules are the empty and recursive equations for `#negFold` and
  `#posFold`.
- Six rules define the sign-gated step functions and optional-accumulator
  candidate selection used by those folds.
- One rule is the macro expansion of `solutionProgram` into the translated
  program AST.

These are equations, recurrences, structural helpers, or a named proof-term
expansion. They define the mathematical summaries and program term used in the
claims; none asserts an additional mathematical fact beyond those definitions.
The inventory contains no rules carrying the `simplification` attribute.

The `OPERATIONAL_RULE` count is zero for this canonical inventory. Operational
execution rules exist in the separately imported semantics, but they are not
members of the launcher-declared inventory, whose exhaustive
`verification_modules` list contains only `VERIFICATION`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` first compiles the complete `verification.k` at lines 6–9,
including every one of the 11 inventory rules, and then invokes its only
`kprove` command at line 24 against that compiled definition. It does not first
prove any inventory rule against a module omitting the rule, and it does not
insert and recompile a proved rule afterward. The three reachability claims in
`spec.k` are proof targets rather than reusable rules in the canonical
inventory. Thus there is no Stage 1 evidence satisfying the required ordering
and exact-correspondence test for a separately proved derived lemma.

## Domain lemmas

The domain-lemma set is empty. No canonical inventory rule is an additional
trusted mathematical fact used to close the proof; all mathematical-summary
rules in the inventory are definitional equations.

## Classification totals

| Classification | Count |
|---|---:|
| `DEFINITION` | 11 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |
