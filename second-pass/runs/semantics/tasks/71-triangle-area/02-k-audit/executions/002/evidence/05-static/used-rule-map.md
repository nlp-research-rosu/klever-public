# Used-rule map and static decisions

This map is independent of the candidate's prose. The exhaustive source-level
inventory is `rule-inventory.tsv`. Because the rendered mode is
`SUPPLIED_SEMANTICS`, all entries under `reference-semantics/` are the immutable
trusted baseline; the audit nevertheless traced every construct actually used
by `solution.mpy` through the following rules.

| Program construct / effect | Declaration and operational path | Static decision |
|---|---|---|
| `Module`, statement lists | `syntax.k:56,61`; `core.k:124-127` | Sound sequencing: loading exposes the exact statements in order. |
| `FuncDef`, `Params` | `syntax.k:53,57,60`; `functions.k:14-16` | Sound for this module-level definition: binds the exact parameter list, body, and definition environment. |
| Call and left-to-right argument evaluation | `syntax.k:28`; `call.k:18-21,69-75`; `core.k:183-191` | Sound on the exact empty-stack call configurations. Callee and three arguments evaluate left to right; a frame is allocated, parameters bind in order, and return restores the caller. |
| Name lookup and assignment | `syntax.k:12,41`; `core.k:129-181`; `controls.k:8-18` | Sound on these plain frames: `a,b,c,s` resolve through the active frame, `round` through the fixed builtins scope, and `s` is written to the active scope. Cell-priority rules are inapplicable because the frame has no `$cells`. |
| Integer literals and unary `-` | `syntax.k:9,14`; `core.k:193-196`; `operators.k:10`; `int.k:7` | Sound; the invalid return becomes mathematical integer `-1`. |
| Integer `+` and `<=` | `syntax.k:15,30,32`; strict contexts in `operators.k:12,15-17`; `int.k:9,23` | Sound on `Int` parameters and preserves left-to-right operand evaluation. |
| Short-circuit `or` | `syntax.k:16`; `bool.k:13-25` | Sound and value-returning. Here every element is `Bool`, so it yields the first true comparison or the final false comparison exactly as Python does. |
| `If` | `syntax.k:49`; `controls.k:50-54`; `core.k:198-205` | Sound: comparison results are booleans, the selected branch is sequenced, and the empty else is `.Stmts`. |
| Return / frame pop | `syntax.k:50`; `functions.k:77-90` | Sound on the exact call context; the return discards the remaining function-body statements, stores the value, pops the frame, and restores the empty continuation. |
| True division of two integers | `float.k:29-32` | Fixed trusted primitive. Symbolic proof retains `divII(sum,2)`; LLVM concretely uses 53/11 floating conversion and float division. Divisor is the literal 2. |
| Mixed float/int subtraction and multiplication | `float.k:101-121,131-139,194-202` | Fixed trusted primitives. `intToF`, `subF`, and `mulF` remain opaque in proofs and have concrete LLVM equations. Sort-disjoint cases select the expected promotion. |
| Exponentiation by `0.5` | `float.k:119-121,131-133` | Fixed trusted `powF` primitive with concrete `^Float` equation. It remains structural in the symbolic theorem. |
| Lookup/call of `round(...,2)` | `core.k:156-181`; `call.k:18-32`; `float.k:216-228` | Fixed trusted `roundFN` primitive. The proof constrains the returned term but does not derive IEEE-754 or Python rounding mathematics inside Haskell. |
| Concrete smoke assertions | `assert.k:6-15`, imported only for smoke execution | No role in positive proof closure because `solution.mpy` and every target claim contain no `Assert`. The witness run uses it only as a concrete oracle. |

## Candidate-local declarations and rules

`verification.k` has five syntax declarations and five unconditional function
rules. There are no candidate-local priority, simplification, `total`,
`functional`, opaque, or operational bridge rules.

1. `triangleAreaBody` names the exact body constructor sequence. It is a
   definitional alias, not an execution shortcut.
2. `triangleAreaClosure` names `closureVal(("a","b","c"), triangleAreaBody,0)`.
   It pins the parameters, body, and module definition environment.
3. `triangleAreaModule` names the exact module/function binding. The generated
   pinning claim loads the constructor term mechanically inserted from
   `solution.mpy` and closes only against this same closure.
4. `semiPerimeter` and `expectedArea` are truthful, terminating definitional
   summaries. Fully expanding them yields the same left-associated sequence
   `divII`, `intToF`, `subF`, `mulF`, `powF`, `roundFN` produced by actual
   execution. They neither intercept `<k>` execution nor introduce fresh
   values.

No local rule has overlapping guards or recursive descent. No local rule
fabricates a value, changes control, writes state, or preempts the supplied
semantics. Accordingly there is no unsound-rule finding and no false-conclusion
witness to report.
