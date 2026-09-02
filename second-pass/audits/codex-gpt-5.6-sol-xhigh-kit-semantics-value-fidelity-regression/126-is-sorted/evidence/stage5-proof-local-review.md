# Hand audit of every proof-local K item

This review covers K-0929 through K-0946 in
`stage5-rule-inventory.md`. There are no proof-local `functional`,
`simplification`, `priority`, `concrete`, `symbol`, or `no-evaluators`
attributes. No proof-local item is classified as unsound, so there is no
unsound-rule false-conclusion witness to report.

| Inventory item | Static decision | Basis and scope |
|---|---|---|
| K-0929 `isSortedLoopBody` syntax | Sound | A ground `[macro]` constructor. It adds no value, state, control, or oracle. |
| K-0930 `isSortedFunctionBody` syntax | Sound | A ground `[macro]` constructor. It adds no runtime behavior. |
| K-0931 four `Bool` function declarations | Sound declarations | `nonNegativeInts`, `scanCounts`, `nextCountResult`, and `intendedSorted` are proof summaries, not operational bridges. Their equations below are exhaustive on their declared domains. |
| K-0932 `countArgument` declaration | Sound declaration | Total on `Val × ValSeq`: K-0940 covers exactly `ref(0)` and K-0941 is the `owise` complement. It is used only by the connected loop summary. |
| K-0933 loop-body macro equation | Sound | Literal constructor-for-constructor expansion of the submitted loop body: call `lst.count(current)`, compare `> 2`, and assign `result = false` only on the true branch. It is not a `<k>` rewrite. |
| K-0934 function-body macro equation | Sound | Literal expansion of all four submitted statements, in order: sorted equality assignment, `current = 0`, the real `For`, and `Return(result)`. It is not a call shortcut. |
| K-0935 `nonNegativeInts(.ValSeq)` | Sound | Empty sequence satisfies the domain. |
| K-0936 integer-head domain equation | Sound | Requires the head to have K sort `Int`, checks `I >= 0`, and structurally descends on `REST`. |
| K-0937 non-integer-head domain equation | Sound | Guarded by `notBool isInt(V)` and therefore disjoint from K-0936; it completes the cons case and rejects Bool, ref, list, string, float, and other non-Int values. |
| K-0938 `COUNT > 2` update | Sound | Exactly the source true branch; returns `false` regardless of the old result. |
| K-0939 `COUNT <= 2` update | Sound | Exactly the source no-assignment path. The two integer guards are disjoint and exhaustive. |
| K-0940 `countArgument(ref(0), INPUT)` | Sound in its complete use context | The loop claim pins heap slot 0 to `list(sortVS(INPUT))`. The supplied non-mutating-method argument rule dereferences `ref(0)` to precisely that value. This helper does not rewrite `<k>` and is not asserted as a global heap theorem. |
| K-0941 `countArgument` `owise` equation | Sound | Identity on every value other than `ref(0)`. On the entry theorem’s integer domain this is the only reachable case. Together with K-0940 it is total and non-overlapping. |
| K-0942 empty `scanCounts` | Sound | No loop iterations remain, so the current Boolean is returned. |
| K-0943 cons `scanCounts` | Sound | One structural step counts the current item in the unchanged full `INPUT`, applies exactly the source threshold update, and recurses on the strict tail `REST`. Termination of the mathematical helper follows from the tail descent. |
| K-0944 `intendedSorted` | Sound definition | Names the exact initial result (`VALUES ==K sortVS(VALUES)`) followed by the exact loop scan. It neither executes nor replaces program code. Its bridge to the English word “sorted” remains conditional on the supplied opaque `sortVS` contract. |
| K-0945 loop reachability claim | Sound derived circularity | The fresh focused proof closed. Its complete match fixes the real `#loop`, exact trailing `Return ~> #endcall ~> .K`, environment, module/local bindings, scope locations, heap value, heap location, exact caller frame, return cell, exception cell, and exit code. There is no arbitrary continuation or omitted configuration cell. The claim remains true for any `REST`, because it summarizes counting those remaining elements against fixed `INPUT`. |
| K-0946 entry reachability claim | Sound and result-constraining | It loads the exact K AST, resolves the real module closure, calls it on `list(INPUT)`, and executes all fixed semantics. The precondition is exactly a finite sequence of nonnegative K integers. The destination fixes the returned Boolean to `intendedSorted(INPUT)` and fixes all observable cells, including the one allocation performed by `sorted`. The full fresh proof closed, the false-result mutation failed at `true ≠ false`, and the changed-body probe failed at `false ≠ true`. |

## Coverage, overlap, and descent conclusions

- Every proof-local total function has complete guarded coverage.
- The only guarded overlaps are deliberately disjoint:
  integer versus `not isInt`, `COUNT > 2` versus `COUNT <= 2`, and exact
  `ref(0)` versus `owise`.
- Both recursive functions descend on a strict sequence tail.
- No proof-local opaque or fresh result-bearing symbol exists.
- No proof-local equation has an operational `<k>` left-hand side; therefore
  there is no operational bridge whose continuation or state footprint could
  exceed a connection theorem.
- `scanCounts` is program-derived, but K-0945 is the universal fixed-semantics
  connection over its complete matched loop configuration. It is not justified
  merely by sharing a symbol with the postcondition.
