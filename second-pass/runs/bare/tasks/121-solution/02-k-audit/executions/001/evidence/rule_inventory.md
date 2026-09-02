# Reviewer rule and declaration inventory

Scope: the local declarations in the submitted `semantic.k`,
`verification.k`, and `spec.k`. Imported K built-ins are accounted for
separately as trusted primitives; there are no submitted helper `.k` files.

## Local syntax declarations

| ID | Source | Declaration/production | Attributes | Used role and judgment |
|---|---|---|---|---|
| S01 | `semantic.k:7` | `Pgm ::= Module(Stmt)` | none | Root AST node; exact submitted term uses it. |
| S02 | `semantic.k:9` | `Stmt ::= FuncDef(String,Params,Stmt)` | none | Exact submitted function node. |
| S03 | `semantic.k:10` | `Stmt ::= Return(Expr)` | none | Exact submitted return node. |
| S04 | `semantic.k:12` | `Params ::= Params(String)` | none | Single parameter; exact submitted term uses `"lst"`. |
| S05 | `semantic.k:14` | `Expr ::= Name(String)` | none | Used by `sum`, `x`, and `lst`; evaluated by R04 when used as a value. |
| S06 | `semantic.k:15` | `Expr ::= Int(Int)` | none | Used by literal `2` and `0`; evaluated by R03. |
| S07 | `semantic.k:16` | `Expr ::= BinOp(String,Expr,Expr)` | none | Submitted operator is `%`; evaluated by R05. |
| S08 | `semantic.k:17` | `Expr ::= Compare(Expr,CmpOp)` | none | Submitted operator is `!=`; evaluated by R06. |
| S09 | `semantic.k:18` | `Expr ::= Subscript(Expr,Slice)` | none | Submitted `lst[::2]`; R07 defines the exact step-2 form, while R16–R20 implement it by cursor traversal. |
| S10 | `semantic.k:19` | `Expr ::= ListComp(Expr,CompFor)` | none | Submitted list comprehension; interpreted in fused R16–R20. |
| S11 | `semantic.k:20` | `Expr ::= Call(Expr,Expr)` | none | Submitted `sum(...)`; interpreted only in the exact fused R16–R20 pattern. |
| S12 | `semantic.k:22` | `CmpOp ::= CmpOp(String,Expr)` | none | Submitted `!= 0`; R06. |
| S13 | `semantic.k:23` | `Slice ::= Slice(Bound,Bound,Bound)` | none | Submitted omitted/omitted/2 slice. |
| S14 | `semantic.k:24` | `Bound ::= NoBound` | none | Represents omitted lower and upper bounds. |
| S15 | `semantic.k:24` | `Bound ::= Expr` | injection | Carries step `Int(2)`. |
| S16 | `semantic.k:25` | `CompFor ::= CompFor(Expr,Expr,Expr)` | none | One target, iterator, and condition; exact submitted comprehension. |
| S17 | `semantic.k:27` | `Ints ::= nil` | none | Empty mathematical integer-list constructor. |
| S18 | `semantic.k:28` | `Ints ::= cons(Int,Ints)` | none | Non-empty mathematical integer-list constructor. |
| S19 | `semantic.k:37` | `Val ::= intVal(Int)` | none | Integer evaluation result. |
| S20 | `semantic.k:38` | `Val ::= boolVal(Bool)` | none | Condition result. |
| S21 | `semantic.k:39` | `Val ::= listVal(Ints)` | none | Parameter/slice result. |
| S22 | `semantic.k:40` | `Env ::= emptyEnv` | none | End of the deliberately small lexical environment. |
| S23 | `semantic.k:41` | `Env ::= bind(String,Val,Env)` | none | Parameter and comprehension-variable binding. |
| S24 | `semantic.k:43` | `KItem ::= run(Pgm,Ints,Ints,Int)` | none | Machine state: exact AST, remaining cursor, original input, accumulator. |
| S25 | `semantic.k:44` | `KItem ::= result(Int)` | none | Observable final result. |
| S26 | `semantic.k:50` | `Val ::= lookup(String,Env)` | `function` | Partial lexical lookup; R01–R02 cover every binding encountered by the submitted program. |
| S27 | `semantic.k:55` | `Val ::= eval(Expr,Env)` | `function` | Partial expression evaluator; R03–R07 cover every expression evaluated by the submitted program. |
| S28 | `semantic.k:68` | `Int ::= asInt(Val)` | `function` | Checked projection in R08. |
| S29 | `semantic.k:69` | `Bool ::= asBool(Val)` | `function` | Checked projection in R09. |
| S30 | `semantic.k:70` | `Ints ::= asInts(Val)` | `function` | Checked projection in R10. |
| S31 | `semantic.k:75` | `Ints ::= everyOther(Ints)` | `function` | Pure step-2 slice helper, R11–R13; not reached by fused R16–R20 for the submitted top-level expression. |
| S32 | `semantic.k:80` | `Bool ::= testAt(Expr,String,Int,String,Ints)` | `function` | Evaluates the pure condition under correct shadowing; R14. |
| S33 | `semantic.k:85` | `Int ::= valueAt(Expr,String,Int,String,Ints)` | `function` | Evaluates the pure body under correct shadowing; R15. |
| S34 | `verification.k:7` | `Pgm ::= solutionProgram` | `function` | Nullary exact-program alias; V01. |
| S35 | `verification.k:23` | `Int ::= expected(Ints,Int)` | `function` | Mathematical contract, V02–V06. |

No declaration has `total`, `functional`, `simplification`, `concrete`,
`priority`, `owise`, `fresh`, or opacity attributes. There are no local
uninterpreted result symbols. Partial function applications outside their
listed supported patterns become visibly stuck.

## Configuration and local rules

The sole configuration is `semantic.k:48`:
`<k> run($PGM, $INPUT, $INPUT, 0) </k>`. It has no hidden heap, I/O, stack,
allocation, exception, or global-binding cell. That is adequate for the
submitted pure function over integer lists, but it is not a general Python
configuration.

| ID | Source | Rule | Classification | Coverage, overlap, descent, and judgment |
|---|---|---|---|---|
| R01 | `semantic.k:51` | lookup matching head name | semantic equation | Correct lexical head lookup. |
| R02 | `semantic.k:52-53` | skip unequal binding | semantic equation | Guard is disjoint from R01; environment tail decreases. Unbound names remain stuck. |
| R03 | `semantic.k:56` | integer literal evaluation | semantic equation | Correct. |
| R04 | `semantic.k:57` | name evaluation by lookup | semantic equation | Correct for the constructed environment. |
| R05 | `semantic.k:59-60` | `%` via `modInt` | semantic equation | Correct for the submitted fixed positive divisor `2`, including negative dividends. Over-broad for negative divisors: `1 % -2` is `-1` in CPython but this rule yields `1`; see `16_semantic_overbreadth.log`. That syntax is unreachable from `solutionProgram`. |
| R06 | `semantic.k:62-63` | integer `!=` comparison | semantic equation | Correct on integer-valued operands. |
| R07 | `semantic.k:65-66` | omitted/omitted/2 slice | semantic equation | Correct for integer lists by R11–R13. The fused run rules do not invoke it. |
| R08 | `semantic.k:71` | `asInt(intVal(I))` | semantic equation | Correct projection; wrong variants visibly stick. |
| R09 | `semantic.k:72` | `asBool(boolVal(B))` | semantic equation | Correct projection; wrong variants visibly stick. |
| R10 | `semantic.k:73` | `asInts(listVal(IS))` | semantic equation | Correct projection; wrong variants visibly stick. |
| R11 | `semantic.k:76` | `everyOther(nil)` | definitional equation | Correct empty slice base. |
| R12 | `semantic.k:77` | singleton step-2 slice | definitional equation | Correct singleton base. |
| R13 | `semantic.k:78` | retain head, skip second, recurse | definitional equation | Correct; input decreases by two and cases R11–R13 are disjoint/exhaustive over constructor lists. |
| R14 | `semantic.k:81-83` | `testAt` | definitional wrapper | Correctly binds the comprehension variable over the parameter. Actual condition is pure and fully defined. |
| R15 | `semantic.k:86-88` | `valueAt` | definitional wrapper | Same binding and purity judgment for the body. |
| R16 | `semantic.k:93-99` | empty cursor to accumulator result | fused operational rule | Correct base case and preserves the continuation through `...`. |
| R17 | `semantic.k:101-108` | singleton, true guard, add body | fused operational rule | Correct for actual pure body/guard; singleton branch is disjoint from R16/R19–R20 and guard complements R18. |
| R18 | `semantic.k:110-117` | singleton, false guard, no add | fused operational rule | Correct and guard-disjoint from R17 when R14 produces a Bool. |
| R19 | `semantic.k:119-127` | length at least two, true guard | fused operational rule | Correctly retains current even-position item, skips the next item, preserves original input/program/continuation, and decreases cursor length by two. |
| R20 | `semantic.k:129-136` | length at least two, false guard | fused operational rule | Correct complement to R19, with the same preservation/descent. |
| V01 | `verification.k:8-19` | `solutionProgram` exact AST equation | exact-program alias | Normalized RHS is identical to submitted `solution.mpy`; see `13_pinning.log`. |
| V02 | `verification.k:24` | `expected(nil,ACC)` | contract definition | Correct base. |
| V03 | `verification.k:25-26` | singleton odd, add | contract definition | Correct for positive divisor 2. |
| V04 | `verification.k:27-28` | singleton even, do not add | contract definition | Guard complements V03. |
| V05 | `verification.k:29-30` | at least two, odd, add and skip | contract definition | Correct and decreases by two. |
| V06 | `verification.k:31-32` | at least two, even, skip | contract definition | Correct complement to V05. |

R16–R20 are an operational fusion of slicing, comprehension allocation, and
`sum`, not an oracle: `BODY` and `COND` remain result-bearing and are evaluated
by R14–R15. Reviewer mutations of each changed the concrete result from 12 to
0 (`14_operational_sensitivity.log`), and a framed continuation was preserved
by the machine-checked `continuation-preserved` witness
(`15_audit_witness.log`). The fusion omits temporary list allocation, but that
allocation is unobservable for this pure body/condition and sole consumer.

## Claims

| ID | Source | Precondition | Postcondition |
|---|---|---|---|
| C01 | `spec.k:6-10` | Exact example-one configuration; no additional `requires`. | Same frame with `result(12)` at the front. |
| C02 | `spec.k:12-16` | Exact example-two configuration; no additional `requires`. | Same frame with `result(9)`. |
| C03 | `spec.k:18-22` | Exact example-three configuration; no additional `requires`. | Same frame with `result(0)`. |
| C04 | `spec.k:24-26` | Any well-sorted constructor integer cursor `INPUT`, any original integer list and accumulator; no additional `requires`. | Same frame with `result(expected(INPUT,ACC))`. |

The three example claims and the universal claim were selected and proved
separately. C04 supplies the circularity used after R19/R20 return to a smaller
`run(solutionProgram, REST, ORIGINAL, updatedACC)` state; there are no helper
claims or proof-only rewrites.

## Submitted-construct coverage map

`solution.mpy` uses exactly S01–S14, S16, and the `Ints` runtime representation
S17–S18. Its `Module/FuncDef/Return/Call(Name("sum"),ListComp(...))` outer
control is matched by R16–R20. The iterator
`Subscript(Name("lst"),Slice(NoBound,NoBound,Int(2)))` is represented by the
cursor transition in R16–R20. The body `Name("x")` maps to R04/R01 through R15.
The condition `Compare(BinOp("%",Name("x"),Int(2)),CmpOp("!=",Int(0)))` maps to
R03–R06/R01 through R14. Every used construct is therefore declared and has a
reachable behavior; unused grammar alternatives need no broader coverage.
