# Submitted-program constructor and rule map

The trusted translator emits these constructors in `solution.mpy`; the target
claim starts after module loading with the exact closure established by
`pinning-spec.k`.

| Constructor/value | Declaration | Execution rules used by the target |
|---|---|---|
| `Module(Stmts)` | `semantics/syntax.k:61` | Module loading is independently connected to the pre-bound closure by `core.k:124-127` and `functions.k:14-16`; `pinning-spec.k` closes with `#Top`. |
| `FuncDef(String, Params, Stmts)` | `semantics/syntax.k:53`, parameter/list declarations at `56-60` | `functions.k:14-16` creates `closureVal` with the same parameter, body, and defining scope. |
| `Return(Expr)` | `semantics/syntax.k:50` (`strict`) | Strictness evaluates the nested expression; `functions.k:78-90` records the value and pops/restores the call frame. |
| `Call(Expr, Exprs)` | `semantics/syntax.k:28`, `Exprs` at `37` | `call.k:20-21` evaluates callee then arguments; `core.k:185-191` evaluates arguments left-to-right; `call.k:24-32,69-74` dispatches method, builtin, or the real closure. |
| `Name(String)` | `semantics/syntax.k:12` | `core.k:130-154` follows the current scope and parent links. The exact `builtinsScope` at `core.k:157-181` fixes `len` and `set` bindings. |
| `Attribute(Expr,String)` | `semantics/syntax.k:29` (`strict(1)`) | `call.k:16` produces the bound method after evaluating the receiver. |
| Input `str(CS:IntSeq)` | `core.k:13-15,25-39` | The entry claim supplies the arbitrary symbolic code sequence directly; it is bound to `string` by `functions.k:63-66`. |
| `string.lower()` | method application declarations in `methods.k:10` | `methods.k:19,140-156` maps each code using the ASCII-only `lowerC`. |
| `set(...)` | `setV` and helpers in `set.k:8-24` | `builtins.k:41` invokes `dedupCodes`; complementary guarded branches in `set.k:19-24` fold insert-if-absent. |
| `len(...)` | `applyBuiltin`/`seqLen` in `builtins.k:17-26` | `seqLen(setV(DS))` reduces to `isLen(DS)`; `isLen` is defined by `core.k:227-229`. |

The target has no assignment, branch, loop, heap allocation, exception,
output, or proof-local execution bridge. During the only user-function call,
`env`, `scopes`, `scopeLoc`, `stack`, and `ret` are changed and then restored;
`heap`, `heapLoc`, `exc`, and `exit-code` remain unchanged.
