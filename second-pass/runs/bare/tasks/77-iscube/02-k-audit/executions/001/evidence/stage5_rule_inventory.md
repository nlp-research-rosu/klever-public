# Local K declaration and rule inventory

This inventory covers every local declaration and rule in `semantic.k` and
`verification.k`. There are no generated helper K files besides these sources
and `spec.k`; `spec.k` contributes six reachability claims but no ordinary or
simplification rules.

## `semantic.k`: syntax and configuration

| Lines | Declaration | Used by `solution.mpy` | Review |
|---|---|---:|---|
| 8 | `Pgm ::= Module(Stmts)` | yes | Exact outer translated constructor. |
| 11 | empty-separated `List{Stmt,""}` | yes | Matches translator juxtaposition and `.Stmts`; execution rules preserve order. |
| 13 | `Params(String)` | yes | Exact single-parameter constructor. |
| 15 | `Int(Int)` | yes | Literal expression. |
| 16 | `Name(String)` | yes | Variable reference and assignment target. |
| 17 | `UnaryOp(String,Expr) [strict(2)]` | yes | Operand evaluation; only `"-"` is used and modeled. |
| 18 | `BinOp(String,Expr,Expr) [strict(2,3)]` | yes | Both operands evaluate; only pure operands and `"+"`/`"*"` occur. `strict`, unlike `seqstrict`, does not itself guarantee Python left-to-right order, but all used operand evaluations are pure and total in reachable states, so the order difference is unobservable here. |
| 19 | `Compare(Expr,CmpOp) [strict(1)]` | yes | Evaluates the left operand before the explicit right-hand continuation. |
| 21 | `CmpOp(String,Expr)` | yes | Carries `<` and `==` right operands. |
| 23 | `FuncDef(String,Params,Stmts)` | yes | One translated definition. |
| 24 | `If(Expr,Stmts,Stmts)` | yes | Negative-input normalization. |
| 25 | `Assign(Expr,Expr)` | yes | All used targets are `Name`. |
| 26 | `While(Expr,Stmts)` | yes | Search loop. |
| 27 | `Return(Expr)` | yes | Final Boolean return. |
| 36–39 | `Value`, `IntVal`, `BoolVal`, `KResult`, and `Expr ::= Value` | yes | Values terminate strict evaluation and re-enter expression positions. |
| 41 | `function(String,Stmts)` | yes | Stores one parameter name and body. |
| 43–49 | `exec`, `invoke`, `assignTo`, `ifKont`, `whileKont`, `compareKont`, `returnKont` | yes | Internal continuations for sequential execution and the one-argument entry wrapper. No opaque symbol is present. |
| 51–57 | `<mpy>` configuration with `<k>`, `<funs>`, `<env>`, `<result>` | yes | Exactly the computation, function binding, local variables, and return value needed by this program. No heap, I/O, allocation, or exception cell is modeled because no submitted construct needs one. |

## `semantic.k`: operational rules

| ID / lines | Rule | Review |
|---|---|---|
| S1 / 60 | `Module(STMTS) => exec(STMTS)` | Faithful module-body scheduling. |
| S2 / 61 | `exec(.Stmts) => .K` | Faithful empty-list termination. |
| S3 / 62 | `exec(S REST) => S ~> exec(REST)` | Faithful sequential statement order. |
| S4 / 64–65 | load `FuncDef` into an empty function map | Faithful for the submitted single-definition module. Extra definitions deliberately remain unsupported. |
| S5 / 67–69 | `invoke(IntVal(A))` looks up `"iscube"`, installs its exact body, and initializes the one-argument environment | Faithful task entry wrapper. It reads the binding installed by S4 and does not fabricate a result. |
| S6 / 73 | `Int(I) => IntVal(I)` | Exact unbounded integer literal. |
| S7 / 74–75 | `Name(X) => V` from `<env>` | Exact bound-variable lookup; missing names visibly stick. |
| S8 / 77 | unary minus | Exact integer negation. |
| S9 / 78 | integer addition | Exact unbounded addition. |
| S10 / 79 | integer multiplication | Exact unbounded multiplication. |
| S11 / 81 | schedule comparison RHS after evaluated LHS | Preserves the program’s comparison dataflow. |
| S12 / 83 | integer `<` | Exact comparison. |
| S13 / 84 | integer `==` | Exact comparison. |
| S14 / 87 | assignment schedules RHS and remembers the name | Faithful for every submitted assignment. |
| S15 / 88–89 | update the environment with the resulting value | Exact local-state update. |
| S16 / 91 | schedule `if` condition and branch continuation | Exact conditional control. |
| S17 / 92 | true branch | Exact branch selection. |
| S18 / 93 | false branch | Exact branch selection. |
| S19 / 95 | schedule `while` condition and loop continuation | Exact loop-head control. |
| S20 / 96 | true guard executes body then repeats the same loop | Exact small-step loop iteration. |
| S21 / 97 | false guard exits | Exact loop exit. |
| S22 / 99 | schedule return expression | Exact return evaluation. |
| S23 / 100–101 | write the value to `<result>` and discard the remaining function continuation | Correct abrupt function return for this single-frame language; the complete `<k>` cell is matched and no unmodeled observable cell is discarded. |

The explicit rules have disjoint constructor or Boolean-value heads. Generated
strictness contexts apply only while their selected operands are not `KResult`,
so they do not compete with the value rules. Reachable lookups are bound:
`a` is installed by S5, and `n` is assigned before the loop.

## `verification.k`

| ID / lines | Declaration or rule | Class and review |
|---|---|---|
| V1 / 10–24 | `Pgm ::= iscubeProgram`; ordinary rule expanding it to the full constructor tree | Definitional syntax abbreviation. The tree matches `solution.mpy` exactly and then executes under S1–S23. It neither skips a body nor supplies a result. |
| V2 / 26 | `cube(Int) [function,total]` | Total mathematical helper over all K integers. |
| V3 / 27 | `cube(I) => I*I*I` | Single unguarded, terminating, exhaustive definition; exact integer cube. |
| G1 / 36–44 | guarded simplification `I < N+1 => true` | Valid derived lemma. If the conclusion were false, `I=N+1` by the guard `I<=N+1`; then `I^3=(N+1)^3>N^3+D`, contradicting the guard `I^3<N^3+D` and `D<(N+1)^3-N^3`. |
| G2 / 46–54 | guarded simplification `I == N+1 => true` | Valid derived lemma. If `I!=N+1`, integer order and `I<=N+1` give `I<=N`. Nonnegativity gives `I^3<=N^3<N^3+D`, contradicting `I^3>=N^3+D`. |

There are no priority rules, opaque symbols, `functional` declarations, other
`total` declarations, proof-local operational bridges, or answer-encoding
rules. G1 and G2 have different predicate heads; their guards and conclusions
are mathematically consistent. They help the prover establish loop indices but
do not rewrite the program, its state, or its returned Boolean.

## Construct-to-rule coverage

`Module` → S1; statement lists → S2–S3; `FuncDef`/`Params` and task invocation
→ S4–S5; `If` → S16–S18; `Compare`/`CmpOp("<",...)` → S11–S12;
`CmpOp("==",...)` → S11/S13; `Name` → S7; `Int` → S6; `Assign` → S14–S15;
`UnaryOp("-")` → S8; `While` → S19–S21; `BinOp("+")` → S9;
`BinOp("*")` → S10; `Return` → S22–S23. Every constructor in the submitted
`solution.mpy` therefore has both a declaration and applicable execution rule.
