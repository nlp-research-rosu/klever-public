# Exhaustive local K inventory

Scope: scratch copies of `semantic.k`, `verification.k`, and `spec.k`. Line
numbers below are those of the immutable candidate sources. Imported K domains
are accounted for separately as trusted primitives; this inventory contains
every local declaration and rule.

## Declarations

| ID | Location | Declaration | Review |
|---|---|---|---|
| D1 | `semantic.k:7` | `Program ::= Module(Stmts)` | Exact submitted top-level form. |
| D2 | `semantic.k:8` | `Stmts ::= List{Stmt,""}` | Ordered statement sequence; the generated empty-list unit is `.Stmts`. |
| D3 | `semantic.k:10-12` | `Stmt ::= FuncDef \| If \| Return` | Covers every submitted statement form. |
| D4 | `semantic.k:14` | two-name `Params` | Covers the exact entry and recursive signature. |
| D5 | `semantic.k:16` | comma-separated `Exprs` | Supports the submitted one- and two-argument calls. |
| D6 | `semantic.k:17-21` | `Expr ::= Name \| Int \| BinOp \| Compare \| Call` | Covers every submitted expression; `Int` is locally extra and unused. |
| D7 | `semantic.k:22` | `CmpOp(String,Expr)` | Covers the submitted `<` comparison. |
| D8 | `semantic.k:32-34` | `Value ::= intVal \| strVal \| boolVal` | Sufficient result domain for the submitted body. |
| D9 | `semantic.k:36` | `appendStmts(Stmts,Stmts) [function]` | Definitional statement-list append. |
| D10 | `semantic.k:43-53` | 11 internal `KItem` forms: `call`, `exec`, `eval`, `branch`, `cmpLeft`, `cmpRight`, `binLeft`, `binRight`, `toString`, `callArgLeft`, `callArgRight` | Explicit control frames; none is opaque. |
| D11 | `semantic.k:55-56` | one-cell `<k>` configuration initialized with `call($PGM,"change_base",intVal($X),intVal($BASE))` | Adequate for this pure program; no mutable state or I/O exists in the body. |
| D12 | `verification.k:9` | `baseString(Int,Int) [function] : String` | Definitional mathematical summary; it does not replace operational execution. |
| C1 | `spec.k:9-31` | one all-path reachability claim | Executes an exact constructor copy of the submitted function under `X >= 0`, `2 <= B <= 9`, preserving arbitrary `CONT`, and constrains the result to `strVal(baseString(X,B))`. |

There are no local `[total]`, `[functional]`, `[simplification]`,
`[simplifier]`, `[priority]`, `[owise]`, `[anywhere]`, macro, or opaque
declarations/rules. The only attributes are the two `[function]` declarations
D9 and D12.

## Rules

| ID | Location | Rule effect | Classification and decision |
|---|---|---|---|
| S1 | `semantic.k:37` | append empty list | True terminating equation. |
| S2 | `semantic.k:38` | append nonempty list recursively | True equation; decreases the first list; disjoint from S1. |
| S3 | `semantic.k:59-65` | select the sole named function, bind two parameters, begin its body | Faithful on the exact submitted module, distinct parameter names, and exact call binding. |
| S4 | `semantic.k:67` | empty statement execution returns `strVal("")` | Not faithful to general Python fall-through (`None`), but unreachable from the submitted body for every input: both paths encounter `Return`. No intended-input false conclusion uses it. |
| S5 | `semantic.k:72` | evaluate a return expression and discard remaining statements | Faithful return control for this subset; the surrounding K continuation is preserved. |
| S6 | `semantic.k:74-78` | evaluate an `If` guard before branching | Faithful evaluation order. |
| S7 | `semantic.k:79-83` | true branch prepended to remaining statements | Faithful control flow. |
| S8 | `semantic.k:84-88` | false branch prepended to remaining statements | Faithful control flow. |
| S9 | `semantic.k:91` | integer AST literal to `intVal` | Faithful but unused by the submitted body. |
| S10 | `semantic.k:92` | name lookup from the explicit environment map | Faithful for bound submitted names; unbound names stop visibly. |
| S11 | `semantic.k:95-99` | schedule comparison left operand | Faithful left-to-right order. |
| S12 | `semantic.k:100-104` | schedule comparison right operand | Faithful left-to-right order and operand retention. |
| S13 | `semantic.k:105-106` | compute `I <Int J` | Operand orientation is correct for submitted `x < base`. |
| S14 | `semantic.k:109-113` | schedule binary left operand | Faithful left-to-right order. |
| S15 | `semantic.k:114-118` | schedule binary right operand | Faithful left-to-right order and operand retention. |
| S16 | `semantic.k:119-121` | nonzero integer floor division | Agrees with Python on the theorem domain `X >= 0`, `B >= 2`. |
| S17 | `semantic.k:122-124` | nonzero integer remainder | Agrees with Python on the theorem domain `X >= 0`, `B >= 2`. |
| S18 | `semantic.k:125-126` | string concatenation | Faithful and order-correct. |
| S19 | `semantic.k:129-133` | evaluate the argument of one-argument builtin `str` | Correct for the unshadowed builtin binding in this closed module. |
| S20 | `semantic.k:134` | `str(int)` via `Int2String` | Faithful for mathematical integers, including the submitted base-case values. |
| S21 | `semantic.k:136-140` | evaluate first argument of an ordinary two-argument call | Faithful order. |
| S22 | `semantic.k:141-145` | evaluate second argument, retaining the first | Faithful order. |
| S23 | `semantic.k:146-150` | invoke the named module function with both values | Faithful exact recursive binding and preserves the caller continuation. |
| V1 | `verification.k:11-12` | `baseString(X,B) = Int2String(X)` when `X < B` | True on its guard; for the theorem domain this is the base-representation case. |
| V2 | `verification.k:14-16` | recursive quotient representation plus remainder digit when `B <= X` and `B > 0` | True on its guard; on the theorem domain `B >= 2`, quotient strictly decreases. |

V1 and V2 have disjoint guards. They cover every use under C1. D12 is partial
outside that domain but is not declared total. No operational bridge or oracle
rewrites a submitted program term; C1 itself is the execution-to-summary
connection theorem.

## Construct coverage

`solution.mpy` uses `Module`, `FuncDef`, `Params`, `If`, `Compare`, `Name`,
`CmpOp("<",...)`, `Return`, one-argument `Call` to `str`, two-argument
recursive `Call`, `BinOp("//")`, `BinOp("%")`, `BinOp("+")`, and empty/nonempty
`Stmts`. These map respectively to D1-D7 and operational rules S1-S3, S5-S8,
S10-S23. Tests with `x < base` and `x >= base` exercise both branches. S4 and
S9 are the only local operational rules not needed by the submitted program.

## Language-model boundary witness

The operational rules use an unbounded K continuation stack. They do not model
CPython's finite recursion limit or `RecursionError`. At positive satisfying
input `X = 2**997`, `B = 2`, fresh K execution reaches the 998-character
binary string, while CPython 3.10.12 with recursion limit 1000 raises
`RecursionError`. This is not a false local rewrite equation in the idealized
subset; it is a material generated-semantics-versus-real-Python adequacy gap.
See `stage5_k_recursion_boundary.log`.
