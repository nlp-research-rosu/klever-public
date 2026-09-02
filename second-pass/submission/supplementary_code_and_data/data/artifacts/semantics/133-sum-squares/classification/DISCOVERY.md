# Trust-boundary discovery

The canonical inventory has SHA-256
`bd165355783fb2112441edb679eaeab096d8e63b6d11308d5b6753496a59ad5e`
and contains five rules.

## Definitions

The first two inventory entries are the base and recursive equations for
`sumSquaresFrom`. Together they define the mathematical accumulator summary:
the empty sequence returns the accumulator, while the nonempty case adds the
squared ceiling of the head and recurs on the tail.

The third and fourth entries are the base and recursive equations for
`lastFrom`. This structural helper records the final loop-target value so that
the complete scope update can be stated without an existential.

All four are classified as `DEFINITION`; none asserts an independent
mathematical fact beyond defining its named proof term.

## Separately proved derived lemma

`rule-1a11afc07a69ef715908d8b2c198565b0dbe50b4471cb0f1473036bc47d7bf15`
is classified as `PROVED_DERIVED_LEMMA`.

The Stage 1 evidence establishes the required ordering and correspondence:

1. `prove.sh` first compiles `verification.k` with
   `--main-module SUM-SQUARES-VERIFICATION-BASE`.
2. That base module contains only the four defining equations above. The
   reusable loop rule is in the later `SUM-SQUARES-VERIFICATION` module and is
   therefore absent from `loop-verification-kompiled`.
3. `prove.sh` then invokes `kprove` for
   `SUM-SQUARES-LOOP-SPEC.loop-correct` against that base definition.
4. The claim in `spec.k` has the same loop-state rewrite and
   `notBool (L in_keys(GLOBAL))` side condition as the inventoried rule. The
   rule's `priority(40)` attribute is rewrite scheduling metadata and does not
   alter the proved logical statement.
5. Only after that proof does `prove.sh` compile the full
   `SUM-SQUARES-VERIFICATION` module containing the promoted rule and use it
   for the downstream `function-correct` proof.

## Remaining categories

The `DOMAIN_LEMMA` set is empty. The `OPERATIONAL_RULE` set is also empty:
the local verification-module closure consists only of the four summary
definitions and the separately proved loop rule. No inventory entry carries
the `simplification` attribute.
