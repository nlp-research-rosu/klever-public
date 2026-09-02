# Material source-construct map

The complete supplied-semantics declaration inventory is in
`rule_inventory.txt` (928 top-level declarations: 227 syntax declarations,
695 rules, five contexts, and one configuration). The supplied tree is the
benchmark's fixed trust boundary. The material subset exercised by
`solution.mpy` is mapped here; unrelated fixed rules cannot contribute a
proof-local correctness shortcut.

| Source construct / effect | Fixed declaration and material rules | Review |
|---|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:49–60,124–127` | Exact initial cells; module is decomposed left-to-right and fully consumed. |
| `FuncDef` and closure binding | `syntax.k:53`; `functions.k:14–16` | Binds exact parameter/body/defining environment into scope 0. |
| Name lookup | `syntax.k:12`; `core.k:130–154` | Walks the concrete scope chain. Entry fixes builtin `len`; helper bridges begin only after exact closure selection. |
| Calls and argument order | `syntax.k:28`; `call.k:18–21,69–74`; `core.k:183–191` | Callee first, then arguments left-to-right; user call allocates a frame and exact local scope. |
| Parameter binding | `functions.k:62–75` | One argument binds to the exact `word` or `ch` parameter. |
| Literals | `syntax.k:9–13`; `core.k:193–196`; `str.k:12–17` | Integer/Boolean direct; all program string literals are ASCII and satisfy the literal rule's guard. |
| Assignment | `syntax.k:41 [strict(2)]`; `controls.k:8–18` | RHS evaluates before the current local map is updated. No cellvars or heap aliases occur. |
| `len(word)` | `core.k:156–181`; `call.k:31`; `builtins.k:17–26`; `core.k:227–229` | Exact builtin binding; string length is the constructor length. |
| Integer `-`, `+`, `>` | `syntax.k:15,30–32`; `operators.k:12,14–17`; `int.k:13,22–27` | Standard unbounded integer arithmetic/comparison; index decrement and loop test are faithful. |
| String `==` | `operators.k:14–17`; `str.k:24–26` | Structural equality of code sequences, matching one-character helper arguments against ASCII literals. |
| Unary `not` | `syntax.k:14`; `operators.k:10`; `bool.k:8`; `core.k:198–205` | Applies Boolean truthiness; all relevant values are Booleans. |
| Short-circuit `and` | `syntax.k:16`; `bool.k:13–25` | Evaluates left-to-right and stops at the first false value, matching Python. |
| String subscript | `syntax.k:22,38`; `subscript.k:25–41`; `core.k:227–229` | Evaluates object then index, normalizes nonnegative indices, and returns a singleton string. All program accesses are in bounds under the loop invariant. |
| `While` / loop continuation | `syntax.k:46`; `controls.k:65–91` | Condition is reevaluated; true executes body then loops, false consumes the loop. Inner helper loop becomes one-shot after it sets `found=true`. |
| `Return` and frame cleanup | `syntax.k:50 [strict]`; `functions.k:77–90` | Evaluates result, sets return state, pops exactly one frame, restores caller environment/scope counter, and removes the callee scope. |
| Function result and state | `core.k:44–60`; `functions.k:85–90` | The entry and loop theorems constrain the returned string and all material control/state cells. |

The used fixed subset contains no float operation, sort oracle, MD5 oracle,
assert oracle, I/O, collection mutation, or other opaque result-bearing
primitive. LLVM warnings about unrelated globally total symbols in unused
modules do not affect this theorem. `intSeqAt`, the used positional primitive,
is deliberately partial in the supplied semantics and is invoked only under
proved bounds.
