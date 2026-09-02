# Source-level K inventory and static disposition

This inventory covers every local declaration in the submitted
`semantic.k`, `verification.k`, and `spec.k`. Imported K builtins are recorded
separately as trust boundaries; generated compiler rules are not
candidate-authored extensions.

## `semantic.k`: syntax and configuration

| Lines | Declaration | Submitted-program use | Disposition |
|---|---|---|---|
| 6 | `Program ::= Module(Stmts)` | Top-level translated term | Exact constructor coverage. |
| 8 | `Stmts ::= List{Stmt,""}` | Function, loop, and branch bodies | Empty and cons/list forms are both used. |
| 9 | `Strings ::= List{String,","}` | `Params("n")` | Only the singleton form is used. |
| 10 | `Exprs ::= List{Expr,","}` | Empty and singleton `ListExpr` | Both used arities are modeled. |
| 12 | `Params(Strings)` | One parameter, `"n"` | Matched as one `String` by the module-entry rule. |
| 14–18 | `Stmt`: `FuncDef`, `Assign`, `While`, `If`, `Return` | All five occur | Every submitted statement constructor is declared. |
| 20–24 | `Expr`: `Int`, `Name`, `ListExpr`, `BinOp`, `Compare` | All five occur | Every submitted expression constructor is declared. |
| 26 | `CmpOp(String,Expr)` | `<=` and `==` | Both used operators have semantic rules. |
| 37–39 | `Value`: integer, Boolean, list | All three occur dynamically | Adequate for the candidate's operations. |
| 41 | `Result`: `noResult`, `done(Value)` | Function return | Makes completion and returned value observable. |
| 43–49 | `<py>` configuration with `<k>`, `<input>`, `<env>`, `<result>` | Entire execution | No unused cell; immutable integer/list values need no heap or alias cell for this program. |
| 51–61 | Control items `exec`, `eval`, `store`, `singleton`, binary/comparison frames, branch frames, `doReturn` | Entire execution | Explicit continuations implement the candidate's evaluation order and control. |

There are no local `function`, `total`, `functional`, `opaque`, priority,
`simplification`, or `anywhere` declarations in `semantic.k`.

## `semantic.k`: every ordinary rule

| ID / lines | Rule | Complete local role and disposition |
|---|---|---|
| S1 / 63–65 | `Module(FuncDef(... Params(P:String), BODY))` initializes `P` from `<input>` and starts `BODY` | Benchmark entry convention for the exact submitted one-function/one-parameter module. It ignores the function-name token but does not replace the body: `BODY` is executed. Exact candidate binding is mechanically pinned by expanded-term identity. |
| S2 / 67 | `exec(.Stmts) => .K` | Correct empty statement-sequence completion. |
| S3 / 68 | `exec(S REST) => S ~> exec(REST)` | Correct left-to-right statement sequencing. |
| S4 / 70 | assignment to `Name(X)` evaluates RHS then stores | Exact target form used by all submitted assignments. |
| S5 / 71–72 | value/store updates `ENV[X]` | Correct local-binding update; frames `<k>` suffix and all other cells. |
| S6 / 74 | `If` evaluates its condition first | Correct evaluation order. |
| S7 / 75 | true branch selects `THEN` | Correct Boolean control. |
| S8 / 76 | false branch selects `ELSE` | Correct Boolean control; disjoint from S7. |
| S9 / 78 | `While` evaluates its condition first | Correct loop-head behavior. |
| S10 / 79–80 | true loop guard executes body then the same loop | Correct sequencing and stable recurring loop-head configuration. |
| S11 / 81 | false loop guard exits | Correct loop termination; disjoint from S10. |
| S12 / 83 | `Return(E)` evaluates `E` then schedules return | Correct return-expression evaluation order. |
| S13 / 84–85 | a value at `doReturn` discards the active suffix and writes `done(V)` | Correct abrupt return for the actual context, where the suffix is `exec(.Stmts)`. It preserves input/environment cells and records the exact value. The candidate has no cleanup, exception, or caller frame that this could mishandle. |
| S14 / 87 | integer literal evaluates to `intVal` | Exact Python/K arbitrary-precision integer literal behavior. |
| S15 / 88–89 | name lookup reads its unique map binding | Correct for every submitted read, all of which are initialized before use. |
| S16 / 91 | empty list literal gives `.List` | Exact used empty-list form. |
| S17 / 92 | singleton list evaluates its element first | Exact used nonempty-list form and evaluation order. |
| S18 / 93 | singleton integer becomes `ListItem(I)` | Exact for all submitted list elements, which are integers. |
| S19 / 95 | binary operation evaluates left first | Matches Python's left-to-right operand order. |
| S20 / 96 | after left value, evaluates right and retains left | Matches Python's operand order. |
| S21 / 97 | integer `+` | Exact on arbitrary-precision integers. |
| S22 / 98 | integer `*` | Exact on arbitrary-precision integers. |
| S23 / 99 | integer `%` | Exact on the used domain: loop index is positive and divisor is `2`. No claim is made for unused negative-divisor behavior. |
| S24 / 100 | list `+` concatenates K lists | Same returned sequence as Python concatenation. Fresh-object identity is unobservable: the program has no aliasing or identity operation. |
| S25 / 102–103 | comparison evaluates left first | Correct order. |
| S26 / 104 | after left value, evaluates right and retains left | Correct order. |
| S27 / 105 | integer `<=` | Exact used loop guard. |
| S28 / 106 | integer `==` | Exact used parity comparison. |

S7/S8, S10/S11, the type-specific S21–S24 rules, and S27/S28 have
disjoint constructor/operator domains. No priority is needed. Each material
operation in `solution.mpy` follows these rules; no answer-producing shortcut
or oracle rewrites an `exec`, `eval`, `While`, or program-defined body.

## `verification.k`: declarations

| Lines | Declaration / attributes | Use and disposition |
|---|---|---|
| 6 | `mathFactorial(Int):Int [function]` | Truthful partial mathematical function; unused by either reachability postcondition. No `total` declaration. |
| 7 | `mathTriangle(Int):Int [function]` | Truthful partial mathematical function; unused by either reachability postcondition. No `total` declaration. |
| 8 | `expectedAt(Int):Int [function]` | Truthful parity dispatcher for positive indices; unused by either reachability postcondition. No `total` declaration. |
| 9 | `expected(Int):List [function]` | Result-bearing postcondition summary for `N >= 0`. Fully defined over every claim use. |
| 10 | `expectedCompletion(Int,Int,Int,Int,List):List [function]` | Result-bearing loop summary. Its three guards cover every integer `I,N` pair and recurse by increasing `I` until `I>N`. |
| 44 | `solution:Program [macro]` | Compile-time syntax shorthand, not an opaque runtime value or operational bridge. Expanded KORE equals trusted regenerated `solution.mpy`. |
| 45 | `solutionLoop:Stmt [macro]` | Compile-time syntax shorthand for the exact submitted loop. |

There are five `[function]` declarations. There are no `[total]`,
`[functional]`, `opaque`, priority, `simplification`, or `anywhere`
declarations. There are no local trusted primitives.

## `verification.k`: every function/macro rule

| ID / lines | Rule | Guard/overlap/descent/value disposition |
|---|---|---|
| V1 / 12 | `mathFactorial(0) => 1` | Correct base case. |
| V2 / 13–14 | positive factorial recursion | Guard disjoint from V1; argument descends by one. Partial only for negative inputs, which are neither declared total nor used. |
| V3 / 16 | `mathTriangle(0) => 0` | Correct base case. |
| V4 / 17–18 | positive triangular recursion | Guard disjoint from V3; argument descends by one. Partial only for unused negative inputs. |
| V5 / 20–21 | positive even `expectedAt` selects factorial | Correct and disjoint from V6. |
| V6 / 22–23 | positive odd `expectedAt` selects triangular sum | `%=0` versus `%!=0` partitions positive integers. |
| V7 / 28–29 | `expected(N)` initializes completion at `I=1,F=1,T=0,L=[]` for `N>=0` | Exactly the main program's initialization and full claimed domain. |
| V8 / 31–32 | completion returns `L` when `I>N` | Correct zero-remaining-iteration case; disjoint from V9/V10. |
| V9 / 33–37 | at even `I<=N`, update both accumulators and append `F*I` | Correct next even element; guard is disjoint from V10; `I` increases. |
| V10 / 38–42 | at odd `I<=N`, update both accumulators and append `T+I` | Correct next odd element; guard is disjoint from V9; `I` increases. |
| V11 / 47–60 | expands `solutionLoop` | Exact source loop. Constructor-level comparison and body mutation establish sensitivity; it does not remain as a runtime rewrite after macro expansion. |
| V12 / 62–70 | expands `solution` | Exact source function binding/body. Constructor-level comparison establishes identity; it does not summarize execution. |

V8–V10 cover all integers because exactly one of `I>N` or `I<=N` holds,
and parity equality/inequality partitions the latter case. Thus the only
result-bearing summary used by claims is fully equationally fixed; there is no
fresh or unconstrained result-bearing symbol. V1–V6 are dead with respect to
claim closure and cannot smuggle a conclusion into the proof.

## `spec.k`: claims

| ID / lines | Claim | Disposition |
|---|---|---|
| C1 / 6–26 | `loop-invariant` | Auxiliary all-path reachability circularity over the exact `solutionLoop ~> exec(Return(...))` continuation, complete five-binding environment, and `noResult`. For `N>=0,I>=1`, it constrains both the environment's `result` and the `<result>` cell to the same fully defined `expectedCompletion`. It allows arbitrary `F,T,L`, which strengthens rather than narrows the theorem. |
| C2 / 28–41 | `main-correct` | Entry all-path reachability claim over the exact `solution` macro, `N>=0`, empty environment, and `noResult`. It requires the exact five-binding final environment and constrains both result locations to `expected(N)`. |

C1 is used as the loop circularity when C1 and C2 are proved together.
Selecting only C2 deliberately removes that dependency and does not close
within 60 seconds; the explicit complete target set closes. C1 alone also
closes. This dependency is normal lemma/circularity use, not an assumption:
the complete proof run discharges both claims.

## Constructor-to-rule coverage

| Submitted constructor/operation | Declaration and rules |
|---|---|
| `Module(FuncDef("f",Params("n"),...))` | Program/statement/parameter syntax; S1 executes the exact body and binds `n`. |
| statement lists and empty list | `Stmts`; S2–S3. |
| `Assign(Name(...),...)` | statement/expression syntax; S4–S5. |
| `While` | statement syntax; S9–S11. |
| `If` | statement syntax; S6–S8. |
| `Return(Name("result"))` | statement/expression syntax; S12–S13 plus S15. |
| `Int(0/1/2)` and `Name` | expression syntax; S14–S15. |
| `ListExpr()` and `ListExpr(Name(...))` | expression/list syntax; S16–S18. |
| integer `+`, `*`, `%` | `BinOp`; S19–S23. |
| list `+` | `BinOp`; S19–S20 and S24. |
| integer `<=`, `==` | `Compare`/`CmpOp`; S25–S28. |

## Static conclusion

All local rule domains used by the submitted program are covered, terminating
where declared as functions, and pairwise consistent. The only execution
acceleration is the machine-proved loop circularity; there is no operational
bridge or opaque value. No candidate-authored rule admits a false conclusion
on the intended nonnegative-integer domain, so there is no unsound-rule false
witness to report. The separate body mutation demonstrates that changing the
executed factorial update changes the expanded term and produces a stuck proof
with ground witness `n=2` (`[1,4]` instead of `[1,2]`).
