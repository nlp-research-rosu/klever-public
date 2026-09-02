# Trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, with inventory
SHA-256:

```text
dcee802c03417266ab4623041694bde1adf79041f845102f9e270390ab64a2c7
```

It contains six unique `source_rule_id` values, all in module
`VERIFICATION`, all carrying the `simplification` attribute. Each appears
exactly once and in canonical inventory order in `trust-boundary.json`.

## Classification

All six rules are `DEFINITION`.

- `rule-7123...` is the nonpositive base equation for `digitResult`.
- `rule-9fdc...` is its guarded terminal one-digit equation.
- `rule-974c...` is its fold-oriented positive recurrence.
- `rule-eaf0...` is the nonpositive base equation for `fizzResult`.
- `rule-3758...` is its qualifying-candidate recurrence.
- `rule-1815...` is its complementary nonqualifying recurrence.

These rules only define the mathematical accumulator summaries
`digitResult` and `fizzResult`. They do not match a K configuration, program
AST node, continuation, environment, or state cell, so none is an
`OPERATIONAL_RULE`. Fold orientation is used to make symbolic simplification
terminate; it does not change their role as recurrence equations.

The Stage 1 audit corroborates this reading. `/reference/k-proof/PROOF.md`
labels the rules as a definitional summary, derived definitional equation, or
definitional recurrence, and explicitly says that no rule intercepts a
program AST term.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The required proof-before-admission evidence is absent for every canonical
rule. `/reference/k-proof/prove.sh` first compiles `verification.k`—already
containing all six inventory rules—into `verification-kompiled`, and only
then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It does not first prove the exact statement of any inventory rule against a
module from which that rule is absent. The loop claims `SPEC.inner-loop` and
`SPEC.outer-loop` are machine-checked reachability claims, but they are not
rules in the canonical inventory and therefore are not entries in this
classification.

## Domain lemmas

The domain-lemma set is empty.

No canonical rule adds an independent arithmetic or domain fact beyond the
guarded base/terminal/recurrence equations that define the two summary
symbols. In particular, the terminal `digitResult` equation is classified as
a defining case, not promoted to a proved lemma merely because Stage 1 calls
it a “derived definitional equation.”
