# Submitted-program constructor and execution-rule map

This map is based on the trusted-regenerated `solution.mpy`. Line references are
to `/tmp/audit-work/source/reference-semantics`.

| Submitted constructor/operation | Declaration | Execution path |
|---|---|---|
| `Module` and statement list | `semantics/syntax.k:56,61` | `semantics/core.k:124-127` (`#loadAll`, left-to-right statement sequencing, empty list) |
| `FuncDef`, `Params`, parameter-name list | `semantics/syntax.k:53,57,60` | `semantics/functions.k:14-16` creates the `closureVal` in the current module scope |
| `Call(Name("digits"), Int(N))` | `semantics/syntax.k:28` | `semantics/call.k:20-21` evaluates callee then arguments; `semantics/core.k:185-191` evaluates arguments left-to-right; `semantics/call.k:69-75` pushes a user frame; `semantics/functions.k:63-66` binds `n` |
| `Name` | `semantics/syntax.k:12` | `semantics/core.k:130-154` follows current/parent scopes. The higher-priority cell path is disabled because this unannotated frame has no `"$cells"` key. |
| `Assign(Name, Expr)` | `semantics/syntax.k:41` with strict RHS | `semantics/controls.k:9-18`. The ordinary local-map update applies; the cell-write priority path is disabled by the same absent `"$cells"` guard. |
| `Int` literal | `semantics/syntax.k:9` | `semantics/core.k:193-196` |
| `BinOp` | `semantics/syntax.k:15` with `seqstrict(2,3)` | `semantics/operators.k:12` dispatches after left-to-right evaluation. Integer `*`, `%`, and `//` are `semantics/int.k:14-20`; divisors are fixed nonzero `2` and `10`. |
| `Compare` / `CmpOp` | `semantics/syntax.k:30,32` | evaluation contexts and dispatch at `semantics/operators.k:14-17`; integer `>`, `==` at `semantics/int.k:22-27` |
| `If` | `semantics/syntax.k:49` with strict condition | `semantics/controls.k:50-54`; integer truthiness is `semantics/core.k:198-205` |
| `While` | `semantics/syntax.k:46` | `semantics/controls.k:65-82`: condition evaluation, truthy branch, body, loop label, and false exit |
| `Return` | `semantics/syntax.k:50` with strict value | `semantics/functions.k:77-90`: set return state, pop frame, restore environment/scope counter/stack, and resume caller continuation |

No program constructor allocates or dereferences a heap object, invokes a
builtin, uses a float/string/list/tuple/dict/set/range/sort/md5 operation, or
raises an exception. Therefore the opaque `no-evaluators` symbols and the
concrete-only module cannot influence a branch, state cell, or returned value.

The actual state footprint is:

- module loading updates scope `0` with the `digits` closure;
- the call pushes then pops one frame, temporarily changes `<env>`,
  `<scopeLoc>`, `<stack>`, and `<ret>`, and creates/deletes local scope `1`;
- the body updates only local names `product`, `found`, and `n`;
- `<heap>`, `<heapLoc>`, `<exc>`, and `<exit-code>` remain unchanged.

