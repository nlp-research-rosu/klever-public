# Used constructor and semantics map

This map is reviewer-authored. Line numbers refer to the trusted scratch copy at
`/tmp/audit-work/candidate-src/reference-semantics/`; candidate and trusted
semantics were already proved byte-identical.

| Submitted constructor/effect | Declaration | Rules that execute it | Review |
|---|---|---|---|
| `Module(Stmts)` | `semantics/syntax.k:61` | `semantics/core.k:124-127` (`#loadAll`, left-to-right statement sequencing) | The whole submitted module is loaded; no body is skipped. |
| `FuncDef`, `Params` | `semantics/syntax.k:53,57` | `semantics/functions.k:14-16` | Binds a closure containing the exact body and defining scope. |
| `Assign(Name, Expr)` | `semantics/syntax.k:41` (strict RHS) | `semantics/controls.k:9-11` | Evaluates RHS before updating the current scope. |
| `Name` | `semantics/syntax.k:12` | `semantics/core.k:130-154` | Starts at `<env>` and walks parents; the proof pins the selected function binding and locals. |
| `ListExpr` and allocation | `semantics/syntax.k:17` | `semantics/list.k:13-15`; `semantics/core.k:117-121` | Evaluates elements left-to-right and allocates a fresh heap object. |
| `Float` literal | `semantics/syntax.k:10`; `semantics/float.k:20` | `semantics/float.k:21` | Produces the supplied K `Float`; literal parsing is trusted. |
| `For` / list iteration | `semantics/syntax.k:45` | `semantics/controls.k:65-74`; `semantics/list.k:9-10` | Evaluates iterable once, consumes one `vCons` per iteration, binds the head, executes the body, and continues with the tail. |
| `If` | `semantics/syntax.k:49` (strict condition) | `semantics/controls.k:51-54` | Exactly one branch executes after `truthy`; comparison results are `Bool`. |
| `Compare` / `CmpOp` | `semantics/syntax.k:30,32` | evaluation contexts `semantics/operators.k:14-17`; numeric equations `semantics/float.k:43,125-150,195-206`; proof-local derived twins `verification.k:84-91` | Left then right evaluation; the two proof simplifications agree constructor-by-constructor with fixed Int/Float cases. |
| `Expr(Call(...))` | `semantics/syntax.k:28-29,52` | call routing `semantics/call.k:15-24`; discard `semantics/controls.k:46-48` | Receiver and arguments are evaluated before dispatch; the returned `noneV` from `append` is discarded. |
| list `.append` | method value at `semantics/call.k:16,24` | `semantics/list.k:52-55` | Mutates only the heap list at the receiver reference and appends exactly one value. |
| `Str` | `semantics/syntax.k:13` | `semantics/str.k:13-17` | Converts the submitted ASCII grade literals to exact code sequences. |
| `Return` and frame pop | `semantics/syntax.k:50` | `semantics/functions.k:77-90` | Sets `retV`, discards the remaining callee continuation, returns the value to the saved caller continuation, restores caller environment, and pops the callee scope. |
| call frame and parameter binding | `semantics/call.k:69-75`; `semantics/functions.k:62-66` | same | Creates the callee frame with the defining scope as parent, pushes the saved continuation, and binds `grades` to the evaluated argument. |
| `ValSeq` append used in postcondition | `semantics/list.k:18-20` | proof-local `gradeAcc` at `verification.k:137-143` | Both functions structurally recurse on finite constructor sequences; no heap/control rule is replaced. |

Configuration cells are declared at `semantics/core.k:49-60`. The entry claim
pins `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`, `<heapLoc>`,
`<stack>`, `<ret>`, `<exc>`, and `<exit-code>`. The loop claim additionally
frames all unmentioned cells and preserves the continuation following `#loop`.

