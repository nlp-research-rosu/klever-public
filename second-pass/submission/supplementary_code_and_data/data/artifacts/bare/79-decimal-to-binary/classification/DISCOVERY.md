# Trust-boundary discovery

The canonical inventory has SHA-256
`8ca2a5f1a90d61032329f1598dcd845621cd681c0e59b1c0e082b1fc9c6391af`
and contains two rules, both in module `VERIFICATION`. Each rule is classified
exactly once and retained in canonical inventory order in
`trust-boundary.json`.

## Definitions

- `rule-ed8bbd309f359712e14b367074db45188fe24eaf8c4627ee880a9f79a085944d`
  is the guarded nonnegative branch of `decimalToBinarySpec`. It defines the
  named contract summary as the binary digits surrounded by `db`.
- `rule-a6053be073dfd18cdaa5f54e44324cf4a4b209cc24dc48ad172447920b03637f`
  is the guarded negative branch of the same function. It defines the result
  that follows Python's negative `bin` rendering and the solution's `[2:]`
  slice, again surrounded by `db`.

These are equations defining a named mathematical summary, so both are
`DEFINITION`. Neither is an ordinary execution rule: execution is modeled by
the rules in `SEMANTIC`, while these two rules give the reference result used
on the destination side of the reachability claims.

## Separately proved derived lemmas

There are no separately proved derived lemmas. The Stage 1 `prove.sh` first
compiles `verification.k` into `.kbuild` and only afterward runs
`kprove spec.k --definition .kbuild`. Consequently, both inventoried rules are
already present in the definition used to prove the claims. Stage 1 contains
no proof command that establishes either exact rule statement against a module
from which that rule is absent, so neither meets the evidence requirement for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. The inventory contains no additional trusted
mathematical fact; both inventoried rules are definitional branches of the
reference function. Neither rule carries the `simplification` attribute.
