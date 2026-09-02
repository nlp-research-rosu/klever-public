# Exhaustive local K inventory

Source line references are to the immutable candidate files. Imported K
builtins are listed separately as trust boundaries; this inventory covers every
local declaration and rule in `semantic.k` and `verification.k`.

## Local syntax declarations

| ID | Location | Declaration or production | Used by the submitted term | Audit |
|---|---|---|---|---|
| S1 | `semantic.k:6` | `Pgm ::= PyProgram` | Top-level parser subsort | Sound |
| S2 | `semantic.k:8` | `PyProgram ::= Module(PyStmts)` | Yes | Exact AST constructor |
| S3 | `semantic.k:9` | `PyStmts ::= List{PyStmt,""}` | Yes | Ordered finite statement sequence |
| S4 | `semantic.k:11` | `Params(String)` | Yes | Exact one-parameter representation |
| S5 | `semantic.k:13` | `ImportFrom(String,String)` | Yes, typing-only import | Exact constructor; behavior is scoped by R4 |
| S6 | `semantic.k:14` | `FuncDef(String,Params,PyStmts)` | Yes | Exact constructor |
| S7 | `semantic.k:15` | `Assign(PyExpr,PyExpr)` | Yes | Exact constructor |
| S8 | `semantic.k:16` | `For(PyExpr,PyExpr,PyStmts)` | Yes | Exact constructor |
| S9 | `semantic.k:17` | `Return(PyExpr)` | Yes | Exact constructor |
| S10 | `semantic.k:19` | `Name(String)` | Yes | Exact constructor |
| S11 | `semantic.k:20` | `Str(String)` | Yes | Exact constructor |
| S12 | `semantic.k:21` | `BinOp(String,PyExpr,PyExpr)` | Yes | Exact constructor |
| S13 | `semantic.k:23` | `.StrList` | Yes, input base | Finite-list base |
| S14 | `semantic.k:24` | `String :: StrList` | Yes, input step | Ordered-list constructor |
| S15 | `semantic.k:25` | `sVal(String)` | Yes | String runtime value |
| S16 | `semantic.k:26` | `lVal(StrList)` | Yes | List runtime value |
| S17 | `semantic.k:28` | `noFunction` | Yes | Empty function slot |
| S18 | `semantic.k:29` | `function(String,String,PyStmts)` | Yes | Stored single binding |
| S19 | `semantic.k:30` | `noResult` | Yes | No-return sentinel |
| S20 | `semantic.k:30` | `Result ::= PyVal` | Yes | Returned-value subsort |
| S21 | `semantic.k:32` | `load(PyProgram)` | Yes | Loader continuation |
| S22 | `semantic.k:33` | `moduleLoaded` | Yes | Loader delimiter |
| S23 | `semantic.k:34` | `invoke(String,PyVal)` | Yes | Call continuation |
| S24 | `semantic.k:35` | `assignTo(String)` | Yes | Assignment continuation |
| S25 | `semantic.k:36` | `addLeft(PyExpr)` | Yes | Left-to-right evaluation continuation |
| S26 | `semantic.k:37` | `addRight(PyVal)` | Yes | Addition continuation with saved left value |
| S27 | `semantic.k:38` | `startFor(String,PyStmts)` | Yes | Loop setup continuation |
| S28 | `semantic.k:39` | `loop(String,StrList,PyStmts)` | Yes | Remaining-list loop state |
| S29 | `semantic.k:40` | `bindLoop(String,PyVal)` | Yes | Iteration binding continuation |
| S30 | `semantic.k:41` | `finishReturn` | Yes | Return publication continuation |
| S31 | `semantic.k:42` | `cleanup` | Yes | Call-local cleanup continuation |
| S32 | `verification.k:5` | `concatAcc(String,StrList) [function]` | Only claims/postconditions | Definitional left-fold summary |

There are no local declarations with `total`, `functional`,
`simplification`, `concrete`, `priority`, `owise`, `opaque`, or `impure`
attributes. There are no local syntax macros.

## Configuration and state

`semantic.k:49-57` declares exactly six cells: `<k>` for computation,
`<function>` for the sole stored function, `<argument>` for `strings`,
`<accumulator>` for `result`, `<iterationItem>` for `string`, and `<result>`
for the published return. The initialized computation loads `$PGM` and invokes
`"concatenate"` with `$ARG`. No heap, I/O, exception, or allocation state is
modeled; the exact submitted function needs none on `list[str]` inputs.

## Ordinary operational rules

| ID | Location | Rewrite and footprint | Soundness on the exact submitted program |
|---|---|---|---|
| R1 | `semantic.k:60` | `load(Module(STMTS))` sequences `STMTS` then `moduleLoaded`; reads/writes only `<k>` | Exact module sequencing |
| R2 | `semantic.k:61` | Empty `PyStmts` becomes `.K`; `<k>` only | Exact list-unit behavior |
| R3 | `semantic.k:62` | Statement head becomes head followed by tail; `<k>` only | Preserves source order |
| R4 | `semantic.k:63` | Any `ImportFrom` becomes `.K`; `<k>` only | Sound for the exact typing-only import, which has no runtime use. Over-broad as a general Python rule: `from definitely_missing import x` raises in Python but this rule erases it. That witness is outside the pinned program term and no entry input can change the fixed import. |
| R5 | `semantic.k:64-65` | `FuncDef` becomes `.K` and replaces `<function>` with its name, parameter, and exact body | Exact for the sole definition |
| R6 | `semantic.k:66` | `moduleLoaded` becomes `.K`; `<k>` only | Exact delimiter removal |
| R7 | `semantic.k:69-71` | `invoke(F,ARG)` requires stored `function(F,"strings",BODY)`, schedules exact `BODY ~> cleanup`, and binds `<argument>` | Pins selected name, formal parameter, body, and argument; one first-order call requires no stack |
| R8 | `semantic.k:74` | `Str(S)` becomes `sVal(S)` | Exact literal evaluation |
| R9 | `semantic.k:75-76` | `Name("strings")` reads `<argument>` | Exact parameter lookup |
| R10 | `semantic.k:77-78` | `Name("result")` reads `<accumulator>` | Exact local lookup |
| R11 | `semantic.k:79-80` | `Name("string")` reads `<iterationItem>` | Exact loop-variable lookup |
| R12 | `semantic.k:81` | Assignment evaluates RHS before `assignTo(X)` | Correct Python RHS-before-store order |
| R13 | `semantic.k:82-83` | `PyVal ~> assignTo("result")` updates `<accumulator>` | Covers both and only submitted assignments |
| R14 | `semantic.k:84` | `BinOp("+",LEFT,RIGHT)` evaluates `LEFT` before `RIGHT` | Correct Python operand order |
| R15 | `semantic.k:85` | Saves evaluated left value while evaluating right | Correct continuation and no cell changes |
| R16 | `semantic.k:86` | `sVal(S1)` plus `sVal(S2)` becomes `sVal(S1 +String S2)` | Correct order and value, conditional on trusted K `STRING.concat` matching Python string concatenation |
| R17 | `semantic.k:90` | `For(Name(X),ITER,BODY)` evaluates `ITER` before loop setup | Correct iterable-first order |
| R18 | `semantic.k:91` | A list value starts `loop(X,ITEMS,BODY)` | Exact for `list[str]` |
| R19 | `semantic.k:92` | Empty remaining list ends loop | Correct boundary |
| R20 | `semantic.k:93-94` | Cons list binds head, runs body, recurs on tail | Correct left-to-right traversal and decreasing finite tail |
| R21 | `semantic.k:95-96` | Binding `"string"` updates `<iterationItem>` | Exact submitted target binding |
| R22 | `semantic.k:100` | `Return(E)` evaluates `E` before `finishReturn` | Exact because the pinned return is last. Over-broad for arbitrary bodies: `Return(Str("x")) Assign(...)` would wrongly continue after publishing the return; no such continuation occurs in the pinned body or loop claim. |
| R23 | `semantic.k:101-102` | `PyVal ~> finishReturn` publishes `<result>` | Exact return value; other cells preserved until cleanup |
| R24 | `semantic.k:103-107` | `cleanup` clears function and call-local cells, preserving `<result>` | Exact observable result and the claim’s closed final configuration |

The rule LHSs that can coexist are either sequential continuations or have
disjoint constructors/literal names. There are no priority interactions.
R19 and R20 are disjoint (`.StrList` versus cons). R8-R11, R13, R15-R16,
R18, R21, and R23 are sort/literal constrained, so a used ill-typed operation
would stop rather than fabricate a value.

## Definitional equations and claims

| ID | Location | Kind | Audit |
|---|---|---|---|
| E1 | `verification.k:6` | `concatAcc(ACC,.StrList) => ACC` | True fold base |
| E2 | `verification.k:7` | `concatAcc(ACC,S::REST) => concatAcc(ACC +String S,REST)` | True fold step; structurally decreases `REST` |
| C1 | `spec.k:10-24` | Loop reachability claim | Exact loop body and exact return/cleanup suffix; result is `concatAcc(ACC,ITEMS)` |
| C2 | `spec.k:28-47` | Entry reachability claim | Exact submitted constructor tree, arbitrary finite `StrList`, and result `concatAcc("",INPUT)` |

E1 and E2 have disjoint guards by constructor, cover all `StrList` terms, agree
with the operational accumulator update, and terminate. Although `concatAcc`
is not marked `total`, its equations are exhaustive. Neither equation replaces
program execution: the symbol appears only in proof results and the
postcondition.

## Imported trust boundary

The local semantics imports K's `STRING` module. The proof therefore trusts
the backend-hooked `String` carrier and total `STRING.concat` (`+String`), plus
ordinary K term/list matching and reachability logic. The candidate introduces
no opaque result symbol, oracle, operational bridge, simplification lemma, or
task-answer rewrite.
