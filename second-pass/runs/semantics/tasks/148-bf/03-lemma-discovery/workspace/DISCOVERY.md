# K proof trust-boundary discovery

The canonical inventory identifies 32 rules in the local verification-module
closure, all from `BF-VERIFICATION`. The inventory checksum copied into
`trust-boundary.json` is
`32b8f6680c4da8b95e04a35fe8a501b6b875819997e01433ae305f5d963eeb07`.

## Classification summary

- **DEFINITION — 29 rules.** These are the three program/proof-term
  expansions (`bfBody`, `bfCall`, and `bfRun`), the independent contract
  summaries (`planetVals` and `expectedBetween`), the eight `planetCodes`
  equations, the eight `planetPosition` equations, and the eight
  `planetExpr` equations. Each is an equation, macro expansion, constructor
  mapping, or structural proof helper. None asserts an extra mathematical
  fact beyond the named term it defines.
- **OPERATIONAL_RULE — 3 rules.** The three rules over
  `#validCases(Int, Int)` execute the target, observe its result with an MPY
  `Assert`, and advance or terminate the deterministic 64-case loop. They are
  execution/observation rules in the verification harness.
- **PROVED_DERIVED_LEMMA — 0 rules.**
- **DOMAIN_LEMMA — 0 rules.**

The canonical inventory contains no rule carrying the `simplification`
attribute, so there is no simplification-attributed rule requiring a
`DEFINITION`/`DOMAIN_LEMMA` choice.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 ordering evidence does not establish the required two-stage
pattern for any inventory rule. In `prove.sh`, `verification.k` is first
compiled directly into `verification-kompiled`; `kprove` then proves the
claims in `spec.k` against that already-complete module. The script checks
that this target-proof command prints exactly `#Top`, but it never proves an
inventory rule against a module lacking that rule and never subsequently
installs an exact corresponding rule. The three claims in `spec.k` prove the
64 valid ordered pairs and the two invalid-name partitions as end goals; they
are not reusable rules in the canonical inventory.

Accordingly, no comment or successful end-to-end claim is treated as evidence
for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. No inventory rule is an additional trusted
mathematical fact used to close the proof: the mathematical-looking rules are
definitional encodings of the planet sequence, indices, expressions, or
expected slice, while the remaining three rules are operational proof-harness
steps.
