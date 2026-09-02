# Reviewer rule and declaration inventory

The inventory below is reconstructed from the regular source files copied to
`/tmp/audit-work/100-make-a-pile/source`. The mechanical declaration scan is
`logs/27-source-declaration-scan.log`.

## `semantic.k`: local syntax and configuration

| ID | Lines | Declaration / production | Used by submitted term | Assessment |
|---|---:|---|---|---|
| S01 | 6 | `PyModule ::= Module(Stmts)` | yes | Constructor for the translated file. |
| S02 | 8 | `Stmts ::= List{Stmt,""}` | yes | Juxtaposed statement list used for function and loop bodies. |
| S03 | 9 | `Strings ::= List{String,","}` | yes | One parameter (`"n"`). |
| S04 | 11 | `Stmt ::= FuncDef(String,Params(Strings),Stmts)` | yes | Sole submitted function. |
| S05 | 12 | `Stmt ::= Assign(Expr,Expr)` | yes | All assignments have `Name` on the left. |
| S06 | 13 | `Stmt ::= While(Expr,Stmts)` | yes | Submitted loop. |
| S07 | 14 | `Stmt ::= Return(Expr)` | yes | Submitted return. |
| S08 | 16 | `Expr ::= Name(String)` | yes | `n`, `i`, and `result`. |
| S09 | 17 | `Expr ::= Int(Int)` | yes | `0`, `1`, and `2`. |
| S10 | 18 | `Expr ::= ListExpr(Exprs)` | yes | Empty and singleton lists only. |
| S11 | 19 | `Expr ::= BinOp(String,Expr,Expr)` | yes | `+`, `-`, and `*`. |
| S12 | 20 | `Expr ::= Compare(Expr,CmpOp)` | yes | Loop guard. |
| S13 | 21 | `Exprs ::= List{Expr,","}` | yes | Empty and singleton forms. |
| S14 | 22 | `CmpOp ::= CmpOp(String,Expr)` | yes | `>=`. |
| S15–S18 | 31–34 | `Val ::= VInt | VBool | VList | VNone` | yes | Runtime value domain; `VNone` is the initial result only. |
| S19–S20 | 35–36 | `Vals ::= .Vals | VCons(Val,Vals)` | yes | Internal proper list. |
| S21 | 37 | `Expr ::= Val` | yes | Allows evaluated values in computation. |
| S22 | 39 | `KItem ::= exec(Stmts)` | yes | Statement-list continuation. |
| S23 | 40 | `KItem ::= assignTo(String)` | yes | Assignment continuation. |
| S24–S25 | 41–42 | `binLeft`, `binRight` | yes | Left-to-right binary evaluation. |
| S26–S27 | 43–44 | `makeList`, `listOne` | yes | Empty/singleton list evaluation. |
| S28–S29 | 45–46 | `compareLeft`, `compareApply` | yes | Left-to-right comparison. |
| S30 | 47 | `whileGuard` | yes | Loop guard continuation. |
| S31 | 48 | `finishReturn` | yes | Abrupt top-level return. |
| S32 | 50 | `vAppend(Vals,Vals) [function]` | yes | List concatenation. Not marked `total`; its two equations nevertheless cover both local `Vals` constructors. |
| S33 | 55 | `pileFrom(Int,Int) [function]` | proof/spec only | Mathematical suffix `[N+2I,...,N+2(N-1)]`. Not an operational program construct. |
| C01 | 61–67 | `<mpy><k>$PGM</k><n>$N</n><env>.Map</env><result>VNone</result></mpy>` | yes | Exactly the state needed by this sole top-level invocation. |

There are no local syntax priorities, `strict`/`seqstrict` attributes, `total`
attributes, `functional` attributes, or declared opaque symbols in
`semantic.k`.

## `semantic.k`: functions and operational rules

| ID | Lines | Rule | Classification and assessment |
|---|---:|---|---|
| R01 | 51 | `vAppend(.Vals,YS) => YS` | True base equation. |
| R02 | 52 | `vAppend(VCons(V,XS),YS) => VCons(V,vAppend(XS,YS))` | True structural equation; decreases the first list. R01/R02 are disjoint and exhaustive. |
| R03 | 56–57 | `pileFrom(N,I) => .Vals requires I >= N` | True base equation. |
| R04 | 58–59 | `pileFrom(N,I) => VCons(VInt(N+2*I),pileFrom(N,I+1)) requires I < N` | True recursive equation. The guard is disjoint from and exhaustive with R03 over `Int`; distance to `N` decreases. |
| R05 | 70–72 | Load sole one-argument `FuncDef`, bind parameter to `<n>`, execute body | Sound for the submitted one-function module. It intentionally ignores the function name and is not a general Python module/call semantics. |
| R06 | 74 | `exec(.Stmts) => .K` | Correct empty statement sequence. |
| R07 | 75 | `exec(S SS) => S ~> exec(SS)` | Correct left-to-right statement sequencing. |
| R08 | 77 | `Int(I) => VInt(I)` | Correct integer literal. |
| R09 | 78–79 | `Name(X) => V` from matching environment entry | Correct lookup for bound submitted names. Missing names stop visibly. |
| R10 | 81 | `ListExpr(ES) => makeList(ES)` | Evaluation setup. |
| R11 | 82 | `makeList(.Exprs) => VList(.Vals)` | Correct empty list. |
| R12 | 83 | Singleton `makeList(E,.Exprs) => E ~> listOne` | Correct and sufficient for the submitted singleton literal; larger literals are intentionally unsupported. |
| R13 | 84 | `V ~> listOne => VList(VCons(V,.Vals))` | Correct singleton result. |
| R14 | 86 | `BinOp(OP,E1,E2) => E1 ~> binLeft(OP,E2)` | Begins left operand first. |
| R15 | 87 | `V1 ~> binLeft(OP,E2) => E2 ~> binRight(OP,V1)` | Evaluates right operand after preserving the left value. |
| R16 | 88 | Integer `+` | Correct `L + R`. |
| R17 | 89 | Integer `-` | Correct `L - R`. |
| R18 | 90 | Integer `*` | Correct `L * R`. |
| R19 | 91 | List `+` | Correct ordered concatenation `vAppend(XS,YS)`. Typed patterns disambiguate it from R16. |
| R20 | 93 | Begin comparison with left operand | Correct order. |
| R21 | 94 | Preserve left comparison value and evaluate right | Correct order. |
| R22 | 95 | Integer `>=` | Correct `A >= B`. |
| R23 | 97 | `Assign(Name(X),E) => E ~> assignTo(X)` | Evaluates RHS before mutation. |
| R24 | 98–99 | Update environment at `X` | Correct local assignment; leaves other cells and continuation framed. |
| R25 | 101 | Evaluate `While` condition | Correct setup. |
| R26 | 102–103 | True guard executes body then repeats the identical loop | Correct iterative control and recurring loop head. |
| R27 | 104 | False guard consumes loop | Correct exit. |
| R28 | 106 | `Return(E) => E ~> finishReturn` | Evaluates the result expression. |
| R29 | 107–108 | Store return value and discard `_REST` | Correct abrupt return for this top-level function. The rule is broader than a general call-stack semantics, which the submitted program does not need. |

R05–R29 are ordinary semantic rules. None has an explicit priority or
simplification attribute. Their relevant typed left-hand sides are disjoint.
The imported `INT`, `BOOL`, `MAP`, generated-list, and K-sequencing operations
remain trusted primitives.

## `verification.k`: local declarations

| ID | Lines | Declaration | Assessment |
|---|---:|---|---|
| V01 | 9 | `evalExpr(Expr,Map) [function]` | Separate cell-free evaluator; partial outside the used subset. |
| V02 | 10 | `evalBin(String,Val,Val) [function]` | Separate typed binary evaluator. |
| V03 | 11 | `evalCmp(String,Val,Val) [function]` | Separate comparison evaluator. |
| V04–V05 | 29–30 | `Outcome ::= Normal(Map) | Returned(Map,Val)` | Big-step outcomes. |
| V06 | 31 | `evalStmts(Stmts,Map) [function]` | Separate statement evaluator. |
| V07 | 32 | `evalLoop(Expr,Stmts,Stmts,Map)` | Result-bearing opaque loop term: it has no execution equations. |
| V08 | 33 | `evalEntry(PyModule,Int) [function]` | Separate module-entry evaluator. |
| V09 | 34 | `proof(Outcome) [function]` | Proof-only wrapper; its only local equation is V16 below. |
| V10 | 35 | `goal(Proof)` | Uninterpreted outer wrapper used as the reachability term. |

No declaration is marked `total` or `functional`. There are no priorities.
V07 and V10 are opaque in behavior; V07 is result-bearing because V16 uses it
to determine the final returned value.

## `verification.k`: functions, bridge, and rules

| ID | Lines | Rule | Classification and assessment |
|---|---:|---|---|
| V-R01 | 13 | `evalExpr(Int(I),_)` | Correct duplicate of R08. |
| V-R02 | 14 | `evalExpr(Name(X),(X|->V) REST)` | Correct lookup on used maps. |
| V-R03 | 15 | Empty `ListExpr` | Correct duplicate of R11. |
| V-R04 | 16–17 | Singleton `ListExpr` | Correct for the used singleton form. |
| V-R05 | 18–19 | `BinOp` delegates to `evalBin` | Correct mathematical evaluation for pure submitted expressions. |
| V-R06 | 20–21 | `Compare` delegates to `evalCmp` | Correct mathematical evaluation. |
| V-R07–V-R10 | 23–26 | Integer `+`, `-`, `*`, and list `+` | Correct equations; typed cases are disjoint. |
| V-R11 | 27 | Integer `>=` | Correct equation. |
| V-R12 | 37 | Empty statements return `Normal` | Correct duplicate of R06. |
| V-R13 | 38–39 | Assignment updates map then evaluates rest | Correct for pure RHS expressions and submitted assignments. |
| V-R14 | 40–41 | Return ignores rest and returns evaluated expression | Correct for the submitted top-level body. |
| V-R15 | 42–43 | While becomes `evalLoop(COND,BODY,REST,ENV)` | This does not execute a loop; it hands control to opaque V07. |
| V-R16 | 47–65 | `[simplification] proof(evalLoop(exact target loop, exact trailing return, invariant state)) => proof(Returned(exact desired final state/value))` | **Illegitimate proof-local correctness axiom.** It is an operational/result bridge that bypasses R25–R27 and directly installs the task result. Its guard states the accumulator invariant, but no K theorem derives this equation. The initialization/preservation/exit claims are not premises or dependencies of this rule, and the loop claim is normalized by this same rule. The equation happens to describe the submitted loop correctly on the guarded domain, so the review does not claim a ground counterexample against the unmodified submitted program; the defect is the missing derivation and real-semantics connection. Logs 19–22 provide the required sensitivity witness: changing operational multiplication makes concrete `n=3` return `[5,6,7]`, while this bridge still proves the claimed `[3,5,7]` result with `#Top`. |
| V-R17 | 67–69 | `evalEntry` extracts any sole one-parameter function body and starts `evalStmts` | Correct within the separate evaluator, but there is no reachability theorem connecting it to R05 and the `<k>/<env>/<result>` configuration. |

V-R01–V-R15 and V-R17 are ordinary function equations. V-R16 is the only
local simplification rule. There are no other helper K files.

## `spec.k`: reachability claims

| ID | Lines | Claim | Static disposition |
|---|---:|---|---|
| Q01 | 6–16 | Initialization | Ground-true and symbolically reduced by the cell-free function equations; fresh run warns “proven without rewriting.” |
| Q02 | 18–33 | Preservation | Ground-true and reduced by equations for expressions, assignment, `pileFrom`, and `vAppend`; warns “proven without rewriting.” |
| Q03 | 35–47 | Exit | Ground-true and reduced by the cell-free return equation; warns “proven without rewriting.” |
| Q04 | 50–68 | Loop invariant/summary | Its left side is exactly consumed by V-R16. It therefore assumes, rather than derives, its own conclusion; warns “proven without rewriting.” |
| Q05 | 71–91 | Functional correctness | Contains the exact submitted AST, but under `evalEntry`, not in `<k>`. It reduces through V-R17/V-R13/V-R15 and then V-R16; warns “proven without rewriting.” |

## Submitted-construct coverage map

| Submitted constructor/operator | Parser declaration | Small-step rules | Proof-layer equations |
|---|---|---|---|
| `Module`, sole `FuncDef`, `Params("n")` | S01, S04, S03 | R05 | V-R17 |
| Statement sequence | S02 | R06–R07 | V-R12–V-R15 |
| `Assign(Name(...),...)` | S05, S08 | R23–R24 | V-R13 |
| `ListExpr()` and singleton `ListExpr(E)` | S10, S13 | R10–R13 | V-R03–V-R04 |
| `Name`, `Int` | S08–S09 | R08–R09 | V-R01–V-R02 |
| `BinOp("-",...)`, `BinOp("+",...)`, `BinOp("*",...)` | S11 | R14–R19 plus R01–R02 | V-R05, V-R07–V-R10 |
| `Compare(...,CmpOp(">=",0))` | S12, S14 | R20–R22 | V-R06, V-R11 |
| `While` | S06 | R25–R27 | V-R15 then opaque V07/V-R16 |
| `Return` | S07 | R28–R29 | V-R14 |

Thus the generated small-step semantics has minimal but complete coverage for
the submitted term. The proof layer does not use that coverage for the loop or
entry theorem.
