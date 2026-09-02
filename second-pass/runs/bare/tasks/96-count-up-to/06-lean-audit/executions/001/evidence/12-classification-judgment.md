# Independent Stage 3 classification

The canonical inventory has eight rules, all in the local `VERIFICATION`
module. `MPY` is imported from `semantic.k`, so it is not another local module
inside the `verification.k` closure. None of the eight rules has a
`simplification` attribute.

| Lines | `source_rule_id` | Independent class | Reason |
|---|---|---|---|
| 11–12 | `rule-4c9c7cd0ecff4b21cb2a0220c1266d98e432dae12759c131c91d6693489f0993` | `DEFINITION` | Base equation for the newly declared proof-side function `noFactor`; it names the empty remaining divisor-search suffix. |
| 14–17 | `rule-955cda9f3354ba04534cae8c06c05905914e9d2d6daf0bc6bc5ded052d940be2` | `DEFINITION` | Divisor case of the same recurrence. On the guarded domain it fixes the summary to `false`. |
| 19–22 | `rule-577db1aaf2625dbeb758307db9641573f59928437d750b64a81d788c69b0e08d` | `DEFINITION` | Recursive `noFactor` equation; the candidate divisor strictly advances. |
| 27 | `rule-e47ad287a5faffc436895fc5017ba26a9df44510cd197aba879225609e7c4c40` | `DEFINITION` | First defining branch of the newly declared `isPrime` summary. |
| 28 | `rule-dc7cdce70c542df1714b2772a5d2476a13e792688f8d9cd7a872d34c5d06c842` | `DEFINITION` | Second defining branch of `isPrime`, reducing it to the divisor-search summary. |
| 33–34 | `rule-403f46dd6096062e1aeedc2696c1ce761f7414c3e91f819ddcabea36164a8662` | `DEFINITION` | Base equation for the newly declared `primesFrom` list recurrence. |
| 36–39 | `rule-2ff40da2add1eb80cc1ec89686f3a022e3631a8b2dcf0d901316d114807529a9` | `DEFINITION` | Recursive `primesFrom` equation; it conditionally retains `C` and advances to `C + 1`. |
| 41 | `rule-7cc9f28ac165f611ede21e85e873ac0356fd4511c1ba99151ed097b72984ab3c` | `DEFINITION` | Unconditional alias defining `primesBelow` from `primesFrom`. |

These are not operational rules: none has a `<k>` configuration on its
left-hand side, and their heads are fresh proof-side functional symbols
declared in `verification.k`. They are not proved-derived lemmas: none is first
proved in a module excluding the rule. They are not domain lemmas: each rule
defines one of the newly introduced summary symbols rather than asserting an
independent proposition or rewrite over pre-existing mathematics.

The equations are relevant to the exact postcondition
`<result> .K => primesBelow(N) </result>`. On the claim domains:

- `C >= 2` and `D >= 2` make the three `noFactor` guards exhaustive and
  disjoint; recursion advances `D`.
- The two `isPrime` guards partition integers, and for `C >= 2` the definition
  starts `noFactor` at divisor `2`.
- For `C >= 2`, the two `primesFrom` branches partition `C >= N` and `C < N`;
  recursion advances `C`.
- `primesBelow(N)` starts that recurrence at `2`, matching both `scan(2,N)` and
  the source program's initial candidate.

Accordingly, the independent `DOMAIN_LEMMA` set is genuinely empty.
