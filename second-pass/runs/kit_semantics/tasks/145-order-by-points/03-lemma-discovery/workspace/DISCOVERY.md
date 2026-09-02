# Trust-boundary rule discovery

## Canonical scope

The sole classification source is
`/reference/rule-inventory.json`, whose canonical inventory hash is
`d1938e7b1244c903982851964801e608d93aaaa374c0212142e8a48ca89529d1`.
It contains 20 rules, in order, from `VERIFICATION-SYNTAX` and
`VERIFICATION`. `trust-boundary.json` preserves that order and includes each
canonical `source_rule_id` exactly once.

The inventory contains no rule with the `simplification` attribute. It also
contains no rule over `<k>` or another configuration cell, so none is an
ordinary execution or observation rule in the local verification model.

## Classification result

All 20 canonical rules are `DEFINITION`:

- The first four rules expand the syntax names `digitSumLoopBody`,
  `digitSumBody`, `orderByPointsBody`, and `solutionModule`. They are macro
  equations naming exact program terms.
- The `magnitude`, `leadingDigit`, `lowerDigitSum`,
  `lowerDigitSumAcc`, and `signedDigitSum` rules are guarded equations or
  recurrences defining the mathematical digit summaries used in the claims.
- The three `allInts` rules structurally define the target claim's input-domain
  predicate.
- The final `expectedOrder` rule defines a named proof term by expanding it to
  the supplied `sortKeyVS` term with the exact `digit_sum` closure. It does not
  add an ordering, permutation, or stability fact about `sortKeyVS`.

There are no `OPERATIONAL_RULE` entries because no canonical rule performs or
observes machine execution. The execution semantics used by Stage 1 are
imported from the supplied MPY modules and are outside this launcher-generated
local-rule inventory.

## Separately proved derived lemmas

There are no canonical rules classified as `PROVED_DERIVED_LEMMA`.

Stage 1's `prove.sh` runs:

```sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

The saved `/reference/k-proof/proof-logs/kprove.out` begins with `#Top`, proving
the three reachability claims in `spec.k`. However, the proof definition used
by that command already contains every rule in the canonical inventory.
Stage 1 does not first prove the exact statement of any reusable inventory rule
against a module that omits that rule and then add the proved rule afterward.
Consequently, no inventory entry meets the required evidence ordering for
`PROVED_DERIVED_LEMMA`.

In particular, `SPEC.digit-sum-loop` is described in Stage 1's `PROOF.md` as a
derived loop circularity, but it is a reachability claim in `spec.k`, not a
`source_rule_id` in the canonical rule inventory. It therefore is not an entry
to classify here and cannot turn any of the 20 defining equations into a
separately proved derived rule.

## Domain lemmas and remaining trust

The domain-lemma set is empty.

No canonical rule states an additional trusted mathematical fact beyond a
definition. Stage 1's material result-bearing trust boundary is the opaque
`sortKeyVS` primitive imported from the supplied reference semantics. That
primitive is outside the canonical local verification-module rule inventory;
the local `expectedOrder` equation merely names its application and remains a
`DEFINITION`.
