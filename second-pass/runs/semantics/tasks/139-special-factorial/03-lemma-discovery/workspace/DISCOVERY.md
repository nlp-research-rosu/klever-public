# Trust-boundary discovery

The canonical inventory contains four rules, all from the local `VERIFICATION`
module. Each rule is classified as `DEFINITION`.

- `rule-061c723304f7123e51ae42344edc69b86c8037ca6606ef3145658939fb695c6b`
  is the non-positive base equation for the total `factorial` summary.
- `rule-458409c7bc07693a15b8bbc9bc5f73e395714f67d4b55f228b0496515b94136f`
  is the positive-input recurrence for `factorial`.
- `rule-edc55d2e0a1a07541a0d8f6c1255456689844a9679ab6259bceb68f8c6465dbe`
  is the non-positive base equation for the total `specialFactorial` summary.
- `rule-0e4e7b60244adfbc0ed7ab152432bbfd95134e586f60ecb865844be14801286a`
  is the positive-input recurrence for `specialFactorial`.

These equations give meaning to the named mathematical summaries used by the
claims. They are neither Python execution/observation rules nor independent
mathematical facts about already-defined terms. None of the inventory rules
carries the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 evidence does not demonstrate the ordering required for
`PROVED_DERIVED_LEMMA`. In `/reference/k-proof/prove.sh`,
`verification.k` is compiled into `verification-kompiled` before `kprove` is
run on `spec.k`. Consequently, all four inventory rules are already in the
proof definition when the two Stage 1 claims are proved. Neither
`special-factorial-correct` nor `special-factorial-loop` first proves the exact
statement of any one of these four rules against a module from which that rule
is absent.

## Domain lemmas

The domain-lemma set is empty.
