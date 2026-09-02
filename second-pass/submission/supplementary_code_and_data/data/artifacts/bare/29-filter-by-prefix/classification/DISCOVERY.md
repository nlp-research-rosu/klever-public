# Trust-boundary discovery

The exhaustive canonical inventory has SHA-256 `3ecb060b882616a370eae5419482adde58064f9a3c6374dbc81a0471bc36511e` and contains six rules from the local verification-module closure. Every rule is classified exactly once and in canonical inventory order.

## Definitions

All six inventory rules are `DEFINITION`:

- `rule-ac0ad2ee8798223b8d0e68f0c8edbc98f7bc9e543cfba6d48da1cb3944018a09` defines `filterByPrefix` as `filterAcc` with an initially empty accumulator.
- `rule-06feaa8530d12459c98e102bb67013c17f71df32409bc8a99a2f757e94c488e4` defines the empty-input base case of `filterAcc`.
- `rule-01b01b51ccb5f30e112b181d8839f4789ef0b9fcc3d5f02a98fb2f9bc4993603` defines the matching-head recurrence of `filterAcc`. Its `simplification` attribute does not change its definitional role.
- `rule-47fea1538ad0507cb91d9ff53c08576f802ff5036458e5bb1455a1df4a263e0f` defines the nonmatching-head recurrence of `filterAcc`. Its `simplification` attribute does not change its definitional role.
- `rule-95ab8d93624db21de3cda929dad814e59f3f67a33233478cbd9d06222bf7e749` expands the named structural helper `loopBody()` into the translated loop-body statement list.
- `rule-11b0160cb56a842bbc83e22736af7b949ed225b38ba35c6c68f048a2c056b8a0` expands the named structural helper `solutionProgram()` into the translated module used by the end-to-end proof.

None of these is an `OPERATIONAL_RULE`: the inventory contains summary equations and named proof-term expansions, not ordinary execution or observation transitions.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1 `prove.sh` compiles `semantic.k` with the `VERIFICATION` module already included and then runs one `kprove spec.k` command. It does not first prove any inventoried rule against a module lacking that rule, nor does it subsequently add an exactly corresponding reusable rule. The `loop-correct` and `program-correct` items in `spec.k` are proof claims, but they are not inventoried rules reinjected after a prior proof, so they provide no basis for a `PROVED_DERIVED_LEMMA` classification.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule states an additional trusted mathematical fact about strings, prefix testing, append, or list algebra beyond the definitions above.
