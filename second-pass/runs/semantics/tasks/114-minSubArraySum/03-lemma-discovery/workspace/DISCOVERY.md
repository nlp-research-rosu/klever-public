# K proof trust-boundary discovery

The canonical inventory contains 20 rules, all classified exactly once and in
inventory order in `trust-boundary.json`.

## Classification summary

- **DEFINITION (16 rules):** the two `intVals` equations; the
  `chooseSmaller`, `nextCurrent`, `kadaneCurrent`, `kadaneSmallest`,
  `minSubArraySumSpec`, and `lastFrom` equations/recurrences; and the four
  macros naming the translated loop body, function body, function definition,
  and closure. These rules define representation terms, mathematical
  summaries, folds, or named syntax terms.
- **OPERATIONAL_RULE (2 rules):** the empty and nonempty `#iterNext` cases for
  a list represented through `intVals`. They specify ordinary iterator
  observations in the verification model.
- **PROVED_DERIVED_LEMMA (1 rule):**
  `rule-ebdc46c197940f4814a9d88d03be7d1724ee648b5ba27ec4399dcd5e0a3104a8`,
  the reusable loop-summary rule.
- **DOMAIN_LEMMA (1 rule):**
  `rule-7a7edac73364fddfa1ef4bac81d105b3bf56b8eb38bcf5f58c3e0870f8a6ae55`,
  the `simplification` rule for observing element zero through `intVals`.
  Although it is consistent with the representation and imported subscript
  semantics, Stage 1 does not prove this exact helper before using it, so it
  remains in the trusted mathematical boundary.

The domain-lemma set is **not empty**; it contains exactly the one `valSeqAt`
simplification rule identified above.

## Separately proved derived lemma and evidence

There is exactly one separately proved derived lemma: the loop summary with
source rule ID
`rule-ebdc46c197940f4814a9d88d03be7d1724ee648b5ba27ec4399dcd5e0a3104a8`.

The Stage 1 evidence establishes the required ordering and correspondence:

1. `spec.k` module `LOOP-SPEC` imports `VERIFICATION-BASE` and states the same
   loop reachability relation, including the same loop term, environment,
   scope pre-state, and scope post-state.
2. `verification.k` places the reusable rule only in module `VERIFICATION`;
   `VERIFICATION-BASE` does not contain or import it.
3. `prove.sh` first compiles `verification.k` with
   `--main-module VERIFICATION-BASE` into
   `verification-base-kompiled`.
4. It then runs `kprove` on `LOOP-SPEC` against that base definition.
5. Only after that proof command does the script compile
   `--main-module VERIFICATION`, making the matching reusable summary rule
   available for `FUNCTION-SPEC`.

The rule's `priority(30)` attribute controls reuse after proof and does not
alter the reachability statement proved by `LOOP-SPEC`. The `LOAD-SPEC` and
`FUNCTION-SPEC` claims are proof targets, but no other canonical inventory
rule is an exact reusable restatement of either claim, so they do not create
additional `PROVED_DERIVED_LEMMA` classifications.
