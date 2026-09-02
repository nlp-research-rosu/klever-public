# Submitted-program constructor and execution map

This map is based on the clean trusted supplied-semantics copy and the
byte-identical `solution.mpy`.

| Submitted construct | Declaration | Material execution rules |
|---|---|---|
| `Module` and statement juxtaposition | `syntax.k:56,61` | `core.k:124-127` loads and sequences the module left-to-right. |
| `ImportFrom("typing","List")` | `syntax.k:43,60` | `controls.k:35-44`; the non-`math` import is an `owise` no-op, which is semantically inert because this import is typing-only. |
| annotated `FuncDef`, `Params`, `CellVars`, `FreeVars` | `syntax.k:53-60` | `functions.k:33-45` creates the exact closure; `call.k:80-94` allocates its frame/cells and binds arguments; `functions.k:63-75` writes parameters. |
| `Assign` | `syntax.k:41` with strict RHS | `controls.k:9-18` writes through declared closure cells, preserving Python closure binding for `min_number` and `max_number`. |
| `Name` | `syntax.k:12` | `core.k:130-154` implements scope-chain lookup and closure-cell dereference. |
| `Call` | `syntax.k:28` | `call.k:18-32` evaluates callee then arguments; `core.k:183-191` evaluates arguments left-to-right. Candidate `verification.k:12-17` preempts only the material `min`/`max` dispatches. |
| `min(numbers)` / `max(numbers)` | builtins namespace in `core.k:156-181` | Fixed dispatch is `call.k:29-30`, integer folds are `builtins.k:75-94`, float folds are `float.k:237-255`; candidate priority bridges replace these fixed folds with `minVF`/`maxVF`. |
| `Return` | `syntax.k:50` with strict result | `functions.k:77-90` records the value, pops the exact call frame, restores control, and preserves heap allocations. |
| `ListComp` / `CompFor` / `Bool(true)` | `syntax.k:9-20,35-36` | Fixed macro expansion is `comprehension.k:10-26`, using `controls.k:69-75` and list iteration `list.k:8-15`; candidate `verification.k:54-81` instead summarizes the exact comprehension expression. |
| nested `BinOp("-",...)` then `BinOp("/",...)` | `syntax.k:14-15` uses left-to-right `seqstrict(2,3)` | `operators.k:10-12`; material float cases are `float.k:101-109`, producing opaque proof-side `subF`/`divF` terms with trusted concrete LLVM twins. |
| output list allocation and returned reference | `core.k:117-121`, `list.k:12-15` | Candidate comprehension bridge performs one `#alloc`; `verification.k:85-87` observes the heap value at the returned reference. |

Configuration/cell check: `core.k:49-60` defines every cell appearing in the
claim. The entry pins the initial environment, scope store, scope allocator,
empty heap/heap allocator, empty stack, `noRet`, `NoExc`, and exit code 0.
The post existentially frames the final scope store, heap, and allocators while
requiring the returned list value and restoring the control cells. The
program-wrapper rule itself changes only `<k>`; source execution performs all
binding, call, return, and state transitions.
