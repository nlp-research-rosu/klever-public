# Used-constructor and rule map

This map covers every constructor in the submitted `solution.mpy`. The complete
declaration/rule inventory, including modules unreachable from these
constructors, is `rule_inventory.tsv`.

| Submitted constructor/operation | Declaration | Rules on the reachable path | Audit disposition |
|---|---|---|---|
| `Module(Stmts)` and statement concatenation | `semantics/syntax.k:56,61` | `core.k:124-127` loads and sequences statements, with `.Stmts` as the unit | The entry claim starts from the mechanically identical closure binding instead of replaying module load; direct `FuncDef` below shows that this is inert. |
| `FuncDef("fizz_buzz", Params("n"), BODY)` | `syntax.k:53,57` | `functions.k:14-16` installs `closureVal("n",BODY,L)` in the current scope | Matches the entry's unique binding at defining environment `0`; constructor identity is machine checked. |
| `Call(Name("fizz_buzz"), Int(N))` | `syntax.k:9,12,28` | `call.k:20-21`, `core.k:130-154,186-197`, `call.k:69-74` | Looks up the exact binding, evaluates the sole argument left-to-right, allocates the callee frame, and schedules the exact body. No problem-local call interception exists. |
| Local parameter binding | `core.k:36-42`; `functions.k:8-11` | `functions.k:63-66` | Binds `"n"` to the evaluated integer in the new local scope. Cell-variable rules are guard-inapplicable because this is a plain closure/frame. |
| `Assign(Name(...), Expr)` | `syntax.k:41 [strict(2)]` | `controls.k:9-18` | RHS evaluates first; the plain-frame rule updates the current local map. Cell-write priority rule is guard-inapplicable. |
| `Name(...)` | `syntax.k:12` | `core.k:130-154` | All four locals are found in the exact current frame; parent lookup and cell dereference are guard-inapplicable. |
| `Int(...)` | `syntax.k:9` | `core.k:193` | Produces an unbounded K integer. |
| `While` and internal `#while` | `syntax.k:46`; `controls.k:65-67` | `controls.k:77-82,85` | Evaluates each guard, executes the body only when truthy, and restores the loop head through `#loopLbl`. |
| `If(..., then, .Stmts)` | `syntax.k:49` | `controls.k:51-54` | Evaluates the guard before selecting exactly one branch. The explicit `.Stmts` in the claim is the empty list unit accepted implicitly by the translated constructor. |
| `BoolOp("or", ...)` | `syntax.k:16` | `bool.k:16-25` | Evaluates the left comparison first and short-circuits when true; otherwise evaluates the right comparison. Both operands are Booleans here. |
| `Compare(..., CmpOp(...))` | `syntax.k:30,32` | `operators.k:15-17`; `int.k:22-27` | Evaluates left then right, dispatches integer `>`, `==`; no reference rules apply. |
| Integer `-`, `+`, `%`, `//` | `syntax.k:15 [seqstrict(2,3)]` | `operators.k:12`; `int.k:9-20` | Left-to-right evaluation; integer subtraction/addition; Python-style modulo and floor division. All divisors in the program are the positive constants 10, 11, and 13. |
| Boolean added to integer | same `BinOp("+",...)` declaration | `int.k:10-12` | Converts `true` to `1` and `false` to `0`, matching CPython's `bool` subclass behavior used by the source. |
| Truthiness of integer/Boolean guards | `core.k:199` | `core.k:200-202` | Booleans are themselves; integers are false iff zero. |
| `Return(Name("count"))` | `syntax.k:50 [strict]` | `functions.k:78-90` | Evaluates the return expression, records it, discards the remaining callee continuation as Python return does, pops only the callee frame, restores caller state, and exposes the value. |
| Proof summaries `digitResult`, `fizzResult` | `verification.k:7-8 [function]` | six simplification equations at `verification.k:18-54` | They do not match program AST/K control terms. Manual overlap, guard, value, and descent review is recorded in `REVIEW.md`. |
| Loop circularities | three claims at `spec.k:7,36,77` | fixed semantics plus the two loop claims | The inner and outer claims match the exact real loop heads and local map; the entry claim uses them only after fixed execution reaches those heads. |
