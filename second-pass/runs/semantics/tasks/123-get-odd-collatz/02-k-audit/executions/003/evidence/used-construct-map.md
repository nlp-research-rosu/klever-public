# `solution.mpy` construct-to-semantics map

| Submitted construct | Declaration | Material rules / evaluation behavior | Audit result |
|---|---|---|---|
| `Module(Stmts)` | `reference-semantics/semantics/syntax.k:61` | `core.k:124-127` loads and sequences every statement | Exact submitted module is loaded by `#getOddCollatz`; KAST identity checked. |
| `FuncDef`, `Params` | `syntax.k:53,57,60` | `functions.k:14-16` installs a closure in the current scope | Closure body and defining scope `0` match the submitted function. |
| `Assign(Name, Expr)` | `syntax.k:41` (`strict(2)`) | `controls.k:9-18`; plain-frame rule applies | RHS is evaluated before the scope update; candidate uses no cells. |
| `ListExpr(.Exprs)` | `syntax.k:17` | `list.k:13-15`, `core.k:117-121,185-191,213-219` | Empty list evaluates left-to-right and allocates heap location `0`. |
| `While` | `syntax.k:46` | `controls.k:65-85` | Re-evaluates the guard, executes the body, then returns through `#loopLbl` to the loop head. |
| `If` | `syntax.k:49` (`strict(1)`) | `controls.k:51-54` | Guard evaluates before exactly one branch. |
| `Compare`, `CmpOp` | `syntax.k:30,32` | `operators.k:14-17`; integer `==`/`!=` at `int.k:26-27` | Both candidate guards are exact integer comparisons. |
| `BinOp` | `syntax.k:15` (`seqstrict(2,3)`) | `operators.k:12`; integer `+`, `*`, `%`, `//` at `int.k:9,14-20` | Left-to-right evaluation; `pyMod` and floor division agree with Python on divisor `2`. |
| `Name` | `syntax.k:12` | `core.k:130-154` | Current frame lookup followed by module/builtins parent lookup. |
| `Call`, `Attribute` | `syntax.k:28-29` | `call.k:16-21`, `core.k:185-191` | Callee first, then arguments left-to-right. |
| `odd_numbers.append(n)` | declarations above | `call.k:52-60`, `list.k:53-55` | Mutating method keeps the receiver reference and appends in place. |
| `sorted(odd_numbers)` | builtin binding at `core.k:157-181` | builtin argument dereference at `call.k:38-41`; allocation at `sort.k:36-37` | Produces a fresh list whose sequence is the opaque fixed-semantics primitive `sortVS(VS)`. |
| `Expr(Call(...))` | `syntax.k:52` (`strict`) | `controls.k:48` | The append effect happens before its `noneV` result is discarded. |
| `Return(Call(...))` | `syntax.k:50` (`strict`) | `functions.k:78-90` | The `sorted` call completes, return stores the ref, pops the frame, restores the caller, and preserves the heap. |
| Configuration/state | `core.k:49-60` | allocation, scopes, stack, return, exception, and exit cells above | Every material used operation updates or preserves the expected cells; no used operation is fabricated or skipped. |

The full 943-item declaration/rule/claim inventory is in
`rule-inventory.tsv`. It includes 230 syntax declarations, 700 rules, one
configuration, five contexts, and seven claims. There are no
`[simplification]`, `[functional]`, or `[anywhere]` declarations in the
candidate/imported K source. All 22 `[no-evaluators]` symbols are inventoried;
only `sortVS` is reached by this program.
