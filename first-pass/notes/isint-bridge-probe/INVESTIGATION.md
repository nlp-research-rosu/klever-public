# isInt-bridge probe — cracking symbolic same-list element arithmetic

## Question

On the unified semantics a list element is an opaque `Val` (`valSeqAt(NUMS, I)`), so
`nums[i] - nums[j]` / `nums[i] + nums[j]` does not reduce — the applyBin/applyCmp Int-cast
lemmas in `lemmas.k` require `isInt(V) andBool isInt(W)`, and `isInt(valSeqAt(NUMS,I))` is
**not** derivable from an `allInt(NUMS)` precondition (a symbolic `allInt(NUMS)` is opaque;
there is no rule linking it to `isInt` of an element). And `isInt(...) => true` cannot be a
`[simplification]` LHS — `isInt` is a hooked predicate, not a function/functional/mlOp symbol.

This is the **isInt wall** that blocks the element-based nested loops: Q43 pairs_sum_to_zero,
Q40 triples_sum_to_zero, Q20 find_closest_elements, Q87 get_row.

## Candidate fix — a guarded applyBin/applyCmp ECHO

`applyBin` / `applyCmp` ARE function symbols, so they CAN be `[simplification]` LHSs. Echo them
on two SAME-LIST operands, casting via `{}:>Int`, guarded by `allInt(NUMS)` (SOUND: `allInt`
means every element really is an `Int`, so the projection is faithful):

```k
rule applyBin(OP, valSeqAt(NUMS, I), valSeqAt(NUMS, J))
  => applyBin(OP, {valSeqAt(NUMS, I)}:>Int, {valSeqAt(NUMS, J)}:>Int)
  requires allInt(NUMS) [simplification]
// (same for applyCmp)
```

## Result — CONCLUSIVE (differential)

Claim: `applyBin("+", valSeqAt(NUMS,0), valSeqAt(NUMS,1)) => ?_:Int` under
`allInt(NUMS) andBool vsLen(NUMS) >=Int 2`.

| definition | result |
| --- | --- |
| `verif.k` (WITH echo) | `#Top` — the sum reduces to an Int (echo fires in the simplification phase, so "proven without rewriting") |
| `verif-noecho.k` (control) | **FAIL** — "configuration cannot be rewritten further"; the sum stays a stuck opaque `Val` |

The control failing proves the `?_:Int` target is NOT vacuous: the echo is exactly what
discharges the reduction. The echo both **compiles** (applyBin/applyCmp are valid LHSs) and
**fires** under the `allInt` guard.

## Status / next step

The ATOMIC wall is cracked. NOT yet done: integrate the echo into a full nested-loop
existential proof (Q43 is the cleanest: `exists i<j with l[i]+l[j]==0`). Open questions for that
proof — does the echo fire inside a loop-invariant's path condition (where `allInt(NUMS)` is a
stored precondition), and does the Bool existential fold compose? Do this DELIBERATELY (own
session), add the echo either problem-local (verification.k) or shared (guarded, inert when
`allInt` is false — then re-run the full regression). See the `nested-loop-rung-unified` memory.
