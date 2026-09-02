# Exhaustive local K inventory and reviewer decision

This inventory covers the immutable candidate sources copied to
`/tmp/audit-work/candidate-src`. Imported K distribution modules are accounted
for separately as a trust boundary.

## Syntax and attributes

| ID | Source | Declaration / alternatives | Target role | Decision |
|---|---|---|---|---|
| Y01 | `semantic.k:10` | `Module ::= Module(Stmts)` | translated module | Sound constructor syntax |
| Y02 | `semantic.k:12` | `Stmts ::= List{Stmt,""}` | ordered statement sequence | Sound; juxtaposition matches translator output |
| Y03–Y07 | `semantic.k:13-18` | `FuncDef`, `Assign`, `For`, `If`, `Return` | every statement constructor in `solution.mpy` | Sound and complete for the submitted body |
| Y08–Y09 | `semantic.k:20-21` | `Params`, comma-separated `Strings` | one `lst` parameter | Sound |
| Y10 | `semantic.k:23` | comma-separated `Exprs` | `isinstance` arguments | Sound |
| Y11–Y17 | `semantic.k:24-31` | `Int`, `Float`, `Bool`, `Name`, `BinOp`, `Compare`, `Call` | submitted expressions plus runtime-tag test inputs | Sound; used source constructors are all present |
| Y18–Y19 | `semantic.k:33-34` | `CmpOps`, `CmpOp` | single `>=` and `==` comparisons | Sound |
| Y20–Y23 | `semantic.k:38-42` | `pyInt`, `pyFloat`, `pyBool`, `pyList` | modeled Python value tags | Sound for built-in values in scope |
| Y24–Y28 | `semantic.k:43-48` | `nil`, `intCons`, `floatCons`, `boolCons`, `listCons` | finite heterogeneous lists | Sound tagged finite-list representation |
| Y29–Y35 | `semantic.k:50-53` | `noResult`/`Val`, `function`, `noFunction`/`Function`, `noValue`/`Val` | explicit result, function, and local slots | Sound |
| Y36–Y40 | `semantic.k:75-79` | `start`, `bind`, `branch`, `loop`, `returnValue` | internal control | Sound for the single-function subset |
| Y41 | `semantic.k:82` | `eval(Expr,Val,Val,Val) [function]` | pure expression evaluator | Sound partial function; equations cover every expression reached by the submitted program |
| Y42–Y47 | `semantic.k:83-88` | `isIntVal`, `addVal`, `mulVal`, `modVal`, `geVal`, `eqVal`, all `[function]` | used primitive operations | Sound partial functions on reached tags |
| Y48 | `semantic.k:89` | `asInt(Val) [function]` | int/bool numeric projection | Sound partial function |
| Y49 | `semantic.k:90` | `asBool(Val) [function]` | branch guard projection | Sound partial function |
| Y50 | `verification.k:9` | `loopBody [function]` | names exact submitted loop body | Sound definitional abbreviation; not an execution summary |
| Y51 | `verification.k:22` | `solutionProgram [function]` | names exact submitted module | Sound definitional abbreviation; mechanical expansion matches `solution.mpy` |
| Y52 | `verification.k:32-34` | `selectedSquare(Int) [function,total,smt-hook(...)]` | mathematical per-integer contribution | Sound and total; guards are complementary and the hook states the same `ite` |
| Y53 | `verification.k:35` | `oddSquareFold(Vals,Int) [function]` | structurally recursive mathematical result | Sound; `nil` and every cons constructor are covered, with Boolean payloads split into true/false cases |

No local declaration has `[functional]`, `[opaque]`, `[simplification]`,
`[concrete]`, or a priority attribute. The sole special rule attribute is
`[owise]` on S15. The sole totality declaration and sole SMT hook are on Y52.

## `semantic.k` rules

| ID | Source | Rule effect | Reviewer decision |
|---|---|---|---|
| S01 | `semantic.k:92` | `eval(Int(I),...) => pyInt(I)` | Sound literal evaluation |
| S02 | `semantic.k:93` | `eval(Float(F),...) => pyFloat(F)` | Sound literal/tag evaluation |
| S03 | `semantic.k:94` | `eval(Bool(B),...) => pyBool(B)` | Sound literal/tag evaluation |
| S04 | `semantic.k:95` | lookup `lst` from evaluator argument | Sound for hard-wired local environment |
| S05 | `semantic.k:96` | lookup `total` | Sound |
| S06 | `semantic.k:97` | lookup `value` | Sound |
| S07 | `semantic.k:99-100` | recursively evaluate `+`, then `addVal` | Sound; submitted operands are pure |
| S08 | `semantic.k:101-102` | recursively evaluate `*`, then `mulVal` | Sound; submitted operands are pure |
| S09 | `semantic.k:103-104` | recursively evaluate `%`, then `modVal` | Sound; reached divisor is the nonzero integer 2 |
| S10 | `semantic.k:106-107` | evaluate `>=` via `geVal` | Sound on reached int/bool operands |
| S11 | `semantic.k:108-109` | evaluate `==` via `eqVal` | Sound on reached int/bool operands |
| S12 | `semantic.k:111-112` | exact `isinstance(E,int)` call via `isIntVal` | Sound for built-in modeled tags |
| S13 | `semantic.k:115` | `pyInt` is an `int` | Sound |
| S14 | `semantic.k:116` | `pyBool` is an `int` | Sound; CPython `bool` subclasses `int` |
| S15 | `semantic.k:117` | all other modeled tags are not `int`, `[owise]` | Sound and disjoint from S13–S14 |
| S16 | `semantic.k:119` | project `pyInt(I)` to `I` | Sound |
| S17 | `semantic.k:120` | project `True` to integer 1 | Sound |
| S18 | `semantic.k:121` | project `False` to integer 0 | Sound |
| S19 | `semantic.k:122` | project `pyBool(B)` to `B` | Sound |
| S20 | `semantic.k:124` | integer/bool addition | Sound on every reached application; unsupported tags remain visibly stuck through `asInt` |
| S21 | `semantic.k:125` | integer/bool multiplication | Sound on every reached application |
| S22 | `semantic.k:126` | integer/bool remainder | Sound on every reached application |
| S23 | `semantic.k:127` | integer/bool `>=` | Sound on every reached application |
| S24 | `semantic.k:128` | integer/bool equality | Sound on every reached application |
| S25 | `semantic.k:131` | module statements followed by `start` | Sound module-loading order for the submitted one-definition module |
| S26 | `semantic.k:133` | split nonempty statement list into head then tail | Sound sequential control |
| S27 | `semantic.k:134` | empty statement list becomes `.K` | Sound |
| S28 | `semantic.k:136-137` | bind exact entry-point definition | Sound for submitted binding and body |
| S29 | `semantic.k:139-142` | bind input to `lst`, begin exact body | Sound one-argument invocation |
| S30 | `semantic.k:144-147` | evaluate and assign `total` | Sound for the only assignment target used |
| S31 | `semantic.k:149-153` | evaluate guard and create `branch` | Sound; guard expressions are pure |
| S32 | `semantic.k:155` | select true branch | Sound |
| S33 | `semantic.k:156` | select false branch | Sound |
| S34 | `semantic.k:158-162` | evaluate iterable and create `loop` | Sound for `for value in lst` |
| S35 | `semantic.k:164` | empty list terminates loop | Sound |
| S36 | `semantic.k:165-167` | bind integer head, run body, recurse on tail | Sound order and state transition |
| S37 | `semantic.k:168-170` | bind float head, run body, recurse | Sound |
| S38 | `semantic.k:171-173` | bind `True`, run body, recurse | Sound |
| S39 | `semantic.k:174-176` | bind `False`, run body, recurse | Sound |
| S40 | `semantic.k:177-179` | bind nested-list head, run body, recurse | Sound; actual `isinstance(...,int)` rejects it |
| S41 | `semantic.k:181-182` | write exact loop variable `value` | Sound |
| S42 | `semantic.k:184-187` | evaluate return expression and create `returnValue` | Sound |
| S43 | `semantic.k:190-195` | return with a pending suffix: discard suffix, clear locals, set result | Sound abrupt function return in this no-call-stack subset; exact returned value and every modeled local cell are preserved/updated correctly |
| S44 | `semantic.k:197-202` | return with no suffix: clear locals, set result | Sound; overlaps S43 only, if at all, with the same result and cell effects |

S20–S24 are deliberately partial outside int/bool arguments. They do not
fabricate a value for unsupported tags: their RHS contains an unreduced
`asInt`, so an out-of-scope use stops visibly. Every use reached from
`solution.mpy` has an int/bool argument.

## `verification.k` equations

| ID | Source | Equation | Reviewer decision |
|---|---|---|---|
| V01 | `verification.k:10-20` | expand `loopBody` | Sound definitional expansion; exact normalized constructor body |
| V02 | `verification.k:23-28` | expand `solutionProgram` | Sound definitional expansion; V01 expansion is constructor-identical to trusted regenerated `solution.mpy` |
| V03 | `verification.k:37-38` | selected nonnegative odd integer contributes `I*I` | Sound mathematics and matches executed nested branches |
| V04 | `verification.k:39-40` | all complementary integers contribute 0 | Sound; guard is the Boolean complement of V03 |
| V05 | `verification.k:42` | empty fold returns accumulator | Sound base case |
| V06 | `verification.k:43-44` | integer head adds `selectedSquare` | Sound induction step |
| V07 | `verification.k:45-46` | float head is ignored | Sound for executed `isinstance` test |
| V08 | `verification.k:47-48` | `True` contributes 1 | Sound for CPython bool-as-int behavior |
| V09 | `verification.k:49-50` | `False` contributes 0 | Sound |
| V10 | `verification.k:51-52` | nested-list head is ignored | Sound for executed `isinstance` test |

V01–V02 name syntax and do not replace an operation. V03–V10 occur only on
the specification side and in the invariant result; no semantic rule rewrites
program execution to `selectedSquare` or `oddSquareFold`. Thus there is no
program-derived opaque oracle or operational bridge.

## Claims

| ID | Source | Role | Reviewer decision |
|---|---|---|---|
| C01 | `spec.k:8-21` | loop circularity from arbitrary suffix and accumulator to exact fold result | Sound invariant: each S35–S40 constructor case agrees with V05–V10, then S42–S44 returns and clears locals |
| C02 | `spec.k:25-34` | end-to-end exact-program claim | Sound and result-constraining; V02 executes S25–S44 and C01 summarizes the real loop |

The proof has no proof-local ordinary rewrite that preempts a semantic rule,
no priority rule, no simplification rule, and no opaque result-bearing symbol.
