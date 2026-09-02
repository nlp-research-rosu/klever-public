# `solution.mpy` construct-to-semantics map

All paths below are under the byte-identical candidate/trusted
`reference-semantics/` tree. The complete declaration inventory is
`rule_inventory.tsv`.

| Submitted constructor | Syntax declaration | Material execution rules |
|---|---|---|
| `Module` | `semantics/syntax.k:61` | `semantics/core.k:124-127` loads and sequences all statements. |
| `FuncDef` / `Params` | `semantics/syntax.k:53,57,60` | `semantics/functions.k:14-16` installs the exact closure body in the current scope. |
| `Assign` | `semantics/syntax.k:41` (`strict(2)`) | `semantics/controls.k:9-18`; the ordinary local-frame rule applies here. |
| `Name` | `semantics/syntax.k:12` | `semantics/core.k:130-154` starts and completes lexical lookup; the local binding is selected before the builtins parent. |
| `Int` / `Bool` | `semantics/syntax.k:9,11` | `semantics/core.k:193-196` cools literals to semantic K `Int`/`Bool` values. |
| `For` | `semantics/syntax.k:45` (`strict(2)`) | `semantics/controls.k:65,69-74` evaluates the iterable once and routes through `#loop`; `semantics/list.k:9-10` yields one list head and structural tail at a time. |
| `If` | `semantics/syntax.k:49` (`strict(1)`) | `semantics/controls.k:51-54`; `semantics/core.k:199-205` supplies truthiness. |
| `UnaryOp("not", ...)` | `semantics/syntax.k:14` (`strict(2)`) | `semantics/operators.k:10` dispatches and `semantics/bool.k:8` applies Boolean negation to `truthy`. |
| `BinOp("%", ...)` | `semantics/syntax.k:15` (`seqstrict(2,3)`) | `semantics/operators.k:12`; fixed `semantics/int.k:15,19-20`; the exact guarded proof-side dynamic-sort twin is `verification.k:45-48`. |
| `Compare(..., CmpOp("==", ...))` | `semantics/syntax.k:30,32`; evaluation contexts `semantics/operators.k:15-16` | `semantics/operators.k:17` dispatches; `semantics/int.k:26` supplies integer equality. |
| `AugAssign(..., "+", ...)` | `semantics/syntax.k:44` (`strict(3)`) | `semantics/controls.k:20-23` reads and writes the same local; fixed `semantics/int.k:9`; the exact guarded proof-side dynamic-sort twin is `verification.k:49-52`. |
| `Return` | `semantics/syntax.k:50` (`strict`) | `semantics/functions.k:78-90` records the value, restores the caller continuation/environment, and removes the function frame. |
| `Call` added by the entry claim | `semantics/syntax.k:28` | `semantics/call.k:18-21,69-75` evaluates the callee and arguments left-to-right, binds the closure parameters, executes the stored body, and pushes/restores the frame. |

The relevant state footprint is therefore: `<k>` control; `<env>` and
`<scopes>` for definition, lookup, arguments, locals and final module result;
`<stack>`, `<ret>` and `<scopeLoc>` for call/return. The submitted code performs
no allocation, mutation of its input, output, exception, import, or abrupt loop
control. The entry claim explicitly pins those material cells and requires
`NoExc`, `noRet`, an empty stack and the restored allocation counter.
