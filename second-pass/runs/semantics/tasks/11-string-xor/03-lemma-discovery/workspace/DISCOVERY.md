# Trust-boundary discovery

The canonical inventory contains 19 rules, all in
`STRING-XOR-VERIFICATION`. Every inventory rule is classified as
`DEFINITION`.

## Classification basis

The rules fall into two definitional groups:

- `binaryCode`, `xorCode`, `xorAcc`, `binaryCodes`, `xorLastX`, and
  `xorLastY` are equations and recurrences defining mathematical predicates
  and summaries used by the reachability claims.
- `stringXorTarget`, `stringXorLoopBody`, `stringXorBody`,
  `stringXorClosure`, and `stringXorModule` expand named proof terms into the
  exact translated AST, closure, and module structures.

These are definitions of newly introduced symbols, rather than facts about
independently defined operations. None is an additional execution or
observation rule, so the inventory has no `OPERATIONAL_RULE` entries. The
inventory reports no `simplification` attributes.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The Stage 1 evidence does not show any inventory rule being proved before it
is introduced. In `/reference/k-proof/prove.sh`, lines 33-37 compile
`verification.k` as `STRING-XOR-VERIFICATION`, which already contains all 19
inventory rules. Only afterward, lines 38-41 run `kprove` for
`STRING-XOR-SPEC.loop-invariant` and
`STRING-XOR-SPEC.solution-correct`. Those two statements are claims in
`spec.k`, not rules in the canonical inventory. Consequently, no inventory
rule has the required proof-before-introduction ordering or exact
correspondence for the derived-lemma classification.

## Domain lemmas

The domain-lemma set is empty. No inventory rule is classified as
`DOMAIN_LEMMA`; all mathematical content in the local verification module is
introduced through equations or recurrences defining its own summary
symbols.
