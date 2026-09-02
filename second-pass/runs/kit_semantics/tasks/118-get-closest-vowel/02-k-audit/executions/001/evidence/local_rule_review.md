# Reviewer rule-by-rule classification

This is the reviewer-authored classification of every proof-local declaration,
rule, and positive claim. Exact normalized text and hashes are in
`rule_inventory.txt`.

## `foundation.k` declarations

| Lines | Item | Classification and decision |
|---|---|---|
| 7–10 | `isVowelBody`, `getClosestBody`, `getClosestLoopBody`, `getClosestProgram` | Four syntax macros. Sound compile-time aliases: fresh expanded KORE for `getClosestProgram` is byte-identical to trusted regeneration of `solution.mpy`. They add no runtime behavior. |
| 12 | `closestCandidate` | Partial mathematical function. Sound: it names the singleton containing `intSeqAt(CS,I)`; every theorem-relevant use is in bounds. It is correctly not marked `total`. |
| 13 | `vowelPred` | Total Boolean function. Sound and exhaustive for all integers: one unconditional equation tests exactly the ten ASCII vowel codes. |
| 14 | `isVowelCode` | Total Boolean function. Sound: its two rules are guarded by a total predicate and its negation, hence disjoint and exhaustive. |
| 15 | `closestQualifies` | Partial documentary function. Sound on defined terms and correctly not marked `total`; it does not contribute to positive-claim closure. |
| 16 | `closestScan` | Partial function declaration. Its six equations below are deterministic and cover the complete scan domain used by the theorem. Correctly not marked `total` globally. |
| 17 | `closestVowel` | Total function on every finite `IntSeq`. Sound: starts at `len-2`; lengths at most two take the base case, and longer inputs recurse on a decreasing in-bounds index. |

## `foundation.k` rules

| Line | Rule | Decision |
|---|---|---|
| 24 | `isVowelBody => ...` | Sound macro equation; exact helper body from `solution.mpy`. |
| 68 | `getClosestLoopBody => ...` | Sound macro equation; exact inner-while and decrement body. |
| 94 | `getClosestBody => ...` | Sound macro equation; exact initialization, outer loop, and return body. |
| 103 | `getClosestProgram => ...` | Sound macro equation; exact two function bindings and bodies. |
| 114 | `closestCandidate(CS,I)` | Sound definitional equation; it introduces no oracle and preserves the actual indexed code. |
| 117 | `vowelPred(C)` | Sound exhaustive definition of case-sensitive ASCII vowels. |
| 128 | `isVowelCode(C) => true` | Sound on guard `vowelPred(C)`. |
| 131 | `isVowelCode(C) => false` | Sound on complementary guard `notBool vowelPred(C)`. |
| 135 | `closestQualifies(CS,I)` | Sound direct conjunction of current-vowel, left-nonvowel, and right-nonvowel tests when the three accesses are defined. |
| 140 | scan base `I <= 0` | Sound: internal indices are strictly positive, so no remaining candidate exists; preserve accumulator `R`. |
| 143 | scan with `F=true`, `I>0` | Sound: after the rightmost candidate has been stored, later (leftward) indices cannot replace it; decrease `I`. |
| 147 | qualifying scan branch | Sound: the three predicate guards are exactly the desired qualification test; store the singleton candidate, set found, and decrease `I`. |
| 158 | current code non-vowel | Sound complementary branch; preserve result/found and decrease `I`. |
| 163 | current vowel, left vowel | Sound non-qualifying branch; the right neighbor is immaterial and no result changes. |
| 169 | current vowel, left non-vowel, right vowel | Sound remaining non-qualifying branch. Together, lines 147/158/163/169 are disjoint and exhaustive for `F=false`. |
| 177 | `closestVowel` initialization | Sound: matches program initialization `i=len-2`, empty result, `found=false`. |
| 183 | guarded `#Ceil(intSeqAt(...))` | Sound derived definedness lemma. Witness proof is structural induction on `CS`; `0 <= I < isLen(CS)` guarantees a constructor at index `I`. It fixes no value. |
| 188 | guarded `#Ceil(closestScan(...))` | Sound derived definedness lemma. Induction on `I`: the guard puts all three accesses in bounds, the six cases are exhaustive, and recursive calls decrease `I`. It fixes no value. |

No pair of local equations has an overlapping guard with unequal right-hand
sides. Every recursive equation descends. The only `total` declarations are
the three globally covered functions above; there is no local opaque symbol,
`no-evaluators` symbol, fresh result, or unconstrained oracle.

## Operational bridges

| File:line | Rule | Classification and decision |
|---|---|---|
| `helper-verification.k:14` | Exact `_is_vowel` application to `true` | Operational bridge; sound. `CONNECTION-SPEC.helper-vowel` proves the identical complete configuration and guard under `foundation.k`, which does not import this bridge. Its `CONT:K` universally covers the bridge's K-cell ellipsis. Net scopes, heap, allocation counters, stack, return, exception, and exit state are unchanged. |
| `helper-verification.k:55` | Exact `_is_vowel` application to `false` | Operational bridge; sound for the complementary guard by `CONNECTION-SPEC.helper-consonant`, with the same exact context and state-footprint argument. |
| `verification.k:12` | Exact outer loop + return + `#endcall` to scan result | Operational bridge; sound. `LOOP-CONNECTION-SPEC.loop-invariant` proves the identical loop/body/suffix, bindings, guard, frame pop, local-scope deletion, environment restoration, and all preserved cells. That theorem imports the already-justified helper bridges but does not import this loop bridge. |

The priority-40 attributes merely make the justified exact-context bridges
preempt generic fixed-semantics rules. The helper guards are complementary. The
loop bridge has an exact suffix and does not accept an arbitrary continuation.
Fresh reruns of the helper-body, loop-body, and changed-continuation probes
produced the expected reachable wrong values and stuck against their false
destinations.

## Positive claims

| File:line | Claim | Decision |
|---|---|---|
| `connection-spec.k:6` | `helper-vowel` | Sound bridge-free universal connection theorem for the true predicate domain and arbitrary `CONT:K`. |
| `connection-spec.k:47` | `helper-consonant` | Sound bridge-free universal connection theorem for the complementary predicate domain and arbitrary `CONT:K`. |
| `loop-connection-spec.k:6` | `loop-invariant` | Sound universal execution theorem for the exact loop/return/call-frame context; its circularity is the decreasing-index scan invariant. |
| `spec.k:6` | `entry` | Sound, result-constraining entry theorem for every finite `CS:IntSeq`; the right-hand result is `str(closestVowel(CS))`, not an existential or free result. |

All four claims were selected and rerun independently from fresh definitions;
each exited 0 and printed `#Top`.
