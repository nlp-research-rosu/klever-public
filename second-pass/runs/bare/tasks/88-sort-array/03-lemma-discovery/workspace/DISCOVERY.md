# Trust-boundary discovery

The canonical inventory hash is
`84940db527ace0ce0f07ad3424ced9f275db79b29ec0266a21eaf17e7c2056c4`.
The inventory contains 11 rules, all from `MPY-VERIFICATION`, and every rule
is represented exactly once in `trust-boundary.json` in canonical inventory
order.

## Classification

All 11 rules are `DEFINITION`:

- The two `expectedSort` equations define the empty and nonempty cases of the
  named postcondition summary.
- The `endpointEven` equation defines the endpoint-parity Boolean used by that
  summary.
- The two `nonnegative` equations are the base case and structural recurrence
  defining the HumanEval input-domain predicate.
- The three `ascending` equations are the empty, singleton, and recursive
  cases defining the ascending-order observer.
- The three `descending` equations are the corresponding cases defining the
  descending-order observer.

Although the last three groups are executable observers, their inventoried
rules are equations and structural recurrences defining mathematical
predicates. They do not advance a program configuration or introduce a
separate fact about an already defined predicate, so they are definitions
rather than operational rules or lemmas.

The canonical inventory gives every rule an empty attribute list. In
particular, there are no `simplification`-attributed rules requiring a
`DEFINITION` versus `DOMAIN_LEMMA` decision.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first runs:

```text
kompile semantic.k --backend haskell --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX
```

This installs the complete `MPY-VERIFICATION` module, including all 11
inventoried rules, into the definition used for the later and only `kprove`
command:

```text
kprove spec.k --definition semantic-kompiled --spec-module SPEC
```

There is no earlier `kprove` invocation against a module that omits any
inventoried rule, and `spec.k` contains reachability claims rather than
exact claims proving any inventoried equation before installation. The
preceding CPython checks and `krun` executions are tests, not separate proofs
of exact reusable rules. Consequently, Stage 1 supplies no ordering evidence
that could justify `PROVED_DERIVED_LEMMA` for any inventory entry.

## Domain lemmas

The domain-lemma set is empty. None of the inventoried rules adds a trusted
mathematical fact used to close the proof; each merely unfolds a named
summary or recursively defined predicate.
