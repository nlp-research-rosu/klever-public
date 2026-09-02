# Trust-boundary discovery

The canonical inventory contains six rules, all from the local `VERIFICATION`
module. Each canonical `source_rule_id` is classified exactly once and remains
in inventory order in `trust-boundary.json`.

## Definitions

Five rules are `DEFINITION`.

- The two `allInts` equations are the empty and nonempty structural cases of a
  total predicate. The recursive case descends through the `ValSeq` tail.
- The three `strangeAcc` equations are the greater-than, equal-bound, and
  less-than cases of the named result summary. Their guards partition integer
  bounds. The recursive case appends the two endpoint values and shrinks the
  remaining interval.

These rules define proof terms; they do not add independent algebraic facts or
replace Python execution. None carries the `simplification` attribute.

## Domain lemma

The rule

```k
rule (M:Map K:Int |-> _V:Scope) [K <- undef] => M
  requires notBool K in_keys(M)
  [simplification]
```

is `DOMAIN_LEMMA`. It states an additional Map identity used to normalize the
scope update emitted by frame popping. It does not define a named function or
recurrence, and its `simplification` attribute rules out classifying it as an
operational rule or proved derived lemma under the requested policy.

The Stage 1 ordering also shows that this rule is trusted rather than
separately proved: `/reference/k-proof/prove.sh` lines 17–20 compile
`verification.k`, already containing the rule at lines 31–33, into
`verification-kompiled`. The later `kprove` commands at lines 23–33 both use
that compiled definition. There is no earlier proof command against a module
that omits the rule and proves its exact statement.

The domain-lemma set is **not empty**. It contains exactly the Map-deletion
simplification rule
`rule-565182bf10d31fb24d96318e023c71c80005ab90c1b99978f05bb734ef394503`.

## Proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules in the canonical inventory.

Stage 1 separately proves the `SPEC.loop-invariant` reachability claim:
`prove.sh` lines 23–26 run `kprove` with
`--claims SPEC.loop-invariant`, and `prove.log` line 165 records `#Top`.
However, that claim is not a canonical rule entry, and it is not a prior proof
of the exact statement of any inventoried rule. It therefore supplies no basis
for assigning `PROVED_DERIVED_LEMMA` to an inventory entry.

## Operational rules

There are no `OPERATIONAL_RULE` entries in the canonical local verification
closure. The program-execution rules are imported from the fixed reference
semantics and are outside the launcher-provided canonical inventory.
