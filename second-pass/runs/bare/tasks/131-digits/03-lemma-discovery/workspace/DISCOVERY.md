# Trust-boundary discovery

The canonical inventory has SHA-256
`213abec6453da6d80e355466d7711c50d96f53815539caa490ba371a6491b303`
and contains 12 rules, all from the `VERIFICATION` module. The classifications
follow that inventory exactly; rules outside it were not added.

## Definitions

Eleven rules are definitions:

- `digitsCond`, `digitsLoopBody`, and `SolutionProgram` expand named proof
  terms into the exact translated condition, statement sequence, and closed
  program term.
- The three `addOddDigit` rules are the exhaustive conditional equations for
  the accumulator update.
- The two `oddProductFrom` rules are its base and recursive fold equations,
  while `oddProduct` supplies the initial zero sentinel.
- The two `finalScratchDigit` rules define the base and recursive cases of the
  operational scratch-cell summary.

These rules introduce named terms or mathematical recurrences; they do not
assert independent facts beyond those definitions.

## Operational rule

`rule-1b6dfc30f83e14335a83a1746f3105c6dee0842578ac512515f9f976bcf8c44d`
is `CheckProgram(P, P) => ProgramsMatch`. It is an observation rule used by
Stage 1 `prove.sh` lines 48–57 to recognize structural equality between
`SolutionProgram` and the generated `solution.mpy`. It is therefore classified
as `OPERATIONAL_RULE`, not as a mathematical lemma.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 evidence does not establish the required proof-first ordering for
any inventory rule. `prove.sh` lines 41–44 first compile `verification.k`,
which already contains every inventoried rule. Its sole `kprove` invocation,
at lines 61–63, then proves the two reachability claims in `spec.k` against
that compiled definition. There is no earlier proof against a module omitting
an inventoried rule, and neither claim is an exact reusable rule appearing in
the canonical inventory.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule is an additional trusted
mathematical fact used to close the proof; the mathematical-summary rules are
recurrence definitions, and the remaining rule is the structural observation
described above.
