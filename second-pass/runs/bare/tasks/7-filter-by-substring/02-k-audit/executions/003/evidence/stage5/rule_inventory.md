# Reviewer rule inventory

Scope: `/candidate/semantic.k` and `/candidate/verification.k`. There are no
other candidate helper K files. Line numbers below refer to those immutable
candidate files.

## Local syntax and configuration inventory

`SEMANTIC-SYNTAX` declares:

| ID | Lines | Declaration | Used by submitted term | Assessment |
|---|---:|---|---|---|
| D1 | 6 | `Pgm ::= Module(Stmts)` | yes | Faithful module wrapper. |
| D2 | 7 | `Stmts ::= List{Stmt,""}` | yes | Represents the adjacent translated statements. |
| D3 | 8 | `Stmt ::= ImportFrom(String,String)` | yes | Adequate for the typing-only import. |
| D4 | 9 | `Stmt ::= FuncDef(String,Params,CellVars,FreeVars,Stmts)` | yes | Constructor identity matches trusted translation. |
| D5 | 10 | `Stmt ::= Return(Expr)` | yes | Candidate body is exactly one return. |
| D6 | 12 | `Params ::= Params(String,String)` | yes | Exactly the two candidate parameters. |
| D7 | 13 | `CellVars ::= CellVars(String)` | yes | Parsed metadata; no dynamic role for this pure function. |
| D8 | 14 | `FreeVars ::= FreeVars()` | yes | Parsed metadata; no dynamic role here. |
| D9 | 16 | `Expr ::= Name(String)` | yes | Used for all variable references. |
| D10 | 17 | `Expr ::= ListComp(Expr,CompFors)` | yes | Used for the return expression. |
| D11 | 18 | `Expr ::= Compare(Expr,CmpOps)` | yes | Used for the membership guard. |
| D12 | 19 | `CompFors ::= List{CompFor,""}` | yes | Submitted term has one generator. |
| D13 | 20 | `CompFor ::= CompFor(Expr,Expr,Exprs)` | yes | Submitted term has target, iterable, and one condition. |
| D14 | 21 | `Exprs ::= List{Expr,","}` | yes | Singleton condition list in the submitted term. |
| D15 | 22 | `CmpOps ::= List{CmpOp,","}` | yes | Singleton comparison-operation list. |
| D16 | 23 | `CmpOp ::= CmpOp(String,Expr)` | yes | Submitted operator is `"in"`. |
| D17 | 25–26 | `PyList ::= Nil \| Cons(String,PyList)` | runtime input/result | Covers finite lists of K strings, matching the typed source domain structurally. |
| D18 | 28 | `KItem ::= execute(Pgm,String,PyList,String)` | entry | Explicit program/function/input/substr invocation. |

`SEMANTIC` has one cell only: lines 38–42 initialize `<k>` with
`execute($PGM,$FUNCTION,$INPUT,$SUBSTRING)`. This is adequate for the submitted
pure expression: there is no heap, I/O, exception, mutation, or externally
observable comprehension-local binding after return.

The remaining local constructors/declarations are:

| ID | Lines | Declaration / attributes | Assessment |
|---|---:|---|---|
| D19 | 44 | `Function ::= function(Params,Stmts)` | Internal closure record. |
| F1 | 45 | `lookupFunction(String,Stmts) [function]` | Partial outside supported modules; covered on the exact program. |
| F2 | 58 | `returnExpr(Stmts) [function]` | Partial outside one-return bodies; covered on the exact program. |
| F3 | 61 | `invoke(Function,PyList,String) [function]` | Covered for the exact two-parameter function. |
| F4 | 62 | `evalList(Expr,Map) [function]` | Covered for the exact list expression and list-name lookup. |
| D20 | 63 | `substringFilter(String)` | Internal filter descriptor. |
| F5 | 64 | `evalComp(PyList,SubstringFilter) [function,total]` | Constructors and complementary guards give structural coverage. |
| F6 | 65 | `evalString(Expr,Map) [function]` | Covered for the exact string-name lookup. |
| F7 | 66 | `containsString(String,String) [function]` | Total through imported string/int primitives, but not Python-faithful at one material boundary. |
| F8 | verification 7 | `solutionProgram : Pgm [function]` | Exact submitted term; one defining rule. |
| F9 | verification 22 | `filterRef(PyList,String) [function,total]` | Structurally total, but inherits the defective membership predicate. |

There are no local `[functional]`, `[simplification]`, priority, `owise`,
anywhere, fresh, or opaque declarations. Only F5 and F9 are marked `total`.
No local symbol is unconstrained. Imported maps, booleans, integers, strings,
K equality, and collection syntax are part of the K trust boundary.

## Rule inventory

| ID | File:lines | Rule and class | Complete local-domain assessment |
|---|---|---|---|
| S1 | semantic 47–49 | Skip `ImportFrom` during lookup; semantic equation | Correct on the submitted typing-only import. A general Python import can have effects, but that broader construct is not used or claimed. |
| S2 | semantic 50–52 | Matching `FuncDef` becomes `function`; semantic equation | Correct for the sole submitted definition and preserves parameters/body. |
| S3 | semantic 53–56 | Skip nonmatching `FuncDef`; guarded semantic equation | Guard is disjoint from S2. Selecting the first of duplicate same-name definitions would not model general Python rebinding, but the exact submitted module has one definition. |
| S4 | semantic 59 | Select first `Return`; semantic equation | Exact body has one return and no preceding effects. Broader statement sequences are intentionally unsupported. |
| S5 | semantic 68–70 | `execute(Module(...))` to lookup/invoke; ordinary operational rule | Preserves the complete one-cell state and active continuation. It executes the provided program term rather than naming only the answer. |
| S6 | semantic 72–75 | Bind two arguments, extract/evaluate return; semantic equation | Correct for distinct submitted parameter names and pure body. Map environment contains both actual values. |
| S7 | semantic 77 | `evalList(Name(...))` map lookup; semantic equation | Correct typed lookup; exact candidate use is covered. |
| S8 | semantic 78 | `evalString(Name(...))` map lookup; semantic equation | Correct typed lookup; exact candidate use is covered. |
| S9 | semantic 80–87 | Specialized one-generator membership list-comprehension evaluation; semantic equation / execution summary | The complete pattern forces element=target, generator target=target, operator=`"in"`, and condition haystack=target. With the candidate’s pure name expressions it preserves order and duplicates and has no omitted observable state. It is a narrow direct semantics, not an unconstrained oracle. Its Python fidelity is conditional on S13. |
| S10 | semantic 89 | `evalComp(Nil,_) => Nil`; structural equation | Correct zero-iteration behavior. |
| S11 | semantic 90–92 | Keep head when `containsString`; guarded structural equation | Internally correct and recursively descending. Guard is disjoint from S12. |
| S12 | semantic 93–95 | Drop head when `notBool containsString`; guarded structural equation | Internally correct and recursively descending. Together with S11 it is exhaustive for Boolean S13 results. |
| S13 | semantic 97–98 | `containsString(H,N) => findString(H,N,0) >=Int 0`; imported-primitive bridge | **Materially unsound as a model of Python `N in H`.** Witness on the intended typed domain: `H=""`, `N=""`. Python evaluates `"" in ""` to `True`; rebuilt K execution of the exact submitted program on `Cons("",Nil), ""` returns `Nil`, enabling the false conclusion that the empty string should be dropped. Evidence: `../stage3/clean_rebuild.log`. |
| V1 | verification 8–20 | `solutionProgram` to constructor term; definitional equation | Mechanical whitespace-insensitive constructor-token comparison is exact. Evidence: `../stage4/check_pinning_and_body_sensitivity.log`. |
| V2 | verification 23 | `filterRef(Nil,_) => Nil`; reference-summary equation | Correct base case. |
| V3 | verification 24–26 | `filterRef` keep rule; guarded summary equation | Structurally correct conditional on S13. It mirrors S11. |
| V4 | verification 27–29 | `filterRef` drop rule; guarded summary equation | Structurally correct conditional on S13. It mirrors S12 and therefore inherits S13’s false intended-domain result: `filterRef(Cons("",Nil),"") => Nil`, while the contract requires `Cons("",Nil)`. |

## Construct-to-rule coverage

The trusted constructor term uses D1–D16 and is executed through S1, S2, S4,
S5, S6, S7, S8, and S9. Runtime list inputs/results use D17; recursion uses
S10 plus exactly one of S11/S12 for every head; membership uses S13. The
typing-only `ImportFrom` is the only skipped source construct. `CellVars` and
`FreeVars` are translator metadata carried through lookup but have no material
runtime behavior in this pure, non-closure function.

The configuration has no omitted material state for this exact program.
Evaluation order skipped by S9 is observationally inert because all evaluated
subexpressions are environment lookups and the comprehension has no side
effects. Calls, returns, guards, recursion, order, and duplicate preservation
are otherwise represented. Unsupported unused Python constructs are not a
defect in generated-semantics mode.

## Claims (not semantic rules)

`spec.k` contains six claims. `UNIVERSAL-PROGRAM-REDUCTION` constrains arbitrary
exact-program execution only to the internal `evalComp` term. `UNIVERSAL-BASE`
is the Nil equality. `UNIVERSAL-STEP-KEEP` and `UNIVERSAL-STEP-DROP` assume the
tail equality in their `requires` clause and prove one constructor step; both
were reported by the backend as trivial claims. `EMPTY-EXAMPLE` and
`PROMPT-EXAMPLE` constrain two fixed executions.

No candidate claim states the actual universal postcondition
`execute(solutionProgram,...,INPUT,SUBSTRING) => filterRef(INPUT,SUBSTRING)`.
The reviewer-created direct target stops at
`evalComp(INPUT,substringFilter(SUBSTRING))` versus
`filterRef(INPUT,SUBSTRING)`. The base/step suite can support an informal
meta-level structural-induction argument, but the K artifacts do not
machine-check that universally quantified composed reachability claim.
