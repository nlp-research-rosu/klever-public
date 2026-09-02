# Reviewer local K inventory

Inventoried source digests:

- `semantic.k`: `0dd7b3792eea2235fbd6d643aa1d5527f3cbe890f8575c515e2b8c45246f1b2d`
- `verification.k`: `5abfd379507b8b0e69ccfec2cdd23d81bba7c88a4fe2942c887f8136b6d9c112`
- `spec.k`: `b66e536e33cb3ed77e26d1a482e55b0286b8a44cbc956fb04dfa9f117fa6b5d7`

## Syntax, configuration, and attributes

| ID | Source | Complete local declaration | Audit |
|---|---|---|---|
| S01 | `semantic.k:5` | `Pgm ::= Module(Stmts)` | Represents the translated module. |
| S02 | `semantic.k:7` | `Stmts ::= List{Stmt, ""}` | Ordered statement sequence used by the body. |
| S03 | `semantic.k:8` | `Exprs ::= List{Expr, ","}` | Ordered tuple-expression sequence. |
| S04 | `semantic.k:9` | `Strings ::= List{String, ","}` | Runtime tuple payload. |
| S05 | `semantic.k:11` | `Params ::= Params(Strings)` | The actual term has one string parameter. |
| S06 | `semantic.k:13-15` | `Stmt ::= FuncDef(String,Params,Stmts) \| Assign(Expr,Expr) \| Return(Expr)` | Exactly the statement constructors used. |
| S07 | `semantic.k:17-22` | `Expr ::= Name(String) \| Int(Int) \| Str(String) \| TupleExpr(Exprs) \| BinOp(String,Expr,Expr) \| Subscript(Expr,Expr)` | Exactly the expression constructors used. |
| S08 | `semantic.k:33-35` | `Value ::= vInt(Int) \| vStr(String) \| vTuple(Strings)` | Runtime values needed by the program. |
| S09 | `semantic.k:36` | `KResult ::= Value` | Values are computations' terminal items. |
| S10 | `semantic.k:38` | `Result ::= noResult \| result(Value)` | Explicit external return cell. |
| C01 | `semantic.k:40-46` | `<mini-python>` containing `<k>`, `<input>`, `<env>`, and `<result>` | Every cell is read or written. Initial environment/result are empty/`noResult`. |
| S11 | `semantic.k:48-56` | `KItem ::= exec \| stmt \| eval \| assignTo \| binLeft \| binRight \| subscriptIndex \| subscriptApply \| returning` | Control frames make evaluation order explicit. |
| S12 | `semantic.k:58` | `Strings ::= tupleStrings(Exprs) [function]` | Semantic helper; not `total` or `functional`. |
| S13 | `semantic.k:62` | `String ::= tupleAt(Strings,Int) [function]` | Semantic helper; not `total` or `functional`. |
| S14 | `verification.k:6` | `Pgm ::= romanProgram [macro]` | Parse-time name for the exact submitted constructor term. |
| S15 | `verification.k:44` | `String ::= miniRoman(Int) [function]` | Definitional result summary; not `total` or `functional`. |

There are no local `[total]` declarations, explicit `[functional]`
declarations, opaque/uninterpreted declarations, priority rules, `owise` rules,
heating/cooling rules, anywhere rules, or local context declarations. The only
local rule attributes are `[simplification, concrete(I)]` on R03/R04 and
`[macro]` on S14.

## `semantic.k` rules

| ID | Lines | Complete role/domain | Class and state footprint | Soundness assessment |
|---|---:|---|---|---|
| R01 | 59 | `tupleStrings(.Exprs) => .Strings` | Definitional semantic helper; no cells. | True base equation. |
| R02 | 60 | `tupleStrings(Str(S), ES) => S, tupleStrings(ES)` | Definitional semantic helper; no cells. | True structural conversion for the actual all-string tuple literals; recursion descends the expression list. |
| R03 | 63-65 | `tupleAt(S, REST, I) => S` when `I == 0`, concrete simplification | Definitional semantic helper; no cells. | True zero-based lookup equation for a nonempty tuple. |
| R04 | 66-68 | `tupleAt(S, REST, I) => tupleAt(REST,I-1)` when `I > 0`, concrete simplification | Definitional semantic helper; no cells. | True recursive lookup; decreases a positive integer. R03/R04 guards are disjoint. The helper is deliberately partial for negative/out-of-range indexes. |
| R05 | 70-72 | A single-function module with one parameter starts `exec(BODY)`, binds that parameter to `<input>`, and changes an empty `<env>` to the singleton binding | Operational entry adapter; reads `<input>`, writes `<k>/<env>`, preserves `<result>`. | Exact for this submitted one-function entry module. Function name is irrelevant only because the generated semantics' entry convention invokes the sole translated function. |
| R06 | 74 | `exec(.Stmts) => .K` with continuation framed | Operational control; `<k>` only. | Correct empty-sequence behavior. |
| R07 | 75 | `exec(S SS) => stmt(S) ~> exec(SS)` with continuation framed | Operational control; `<k>` only. | Correct left-to-right statement sequencing. |
| R08 | 77 | Assignment to `Name(X)` evaluates the RHS then installs `assignTo(X)` | Operational control; `<k>` only. | Correct evaluation order for each actual assignment. |
| R09 | 78-79 | `V ~> assignTo(X)` removes the frame and updates `ENV[X]` | Operational state update; reads/writes `<env>`, advances `<k>`. | Correct binding update. |
| R10 | 81 | `stmt(Return(E)) ~> REST => eval(E) ~> returning`, discarding `REST` | Operational abrupt control; rewrites the entire `<k>` cell. | Correct for an entry-function return in this call-frame-free subset. The actual suffix is only remaining function-body execution. |
| R11 | 82-83 | `V ~> returning => .K`, `noResult => result(V)` | Operational return; writes `<k>/<result>`. | Correctly exposes the returned value. Exact `<k>` pattern prevents an additional continuation from being silently discarded here. |
| R12 | 85 | `eval(Int(I)) => vInt(I)` | Literal evaluation; `<k>` only. | True. |
| R13 | 86 | `eval(Str(S)) => vStr(S)` | Literal evaluation; `<k>` only. | True. |
| R14 | 87 | `eval(TupleExpr(ES)) => vTuple(tupleStrings(ES))` | Tuple evaluation; `<k>` only. | Exact for the actual tuple expressions, whose elements are all side-effect-free `Str` literals. Other element kinds are intentionally unmodeled. |
| R15 | 88-90 | `eval(Name(X)) => ENV[X]` when `X in_keys(ENV)` | Lookup; reads `<env>`, advances `<k>`. | Correct and guarded against missing bindings. |
| R16 | 92-93 | `eval(BinOp(OP,LEFT,RIGHT)) => eval(LEFT) ~> binLeft(OP,RIGHT)` | Evaluation-order frame; `<k>` only. | Preserves Python left-before-right order. |
| R17 | 94-95 | A computed left value causes evaluation of `RIGHT`, saved as `binRight(OP,LEFT)` | Evaluation-order frame; `<k>` only. | Preserves the left value and evaluates the right second. |
| R18 | 97-99 | Integer `I1 // I2` becomes K `I1 /Int I2`, guarded by nonzero `I2` | Trusted primitive bridge; `<k>` only. | On the actual domain `I1 >= 1` and positive divisors 10/100/1000, K integer division equals Python floor division. |
| R19 | 100-102 | Integer `I1 % I2` becomes K `I1 modInt I2`, guarded by nonzero `I2` | Trusted primitive bridge; `<k>` only. | On the actual nonnegative operands and positive divisors, K modulo equals Python modulo. |
| R20 | 103-104 | Integer `I1 + I2` becomes K `I1 +Int I2` | Trusted primitive bridge; `<k>` only. | Mathematically true; unused by this program. |
| R21 | 105-106 | String `S1 + S2` becomes K `S1 +String S2` | Trusted primitive bridge; `<k>` only. | Correct ordered concatenation and materially used. |
| R22 | 108-109 | A subscript evaluates `BASE` before `INDEX` | Evaluation-order frame; `<k>` only. | Matches Python evaluation order. |
| R23 | 110-111 | A computed base causes evaluation of `INDEX`, preserving the base | Evaluation-order frame; `<k>` only. | Correct. |
| R24 | 112-113 | Tuple plus integer index becomes `vStr(tupleAt(ITEMS,I))` | Result-bearing semantic abstraction; `<k>` only. | R03/R04 truthfully and terminatingly define every actual use: domain arithmetic gives the thousands index in 0..1 and all other indexes in 0..9. Negative indexing and IndexError behavior are outside the actual program/domain and remain unmodeled. |

## `verification.k` rules and `spec.k` claim

| ID | Lines | Complete role/domain | Class and footprint | Soundness assessment |
|---|---:|---|---|---|
| V01 | `verification.k:7-42` | `romanProgram` expands to the complete `Module(FuncDef(...))` constructor body | Syntax macro; no runtime cell effect. | Independent `kast` comparison against trusted regeneration is byte-identical after expansion. It is not an operational shortcut. |
| V02 | `verification.k:45-61` | For every K `Int N`, `miniRoman(N)` expands to the four digit-table lookups joined by `+String` | Definitional summary; no cells. | Direct abbreviation of the value computed by the fixed execution rules. The target precondition makes all lookups defined; it does not replace or preempt the program body. |
| Q01 | `spec.k:4-9` | From the initial cells and `1 <= N <= 1000`, executing `romanProgram` reaches `.K`, any final map, and exactly `result(vStr(miniRoman(N)))` | Sole positive reachability claim. | Satisfiable (for example `N=1`, `N=19`, or `N=1000`); result-constraining. No loop claims, auxiliary claims, circularities, or omitted result cell exist. |

## Constructor coverage

The submitted `solution.mpy` uses `Module`, `FuncDef`, `Params`, statement-list
concatenation, `Assign`, `Return`, `Name`, `Int`, `Str`, `TupleExpr`,
expression-list concatenation, `BinOp` with `"//"`, `"%"`, and `"+"`, and
`Subscript`. They map respectively to S01, S06, S05, S02, S06, S06, S07, S07,
S07, S07/S03, S07/R18-R21, and S07/R22-R24. All runtime control frames and all
four cells used by those rules are inventoried above.

No local rule encodes an arbitrary answer, fabricates a fresh value, bypasses
the body, or has overlapping contradictory equations. The proof depends on
the built-in K contracts for unbounded integers, strings, maps, list syntax,
and reachability reasoning; those imports are not locally redefined.
