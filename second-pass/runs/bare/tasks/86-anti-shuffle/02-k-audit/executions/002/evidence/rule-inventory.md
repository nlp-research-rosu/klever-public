# Exhaustive local K inventory

Source line references are to the immutable candidate files copied unchanged to
`/tmp/audit-work/anti-shuffle/`.

## `semantic.k`: syntax, attributes, and configuration

| ID | Lines | Declaration | Attributes / role |
|---|---:|---|---|
| S01 | 5 | `Pgm ::= Module(Stmts)` | Submitted module root. |
| S02 | 7 | `Stmts ::= List{Stmt,""}` | Associative statement-list production and generated `.Stmts` unit. |
| S03 | 9–11 | `Stmt ::= FuncDef \| Return \| If` | All three submitted statement forms. |
| S04 | 13–14 | `Params ::= Params(String) \| Params(String,String,String)` | One- and three-parameter functions. |
| S05 | 16–23 | `Expr ::= Name \| Str \| Int \| BinOp \| Compare \| Subscript \| Call/1 \| Call/3` | Every submitted expression form. |
| S06 | 25 | `CmpOp ::= CmpOp(String,Expr)` | Comparison operator/value pair. |
| S07 | 26–27 | `Index ::= Expr \| Slice(Expr,NoBound,NoBound)` | Integer index and open-ended slice. |
| S08 | 34–35 | `StrVals ::= vals(String) \| vals(String,String,String)` | Evaluated argument tuples. |
| S09 | 37 | `Function ::= fun(Params,Stmts)` | Function binding value. |
| S10 | 38 | `findFun(String,Stmts) : Function` | `[function]`; intentionally partial when no definition exists. |
| S11 | 39 | `bindParams(Params,StrVals) : Map` | `[function,total]`; declared total although mismatched arities have no equation. |
| S12 | 40 | `appendStmts(Stmts,Stmts) : Stmts` | `[function]`; equations cover the list constructors. |
| S13 | 53–72 | 20 `KItem` productions | `run`, `invoke`, `invokeFound`, `exec`, `eval`, `val`, `boolVal`, `restore`, `returnValue`, `ifKont`, `plusLeft`, `plusRight`, `indexKont`, `sliceKont`, `compareLeft`, `compareRight`, `callOne`, `callSecond`, `callThird`, and `callInvoke`. These are explicit continuation-machine states, not opaque result symbols. |
| S14 | 74–80 | `<python>` configuration | `<k>` starts at `run($PGM,$INPUT)`; functions and environment start empty; result starts `""`. |

There are no local `functional`, `simplification`, `concrete`, `owise`,
priority, or anywhere declarations. There are no result-bearing opaque symbols.

## `semantic.k`: every local rule

| ID | Lines | Rule / decision |
|---|---:|---|
| R01 | 42 | `findFun` returns the first same-name definition. Sound for the submitted unique-name function list. |
| R02 | 43–44 | `findFun` skips a different name. Guard is disjoint from R01. |
| R03 | 46 | Bind one parameter to one string. Sound. |
| R04 | 47–48 | Bind three parameters to three strings. Sound for distinct submitted parameter names. |
| R05 | 50 | Append to the empty statement list. Sound list equation. |
| R06 | 51 | Preserve a head statement while recursively appending. Sound and structurally decreasing. |
| R07 | 82–83 | `run(Module(FS),INPUT)` loads `FS` and invokes `anti_shuffle`. Sound for a module containing only the three function definitions. |
| R08 | 85–86 | Resolve an invocation through `findFun`. Sound on the three reachable names. |
| R09 | 87–88 | Enter a function body, save the old environment, and bind evaluated arguments. Sound for the submitted local-only functions. |
| R10 | 89–90 | On a returned `val`, restore the caller environment. Sound. |
| R11 | 92 | Execute `Return(E)` by evaluating `E` and discard the remaining body. Correct return control. |
| R12 | 93 | Remove `returnValue` after expression evaluation. Sound. |
| R13 | 94–96 | Evaluate an `If` guard before choosing a branch. Sound order. |
| R14 | 97–100 | True guard executes `THEN` followed by the original remainder. Sound. |
| R15 | 101–104 | False guard executes `ELSE` followed by the original remainder. Disjoint/exhaustive with R14 on `Bool`. |
| R16 | 106 | Evaluate a string literal. Sound. |
| R17 | 107–108 | Look up a string-valued local name. Sound on reachable environments. |
| R18 | 110 | Start left-to-right string addition. Sound for used `+`. |
| R19 | 111 | After the left operand, evaluate the right operand. Sound. |
| R20 | 112 | Concatenate the two strings with `+String`. Sound Python-string abstraction subject to the K String trust boundary. |
| R21 | 114 | Evaluate the receiver before integer subscripting. Sound order. |
| R22 | 115 | Model `S[I]` as `substrString(S,I,I+1)`. Sound only for valid indices; all submitted reachable indices are zero after a nonempty check. |
| R23 | 116–118 | Evaluate the receiver before an open-ended slice. Sound order. |
| R24 | 119–121 | Model `S[I:]` as `substrString(S,I,lengthString(S))`. Sound on the used nonnegative `I=1`. |
| R25 | 123–125 | Evaluate a comparison's left operand first. Sound. |
| R26 | 126–128 | Evaluate the comparison's right operand second. Sound. |
| R27 | 129 | String `==` uses `==String`. Sound on the selected K String interpretation. |
| R28 | 130 | String `<=` uses `<=String`. Sound on the selected K String interpretation. |
| R29 | 132 | For a one-argument named call, evaluate the argument first. Sound. |
| R30 | 133 | Invoke the named one-argument function with its evaluated value. Sound for the statically unshadowed submitted calls. |
| R31 | 134–136 | Begin a three-argument call with argument 1. Sound Python left-to-right order. |
| R32 | 137–139 | After argument 1, evaluate argument 2. Sound. |
| R33 | 140–142 | After argument 2, evaluate argument 3. Sound. |
| R34 | 143–145 | Invoke with the three evaluated arguments. Sound. |
| R35 | 147–148 | Only when `val(V)` is the entire computation, store `V` in `<result>` and finish. Sound normal-return finalization. |

R08–R10 model calls with unbounded semantic stack depth and no exception state.
That is observably different from the submitted CPython program on the
1100-character witness in `21-long-input-semantics.log`: K returns normally
while CPython raises `RecursionError`.

## `verification.k`: declarations and every rule

| ID | Lines | Declaration / equation | Classification and decision |
|---|---:|---|---|
| V01 | 8, 10 | `solutionProgram [function,total] => Module(solutionFunctions)` | Definitional program constant; zero-argument domain is completely covered. |
| V02 | 9, 11–52 | `solutionFunctions [function,total] =>` the three constructor bodies | Definitional program constant; mechanical AST comparison with `solution.mpy` succeeds. |
| V03 | 56, 58–59 | `refInsert(C,WORD,BEFORE)` when `WORD==""` | Definitional result summary; base case. |
| V04 | 60–63 | `refInsert` when nonempty and `C<=head` | Definitional result summary; insertion case. |
| V05 | 64–69 | `refInsert` when nonempty and not `C<=head` | Definitional result summary; recurses on a one-shorter `WORD`. V03–V05 are disjoint and exhaustive. |
| V06 | 73, 76–77 | `refProcess(TEXT,WORD,RESULT)` when `TEXT==""` | Definitional result summary; base case. |
| V07 | 78–84 | `refProcess` on a leading ASCII space | Preserves the delimiter, closes the current word, and recurses on shorter `TEXT`. |
| V08 | 85–91 | `refProcess` on a non-space leading character | Inserts the character into the current word and recurses on shorter `TEXT`. V06–V08 are disjoint and exhaustive. |
| V09 | 74, 93 | `antiShuffleSpec(S) [function,total] => refProcess(S,"","")` | Completely covered definitional wrapper. |

There are no operational bridge rules in `verification.k`: none rewrites a
program `invoke`, `eval`, `exec`, call, or continuation to a summary. There are
no simplification, priority, concrete, `owise`, or opaque declarations. The
result-bearing `refInsert` and `refProcess` symbols are connected to exact fixed
execution by the separately reconstructed C01 and C02 claims.

## `spec.k`: every claim

| ID | Lines | Claim |
|---|---:|---|
| C01 | 6–15 | `insert-correct`: exact `insert_char(C,W,B)` invocation returns `refInsert(C,W,B)`, restoring any caller environment and preserving an arbitrary continuation. |
| C02 | 18–27 | `process-correct`: exact `process_words(T,W,R)` invocation returns `refProcess(T,W,R)` with the same framing. |
| C03 | 30–36 | `universal-correct`: for every K `String` `S`, running the exact program from empty initial cells finishes with `antiShuffleSpec(S)`. |
| C04 | 39–45 | `"Hi"` returns `"Hi"`. |
| C05 | 47–53 | `"hello"` returns `"ehllo"`. |
| C06 | 55–61 | `"Hello World!!!"` returns `"Hello !!!Wdlor"`. |
| C07 | 63–69 | `"  ba  dc "` returns `"  ab  cd "`. |

C01 closes without trusted claims. C02 closes using independently closed C01.
C03–C07 close using independently closed C01 and C02. No candidate claim is
accepted only because it was marked trusted in the same unverified batch.
