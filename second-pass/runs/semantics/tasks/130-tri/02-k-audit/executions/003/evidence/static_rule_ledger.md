# Static declaration and rule ledger

This ledger accompanies `k_declaration_rule_inventory.txt`, which contains every
matched declaration, attribute, context, rule, configuration, and claim with its
source line. `k_inventory_summary.tsv` gives per-file counts. The supplied tree
contains 695 rules; `verification.k` adds 16 rules and `spec.k` adds two claims.

## Supplied-semantics inventory decisions

The candidate copy is byte/type identical to the trusted supplied tree. The
following decisions cover every declaration and rule in each file; unused
modules are still inventoried but do not contribute to either target proof.

| File | Rules | Audit decision |
|---|---:|---|
| `semantics.k` | 0 | Assembly only. `MPY` excludes concrete-only rules and is the proof import; `MPY-KRUN` additionally imports `MPY-CONCRETE`, as required for concrete execution. |
| `semantics/syntax.k` | 0 | The 16 syntax groups declare the translated constructors. Used constructors map exactly to `Module`, `FuncDef`, `Params`, `Int`, `Name`, `ListExpr`, `If`, `While`, `Assign`, `AugAssign`, `BinOp`, `Compare`/`CmpOp`, `Call`, `Attribute`, `Expr`, and `Return`. Strictness or explicit contexts provide the intended evaluation order. |
| `semantics/core.k` | 46 | Configuration, algebraic values, heap allocation, sequential statements, scope lookup, literal evaluation, argument evaluation, truthiness, and list helpers were reviewed. The used rules faithfully maintain env/scopes/heap/heapLoc/stack/ret/exc/exit-code. Remaining closure-cell and generic helpers are outside this program’s dependency. No task answer is encoded. |
| `semantics/iter.k` | 0 | Iterator declarations only; unused by the submitted while-loop. |
| `semantics/range.k` | 6 | Unused: the candidate uses `while`, not canonical’s `for range`. No target claim depends on these rules. |
| `semantics/operators.k` | 10 | Used generic unary/binary/compare dispatch and compare evaluation contexts are faithful. Heap-object dereference cases are either unused or preserve the stored value. |
| `semantics/int.k` | 16 | Used `+`, `%`, `//`, `==`, and `<=` cases. `pyMod` and floor-division agree with Python on the proof domain; divisor is the concrete positive integer 2. Other disjoint integer cases are unused. |
| `semantics/bool.k` | 13 | The program does not use `BoolOp`; the rules are disjoint short-circuit cases. Boolean equality cases are not needed for the target. |
| `semantics/float.k` | 121 | Entirely outside the proof dependency because the candidate uses integer `//`. Its opaque float primitives are a supplied trust boundary, not imported proof-local answers. The trusted canonical uses `/` and therefore returns floats after index 1; this representation difference is recorded separately. |
| `semantics/str.k` | 28 | Unused by the program. Compiler warnings concern unused pattern variables in `strLt`, not target semantics. |
| `semantics/set.k` | 12 | Unused and sort-disjoint. |
| `semantics/list.k` | 27 | Used list-literal allocation, `valSeqConcat`, and the priority-40 in-place `append` rule. The append rule reads/writes only heap location `H`, preserves the ref and all other cells, returns `noneV`, and matches Python’s mutator behavior. Equality, iteration, and membership rules are unused by the proof. |
| `semantics/tuple.k` | 21 | Unused and constructor-disjoint. |
| `semantics/subscript.k` | 40 | Unused: the rewritten candidate tracks the previous values in scalar locals rather than indexing the list. |
| `semantics/comprehension.k` | 7 | Unused macro rules. |
| `semantics/methods.k` | 75 | Pure-method functions are unused. The submitted `append` is handled by the exact list mutator rule, not `applyMethod`. |
| `semantics/controls.k` | 34 | Used assignment, augmented assignment, expression-discard, if, while, and loop-label rules are faithful. `While` evaluates the guard each iteration; true executes the body before re-entering and false terminates. Assignment changes only the current scope; `i += 1` uses fixed integer addition. Imports, for, break/continue, cell writes, and ref truthiness are unused. |
| `semantics/functions.k` | 15 | Used parameter binding, return, `#endcall`, and `#pop` preserve the return value, restore caller control/env, remove only the callee scope, and preserve escaping heap lists. Annotated-closure rules are unused. |
| `semantics/builtins.k` | 137 | Builtin operations are unused in the target proof. In particular no opaque `md5hexCodes`, eval, sorting, or fold result influences the claim. |
| `semantics/call.k` | 21 | Used generic call routing and the `closureVal` application rule evaluate the callee/argument, allocate a fresh scope, bind `n`, push the exact continuation, execute the supplied body, and return through the fixed frame rules. Builtin/type/method routes other than append are unused. |
| `semantics/sort.k` | 19 | Opaque `sortVS`/`sortKeyVS` and their concrete legs are unused and have no target dependents. |
| `semantics/assert.k` | 3 | Used only by the independent LLVM smoke artifact; successful assertions leave the state normal, false ones set `AssertionError` and exit 1. It is not imported as a proof shortcut. |
| `semantics/dict.k` | 28 | Unused and constructor-disjoint. |
| `semantics/concrete.k` | 16 | Imported only by the fresh LLVM runtime definition. Deep equality and keyed sort are unused by the candidate assertions except ordinary flat-list equality, which stays in `list.k`. |

No supplied rule on the used slice fabricates a result, suppresses a material
effect, changes binding, or leaves a used construct unmodeled.

## `verification.k`: every local declaration and rule

| Lines | Extension | Class and decision |
|---|---|---|
| 9–10 | `triAt(Int)` as `[function,total,symbol,no-evaluators]` | Result-bearing definitional summary. It is opaque except for the following equations. All uses have nonnegative indices; its unconstrained negative domain is not reached. |
| 12 | `triAt(0) => 1` | True base equation. |
| 13 | `triAt(1) => 3` | True base equation. |
| 15–18 | even equation using `pyMod` | True for `I >= 2` and even `I`; it states `triAt(I) = 1 + I/2`. |
| 22–25 | canonicalized even equation | Same value and guard as the preceding equation; overlaps agree. |
| 27–31 | odd recurrence equation using `pyMod` | True for odd `I >= 3`; the last arithmetic term is `triAt(I+1) = 1 + (I+1)/2`. |
| 34–40 | backend-normalized odd equation | Same recurrence after unfolding `pyMod`; overlaps agree. |
| 44 | `triPrefix(Int)` constructor | Dead scaffolding. The dependency reconstruction deletes this declaration and every related rule while both target proofs still close. |
| 45–46 | `prefixIndex(ValSeq)` as `[function,total,symbol,no-evaluators]` | Result-bearing inductive summary. Its equations certify the two bases and one correct append. Its values on all other sequences are underdefined; therefore the postcondition is not an injective/equivalent characterization of the returned list. This is the principal validation limitation. |
| 48 | `[1] => triPrefix(0)` | Dead scaffolding; deleted in the successful minimal reconstruction. A direct exact-state probe showed it did not rewrite the returned heap. |
| 49 | `[1,3] => triPrefix(1)` | Dead scaffolding; same dependency result. |
| 50 | `prefixIndex([1]) => 0` | True base certificate and used for the `N=0` path. |
| 51 | `prefixIndex([1,3]) => 1` | True base certificate and used to establish the loop invariant. |
| 52 | `prefixIndex(triPrefix(J)) => J` | Dead with `triPrefix`; deleted in the successful minimal reconstruction. |
| 53–58 | append-certificate equation | True sufficient rule: appending `triAt(I)` to a sequence certified through `I-1` certifies index `I`. It does not replace the list append or any program execution. |
| 59–62 | synthetic `valSeqConcat(triPrefix(...),...)` equation | Dead scaffolding; deleted in the successful minimal reconstruction. |
| 66–68 | `TriLoopCond` macro | Exact syntax macro; expanded term matches the submitted loop condition. |
| 70–86 | `TriLoopBody` macro | Exact syntax macro; no operational shortcut. The executed-body mutation changed this expansion and caused the loop proof to fail. |
| 88–100 | `TriFunctionBody` macro | Exact syntax macro. `kast --expand-macros` JSON is byte-identical to the body mechanically extracted from trusted regeneration. |

There are no local priority rules, external primitives, call interceptions, or
rules that skip program-defined control flow.

## `spec.k`: both claims

| Lines | Claim | Decision |
|---|---|---|
| 8–55 | Loop circularity | Satisfiable (for example `I=2`, `R=1`, `n=2`, `VS=[1,3]`, `a=1`, `b=value=3`, `i=2`). It executes the exact real guard/body and constrains final `i` to `I+R` and the summary index to `I+R-1`. Final scalar locals are intentionally framed existentially and do not affect the return contract. |
| 62–83 | Entry claim | Full input domain `N >= 0`; exact closure parameter/body/scope, exact empty initial heap, and returned ref/heap allocation. It constrains the actual returned sequence through `prefixIndex(result)=N`, not by structural equality to the recurrence sequence. Dynamic, concrete-K, body-sensitivity, and false-postcondition evidence show this is discriminating, but the missing converse/structural characterization leaves an informal summary-to-contract bridge. |

## Overlap, coverage, and trust conclusions

- `triAt` guards cover every index reached by the program: bases 0/1, even
  indices at least 2, and odd indices at least 3. Duplicate normalized rules
  agree on overlaps.
- `prefixIndex` intentionally does not cover arbitrary sequences. `[total]`
  keeps unmatched applications defined but opaque. No target proof treats an
  unmatched value as a numeral; nevertheless, the equality in the final claim
  is only a sufficient inductive certificate, not an equivalence theorem.
- The proof executes all material operations under supplied semantics. Removing
  all `triPrefix` rules does not change closure, so none is an operational
  bridge contributing to the proof.
- Opaque primitives in unused supplied modules have no dependents. The only
  result-bearing opaque symbols in the target are `triAt` and `prefixIndex`,
  whose contributing equations are above.
