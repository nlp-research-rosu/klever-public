# K proof trust-boundary discovery

The canonical inventory at `/reference/rule-inventory.json` contains four
rules, all from `VERIFICATION`. The classifications below follow its order and
use its inventory digest
`f38a1491cb3c65e71c192caf52eb6600fcdf687c33cb0e73a7ecdff92e9a190d`.
No inventory rule carries the `simplification` attribute.

## Classifications

1. `rule-d095c8888afcb3dd088fdc3c664435491743c78be0a54a41138084f98215f5e0`
   is a **DEFINITION**. It expands the named value `multiplyClosure` into the
   closure containing the translated function body. It introduces a named
   proof term rather than asserting an independent mathematical property.
2. `rule-4a53979712cc9f4bc859fe5870bc02792a9f2614c0ffbd65fb212ab383807457`
   is an **OPERATIONAL_RULE**. It is the verification model's execution
   adapter from `#runMultiply(A, B)` to a call of `multiplyClosure`; it does
   not add a mathematical fact about integers.
3. `rule-9dd6dbfcce1300ea93b427dc414913c5a4ca13d4f90781207d2a75f3181ad8e0`
   is a **DEFINITION**. It defines the mathematical contract summary
   `unitDigit(I)` to be `pyMod(I, 10)`.
4. `rule-6aad8f4cafb083a2584e89e9e7ced610b42247ea1e1eadf1af9063b72ec8e2cd`
   is a **DEFINITION**. It defines `unitDigitProduct(A, B)` as the product of
   the two previously defined summaries.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 `prove.sh` first compiles `verification.k` as module
`VERIFICATION`, so all four inventoried rules are already present in the
definition used by the subsequent `kprove spec.k` command. `spec.k` proves
the final `multiply-correct` reachability claim, but neither it nor any other
mounted Stage 1 evidence first proves the exact statement of an inventoried
rule against a module from which that rule is absent. Consequently, no rule
meets the required ordering and exact-correspondence test for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. None of the four rules supplies an additional
trusted mathematical fact: the mathematical-summary rules are definitions,
and the remaining rule is operational.
