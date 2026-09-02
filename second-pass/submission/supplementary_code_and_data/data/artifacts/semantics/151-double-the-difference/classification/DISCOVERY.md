# Trust-boundary discovery

The canonical inventory identifies 10 rules in the local verification-module closure. Each appears exactly once in `trust-boundary.json`, in canonical inventory order.

## Operational rules

The three `#iterNext(list(numVals(...)))` rules are classified as `OPERATIONAL_RULE`. Together they give the verification model's proof-domain list representation its ordinary MPY iterator behavior:

- the empty representation produces `#iterDone`;
- an integer-headed representation yields the integer and its tail;
- a float-headed representation yields the float and its tail.

These rules describe how the modeled input is executed and observed. They are not additional arithmetic or logical facts.

## Definitions

The other seven rules are classified as `DEFINITION`:

- `oddSquare` defines the per-integer contribution;
- the three `doubleDifferenceSpec` equations define the recursive result summary for empty, integer-headed, and float-headed sequences;
- the three `finalNumber` equations define the final value of the Python loop-target local for the same sequence cases.

They are equations or structural recurrences for named proof terms. None of the canonical rules carries the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The Stage 1 `prove.sh` first compiles `verification.k`, which already contains all 10 inventoried rules, and then runs one `kprove` invocation over `spec.k` against that compiled module. It does not first prove the exact statement of any inventoried rule against a module lacking that rule, nor does it subsequently install such a rule. The `loop-invariant` and `double-the-difference-correct` items in `spec.k` are proved claims, not inventoried reusable rules, so they do not change this classification.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule supplies an additional trusted mathematical fact beyond the operational input model and the definitions of the proof summaries.
