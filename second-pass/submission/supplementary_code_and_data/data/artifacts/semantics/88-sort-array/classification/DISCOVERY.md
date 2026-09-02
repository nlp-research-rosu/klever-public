# Trust-boundary discovery

The canonical inventory contains nine rules, all from the `VERIFICATION`
module. Each rule is classified exactly once and remains in canonical
inventory order in `trust-boundary.json`.

## Classification summary

- **DEFINITION — 8 rules.** `sortArrayBody` and `sortArrayClosure` name and
  expand the translated program body and callable proof value. The two
  `intsVS` equations define a structural conversion, the two
  `nonNegativeIS` equations define a recursive summary predicate, and the two
  `snocVS` equations define append-at-the-end structurally.
- **OPERATIONAL_RULE — 0 rules.** The local module adds no ordinary execution
  or observation behavior other than the trusted fact identified below.
- **PROVED_DERIVED_LEMMA — 0 rules.**
- **DOMAIN_LEMMA — 1 rule.**
  `rule-ab4b49bc5cb4d2f873e2b399b9cb8d81a81689b74a6ddc22dfb813e2f897e479`
  rewrites `array[-1]` to the final value of a sequence represented with
  `snocVS`. This is an additional mathematical fact used to avoid symbolic
  unfolding of an arbitrary-length middle segment.

No inventory rule carries the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas. Stage 1 `prove.sh` first
compiles `verification.k` as module `VERIFICATION`; that compiled definition
already contains the priority-40 negative-index rule. Its only `kprove`
command then proves `spec.k` against that definition. There is no earlier
proof command against a module omitting the rule, and therefore no Stage 1
evidence satisfying the required proof-before-use ordering or exact-rule
correspondence for `PROVED_DERIVED_LEMMA`.

## Domain-lemma set

The domain-lemma set is **not empty**. It consists exactly of the priority-40
negative-index rule listed above. Although its Stage 1 comment calls it a
derived negative-index lemma, the available proof script treats it as part of
the proof definition rather than proving it separately, so it remains inside
the trusted boundary.
