# Constructor-to-semantics map for `solution.mpy`

| Submitted constructor or effect | Declaration | Material execution rules |
|---|---|---|
| `Module(Stmts)` | `semantics/syntax.k:56-61` | `#loadAll(Module(SS)) => SS` and statement sequencing in `semantics/core.k:123-127` |
| `FuncDef("exchange", Params(...), Body)` | `semantics/syntax.k:53,57,60` | Installs `closureVal` in the current scope at `semantics/functions.k:14-16` |
| `Expr(Str(docstring))` | `semantics/syntax.k:13,52` | String literal conversion at `semantics/str.k:13-17`; expression value is discarded at `semantics/controls.k:46-48` |
| `Assign(Name(...), Int(...))` | `semantics/syntax.k:9,12,41` | RHS strictness is declared on `Assign`; integer literal at `semantics/core.k:193-196`; ordinary frame update at `semantics/controls.k:9-11` |
| `For(Name, Name, Body)` | `semantics/syntax.k:12,45` | Name lookup at `semantics/core.k:129-154`; `For` to `#loop` and loop protocol at `semantics/controls.k:62-74`; list iterator cases at `semantics/list.k:8-10` |
| Loop-target binding | `#bindTgt` imported through `MPY-TUPLE` | For-loop yield sends the value through `#bindTgt` at `semantics/controls.k:73-74`; the ordinary name target updates the current frame at `semantics/tuple.k:32-34` |
| `BinOp("%", Name("value"), Int(2))` | `semantics/syntax.k:15` (`seqstrict(2,3)`) | Cooled operator routing at `semantics/operators.k:12`; Int modulo at `semantics/int.k:15,19-20`; proof-local Bool/Float promotions at `verification.k:106-107` |
| `Compare(..., CmpOp("==", Int(0)))` | `semantics/syntax.k:30,32` | Left then wrapped-right evaluation contexts and routing at `semantics/operators.k:14-17`; Int equality at `semantics/int.k:26`; proof-local Float promotion at `verification.k:108`; connected pure simplification at `verification.k:161-163` |
| `If(condition, then, .Stmts)` | `semantics/syntax.k:49` (`strict(1)`) | `If` to `#branch` and true/false selection at `semantics/controls.k:50-54`; `Bool` is a `Val`/`KResult` |
| `AugAssign(Name("even_count"), "+", Int(1))` | `semantics/syntax.k:44` (`strict(3)`) | Ordinary binding update at `semantics/controls.k:20-23`; Int addition at `semantics/int.k:9` |
| `Call(Name("len"), Name("lst1"))` | `semantics/syntax.k:28` | Callee-before-arguments evaluation at `semantics/call.k:18-21` and `semantics/core.k:183-191`; builtin lookup from `builtinsScope` at `semantics/core.k:156-181`; dispatch at `semantics/call.k:31`; `len(list(VS)) = vsLen(VS)` at `semantics/builtins.k:19-26` and `semantics/core.k:223-225` |
| Final `Compare(..., CmpOp(">=", len-call))` | `semantics/syntax.k:30,32` | Comparison routing at `semantics/operators.k:14-17`; Int `>=` at `semantics/int.k:25` |
| `Return(Str("YES"/"NO"))` | `semantics/syntax.k:13,50` (`strict`) | String conversion at `semantics/str.k:13-17`; return records `retV`, discards the remaining body, pops the exact call frame, restores continuation/environment, and deallocates the frame at `semantics/functions.k:77-90` |
| Function call/frame lifecycle | `closureVal`, `frame`, `#bindP` in `semantics/core.k`/`functions.k` | User call allocates a frame, binds arguments, runs the actual body, and installs `#endcall` at `semantics/call.k:69-74`; parameter binding at `semantics/functions.k:62-66`; return/pop above |

The proof entry supplies bare `list(VS)` values rather than source list
constructors. The supplied core explicitly permits bare lists as read-only
input values; this function never mutates either list. Concrete source list
literals allocate heap references, but `For` and `len` dereference them before
the same read-only operations (`semantics/controls.k:104-108` and
`semantics/call.k:34-50`).
