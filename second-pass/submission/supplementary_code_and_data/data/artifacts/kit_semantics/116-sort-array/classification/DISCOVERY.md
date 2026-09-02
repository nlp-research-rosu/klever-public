# Rule trust-boundary discovery

## Canonical inventory

The exhaustive source is `/reference/rule-inventory.json`, with inventory
SHA-256:

```text
dc118fb2034590e8e04149fd7a07acea6f25a1a3a3647e0f86dec6fe34a96c14
```

It contains four rules, all from module `VERIFICATION`. Every canonical
`source_rule_id` appears exactly once in `trust-boundary.json`, in inventory
order. None of the four rules carries the `simplification` attribute.

## Classifications

### `rule-f5c7b761ec71892275f909c07e8f29124daca7a634e74c5709cda21666d9b165`

Classification: `DEFINITION`.

This equation defines the empty-sequence base case of the newly declared total
predicate `allIntVS`. It is a structural definition, not a Python execution
rule or an additional mathematical assertion.

### `rule-581f4df071fdd7d974c5141cf36a1e876f38b798cc51952636578533c09a0f8a`

Classification: `DEFINITION`.

This equation defines the `vCons` case of `allIntVS`: the head must satisfy the
existing sort predicate `isInt`, and the definition recurses on the strictly
smaller tail. Together with the base case, it is the structural recurrence
defining the domain predicate.

### `rule-7a08aa58034b9a659c1e60660998e0b301a0f3e3408204cc84b658c58946b4d0`

Classification: `DEFINITION`.

This is the `I >=Int 0` defining equation for the newly declared total summary
`popcountAbs`. It names the fixed-semantics computation
`cntSub(binCodes(I), iCons(49, .IntSeq))`; it does not replace an operational
configuration or state transition.

### `rule-caabcce04b85453cd68f8e2e64ab67393a09fdfcffd4cf6a5de838b958201752`

Classification: `DEFINITION`.

This is the complementary `I <Int 0` defining equation for `popcountAbs`, using
`0 -Int I` as the magnitude. The two guarded equations are a case-split
definition of the named summary, not separately asserted mathematics.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

Stage 1's `prove.sh` first compiles `verification.k` into
`verification-kompiled` and then runs:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Thus all four inventoried rules are already present in the proof definition
when the claims are proved. The `key-nonnegative` and `key-negative` claims
machine-check execution of the source lambda against the defined
`popcountAbs` term, but `prove.sh` does not first prove the exact statement of
any inventoried rule against a module excluding that rule. The required
proof-before-installation evidence therefore does not exist for any rule.

The negative `spec-vacuity.k` and `spec-body-mutation.k` runs are validation
probes, not proofs of reusable rules.

## Operational rules

There are no `OPERATIONAL_RULE` classifications. All four rules rewrite only
the two proof-local mathematical functions `allIntVS` and `popcountAbs`; none
matches a K configuration cell, program expression, continuation, heap,
binding, or control state.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule introduces an additional
trusted mathematical fact used to close the proof; all four are equations
defining proof-local summaries.
