# Trust-boundary discovery

The canonical inventory contains 10 rules, all from the local `VERIFICATION`
module. Each inventory rule is classified exactly once and remains in canonical
inventory order in `trust-boundary.json`.

## Definitions

Nine rules are `DEFINITION`:

- `vowelCodes` expands a macro to the fixed character-code sequence.
- `isVowelCode` defines the vowel predicate.
- The three `removeVowelCodesAcc` equations define its base, vowel, and
  non-vowel recurrence cases.
- `removeVowelCodes` defines the top-level mathematical summary by initializing
  the accumulator.
- `removeVowelsLoopBody`, `removeVowelsBody`, and `removeVowelsProgram` are
  macro expansions naming exact fragments of the translated program AST.

These rules introduce constants, mathematical summaries, recurrences, or named
proof terms. They do not add independently asserted mathematical facts about an
already-defined reference-semantics operation.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-94d2fdc35d3fdf3c396f6195fb860162747c2dc403f48fae46276855a3075f93`,
  which rewrites the supplied semantics' existing `strContains` function for a
  one-character needle and the fixed `vowelCodes` haystack to `isVowelCode`.

This specialization is mathematically plausible, but it is part of
`verification.k` when the Haskell proof definition is compiled. The Stage 1
script never first proves the exact specialization against a module lacking
that rule. Its `priority(40)` attribute only controls rule selection and does
not supply proof evidence. The nearby “proved-by-definition” comment likewise
does not establish a separate proof, so this rule is `DOMAIN_LEMMA`, not
`PROVED_DERIVED_LEMMA`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The Stage 1 evidence is `/reference/k-proof/prove.sh`: it compiles
`verification.k` as module `VERIFICATION` and only afterward runs
`kprove spec.k --definition verification-kompiled`. Thus all 10 inventoried
rules, including the `strContains` specialization, are already present during
the proof. `spec.k` contains three loop claims and one entry-point claim, but
there is no earlier proof command against a rule-free module and no subsequent
module that installs an exactly corresponding proved rule.

## Operational and simplification rules

No canonical inventory rule is classified as `OPERATIONAL_RULE`; the program
execution machinery is imported from the supplied `MPY` semantics, while the
local inventoried AST rules are macros and the remaining local rules are
summary definitions or the domain specialization above.

No canonical rule carries the `simplification` attribute, so the special
classification restriction for simplification rules is vacuously satisfied.
