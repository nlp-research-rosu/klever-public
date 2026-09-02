# Trust-boundary discovery

The canonical inventory at `/reference/rule-inventory.json` contains five
rules from the local `VERIFICATION` module. Each is classified exactly once
and retained in canonical inventory order in `trust-boundary.json`.

## Definitions

The first four rules introduce and define named mathematical summaries used by
the specification:

- `decimalDigit(N, 1)` defines the units-place case.
- `decimalDigit(N, P)` defines higher positive decimal places with the supplied
  Python-style quotient and remainder operations.
- `decimalDigitSum(N)` defines the sum of all five possible places under the
  stated `0 <= N <= 10000` bound.
- `binaryNumeral(N)` defines the named expected-result term through the
  reference semantics' `binCodes`.

These are equations defining new proof vocabulary, so they are
`DEFINITION`s. No inventoried rule has the `simplification` attribute.

## Trusted domain lemma

Rule
`rule-a85038e1ac209993c7ddd60086463b961c8ffbd45be861486d9c8442d108f370`
rewrites slicing two characters from a string beginning with the character
codes for `0b` directly to its remaining tail. The Stage 1 source describes
this as the identity needed when symbolic `buildIS` evaluation leaves an
opaque tail. It therefore supplies an additional mathematical fact beyond the
ordinary reference-semantics execution path and is classified as a
`DOMAIN_LEMMA`.

The domain-lemma set is **not empty**; it contains exactly that prefix-slice
rule.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications and no separately proved
derived lemmas in the mounted Stage 1 evidence. In `/reference/k-proof/prove.sh`,
`verification.k` is first compiled as module `VERIFICATION`; that compilation
already contains all five inventoried rules. The script then invokes one
`kprove` command on `spec.k` against that compiled definition. It does not
first prove the exact prefix-slice statement against a module from which the
rule is absent, nor does it perform such an ordered proof for any other
inventoried rule. Consequently, the successful Stage 1 `#Top` result proves
the program claim while assuming the prefix-slice rule; it is not evidence
that the rule itself was separately derived.

No rule is classified as `OPERATIONAL_RULE`: the four equations are
specification definitions, while the remaining local execution-shaped rule
was introduced specifically as an unproved symbolic slicing fact rather than
as an ordinary rule of the supplied verification model.
