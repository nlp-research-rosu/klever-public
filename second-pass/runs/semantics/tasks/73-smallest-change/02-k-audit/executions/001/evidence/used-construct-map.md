# Submitted `solution.mpy` construct-to-semantics map

The submitted AST uses only the constructs listed below. Line references are to
the isolated byte-identical supplied semantics copy.

| Submitted construct | Syntax declaration | Fixed-semantics rules | Proof-extension treatment | Audit result |
|---|---|---|---|---|
| `Module(Stmts)` and statement sequencing | `semantics/syntax.k:61`; `semantics/core.k:49-60,124-127` | configuration begins with `#loadAll`; module body loads and statements sequence | No entry claim begins at `Module(...)`; module loading is omitted | Not pinned |
| `FuncDef`, `Params` | `semantics/syntax.k:53,57,60` | `semantics/functions.k:14-16` installs exact closures in the active scope | Proof-local `#helperClosure` and `#mainClosure` macros manually construct closures | Textually matching, but no mechanical link to loaded program |
| `Name` | `semantics/syntax.k:12` | `semantics/core.k:130-154` walks lexical scopes and builtins | Bridges match after callee/argument lookup and thereafter avoid helper-name lookup entirely | Recursive binding is assumed by the synthetic target |
| `Call` and argument evaluation | `semantics/syntax.k:28` | `semantics/call.k:20-21`; `semantics/core.k:183-191` evaluates callee then arguments left-to-right | At `#applyK`, priority-40 bridge rules replace both user closures with `#targetCall` | Fixed closure call/body execution bypassed |
| User call frame, parameter binding, return | `semantics/functions.k:8-11` | `semantics/call.k:69-74`; `semantics/functions.k:63-90` bind, push, execute, pop, and restore | None of those rules executes after the bridge | No bridge-free connection theorem |
| `If` | `semantics/syntax.k:49` | strict condition plus `semantics/controls.k:51-54` truth branch | Replaced by `#targetCall` base/recursive guards | Hand-coded recurrence |
| `Return` | `semantics/syntax.k:50` | strict expression plus `semantics/functions.k:78-90` return/pop | Replaced by direct integer result from target rules | Abrupt control bypassed |
| `Int` | `semantics/syntax.k:9`; `semantics/core.k:194` | literal becomes mathematical K `Int` | Target recurrence uses mathematical `Int` | Sound within supplied unbounded-integer model |
| `BinOp("+",...)`, `BinOp("-",...)` | `semantics/syntax.k:15` | sequential strictness, `semantics/operators.k:12`, `semantics/int.k:9,13` | Target recurrence directly uses `+Int`/`-Int` | Arithmetic recurrence agrees on valid inputs |
| `Compare` / `CmpOp(">=",...)` / `CmpOp("!="...)` | `semantics/syntax.k:30,32` | left-then-right contexts in `semantics/operators.k:15-17`; integer cases `semantics/int.k:25,27` | Target rules use integer guards and `==K` on list elements | Agrees for intended integer elements |
| `Subscript` | `semantics/syntax.k:22,38` | left-then-index contexts and heap dereference in `semantics/subscript.k:27-40`; `valSeqAt` at lines 11-14 | Target recurrence reads `valSeqAt` directly from the heap list | In-bounds under `targetValid`; avoids real AST evaluation |
| Builtin `len` | builtins binding `semantics/core.k:157-181` | lookup/call routing plus `semantics/builtins.k:20-26` | Main target rule uses `vsLen` directly | Result formula agrees, builtin execution bypassed |
| Input list heap object `ref(H) -> list(VS)` | `semantics/core.k:18,25-34,44-60` | fixed rules dereference at consumers | Correctness claim explicitly requires exactly this heap entry | Satisfiable but synthetic-entry-specific |

Relevant configuration cells are `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`,
`<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`
(`semantics/core.k:49-60`). The correctness claim frames all except `<k>` and
therefore proves them unchanged for `#targetCall`; it does not establish that a
real loaded closure reaches that synthetic entry while preserving them.

The proof imports `MPY`, not `MPY-KRUN`, so the concrete-only rules in
`semantics/concrete.k` are absent from the proof definition. The submitted
program does not use the concrete-only deep-list equality or keyed-sort rules.
