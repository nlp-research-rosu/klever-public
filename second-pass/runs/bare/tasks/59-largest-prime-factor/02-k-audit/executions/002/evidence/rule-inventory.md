# Exhaustive local rule and declaration inventory

Line references below are to the immutable candidate files. Imported K
built-ins (`INT`, `BOOL`, `MAP`) are listed separately as trusted primitives;
there are no other candidate-local helper K files.

## `semantic.k`

### Syntax, attributes, and configuration

| ID | Lines | Declaration | Attributes / role |
|---|---:|---|---|
| D1 | 5 | `PyModule ::= Module(Stmts)` | Submitted module constructor |
| D2 | 6 | `Stmts ::= List{Stmt, ""}` | Juxtaposed statement sequence |
| D3 | 7 | `Strings ::= List{String, ","}` | Parameter-name sequence |
| D4 | 8 | `Params ::= Params(Strings)` | Parameter constructor |
| D5 | 10–14 | `Stmt ::= FuncDef \| Assign \| While \| If \| Return` | Five statement constructors |
| D6 | 16–19 | `Expr ::= Int \| Name \| BinOp \| Compare` | Four expression constructors |
| D7 | 20 | `CmpOps ::= List{CmpOp, ","}` | Comparison-operation sequence |
| D8 | 21 | `CmpOp ::= CmpOp(String, Expr)` | Comparison constructor |
| D9 | 30 | `Result ::= noResult \| result(Int)` | Result cell values |
| D10 | 32–38 | `<py><k><input><env><result>` | All four child cells are read by rules or claims |
| D11 | 42 | `evalInt(Expr, Map):Int` | `[function]`, not `total` |
| D12 | 52 | `evalBool(Expr, Map):Bool` | `[function]`, not `total` |
| D13 | 58–60 | `exec(Stmts)`, `execStmt(Stmt)`, `setVar(String,Int)` | Internal `KItem`s |

There are no `total`, `functional`, `simplification`, `priority`, `owise`,
`concrete`, or opaque declarations.

### Function and semantic rules

| ID | Lines | Rule / complete match domain | Review |
|---|---:|---|---|
| S1 | 43 | `evalInt(Int(I), _) => I` | Truthful literal projection. |
| S2 | 44 | `evalInt(Name(X), X |-> I _M) => I` | Truthful lookup when the map contains the unique key `X`; every submitted lookup is bound. |
| S3 | 45 | `evalInt(BinOp("+",A,B),M)` | K unbounded integer addition matches positive-domain Python addition. |
| S4 | 46 | `evalInt(BinOp("*",A,B),M)` | K unbounded integer multiplication matches Python here. |
| S5 | 47–48 | `evalInt(BinOp("//",A,B),M)` when divisor is nonzero | K `/Int` agrees with Python `//` for the reachable positive operands; zero is visibly stuck. |
| S6 | 49–50 | `evalInt(BinOp("%",A,B),M)` when divisor is nonzero | K `%Int` agrees with Python `%` for the reachable positive operands; zero is visibly stuck. |
| S7 | 53–54 | one-element `Compare` with `<=` | Truthful for the integer operands used by the loop guard. |
| S8 | 55–56 | one-element `Compare` with `==` | Truthful for the integer operands used by the divisibility guard. |
| S9 | 63–66 | exact one-function `largest_prime_factor(n)` module, empty env | Entry-harness bridge: binds the supplied `<input>` integer to `n` and executes the exact body. It does not summarize or replace any body operation. It is intentionally not general Python module/call semantics. |
| S10 | 68 | `exec(.Stmts) => .K` | Correct sequence base case. |
| S11 | 69 | `exec(S SS) => execStmt(S) ~> exec(SS)` | Correct left-to-right statement sequencing. |
| S12 | 71–72 | assignment to `Name(X)` under env `M` | Computes the RHS from the old map before update; submitted RHSs are pure. |
| S13 | 73–74 | `setVar(X,I)` | Correct local-map overwrite. |
| S14 | 76–78 | `If` when `evalBool` is true | Selects only the then body. |
| S15 | 79–81 | `If` when `evalBool` is false | Selects only the else body. S14/S15 guards are disjoint and exhaustive when the submitted condition evaluates. |
| S16 | 83–86 | `While` when true | Executes the body and rechecks the same loop. |
| S17 | 87–89 | `While` when false | Consumes the loop. S16/S17 guards are disjoint and exhaustive when the submitted condition evaluates. |
| S18 | 91–93 | `Return(E)` with `noResult` | Sets the result from the current env. It does not discard a nonempty continuation, so it is faithful only when return is last. The submitted body and helper claim use exactly that reachable context. |

S18 is an off-path language-model limitation, not a shortcut used by this
proof. `return-followed.mpy` and `return-followed.log` preserve a witness:
with contract-valid input 4, a synthetic function containing `return 1`
followed by `return 2` gets stuck after setting `result(1)`, whereas Python
terminates immediately. No such suffix occurs in `solution.mpy`.

## `verification.k`

| ID | Lines | Declaration or rule | Class and review |
|---|---:|---|---|
| V-D1 | 9 | `lpfSpec(Int,Int):Int [function]` | Partial definitional summary; neither opaque nor `total`. |
| V1 | 10–11 | `lpfSpec(N,F) => N` if `F*F > N` | Base equation matching loop exit. |
| V2 | 12–13 | `lpfSpec(N,F) => lpfSpec(N/F,F)` if `F*F <= N` and `N%F==0` | Divisible transition matching the real loop body. |
| V3 | 14–15 | `lpfSpec(N,F) => lpfSpec(N,F+1)` if `F*F <= N` and `N%F!=0` | Nondivisible transition matching the real loop body. |
| V-D2 / M1 | 19–27 | `factorLoop [macro]` and its macro rule | Compile-time constructor alias, not an operational bridge. |
| V-D3 / M2 | 29–35 | `solutionModule [macro]` and its macro rule | Compile-time constructor alias, not an operational bridge. |

V1–V3 are pairwise disjoint. On every claimed state (`N > 1`, `F >= 2`)
they cover the loop guard and its two branches; recursive calls preserve those
conditions. Divisible steps strictly reduce positive `N`; nondivisible steps
increase `F` until the base guard holds. These equations truthfully define the
residual trial-division computation. They do not themselves prove the separate
number-theoretic proposition that the result is the largest prime factor.

There are no proof-local ordinary operational rules, priorities,
simplification rules, total/functional attributes, fresh/opaque symbols, or
oracles.

## `spec.k`

There are four reachability claims and no local syntax, functions, ordinary
rules, priorities, simplifications, or opaque symbols:

| Claim | Lines | Role |
|---|---:|---|
| `loop-refines-lpf` | 8–17 | Circular loop refinement over all `N > 1`, `F >= 2`. |
| `largest-prime-factor-correct` | 21–29 | Entry execution equals `lpfSpec(N,2)` for every `N > 1`. |
| `prompt-example-13195` | 31–37 | Fixed result 29. |
| `prompt-example-2048` | 39–45 | Fixed result 2. |

## Submitted-constructor coverage

| Submitted constructor/operator | Declaration | Behavior |
|---|---|---|
| `Module`, exact `FuncDef`, `Params` | D1, D4, D5 | S9 |
| statement list | D2 | S10–S11 |
| `Assign(Name, ...)` | D5–D6 | S12–S13 |
| `While` | D5 | S16–S17 |
| `If` | D5 | S14–S15 |
| last-position `Return(Name("n"))` | D5–D6 | S18 in its faithful reachable context |
| `Int`, `Name` | D6 | S1–S2 |
| `BinOp("+")`, `BinOp("*")`, `BinOp("//")`, `BinOp("%")` | D6 | S3–S6 |
| `Compare`/`CmpOp("<=")` | D6–D8 | S7 |
| `Compare`/`CmpOp("==")` | D6–D8 | S8 |

The submitted function has no calls, heap objects, I/O, exceptions, break,
continue, nested functions, globals, or observable allocation, so no semantic
rule for those constructs is required by the generated-semantics boundary.
