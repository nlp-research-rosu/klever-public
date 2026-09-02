# Independent Stage 3 classification

The canonical local closure is the single module `VERIFICATION`. The inventory
contains 13 rules. Classification below was made from the frozen rule text,
the frozen source program, `spec.k`, and the supplied MPY operational
semantics, without relying on the Stage 3 rationale.

| Order | Source span | Source rule ID | Independent class | Reason |
|---:|---:|---|---|---|
| 1 | 9–56 | `rule-7f4f9af315eb522322f17b77c915d50f8bd0611a3572578dfd213fe3f0b32330` | `DEFINITION` | The only rule for the fresh nullary function `solutionBody`; it expands a named proof/program-AST term to the exact translated statement sequence. Expansion precedes fixed-semantics execution and does not summarize or skip an invocation. |
| 2 | 59–64 | `rule-47743bbe3fa51213e3ff4782da02c10b32bb1d47c69138b0c7335259226c16f1` | `DEFINITION` | The only rule for the fresh nullary function `solutionModule`; it names the module AST containing the function definition and `solutionBody`. |
| 3 | 69–71 | `rule-e48e6128a9ac300474330de945f6d5631d68771748dc45bf6155fea948b7e0a8` | `OPERATIONAL_RULE` | An ordinary launcher rewrite. It turns `#runEvenOdd(N)` into fixed MPY operations `#loadAll(solutionModule)` followed by a normal `Call`; it neither asserts a mathematical fact nor replaces the function body’s execution. |
| 4 | 76 | `rule-728172cfae584189cc501f826bf6a452bc87072ce2d8402236a6dee15188e3ae` | `DEFINITION` | The sole defining equation for the fresh arithmetic summary helper `leadingDigit`. |
| 5 | 79–80 | `rule-e2eb7b8d61dc0eea652c0941f5813de34e27998af2a56227f44df813add45185` | `DEFINITION` | The sole defining equation for the fresh helper `currentBlock`. On `100 ≤ N < 1000`, it equals the source expression `(N % 100 - leadingDigit(N)) // 10 + 1`; the shifted numerator is positive, so the supplied integer semantics gives the same quotient. |
| 6 | 83–84 | `rule-11b0c5550e336c932bc95e87975bce569169d171a88dd22795a8a0309cca5e03` | `DEFINITION` | A guarded defining clause of the fresh summary function `evenPalindromes` for `1 ≤ N < 10`. |
| 7 | 85–86 | `rule-a81d2d672fa0c967d9c92829b059e3e2194f5d86224e4f88113a08ee0987f246` | `DEFINITION` | A guarded defining clause of `evenPalindromes` for `10 ≤ N < 100`. |
| 8 | 87–92 | `rule-7ded12e98989cd9ee67f2d9c8a6eb6189f7c008b29745a63a5f3acff091a2557` | `DEFINITION` | A guarded defining clause of `evenPalindromes` for `100 ≤ N < 1000`, using the two fresh summary helpers. |
| 9 | 93 | `rule-02dafb48eb7be78148da42c48c6295fde126d5750e3777bc30e175feb234af45` | `DEFINITION` | The final defining clause of `evenPalindromes` at the isolated upper endpoint `N = 1000`. |
| 10 | 96–97 | `rule-e61ad1766417d0961d5ec6a0055a5808dc1651b3231e0af7e0c924207408ef6e` | `DEFINITION` | A guarded defining clause of the fresh summary function `oddPalindromes` for `1 ≤ N < 10`. |
| 11 | 98–100 | `rule-c0ba22541fd6907bd6221f3194ba24a1b03a82feae66249a899ed0f4b3d5552d` | `DEFINITION` | A guarded defining clause of `oddPalindromes` for `10 ≤ N < 100`. |
| 12 | 101–106 | `rule-e1565647ff7402e03fd16b14fca74d9c3fc1f03ac35ee76fad24cfa74623c8ac` | `DEFINITION` | A guarded defining clause of `oddPalindromes` for `100 ≤ N < 1000`, using the two fresh summary helpers. |
| 13 | 107 | `rule-5f65dc740e7e4e89319a97064f5be743c7ed5272dfb6c1586b823ae1013d6225` | `DEFINITION` | The final defining clause of `oddPalindromes` at the isolated upper endpoint `N = 1000`. |

## Cross-rule judgment

- Independent totals: 12 `DEFINITION`, 1 `OPERATIONAL_RULE`, 0
  `PROVED_DERIVED_LEMMA`, and 0 `DOMAIN_LEMMA`.
- No rule qualifies as `PROVED_DERIVED_LEMMA`: Stage 1 contains no earlier
  bridge-free proof of any exact rule followed by later use. The summary
  equations are present in the verification module from the outset.
- No rule is a hidden `DOMAIN_LEMMA`: every arithmetic equation has a fresh
  summary/helper symbol on its left-hand side and is a defining clause.
  There is no non-definitional theorem about pre-existing arithmetic or
  palindrome predicates.
- The four guards for each even/odd summary are disjoint and cover every input
  in the frozen source contract `1 ≤ N ≤ 1000`.
- The inventory records no rule-level `simplification` attribute. The rules
  belonging to K functions are all independently classified as definitions,
  so the simplification-class restriction is satisfied in any event.
- Exhaustive finite validation over all 1,000 contract inputs found zero
  mismatches among the frozen source formula, the Stage 3 summary equations,
  and an independently enumerated palindrome oracle. Counterfactual changes
  to the current-block increment, parity branch, or upper endpoint were
  detected. This validates relevance and discriminating behavior; it is
  supporting evidence rather than the basis of the syntactic classification.
