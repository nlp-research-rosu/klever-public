# Exhaustive local declaration and rule inventory

Scope: `/candidate/semantic.k`, `/candidate/verification.k`, and the sole
entry claim in `/candidate/spec.k`. Imported K built-ins are listed in the
trust ledger in `REVIEW.md`; this inventory covers every candidate-local syntax
declaration and all 83 candidate-local rules.

## Syntax, configuration, attributes, and opaque symbols

`semantic.k` has 23 `syntax` declarations:

1. `Program`: `Module(Stmts)`.
2. `Stmts`: empty-separated list of `Stmt`.
3. `Stmt`: `FuncDef`, `Return`, `Assign`, `If`.
4. `Params`: `Params(Strings)`.
5. `Strings`: comma-separated `String` list.
6. `Expr`: `Int`, `Name`, `BinOp`, `Compare`, `ListExpr`, `TupleExpr`,
   `ListComp`, `KwArg`, `Subscript`, `Call`.
7. `Exprs`: comma-separated `Expr` list.
8. `CmpOps`: comma-separated `CmpOp` list.
9. `CmpOp`: operator string plus right operand.
10. `CompFors`: empty-separated `CompFor` list.
11. `CompFor`: target, iterable, filters.
12. `Index`: expression or `Slice`.
13. `Bound`: expression or `NoBound`.
14. `Ints`: comma-separated `Int` list.
15. `Val`: `VInt`, `VList`, abstract `VArray`, `VBool`, `VEq`, `VLt`,
    `VCandidates`, `VCandidatesArray`, `minEvenInts`, `chooseEven`,
    `minEvenArray`, and `VNone`.
16. `Vals`: comma-separated `Val` list.
17. `Int`: `headInt(Ints)` and `arrayAt(Int,Int)`.
18. `Ints`: `tailInts(Ints)`.
19. `Fun`: `fun(Params,Stmts)`.
20. `Frame`: `frame(Map,K)`.
21. `ArgPack`: `argPack(Vals)`.
22. `KItem`: `start`, `done`, `exec`, `execStmt`, `eval`, `evalExprs`,
    `evalArgs`, `assignName`, `select`, binary/comparison continuations,
    expression/argument collectors, subscript continuations, named-call and
    min continuations, `invoke`, `functionReturn`, and `implicitReturn`.
23. `Map`: `bindParams(Params,Vals)`.

The configuration has exactly six state cells under `<py>`: `<k>`, `<args>`,
`<env>`, `<funs>`, `<stack>`, and `<result>`. Every cell is used. There is no
heap, I/O, exception, or allocation cell.

`verification.k` has four `syntax` declarations: the four scan functions
`specScanArray`, `specFinish`, `specConsiderArray`, and `specEvenArray`; and
the three nullary definitional abbreviations `pluckBody`, `solutionProgram`,
and `solutionFunctions`.

All local function-like productions use `[function,total]`. They are:
`minEvenInts`, `chooseEven`, `minEvenArray`, `headInt`, `arrayAt`, `tailInts`,
`bindParams`, the four `spec*` functions, `pluckBody`, `solutionProgram`, and
`solutionFunctions`. There are no `[functional]` declarations, simplification
rules, local lemmas, auxiliary claims, or loop/circularity claims. The only
priorities are `[priority(40)]` on the two direct empty-list comparisons
(`semantic.k:177-183`) and the specialized `min(..., default=[])` rule
(`semantic.k:227-229`).

Opaque or incompletely defined symbols:

- `arrayAt(ID,OFFSET)` has no candidate equation. It is a result-bearing
  abstract input observer.
- `minEvenArray(ID,OFFSET,LENGTH)` has no equation in `semantic.k`; the sole
  equation is the proof-local V10 below.
- `headInt` and `tailInts` have equations only for nonempty `Ints`.
- `bindParams` has equations only for equal-length parameter/value lists.
- `chooseEven` is not covered for an even head and arbitrary nonempty
  `VList` lengths other than the reachable two-element result.

The LLVM rebuild reports non-exhaustive `[total]` matches for
`minEvenArray`, `headInt`, `arrayAt`, `tailInts`, and `bindParams`.

## `semantic.k` rules (70)

| ID | Source | Rule / complete guard | Classification and audit decision |
|---|---:|---|---|
| S01 | 71 | `headInt(I,_IS) => I` | Truthful head observer on nonempty `Ints`; the `[total]` declaration is overbroad at empty input. Unused by the submitted body. |
| S02 | 72 | `tailInts(_I,IS) => IS` | Truthful tail observer on nonempty `Ints`; overbroad totality at empty input. Unused by the submitted body. |
| S03 | 76 | `minEvenInts(.Ints,_INDEX) => []` | Correct concrete scan base case. |
| S04 | 77-78 | nonempty `minEvenInts` recurses on tail and increments index | Correct descent over a finite constructor list. |
| S05 | 79-80 | odd `HEAD`: `chooseEven(...,REST) => REST` | Correct and accepts any `REST`; parity guard is disjoint from S06-S08. |
| S06 | 81-82 | even head, empty rest: return `[HEAD,INDEX]` | Correct. |
| S07 | 83-85 | even head and `HEAD <= BEST`: return head pair | Correct; equality selects the earlier index because recursion scans the tail first. |
| S08 | 86-88 | even head and `HEAD > BEST`: retain rest pair | Correct; disjoint from S07. `chooseEven` remains non-total on unreachable malformed list results. |
| S09 | 130 | `<k> Module(SS) => exec(SS) ...</k>` | Correct module-loading entry for the modeled subset. |
| S10 | 131 | `exec(.Stmts) => .` | Correct sequence base. |
| S11 | 132 | `exec(S SS) => execStmt(S) ~> exec(SS)` | Correct left-to-right statement sequencing. |
| S12 | 134-135 | load `FuncDef` into `<funs>` | Correct for module-level function bindings; later definitions overwrite earlier ones. |
| S13 | 137-138 | `start => invoke("pluck",A) ~> done` | Correct benchmark entry convention, not general Python module behavior. |
| S14 | 139-140 | returned `Val ~> done` updates `<result>` | Correct. |
| S15 | 143 | assignment evaluates RHS before `assignName` | Correct for the modeled name-assignment subset. |
| S16 | 144-145 | store evaluated value in `<env>` | Correct. |
| S17 | 147 | `If` evaluates guard before branch selection | Correct. |
| S18 | 148 | `VBool(true)` selects then branch | Correct. |
| S19 | 149 | `VBool(false)` selects else branch | Correct. |
| S20 | 150-151 | `VEq(I,J)` selects then when `I == J` | Correct. |
| S21 | 152-153 | `VEq(I,J)` selects else when `I != J` | Correct and disjoint from S20. |
| S22 | 154-155 | `VLt(I,J)` selects then when `I < J` | Correct. |
| S23 | 156-157 | `VLt(I,J)` selects else when `I >= J` | Correct and disjoint from S22. |
| S24 | 159 | `Return(E)` evaluates `E`, then `functionReturn` | Correct. |
| S25 | 162 | integer literal evaluates to `VInt` | Correct. |
| S26 | 163-164 | name lookup from `<env>` | Correct when the binding exists; missing-name exceptions are unmodeled and unused. |
| S27 | 166-167 | binary operation evaluates left first | Correct. |
| S28 | 168-169 | then evaluate right, saving left | Correct left-to-right order. |
| S29 | 170 | integer `+` | Correct for mathematical integers. |
| S30 | 171 | integer `%` | Correct for the submitted divisor 2. Division-by-zero behavior is unmodeled and unused. |
| S31 | 177-179 | priority comparison `Name(X) == []` for `VList(IS)` | Correct extensional empty test on modeled lists. It bypasses generic operand evaluation but the exact operands have no effects in the submitted subset. |
| S32 | 180-183 | priority comparison `Name(X) == []` for `VArray(...,LENGTH)` | Correct only under the informal invariant that `LENGTH` is the represented sequence length. |
| S33 | 184-185 | generic single comparison evaluates left | Correct. |
| S34 | 186-187 | evaluated `Val` causes right evaluation | Correct. |
| S35 | 188-189 | duplicate specialized `VList` case for S34 | Same RHS as S34; harmless overlap. |
| S36 | 190 | integer equality yields deferred `VEq` | Correct. |
| S37 | 191 | integer `<=` yields `VBool` | Correct. |
| S38 | 192 | integer `<` yields deferred `VLt` | Correct. |
| S39 | 193-194 | `VList(IS) == []` | Correct. |
| S40 | 195-196 | `[] == VList(IS)` | Correct; on `[] == []` it overlaps S39 with the same result. |
| S41 | 198 | list literal delegates to element evaluation | Correct. |
| S42 | 199 | empty expression list yields empty `VList` | Correct. |
| S43 | 200 | list elements evaluated left-to-right | Correct. |
| S44 | 201-202 | collect an integer element | Correct for integer-only lists. |
| S45 | 203 | prepend evaluated integer | Correct. |
| S46 | 208-216 | exact enumerate/filter/pair list comprehension on `VList(IS)` becomes `VCandidates(IS)` | Operational bridge. The recursive S03-S08 consumer is mathematically correct on concrete lists, and ground runs agree, but there is no bridge-free universal connection theorem. The bridge omits `<funs>` and therefore also matches shadowed `enumerate`; `operational_context_witness.log` gives a false-behavior witness on input `[2]` (Python `[]`, K `[2,0]`). |
| S47 | 217-225 | same comprehension on `VArray` becomes `VCandidatesArray(ID,OFFSET,LENGTH)` | Result-bearing operational bridge. It bypasses enumerate lookup, iteration, predicate evaluation, and pair allocation and introduces an opaque summary. No bridge-free connection theorem exists. This is on the entry proof path. |
| S48 | 227-229 | priority `min(ITEMS, default=[])` evaluates only `ITEMS`, then `minDefaultEmpty` | Specialized operational bridge. It ignores possible `min` shadowing and accepts any continuation; target context has no shadowing, but no complete-context connection theorem is supplied. |
| S49 | 230 | concrete candidates reduce to transparent `minEvenInts(IS,0)` | Correct concrete summary when S46's interpretation is assumed. |
| S50 | 231-232 | abstract candidates reduce to opaque `minEvenArray(ID,OFFSET,LENGTH)` | Material result-bearing abstraction. `semantic.k` cannot execute it: fresh fixed-semantics execution stops at this term. |
| S51 | 234-235 | exact `[1:]` slice evaluates base | Correct evaluation order, unused. |
| S52 | 236 | concrete list slice uses `tailInts` | Correct on nonempty lists but empty slicing is stuck despite Python returning `[]`; unused. |
| S53 | 237-238 | abstract slice increments offset and decrements length | False at represented empty arrays: length 0 becomes -1, whereas Python `[][1:]` remains length 0. Unused by submitted program. |
| S54 | 239 | general subscript evaluates base then index | Correct order, unused. |
| S55 | 240 | concrete list retains `Ints` for index | Correct setup, unused. |
| S56 | 241-242 | abstract array retains ID/offset/length for index | Correct setup, unused. |
| S57 | 243 | concrete index 0 returns `headInt` | Correct only for nonempty lists; empty-index exception is unmodeled. Unused. |
| S58 | 244-245 | abstract index 0 returns `arrayAt` | Omits bounds/exception behavior. Unused. |
| S59 | 247 | generic named call evaluates arguments | Correct for modeled user functions; callable lookup is delayed to `invoke`. |
| S60 | 248 | empty argument list | Correct. |
| S61 | 249 | arguments evaluated left-to-right | Correct. |
| S62 | 250 | collect any `Val` argument | Correct. |
| S63 | 251-252 | duplicate specialized `VArray` collector | Same RHS as S62; harmless overlap. |
| S64 | 253 | prepend collected argument | Correct. |
| S65 | 254 | dispatch collected named call to `invoke` | Correct within the subset. |
| S66 | 256 | empty params plus empty values yields empty map | Correct. |
| S67 | 257-258 | bind one parameter/value and recurse | Correct for equal arities; `[total]` is overbroad for mismatches. |
| S68 | 261-265 | invoke selected function, bind args, save caller env and complete continuation in a frame | Correct for the exact target call; preserves `<funs>`, `<args>`, and `<result>`. |
| S69 | 267-270 | explicit return discards current function remainder, restores caller, and resumes saved continuation | Correct early-return control for the framed subset. |
| S70 | 272-274 | implicit return restores caller with `VNone` | Correct for the framed subset. |

## `verification.k` rules (13)

| ID | Source | Rule / complete guard | Classification and audit decision |
|---|---:|---|---|
| V01 | 19-21 | scan length 0 finishes | Correct scan base for nonnegative lengths. |
| V02 | 22-25 | positive length reads `arrayAt(ID,OFFSET)` and considers it | Correct recursive scan step under the abstract-array representation. |
| V03 | 27-28 | `FOUND == 0` finishes with `[]` | Correct. |
| V04 | 29-30 | `FOUND != 0` finishes with `[BEST,BESTINDEX]` | Correct and disjoint from V03. |
| V05 | 32-36 | odd head advances without changing best | Correct. |
| V06 | 37-41 | even head dispatches to even handling | Correct and parity-disjoint from V05. |
| V07 | 43-47 | first even head becomes best and sets found to 1 | Correct. |
| V08 | 48-52 | later strictly smaller even becomes best | Correct. |
| V09 | 53-57 | later greater-or-equal even retains prior best/index | Correct; equality preserves first index. Guards V07-V09 are exhaustive on reachable integer state. |
| V10 | 62-63 | `minEvenArray(ID,OFFSET,LENGTH) => specScanArray(ID,OFFSET,LENGTH,0,0,0,0)` | Proof-local operational/value bridge and sole connection between the executed summary and the postcondition. Its match domain is every occurrence and continuation of `minEvenArray`; it has no guard, fixed-semantics evaluator, bridge-free theorem, or independent value justification. Removing it leaves the positive claim stuck at exactly this equality. An admitted opposite ground completion produces `[]` for represented `[2]` while Python produces `[2,0]`. This is an illegitimate result-bearing oracle/answer equation. |
| V11 | 70-81 | `pluckBody` expands to the exact submitted function body | Truthful definitional abbreviation; unconditionally covered. |
| V12 | 83-84 | `solutionProgram` expands to module/function binding | Truthful definitional abbreviation; constructor-pinning check closes. |
| V13 | 86-87 | `solutionFunctions` expands to the loaded function map | Truthful definitional abbreviation. |

## Sole entry claim and construct coverage

`spec.k:9-19` is the only claim. Its precondition is `LENGTH >= 0`. It starts
the exact `solutionProgram`, passes `VArray(ID,0,LENGTH)` as the one argument,
and requires empty environment/function/stack cells and `VNone` result. It
requires termination at `.K`, empty caller environment and stack, the exact
loaded `pluck` binding, and result
`specScanArray(ID,0,LENGTH,0,0,0,0)`.

Every constructor in trusted-regenerated `solution.mpy` maps as follows:

| Submitted constructor | Declaration | Material rules |
|---|---|---|
| `Module`, `FuncDef`, `Params` | syntax items 1, 3-5 | S09-S13 |
| `Return` | syntax item 3 | S24, S68-S70 |
| outer `Call(Name("min"),...,KwArg(...))` | syntax item 6 | S48-S50 |
| `ListComp`, `CompFor`, `TupleExpr` | syntax items 6, 10-11 | S46/S47 (whole-form bridge) |
| inner `Call(Name("enumerate"),Name("arr"))` | syntax item 6 | not evaluated; consumed syntactically by S46/S47 |
| `Compare`, `CmpOp`, `BinOp("%",...)`, `Int`, `Name` inside the comprehension | syntax items 6, 8-9 | not evaluated; consumed syntactically by S46/S47 |
| pair `ListExpr(value,index)` and default empty `ListExpr` | syntax items 6-7 | pair consumed by S46/S47; default shape consumed by S48 |
| concrete input `VList` | semantic value syntax | S46, S48, S49, S03-S08 |
| proof input `VArray` | semantic value syntax | S47, S48, S50, then V10 and V01-V09 |

Thus all used syntax is declared, but the proof path does not execute the
material enumerate/filter/min computation. It changes representation at S47,
reaches the unconstrained result at S50, and obtains the claimed result only
from V10.
