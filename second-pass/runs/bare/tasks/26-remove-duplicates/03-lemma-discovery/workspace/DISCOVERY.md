# Trust-boundary classification

The canonical inventory contains three rules, in the order used by
`trust-boundary.json`. All three are classified as `DEFINITION`:

1. `rule-eead64180cce1cdc54b47266673a3b5fdf72418beb97f8d7bc07df03affe9237`
   is a wrapper expansion from `removeRepeated` to the accumulator-style
   `removeRepeatedOnto` summary with an empty suffix.
2. `rule-4b2e81eee048157b7718fb38321ccd6a0df2d72177e63dbc46d4d028c48dffff`
   is the empty-list base case of that summary recurrence.
3. `rule-21d0f4e4939c7bf24a8212763a583e9e9f1d7cc35fcef917a31103579967b976`
   is its recursive cons case, conditionally retaining the current element
   when its count in the original list is one.

These rules define the verification summary itself. They do not execute the
translated Python configuration, and they do not assert additional facts
beyond the summary's recurrence. The canonical inventory reports no
`simplification` attributes.

## Separately proved derived lemma

Stage 1 separately proves the claim labeled `walk-correct`. The first
`kprove` command in `/reference/k-proof/prove.sh` selects
`--claims walk-correct` and proves it against the compiled `VERIFICATION`
module. The next `kprove` command uses `--trusted walk-correct` while proving
the end-to-end `program-correct` claim. This establishes the required
prove-before-reuse ordering.

`walk-correct` is a claim in `spec.k`, not a rule in the canonical
verification-module inventory. It therefore has no canonical
`source_rule_id` and no JSON classification entry. None of the three
inventoried rules is classified as `PROVED_DERIVED_LEMMA`.

The domain-lemma set is empty.
