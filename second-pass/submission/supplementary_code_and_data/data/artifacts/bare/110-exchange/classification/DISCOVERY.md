# K proof trust-boundary discovery

The canonical inventory hash is
`76c60c5d4bad411cf1086bae00f60ef87db52f0f9e6c79624a6c5b01245d8389`.
The inventory contains eight rules, all from the `VERIFICATION` module.

## Classification

Every inventory rule is classified as `DEFINITION`:

- `countBody` expands a named proof term into the parity-counting statement
  body.
- `solutionProgram` expands a named proof term into the exact translated
  program AST. Stage 1's `cmp` command checks this expanded term against
  `solution.mpy`.
- The two `evenBit` rules are the exhaustive conditional equations defining
  the parity indicator.
- The two `countEven` rules are the base and recursive equations defining the
  list-count summary.
- The two `lastValue` rules are the base and recursive equations defining the
  structural summary of the loop variable's final value.

These are macro expansions, recurrences, or structural mathematical helpers.
They are not ordinary execution/observation transitions, so no inventory rule
is `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The Stage 1 ordering is explicit in `prove.sh`: it first runs
`kompile semantic.k`, and `semantic.k` imports `verification.k`, so all eight
inventory rules are already in the compiled definition. Only afterward does
the script run `kprove spec.k`. That command proves the claims
`loop-counts-even`, `exchange-yes`, and `exchange-no`. None of those claims is
an exact inventory-rule statement, and Stage 1 does not subsequently introduce
an exact proved claim as a reusable verification rule. Thus the mounted
evidence does not establish the proof-before-introduction ordering required
for this classification.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. No inventory rule asserts an additional
mathematical fact beyond the named macro and recursive/conditional
definitions above. The inventory also contains no rule carrying the
`simplification` attribute.
