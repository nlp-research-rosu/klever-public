# Exhaustive local K declaration and rule inventory

Scope: fresh source copies of `semantic.k`, `verification.k`, and `spec.k`.
Imported K builtin declarations are not repeated here; they are accounted for
as trusted primitives in the review. There are no generated helper K files.

## Local syntax and attributes in `semantic.k`

The following are all local syntax declarations:

| Lines | Sort | Every declared alternative | Attributes |
|---|---|---|---|
| 8–15 | sort declarations | `Program`, `Stmt`, `Stmts`, `Expr`, `Params`, `Cmp`, `Index`, `Bound` | none |
| 17 | `Program` | `Module(Stmts)` | `symbol(Module)` |
| 19–20 | `Stmts` | `Stmt`; `Stmt Stmts` | second alternative `symbol(StmtsCons)` |
| 22 | `Params` | `Params(String)` | `symbol(Params)` |
| 24–27 | `Stmt` | `FuncDef(String,Params,Stmts)`; `If(Expr,Stmts,Stmts)`; `Return(Expr)` | `symbol(FuncDef)`, `symbol(If)`, `symbol(Return)` |
| 29–36 | `Expr` | `Int(Int)`; `Name(String)`; `ListExpr()`; `UnaryOp(String,Expr)`; `BinOp(String,Expr,Expr)`; `Compare(Expr,Cmp)`; `Call(Expr,Expr)`; `Subscript(Expr,Index)` | respective `symbol(Int)`, `Name`, `ListExpr`, `UnaryOp`, `BinOp`, `Compare`, `Call`, `Subscript` |
| 38 | `Cmp` | `CmpOp(String,Expr)` | `symbol(CmpOp)` |
| 39–40 | `Index` | `Expr`; `Slice(Bound,Bound,Bound)` | `symbol(Slice)` on the second |
| 41–42 | `Bound` | `Expr`; `NoBound` | `symbol(NoBound)` on the second |
| 44–45 | sort declarations | `Value`, `VList` | none |
| 46–48 | `Value` | `IntV(Int)`; `BoolV(Bool)`; `ListV(VList)` | respective `symbol` attributes |
| 49–50 | `VList` | `VNil`; `VCons(Int,VList)` | `symbol(VNil)`, `symbol(VCons)` |
| 52–57 | `Value` | `list()` and `list(Int,...)` for arities 1 through 5 | all `macro` |
| 78–79 | sort declarations | `Function`, `Frame` | none |
| 80 | `Function` | `function(String,Stmts)` | `symbol(function)` |
| 81 | `Frame` | `frame(Map)` | `symbol(frame)` |
| 83–94 | `KItem` | `invoke`; `finishK`; `callK`; `returnK`; `ifK`; `unaryK`; `binLeftK`; `binRightK`; `compareLeftK`; `compareRightK`; `subscriptK`; `indexK` with the argument sorts shown in source | respective `symbol` attributes |

There are no local `function`, `total`, `functional`, `simplification`,
priority, `owise`, SMT-hook, or opaque declarations in `semantic.k`.

The configuration at lines 96–102 has exactly four state components beneath
`<mpy>`: computation `<k>`, global function map `<funs>`, current local
environment `<env>`, and caller-environment list `<stack>`. There is no heap,
output, exception, or resource-limit cell.

## Every rule in `semantic.k`

| Lines | Rule | Classification and audit result |
|---|---|---|
| 59 | `list() => ListV(VNil)` | Exact test-input macro expansion; sound. |
| 60 | `list(I1) => ListV(VCons(I1,VNil))` | Exact arity-1 expansion; sound. |
| 61 | arity-2 `list` expansion | Exact constructor expansion; sound. |
| 62–63 | arity-3 `list` expansion | Exact constructor expansion; sound. |
| 64–65 | arity-4 `list` expansion | Exact constructor expansion; sound. |
| 66–67 | arity-5 `list` expansion | Exact constructor expansion; sound. |
| 104 | `Module(S1:Stmt S2:Stmt) => S1 ~> S2` | Loads the submitted module's exactly two definitions in source order. It intentionally does not model other module lengths. Sound for this program. |
| 106–107 | `FuncDef` updates `<funs>` and disappears | Correct for the two distinct top-level function definitions. The stored body and parameter are unchanged. |
| 109 | `invoke(F,V) => V ~> callK(F) ~> finishK` | Evaluates the already supplied argument value, invokes the named function, then requires a final value. Sound for the audit entry. |
| 110 | `V ~> finishK => V` | Removes only the outer invocation marker; sound. |
| 112–115 | `V ~> callK(F) => BODY`, function lookup, fresh one-binding environment, caller push | Exact binding/state transition for this program's one-argument global functions. No body is skipped. |
| 117–119 | `V ~> returnK => V`, restore caller environment, pop frame | Correct for every reachable `Return` in the submitted bodies: each return is the sole statement of its selected branch. |
| 121 | `If` evaluates test before selecting branch | Correct Python evaluation order. |
| 122 | true `ifK` selects `THEN` | Sound and disjoint from line 123. |
| 123 | false `ifK` selects `ELSE` | Sound and disjoint from line 122. |
| 124 | `Return(E) => E ~> returnK` | Evaluates the expression before returning; sound in each reachable branch. |
| 126 | `Int(I) => IntV(I)` | Exact unbounded-integer literal injection. |
| 127–128 | `Name(X)` reads `<env>` | Correct for `arr` and `num`, the only expression names. |
| 129 | `ListExpr() => ListV(VNil)` | Exact meaning of the only list literal, `[]`. |
| 131 | `UnaryOp(OP,E)` evaluates operand first | Correct order. Unsupported operators then remain visibly stuck. |
| 132 | unary `"-"` negates an integer | Sound for mathematical integers. |
| 134 | `BinOp` begins with left operand | Correct left-to-right order. |
| 135 | after left value, evaluates right operand | Correct order and remembers the left value. |
| 136 | integer `"+"` | Sound unbounded integer addition. |
| 137–138 | integer `"%"`, nonzero divisor | K t-remainder is sound on all reachable uses because both dividend and divisor are positive. The rule is broader than Python for negative dividends; see the containment note below. |
| 139–140 | integer `"//"`, nonzero divisor | K t-division is sound on all reachable uses because both dividend and divisor are positive. The rule is broader than Python for negative dividends; see the containment note below. |
| 142–143 | `Compare` begins with left operand | Correct order for every submitted comparison. |
| 144–145 | evaluates the comparator after the left value | Correct order and retains the left value. |
| 147–148 | integer `<`, true guard | Mathematically sound; complementary to lines 149–150. |
| 149–150 | integer `<`, false guard | Mathematically sound; guards are exhaustive/disjoint. |
| 151–152 | integer `>`, true guard | Mathematically sound; complementary to lines 153–154. |
| 153–154 | integer `>`, false guard | Mathematically sound; guards are exhaustive/disjoint. |
| 156–157 | empty list equals empty list | Sound for the submitted `arr == []`. |
| 158–159 | nonempty list does not equal empty list | Sound and complementary for all `VList` values. |
| 161 | `Call(Name(F),ARG)` evaluates the argument then calls `F` | Correct for the two statically global, unshadowed function names in this program. |
| 163 | `Subscript(BASE,IDX)` evaluates base first | Correct order. |
| 164–165 | integer index expression evaluates after list base | Correct order for the literal index `0`. |
| 166 | index `0` of nonempty list returns its head | Sound; the program reaches it only after proving nonemptiness. |
| 167–169 | exact slice `[1:]` returns the tail | Sound value abstraction for immutable `VList`; allocation identity is unobservable in this nonmutating program. |

Containment note, not an intended-domain unsoundness finding: K `/Int` and
`%Int` round/remainder toward zero, while Python `//` and `%` differ for a
negative dividend and positive divisor. The concrete off-path witness is
`-11 /Int 10 = -1`, `-11 %Int 10 = -1`, versus Python `-11 // 10 = -2`,
`-11 % 10 = 9`. The submitted body never sends a negative dividend to either
rule: under `num < -9` it divides/modulos `-num > 0`, and under `num > 9` it
uses `num > 0`. Evidence is in `negative-*-krun-module-int.log` and
`python-negative-arithmetic.log`.

Two additional deliberately narrow modeling limits do not enable a false
conclusion for this fixed program: the `Return` rule does not discard a
trailing statement (none is reachable in a selected body), and the `Call` rule
resolves only the global function map (neither `digit_sum` nor `count_nums` is
shadowed). These are scope limitations, not witnessed unsoundness on the
intended input domain.

## Local syntax, functions, and every rule in `verification.k`

| Lines | Extension | Attributes/class | Complete audit |
|---|---|---|---|
| 9–10, 12–26 | `digitBody`, `countBody` syntax and rules | two `Stmts` macros | Exact constructor copies of the two submitted bodies. They do not skip execution. |
| 44–48 | `solutionProgram` syntax and rule | `Program` macro | Expands to the exact two-function `Module`. Fresh `kast --expand-macros` KORE is byte-identical to parsing submitted `solution.mpy`. |
| 50–53 | `solutionFuns` syntax and rule | `Map` macro | Exact map produced by executing those two `FuncDef` nodes; no oracle or fresh value. |
| 58–71 | `signedDigitSum(Int)` and three rules | `function`, `total`, `symbol` | Definitional mathematical summary. Guards `N < -9`, `N > 9`, and `-9 <= N <= 9` are exhaustive and pairwise disjoint. Recursion strictly decreases absolute decimal magnitude. No operational term rewrites to this function; universal claim 1 connects real helper execution to it. |
| 73–74, 80–82 | `countPositive(VList)` and two rules | `function`, `total`, `symbol` | Definitional structural count. `VNil`/`VCons` cover all `VList`; recursion strictly decreases list length. Claims 2–4 connect actual recursive execution to it. |
| 75–79 | `boolToInt(Bool)` and two rules | `function`, `total`, `symbol`, `smt-hook((ite #1 1 0))` | `true -> 1`, `false -> 0` are exhaustive/disjoint and agree with the SMT `ite` encoding. It is not opaque. |

There are no local ordinary operational bridges, simplification rules,
priority rules, `owise` rules, `functional` declarations, fresh symbols,
unconstrained opaque symbols, or rules encoding a result without executing a
program body. All macros are compile-time names. All three total functions have
complete, nonoverlapping equations and terminating recursion.

## Construct coverage map for submitted `solution.mpy`

| Submitted construct | Declaration | Runtime behavior |
|---|---|---|
| `Module` with two `FuncDef` nodes | lines 17, 24 | lines 104, 106–107 |
| one-parameter `Params` | line 22 | consumed by lines 106–107 and 112–115 |
| `If` / `Return` | lines 26–27 | lines 121–124, 117–119 |
| `Int`, `Name`, empty `ListExpr` | lines 29–31 | lines 126–129 |
| unary `-` | line 32 | lines 131–132 |
| binary `+`, `%`, `//` | line 33 | lines 134–140 |
| comparisons `<`, `>`, `==` via `CmpOp` | lines 34, 38 | lines 142–159 |
| single-argument global `Call` | line 35 | lines 161, 112–119 |
| subscript `0` | lines 36, 39 | lines 163–166 |
| exact slice `[1:]` | lines 36, 40–42 | lines 163, 167–169 |
| integer-list input values | lines 46, 48–50 | equality/index/slice rules above |

Every submitted syntactic node has both a declaration and a reachable semantic
rule path. Unsupported alternatives stop rather than fabricate a value.

## Claim inventory (`spec.k`)

1. Lines 8–13: universal real-execution connection for `digit_sum`.
2. Lines 16–21: empty-list real-execution case for `count_nums`.
3. Lines 24–30: nonempty positive-head recursive case.
4. Lines 34–40: nonempty nonpositive-head recursive case.
5. Lines 44–49: clean-state end-to-end empty entry.
6. Lines 51–57: clean-state end-to-end positive-head entry.
7. Lines 59–65: clean-state end-to-end nonpositive-head entry.

Claims 1–4 are the mutually supporting induction/connection layer; claims 5–7
pin clean program loading and invocation. The aggregate module is the intended
positive target. Stripping claims 1–4 from one another removes required
induction hypotheses; the recorded standalone diagnostics are therefore
dependency checks, not alternate target proofs.
