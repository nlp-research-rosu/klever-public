# Proof-local rule-by-rule review

This file supplies the per-entry decision for every local declaration, rule,
and claim in `verification.k` and `spec.k`. The fixed supplied-semantics entries
are individually source-positioned in `static-rule-inventory.md`; they are the
launcher-selected fixed baseline, exactly match the candidate copy, and are
accepted at that selected semantics level. `stage5-used-construct-map.md`
identifies every fixed rule family reachable from the submitted program.

## Local declarations

| Lines | Declaration | Decision |
|---|---|---|
| `verification.k:7` | `#helperBody` macro | Exact constructor body; accepted as syntax identity, but not as evidence that the body executes. |
| `verification.k:34` | `#mainBody` macro | Exact constructor body; same decision. |
| `verification.k:43` | `#helperClosure` macro | Exact parameters, body, and defining scope 0; accepted as constructor identity. |
| `verification.k:47` | `#mainClosure` macro | Exact parameters, body, and defining scope 0; accepted as constructor identity. |
| `verification.k:52` | total function `changeRange` | Complete over `L >= R` / `L < R`; mathematically descending and accepted for in-bounds integer-list uses. |
| `verification.k:64-65` | `TargetCall`, `#targetCall` | Fresh proof machine; rejected as a replacement for fixed execution unless connected by a bridge-free theorem. No such theorem exists. |
| `verification.k:88` | `#addMismatch` | Fresh arithmetic continuation; its sole rule is mathematically sound. |
| `verification.k:118` | total `targetAnswer` | Complete over the two `TargetCall` constructors; truthful only as a definition of the target machine, not a connection to program execution. |
| `verification.k:124` | total `targetValid` | Complete syntactically, but its admitted domain is too broad for the target machine's raw equality/index operations. |

There are no proof-local opaque symbols and no proof-local simplification
attributes. The only local priority rules are the two call bridges at priority
40.

## Sixteen local rules

| # | Lines | Rule/class | Decision and justification |
|---|---|---|---|
| 1 | `8-32` | `#helperBody` macro equation | Accepted constructor expansion; mechanically identical to the submitted helper body. |
| 2 | `35-41` | `#mainBody` macro equation | Accepted constructor expansion; mechanically identical to the submitted public body. |
| 3 | `44-45` | `#helperClosure` macro equation | Accepted constructor expansion only. |
| 4 | `48-49` | `#mainClosure` macro equation | Accepted constructor expansion only. |
| 5 | `53-54` | `changeRange` base equation | Accepted: an inclusive interval with `L >= R` has no unchecked mirrored pair. |
| 6 | `55-59` | `changeRange` recursive equation | Accepted on its used, in-bounds integer-list domain; the interval shrinks by two and adds exactly one raw-value mismatch. It is not itself an execution theorem. |
| 7 | `73-78` | priority operational bridge for the public closure | Rejected. It preempts `call.k:69-74`, skips name lookup already encoded in the body, parameter binding, `len`, helper lookup/call, frames, return/pop, control, and all body evaluation. No bridge-free universal connection claim exists. The body mutation proves that changing the actual matched closure to `return 999` still lets this rule prove result 0 for `[]`. |
| 8 | `79-86` | priority operational bridge for the helper closure | Rejected for the same missing connection. It accepts every integer `L,R` and arbitrary continuation/cell context. For `[5], L=-1, R=0`, fixed `Subscript` normalizes `-1` and returns 0, while the target machine uses raw `valSeqAt(VS,-1)`; `stage5-negative-index-fixed.log`, the residual in `stage5-negative-index-bridge-proof.log`, and the permitted-model proof in `stage5-negative-model-proof.log` give the concrete/symbolic witness. |
| 9 | `90-99` | target main-to-helper rewrite | As a target-machine definition it computes `(0,len-1)`. Rejected as program semantics because it hand-substitutes `len` and the helper binding without executing or proving them. |
| 10 | `101-102` | target helper base rewrite | Mathematically sound for the target machine and matches the source base branch. |
| 11 | `104-113` | target helper recursive rewrite | Rejected globally. It substitutes `valSeqAt` and raw `==K` for fixed `Subscript` plus `Compare`. It omits negative-index normalization and heap-object structural equality. The formal main domain admits `[[5],[5]]`: fixed Python and fixed K return 0, while the unmodified candidate proves 1 (`stage5-nested-list-fixed.log`, `stage5-nested-list-bridge-proof.log`). |
| 12 | `115-116` | `#addMismatch` equation | Accepted arithmetic equation: add one iff the Boolean is true. |
| 13 | `119-120` | `targetAnswer(mainCall,...)` | Accepted as a definition of the hand-written summary, not as evidence about source execution. |
| 14 | `121-122` | `targetAnswer(helperCall,...)` | Same decision. |
| 15 | `125` | `targetValid(mainCall,...) => true` | Rejected as a validity characterization. It admits every `ValSeq`, including the nested-list false-conclusion witness. |
| 16 | `126-128` | helper `targetValid` bounds | Bounds are sufficient to keep recursive positive-index reads in range, but the unrestricted `ValSeq` still admits raw-ref equality discrepancies; rejected as a complete validity characterization. |

## Three claims

| Lines | Claim | Decision |
|---|---|---|
| `spec.k:6-11` | `public-entry-bridge` | Closes only because local rule 7 states the same bridge. It is not a bridge-free connection theorem and does not validate the skipped body/control/state. |
| `spec.k:13-21` | `helper-entry-bridge` | Same circularity. Its unrestricted `L,R` domain includes the negative-index inequivalence. |
| `spec.k:23-40` | `smallest-change-correct` | A valid induction over the invented `#targetCall` machine, but its `<k>` cell never contains either submitted closure or body. It is false as a theorem about fixed execution on its own formal `mainCall` precondition (`[[5],[5]]` witness), and it is not connected to the intended integer-list program by a bridge-free proof. |

## Configuration/control assessment

The fixed closure call reads/writes `<env>`, `<scopes>`, `<scopeLoc>`,
`<stack>`, and `<ret>` (`call.k:69-74`, `functions.k:78-90`). Both priority
bridges match only `<k>` with an arbitrary suffix and frame every other cell.
They therefore accept more control states than the fixed call rule and provide
no theorem over the complete matched context. For ordinary valid calls the
fixed frame is eventually restored, but that finite observation neither proves
universal context containment nor repairs the result discrepancies above.
