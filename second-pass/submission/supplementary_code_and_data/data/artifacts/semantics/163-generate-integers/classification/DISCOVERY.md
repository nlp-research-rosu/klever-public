# Trust-boundary discovery

The canonical inventory contains seven rules, all from the local
`VERIFICATION` module. Each is classified exactly once and in canonical
inventory order in `trust-boundary.json`.

## Definitions

All seven rules are `DEFINITION`:

- `generateIntegersBody` is a macro expansion naming the exact translated
  statement sequence of the implementation.
- `solutionModule` and `generateIntegersClosure` are macro expansions that
  assemble named proof terms used by the reachability claim.
- `betweenEndpoints` defines inclusive membership between two endpoints in
  either order.
- The two `keepDigit` equations define the true and false cases of a
  structural selection helper.
- `evenDigits` defines the mathematical result sequence by applying that
  helper, in ascending order, to `2`, `4`, `6`, and `8`.

These are equations, macro expansions, and structural helpers. They do not add
independent mathematical facts beyond the meanings of their newly introduced
symbols. None of the seven inventory records has a `simplification`
attribute.

## Operational rules

The local verification-module closure adds no `OPERATIONAL_RULE`. Execution is
provided by the imported reference semantics; the inventoried local rules only
name program and summary terms.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` first compiles `verification.k` as module `VERIFICATION`,
which already contains all seven inventoried rules. It then invokes:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC --smt-timeout 10000
```

That invocation proves the end-to-end claim in `spec.k` against the definition
containing every inventoried rule. There is no earlier proof command against a
module omitting any candidate rule, and therefore no Stage 1 evidence of the
required prove-before-import ordering or exact reusable-rule correspondence.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. No additional trusted mathematical fact is
present in the canonical local rule inventory.
