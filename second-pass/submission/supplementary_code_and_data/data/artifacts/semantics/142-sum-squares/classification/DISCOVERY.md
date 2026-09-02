# Trust-boundary discovery

The canonical inventory has SHA-256 identifier
`fb2247fda028d52dd357d684d057d57de6c0fdc5ca64386b23db79ef939df529`
and contains 13 rules from `SUM-SQUARES-VERIFICATION`.

## Classification

- 2 rules are `OPERATIONAL_RULE`: the empty and nonempty `#iterNext`
  observations for the symbolic `intVals` representation. They extend the
  verification model's iterator behavior and execute in the `<k>` cell.
- 11 rules are `DEFINITION`: the three cases of `contribution`, the
  `sumSquares`, `endIndex`, and `endValue` base/recursive equations, and the
  two macro expansions naming the exact loop and function bodies.
- 0 inventory rules are `PROVED_DERIVED_LEMMA`.
- 0 inventory rules are `DOMAIN_LEMMA`.

No inventory rule has the `simplification` attribute.

## Separately proved derived lemmas

Stage 1 separately proves two reusable claims:

1. `SUM-SQUARES-SPEC.loop` is first proved without a trusted claim by the
   first `kprove` command in `prove.sh` (lines 28–33). The symbolic definition
   used there is compiled from `verification.k`, which does not contain the
   loop claim as a rule. The next proof retains the exact same claim label and
   admits it with `--trusted SUM-SQUARES-SPEC.loop` while proving
   `SUM-SQUARES-SPEC.body` (lines 35–41). Its successful proof result is the
   first `#Top` in `prove.log` (line 152).
2. `SUM-SQUARES-SPEC.body` is first proved by that second command, with only
   the already-proved loop claim admitted. The final command then retains the
   exact same body claim and admits it with
   `--trusted SUM-SQUARES-SPEC.body` while proving
   `SUM-SQUARES-SPEC.main` (lines 43–49). Its successful proof result is the
   second `#Top` in `prove.log` (line 181); the end-to-end main proof produces
   the third `#Top` (line 210).

These reusable claims occur in `spec.k`, not in the launcher-generated rule
inventory for `SUM-SQUARES-VERIFICATION`. Consequently, no canonical
`source_rule_id` is classified as `PROVED_DERIVED_LEMMA`.

## Domain-lemma boundary

The domain-lemma set is empty. The verification module adds no trusted
mathematical fact: its mathematical rules define named summaries, while its
remaining two rules provide iterator execution behavior.
