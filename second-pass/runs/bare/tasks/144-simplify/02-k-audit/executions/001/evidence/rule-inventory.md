# Reviewer rule and declaration inventory

Sources audited: the scratch copies of `semantic.k`, `verification.k`, and
`spec.k`. There are no generated helper K files.

## Imports and configuration

- `MPY-SYNTAX` imports `INT` and `STRING`.
- `SEMANTIC` imports `MPY-SYNTAX`, `BOOL`, and `MAP`.
- `VERIFICATION` imports `SEMANTIC`.
- `SPEC` imports `VERIFICATION`.
- The only configuration is `<simplify>` with four cells: `<k>` initially
  contains `$PGM:Module ~> invoke("simplify", $ARGS:PyVals)`;
  `<functions>` and `<env>` initially contain `.Map`; `<result>` initially
  contains `noResult`. Every cell is used.

## Local syntax declarations

1. `ParamList ::= List{String, ","}`: comma-separated formal names.
2. `Params ::= Params(ParamList)`: formal-parameter wrapper.
3. `Expr` source constructors:
   `Name(String)`, `Int(Int)`, `Str(String)`, `Attribute(Expr,String)`,
   `Call(Expr,Expr)`, `Subscript(Expr,Expr)`,
   `BinOp(String,Expr,Expr)`, and `Compare(Expr,CmpOp)`.
4. `CmpOp ::= CmpOp(String,Expr)`: one comparison operator and RHS.
5. `Stmt` source constructors:
   `FuncDef(String,Params,Stmts)`, `Assign(Expr,Expr)`, and `Return(Expr)`.
6. `Stmts ::= List{Stmt, ""}`: juxtaposed statement list.
7. `Module ::= Module(Stmts)`: source module.
8. `PyVal` runtime constructors:
   `intVal(Int)`, `boolVal(Bool)`, `strVal(String)`,
   `pairList(PyVal,PyVal)`, `builtinInt`, `splitMethod(PyVal)`, and
   `slashSplit(String)`.
9. `Int ::= decimalValue(String)`.
10. `Expr ::= PyVal`: runtime values inject into expressions.
11. `PyVals ::= List{PyVal, ","}`: comma-separated invocation values.
12. `Function ::= function(Params,Stmts)`: stored function body.
13. `Result ::= noResult | result(PyVal)`: observable return cell.
14. `KItem` control constructors:
    `exec(Stmts)`, `invoke(String,PyVals)`, `bind(String)`,
    `finishReturn`, `getAttribute(String)`, `callWith(Expr)`,
    `apply(PyVal)`, `indexWith(Expr)`, `indexApply(PyVal)`,
    `binRight(String,Expr)`, `binApply(String,PyVal)`,
    `compareRight(String,Expr)`, and `compareApply(String,PyVal)`.
15. `Module ::= simplifyProgram` in `VERIFICATION`: a closed abbreviation for
    the submitted translated module.

Declarations 1–15 are recognizable encodings of exactly the submitted AST and
its required runtime/control data. Unsupported Python constructs remain
unparseable or stuck. `pairList` deliberately models only the two components
needed from a valid one-slash fraction.

## Function, totality, priority, and opacity inventory

- `slashSplit(String)` is local `[function]`; it has one base equation guarded
  by finding a slash and marked `[owise]`, plus one proof-local
  `[simplification]` specialization.
- `decimalValue(String)` is local `[function]`; it has one base `[owise]`
  equation and one proof-local `[simplification]` specialization.
- There are no local `[total]` declarations, `[functional]` declarations,
  fresh variables, opaque/uninterpreted result symbols, hooks, macros, or
  explicit `priority(N)` attributes.
- The only local priority-like attributes are the two `[owise]` base equations.
  The three proof rules carrying `[simplification]` are equations trusted by
  symbolic rewriting.
- Imported `INT`, `STRING`, `BOOL`, and `MAP` hooks are external primitives.
  Result-bearing imported hooks used here are `Int2String`, `String2Int`,
  `+String`, `findString`, `substrString`, and `lengthString`; integer
  multiplication, modulo, comparison, and map lookup/update are also trusted.

## Ordinary semantic rules

| ID | Source | Complete role/domain | Static decision |
|---|---|---|---|
| S01 | `semantic.k:66` | `Module(SS) => exec(SS)` in the current continuation. | Sound module-entry step. |
| S02 | `semantic.k:67` | `exec(.Stmts) => .K`. | Sound empty-sequence termination. |
| S03 | `semantic.k:68` | `exec(S SS) => S ~> exec(SS)`. | Sound left-to-right statement scheduling. |
| S04 | `semantic.k:70-71` | Store `function(PS,BODY)` at name `F`, consume the definition. | Sound for the single top-level definition; map update is the only state effect. |
| S05 | `semantic.k:73-75` | Invoke a stored exactly-two-parameter function; reset the local environment to its two argument bindings and schedule its body. | Sound for exact `simplify(x,n)` invocation. It intentionally omits general call stacks/defaults/aliasing, none used. |
| S06 | `semantic.k:77` | `Assign(Name(X),E)` evaluates `E` before `bind(X)`. | Sound for every submitted assignment target. |
| S07 | `semantic.k:78-79` | Bind a completed `PyVal` into `env`. | Sound map update and assignment completion. |
| S08 | `semantic.k:81` | `Return(E)` evaluates `E` before `finishReturn`. | Sound return-expression order. |
| S09 | `semantic.k:82-83` | A returned `PyVal` discards `_REST`, empties `<k>`, and writes `result(V)`. | Sound for this top-level-only invocation: `_REST` is only the function-body tail/empty continuation. The rule is broader than a general Python call-stack model, but no intended input reaches a caller continuation. |
| S10 | `semantic.k:85` | `Int(I) => intVal(I)`. | Sound integer-literal evaluation. |
| S11 | `semantic.k:86` | `Str(S) => strVal(S)`. | Sound string-literal evaluation. |
| S12 | `semantic.k:87` | `Name("int") => builtinInt`. | Sound for the unshadowed builtin in the submitted body; broader Python shadowing is unmodeled but unreachable here. |
| S13 | `semantic.k:88-89` | Look up `Name(X)` in `<env>`. | Sound lexical-local lookup for this body. It does not overlap S12 on reachable states because the exact environment never binds `"int"`. |
| S14 | `semantic.k:91` | Evaluate attribute receiver before `getAttribute(A)`. | Sound Python receiver-before-call order. |
| S15 | `semantic.k:92` | Completed receiver plus `"split"` becomes `splitMethod(V)`. | Sound method binding for the submitted string receivers; non-string receivers later get stuck. |
| S16 | `semantic.k:94` | Evaluate call callee before `callWith(E)`. | Sound one-argument call order. |
| S17 | `semantic.k:95` | After callee, evaluate the argument before `apply(V)`. | Sound one-argument call order and binding of the evaluated callee value. |
| S18 | `semantic.k:96-97` | Applying `splitMethod(strVal(S))` to `strVal("/")` yields `slashSplit(S)`. | Sound for the exact calls. No state/control is skipped. |
| S19 | `semantic.k:98-103` | If a slash exists, split at its first index into a `pairList`; `[owise]`. | Sound for every intended fraction string, which contains one slash and two nonempty positive-decimal components. It is not a general model of Python `split`: `"1/2/3"` would need three elements; that input is outside the intended domain and produces `#Bottom` here. This is an excluded over-broad-domain limitation, not an intended-domain false-conclusion witness. |
| S20 | `semantic.k:104` | Apply `builtinInt` to `strVal(S)`, producing `intVal(decimalValue(S))`. | Sound builtin-call bridge for valid decimal components. |
| S21 | `semantic.k:105` | `decimalValue(S) => String2Int(S)`; `[owise]`. | Sound on the intended nonempty positive-decimal strings. Invalid Python integer strings are intentionally outside coverage. |
| S22 | `semantic.k:107` | Evaluate subscript base before its index. | Sound Python evaluation order. |
| S23 | `semantic.k:108` | After the base is a value, evaluate the index before indexing. | Sound Python evaluation order. |
| S24 | `semantic.k:109` | Index `0` of `pairList(V0,_)` is `V0`. | Sound for `x_parts[0]` and `n_parts[0]`. |
| S25 | `semantic.k:110` | Index `1` of `pairList(_,V1)` is `V1`. | Sound for `x_parts[1]` and `n_parts[1]`. |
| S26 | `semantic.k:112` | Evaluate binary LHS before `binRight(OP,R)`. | Sound left-to-right operand order. |
| S27 | `semantic.k:113` | After LHS value, evaluate RHS before `binApply(OP,V)`. | Sound left-to-right operand order; saved `V` is the LHS. |
| S28 | `semantic.k:114` | `intVal(B) ~> binApply("*",intVal(A)) => intVal(A *Int B)`. | Sound unbounded-integer multiplication; operand naming preserves `A * B`. |
| S29 | `semantic.k:115-116` | Positive/negative integers use `A %Int B` when `B != 0`. | Sound for intended positive divisor `B*D`; the guard models the zero-divisor error by getting stuck. |
| S30 | `semantic.k:118` | Evaluate comparison LHS before `compareRight(OP,R)`. | Sound comparison order. |
| S31 | `semantic.k:119` | After LHS value, evaluate RHS before `compareApply(OP,V)`. | Sound comparison order; saved `V` is the LHS. |
| S32 | `semantic.k:120-121` | Integer equality yields `boolVal(A ==Int B)`. | Sound for the submitted single `==` comparison. |

## Verification rules

| ID | Source | Class and complete domain | Static decision |
|---|---|---|---|
| V01 | `verification.k:7-31` | Ordinary definitional abbreviation: `simplifyProgram` rewrites to a closed `Module(...)` term. | Sound. The whitespace-insensitive token stream is identical to the trusted-translator output for `solution.py`; no body is skipped or summarized. |
| V02 | `verification.k:36-38` | Result-bearing simplification of `slashSplit(Int2String(A) +String "/" +String Int2String(B))` for all K integers `A,B`. | Mathematically sound conditional on imported string-hook contracts: integer strings contain only optional `-` plus digits, hence no slash; the concatenation has exactly one separator and S19 returns the two original strings. It preempts the `[owise]` base equation. Ground positive and negative/zero checks close and full base/extended program states agree. A bridge-free universal K claim remains stuck because symbolic string hooks are opaque, so the universal connection is an explicit informal/trusted-builtin boundary. |
| V03 | `verification.k:39` | Result-bearing simplification `decimalValue(Int2String(I)) => I` for all K integers. | Sound conditional on the imported inverse conversion contract and S21. It overlaps S21 only through `[owise]`; the RHSs agree after V04. Ground negative check closes. The bridge-free universal claim remains symbolically stuck. |
| V04 | `verification.k:40` | Result-bearing simplification `String2Int(Int2String(I)) => I` for all K integers. | Sound inverse law for K’s fixed decimal conversion hooks. The installed K contract defines these representations, and ground negative testing closes. It is not task-answer encoding, but the Haskell backend cannot prove the universal inverse without this equation, so the law is a named external primitive assumption. |

The three simplifications have disjoint top symbols except that V03 can feed
V04. V03 and the base S21 overlap only because S21 is `[owise]`, and both paths
agree under V04. V02 and base S19 likewise overlap only through S19’s `[owise]`.
There are no conflicting simplification RHSs, recursive definitions, or
uncovered uses on the formal claim domain.

## Claims

1. `SPEC.simplify-general`: for canonical positive decimal strings
   `A/B` and `C/D`, the exact program terminates with
   `boolVal(((A*C) % (B*D)) == 0)`. The postcondition fixes the returned value;
   only final internal maps are existential.
2. `SPEC.example-true`: exact program on `"1/5","5/1"` returns `true`.
3. `SPEC.example-false-one`: exact program on `"1/6","2/1"` returns `false`.
4. `SPEC.example-false-two`: exact program on `"7/10","10/2"` returns `false`.

There are no helper, loop, circularity, or auxiliary claims.

## Used-construct coverage map

- `Module`/`FuncDef`/`Params`/statement sequencing: S01–S05.
- `Assign(Name,Expr)`: S06–S07.
- `Return`: S08–S09.
- `Name`, `Int`, `Str`: S10–S13.
- `Attribute(...,"split")` and `Call`: S14–S21.
- `Subscript` at `0` and `1`: S22–S25.
- `BinOp("*",...)` and `BinOp("%",...)`: S26–S29.
- `Compare(...,CmpOp("==",...))`: S30–S32.
- Function/result/environment/configuration state: configuration plus
  S04–S09.

Every submitted constructor has a declaration, an evaluation-order path, and a
terminal behavior on the formal positive canonical-decimal domain.
