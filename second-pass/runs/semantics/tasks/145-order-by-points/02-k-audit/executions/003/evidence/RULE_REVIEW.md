# Rule-by-rule review ledger

This ledger assigns a review disposition to every item enumerated in
`RULE_INVENTORY.md`. “Off path” means the submitted `solution.mpy` cannot reach
the item for the HumanEval input type (a list of integers); it is not being used
to excuse a false rule on the proof path.

| File | Inventoried rules | Disposition |
|---|---:|---|
| `semantics.k` | 0 | Assembly only. `MPY` excludes `MPY-CONCRETE`; `MPY-KRUN` includes it. This distinction is material and was respected in both clean builds. |
| `semantics/syntax.k` | 0 | The 16 syntax declarations cover every constructor used by `solution.mpy`: `Module`, `FuncDef`, `Params`, `Assign`, `Compare`/`CmpOp`, `Call`, `Name`, `Int`, `While`, `BinOp`, `AugAssign`, `If`, `Return`, and `KwArg`. Strictness gives the used left-to-right operand evaluation. |
| `semantics/core.k` | 46 | Configuration, allocation, module loading, sequencing, name lookup, builtin scope, argument evaluation, literals, truthiness, and sequence helpers were checked. Used rules preserve all named cells. Recursive helpers descend structurally. Cell/closure-only and list-index helpers are off path. No false conclusion witness was found on list-of-integers inputs. |
| `semantics/iter.k` | 0 | Declarations only; off the submitted symbolic path. |
| `semantics/range.k` | 6 | Off path. Equations are the expected signed-step range fold for nonzero steps. |
| `semantics/operators.k` | 10 | Used `Compare`, `BinOp`, and unary dispatch evaluate operands and route to typed operations. Heap dereference cases are off the digit-key path except the list argument is dereferenced in call dispatch. |
| `semantics/int.k` | 16 | Used `<`, `%`, `+`, `-`, `*`, and `//` equations agree with unbounded Python integer arithmetic for divisor 10. `pyMod` plus `(n-pyMod)/10` implements floor semantics. The program never divides by zero. |
| `semantics/bool.k` | 13 | Used only through the boolean result of `n < 0` and truthiness; equations are standard. `BoolOp` rules are off path. |
| `semantics/float.k` | 121 | Entirely off path. Its numerous declared opaque float primitives are trust boundaries for other tasks and do not influence any claim here. |
| `semantics/str.k` | 28 | Entirely off path. The program performs arithmetic digit extraction, not string conversion. |
| `semantics/set.k` | 12 | Entirely off path. |
| `semantics/list.k` | 27 | List value/iteration declarations are available, but the target path passes a bare `list(VS)` to `sorted`; list literal, concatenation, equality, membership, and mutation rules are off path. |
| `semantics/tuple.k` | 21 | Entirely off path. |
| `semantics/subscript.k` | 40 | Entirely off path. The total-but-underspecified out-of-bounds `valSeqAt` boundary is not used. |
| `semantics/comprehension.k` | 7 | Entirely off path. |
| `semantics/methods.k` | 75 | Entirely off path. |
| `semantics/controls.k` | 34 | Used assignment, augmented assignment, `If`, and `While` rules have disjoint truth guards, update the current frame, and preserve continuation/cells. Imports, expression statements, `For`, loop-control, and heap-object condition rules are off path. |
| `semantics/functions.k` | 15 | Used `FuncDef`, parameter binding, closure call/frame push, `Return`, and frame pop rules preserve binding and caller continuation. Annotated closure-cell rules are off path. |
| `semantics/builtins.k` | 137 | The only used equation is `applyBuiltin("abs", I, .Vals) => absInt(I)` (plus call routing in `call.k`), which is correct for all K integers. Other builtin folds and the opaque `md5hexCodes` symbol are off path. |
| `semantics/call.k` | 21 | Used rules evaluate callee then arguments left-to-right, dereference the input list for the builtin, bind the exact selected closures, push/pop a frame, and route the builtin call. The keyed-sort dispatch is supplied by `sort.k`. |
| `semantics/sort.k` | 19 | **Gate A failure on rules 61–62 and declaration 49.** The used keyed-sort call rewrites directly to `#alloc(list(sortKeyVS(VS, KV)))`; `sortKeyVS` has no proof-side equations and does not execute the program-defined key closure. Rules for unkeyed/reversed/mutating sort are off path. |
| `semantics/assert.k` | 3 | Used only by the independent LLVM smoke harness, not by target proofs. The rules correctly turn false assertions into `AssertionError`/exit 1. |
| `semantics/dict.k` | 28 | Entirely off path. |
| `semantics/concrete.k` | 16 | Present only in the LLVM definition, never in the proof definition. The used concrete keyed-sort rules call the actual key closure for each element and stable-insert after equal keys. They support testing but cannot justify the proof-side opaque bridge universally. |
| `verification.k` | 9 | All seven nullary function equations and two entry rewrites were inspected. The body/module equations are exact constructor definitions, not shortcuts; the two entry rules load and call the exact module. There are no proof-local lemmas, simplification rules, priority rules, or operational result bridges. Constructor identity was checked mechanically. |

## Material construct-to-rule map

| Submitted constructor/operation | Declaration and operational rules |
|---|---|
| `Module`, statement sequence | `syntax.k:53,56,61`; `core.k:124-127`; `functions.k:14-16` |
| `FuncDef`, closure lookup/call/return | `functions.k:14-16,63-90`; `core.k:130-181`; `call.k:19-21,31,38-50,69-75` |
| `Assign`, `AugAssign` | `syntax.k:41,44`; `controls.k:9-31` |
| integer literal, `<`, `%`, `+`, `-`, `*`, `//` | `core.k:193-196`; `operators.k:10-17`; `int.k:7-27` |
| `abs(n)` | `core.k:156-181`; `call.k:19-21,31`; `builtins.k:43-44` |
| `While`, `If`, truthiness | `syntax.k:46,49`; `core.k:198-205`; `controls.k:50-60,76-82` |
| `sorted(nums, key=digit_sum)` | `core.k:94-102,183-191`; `call.k:19-21,31,38-46`; `sort.k:44-64` |
| concrete keyed sorting used only by `krun` | `concrete.k:20-59` |

## Opaque and total symbols

The complete declaration list is in `RULE_INVENTORY.md`. Opaque symbols occur
in `float.k`, `builtins.k` (`md5hexCodes`), and `sort.k` (`sortVS`,
`sortKeyVS`). Only `sortKeyVS` can affect the target result. No
`[simplification]` or `[functional]` declarations were found. `[total]` on
`sortKeyVS` establishes definedness only; it supplies no ordering, stability,
permutation, binding, or key-call equation.

## Concrete false-conclusion witness

For satisfying input `[1, 11]`, the key results are `1` and `2`, so ascending
stable order is `[1, 11]`. The proof theory has no equation constraining
`sortKeyVS`. In the reviewer experiment, adding the admissible opposite
interpretation

```k
rule sortKeyVS(VS:ValSeq, _:Val) => revVS(VS)
```

made a claim returning `[11, 1]` close with `#Top`. The clean build and proof
log is `stage5_opposite_interpretation.log`. This demonstrates the exact
unconstrained-value failure; it is not merely missing test coverage.

The body-sensitivity experiment changed the actual compiled `digit_sum` return
to `Int(999)` (confirmed in `stage5_body_term_check.log`). The unrestricted
order claim still closed because the same changed closure term appears inside
the opaque postcondition; see `stage5_body_sensitivity.log`. Thus the claim is
syntactically body-sensitive, but there is no semantic connection theorem for
what that body computes.
