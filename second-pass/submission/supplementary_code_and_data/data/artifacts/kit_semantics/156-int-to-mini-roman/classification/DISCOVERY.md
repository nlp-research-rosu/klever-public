# Trust-boundary discovery

The canonical inventory at `/reference/rule-inventory.json` has schema version
2, inventory SHA-256
`da15137333fc4ba0e27fa6e78b326e34c147bb1051cc398ad15e8b90fba881b1`,
and exactly three rules. `trust-boundary.json` preserves their inventory order
and classifies each `source_rule_id` exactly once.

## Definitions

All three rules are `DEFINITION`:

- `rule-73432c3a885f4063bc8df0e53921bf98bff4057d4844018e2315176d083cc1ac`
  expands `intToMiniRomanBody` to the exact translated statement sequence.
- `rule-9c027b657c924d9bded261a2258c44e3b4f2a5adc4d1fa50a891947006f320c6`
  expands `solutionModule` to the named function module.
- `rule-0ea1d474a57944cbe1723cb797da19fe9cb40b152784827f7fc8e7cf966f2e93`
  expands `solutionCall(N)` to the module and parameterized call harness.

These are parse-time macro/structural expansions. They name proof terms and
are removed by expansion before the imported MPY operational semantics
executes the resulting program. Accordingly, none is an `OPERATIONAL_RULE`.
The canonical inventory contains no rule with the `simplification` attribute.

## Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty. Stage 1 `prove.sh` compiles
`verification.k` with all three macro definitions already present and then
proves the target claims. It contains no earlier proof against a module that
omits one of these rules, so there is no Stage 1 evidence satisfying the
required prove-first/exact-correspondence ordering for a derived lemma.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. The local verification-module inventory adds
no mathematical fact trusted to close the proof.
