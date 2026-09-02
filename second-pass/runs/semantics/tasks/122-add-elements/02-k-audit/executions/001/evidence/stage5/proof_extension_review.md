# Proof-extension rule review

This inventory is independent of candidate prose. `verification.k` contains
three local function declarations and fourteen equations. There are no local
priority rules, no `<k>` operational rules, and no local `symbol(...)` or
`no-evaluators` declarations.

| Location | Extension/class | Complete domain and overlap check | Static decision |
|---|---|---|---|
| `verification.k:7` | `intsOnly(.ValSeq) => true`; definitional summary | Empty sequence case. Disjoint from line 8. | Sound. |
| `verification.k:8-9` | recursive `intsOnly`; definitional summary | Every `vCons`; recurses on the tail. Together with line 7 covers `ValSeq`. | Sound and terminating. |
| `verification.k:15` | `intValue(I:Int) => I`; refined-sort projection | All concrete `Int` values. No competing equation. | Sound on its equation domain. The `[total]` declaration is broader than the sole equation, so non-Int values remain unconstrained; all proof uses are guarded by `isInt`, and no false intended-domain conclusion witness was found. |
| `verification.k:16` | empty `qualifyingSumAcc`; definitional summary | Empty sequence; disjoint from the recursive cases. | Sound. |
| `verification.k:17-19` | include-head `qualifyingSumAcc`; definitional summary | `isInt(V)` and `abs(V) < 100`. Disjoint from line 20. Recurses on the tail. | Sound for the submitted `abs(element) < 100` computation. It does not encode the trusted canonical's `len(str(elem)) <= 2` behavior for negative two-digit integers. |
| `verification.k:20-22` | skip-head `qualifyingSumAcc`; definitional summary | `isInt(V)` and `abs(V) >= 100`. Exhaustive with line 17 on integer heads. Recurses on the tail. | Sound for the submitted computation. |
| `verification.k:27-30` | refined-sort `applyBuiltin("abs", ...)`; result-bearing derived lemma | Guard `isInt(V)`. On overlap with supplied `builtins.k:44`, `V=I:Int` and `intValue(I)=I`, so both sides are `absInt(I)`. | No false witness found; ground execution agrees. The candidate supplied no bridge-free universal connection claim for the symbolic sort refinement, which is a validation evidence gap. |
| `verification.k:31-34` | refined-sort `applyBin("+", ...)`; result-bearing derived lemma | Guard `isInt(V)`. On overlap with supplied `int.k:9`, `V=I:Int`, and both sides are `A +Int I`. | No false witness found; ground execution agrees. The candidate supplied no bridge-free universal connection claim. |
| `verification.k:39-40` | map-update membership lemma | Any map update at the queried key. | Sound: the update installs that key. |
| `verification.k:41-44` | distinct-key membership lemma | Guard `K1 =/=K K2`, disjoint from same-key case. | Sound: updating another key preserves membership of `K1`. |
| `verification.k:45-46` | map-update lookup lemma | Lookup of the just-updated key. | Sound: lookup returns the installed value. |
| `verification.k:47-49` | distinct-key lookup lemma | Guard `K1 =/=K K2`, disjoint from same-key case. | Sound: updating another key preserves the old lookup. |
| `verification.k:54-60` | prefix/suffix `slAdjust` acceleration; result-bearing derived lemma | `I=len(PREFIX)+1`, `LEN=len(PREFIX++SUFFIX)+1`, step `1`. Nonnegative lengths imply `0 <= I <= LEN`; supplied `slAdjust`/`clampHi` returns `I`. | Mathematically sound on the complete match domain. No bridge-free K connection theorem was supplied. |
| `verification.k:61-68` | prefix/suffix `buildVS` acceleration; result-bearing derived lemma | Sequence is `HEAD :: PREFIX ++ SUFFIX`, start `0`, stop `len(PREFIX)+1`, step `1`. Supplied recursion selects exactly `HEAD :: PREFIX`. | Mathematically sound by induction on `PREFIX`; no overlap disagreement or false witness found. No bridge-free K connection theorem was supplied. |

The eight simplification rules preserve values and do not introduce abrupt
control, change cells, allocate, or discard continuations. The body-sensitivity
mutation in `body_sensitivity_proof.log` changes both real comparison constants
from 100 to 99 while leaving the summary fixed; it builds and then fails on the
unmet summary obligation. This is evidence that the proof is sensitive to the
executed body.
