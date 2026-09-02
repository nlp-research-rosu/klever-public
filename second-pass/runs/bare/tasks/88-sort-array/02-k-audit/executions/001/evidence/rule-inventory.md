# Exhaustive local K declaration and rule inventory

Source line numbers refer to the scratch copies, which are hash-identical to
the candidate source files.

## Declaration inventory

| ID | Source | Declaration | Audit |
|---|---|---|---|
| D01 | `semantic.k:8` | `Module ::= Module(Stmt)` | Used by the submitted `.mpy`; constructor grammar only. |
| D02 | `semantic.k:10-11` | `Stmt ::= FuncDef(...) \| Return(...)` | Both alternatives are used; sufficient for the one-function program. |
| D03 | `semantic.k:13` | `Params ::= Params(String)` | Used by the submitted function. |
| D04 | `semantic.k:15-25` | `Expr` constructors: `Name`, `Int`, 2- and 3-argument `Call`, `KwArg`, `BoolOp`, `Compare`, `CmpOp`, `BinOp`, `UnaryOp`, `Subscript` | Every submitted expression constructor is declared. The grammar is intentionally partial outside this program. |
| D05 | `semantic.k:27-28` | `IntList ::= nil \| cons(Int,IntList)` | Models finite integer lists. |
| D06 | `semantic.k:30-33` | `Val ::= ListVal \| IntVal \| BoolVal \| NoneVal` | Covers all target values. There is no heap or identity representation. |
| D07 | `semantic.k:43-45` | `KItem ::= invoke \| execute \| finish` | Internal control forms for the one function and return. |
| D08 | `semantic.k:47-52` | `<py><k>...<input>...<result>...</py>` configuration | `$PGM` is followed by an invocation on `$INPUT`; input is immutable and result starts at `NoneVal`. |
| D09 | `semantic.k:62` | `eval(Expr,Map) [function]` | Partial by design; all target occurrences have matching rules. Not declared `total`. |
| D10 | `semantic.k:92-99` | `lenVal`, `sortedVal`, `andVal`, `nonemptyVal`, `compareVal`, `binVal`, `unaryVal`, `subscriptVal`, all `[function]` | Transparent helpers, not opaque. They are partial outside target types/operators. |
| D11 | `semantic.k:120-121` | `ilen`, `ilast`, both `[function,total]` | `ilen` is truthfully total. `ilast` is totalized with a false empty-list equation; see U02. |
| D12 | `semantic.k:129-133` | `sortAsc`, `insertAsc`, `sortFlag`, `reverse`, `reverseAcc`, all `[function,total]` | Guard coverage, disjointness, and structural descent are complete. |
| D13 | `verification.k:7` | `expectedSort(IntList) [function,total]` | Transparent exact-result specification; two constructor cases cover `IntList`. |
| D14 | `verification.k:13` | `endpointEven(IntList) [function]` | Intentionally defined only for nonempty lists, its only use. |
| D15 | `verification.k:20-22` | `nonnegative`, `ascending`, `descending`, all `[function,total]` | Constructor-complete observers. Only `nonnegative` is used by a claim. |

There are no local `[functional]`, `[simplification]`, `[concrete]`,
`[priority]`, `[owise]`, or opaque declarations, and no local lemmas or
ordinary proof-module rewrites. `spec.k` contains exactly four reachability
claims.

## Rule inventory

`S` means the equation/rewrite is sound on its complete matched domain at this
semantics level. `U` means false relative to Python and has a preserved witness.

| ID | Source | Rule | Decision |
|---|---|---|---|
| R01 | `semantic.k:54-55` | matching module/function plus invocation becomes `execute(BODY,P|->V)` | S: binds the sole parameter and preserves any continuation. |
| R02 | `semantic.k:57` | `execute(Return(E),ENV) => finish(eval(E,ENV))` | S for the only statement body; continuation is framed. |
| R03 | `semantic.k:58` | exact-cell `finish(V)` empties `<k>` and stores `V` | S: it does not discard a continuation because the `<k>` cell is not framed. |
| R04 | `semantic.k:63` | bound `Name(X)` lookup | S; the target environment contains exactly `array`. |
| R05 | `semantic.k:64` | integer literal to `IntVal` | S. |
| R06 | `semantic.k:66-67` | `len` call dispatch to `lenVal` | S for the target builtin binding assumption. |
| R07 | `semantic.k:69-70` | `sorted(...,reverse=...)` dispatch to `sortedVal` | S as a pure-value model; allocation identity is not represented. |
| R08 | `semantic.k:72-73` | `and` dispatch to `andVal` with RHS unevaluated | S and preserves short-circuit control. |
| R09 | `semantic.k:77-78` | `len(E) > 0` dispatch to `nonemptyVal` | S for `IntList`; a specialized truthful equation. |
| R10 | `semantic.k:80-81` | integer equality dispatch | S for the target occurrence. |
| R11 | `semantic.k:83-84` | binary-operation dispatch | S structurally; target operators are handled below. |
| R12 | `semantic.k:86-87` | unary-operation dispatch | S structurally; target `-` is handled below. |
| R13 | `semantic.k:89-90` | subscription dispatch | Structurally faithful, but inherits U01/U02 for empty `[-1]`. |
| R14 | `semantic.k:101` | list length via `ilen` | S. |
| R15 | `semantic.k:103` | sorted list via `sortFlag` | S as the modeled value of Python `sorted`; transparent insertion-sort equations fix the result. |
| R16 | `semantic.k:105` | `false and E => false` without evaluating `E` | S; essential for the empty case. |
| R17 | `semantic.k:106` | `true and E => eval(E)` | S. |
| R18 | `semantic.k:108` | empty list is not nonempty | S. |
| R19 | `semantic.k:109` | a `cons` list is nonempty | S. |
| R20 | `semantic.k:111` | integer `==` | S. |
| R21 | `semantic.k:113` | integer `+` | S for unbounded Python integers/K `Int`. |
| R22 | `semantic.k:114` | integer `%` | S on the target divisor `2`; the helper is deliberately partial for zero. |
| R23 | `semantic.k:115` | unary integer minus | S. |
| R24 | `semantic.k:117` | index `0` of a `cons` list | S. |
| R25 (U01) | `semantic.k:118` | every list, including `nil`, indexed at `-1` becomes `IntVal(ilast(L))` | U: it omits Python's empty-list `IndexError`. Together with U02 it returns `IntVal(0)` for `[][-1]`. |
| R26 | `semantic.k:122` | `ilen(nil) => 0` | S. |
| R27 | `semantic.k:123` | `ilen(cons(_,IS)) => 1 + ilen(IS)` | S; structural descent. |
| R28 | `semantic.k:124` | last of a singleton | S. |
| R29 | `semantic.k:125` | last of a list of length at least two recurses on the tail | S; structural descent. |
| R30 (U02) | `semantic.k:126` | `ilast(nil) => 0` | U: false totalization of an exceptional Python operation. Same concrete witness as U01. |
| R31 | `semantic.k:135` | ascending sort of empty list | S. |
| R32 | `semantic.k:136` | ascending insertion-sort recursion | S; structural descent through `IS`. |
| R33 | `semantic.k:138` | insert into empty list | S. |
| R34 | `semantic.k:139` | insert before head when `I <= J` | S. |
| R35 | `semantic.k:140` | recurse past head when `I > J` | S; R34/R35 guards are disjoint and exhaustive over `Int`. |
| R36 | `semantic.k:142` | `reverse=false` selects ascending sort | S. |
| R37 | `semantic.k:143` | `reverse=true` reverses the ascending sort | S. |
| R38 | `semantic.k:145` | reverse initializes accumulator | S. |
| R39 | `semantic.k:146` | reverse accumulator base case | S. |
| R40 | `semantic.k:147` | reverse accumulator step | S; structural descent. |
| R41 | `verification.k:9` | `expectedSort(nil) => nil` | S and constructor-complete with R42. |
| R42 | `verification.k:10-11` | nonempty expected result uses endpoint parity and `sortFlag` | S as an exact executable result, but it reuses the semantic sorter. |
| R43 | `verification.k:14-15` | endpoint-even predicate | S on its nonempty domain. |
| R44 | `verification.k:23` | `nonnegative(nil) => true` | S. |
| R45 | `verification.k:24` | element nonnegativity conjoined recursively | S; structural descent. |
| R46 | `verification.k:26` | empty list is ascending | S. |
| R47 | `verification.k:27` | singleton is ascending | S. |
| R48 | `verification.k:28-29` | adjacent `<=` plus recursive ascending | S. |
| R49 | `verification.k:31` | empty list is descending | S. |
| R50 | `verification.k:32` | singleton is descending | S. |
| R51 | `verification.k:33-34` | adjacent `>=` plus recursive descending | S. |

## False-conclusion witness for U01/U02

`last_empty_probe.py` is translated with the trusted translator into
`last_empty_probe.mpy`; its body is `return array[-1]`. On the intended
non-negative-integer-list input `[]`, CPython raises `IndexError`, while the
fresh K definition terminates with `<result> IntVal(0) </result>`.

Commands and outputs: `last-empty-translate.log`, `last-empty-python.log`, and
`last-empty-k.log`.

The submitted source does not reach this bad rule on `[]`: R16 short-circuits
the parity expression. That limits the witness's effect on the submitted path,
but it does not make U01/U02 truthful on their declared domain and does not
satisfy the required global proof-extension/semantics audit.
