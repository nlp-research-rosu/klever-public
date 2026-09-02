# Trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, whose embedded
`inventory_sha256` is
`c5219c4f4f251272c52fa9684ad275eabd947f80b1e95afc4d2f7d773759af91`.
It contains 15 rules, all from module `VERIFICATION`. The JSON output preserves
their canonical order and classifies every `source_rule_id` exactly once.

Classification counts:

| Classification | Count |
|---|---:|
| `DEFINITION` | 15 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

## Definitions

All canonical rules are equations or structural recurrences for declared
function symbols:

- `nonNegativeVals` has an empty base case, an integer-head recurrence, and an
  `owise` fallback rejecting non-integer heads. These rules define the formal
  input-domain predicate.
- `nextRepeated` has complementary equality and inequality cases defining the
  next run length.
- `scanPrevious`, `scanRepeated`, and `scanValue` each have an empty base case
  and a tail-descending recurrence defining final loop-local values.
- `duplicateOK` has an empty base case and a tail-descending recurrence defining
  the at-most-two-adjacent-occurrences summary.
- `scanDuplicates` defines the accumulated Boolean result by conjunction with
  `duplicateOK`.
- `sortedWithAtMostTwo` is a guarded defining equation for the named contract
  predicate. Its reference to the supplied `sortVS` symbol does not turn this
  equation into an additional mathematical lemma; the rule defines the local
  proof term in terms of that imported symbol.

None of these rules has a `<k>`-cell execution pattern or observes/changes K
configuration cells, so the canonical inventory contains no
`OPERATIONAL_RULE`.

## Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty.

Stage 1 `prove.sh` first compiles `verification.k`, with all 15 canonical rules
already present, into `verification-kompiled`. It then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

That run proves the reachability claims in `spec.k`; it does not first prove
the exact statement of any canonical rule against a module lacking that rule.
The later vacuity command is a negative result mutation and likewise proves no
rule. Therefore the mounted evidence does not demonstrate the ordering and
exact statement correspondence required for any
`PROVED_DERIVED_LEMMA` classification.

`SPEC.scan-loop` is separately machine-checked as a reachability claim and is
used as the loop circularity in the full proof, but it is a claim in `spec.k`,
not a rule in the canonical inventory. It is consequently not an entry in
`trust-boundary.json`.

## Domain lemmas

The domain-lemma set is explicitly **empty**. No canonical rule states an
additional trusted mathematical fact beyond the defining equations of the
named summaries.

The Stage 1 report separately identifies the imported reference-semantics
`sortVS` contract as a trust boundary. The launcher inventory contains no
`sortVS` rule from the reference semantics, so no extra, noncanonical entry is
added for it.

## Simplification constraint

No canonical rule carries the `simplification` attribute. Thus the requirement
that every simplification rule be classified as `DEFINITION` or
`DOMAIN_LEMMA` is satisfied vacuously.
