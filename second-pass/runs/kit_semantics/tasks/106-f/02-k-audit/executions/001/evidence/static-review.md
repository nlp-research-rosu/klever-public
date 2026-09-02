# Static rule review

This is the reviewer-authored decision record paired with
`rule-inventory.txt`. The inventory contains the complete source text and line
span of all 1,108 top-level entries in the supplied semantics and
`verification.k`: 230 syntax declarations, one configuration, five contexts,
709 rules, and all module/import/require declarations. The 709 rules comprise
695 supplied-semantics rules and 14 proof-local rules.

The supplied tree was first proved byte-identical to
`/reference/reference-semantics`; it is the fixed semantics selected by the
benchmark, not a candidate-generated language definition. Every inventory
entry is assigned to one row below. “Outside path” means that no term with that
declaration or rule can be produced by the submitted program or either proof
claim. It is therefore not a result-bearing assumption of this theorem. This
classification does not assert that the deliberately partial MPY model is a
complete model of all Python.

## Supplied semantics, exhaustive file-level decisions

| File | Syntax / rules | Decision for all entries in the file |
|---|---:|---|
| `semantics.k` | 0 / 0 | Assembly only. The proof imports `MPY`; concrete tests import `MPY-KRUN`, which additionally imports `MPY-CONCRETE`. Import closure is consistent. |
| `syntax.k` | 16 / 0 | Declarations and strictness annotations are well-sorted. Used constructors map exactly to regenerated `solution.mpy`: `Module`, `FuncDef`, `Params`, `Assign`, `Name`, `ListExpr`, `Int`, `While`, `Compare`, `CmpOp`, `AugAssign`, `BinOp`, `If`, `Expr`, `Call`, `Attribute`, and `Return`. `Assign`/`AugAssign` evaluate RHS first; `If` evaluates its guard; binary operands are left-to-right; `Call` uses explicit routing in `call.k`. Other syntax is outside path. |
| `core.k` | 37 / 46 | Configuration, scope chain, statement sequencing, lookup, literals, argument evaluation, allocation, list helpers, and `builtinsScope` agree with the used execution. Allocation reads/writes heap and `heapLoc`; lookup reads `env`/`scopes`; no used rule fabricates a value. Closure-cell and keyword rules are outside path. All used helper recursions descend structurally. |
| `iter.k` | 1 / 0 | Protocol declarations only; outside path because the submitted program uses `while`, not iteration. |
| `range.k` | 2 / 6 | Outside path. The guarded range helpers/iterator rules are the ordinary nonzero-step definitions. Zero-step exception behavior is intentionally absent from this partial semantics and cannot affect this theorem. |
| `operators.k` | 0 / 10 | Used routing is exact: comparison evaluates both operands then calls `applyCmp`; `BinOp("%",i,2)` calls `applyBin`; heap dereference rules are outside the used integer-only expressions. Priority-40 rules only preempt generic dispatch for heap references. |
| `int.k` | 1 / 16 | Used `+`, `*`, `%`, `==`, and `<=` rules are ordinary unbounded-integer operations. On the proof path `pyMod(I,2)` has a positive nonzero divisor, so its floor-mod equation matches Python. Unused division/exponent cases do not affect the result. |
| `bool.k` | 0 / 13 | Outside path except Boolean values produced by comparisons/truthiness. Short-circuit rules are standard and do not contribute a proof-local conclusion. |
| `float.k` | 34 / 121 | Entirely outside path. Its 19 `no-evaluators` float operations and concrete twins are fixed, explicit trust boundaries for other tasks only. Duplicate mixed Int/Float rules have identical right sides on overlaps. Compiler-noted partial total functions (`floorFI`, `toF`, `ceilF`) are an unused fixed-semantics limitation, not a value source in this proof. |
| `str.k` | 5 / 28 | Outside path. ASCII-only literals and lexicographic helpers state the documented partial string model. |
| `set.k` | 6 / 12 | Outside path. Structural folds descend over `IntSeq`; guards are disjoint. |
| `list.k` | 5 / 27 | Material. `ListExpr` evaluates elements then allocates one heap list; `append` mutates exactly that heap location and returns `noneV`; `valSeqConcat` appends structurally. Iteration, membership, equality, and deep-equality rules are outside path. Priority 40 on `append` is narrower than generic bound-method dispatch and preserves the active continuation and every non-heap cell. |
| `tuple.k` | 4 / 21 | Outside path. No tuple value or unpacking is produced by this program. |
| `subscript.k` | 15 / 40 | Outside path. The compiler warning that total `valSeqAt` has intentionally abstract out-of-bounds/opaque cases is a fixed, unused limitation. |
| `comprehension.k` | 3 / 7 | Outside path. Macro expansions introduce no theorem-specific result. |
| `methods.k` | 27 / 75 | Only method dispatch to list `append` is relevant, and its operational rule is in `list.k`. All string/list-count methods and their structural helper equations are outside path. The compiler-noted partial `joinCodes` totality is unused. |
| `controls.k` | 3 / 34 | Material rules match real control flow. Four initial assignments update the current local scope; three `AugAssign` operations read the bound integer and write `applyBin`; `If` branches on integer comparison truth; `While` reevaluates the exact guard and preserves its continuation via `#loopLbl`; `Expr` discards only the method’s `noneV`. For/break/continue/import/deref rules are outside path. Priority-40 cell/ref cases are disjoint from this plain integer/list-reference local frame. |
| `functions.k` | 4 / 15 | Material rules load the exact function closure, bind its single parameter, set `retV` on `Return`, restore caller environment/continuation, remove only the callee scope, and restore `scopeLoc`. The heap and `heapLoc` are deliberately not rewound, permitting the returned list reference. Annotated closures/cells are outside path. |
| `builtins.k` | 38 / 137 | Outside path. The function binding exists in `builtinsScope`, but the submitted body invokes no builtin. Opaque `md5hexCodes` and compiler-noted partial `mapStrVS` cannot influence any branch, cell, or result here. |
| `call.k` | 3 / 21 | Material route evaluates `Name("f")`, then the argument, then dispatches the exact `closureVal`. It allocates a fresh local scope, pushes the complete caller continuation/environment, runs the exact body, and leaves observable heap allocation to body rules. Bound-method routing evaluates `result.append`’s argument before the narrow append rule. Builtin/type/annotated-closure routes are outside path. |
| `sort.k` | 6 / 19 | Entirely outside path. `sortVS`/`sortKeyVS` are explicit fixed opaque boundaries for other tasks and are absent from the claim term, execution term, summaries, and postcondition. |
| `assert.k` | 0 / 3 | Outside path. |
| `dict.k` | 12 / 28 | Outside path. No dict term is produced. |
| `concrete.k` | 5 / 16 | Not imported by the Haskell proof definition. It is used only by the fresh LLVM definition; none of its deep-equality or keyed-sort redexes occurs in the smoke programs. |

No supplied opaque/total symbol outside ordinary K integer/map/list primitives
occurs in `solution.mpy`, either claim, or the three proof-local summaries.
There is therefore no opposite interpretation of an unused opaque symbol that
can change the intended-domain result.

## Material constructor-to-rule map

| Program construct | Declaration/rules |
|---|---|
| module/function binding | `syntax.k:53,57,61`; `core.k:124-127`; `functions.k:14-16` |
| function lookup/call/return | `core.k:130-154,183-191`; `call.k:18-21,69-74`; `functions.k:63-66,77-90` |
| local assignments and literals | `syntax.k:9,41,44`; `core.k:194`; `controls.k:9-31` |
| fresh empty result list | `list.k:13-15`; `core.k:117-121,217-225` |
| while and if control | `controls.k:50-54,65-82,85`; `core.k:199-205` |
| integer arithmetic/comparison | `operators.k:10-17`; `int.k:9-16,19-27` |
| bound `append` call | `call.k:15-24,52-67`; `list.k:18-20,52-55`; `controls.k:46-48` |

## Proof-local inventory: all 14 rules

`verification.k` adds only three pure functions and fourteen equations. It
contains no `<k>`-cell rule, priority rule, opaque symbol, fresh variable,
state update, call interception, return, or control rewrite.

| Lines | Rules | Classification and decision |
|---|---|---|
| 8-21 | `factRun`: guarded step/base concrete rules and their step/base simplifications | Definitional summary plus symmetric fold lemmas. `I <= N` and `I > N` are exhaustive/disjoint. The step is exactly the program’s `fact := fact*I; I := I+1`. The recursive measure `max(N-I+1,0)` descends. The fold is the defining equality in reverse under the identical guard. |
| 24-37 | `totalRun`: guarded step/base concrete rules and their step/base simplifications | Same decision. The step is exactly `total := total+I; I := I+1`; guards and descent are valid. |
| 42-88 | `resultRun`: even step, odd step, base, and three matching fold simplifications | Definitional summary. The cases `I>N`, `I<=N ∧ pyMod(I,2)=0`, and `I<=N ∧ pyMod(I,2)≠0` are exhaustive and pairwise disjoint. Both branches update both accumulators and `I`; the even branch appends `F*I`, the odd branch appends `T+I`, exactly matching the source. Each fold is the corresponding definition in reverse with the same guard. |

The seven `[simplification]` rules are the only proof-local simplifications.
All seven are true equalities over their full guards. The six `[concrete]`
recursive/base rules are defining equations, and the remaining concrete rule
is the `resultRun` base. The three `[function,total,no-evaluators]`
declarations are not oracles: exhaustive equations fix every use, and the
postcondition does not supply their values independently of execution.

## Static conclusion

Every material fixed-semantics rule executes an operation present in the
regenerated body and preserves the relevant continuation/cells. Every
proof-local equation follows from its definition and ordinary integer/list
mathematics. No rule encodes the HumanEval answer while bypassing execution,
and no false conclusion witness exists on the formal `N >= 0` domain.
