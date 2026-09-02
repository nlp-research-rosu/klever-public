# Exhaustive local K inventory and reviewer judgments

Line numbers refer to the scratch copies, which are byte copies of the candidate
sources. Imported K builtins are the installed K v7.1.293 definitions and are
not candidate-local extensions.

## Syntax and attributes: `semantic.k`

| Lines | Declaration inventory | Used by submitted `solution.mpy` | Judgment |
|---|---|---:|---|
| 6 | `Program ::= Module(Stmts)` | yes | Recognizable translator constructor. |
| 8 | `Stmts ::= List{Stmt,""}` | yes | Matches translated statement lists. |
| 9–12 | `Stmt ::= FuncDef \| Return \| Assign \| If` | FuncDef, Return | Used forms are covered; Assign/If are extra subset forms. |
| 14–15 | `Params`, `Strings` | yes | Matches translator constructors. |
| 17–26 | `Expr ::= Int \| Name \| BinOp \| Compare \| ListExpr \| TupleExpr \| ListComp \| KwArg \| Subscript \| Call` | all except Subscript | All submitted constructors parse. `TupleExpr` is modeled only inside the exact comprehension bridge. |
| 28–34 | `Exprs`, `CmpOps`, `CmpOp`, `CompFors`, `CompFor`, `Index`, `Bound` | all except Index/Bound | Submitted list/comparison/comprehension constructors parse. |
| 48 | `Ints ::= List{Int,","}` | representation | Concrete Python integer arrays/results are flattened into this list sort. |
| 49–62 | `Val ::= VInt \| VList \| VArray \| VBool \| VEq \| VLt \| VCandidates \| VCandidatesArray \| minEvenInts \| chooseEven \| minEvenArray \| VNone` | yes | `VArray`, `VCandidates*`, and the three scan helpers are generated abstractions, not Python values. |
| 57 | `minEvenInts(Ints,Int) [function,total]` | concrete `VList` path | Equations cover every constructor `Ints`; truthful minimum-even/first-index recursion. |
| 58–59 | `chooseEven(Int,Int,Val) [function,total]` | concrete `VList` path | Truthful on the only reachable `REST` values (empty/pair `VList`), but not total over declared `Val`: an even head with `REST=VInt(0)` has no equation. |
| 60–61 | `minEvenArray(Int,Int,Int) [function,total]` | entry proof path | No equation exists in `semantic.k`; the fresh LLVM compiler reports a non-exhaustive match and base execution stops here. Result-bearing opaque program summary. |
| 63 | `Vals ::= List{Val,","}` | yes | Argument representation. |
| 68 | `headInt(Ints) [function,total]` | no | Only nonempty equation exists; empty input witnesses the false totality annotation. |
| 69 | `arrayAt(Int,Int) [function,total]` | entry proof path | No semantic equations; externally interpretable array observer, but the false `total` annotation is compiler-diagnosed. |
| 70 | `tailInts(Ints) [function,total]` | no | Only nonempty equation exists; empty input witnesses the false totality annotation. |
| 90–92 | `Fun`, `Frame`, `ArgPack` | yes | Function, call-frame, and evaluated-argument representations. |
| 94–114 | `KItem ::= start \| done \| exec \| execStmt \| eval \| evalExprs \| evalArgs \| assignName \| select \| binLeft \| binRight \| cmpLeft \| cmpRight \| collectExprs \| prependInt \| collectArgs \| prependArg \| takeTail \| subBase \| subIndex \| arraySubIndex \| callNamed \| minDefaultEmpty \| invoke \| functionReturn \| implicitReturn` | path-dependent | Internal control syntax. Submitted path uses module/call/return, exact comprehension, and `minDefaultEmpty`; many general subset items are unused. |
| 116 | `bindParams(Params,Vals) [function,total]` | yes | Truthful for equal arities, including the one-parameter call. Mismatched arities have no equations, so global totality is false. |
| 118–126 | `<py>` with `<k>`, `<args>`, `<env>`, `<funs>`, `<stack>`, `<result>` | yes | Sufficient state for the used pure subset. There is no heap/array-content cell; `VArray` contents exist only through opaque `arrayAt`. |

There are no local `[functional]` declarations and no `[simplification]`
rules. The only local priority rules are at 177/180 and 227, inventoried below.

## Rules: `semantic.k`

Every local rule start line is listed exactly once.

| Start line(s) | Rule(s) | Judgment |
|---|---|---|
| 71 | `headInt(I,_IS) => I` | Correct for nonempty lists; does not justify global `[total]`. Unused by the submitted program. |
| 72 | `tailInts(_I,IS) => IS` | Correct for nonempty lists; does not justify global `[total]`. Unused by the submitted program. |
| 76 | empty `minEvenInts` | Correct: no even candidate gives `[]`. |
| 77 | recursive `minEvenInts` | Structurally descends and advances the source index. Correct. |
| 79 | odd `chooseEven` | Correctly ignores an odd head. |
| 81 | even head with no tail candidate | Correctly returns `[HEAD,INDEX]`. |
| 83 | even head `<=` tail best | Correctly selects the smaller value and, on equality, the earlier head index. |
| 86 | even head `>` tail best | Correctly retains the tail best. |
| 130 | `Module(SS) => exec(SS)` | Correct module-load kickoff. |
| 131 | empty `exec` | Correctly consumes an empty statement list. |
| 132 | nonempty `exec` sequencing | Preserves statement order. |
| 134 | function-definition registration | Stores the exact parameter/body syntax; correct for used subset. |
| 137 | `start => invoke("pluck",A) ~> done` | Correct fixed entry selection for this task. |
| 139 | value followed by `done` writes `<result>` | Correct completion rule. |
| 143 | assignment kickoff | Left-to-right expression-before-store behavior; unused. |
| 144 | assignment store | Correct environment update for modeled names; unused. |
| 147 | if kickoff | Evaluates guard before branch; unused. |
| 148,149 | Boolean branch selection | Correct and disjoint; unused. |
| 150,152 | integer-equality branch selection | Correct and disjoint; unused. |
| 154,156 | integer-less-than branch selection | Correct and disjoint; unused. |
| 159 | return kickoff | Evaluates expression before return; used. |
| 162 | integer literal evaluation | Correct. |
| 163 | name lookup | Correct map lookup for bound names. |
| 166,168 | binary left/right evaluation | Correct left-to-right order. The actual `%` syntax occurs only inside the comprehension pattern and is not separately executed. |
| 170 | integer addition | Correct; unused on target path. |
| 171 | integer modulo | Correct on modeled integers; unused on target path because of the bridge. |
| 177 | priority-40 `Name(X) == []` on `VList` | Equivalent to list emptiness for represented lists; unused by target body. |
| 180 | priority-40 `Name(X) == []` on `VArray` | Equivalent only under the representation invariant `LENGTH >= 0`; unused by target body. |
| 184 | generic one-comparator kickoff | Correct evaluation order for the modeled one-comparator subset. |
| 186,188 | comparison-left continuation for `Val` and duplicate `VList` case | Overlap has identical right-hand side; harmless. |
| 190 | integer equality value | Correct. |
| 191 | integer `<=` value | Correct. |
| 192 | integer `<` value | Correct. |
| 193,195 | list/empty equality in either evaluation order | Correct for the covered empty-list comparisons. |
| 198 | list-literal kickoff | Correct. |
| 199 | empty list literal | Correct. |
| 200,201,203 | nonempty list collection | Correct left-to-right construction for integer elements. |
| 208 | exact list-comprehension bridge on `VList` | Its `VCandidates(IS)` summary is truthful only for the downstream `minDefaultEmpty` consumer. The rule admits any continuation and `VCandidates` is itself a `Val`; witness: returning this comprehension on input `[2]` yields `VCandidates(2)` rather than Python `[[2,0]]`. Context is over-broad, though the submitted continuation is the supported one. |
| 217 | exact list-comprehension bridge on `VArray` | Same over-broad-context defect, and its result depends on the opaque array representation. |
| 227 | priority-40 exact `min(...,default=[])` kickoff | Correctly preempts the unsupported generic builtin-call path for this exact syntax. |
| 230 | `VCandidates(IS) ~> minDefaultEmpty => minEvenInts(IS,0)` | Correctly connects the concrete-list summary to the truthful recursive definition. |
| 231 | `VCandidatesArray(...) ~> minDefaultEmpty => minEvenArray(...)` | Replaces the property-bearing comprehension/min computation with an undefined result-bearing function. Base-semantics witness: `VArray(68,0,1)` stops at `minEvenArray(68,0,1)`. |
| 234 | slice `[1:]` kickoff | Evaluation order is correct; unused. |
| 236 | `VList` tail slice | Correct only for nonempty lists. False unused-form witness: Python `[][1:] == []`, while this reaches undefined `tailInts(.Ints)`. |
| 237 | `VArray` tail slice | Lacks the empty-length case. False unused-form witness: length 0 becomes offset+1,length -1 rather than remaining empty. |
| 239–243 | index kickoff/base rules and list index 0 | Correct evaluation order, but only index 0 is covered. Unused. |
| 244 | `VArray` index 0 | Has no bounds check. False unused-form witness: indexing a length-0 input should raise `IndexError`, but this produces `arrayAt(ID,OFFSET)`. |
| 247 | generic named-call kickoff | Correct evaluation order for modeled user calls. Builtins are handled only by exact bridges. |
| 248,249 | empty/nonempty argument evaluation | Correct left-to-right order. |
| 250,251 | collect `Val` and duplicate `VArray` argument cases | Overlap has identical behavior; harmless. |
| 253,254 | prepend evaluated argument and invoke named call | Correct order and call transition. |
| 256,257 | empty/recursive parameter binding | Correct on matching arities; no mismatch/duplicate-parameter behavior, so not globally total. |
| 261 | invocation/frame push | Exact whole continuation is stored with caller environment; functions and result are preserved. Correct for used calls. |
| 267 | explicit return/frame pop | Restores caller environment and exact saved continuation while discarding the callee remainder; correct early-return control. |
| 272 | implicit return/frame pop | Correct `None` result for fall-through; unused by the returning target body. |

## Syntax and rules: `verification.k`

| Lines | Extension | Classification and judgment |
|---|---|---|
| 10–17 | `specScanArray`, `specFinish`, `specConsiderArray`, `specEvenArray`, all `[function,total]` | Mathematical contract functions. They are exhaustive only over the invariant domain: scan `LENGTH >= 0` and FOUND as zero/nonzero. Negative scan length is uncovered despite `[total]`. |
| 19,22 | scan finish/step | Disjoint for length 0 versus positive and structurally descending on the claim domain. Correct. |
| 27,29 | finish no-found/found | Disjoint and complete on integer FOUND. Correct. |
| 32,37 | ignore odd / dispatch even | Parity guards are disjoint and complete. Correct. |
| 43 | first even | Correctly initializes best and earliest index. |
| 48 | later strictly smaller even | Correctly replaces best. |
| 53 | later equal-or-larger even | Correctly retains the earlier best/index. |
| 62 | `minEvenArray => specScanArray` | Illegitimate result-bearing operational bridge. It is the only definition of `minEvenArray`, is not a theorem/claim derived from fixed semantics, and directly supplies the requested answer. The opposite completion in `stage5-wrong-oracle-verification.k` proves the exact program returns `[]` for all arrays (`#Top`), false on satisfying input `[2]`, whose two Python results are `[2,0]`. |
| 66 / 70 | `pluckBody [function,total]` and its sole equation | Complete nullary constant; exact submitted body constructor tree. |
| 67 / 83 | `solutionProgram [function,total]` and its sole equation | Complete nullary constant; exact submitted module constructor tree. |
| 68 / 86 | `solutionFunctions [function,total]` and its sole equation | Complete nullary constant; exact post-load function map. |

There are no verification-local priority, simplification, ordinary operational
cell rules, opaque declarations, or auxiliary claims. The 13 verification rule
starts are 19, 22, 27, 29, 32, 37, 43, 48, 53, 62, 70, 83, and 86.

## `spec.k`

The only declaration is the single unlabeled entry claim at line 9. There are
no helper/loop claims and no proof-local simplification rules.
