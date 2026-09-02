# Trust-boundary classification

The canonical inventory contains 11 rules, all from the `VERIFICATION`
module. Every rule is classified exactly once and none carries the
`simplification` attribute.

## Definitions

The first six inventory entries define mathematical summaries:

- The two `sequenceFrom` rules are its recursive and terminating cases.
- The two `sequence` rules define its negative and nonnegative input cases.
- The two `indexAfter` rules are its recursive and terminating cases.

The remaining five entries are structural helpers defining named proof terms:
`loopCondition`, `loopBody`, `targetBody`, `targetFunction`, and
`targetProgram`. Each expands its name to the translated program structure
used by the claims. They are definitions rather than mathematical facts about
independently defined terms.

## Other classifications

No inventoried rule is an `OPERATIONAL_RULE`; the inventory entries are all
function equations or macro-like structural definitions.

There are no `PROVED_DERIVED_LEMMA` entries. Stage 1's `prove.sh` first
compiles `verification.k`, including all 11 inventoried rules, and then runs
one `kprove` command against that compiled module. It does not first prove any
inventoried rule against a module that omits that rule, so there is no
separate proof artifact or prove-before-use ordering that would justify this
classification.

The domain-lemma set is empty.
