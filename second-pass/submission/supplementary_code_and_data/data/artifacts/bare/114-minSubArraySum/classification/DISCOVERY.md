# Trust-boundary classification

The canonical inventory identifies six rules, all in the local
`VERIFICATION` module. Each is classified exactly once and in canonical
inventory order in `trust-boundary.json`.

## Definitions

The first four rules define the mathematical summaries used in the
postconditions:

- `minPrefix(cons(H, nil)) => H` is the singleton base case.
- The recursive `minPrefix` rule defines the minimum non-empty prefix as the
  minimum of the head alone and the head plus a non-empty prefix of the tail.
- `minSubarray(cons(H, nil)) => H` is the singleton base case.
- The recursive `minSubarray` rule defines the minimum contiguous subarray as
  the minimum of a subarray wholly in the tail and a prefix starting at the
  head.

These are equations specifying the meanings of `minPrefix` and
`minSubarray`, rather than separately asserted mathematical facts, so they are
`DEFINITION`.

The remaining two rules expand named proof terms. `solutionFunctions`
expands to the function-closure map, and `solutionProgram` expands to the
translated module term. They are structural macro definitions and are also
`DEFINITION`.

No canonical inventory entry is an `OPERATIONAL_RULE`. The execution rules
are in the Stage 1 semantics, while the launcher-generated canonical inventory
for this task contains only the six rules above from `VERIFICATION`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` first runs:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX
```

and only afterward runs:

```text
kprove spec.k --definition verification-kompiled
```

Consequently, all six inventoried rules are already present in the compiled
module used to prove `spec.k`. Stage 1 contains no earlier proof of any exact
inventoried rule against a module omitting that rule. In particular, the
comment describing `solutionFunctions` as supporting “circular lemmas” does
not make its macro-expansion rule a separately proved derived lemma; the
actual proved items are the claims in `spec.k`, not this inventoried rule.

## Domain lemmas

The domain-lemma set is empty. None of the six rules adds an independent
mathematical fact beyond the defining recurrences or structural term
expansions.
