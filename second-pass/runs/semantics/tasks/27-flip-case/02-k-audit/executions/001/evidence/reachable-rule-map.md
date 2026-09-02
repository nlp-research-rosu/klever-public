# Reachable rule map and extension review

This map is supplementary to `rule-inventory.md`, which lists all 935 local
source directives. It records the exact execution slice used by the submitted
program and the static decision for each contributing group.

| Phase | Source declarations/rules | Static decision |
|---|---|---|
| Parse submitted AST | `semantics/syntax.k:9-30,41-61` | `Module`, `FuncDef`, `Params`, `Return`, `Call`, `Attribute`, `Name`, `Stmts`, `Exprs`, and strings are declared. `Return` and `Attribute` strictness evaluate the returned expression and receiver; `Call` uses the explicit call route. |
| Initial state | `semantics/core.k:13-60` | `IntSeq`, `str`, closure and bound-method values, and every claimed cell are declared. The entry state is the standard empty module state with builtins at `-1`. |
| Load and define | `semantics/core.k:124-127`; `semantics/functions.k:14-16` | `#loadAll` executes the module statements. `FuncDef` installs the submitted body as a closure in scope 0. No body is skipped. |
| Find and call function | `semantics/core.k:130-181,185-191`; `semantics/call.k:20-24,69-74` | `Name("flip_case")` resolves the closure; empty arguments are evaluated; the call creates a temporary scope, saves the exact continuation, and binds `string` left-to-right. Cell-priority rules do not match because this is an unannotated closure and no `$cells` binding exists. |
| Evaluate body | `semantics/functions.k:62-90`; `semantics/call.k:16,20-24` | Parameter binding stores `string -> str(S)`. Strict `Return` evaluates `Call(Attribute(Name("string"),"swapcase"),.Exprs)`. Lookup selects the parameter, `Attribute` creates the bound method, and generic call routing dispatches with no arguments. |
| Compute result | `semantics/methods.k:10,21,112-164` | `applyMethod(...,"swapcase",.Vals)` returns `str(mapSwap(S))`. `mapSwap` structurally descends. `swapC` has disjoint upper/lower guards and an `owise` complement, so coverage is total and overlaps agree vacuously. This is the supplied ASCII case model, not full Python Unicode casing. |
| Return and cleanup | `semantics/functions.k:78-90` | `Return` sets `retV`, `#pop` restores the saved continuation and environment, deletes the temporary scope, resets `scopeLoc`, empties the frame stack, and leaves heap, exception, and exit status unchanged. |
| Candidate aliases | `verification.k:8-18` | Both macros expand to the exact byte-validated submitted constructor tree. They are compile-time aliases, not executable summaries or oracles. |
| Candidate runner | `verification.k:21-24` | The fresh runner expands to `#loadAll(solutionModule) ~> Call(...)`. It preserves the continuation and all cells and does not replace program-defined execution. A helper-free universal direct claim closes under the fixed supplied semantics (`direct-pinning.k`). |
| Entry theorem | `spec.k:8-30` | The pre-state is satisfiable (the standard state with any algebraic `IntSeq`). The RHS fixes the return to `str(mapSwap(S))` and fixes all observable cells; it contains no free result variable or implication. |

No proof-local functions, `total`/`functional` declarations, opaque symbols,
priorities, simplifications, or operational shortcuts occur in
`verification.k`. The supplied baseline contains 155 function declarations,
115 `total` attributes, 41 `priority(40)`, three `priority(45)`, one
`priority(39)`, 35 `concrete`, and 22 `no-evaluators` attributes. None of the
opaque/`no-evaluators` symbols is reachable from this program. There are no
source-level `functional` or `simplification` attributes.

The compiler warned that `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt` are not exhaustively defined despite totality. None occurs in the
reachable term graph above. The full inventory marks these and all other
out-of-slice declarations individually.
