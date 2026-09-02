# Trust-boundary discovery

The canonical inventory contains four rules, all from the `VERIFICATION`
module. Each inventory rule is classified exactly once and remains in canonical
inventory order in `trust-boundary.json`.

## Definitions

- `rule-07c48bd418c1f380b592ff32808bf84ee7148c6cb962214c1eb5e62fb1389d2d`
  is a macro expansion from `chooseNumProgram` to the translated constructor
  tree for `choose_num`.
- `rule-8fc6fcfc4c25cbda5cad5add17e985d6f0d2c48e69c06c6076d9a90cfcd156c9`
  defines the Boolean summary `noEvenInRange(X, Y)`.
- `rule-73eb6eedbfbf548fbcd47b0d6c8e9316fc986455b8b3bbb68501e642a20ccca2`
  defines the Boolean contract summary `chooseNumContract(X, Y, R)`.

These are equations defining named proof terms or mathematical summaries, so
they are `DEFINITION` rules rather than independently trusted mathematical
facts.

## Operational rule

`rule-1cbc5b8826eb3184ebd455e6c0eafb627050f7eb83a90789adfde576808f048f`
is `OPERATIONAL_RULE`. It observes `VInt(R)` in the K cell, consumes the pending
`checkChooseNum(X, Y)` continuation, and produces the Boolean result of the
defined contract checker.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules. Stage 1 `prove.sh` first invokes
`kompile semantic.k --main-module VERIFICATION`, which compiles the
`VERIFICATION` module with all four inventory rules present. It then invokes
`kprove spec.k` against that compiled definition. The eight claims in `spec.k`
prove executions and contract checks, but Stage 1 contains no earlier proof of
the exact statement of any reusable inventory rule against a module from which
that rule was absent. Consequently, none meets the required proof-order and
exact-correspondence criteria.

## Domain lemmas

The domain-lemma set is empty. No inventory rule supplies an additional
mathematical fact beyond the definitions and the operational observation step.
The canonical inventory also reports no rule carrying the `simplification`
attribute.
