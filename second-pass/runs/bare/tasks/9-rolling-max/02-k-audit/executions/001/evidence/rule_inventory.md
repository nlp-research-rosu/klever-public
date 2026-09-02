# Exhaustive local K inventory

Line references are to the read-only files in `/candidate`.

## Syntax, configuration, and attributes

| Source | Declaration | Attribute/class | Audit |
|---|---|---|---|
| `semantic.k:10-11` | `Program ::= Module \| Run(Module,[Ints])` | syntax | Covers translated modules and the concrete harness. |
| `semantic.k:13` | `Module ::= Module(Stmts)` | syntax | Matches translator output. |
| `semantic.k:15` | `Stmts ::= List{Stmt,""}` | syntax | Ordered statement blocks. |
| `semantic.k:16-22` | `Stmt ::= ImportFrom \| FuncDef \| Assign \| For \| If \| Expr \| Return` | syntax | Exactly the statement constructors used by `solution.mpy`; some constructors accept a broader unused subset. |
| `semantic.k:24` | `Strings ::= List{String,","}` | syntax | Used for imports and parameters. |
| `semantic.k:25` | `Params ::= Params(Strings)` | syntax | Used by the single-argument function. |
| `semantic.k:26` | `Ints ::= List{Int,","}` | syntax | Concrete `Run` input. |
| `semantic.k:28-34` | `Expr ::= Name \| Int \| Bool \| ListExpr \| Compare \| Call \| Attribute` | syntax | Exactly the expression constructors used by `solution.mpy`; execution rules intentionally cover only the used arities/forms. |
| `semantic.k:36` | `Exprs ::= List{Expr,","}` | syntax | Argument/list literal sequences. |
| `semantic.k:37` | `CmpOp ::= CmpOp(String,Expr)` | syntax | The program uses only `">"`. |
| `semantic.k:38` | `CmpOps ::= List{CmpOp,","}` | syntax | The program uses exactly one comparison operation. |
| `semantic.k:41` | `Val ::= IntVal \| BoolVal \| ListVal \| NoneVal` | runtime syntax | All values exercised by the program. |
| `semantic.k:42` | `Expr ::= Val` | subsort syntax | Lets evaluated values occupy expression positions. |
| `semantic.k:44` | `Function ::= Function(Params,Stmts)` | runtime syntax | Function map payload. |
| `semantic.k:45` | `Frame ::= Frame(Map)` | runtime syntax | Saved caller environment. |
| `semantic.k:47-59` | `KItem ::= Invoke \| CallKont \| EndCall \| Cleanup \| Store \| Discard \| Branch \| CompareRight \| GreaterThan \| AppendTo \| StartLoop \| Loop \| Bind` | continuation syntax | Every continuation has a corresponding rule below. |
| `semantic.k:61` | `List ::= intsToList(Ints)` | `[function,total]` | Equations 1-3 are disjoint, exhaustive on `Ints`, and structurally recursive. |
| `semantic.k:72-78` | `<py><k/><functions/><env/><stack/></py>` | configuration | Minimal state used by module loading, calls, variables, and the one call frame. |
| `solution-ast.k:8` | `Program ::= OpRunList(Module,List)` | syntax | Operational proof harness. |
| `solution-ast.k:13` | `Stmts ::= ROLLING-LOOP` | `[macro]` | Exact loop-body constructor transcription. |
| `solution-ast.k:23` | `Stmts ::= ROLLING-BODY` | `[macro]` | Exact function-body constructor transcription. |
| `solution-ast.k:31` | `Module ::= SOLUTION` | `[macro]` | Normalized KAST is byte-identical to normalized submitted `solution.mpy` KAST; see `stage4_solution_macro_identity.log`. |
| `solution-ast.k:38` | `List ::= #rollingMax(List)` | `[function]`, not total | Complete for lists whose items are integers; structurally recursive. |
| `solution-ast.k:39` | `List ::= #scanMax(Int,List)` | `[function]`, not total | Complete for integer-item lists; structurally recursive. |
| `verification.k:8` | `Program ::= VerifyRunList(Module,List)` | syntax | Symbolic proof harness. |
| `verification.k:28` | loop-summary rule priority | `[priority(40)]` | Causes the proof bridge to preempt the ordinary `For` rule; priority changes selection, not truth. |

There are no local `[functional]`, `[simplification]`, `[concrete]`, or opaque
declarations. The only local `[total]` declaration is `intsToList`. The three
macros and three function symbols are listed above.

## Rule-by-rule inventory

| No. | Source | Rule/role | Class and assessment |
|---:|---|---|---|
| 1 | `semantic.k:81` | `intsToList(.Ints) => .List` | Function equation; true empty case. |
| 2 | `semantic.k:82` | singleton `intsToList(I)` | Function equation; true singleton case. |
| 3 | `semantic.k:83` | recursive `intsToList(I,IS)` | Function equation; true cons case and descending recursion. |
| 4 | `semantic.k:85` | `Run` loads module, invokes `rolling_max`, then cleans up | Ordinary harness rule; correct for the submitted entry point. |
| 5 | `semantic.k:86` | `Module(SS) => SS` | Ordinary sequencing rule; correct. |
| 6 | `semantic.k:87` | statement-list head sequencing | Ordinary sequencing rule; preserves order. |
| 7 | `semantic.k:88` | empty statement block | Ordinary sequencing rule; correct. |
| 8 | `semantic.k:89` | preserve a value before trailing empty statements | Ordinary sequencing rule; needed for the final return; correct on the used control shape. |
| 9 | `semantic.k:91` | discard `ImportFrom` | Ordinary rule; acceptable for the used `typing` import, whose bindings are never read. It is intentionally not general Python import semantics. |
| 10 | `semantic.k:92-93` | store `FuncDef` in `<functions>` | Ordinary state rule; correct for the used definition. |
| 11 | `semantic.k:96` | evaluate the sole argument of `Call(Name(...))` | Ordinary call rule; correct left-to-right behavior for the used one-argument call. |
| 12 | `semantic.k:97` | turn evaluated argument into `Invoke` | Ordinary call-continuation rule; correct. |
| 13 | `semantic.k:98-101` | enter one-argument function with fresh local env and saved caller | Ordinary control/state rule; correct for the only non-nested invocation. Nested calls are deliberately unsupported. |
| 14 | `semantic.k:102-104` | return value and restore caller env/frame | Ordinary control/state rule; correct for the used single frame. |
| 15 | `semantic.k:106-107` | retain returned value and clear functions at harness cleanup | Ordinary harness rule; correct. |
| 16 | `semantic.k:110` | integer literal | Ordinary expression rule; correct. |
| 17 | `semantic.k:111` | Boolean literal | Ordinary expression rule; correct. |
| 18 | `semantic.k:112` | empty list literal | Ordinary expression rule; correct for the only used list literal. Nonempty `ListExpr` is syntactically admitted but unused and intentionally unmodeled. |
| 19 | `semantic.k:113` | name lookup in `<env>` | Ordinary state read; correct. |
| 20 | `semantic.k:116` | evaluate assignment RHS then `Store` | Ordinary evaluation-order rule; correct for name targets. |
| 21 | `semantic.k:117-118` | update name binding | Ordinary state write; correct. |
| 22 | `semantic.k:119` | `Return(E) => E` | Correct on the submitted body's trailing return. Over-broad for unused Python code with a following statement because it does not abruptly discard the continuation; no such context occurs in `solution.mpy`. |
| 23 | `semantic.k:120` | evaluate expression statement then discard | Ordinary evaluation-order rule; correct. |
| 24 | `semantic.k:121` | discard expression value | Ordinary control rule; correct. |
| 25 | `semantic.k:124` | evaluate left side of the sole `>` comparison | Ordinary evaluation-order rule; correct for the used comparison shape. |
| 26 | `semantic.k:125` | evaluate comparison right side after the left | Ordinary evaluation-order rule; correct. |
| 27 | `semantic.k:126` | integer greater-than result | Ordinary expression rule; true (`I >Int J` for source `I > J`). |
| 28 | `semantic.k:129` | evaluate `If` guard then branch | Ordinary evaluation-order rule; correct. |
| 29 | `semantic.k:130` | true branch | Ordinary control rule; correct. |
| 30 | `semantic.k:131` | false branch | Ordinary control rule; correct. |
| 31 | `semantic.k:134` | evaluate sole argument to named-list `.append` | Ordinary evaluation-order rule; correct for the used receiver/arity. |
| 32 | `semantic.k:135-136` | append integer, return `NoneVal`, mutate named list binding | Ordinary state rule; correct for the used unaliased integer list. |
| 33 | `semantic.k:139` | evaluate `for` iterable | Ordinary evaluation-order rule; correct. |
| 34 | `semantic.k:140` | start loop over evaluated `ListVal` | Ordinary control rule; correct. |
| 35 | `semantic.k:141` | empty loop terminates | Ordinary control rule; correct. |
| 36 | `semantic.k:142` | bind list head, execute body, recurse on tail | Ordinary control rule; correct order for integer-item lists. |
| 37 | `semantic.k:143-144` | loop-variable binding | Ordinary state rule; correct. |
| 38 | `solution-ast.k:9-10` | `OpRunList` harness | Ordinary harness rule; equivalent to `Run` with a value-level input list. |
| 39 | `solution-ast.k:14-21` | expand `ROLLING-LOOP` | Macro equation; exact constructor transcription of the submitted loop. |
| 40 | `solution-ast.k:24-29` | expand `ROLLING-BODY` | Macro equation; exact constructor transcription of the submitted body. |
| 41 | `solution-ast.k:32-34` | expand `SOLUTION` | Macro equation; exact normalized KAST match to submitted `solution.mpy`. |
| 42 | `solution-ast.k:41` | `#rollingMax(.List)` | Mathematical function equation; true. |
| 43 | `solution-ast.k:42` | emit head then scan tail | Mathematical function equation; true definition of prefix maxima. |
| 44 | `solution-ast.k:44` | empty `#scanMax` | Mathematical function equation; true. |
| 45 | `solution-ast.k:45-47` | new item greater than carried max | Mathematical function equation; true. |
| 46 | `solution-ast.k:48-50` | new item not greater than carried max | Mathematical function equation; true; guard is disjoint from and exhaustive with rule 45 for integers. |
| 47 | `verification.k:9-10` | `VerifyRunList` harness | Ordinary harness rule; same behavior as `OpRunList`. |
| 48 | `verification.k:17-28` | replace the entire real `For` loop with `#rollingMax(XS)` and delete three local bindings | **Illegitimate operational bridge.** It has no universal connection claim; it directly assumes the result-bearing loop theorem. Its exact-map RHS is also false for fixed execution: for `[2,1]`, fixed execution retains `first=false`, `maximum=2`, and `number=1` (`stage5_bridge_true_footprint_operational.log`, `#Top`), while this rule deletes them. Its `<k> ...` accepts arbitrary continuations. `stage5_bridge_false_footprint_verification.log` proves the bridge-fabricated false footprint (`#Top`), while the same claim under fixed rules fails in `stage5_bridge_false_footprint_operational.log`. With the observable suffix `Name("first")`, fixed execution proves `BoolVal(false)` (`stage5_bridge_continuation_operational.log`) but the bridge preempts it, deletes `first`, and gets stuck (`stage5_bridge_continuation_verification.log`). |

## Construct coverage map for `solution.mpy`

| Submitted construct | Declaration and execution rules |
|---|---|
| `Module` and statement order | syntax `semantic.k:10,13,15-22`; rules 5-8 |
| `ImportFrom("typing",...)` | syntax `semantic.k:16`; rule 9 |
| `FuncDef`, `Params`, entry invocation/call frame | syntax `semantic.k:17,24-25,44-45,47-50`; rules 10-15 and harness rule 4/38/47 |
| `Assign(Name,...)` | syntax `semantic.k:18,28`; rules 19-21 |
| `ListExpr()` | syntax `semantic.k:31,36`; rule 18 |
| `Bool`, `Int`, and `Name` | syntax `semantic.k:28-30,41-42`; rules 16-19 |
| `For(Name,Name,body)` | syntax `semantic.k:19,57-59`; rules 33-37 (but target proof preempts them with rule 48) |
| `If` | syntax `semantic.k:20,53`; rules 28-30 |
| `Compare(...,">",...)` | syntax `semantic.k:32,37-38,54-55`; rules 25-27 |
| `result.append(maximum)` and expression discard | syntax `semantic.k:21,33-34,36,52,56`; rules 23-24 and 31-32 |
| trailing `Return(Name("result"))` | syntax `semantic.k:22`; rule 22 followed by rule 8 and call-return rule 14 |
