# K proof trust-boundary discovery

The canonical inventory contains 21 rules from `PLUCK-VERIFICATION`. Every
canonical `source_rule_id` is classified once, in inventory order:

- 20 `DEFINITION` rules
- 1 `OPERATIONAL_RULE`
- 0 `PROVED_DERIVED_LEMMA` rules
- 0 `DOMAIN_LEMMA` rules

The definitions are the `asInt` equation; the `pluckTake`, `nextBest`, and
`nextBestIndex` cases; the base and recursive `scanPluck` equations; the four
`pstate` projections; the two `pluckResult` cases; and the two
`allNonNegative` cases. These equations define proof terms, the functional
reference fold, its result, or the input-domain predicate. They do not assert
independent mathematical facts.

The sole operational rule is
`rule-3f5db89b9787a3fdf999e8c890b73a2db174f5c7f8ef866a09ac4e01f6c1c04a`.
It is a `<k>`-cell transition specializing ordinary list iteration when the
head satisfies `isInt`; it yields `asInt(V)` and advances to the tail. This is
part of the verification execution model. Its source comment calls it a
“derived specialization,” but Stage 1 does not first prove this exact rule in
a module that omits it. It is therefore not classified as a proved derived
lemma.

## Separately proved derived lemma

Stage 1 separately proves exactly one reusable derived claim:
`PLUCK-SPEC.pluck-loop`.

- In `prove.sh` lines 18–22, `proof-kompiled` is built from
  `PLUCK-VERIFICATION`, which does not contain the `pluck-loop` claim.
- In `prove.sh` lines 24–29, the first `kprove` command proves the exact
  `PLUCK-SPEC.pluck-loop` claim without a `--trusted` option.
- `prove.log` line 220 records `#Top` for that command.
- In `prove.sh` lines 31–38, the next command selects the same exact claim
  label and marks it trusted while proving `PLUCK-SPEC.pluck-correct`.
- `prove.log` line 249 records `#Top` for the dependent proof.

`pluck-loop` is a claim in `spec.k`, not a rule in the canonical
verification-module inventory. Consequently it has no `source_rule_id` entry
to classify as `PROVED_DERIVED_LEMMA`; none of the 21 inventoried rules meets
that classification's Stage 1 ordering requirement.

No inventoried rule carries the `simplification` attribute.

The domain-lemma set is empty.
