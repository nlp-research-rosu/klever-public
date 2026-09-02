# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`
`360e01670f3b99020548a8895a06b99e29352f5581ab4741bdfafc1dec0ce0da`.
It contains four rules, all in the mounted Stage 1 `VERIFICATION` module.
`trust-boundary.json` preserves their inventory order and classifies every
`source_rule_id` exactly once.

## Classification

All four rules are `DEFINITION`. They are the guarded branches of the
`[function, total]` symbol `chooseNumSpec(Int, Int)`:

1. `rule-05e369c2e0f0a26d0d7e674102a669feb198db11697b02b0e440dae13cd6c789`
   defines the result when `X > Y`.
2. `rule-18311e31edf98c4536c300005037838e4651a7b61c9d5624cbb197cfddea4789`
   defines the result when the interval is nonempty and `Y` is even.
3. `rule-c368375f7e518bf5b5f01ece3f7c41709c726a6ea30af9bebc2373407ae0c2c9`
   defines the result when `Y` is odd and `Y - 1` remains in the interval.
4. `rule-958329aed53dacc63f3d6c9422ab4eea2c1be9b87f0cbe409620d2734fa18f44`
   defines the remaining odd-endpoint case, where no even candidate lies in
   the interval.

Their left-hand sides match only the named mathematical summary. They do not
match an MPY configuration cell, source AST execution term, call, return,
continuation, or observation construct. Consequently none is an
`OPERATIONAL_RULE`.

The inventory contains no rule with the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The mounted Stage 1 `prove.sh` compiles `verification.k` as module
`VERIFICATION` and then runs `kprove spec.k` against that compiled definition.
Thus all four inventoried equations are already present when the target claims
are proved. Stage 1 contains no earlier proof against a module omitting any one
of these rules, and no evidence establishing exact rule correspondence before
admission. The target `#Top`, mutation probes, and differential test validate
the finalized proof but do not meet the required rule-free-first ordering for
a separately proved derived lemma.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule is an additional
mathematical fact trusted to close the proof; the four rules collectively
define `chooseNumSpec`.
