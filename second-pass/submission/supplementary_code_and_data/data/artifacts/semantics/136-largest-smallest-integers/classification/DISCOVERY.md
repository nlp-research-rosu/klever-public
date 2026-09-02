# K proof trust-boundary discovery

The canonical inventory at `/reference/rule-inventory.json` contains 26 rules,
all in the local `VERIFICATION` module. Its declared inventory digest is
`c546cc66576bdf88dd066e086ead92df73aa01251b15271d8bc4c78b5a3b2273`.
Classification used the inventory as exhaustive and retained its rule order.

## Classification summary

| Classification | Count | Basis |
|---|---:|---|
| `DEFINITION` | 25 | Equations, guarded definitional cases, recurrences, and named proof-term expansions |
| `OPERATIONAL_RULE` | 1 | A k-cell iterator execution/refinement rule |
| `PROVED_DERIVED_LEMMA` | 0 | No inventory rule has the required prove-before-use evidence |
| `DOMAIN_LEMMA` | 0 | No additional trusted mathematical fact occurs in the inventory |

The sole `OPERATIONAL_RULE` is
`rule-5b53e5e1e7c389a2532855b2ec7b9b198ac32e2c188993cc5f36766b5113bf5f`.
It handles `#iterNext` in the k-cell for an integer-valued list head and exposes
that same head through the defined `intValue` helper. It is an execution rule
in the verification model, not a separately asserted mathematical theorem.

The remaining rules are `DEFINITION`s:

- `intValue` defines the identity projection on an `Int`.
- `scanBody`, `finishBody`, `solutionBody`, and `largestSmallestModule` expand
  named proof terms into the translated program constructors.
- The four guarded `negStep` cases and four guarded `posStep` cases define the
  sentinel-based extrema updates by exhaustive arithmetic cases.
- `negFold`, `posFold`, and `finalValue` are base/recursive definitions over
  `ValSeq`.
- `allInts` structurally defines the admissible-input predicate.
- `optionalNeg` and `optionalPos` define conversion from the internal zero
  sentinels to result values.

No inventory rule carries the `simplification` attribute. Thus there is no
special simplification-attributed rule requiring a `DOMAIN_LEMMA` choice.

## Separately proved derived lemmas

There are **no separately proved derived lemmas**.

The mounted Stage 1 `prove.sh` first compiles `verification.k` as
`VERIFICATION`, so all 26 inventory rules are already present in
`verification-kompiled`. It then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

That invocation proves the `scan-loop` and `entry-point-correct` reachability
claims from `spec.k`. It does not first prove the exact statement of any
inventory rule against a module lacking that rule, and it does not subsequently
introduce such a proved rule for reuse. In particular, the comment describing
the iterator rule as a conservative refinement is not prove-before-use
evidence. The `scan-loop` claim is proof evidence for the loop summary claim,
but it is not itself a canonical inventory rule and is never promoted into
`verification.k` as an exact reusable rule.

## Domain lemmas

The domain-lemma set is **empty**. All mathematical-summary rules are
definitional equations or recurrences, while the only non-definitional rule is
the operational iterator refinement described above.
