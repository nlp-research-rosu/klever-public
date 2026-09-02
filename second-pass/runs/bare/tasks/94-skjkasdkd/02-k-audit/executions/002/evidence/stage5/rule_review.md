# Exhaustive local K declaration and rule review

Source line numbers refer to the immutable files under `/candidate`. Imported
`domains.md` modules are the standard K trust boundary; this inventory covers
every declaration and rule introduced locally in `semantic.k`,
`verification.k`, and `spec.k`.

## Syntax and attribute inventory

| Lines | Local declaration | Submitted-program use and assessment |
|---|---|---|
| `semantic.k:8` | `Pgm ::= Module(Stmts)` | Used by `solution.mpy`; faithful constructor representation. |
| `semantic.k:10` | `Stmts ::= List{Stmt,""}` | Used for function/module bodies; ordered concatenation is required. |
| `semantic.k:11-13` | `Stmt ::= FuncDef | Return | If` | Exactly the three statement forms in the translated program. |
| `semantic.k:15-16` | `Params`, comma-separated `Strings` | Covers all function parameter lists. |
| `semantic.k:18` | comma-separated `Exprs` | Covers call and Boolean operands. |
| `semantic.k:19-26` | `Expr ::= Int | Bool | Name | BinOp | BoolOp | Compare | Call | Subscript` | Covers every expression constructor in `solution.mpy`, with no fabricated catch-all form. |
| `semantic.k:28-29` | `CmpOps`, `CmpOp` | The program uses one comparison operator per comparison; that used form has rules. |
| `semantic.k:31-33` | `Index ::= Expr | Slice(...)`; `Bound ::= Expr | NoBound` | Covers exactly index `0` and slice `1:` used by the program. |
| `semantic.k:43-46` | `Val ::= intVal | boolVal | listVal`; `Vals` list | Sufficient runtime value domain for the submitted integer-list program. |
| `semantic.k:48` | `Def ::= def(Params,Stmts)` | Stores exact function bindings and bodies. |
| `semantic.k:50` | `collectDefs(Stmts) [function]` | Definitional environment construction; equations reviewed below. |
| `semantic.k:55` | `getDef(Map,String) [function]` | Partial lookup, used only for present unique program definitions. |
| `semantic.k:58` | `lookupEnv(Map,String) [function]` | Partial lookup, used only for bound parameters. |
| `semantic.k:61` | `bind(Params,Vals) [function]` | Partial on arity mismatch; all submitted calls have exact arity. |
| `semantic.k:66-68` | `valLength`, `intHead` `[function]`; `intTail` `[function]` | `intHead`/`intTail` are partial outside nonempty integer lists. That is exactly the source-contract type and guarded use. |
| `semantic.k:74` | `appendStmts` `[function]` | Ordered statement-list concatenation. |
| `semantic.k:78` | `Result ::= noResult | result(Val)` | Explicit single observable result cell. |
| `semantic.k:79-98` | `KItem` control constructors `init`, `invokeProgram`, `invoke`, `invokeDef`, `execStmts`, `eval`, `evalArgs`, `argsDone`, `returnIf`, binary/comparison/and/argument/call/subscript frames, and `finish` | These are internal small-step frames, not opaque or result-bearing oracles. Every frame is introduced and consumed by inventoried operational rules. |
| `verification.k:8-9` | `solutionProgram [macro]` | Macro expands to the submitted constructor term. Fresh `kast --expand-macros` JSON is byte-identical to parsed `solution.mpy` (`stage4/program_term_identity.log`). |
| `verification.k:46-49` | `programDefs(Pgm) [function]`; `solutionDefs [macro]` | Both reduce to `collectDefs` of the mechanically matched program term; neither bypasses bodies. |
| `verification.k:52-53` | `refPrimeFrom`, `refPrime` `[function,total]` | Mathematical specification functions. `refPrime` is exhaustive. `refPrimeFrom` is exhaustive and descending over every proof use (`N>=2,D>=2`), but its global `total` declaration is broader than its equations at `D=0`; this unused over-declaration is a trust/evidence limitation, not a wrong conclusion on an integer-list entry state. |
| `verification.k:63-66` | `refChoose`, `refLargest`, `refDigitSum`, `refAnswer` `[function]` | Transparent structural specification functions; no opacity or oracle. |

There are no local priority rules, simplification rules, `[concrete]`
rules, `[functional]` declarations, fresh symbols, or opaque/uninterpreted
result symbols. The only local `total` attributes are the two listed above.
The only local macros are `solutionProgram` and `solutionDefs`.

## Rule inventory: semantic helper equations

| ID / line | Rule | Decision |
|---|---|---|
| H1 / 51 | `collectDefs(.Stmts) => .Map` | Sound empty definition environment. |
| H2 / 52-53 | collect one `FuncDef` then recurse | Sound ordered collection for the program's six unique function names. |
| H3 / 56 | `getDef` selects the queried map binding | Sound for a present unique key; every submitted call name is present except separately handled `len`. |
| H4 / 59 | `lookupEnv` selects the queried binding | Sound for bound parameters; every submitted `Name` is bound in its active environment. |
| H5 / 62 | empty params/args bind to empty map | Sound. |
| H6 / 63-64 | bind heads then recurse | Sound for equal arity; all six function definitions are called at their declared arity. |
| H7 / 69 | empty `Vals` length is zero | Sound. |
| H8 / 70 | nonempty length is one plus tail length | Sound and descending. |
| H9 / 71 | integer-list head extraction | Sound on the source-contract list element type. |
| H10 / 72 | integer-list tail extraction | Sound on the source-contract list element type. |
| H11 / 75 | append to empty left statements | Sound. |
| H12 / 76 | preserve the left head and recurse | Sound ordered append. |

## Rule inventory: operational semantics

| ID / line | Rule | Decision |
|---|---|---|
| O1 / 106 | `init(P,A) => invokeProgram(P,A) ~> finish` | Sound initialization and exact final-result continuation. |
| O2 / 107-109 | module invocation selects `skjkasdkd` in collected definitions | Sound minimal entry-point rule for this submitted task. |
| O3 / 111-113 | `invoke` looks up the selected definition | Sound; it does not replace body execution. |
| O4 / 114-116 | `invokeDef` binds parameters and enters exact body | Sound exact call entry. |
| O5 / 118-120 | execute `Return(E)` by evaluating `E`, dropping following statements | Sound return behavior for these bodies; the caller continuation remains on `<k>`. |
| O6 / 121-124 | evaluate an `If` guard before selecting a branch | Sound evaluation order. |
| O7 / 125-128 | true guard prepends then-statements to the suffix | Sound. |
| O8 / 129-132 | false guard prepends else-statements to the suffix | Sound. |
| O9 / 134 | integer literal evaluation | Sound. |
| O10 / 135 | Boolean literal evaluation | Sound. |
| O11 / 136 | parameter-name lookup | Sound on every bound submitted name. |
| O12 / 138-140 | begin binary operation with left operand | Sound left-to-right evaluation. |
| O13 / 141-143 | after left value, evaluate right operand with saved left value | Sound. |
| O14 / 144 | integer addition | Sound for Python unbounded integers. |
| O15 / 145 | integer multiplication | Sound for Python unbounded integers. |
| O16 / 146-147 | modulo with nonzero divisor | Sound on every submitted execution: `n>=2`, positive divisor, or nonnegative digit input. |
| O17 / 148-149 | integer division with nonzero divisor | K `/Int` agrees with Python `//` on the only reachable operands here (nonnegative numerator, divisor 10). Negative-operand Python floor behavior is outside actual uses. |
| O18 / 151-153 | begin one comparison with left operand | Sound for every translated comparison. |
| O19 / 154-156 | evaluate comparison right operand | Sound left-to-right order. |
| O20 / 157-159 | integer `<` | Sound. |
| O21 / 160-162 | integer `>` | Sound. |
| O22 / 163-165 | integer `==` | Sound. |
| O23 / 167-169 | begin Boolean `and` with left operand | It evaluates the left first. |
| O24 / 170-172 | evaluate the right operand even when the left is false | This is not general Python short-circuit control. In the sole submitted use the right operand is the pure, total integer comparison `n > best`; on every integer-list entry state it cannot alter value, state, control, or exceptions. Thus this is an operational-model limitation, but no false result conclusion witness exists on the intended domain. |
| O25 / 173 | Boolean conjunction result | Sound after two Boolean operands. |
| O26 / 175-177 | call a named callee after evaluating arguments | Sound for the submitted global function/builtin names; the program has no rebinding or first-class callees. |
| O27 / 178 | empty argument list | Sound. |
| O28 / 179-181 | evaluate the first argument | Sound Python left-to-right order. |
| O29 / 182-184 | continue with remaining arguments | Sound. |
| O30 / 185 | prepend the saved argument to evaluated tail | Sound order preservation. |
| O31 / 186-188 | builtin `len` on `listVal` | Sound for the submitted builtin call and finite lists. |
| O32 / 189-190 | non-`len` call enters a program definition | Sound and disjoint from O31; all such names have exact bodies in `collectDefs`. |
| O33 / 192-194 | evaluate the subscript base | Sound for the constant index/slice forms in the program. |
| O34 / 195-198 | nonempty integer-list index `0` | Sound, and reachable only after the explicit length test. |
| O35 / 199-203 | nonempty integer-list slice `1:` | Sound tail operation, and guarded by the same length branch. |
| O36 / 205-206 | `finish` consumes a final value and writes the result cell | Sound, exact, and the only rule changing `<result>`. |

## Rule inventory: verification definitions

| ID / line | Rule | Class and decision |
|---|---|---|
| V1 / 9-44 | expand `solutionProgram` to the six translated function bodies | Syntax macro; mechanically identical to trusted regeneration, not an execution bridge. |
| V2 / 48 | `programDefs(Module(SS)) => collectDefs(SS)` | Definitional helper; truthful. |
| V3 / 49 | `solutionDefs => programDefs(solutionProgram)` | Syntax macro; preserves the exact binding/body map. |
| V4 / 54-55 | `refPrimeFrom(N,D) => true` if `D*D>N` | Truthful characterization of the submitted helper from its current divisor. For primality, all uses start at `D=2`. |
| V5 / 56-57 | return false when the current divisor divides `N` | Truthful for positive reachable divisors. |
| V6 / 58-59 | otherwise recurse at `D+1` | Truthful and descending toward the square-root boundary for `N>=2,D>=2`. |
| V7 / 60 | `refPrime(N) => false` for `N<2` | Correct mathematical primality boundary and exact source helper result. |
| V8 / 61 | for `N>=2`, start divisor search at 2 | Correct primality definition. |
| V9 / 67-68 | choose `N` if prime and larger than `BEST` | Truthful. |
| V10 / 69-70 | otherwise retain `BEST` | Truthful, exhaustive, and disjoint from V9. |
| V11 / 71-72 | largest-prime fold base is 0 | Matches source implementation and its no-prime convention. |
| V12 / 73-74 | fold current integer against recursively computed tail best | Truthful structural maximum-prime recursion for integer lists. |
| V13 / 75 | digit-sum base returns `N` below 10 | Truthful on every reachable `N>=0`; also exactly matches the submitted helper on negative direct calls. |
| V14 / 76-77 | add last decimal digit and recurse on quotient for `N>=10` | Truthful and descending for reachable nonnegative values. |
| V15 / 78 | answer is digit sum of the structural largest-prime result | Truthful contract composition. |

V4-V15 are transparent definitional summaries, not operational bridges:
the program bodies still execute under O1-O36. The six reachability claims
connect exact body execution to these definitions. The definitions have
pairwise disjoint guards on every proof-relevant domain and terminate by
increasing divisor, decreasing list length, or decreasing nonnegative decimal
quotient.

## Claim inventory and operational footprint

`spec.k` contains exactly six ordinary reachability claims and no rules:

1. `is_prime_from`, with `N>=2,D>=2`, returns
   `boolVal(refPrimeFrom(N,D))`.
2. `is_prime`, for every `Int`, returns `boolVal(refPrime(N))`.
3. `choose_prime`, for every two `Int`s, returns
   `intVal(refChoose(N,BEST))`.
4. `largest_prime`, for `listVal(VS)`, returns
   `intVal(refLargest(VS))`.
5. `digit_sum`, for every `Int`, returns
   `intVal(refDigitSum(N))`.
6. The entry claim executes `init(solutionProgram,listVal(VS))`, consumes
   `<k>` to `.K`, and changes exactly `noResult` to
   `result(intVal(refAnswer(VS)))`.

The helper claims frame and preserve `<result>` because helper evaluation does
not execute `finish`. The entry claim constrains the complete observable result.
No claim omits another mutable cell because the generated configuration has no
other state cell.

## Construct-to-rule coverage

| `solution.mpy` construct | Declaration | Executing rules |
|---|---|---|
| `Module`, six `FuncDef`s, parameters and statement lists | syntax lines 8-16 | H1-H6, O2-O4 |
| `Return`, `If` | syntax lines 11-13 | O5-O8 |
| `Int`, `Bool`, `Name` | syntax lines 19-21 | O9-O11 |
| `BinOp("+","*","%","//")` | syntax line 22 | O12-O17 |
| `Compare` / `CmpOp("<",">","==")` | syntax lines 24,28-29 | O18-O22 |
| `BoolOp("and",...)` | syntax line 23 | O23-O25, with the scoped short-circuit limitation above |
| `Call(Name(...),...)` | syntax line 25 | O26-O32 |
| `Subscript(...,Int(0))`, `Subscript(...,Slice(Int(1),NoBound,NoBound))` | syntax lines 26,31-33 | O33-O35 |
| top-level result | configuration lines 100-104 | O1 and O36 |

No submitted constructor is unmodeled or handled by a fabricated default rule.
