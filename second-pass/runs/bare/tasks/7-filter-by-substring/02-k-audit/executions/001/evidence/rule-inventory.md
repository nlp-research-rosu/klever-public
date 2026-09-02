# Reviewer rule and claim inventory

Scope: the candidate has exactly two K theory files, `semantic.k` and
`verification.k`; no generated helper `.k` files are present. This inventory
lists every local syntax production, attribute-bearing declaration,
configuration, rule, and submitted claim. Imported K builtins are accounted for
in the trust ledger, not re-inventoried as local rules.

## `semantic.k`: syntax and configuration

| ID | Lines | Declaration | Used by `solution.mpy` | Review |
|---|---:|---|---|---|
| D01 | 6 | `Pgm ::= Module(Stmts)` | yes | Exact outer translated constructor. |
| D02 | 7 | `Stmts ::= List{Stmt,""}` | yes | Holds the import and function definition, and the function body. |
| D03 | 8 | `Stmt ::= ImportFrom(String,String)` | yes | Exact translated import; operationally skipped. |
| D04 | 9 | `Stmt ::= FuncDef(String,Params,CellVars,FreeVars,Stmts)` | yes | Exact translated function definition. |
| D05 | 10 | `Stmt ::= Return(Expr)` | yes | Exact body statement. |
| D06 | 12 | `Params(String,String)` | yes | Exact two-parameter signature. |
| D07 | 13 | `CellVars(String)` | yes | Parses the translator's closure metadata; unused by execution. Safe for this exact program because the captured substring is installed directly in the environment. |
| D08 | 14 | `FreeVars()` | yes | Parses empty free-variable metadata; unused by execution. |
| D09 | 16 | `Expr ::= Name(String)` | yes | Used for target, iterable, and needle. |
| D10 | 17 | `Expr ::= ListComp(Expr,CompFors)` | yes | Exact return expression. |
| D11 | 18 | `Expr ::= Compare(Expr,CmpOps)` | yes | Exact membership guard. |
| D12 | 19 | `CompFors ::= List{CompFor,""}` | yes | Submitted program has one generator. |
| D13 | 20 | `CompFor(Expr,Expr,Exprs)` | yes | Exact generator constructor. |
| D14 | 21 | `Exprs ::= List{Expr,","}` | yes | Submitted program has one guard expression. |
| D15 | 22 | `CmpOps ::= List{CmpOp,","}` | yes | Submitted program has one comparison operator. |
| D16 | 23 | `CmpOp(String,Expr)` | yes | Submitted program uses `"in"` and the target name. |
| D17 | 25 | `PyList ::= Nil` | runtime input/result | Empty finite list. |
| D18 | 26 | `PyList ::= Cons(String,PyList)` | runtime input/result | Finite string-list constructor; preserves order and duplicates. |
| D19 | 28 | `KItem ::= execute(Pgm,String,PyList,String)` | entry | Explicit program/function/input/substring entry term. |
| D20 | 38–42 | `<k>`-only configuration initialized with `execute` | entry | Sufficient for this pure function: there is no mutation, allocation, I/O, exception handling, or persistent frame needed by the used subset. |
| D21 | 44 | `Function ::= function(Params,Stmts)` | yes | Internal selected function value; constructor, no attributes. |
| D22 | 45 | `lookupFunction(String,Stmts) [function]` | yes | Partial function; visibly sticks when no matching definition exists. |
| D23 | 58 | `returnExpr(Stmts) [function]` | yes | Partial extraction function, sufficient for the used leading `Return`. |
| D24 | 61 | `invoke(Function,PyList,String) [function]` | yes | Evaluates the selected two-argument function. |
| D25 | 62 | `evalList(Expr,Map) [function]` | yes | List-valued expression evaluator. |
| D26 | 63 | `SubstringFilter ::= substringFilter(String)` | yes | Internal filter descriptor; constructor, not opaque. |
| D27 | 64 | `evalComp(PyList,SubstringFilter) [function,total]` | yes | Structurally recursive list-comprehension evaluator. Nil/Cons plus complementary Boolean guards cover its used domain. |
| D28 | 65 | `evalString(Expr,Map) [function]` | yes | String-valued name lookup. |
| D29 | 66 | `containsString(String,String) [function]` | yes | Result-bearing predicate. Its only equation is the material semantics defect identified below. |

There are no local `functional`, `simplification`, `anywhere`, `macro`,
`owise`, `priority`, or opaque declarations.

## `semantic.k`: rules

| ID | Lines | Rule and state/control effect | Judgment |
|---|---:|---|---|
| S01 | 47–49 | Skip `ImportFrom` while looking up a function. | Sound for the used typing-only import; no cells are changed. |
| S02 | 50–52 | A same-named `FuncDef` becomes `function(PARAMS,BODY)`. | Sound exact-name selection; unused closure metadata is deliberately omitted from the internal value. |
| S03 | 53–56 | Skip a differently named `FuncDef` under string inequality. | Sound and disjoint from S02. Together with S01 it covers the submitted top-level prefix. |
| S04 | 59 | `returnExpr(Return(E) REST) => E`. | Sound for the used body. It intentionally does not model statements after return because none are used. |
| S05 | 68–70 | Rewrite the whole `<k>` entry from `execute(Module(...),...)` to `invoke(lookupFunction(...),...)`. | Ordinary semantic rule; preserves all four entry values and the only state cell. No continuation is discarded. |
| S06 | 72–75 | Invoke the selected two-parameter body with a two-binding map. | Sound for the submitted distinct names `"strings"`/`"substring"`. It does not model Python call errors outside this syntax/domain. |
| S07 | 77 | List name lookup from the map. | Sound for the typed list binding; map matching preserves the rest. |
| S08 | 78 | String name lookup from the map. | Sound for the typed substring binding; map matching preserves the rest. |
| S09 | 80–87 | Exact-shape list comprehension becomes `evalComp(evalList(iterable), substringFilter(evalString(needle)))`. | Narrowly sound for the submitted one-generator, one-guard expression: the repeated target name is syntactically pinned, order/duplicates are left to S10–S12, and the environment supplies the iterable and needle. It does not fabricate behavior for other list comprehensions; those stick. |
| S10 | 89 | `evalComp(Nil,_) => Nil`. | Sound base case. |
| S11 | 90–92 | Keep `HEAD` and recurse when `containsString(HEAD,NEEDLE)`. | Structurally sound conditional on the predicate; preserves order and duplicates. Its observed results inherit S13's bad predicate interpretation. |
| S12 | 93–95 | Drop `HEAD` and recurse under the negated predicate. | Disjoint from S11 and structurally sound conditional on the predicate. It enables the false result in the S13 witness. |
| S13 | 97–98 | Define containment as `findString(HAYSTACK,NEEDLE,0) >=Int 0`. | **Unsound as a model of Python `NEEDLE in HAYSTACK` on the intended domain.** Witness: `HAYSTACK=""`, `NEEDLE=""`. Both trusted canonical Python and candidate Python return `[""]` for `filter_by_substring([""],"")`; fresh K execution uses this predicate and S12 to return `Nil`. See `stage5-unsound-empty-empty-witness.log`. This is a false observable program conclusion, not merely missing coverage. |

Rule guards S11/S12 are complementary when S13 yields a Boolean; they do not
overlap. All recursive calls descend on the list tail. There is no allocation,
mutable state, output, exception, return-frame pop, priority preemption, or
arbitrary continuation bridge in the local semantics.

## `verification.k`: declarations and rules

| ID | Lines | Extension | Class and judgment |
|---|---:|---|---|
| V01 | 7 | `Pgm ::= solutionProgram [function]` | Definitional program constant; result-bearing only through execution. |
| V02 | 8–20 | `solutionProgram => Module(...)` exact AST | Definitional equation, not an execution bridge. Whitespace-normalized RHS is identical to regenerated `solution.mpy` (`stage4-program-pinning.log`). It terminates in one rewrite and has no overlap. |
| V03 | 22 | `filterRef(PyList,String) [function,total]` | Task-specific definitional summary. Nil/Cons and complementary guards cover the used domain; recursion descends on the tail. |
| V04 | 23 | `filterRef(Nil,_) => Nil` | Mathematically sound base equation. |
| V05 | 24–26 | Keep and recurse under `containsString`. | Sound relative to the locally defined predicate, but it is not an independently correct Python reference because it depends on S13. |
| V06 | 27–29 | Drop and recurse under negated `containsString`. | Disjoint from V05 and sound relative to S13; it produces `Nil` for `filterRef(Cons("",Nil),"")`, so the summary-to-natural-contract bridge is false on the S13 witness. |

No operational bridge, opaque/fresh oracle, lemma rule, simplification,
priority, `functional`, or additional cell rule appears in `verification.k`.
The important concern is not an unconstrained oracle: `filterRef` is fully
defined. The problem is that both execution and reference reuse the same
incorrect result-bearing predicate, so their equality cannot validate Python
substring behavior.

## `spec.k`: submitted reachability claims

| Claim | Preconditions in plain language | Postcondition and audit result |
|---|---|---|
| `UNIVERSAL-PROGRAM-REDUCTION` | Any finite `PyList` and K `String`; exact function name and `solutionProgram`. | Execution reaches `evalComp(INPUT,substringFilter(SUBSTRING))`. Freshly closes, but stops at the internal evaluator rather than constraining the arbitrary-input returned list to `filterRef` or the natural contract. |
| `UNIVERSAL-BASE` | Any substring, empty input. | `evalComp(Nil,...)` reaches `filterRef(Nil,...)`; closes and is true. |
| `UNIVERSAL-STEP-KEEP` | Head predicate true and an assumed K equality between tail evaluator and tail `filterRef`. | Head evaluator reaches head `filterRef`; closes as a conditional induction step. |
| `UNIVERSAL-STEP-DROP` | Head predicate false and the same assumed tail equality. | Drop case reaches head `filterRef`; closes as a conditional induction step. |
| `EMPTY-EXAMPLE` | Ground empty prompt example. | Returns `Nil`; closes and agrees with Python. |
| `PROMPT-EXAMPLE` | Ground four-string prompt example. | Returns the three expected strings; closes and agrees with Python. |

All claim preconditions are satisfiable; concrete substitutions and both Python
results are in `stage4-claim-witnesses.log`. The base and step claims are valid
induction obligations, but the candidate did not submit or close the universal
entry postcondition that their comments say follows. The auditor-written exact
entry claim builds and then gets stuck at
`evalComp(INPUT,...) == filterRef(INPUT,...)`; see
`stage4-intended-universal-{dry-run,kprove}.log`.
