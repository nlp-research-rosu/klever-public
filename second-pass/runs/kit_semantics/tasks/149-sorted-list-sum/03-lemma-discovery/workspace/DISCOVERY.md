# Trust-boundary discovery

## Canonical inventory

The sole rule source for this classification is
`/reference/rule-inventory.json`. Its inventory SHA-256 is
`b08ce0100e0f2d9b83fee2942ff1b1067ccf724a2358ff8bfa0ff65457250849`,
and it contains nine rules in the local verification-module closure. Every
canonical `source_rule_id` appears exactly once and in canonical order in
`trust-boundary.json`.

## Classifications

Eight rules are `DEFINITION`:

- The two `stringsOnly` equations define the empty and recursive cons cases of
  the input-domain predicate.
- The four `scanEven` equations define its empty case, even-string case,
  odd-string case, and non-string totalization case. The two rules carrying
  `simplification` are still defining recurrence equations; that attribute
  changes their proof-time evaluation behavior but does not turn them into
  additional mathematical facts.
- `sortedListSumBody` and `sortedListSumModule` are macro expansions defining
  named constructor-level proof terms. The `[macro]` attributes are on their
  syntax productions, while the canonical inventory records their expansion
  rules.

No canonical rule is an `OPERATIONAL_RULE`. None of the nine rules is an
ordinary execution or observation rule over the K configuration; the actual
Python execution rules come from the supplied `MPY` semantics outside this
local verification-module inventory.

## Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty.

In particular, the Stage 1 report describes
`#Ceil(seqLen(V)) => #Top requires isStrV(V)` as a derived lemma, but the
required proof ordering is absent. Stage 1 `prove.sh` first compiles
`verification.k`, which already contains that simplification rule, into
`verification-kompiled`. Every subsequent `kprove` command uses that compiled
definition. There is no command that first proves the exact definedness
statement against a module that omits the rule, and neither the expected-failure
mutation probes nor finite differential tests establish that exact universal
statement.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

- `rule-1136beadf72d0cbc65d91ccaf863bbe8bdb49cd73e5a05cca27d05c484b771b6`:
  `#Ceil(seqLen(V)) => #Top requires isStrV(V) [simplification]`.

This rule is an additional definedness fact used to close symbolic reasoning.
It is not an equation defining `seqLen`, `isStrV`, or a new summary symbol, and
Stage 1 does not separately prove it before admitting it into the verification
theory. Under the allowed classifications, it is therefore a `DOMAIN_LEMMA`.
