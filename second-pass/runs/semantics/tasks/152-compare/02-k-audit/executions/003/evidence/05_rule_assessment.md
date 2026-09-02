# Rule-by-rule assessment ledger

The line-addressed inventory is `05_inventory.log`. Each declaration/rule in
that inventory is assigned one of the decisions below. The candidate's
`reference-semantics/` is byte-identical to the trusted supplied tree, so
`BASELINE-ACCEPTED` means the rule is part of the selected fixed semantics and
its guards, overlaps, recursion, and state footprint are consistent with its
stated subset. `INERT-FOR-TARGET` means it also cannot match any term on the
submitted program's target path. `REJECTED-UNSOUND` is a candidate proof
extension that has a demonstrated false conclusion.

## Supplied semantics

| File | Decision for every inventoried declaration/rule | Target-path assessment |
|---|---|---|
| `semantics.k` | BASELINE-ACCEPTED | Assembly only. The proof imports `MPY`; concrete execution imports `MPY-KRUN` and its additional `MPY-CONCRETE`. |
| `semantics/syntax.k` | BASELINE-ACCEPTED | Declares every constructor in `solution.mpy`. Relevant strictness is left-to-right for subtraction, assignment RHS, `for` iterable, return, expression statements, and bound attributes. |
| `semantics/core.k` | BASELINE-ACCEPTED | Relevant rules correctly load the module, sequence statements, allocate monotonically, perform lexical lookup through the builtins scope, evaluate argument lists left-to-right, and define integer lists/length/concatenation helpers. Closure-cell, keyword, truthiness, and subscript-write rules are INERT-FOR-TARGET. |
| `semantics/iter.k` | BASELINE-ACCEPTED | Iterator protocol declarations only. |
| `semantics/range.k` | BASELINE-ACCEPTED; INERT-FOR-TARGET | No range term occurs. Guard pairs for positive/negative ranges are disjoint. |
| `semantics/operators.k` | BASELINE-ACCEPTED | The relevant path evaluates both operands then dispatches `"-"`; ref-dereference priority rules do not match integer operands. Other operators are INERT-FOR-TARGET. |
| `semantics/int.k` | BASELINE-ACCEPTED | `applyBin("-", I1, I2) = I1 -Int I2` is the relevant rule. The remaining integer arithmetic/comparison equations are disjoint by operator and INERT-FOR-TARGET. |
| `semantics/bool.k` | BASELINE-ACCEPTED; INERT-FOR-TARGET | No `BoolOp` or boolean comparison occurs. Guarded `and`/`or` pairs are complementary. |
| `semantics/float.k` | BASELINE-ACCEPTED; INERT-FOR-TARGET | No Float term occurs. All opaque/concrete float symbols are outside every target claim. |
| `semantics/str.k` | BASELINE-ACCEPTED | Only the ASCII docstring literal and its discarded expression value are relevant; recursive code conversion decreases string length. Other string operations are INERT-FOR-TARGET. |
| `semantics/set.k` | BASELINE-ACCEPTED; INERT-FOR-TARGET | No set term occurs. Recursive functions descend structurally and guarded branches are complementary. |
| `semantics/list.k` | BASELINE-ACCEPTED | Empty `ListExpr` allocates a fresh `list(.ValSeq)`; `append` updates exactly the referenced heap list by appending one value and returns `noneV`; `valSeqConcat` descends structurally. Equality/membership/deep equality are INERT-FOR-TARGET. |
| `semantics/tuple.k` | BASELINE-ACCEPTED | Zip yields a two-element tuple; tuple-target binding unpacks left-to-right and writes `score`, then `prediction`, in the active scope. Index/equality/membership rules are INERT-FOR-TARGET. |
| `semantics/subscript.k` | BASELINE-ACCEPTED; INERT-FOR-TARGET | No subscript/slice term occurs. The `[total]` out-of-bounds abstraction cannot affect these claims. |
| `semantics/comprehension.k` | BASELINE-ACCEPTED; INERT-FOR-TARGET | The submitted implementation has an explicit loop, not a comprehension. |
| `semantics/methods.k` | BASELINE-ACCEPTED | The generic method function is present, but the only target method is `append`, whose operational rule is in `list.k`; all declared string/list helper equations here are INERT-FOR-TARGET. |
| `semantics/controls.k` | BASELINE-ACCEPTED | Relevant rules assign `result`, lower `For` to `#loop`, call `#iterNext`, bind each yield, execute the body, and recur through `#loopLbl`. The fixed loop changes `score` and `prediction` on each nonempty iteration. Other control/import rules are INERT-FOR-TARGET. |
| `semantics/functions.k` | BASELINE-ACCEPTED | `FuncDef` installs the exact closure; parameter binding writes `game`/`guess`; `Return` records the result; `#pop` restores the caller and removes the callee scope while leaving escaping heap lists allocated. Annotated closure rules are INERT-FOR-TARGET. |
| `semantics/builtins.k` | BASELINE-ACCEPTED | `zip` constructs a truncating `zipObj`; its three iterator cases are exhaustive and disjoint. Integer `abs` is exactly `absInt`. Other builtin folds, evaluator, and opaque MD5 symbol are INERT-FOR-TARGET. |
| `semantics/call.k` | BASELINE-ACCEPTED | Callee then arguments evaluate left-to-right. Normal name lookup selects the supplied `zip` and `abs`; the bound `append` receiver remains a ref, and the closure call creates/restores one frame. Priority dereferences are narrower than generic routes. Other callable cases are INERT-FOR-TARGET. |
| `semantics/sort.k` | BASELINE-ACCEPTED; INERT-FOR-TARGET | No sorting term or opaque sort symbol occurs. |
| `semantics/assert.k` | BASELINE-ACCEPTED; INERT-FOR-TARGET in proof | Used only by the reviewer concrete harness, not by any target reachability claim. |
| `semantics/dict.k` | BASELINE-ACCEPTED; INERT-FOR-TARGET | No dictionary term occurs. |
| `semantics/concrete.k` | BASELINE-ACCEPTED; INERT-FOR-TARGET in proof | Only in the LLVM runtime. Its deep-equality/key-sort rules do not match the harness's flat integer-list equality through the target proof definition. |

No fixed-semantics rule on the target path fabricates the requested answer.
All proof-relevant opaque/concrete-only symbols in the supplied tree are
syntactically unreachable. The target relies only on K's integer, Boolean,
string, map, and list hooks plus the explicit fixed MPY rules identified above.

## Candidate `verification.k`

| Lines | Extension | Class and decision | Reason |
|---|---|---|---|
| 8-10 | `intVals` plus two equations | Definitional summary; ACCEPTED | Empty/cons cases are disjoint, exhaustive for `IntSeq`, and descend structurally. `[total]` is justified. |
| 14-18 | `absDiffs` plus three equations | Definitional summary; ACCEPTED on every use | Empty-left, nonempty-left/empty-right, and both-nonempty cases are disjoint and cover the `intVals` arguments used by the claims. Recursion decreases both nonempty sequences. It denotes zip-truncated elementwise `absInt(A-B)`. |
| 21-26 | `appendBody` macro | Syntax normalization; ACCEPTED | Expanded KAST is exactly the translated loop body. |
| 28-36 | `compareBody` macro | Syntax normalization; ACCEPTED | Expanded KAST is exactly the translated function body, including the docstring. |
| 38-40 | `compareDef` macro | Syntax normalization; ACCEPTED | Mechanical KAST comparison shows exact equality to the sole translated `FuncDef`. |
| 50-67 | priority-40 `#loop` rewrite | Operational bridge; REJECTED-UNSOUND | It replaces all iterator, tuple-binding, subtraction, `abs`, append, and loop-control execution. Its `...` continuation is arbitrary, and it does not reproduce the loop's `score`/`prediction` scope writes. No bridge-free universal connection theorem exists. |

The rejected bridge overlaps the fixed `controls.k:71` `#loop` rule and wins at
priority 40. Its matched footprint reads `<env>`, `<scopes>`, and `<heap>`,
writes only the result heap entry, preserves omitted cells, erases the loop,
and admits every trailing continuation. Its justification, at most, covers the
specific submitted suffix `Return(Name("result"))`; it does not contain its
actual match domain.

False-conclusion witness: from the satisfiable integer-list loop head in
`05_bridge_context_spec.k`, the trailing continuation reads `score`. Fixed
semantics executes one pair, binds `score=1` and `prediction=2`, appends `1`,
and returns `1`. The bridge appends `1` but skips both bindings and returns the
stale `score=99`.

- `BRIDGE-CONTEXT-FALSE` closes with `#Top`.
- The identical conclusion under `COMPARE-COMMON` is rejected; its residual
  shows `<k> 1`, `score |-> 1`, and `prediction |-> 2`.
- `FIXED-CONTEXT-CORRECT` closes with `#Top`.

Thus the bridge can prove a concrete false statement on integer lists inside
its declared match domain. Finite bridge-free operational examples show that
the fixed semantics works on those examples, but they are not a universal
connection theorem and do not repair this globally false priority rule.

The exact universal claim was also rerun in `COMPARE-COMMON` after removing the
bridge. It exited 1 with `WarnStuckClaimState` and two unexplored branches
(`05_universal_without_bridge_depth100.log`), confirming that the delivered
universal `#Top` depends on the rejected extension. This diagnostic is not
itself treated as proof that the desired theorem is false; it exposes the
genuine residual left after the unsound shortcut is removed.
