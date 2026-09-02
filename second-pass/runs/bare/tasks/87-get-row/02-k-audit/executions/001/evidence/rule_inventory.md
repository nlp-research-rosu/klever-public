# Reviewer rule and declaration inventory

Source hashes are in `stage01_integrity.log`. Line numbers below refer to the
candidate source copies in `/tmp/audit-work/87-get-row/source/`.

## Global attribute scan

- Local rules: 50 in `semantic.k`, 19 in `verification.k`.
- Reachability claims: 11 in `spec.k`.
- `[function]`: `vlen`, `vconcat`, `vnth`, `encodeInts`, `encodeMatrix`,
  `rowCoords`, `coordStep`, `matrixCoords`, `addCoord`, `expectedFlags`.
- `[total]`: `rowCoords`, `coordStep`, `addCoord`, `expectedFlags`.
- `[macro]`: `solutionProgram`, `getRowBody`, `promptMatrix`, `thirdMatrix`,
  `promptInput`, `thirdInput`.
- No local `[functional]`, `[simplification]`, `[concrete]`, `[owise]`,
  priority, `anywhere`, `trusted`, or opaque declarations/rules.

## Local syntax and configuration declarations

### `semantic.k`

| ID | Lines | Declaration and productions | Use/judgment |
|---|---:|---|---|
| S01 | 6 | `Program ::= Module(Stmts)` | Exact translated root; used and covered. |
| S02 | 7 | `Stmts ::= List{Stmt,""}` | Statement sequence including `.Stmts`; used and covered. |
| S03 | 8 | `Strings ::= List{String,","}` | Parameters; used by registration/start matching. |
| S04 | 9 | `Params ::= Params(Strings)` | Used and covered as stored/matched data. |
| S05 | 11-16 | `Stmt ::= FuncDef | Assign | For | While | If | Return` | Every alternative used by the submitted program and covered. |
| S06 | 18 | `Exprs ::= List{Expr,","}` | Empty/singleton/tuple expression lists; used and covered. |
| S07 | 19 | `CmpOps ::= List{CmpOp,","}` | Submitted comparisons contain one item; covered for that used shape. |
| S08 | 20-28 | `Expr ::= Name | Int | Bool | ListExpr | TupleExpr | BinOp | Compare | Subscript | Call` | All but `Bool` occur in `solution.mpy`; all have a rule, with operator/type coverage scoped below. |
| S09 | 29 | `CmpOp ::= CmpOp(String,Expr)` | Used for `>=` and `==`; covered. |
| S10 | 38 | `VList ::= vnil | vcons(Value,VList)` | Finite list representation; used throughout. |
| S11 | 39-42 | `Value ::= pyInt | pyBool | pyList | pyTuple` | Exactly the runtime value kinds needed. |
| S12 | 44 | `Function ::= function(Params,Stmts)` | Top-level function registry representation. |
| S13 | 45 | `Result ::= noResult | returned(Value)` | Top-level result state. |
| S14 | 46 | `Args ::= pyArgs(Value,Value)` | Exact two-argument entry harness. |
| C01 | 48-55 | `<py>` configuration with `<k>`, `<args>`, `<env>`, `<functions>`, `<result>` | Every cell is read or written. It models a single top-level call; no heap/I/O/exceptions are needed by the submitted program on the integer-matrix domain. |
| S15 | 57-78 | 22 `KItem` continuations: `start`, `exec`, `execStmt`, `eval`, `assignTo`, `forReady`, `forLoop`, `whileLoop`, `whileGuard`, `ifGuard`, `evalExprs`, `evalExprsTail`, `prependValue`, `asTuple`, `binLeft`, `binRight`, `cmpLeft`, `cmpRight`, `subscriptBase`, `subscriptIndex`, `doLen`, `doReturn` | Manual evaluation/control stack; every symbol has producer and consumer rules. |
| S16 | 80 | `Int ::= vlen(VList) [function]` | Structural length helper; result-bearing and fully defined on `VList`. |
| S17 | 84 | `VList ::= vconcat(VList,VList) [function]` | Structural concatenation helper; result-bearing and fully defined on first `VList`. |
| S18 | 88 | `Value ::= vnth(VList,Int) [function]` | Partial index helper. It is deliberately undefined for negative/out-of-range indices; the submitted loop calls it only with `0 <= I < vlen(VS)`. |

### `verification.k`

| ID | Lines | Declaration and productions | Use/judgment |
|---|---:|---|---|
| V01 | 7 | `Program ::= solutionProgram [macro]` | Exact program macro; expanded KORE equals trusted-translation output. |
| V02 | 8 | `Stmts ::= getRowBody [macro]` | Exact body macro; included in the same KORE identity check. |
| V03 | 31 | `IntList ::= inil | icons(Int,IntList)` | Mathematical finite integer-row domain. |
| V04 | 32 | `Matrix ::= mnil | mcons(IntList,Matrix)` | Mathematical finite ragged integer-matrix domain. |
| V05 | 34 | `VList ::= encodeInts(IntList) [function]` | Representation map, structurally defined. |
| V06 | 38 | `VList ::= encodeMatrix(Matrix) [function]` | Representation map, structurally defined. |
| V07 | 45 | `VList ::= rowCoords(IntList,Int,Int,Int) [function,total]` | Extensional result helper; equations are exhaustive and recursive on the row. |
| V08 | 50 | `VList ::= coordStep(Bool,IntList,Int,Int,Int) [function,total]` | Boolean case split; true/false equations are disjoint and exhaustive. |
| V09 | 56 | `VList ::= matrixCoords(Matrix,Int,Int) [function]` | Extensional result helper; structurally defined on matrices. |
| V10-V13 | 61-64 | `promptMatrix`, `thirdMatrix`, `promptInput`, `thirdInput` `[macro]` | Names exact documented inputs; no operational execution is replaced. |
| V14 | 82 | `VList ::= addCoord(Bool,Value,VList) [function,total]` | Disjoint/exhaustive Boolean constructor helper. |
| V15 | 86 | `VList ::= expectedFlags(Bool,Bool,Bool) [function,total]` | One unconditional equation; exhaustively fixes results for the fixed `[[A,B],[C]]` shape. |

`spec.k` adds no syntax, semantic rules, functions, simplifications, priorities,
or opaque declarations. It contains exactly eleven entry reachability claims.

## `semantic.k` rule-by-rule decisions

All judgments below are for the submitted program on finite nested lists of
integers and integer `x`. No rule is a proof-only bridge or answer oracle.

| ID | Line(s) | Rule effect | Decision |
|---|---:|---|---|
| SR01 | 81 | `vlen(vnil) => 0` | Sound list length base. |
| SR02 | 82 | `vlen(vcons(_,VS)) => 1 + vlen(VS)` | Sound structural step; descends. |
| SR03 | 85 | `vconcat(vnil,VS) => VS` | Sound concatenation base. |
| SR04 | 86 | `vconcat(vcons(V,VS),WS) => vcons(V,vconcat(VS,WS))` | Sound structural step; descends. |
| SR05 | 89 | `vnth(vcons(V,_),0) => V` | Sound zero index. |
| SR06 | 90 | Positive `vnth` recurses with tail and `I-1` | Sound for guarded `I>0`; disjoint from SR05 and descends. |
| SR07 | 92 | `Module(SS) => exec(SS)` | Sound module execution start. |
| SR08 | 94 | Empty `exec` completes | Sound sequence base. |
| SR09 | 95 | Nonempty `exec` executes head then tail | Sound left-to-right statement sequencing. |
| SR10 | 97-98 | Register `FuncDef` in `<functions>` | Sound for the top-level definition; body is stored, not skipped. |
| SR11 | 100-103 | `start` selects exact `get_row(lst,x)`, binds arguments, executes body | Sound specialized entry harness reached after SR10 from the declared initial configuration. It does not assert a result. |
| SR12 | 105 | Assignment evaluates RHS before store | Sound evaluation order. |
| SR13 | 106-107 | Store evaluated assignment value | Sound environment update. |
| SR14 | 109 | `For` evaluates iterable first | Sound for used loop. |
| SR15 | 110 | List value becomes `forLoop` | Sound list-iterator initialization for a program that does not mutate the iterated list. |
| SR16 | 111 | Empty `forLoop` completes | Sound. |
| SR17 | 112-113 | Bind head, execute body, continue with tail | Sound ordered iteration and environment effect. |
| SR18 | 115 | `While` becomes `whileLoop` | Sound control setup. |
| SR19 | 116 | Evaluate while guard | Sound repeated guard evaluation. |
| SR20 | 117 | True guard executes body then loops | Sound. |
| SR21 | 118 | False guard completes | Sound and disjoint from SR20. |
| SR22 | 120 | `If` evaluates condition | Sound. |
| SR23 | 121 | True condition executes then branch | Sound. |
| SR24 | 122 | False condition executes else branch | Sound and disjoint from SR23. |
| SR25 | 124 | Return evaluates expression | Sound. |
| SR26 | 125-129 | Evaluated return consumes the function continuation, records value, clears call-local maps | Sound for the single top-level call model; it preserves the observable result and implements abrupt return. |
| SR27 | 130 | Integer literal to `pyInt` | Sound. |
| SR28 | 131 | Boolean literal to `pyBool` | Sound; unused in submitted tree. |
| SR29 | 132-133 | Name lookup from `<env>` | Sound map lookup/binding. |
| SR30 | 135 | List expression uses expression-list evaluator | Sound. |
| SR31 | 136 | Tuple expression evaluates elements then converts | Sound. |
| SR32 | 137 | Evaluated list representation becomes tuple representation | Sound constructor conversion. |
| SR33 | 139 | Empty expression list to empty `pyList` | Sound. |
| SR34 | 140 | Evaluate expression-list head first | Sound left-to-right evaluation. |
| SR35 | 141 | Evaluate remaining expressions after head | Sound left-to-right continuation. |
| SR36 | 142 | Prepend saved head to evaluated tail | Sound and preserves source order. |
| SR37 | 144 | Binary operation evaluates left first | Sound. |
| SR38 | 145 | Then evaluate right while retaining left | Sound. |
| SR39 | 146 | Integer subtraction `L-R` | Sound operand order. |
| SR40 | 147 | Integer addition `L+R` | Sound. |
| SR41 | 148 | List addition concatenates `L` then `R` | Sound Python-list behavior for used operands. |
| SR42 | 150 | Comparison evaluates left first | Sound for the used one-comparator form. |
| SR43 | 151 | Then evaluates right while retaining left | Sound. |
| SR44 | 152 | Integer `L >= R` | Sound operand order. |
| SR45 | 153 | Integer `L == R` | Sound on the formal integer domain. |
| SR46 | 155 | Subscript evaluates base first | Sound Python evaluation order. |
| SR47 | 156 | Then evaluates index while retaining base | Sound. |
| SR48 | 157 | List/integer subscript invokes `vnth` | Sound on the program's proved-valid nonnegative indices. |
| SR49 | 159 | `len` call evaluates its single argument | Sound for the exact used builtin call. |
| SR50 | 160 | List length returns `pyInt(vlen(VS))` | Sound. |

The semantics intentionally omits unused Python constructs and exception cases.
That is a coverage boundary, not a false rule. All used control and expression
forms have a real rule path; none fabricates the task result.

## `verification.k` rule-by-rule decisions

| ID | Line(s) | Rule effect/class | Decision |
|---|---:|---|---|
| VR01 | 10-11 | Expand `solutionProgram` macro | Sound; exact KORE identity with regenerated `solution.mpy`. |
| VR02 | 13-28 | Expand `getRowBody` macro | Sound; same identity check, and operational semantics still executes it. |
| VR03 | 35 | Encode empty integer row | Sound definitional equation. |
| VR04 | 36 | Encode integer row head/tail | Sound, disjoint from VR03, descending. |
| VR05 | 39 | Encode empty matrix | Sound definitional equation. |
| VR06 | 40-41 | Encode matrix row/tail | Sound, disjoint from VR05, descending. |
| VR07 | 46 | Empty `rowCoords` | Sound base equation. |
| VR08 | 47-48 | Nonempty `rowCoords` delegates on exact equality | Sound, disjoint from VR07, and reaches descending VR09/VR10. |
| VR09 | 51-53 | True coordinate step: recurse on tail, append current coordinate | Sound; tail-first plus append gives descending columns. |
| VR10 | 54 | False coordinate step: recurse without coordinate | Sound and disjoint/exhaustive with VR09. |
| VR11 | 57 | Empty `matrixCoords` | Sound base equation. |
| VR12 | 58-59 | Current row coordinates concatenated before later rows | Sound ascending-row order; descends on matrix. |
| VR13 | 66-70 | Expand documented prompt matrix | Sound literal macro. |
| VR14 | 72 | Encode documented prompt input | Sound literal/representation macro. |
| VR15 | 74-76 | Expand third documented matrix | Sound literal macro. |
| VR16 | 78 | Encode third documented input | Sound literal/representation macro. |
| VR17 | 83 | `addCoord(true,V,VS)` prepends | Sound. |
| VR18 | 84 | `addCoord(false,_,VS)` omits | Sound, disjoint/exhaustive with VR17. |
| VR19 | 87-90 | Build fixed-shape result in B,A,C order | Sound for `[[A,B],[C]]`: coordinates are `(0,1),(0,0),(1,0)`. |

The result helpers are definitional summaries used only in postconditions. They
do not rewrite `exec`, `eval`, loops, return, or another operational term.
There is therefore no operational bridge, result-bearing opaque symbol, or
unconstrained oracle in `verification.k`.

## Used-construct coverage map

| Submitted `solution.mpy` construct | Declaration | Operational rules |
|---|---|---|
| `Module`, statement sequence | S01-S02 | SR07-SR09 |
| `FuncDef`, `Params` | S04-S05 | SR10-SR11 |
| `Assign` | S05 | SR12-SR13 |
| `For` | S05 | SR14-SR17 |
| `While` | S05 | SR18-SR21 |
| `If` | S05 | SR22-SR24 |
| `Return` | S05 | SR25-SR26 |
| `Name`, `Int` | S08 | SR27, SR29 |
| `ListExpr`, `TupleExpr`, `Exprs` | S06, S08 | SR30-SR36 |
| `BinOp("-",...)`, integer/list `BinOp("+",...)` | S08 | SR37-SR41 |
| `Compare` with `>=` and `==` | S07-S09 | SR42-SR45 |
| `Subscript` | S08 | SR46-SR48, SR05-SR06 |
| `Call(Name("len"),...)` | S08 | SR49-SR50, SR01-SR02 |

No syntactic construct in the submitted program is left unmodeled.

## Static conclusion

The local generated semantics and verification equations are sound for every
construct and value path exercised by the submitted program on the intended
finite integer-matrix domain. There is no witnessed false local rule and thus
no rule is labeled unsound. The material defect is theorem scope, not a semantic
shortcut: the eleven claims do not quantify over an arbitrary `Matrix`.
