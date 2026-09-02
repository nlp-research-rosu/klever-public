# K proof trust-boundary discovery

The canonical inventory has SHA-256
`346c37900a0d61a96fe77882416afef84c949544ffd22220a54a8d7281f6c843`
and contains 13 rules from `VERIFICATION`. Every inventory rule is classified
exactly once and in canonical inventory order in `trust-boundary.json`.

## Classification basis

- `solutionBody` and `solutionModule` are `DEFINITION` rules. They expand named
  proof terms into the translated program body and enclosing module AST.
- `#runEvenOdd` is an `OPERATIONAL_RULE`. It is the verification model's
  execution launcher: it loads the module and invokes the target function.
- `leadingDigit` and `currentBlock` are `DEFINITION` rules for arithmetic
  summaries used by the specification.
- The four region equations for `evenPalindromes` and the four region equations
  for `oddPalindromes` are `DEFINITION` rules. Together they define the
  piecewise mathematical summaries over one-digit inputs, two-digit inputs,
  three-digit inputs, and the endpoint 1000.

The inventory has no rule carrying the `simplification` attribute.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications.

The Stage 1 `prove.sh` first compiles `verification.k` as module
`VERIFICATION`, with all 13 inventoried rules already present, and only then
runs `kprove spec.k` against that compiled definition. The four claims in
`spec.k` prove executions over the input regions, but Stage 1 does not first
prove the exact statement of any inventoried reusable rule against a module
from which that rule is absent. Therefore none satisfies the required evidence
and ordering for a separately proved derived lemma.

## Domain lemmas

The domain-lemma set is empty. The palindrome-count formulas occur as the
defining equations of the named mathematical summaries; the inventory contains
no additional trusted mathematical fact about those summaries.
