# Trust-boundary discovery

The canonical inventory hash is `64981393230dd7f9e3ca36660db17e1ce1dc367753e244d73a67ec75c7bf2714`. Its 13 rules occur in the `VERIFICATION` module, and `trust-boundary.json` preserves their inventory order and classifies each exactly once.

## Classification basis

All 13 rules are `DEFINITION` rules:

- `solutionProgram` expands a named proof term to the translated `solve` AST. Stage 1 separately checks this expansion against parsed `solution.mpy` with two `kast` commands and `cmp`.
- The two `oracleDigitSum` equations define decimal digit sum by base case and recurrence.
- The `oracleBinary`, `oracleBinaryPositive`, and `appendOracleBit` equations define binary conversion and its string-construction helpers.
- `sameValue` defines the string-`Value` equality observer.
- `checkInput` defines the named proof term comparing execution of `solutionProgram` with the independent oracle result.
- The two `checkRange` equations define exhaustive checking over a half-open integer range.

These are equations, recurrences, a macro expansion, or structural helpers defining mathematical summaries and named proof terms. None is an ordinary state-transition or observation rule of the verification model, so the inventory contains no `OPERATIONAL_RULE` entries. Execution rules in `semantic.k` are outside the launcher-declared canonical verification-module inventory and therefore are not additional classification targets.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The Stage 1 `prove.sh` compiles `semantic.k` once, with `verification.k` and every inventoried rule already present. It then runs `kprove` on the eleven range claims in `spec.k`. It does not first compile a module omitting any inventoried rule, prove that rule's exact statement, and subsequently introduce the rule. The successful range claims are proof targets, not separately established reusable rules from the inventory, so they do not supply the required ordering or exact-correspondence evidence.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule asserts an additional mathematical fact beyond the definitions used to construct and evaluate the proof terms.
