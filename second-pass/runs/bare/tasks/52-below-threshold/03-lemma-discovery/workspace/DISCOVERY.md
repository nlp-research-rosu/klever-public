# Trust-boundary classification

The canonical inventory contains three rules, all from the `VERIFICATION`
module. Each is classified as `DEFINITION`:

- `rule-a8176184e1ba57504866732ee5f4ad5ab8fcf8101c60b1b27722cc122c120ec4`
  is the empty-sequence base equation for the mathematical summary
  `allBelow`.
- `rule-0208a16b17f61f199b8fd1d9c5435b9b71da6c6ce49cbbca4ffed14d285fb668`
  is the nonempty-sequence recurrence for `allBelow`.
- `rule-50c5600cfb11ade9a3062a0751132a38f4a48d7f51e504490c6e5b59f0180ffb`
  is the macro expansion that defines `solutionProgram`, the named program
  term used in the proof claims.

There are no `OPERATIONAL_RULE` entries in the canonical inventory. The
execution rules are in `semantic.k`, but the launcher inventory is exhaustive
and contains none of them, so no additional entries are invented.

There are no separately proved derived lemmas. Stage 1's `prove.sh` compiles
`verification.k` with all three inventoried rules already present, then runs
`kprove` on the claims in `spec.k`. It does not first prove the exact statement
of any inventoried rule against a module lacking that rule and later install
it. Thus there is no Stage 1 evidence supporting a
`PROVED_DERIVED_LEMMA` classification.

The domain-lemma set is explicitly empty. None of the three rules is an
additional trusted mathematical fact; they are solely summary equations or a
macro definition. None carries the `simplification` attribute.
