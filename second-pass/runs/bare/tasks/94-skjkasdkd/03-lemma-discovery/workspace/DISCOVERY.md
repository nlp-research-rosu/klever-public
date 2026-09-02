# Trust-boundary discovery

The canonical inventory hash is
`3e46f41fca2b599e817e692c7ef1252c24ce1b5baf274b23def3e831810479fe`.
It contains 15 rules, all from the `VERIFICATION` module. Every inventory
rule is classified exactly once, in canonical order, in
`trust-boundary.json`.

## Definitions

All 15 canonical rules are `DEFINITION`.

- `solutionProgram` expands a named proof term to the exact translated program
  AST.
- `programDefs` and `solutionDefs` define structural summaries used to obtain
  the program's function map.
- The three `refPrimeFrom` rules and two `refPrime` rules are the cases and
  recurrence defining the reference primality computation.
- The two `refChoose` rules define its complementary selection cases.
- The two `refLargest` rules define empty-list and recursive-list behavior.
- The two `refDigitSum` rules define the decimal base case and recurrence.
- `refAnswer` defines the top-level mathematical summary by composition.

These rules are equations, recurrences, macro expansions, or structural
helpers. They define the reference vocabulary against which execution is
proved; they do not add separate mathematical facts about that vocabulary.
The canonical inventory reports no rule with a `simplification` attribute.

## Operational rules

There are no `OPERATIONAL_RULE` entries in the canonical inventory. The
inventory contains no K-cell execution transition or observation rule; the
small-step execution rules are in Stage 1's `SEMANTIC` module and are not
canonical inventory entries.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical inventory, so
there are no `PROVED_DERIVED_LEMMA` entries.

The Stage 1 evidence is explicit about the ordering:

1. `prove.sh` compiles `verification.k` into `verification-kompiled`.
2. It then invokes
   `kprove spec.k --definition verification-kompiled --spec-module SPEC`.
3. `spec.k` contains six reachability claims for `is_prime_from`, `is_prime`,
   `choose_prime`, `largest_prime`, `digit_sum`, and the final entry point.

Those six claims are proof goals evaluated together by that final `kprove`
command. None of their exact statements occurs as a rule in
`verification.k` or in the canonical inventory, and Stage 1 does not first
prove one, add it as a reusable rule to a later module, recompile, and use it
for a subsequent proof. Consequently, the mounted evidence does not satisfy
the required proof-before-use criterion for any canonical rule.

## Domain lemmas

The domain-lemma set is empty. No canonical rule is an additional trusted
mathematical fact used to close the proof; the mathematical reference rules
are classified as defining equations and recurrences instead.
