# Trust-boundary discovery

The canonical inventory hash is
`60eb713b2b76c3b7c275bba937b7723b878edafd277c1b79e528ce79ab39b6fd`.
It contains 10 rules, all from the single local verification module
`VERIFICATION`. Every canonical `source_rule_id` is classified exactly once and
in canonical inventory order in `trust-boundary.json`.

## Classification summary

| Classification | Count |
|---|---:|
| `DEFINITION` | 9 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 1 |

The nine `DEFINITION` entries are the equations for four newly named
mathematical helpers:

- `onlyStrings`: empty and recursive equations defining the list-of-strings
  predicate;
- `stringCodes`: the string projection and its exhaustive `[owise]`
  non-string case;
- `totalLen`/`totalLenFrom`: a wrapper, empty case, and descending left-fold
  recurrence defining total character length;
- `lastLoopValue`: empty and descending recurrence equations defining the
  final loop-target value.

These rules define proof terms or mathematical summaries. None rewrites a
`<k>` computation, observes machine state as a new execution rule, or replaces
program control, so the canonical inventory has no `OPERATIONAL_RULE`.

## Domain lemma

The domain-lemma set is **not empty**. It contains exactly:

- `rule-b3f45b5d74172f8b06aeed730c933057ce5ded1254eac17997dee1565ec954d1`:
  `seqLen(V) => isLen(stringCodes(V)) requires isStrV(V)
  [simplification]`.

This rule rewrites the pre-existing semantic observation `seqLen` to an
equality involving the proof-local projection `stringCodes`. It is therefore
an additional mathematical fact over the `isStrV` domain, not an equation
whose left-hand side defines a new proof-local symbol. The canonical inventory
marks it `simplification`, so the permitted choices are `DEFINITION` or
`DOMAIN_LEMMA`; its role makes `DOMAIN_LEMMA` the appropriate classification.

## Separately proved derived lemmas

There are **no separately proved derived lemmas** in the canonical inventory.

Stage 1 `prove.sh` first compiles `verification.k` as module `VERIFICATION`
(lines 16–20) and only afterward runs `kprove spec.k` against that compiled
definition (lines 22–24). Thus all 10 rules—including the simplification
rule—are already present in the theory used to prove the Stage 1 claims.
The remaining `kprove` commands run negative mutation probes against the same
compiled definition. No command proves the exact statement of any inventory
rule against a module that omits that rule, and no separate bridge-free lemma
module or prior proof command exists in the mounted evidence.

Consequently, the Stage 1 comment and `PROOF.md` description of the guarded
`seqLen` rule as “derived” do not satisfy the required proof-ordering criterion
for `PROVED_DERIVED_LEMMA`; it remains part of the trusted domain-lemma set.
