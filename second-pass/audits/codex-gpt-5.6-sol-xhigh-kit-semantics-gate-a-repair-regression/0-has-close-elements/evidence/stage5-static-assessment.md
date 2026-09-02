# Static rule assessment

This assessment applies to every record in `stage5-rule-inventory.txt`. The
inventory is the exhaustive, line-addressed source of individual declarations:
26 source files, 1,104 records, 698 `rule` records, 230 `syntax` records, 5
contexts, 1 configuration, and 3 claims. No local `[simplification]` or
`[functional]` declaration occurs.

## Categorical decision for all inventory records

| Inventory category | Decision |
|---|---|
| `requires`, `module`, `endmodule`, `imports` | Dependency/module declarations; no logical conclusion. The candidate semantics dependency graph is byte-identical to the trusted supplied tree. |
| `syntax`, `context`, `configuration` | Declarations, evaluation contexts, or initial-cell shape. They do not assert the task result. Used productions and cells are mapped below. |
| Fixed-baseline equational rules unused by the submitted program | Definitions for the documented MPY subset. They cannot contribute to these claims because their constructors never occur on the reachable term. No candidate verdict relies on them. The explicit global discrepancies and evidence gaps below are exceptions to an unqualified Python-fidelity assessment. |
| Fixed-baseline operational rules unused by the submitted program | Inert for these claims by constructor/sort/guard mismatch. They add no task-specific conclusion. |
| Fixed-baseline rules on the submitted-program path | Reviewed below. They preserve lookup, left-to-right argument and operand evaluation, scope writes, loop control, return/frame popping, and the result on every claim state. |
| `[concrete]` equations | LLVM-only definitions of concrete operations. They are absent from the Haskell proof theory; they support concrete evidence but do not close the symbolic proof. |
| `[symbol(...), no-evaluators]` declarations | Named opaque Haskell-backend primitives. The program path uses exactly `subF`, `absF`, and `floatLt`; the theorem is conditional on the same `floatLt(absF(subF(A,B)),T)` atom. Other opaque symbols are unreachable. |
| `[total]` declarations | Defined recursively where used. The compiler-detected incomplete cases are listed below; no incomplete case is reachable in these claims. |
| Fixed-baseline priorities and `[owise]` rules | No proof-local priority exists. On the used path, priorities only route heap references/cells or specialized calls; the claims use a bare list and plain frame, so the generic exact rules apply. `[owise]` generic call routing is the intended route. |
| Candidate `targetClosure` macro | Exact normalized constructor identity with the trusted translator output. It is a compile-time abbreviation, not an operational bridge. |
| Candidate `outerRun` macro | Exact normalized constructor identity with the reachable post-initialization outer-loop computation and its `Return(false) ~> #endcall` continuation. |
| Candidate `innerRun` macro | A compile-time abbreviation, hence not a false semantic rewrite, but it is not the actual reachable continuation: inside `#loopLbl(#while(...))` it omits the outer body's final `AugAssign(i, "+", 1)`. This is an auxiliary-claim pinning defect. |
| `outer-loop-true` and `entry-true` claims | Result-constraining and sound under their close-pair precondition. `entry-true` closes in an auditor-authored module containing no helper claims. |
| `inner-loop-true` claim | Sound for the term it states because the assumed first inner comparison returns immediately, but its LHS is not the real inner-loop control state due to the `innerRun` defect. It is not used by the isolated entry proof. |

## Used syntax and rules

| Program construct | Declaration and execution rules | Static decision |
|---|---|---|
| `ImportFrom("typing","List")` | `syntax.k`; non-math `ImportFrom` `[owise]` no-op in `controls.k` | Faithful for this annotation-only import. The entry claim starts after module loading and therefore uses the resulting closure state rather than executing this statement. |
| `FuncDef` / bound entry call | `functions.k` closure creation; `core.k` lookup; `call.k` callee/argument evaluation, frame allocation, `#bindP`; `functions.k` return and `#pop` | Exact parameter order and body; caller environment, stack, callee scope, return, and scope restoration are preserved. Exact arity avoids the subset's missing arity-error behavior. |
| `Assign` and `AugAssign` | strict RHS productions; `controls.k` current-scope updates; `int.k` `+Int` | Exact for plain local integer variables. Cell/ref priority rules do not match. |
| `len(numbers)` | lookup of `builtinV("len")`; left-to-right call evaluation; `applyBuiltin("len")`; `seqLen(list(VS))`; `vsLen` | Exact list length; no allocation or mutation. |
| outer and inner `While` | `controls.k`: `While -> #while`, condition evaluation, `truthy`, body plus `#loopLbl`, false exit | Exact control for `outerRun` and the entry body. The candidate's separate `innerRun` abbreviation has the continuation mismatch described above. |
| `numbers[i]`, `numbers[j]` | subscript contexts, `applyIndex(list(...))`, nonnegative `normIdx`, recursive `valSeqAt` | Both accesses are provably in bounds in the close-pair claims (`i=0`, `j=1`, length 2). |
| float subtraction, absolute value, and `<` | `applyBin("-", Float, Float) -> subF`; `applyBuiltin("abs", Float) -> absF`; `applyCmp("<", Float, Float) -> floatLt` | Opaque but shared fixed primitives in Haskell; concrete IEEE operations in LLVM. The proof is interpretation-parametric/conditional on the exact predicate. |
| `If(... Return(true) ...)` | strict condition, `truthy(Bool)`, `#branch`; abrupt `Return(V) ~> _ -> #pop` | The precondition selects the `true` branch, and return correctly discards the remaining loop continuation. |
| final `Return(false)` | same return/pop rules | Present in the exact closure and outer continuation, but unreachable under the three claims' close-pair precondition. |

## Configuration and state

The used configuration has `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`,
`<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`. The entry claim
starts in module environment 0 with the exact closure, a real builtins scope,
empty heap and stack, `noRet`, `NoExc`, and exit code 0. The call rule allocates
scope 1, pushes the exact continuation, binds both arguments, and `#pop`
restores environment 0, removes scope 1, restores `scopeLoc`, and returns the
Boolean. The list is a bare immutable claim value, so no heap or allocation rule
is exercised.

The final entry result is literally `true`; it is neither a free variable nor
an implication-only summary. The helper conclusions require `retV(true)` and
`#pop`, so they also constrain the returned value.

## Opaque and total symbols

The Haskell proof's result-bearing opaque path is:

`subF(A,B) -> absF(...) -> floatLt(...,T)`.

These are supplied fixed primitives, not program-derived summaries or
candidate rules. The same final Boolean atom appears as the precondition and is
recomputed by fixed dispatch; the theorem therefore establishes control
correctness conditional on that named primitive contract. LLVM execution and
the independent Python differential run provide finite support for the
primitive bridge, not a universal IEEE theorem.

The fresh LLVM build warned that `mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt` have non-exhaustive equations despite `[total]`.
Only `valSeqAt` occurs on the proof path, and only at the explicitly
constructor-headed in-bounds positions 0 and 1, for which its equations are
complete. The other warning domains are unreachable. This is a narrower
evidence/semantics gap, not an asserted false conclusion on a claim state.

## Supplied-baseline global discrepancy with false-conclusion witness

`float.k` defines:

```k
applyCmp(">=", F1, F2) => notBool floatLt(F1, F2)
applyCmp("<=", F1, F2) => notBool gtF(F1, F2)
```

These do not match Python/IEEE unordered-NaN comparisons. Witness:
`F1 = NaN`, `F2 = 0.0`. Both Python comparisons `NaN >= 0.0` and
`NaN <= 0.0` are false, while both K right-hand sides are true because
`NaN < 0.0` and `NaN > 0.0` are false. Neither operator occurs in
`solution.mpy`, any claim, or the proof path. This is a limitation of the
trusted supplied baseline, not a candidate proof extension and not an enabler
of the submitted `<` theorem.

No candidate rule encodes the task answer, fabricates a used result, replaces
program execution, or introduces an unconstrained program-derived oracle.
