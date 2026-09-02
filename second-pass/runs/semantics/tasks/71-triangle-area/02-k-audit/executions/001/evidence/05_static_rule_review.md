# Static rule review ledger

## Inventory basis and per-rule decision

`05_rule_inventory.log` is the exhaustive source-level inventory. It contains
all 1,110 recognized K blocks, including 232 syntax declarations, one
configuration, five contexts, 700 rules, and five claims, with exact source
text and line numbers. Its global attribute scan found 155 function-bearing
blocks, 111 total-bearing blocks, 25 symbol-bearing blocks, 26
`no-evaluators`-bearing blocks, 49 priority-bearing blocks, 30 `owise`-bearing
blocks, 58 concrete-bearing blocks, and no `functional` or `simplification`
blocks.

The following decision applies to every inventoried rule in
`reference-semantics/`: it is byte-identical to the trusted supplied-semantics
mount and is therefore the fixed selected semantics, not a candidate proof
extension. Each rule was classified by its module below and checked for a
match, overlap, priority, or function-symbol dependency on the submitted
program's execution slice. Rules in unused construct modules do not match a
term produced by this program. This accepts those rules at the selected
semantics level; it does not assert that the entire supplied MPY language is a
universal model of every CPython behavior.

## Supplied-semantics modules

| Source | Inventory | Role | Relevance and decision |
|---|---:|---|---|
| `semantics.k` | 23 requires, 23 imports, 2 modules | Aggregates `MPY`; adds `MPY-KRUN` with concrete rules | Exact trusted baseline. Import graph is complete. |
| `syntax.k` | 16 syntax blocks | MPY AST | Declares every submitted construct. Strictness/sequence attributes implement the used evaluation order. |
| `core.k` | 1 configuration, 37 syntax, 46 rules | Values, cells, module load, sequencing, scope lookup, arguments, literals, helpers | Used. Configuration and the specific rules listed below preserve all visible cells. |
| `iter.k` | 1 syntax | Iteration protocol | Unused. |
| `range.k` | 2 syntax, 6 rules | Ranges | Unused. |
| `operators.k` | 2 contexts, 10 rules | Unary/binary/comparison dispatch | Used; dispatch is sort- and operator-specific. Heap-ref priority rules do not match integer/float operands here. |
| `int.k` | 1 syntax, 16 rules | Integer operations | Used for unary minus, addition, subtraction, multiplication, and `<=`; the equations agree with mathematical integers on this slice. |
| `bool.k` | 1 context, 13 rules | Truth and short-circuit `and`/`or` | Used. The head-only context plus complementary `truthy` guards implement left-to-right short circuit. Ref-specific priority rules do not match. |
| `float.k` | 34 syntax, 121 rules | Float literals, conversions, arithmetic, power, rounding, math helpers | Used through the six fixed opaque primitives listed below. Concrete twins are finite bridge evidence only. Unused float/math rules do not match this AST. |
| `str.k` | 5 syntax, 28 rules | Strings | Unused. |
| `set.k` | 6 syntax, 12 rules | Sets | Unused. |
| `list.k` | 5 syntax, 27 rules | Lists | Unused by the submitted program. |
| `tuple.k` | 4 syntax, 21 rules | Tuples and unpacking | Unused. |
| `subscript.k` | 2 contexts, 15 syntax, 40 rules | Indexing and slicing | Unused. Compiler warnings about total `valSeqAt` coverage are outside the execution slice. |
| `comprehension.k` | 3 syntax, 7 rules | Comprehensions | Unused. |
| `methods.k` | 27 syntax, 75 rules | String/list methods | Unused. |
| `controls.k` | 3 syntax, 34 rules | Assignment, conditionals, loops, imports | Assignment and `If` are used; loops/imports are unused. Cell-specific priority assignment cannot match the plain call frame. |
| `functions.k` | 4 syntax, 15 rules | Definition, parameter binding, return, frame pop | Used. The plain-closure path creates and later removes one scope and restores `env`, `scopeLoc`, stack, and return state. |
| `builtins.k` | 38 syntax, 137 rules | Builtins | Only the generic builtin declaration/dispatch support is relevant; `round`'s value equation is in `float.k`. Other builtins are unused. |
| `call.k` | 3 syntax, 21 rules | Callee/argument evaluation and dispatch | Used for the closure and `round`. Arguments evaluate left to right. Ref/method/collection paths do not match. |
| `sort.k` | 6 syntax, 19 rules | Sorting | Unused. |
| `assert.k` | 3 rules | Concrete smoke assertions | Not used by the symbolic target claims; used only by reviewer concrete tests. |
| `dict.k` | 12 syntax, 28 rules | Dictionaries | Unused. |
| `concrete.k` | 5 syntax, 16 rules | LLVM-only concrete helpers | Not imported by the proof module; used only by concrete testing through `MPY-KRUN`. |

No unused rule introduces an equation for one of the proof-local symbols, and
no used term reaches an unused construct's left-hand side.

## Submitted construct-to-rule map

| Submitted construct | Declaration/evaluation |
|---|---|
| `Module`, `FuncDef`, `Params`, statement list | `syntax.k:53-61`; `core.k:124-127`; `functions.k:14-16` |
| `Name`, integer/float literals | `syntax.k:9-12`; `core.k:130-154,193-196`; `float.k:19-21` |
| `UnaryOp("-")` | `syntax.k:14`; `operators.k:10`; `int.k:7` |
| `BinOp("+","-","*","/","**")` | `syntax.k:15` (left-to-right `seqstrict`); `operators.k:12`; `int.k:9-17`; `float.k:30-32,103-121,132-139` |
| `Compare("<=")` | `syntax.k:30-32`; `operators.k:15-17`; `int.k:23` |
| three-way `BoolOp("or")` | `syntax.k:16`; `bool.k:16-25` |
| `If` | `syntax.k:49`; `controls.k:51-54` |
| `Assign(Name("s"), ...)` | `syntax.k:41`; `controls.k:9-18` |
| `Call(Name("round"), value, 2)` | `syntax.k:28`; `core.k:156-191`; `call.k:19-32,69-76`; `float.k:223-228` |
| `Return` | `syntax.k:50`; `functions.k:78-89` |

The program allocates a fresh call scope but no heap object. Parameter binding
updates only that scope. `s` is written to it. Return stores the result,
discards the remaining function continuation, pops the exact frame, removes
the call scope, and restores caller cells. The target claims pin `env`,
`scopes`, `scopeLoc`, `heap`, `heapLoc`, `stack`, and `ret`; omitted `exc` and
`exit-code` cells are not read or written on this execution slice.

## Candidate `verification.k` extensions

There are exactly five local syntax declarations and five equations, with no
local `total`, `functional`, opaque `symbol`, `no-evaluators`, priority,
`owise`, concrete, or simplification attribute.

| Extension | Class and complete decision |
|---|---|
| `triangleAreaBody` | Definitional AST constant. Its sole equation is terminating, has no guard or overlap, and expands to the exact parsed statement list in `solution.mpy`. `04_ast_pin.log` mechanically composes the module and records equal normalized hashes. |
| `triangleAreaClosure` | Definitional value constant. Its sole equation fixes parameters `a,b,c`, the exact body, and defining environment 0. It does not intercept a call or bypass execution. |
| `triangleAreaModule` | Definitional module constant. Its sole equation wraps the exact function definition. The loader claim independently proves that fixed module-loading semantics installs `triangleAreaClosure`. |
| `semiPerimeter(A,B,C)` | Definitional summary. Its exhaustive equation is exactly the structural fixed-semantics result of `(A+B+C)/2` for integer operands: `divII(A+B+C,2)`. It replaces no program redex. |
| `expectedArea(A,B,C)` | Definitional summary. Its exhaustive equation expands to the precise sequence of `divII`, `intToF`, `subF`, `mulF`, `powF(...,0.5)`, and `roundFN(...,2)` terms produced after the stored `s` is looked up. It replaces no program redex and introduces no free value. |

There is no operational bridge and no result-bearing oracle introduced by the
candidate. Each function has one right-sort-covering equation, so there are no
same-symbol guard overlaps. The exponent body-sensitivity mutation in
`05_verification-body-mutation.k` rebuilt successfully and made the valid proof
fail on the expected `0.5` versus `1.0` term equality.

## Fixed opaque primitives used by the result

`divII`, `intToF`, `subF`, `mulF`, `powF`, and `roundFN` are
`[function,total,symbol(...),no-evaluators]` in the trusted supplied
`float.k`, with `[concrete]` LLVM equations. They are not candidate-created.
They affect the final returned value, so the symbolic proof establishes the
exact composition of these primitives, not a backend-independent numerical
theorem about Heron's formula or Python rounding.

Fresh isolated concrete configurations agreed with canonical Python on all 150
cases in `05_k_bridge_cases.py`. A sequential 150-assert program exposed a
separate supplied-runtime state/scale limitation: after 99 preceding calls,
the concrete backend returned `2.01` for `(2,3,3)`, while the isolated case
returned `2.83`. The target claims are all fresh-entry claims, so the isolated
tests are the matching empirical bridge; repeated calls in one loaded module
remain outside the proved scope and are a documented concern.
