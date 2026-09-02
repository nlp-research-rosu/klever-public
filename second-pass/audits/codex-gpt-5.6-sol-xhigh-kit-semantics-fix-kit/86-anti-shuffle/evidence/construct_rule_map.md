# Construct and proof-extension map

The exhaustive machine-readable inventory is `k_inventory.tsv` (1,125 rows,
including all 707 local rules and all 230 local `syntax` declarations). This
file records the reachable construct slice and the proof-local judgment.

## Constructs in `solution.mpy`

| Submitted construct | Declaration | Rules on the reachable path | Judgment |
|---|---|---|---|
| `Module`, `Stmts` | `syntax.k:56,61` | `core.k:124-127` loads and sequences statements left-to-right | Fixed supplied semantics; adequate here. |
| `FuncDef`, `Params` | `syntax.k:53,57` | `functions.k:14-16` installs exact closures in the current scope | Fixed supplied semantics; exact bodies are retained. |
| `Name` | `syntax.k:12` | `core.k:130-154` performs lexical scope-chain lookup | Fixed supplied semantics; call binding is pinned by the entry/module scopes. |
| `Assign` | `syntax.k:41` (`strict(2)`) | `controls.k:9-18` evaluates RHS then updates the current local scope | Fixed supplied semantics; no heap/cell branch is reachable for this program. |
| `Str` | `syntax.k:13` | `str.k:13-17` turns ASCII literals into `str(IntSeq)` | Exact literals are `""`, `" "`, and proof-test `"x"`, all ASCII. Symbolic input is already `str(CODES)`. |
| `Int` | `syntax.k:9` | `core.k:193-196` evaluates the slice bound `1` | Fixed supplied semantics. |
| `BinOp("+",...)` | `syntax.k:15` (`seqstrict(2,3)`) | `operators.k:12`; `str.k:20-24` uses structurally recursive `seqConcat` | Left-to-right evaluation and string concatenation are faithful on the target path. |
| `Compare`/`CmpOp` | `syntax.k:30,32` | `operators.k:15-17`; `str.k:25-26,48-59` | Equality and singleton lexicographic `<` are complete and disjoint for the used strings. |
| `If` | `syntax.k:49` (`strict(1)`) | `controls.k:50-54` | Exactly one branch is selected by the computed Boolean. |
| `For` | `syntax.k:45` (`strict(2)`) | `controls.k:65,69-74`; `str.k:8-10`; `tuple.k:30-41` | Iterable is evaluated once; string iteration yields one-character strings; `Name` target updates the local. |
| `Call` | `syntax.k:28` | `call.k:19-21,69-75`; `core.k:183-191`; `functions.k:63-75` | Callee then arguments evaluate left-to-right; exact closure is selected; a fresh local frame is allocated and parameters bind. |
| `Return` | `syntax.k:50` (`strict`) | `functions.k:77-90` | Sets `ret`, discards the remainder of the current continuation, restores caller state, deletes the local frame, and returns the value. This continuation-discard behavior exposes both bridge bugs. |
| `Subscript`/`Slice`/`NoBound` | `syntax.k:22,38-39` | `subscript.k:43-121`; `core.k:227-229` | For used `suffix[1:]`, bound evaluation, positive-step clamping, and `buildIS` produce the tail. |

The full configuration is `core.k:49-60`: `k`, `env`, `scopes`, `scopeLoc`,
`heap`, `heapLoc`, `stack`, `ret`, `exc`, and `exit-code`. The submitted
program allocates call scopes but no heap objects. Calls and returns modify
`env`, `scopes`, `scopeLoc`, `stack`, and `ret`; all other cells are preserved.

## Proof-local extensions

| Extension | Attributes/class | Static judgment |
|---|---|---|
| Guarded map deletion, `verification.k:9-11` | simplification / derived lemma | Sound: with `I` absent from `REST`, deleting the unique `I` binding yields `REST`. |
| Tail slice, `verification.k:16-22` | simplification / derived lemma | Sound: for length `n+1`, `[1:]` starts and stops at valid bounds and structurally returns `REST`, including the `n=0` boundary. |
| `insertFinish`, `verification.k:26-37` | function,total; three simplifications | Sound definition: empty/nonempty are constructor-disjoint; `<` and `not <` are disjoint/exhaustive; recursion strictly shortens the suffix. |
| `antiFinish`, `verification.k:41-54` | function,total; three simplifications | Sound definition: empty, head 32, and head not 32 cover all cases without overlap; recursion strictly shortens `REM`. |
| `asciiCodes`, `verification.k:56-59` | function,total; two ordinary equations | Sound domain predicate, constructor-complete and descending. |
| Helper bridge, `verification.k:69-103` | priority(40) operational rule | **Unsound.** It matches only the loop and replaces it by `Return(summary)` while framing any continuation. Empty-loop witness: fixed semantics continues to `return "x"` and returns code 120; the bridge discards that continuation and returns code 97. |
| Outer bridge, `verification.k:111-143` | priority(40) operational rule | **Unsound.** Same defect. Empty-loop witness: fixed semantics continues to `return "x"`; the bridge prematurely returns empty. |

There are no proof-local opaque, `functional`, or `concrete` declarations.
The two priority-40 bridge rules preempt the fixed priority-50 `#loop` rule.
The lower-layer reachability claims prove loops only together with their exact
real trailing `Return(... ) ~> #endcall`; they do not prove equivalence for the
arbitrary continuations admitted by the bridges.

## Concrete bridge witnesses

| Check | Fixed semantics | Bridge theory | Evidence |
|---|---:|---:|---|
| Helper false result `"a"` when continuation returns `"x"` | Rejected; residual is `"x"` | `#Top` | `32_helper_bridge_false_concrete_proves.log`, `33_helper_base_false_concrete_rejects.log` |
| Helper true result `"x"` | `#Top` | — | `34b_helper_base_true_concrete_proves.log` |
| Outer false result empty when continuation returns `"x"` | Rejected; residual is `"x"` | `#Top` | `35_outer_bridge_false_concrete_proves.log`, `36_outer_base_false_concrete_rejects.log` |
| Outer true result `"x"` | `#Top` | — | `37_outer_base_true_concrete_proves.log` |
| Exact final-return body mutated to `return "x"` while original target retained | LLVM/Python execute the mutation and return `"x"` on empty input | Entry proof still returns `#Top` | `38_final_return_mutation_generation.log` through `41_final_return_body_mutation_still_proves.log` |
