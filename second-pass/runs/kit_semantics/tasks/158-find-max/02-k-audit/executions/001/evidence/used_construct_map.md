# Submitted-program construct and rule map

The mechanically pinned program term uses these source constructors:
`Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Str`, `UnaryOp`, `Int`,
`For`, `Call`, `BoolOp`, `Compare`, `CmpOp`, `If`, and `Return`. Empty
`Exprs`/`Stmts` are syntax-list units.

| Program operation | Declaration/rule source | Effect checked |
|---|---|---|
| Module/statement syntax and strictness | `semantics/syntax.k:9-61` | Declares every constructor above; strict/seqstrict evaluates assignment RHS, `For` iterable, `If` condition, `Return` expression, unary operands in the required order. |
| Initial configuration and values | `semantics/core.k:10-63` | Defines `Val`, `str(IntSeq)`, `list(ValSeq)`, scopes, heap, stack, return/exception/exit cells. |
| Module loading/sequencing | `semantics/core.k:126-131` | `#loadAll(Module(SS))` executes `SS`; statement lists execute left-to-right. |
| Name lookup/binding selection | `semantics/core.k:134-155`, `semantics/core.k:157-181` | Searches the exact current scope chain and resolves `len`/`set` from builtins unless shadowed. The claim pins the module closure and has no shadowing binding. |
| Literal evaluation | `semantics/core.k:199-202`, `semantics/str.k:13-17` | Integers and the ASCII empty-string literal become modeled values; only `""` is a source literal in the function. Symbolic input strings are already `str(IntSeq)` values. |
| Function definition, call, argument evaluation, return/pop | `semantics/functions.k:12-16`, `semantics/functions.k:62-91`, `semantics/call.k:15-30`, `semantics/call.k:69-76` | Registers the exact closure, evaluates callee then arguments left-to-right, binds `words`, executes the body, returns the selected value, restores the caller, and removes the frame. |
| Assignment | `semantics/controls.k:8-18` | Writes `result`, `max_unique`, `word`, and `unique` in the current local scope. Cell-specific priority rule is inapplicable because the pinned closure is unannotated and has no `$cells`. |
| List iteration and `for` control | `semantics/list.k:8-10`, `semantics/controls.k:60-70`, `semantics/controls.k:82` | A list yields its head and remaining list; loop target binding, body execution, and continuation return to the exact `#loop` head used by `SPEC.loop-inv`. |
| Unary minus and integer comparison | `semantics/operators.k:10-17`, `semantics/int.k:7`, `semantics/int.k:22-27` | Initializes scores to `-1`; evaluates `>`, `==` with ordinary unbounded integer operations. |
| Short-circuit Boolean operations | `semantics/bool.k:13-25` | Implements the translated `unique > max_unique or (unique == max_unique and word < result)` with Python order and short-circuiting. |
| `set(word)` | `semantics/builtins.k:17`, `semantics/builtins.k:40-42`, `semantics/set.k:10-27` | Fixed constructor rule maps a string to distinct codes via a structurally descending first-occurrence fold. The proof-local guarded dynamic twin is reviewed separately. |
| `len(set(word))` | `semantics/builtins.k:19-26`, `semantics/core.k:227-229` | Returns the length of the deduplicated code sequence. |
| Lexicographic string `<` | `semantics/str.k:43-59` | Exhaustive disjoint empty/head-less/head-equal equations implement lexicographic integer-code order. The proof-local guarded dynamic twin is reviewed separately. |
| `If` and result updates | `semantics/controls.k:48-52` | Chooses exactly one branch from the Boolean result; the true branch performs both sequential assignments. |

Priority review for the reachable slice:

- Fixed priority rules for cell writes, heap-reference dereference, mutating
  list operations, imports, floats, dictionaries, and methods do not match the
  unboxed read-only list/string inputs and unannotated closure in this claim.
- No proof-local rule has a `priority` attribute or rewrites a `<k>` control
  context. The two proof-local dispatch rules are simplification equations on
  fixed function symbols and leave every continuation/configuration cell
  untouched.
- The only reachable opaque/no-evaluators symbol is proof-local
  `projectStrTotal`; all target uses are under `isStr`, where it is equated to
  the built-in `Val :> Str` projection. Fixed opaque float, sorting, MD5, and
  keyed-sorting symbols are unreachable from the submitted term.
