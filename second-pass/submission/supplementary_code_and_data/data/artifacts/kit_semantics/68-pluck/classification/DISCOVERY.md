# Trust-boundary discovery

The canonical inventory contains 22 rules from the `VERIFICATION` module. Each
canonical `source_rule_id` appears exactly once in `trust-boundary.json`, in the
inventory order.

## Classification summary

| Classification | Count |
|---|---:|
| `DEFINITION` | 20 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 2 |

The definitions fall into two groups:

- Projection-helper definitions:
  `rule-9e2ee339875a1d59e60ef1a09d50617f8c526c60d097a2a486ebed2a648461c5`,
  `rule-ced5adecb9e0d364813f64698375904533f4eeac50b93f2799465c7b5fead6d0`,
  `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d`,
  `rule-7191d5f6c9756673cca00b440958222ca4d2d1d3d4e18cbc994313a0f4340442`,
  and
  `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081`.
  These define the local domain predicate and the guarded, collapsing,
  normalizing behavior of the named `projectIntTotal` proof term.
- Mathematical-summary definitions: the 15 rules from
  `rule-cf4138b8c8c76302d40452525511bd8b4e31a4b3346bb98e6e73d97d1e6c2974`
  through
  `rule-615dd6754d1e5de3108d82927712a0b9350d18eb111423ada2109218959edb7d`.
  They are exhaustive base/recursive or complementary guarded equations for
  `allNonNegative`, `shouldTake`, `nextBest`, `nextBestIndex`, `scanBest`,
  `scanBestIndex`, `afterIndex`, and `resultList`.

There are no `OPERATIONAL_RULE` entries. None of the canonical rules rewrites a
configuration cell or a `<k>` computation. The one rule extending the imported
`applyBin` operation carries `simplification`, so under the required
classification constraint it is a `DOMAIN_LEMMA`, not an operational rule.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1 evidence does not satisfy the required proof-before-use ordering for any
canonical rule:

1. `/reference/k-proof/prove.sh` lines 16–20 compile `verification.k` as
   `VERIFICATION`, including all 22 canonical rules.
2. Its first positive `kprove` is only afterward, at lines 22–25, and uses that
   already extended compiled definition.
3. The second positive proof at lines 27–29 uses the same definition.
4. The other mounted K files contain target or negative-probe claims, not an
   auxiliary verification module omitting a candidate rule and proving its
   exact form.
5. `loop-proof.out`, `full-proof.out`, and `prove-run.out` show `#Top` for the
   program claims under the complete extended theory. They do not establish any
   inventory rule first against a module that excludes that rule.

Accordingly, Stage 1 comments describing cast rules or the addition dispatch
twin as “derived” are not evidence for `PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly two rules:

- `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
  trusts the simplification characterizing `#Ceil` of the imported partial
  `Val`-to-`Int` cast in terms of `definedProjectInt`. This is a fact about an
  imported construct, not merely an equation defining a local summary, and no
  rule-free Stage 1 proof establishes it.
- `rule-5a57a342f46c274d8d94d5f1c7eda4683981fbe24087e787e4a8ce7782c03167`
  trusts the guarded simplification of imported `applyBin("+", V, I)` to
  projected integer addition. It widens the static match available in the
  reference semantics and directly supports the source normalization used by
  the loop proof. Stage 1 compiles this rule before all positive proofs and
  provides no exact prior correspondence proof without it.

The Stage 1 concrete, differential, vacuity, and body-mutation evidence may
support confidence in these rules, but finite or downstream evidence does not
change their classification or provide the required proof-before-use ordering.
