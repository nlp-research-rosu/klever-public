# Local K declaration and rule inventory

This inventory is reviewer-authored from the immutable candidate sources. Line
numbers refer to the candidate files copied into `/tmp/audit-work/candidate-src`.

## `semantic.k`: syntax, configuration, and functions

| ID | Lines | Declaration | Use / assessment |
|---|---:|---|---|
| SD01 | 5 | `Module ::= Module(Stmts)` | Declares the translated module node; used. |
| SD02 | 6 | `Stmts ::= List{Stmt,""}` | Ordered statement list and `.Stmts`; used. |
| SD03 | 7 | `Params ::= Params(Strings)` | Function parameters; used. |
| SD04 | 8 | `Strings ::= List{String,","}` | Parameter list and `.Strings`; used. |
| SD05 | 10–14 | `Stmt ::= FuncDef | Assign | For | If | Return` | Exactly all submitted statement constructors; every alternative is used. |
| SD06 | 16–21 | `Expr ::= Int | Name | UnaryOp | Attribute | Call | Compare` | Exactly all submitted expression constructors; every alternative is used. |
| SD07 | 22 | `Exprs ::= List{Expr,","}` | Call arguments; used. |
| SD08 | 23 | `CmpOp ::= CmpOp(String,Expr)` | Comparison operator/value pair; used. |
| SD09 | 24 | `CmpOps ::= List{CmpOp,","}` | Comparison list; used. |
| SD10 | 34–35 | `IntSeq ::= .Ints | cons(Int,IntSeq)` | Finite list-of-integers value representation; used. |
| SD11 | 36–38 | `Value ::= VInt | VBool | VList` | Only value variants needed by the program; used. |
| SD12 | 39 | `Result ::= noResult | Value` | Result cell state; used. |
| SD13 | 40 | `KItem ::= boot` | Initial control item; used. |
| CFG | 42–49 | `<mpy>` with `k`, `program`, `input`, `env`, `result` | Every cell is read or written. No heap/I/O is needed because the submitted body has no mutation, allocation, exception handler, or I/O. |
| FD01 | 53 | `eval(Expr,Map) [function]` | Partial by design; rules cover every expression/operator shape reached by `solution.mpy`. |
| FD02 | 54 | `negate(Value) [function]` | Partial by design; reached only on `VInt`. |
| FD03 | 55 | `asInt(Value) [function]` | Partial type projection; reached only on `VInt`. |
| FD04 | 56 | `asInts(Value) [function]` | Partial type projection; reached only on `VList`. |
| FD05 | 73 | `count(Int,IntSeq) [function,total]` | Total: empty/equal/unequal rules below are exhaustive and disjoint; recursion descends on the list. |
| SD14 | 80–83 | `KItem ::= exec | execStmt | choose | loop` | Internal control terms; all used. |

There are no local opaque declarations, `functional` declarations,
simplification rules, or syntax priorities in `semantic.k`.

## `semantic.k`: ordinary rules

| ID | Lines | Rule | Static decision |
|---|---:|---|---|
| SR01 | 58 | integer literal evaluation | Sound constructor-to-`VInt` interpretation. |
| SR02 | 59–60 | guarded name lookup | Sound for an environment containing `Value`s; the key guard prevents absent lookup. |
| SR03 | 61 | unary `-` evaluation | Sound for the sole used operator and integer operand. |
| SR04 | 62–63 | `list.count` call | Sound on `VList(IntSeq)`/`VInt`; exactly counts integer equality and has no side effects on the intended domain. |
| SR05 | 64–65 | `>=` comparison | Sound unbounded-integer comparison. |
| SR06 | 66–67 | `>` comparison | Sound unbounded-integer comparison. |
| SR07 | 69 | integer negation | Sound ordinary integer arithmetic. |
| SR08 | 70 | `VInt` projection | Sound constructor projection. |
| SR09 | 71 | `VList` projection | Sound constructor projection. |
| SR10 | 74 | count on empty list | Sound base case. |
| SR11 | 75 | count on equal head | Sound; adds one and structurally descends. |
| SR12 | 76–77 | count on unequal head | Sound; guard is the disjoint complement of SR11 and structurally descends. |
| SR13 | 85–88 | `boot` exact `search` binding | Sound entry adapter: matches the exact single function binding and binds its sole parameter to the input. |
| SR14 | 90 | execute empty statement list | Sound sequencing base case. |
| SR15 | 91 | execute head then tail | Sound left-to-right statement order. |
| SR16 | 93–94 | assignment | Sound for target `Name`; RHS uses the pre-update environment. |
| SR17 | 96–97 | evaluate `if` guard | Sound; used expressions are pure, and the selected branch is deferred to SR18/SR19. |
| SR18 | 98 | choose true branch | Sound and disjoint from SR19. |
| SR19 | 99 | choose false branch | Sound and disjoint from SR18. |
| SR20 | 101–102 | initialize `for` loop | Sound for the input list; the body does not mutate the iterable, so the `IntSeq` traversal matches Python. |
| SR21 | 103 | empty loop | Sound loop base case. |
| SR22 | 104–105 | one loop iteration | Sound: overwrites the target with the next integer, executes the body, then recurs on the tail. |
| SR23 | 107–109 | return | Sound for this top-level-function model: evaluates against the current environment, discards the remaining function continuation, stores the value, and clears the local environment. |

No SR rule asserts the task result directly, fabricates a fresh value, or
silently handles an unmodeled constructor used by the submitted program.

## `verification-core.k`: macros and mathematical functions

| ID | Lines | Declaration/rule | Static decision |
|---|---:|---|---|
| MD01/MR01 | 7, 10 | `searchProgram [macro]` | Definitional macro; fresh `kast --expand-macros` output is byte-identical to trusted regenerated `solution.mpy` parsing. |
| MD02/MR02 | 8, 11–14 | `searchBody [macro]` | Exact assignment/loop/return body. |
| MD03/MR03 | 9, 15–22 | `searchLoopBody [macro]` | Exact nested-if loop body. |
| FD06/FR01 | 27, 28–29 | `promote [function,total]`, qualifying case | Sound: chooses `I` exactly when frequency is at least `I` and `I` exceeds accumulator `A`. |
| FR02 | 30–31 | `promote`, complementary case | Sound; guard is Boolean negation of FR01, so the two rules are exhaustive and disjoint. |
| FD07/FR03 | 33, 34 | `scan [function,total]`, empty case | Sound base case returning the accumulator. |
| FR04 | 35 | `scan`, nonempty case | Sound structural fold; recursion descends on `IS`. |
| FD08/FR05 | 37–38 | `searchSpec [function,total]` | Sound definition: scans the entire list from initial answer `-1`. |
| FD09/FR06 | 40, 41 | `positive [function,total]`, empty case | Sound Boolean base case; unused by every submitted claim. |
| FR07 | 42 | `positive`, nonempty case | Sound structural conjunction; unused by every submitted claim. |

All four total functions have exhaustive, non-overlapping equations and
structural descent where recursive. There are no opaque or fresh symbols and no
simplification rules.

## `verification.k`: operational bridge

| ID | Lines | Rule | Static decision |
|---|---:|---|---|
| BR01 | 8–16 | Exact loop plus exact `return answer` continuation to `scan`, `[priority(40)]` | Operational bridge, but soundly justified: `LOOP-LEMMA-SPEC.loop-invariant` proves the token-identical reachability step against `VERIFICATION-CORE`, which imports no bridge. It matches every configuration cell and admits no arbitrary continuation. It clears `env` and sets `result` exactly as the fixed return rule does. Ground fixed-versus-extended executions agree for qualifying and rejecting outcomes, and changing the executed body from `>=` to `>` makes the bridge-free lemma fail with the expected residual. |

BR01 is the only local priority rule and the only ordinary rule in
`verification.k`. There are no local syntax/function/total/functional/opaque or
simplification declarations in that file.

## Reachability claims

| ID | Source | Scope |
|---|---|---|
| CL01 | `loop-lemma-spec.k:8–16` | Universal raw-semantics connection theorem for arbitrary `L`, remaining `IS`, accumulator `A`, and previous loop value, in the exact return continuation. |
| CL02 | `spec.k:7–11` | Prompt example one, result `2`. |
| CL03 | `spec.k:13–18` | Prompt example two, result `3`. |
| CL04 | `spec.k:20–24` | Prompt example three, result `-1`. |
| CL05 | `spec.k:29–33` | Every nonempty `IntSeq`: exact submitted program returns `searchSpec` of that list. |

All five claims have satisfiable starts. CL02–CL04 use their literal example
states; CL05 is satisfied by `H = 1, T = .Ints`; CL01 is satisfied, for example,
by `L = IS = cons(1,.Ints), A = -1`, with any previous integer.
