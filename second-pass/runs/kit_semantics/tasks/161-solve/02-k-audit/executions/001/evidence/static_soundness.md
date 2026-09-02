# Static soundness ledger

The exhaustive mechanical inventory is `rule_inventory.log`: 25 K source
files, 251 syntax-declaration starts, 778 rule starts, 5 contexts, and one
configuration. The independent `rg` totals agree exactly with the parser
totals. This ledger gives the audit decision for every inventory class and
then expands every proof-local record individually.

## Inventory-wide decisions

| Inventory class | Count | Audit decision |
|---|---:|---|
| Supplied syntax/configuration/rules | 1,014 records | These are the fixed read-only operational model. Every source record was inventoried. The rules reachable from this program are listed below and were checked against their complete contexts, cells, evaluation order, overlaps, and modeled value operations. All other fixed rules are constructor/tag-disjoint from the reachable terms; they cannot rewrite this program or its summaries. |
| Proof-local declarations/rules | 21 records | Expanded individually below. All are exact macros, truthful structurally recursive definitions, or one independently proved constructor lemma. |
| Opaque `no-evaluators` declarations | 24 records | All are fixed-model primitives for float, sorting, and MD5 operations. Neither the program, a helper claim, nor the postcondition contains any of these symbols. They have no value/control/state influence here. |
| Priority rules | 56 records | The reachable priority rules are ordinary fixed binding/dispatch rules; none is candidate-authored. Unreachable priorities dispatch heap objects, sorting, math, split, subscripting, dictionaries, or closure cells absent from every reachable candidate state. |
| Fixed `[total]` declarations with compiler coverage warnings | `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, `valSeqAt` | None is reachable from this program or postcondition. Their incomplete equation coverage can leave an unused term opaque/defined; it supplies no equality and cannot establish the candidate result. |
| Concrete-only rules | 75 records | They belong to `MPY-CONCRETE`, imported only by the LLVM `MPY-KRUN` module. The Haskell proof module imports `MPY`, so these concrete-only rewrite legs do not contribute to `#Top`. |

No inventoried rule yields a concrete false conclusion on the candidate's
reachable domain. The supplied model intentionally differs from CPython on
non-ASCII literal encoding/classification; the concrete witness is recorded in
`stage3_unicode_gap.log`. That is a model boundary, not an equation used to
claim Unicode equivalence.

## Fixed rules reached by the candidate

| Source | Reached declarations/rules | Static decision |
|---|---|---|
| `syntax.k` | `Module`, `FuncDef`, `Params`, `Expr`, `Str`, `Assign`, `Name`, `Bool`, `For`, `BinOp`, `If`, `Call`, `Attribute`, `AugAssign`, `Return`, statement/expression lists and their strictness attributes | These are exactly the regenerated constructor forms. Strictness evaluates assignment/call/condition operands before their consumers; `BinOp` is left-to-right. |
| `core.k` | configuration; lines 68–70 `isRefV`; 124–127 load/sequencing; 130–134 and 152–154 lookup; 157–181 builtin scope; 185–191 left-to-right argument evaluation; 194–195 literals; 199–203 truthiness; 209 dispatch declaration; 238–240 `appendVal` | Scope lookup selects the actual `solve` closure and local bindings; the input is already a `str(INPUT)` value. Argument accumulation preserves order. `isRefV(str(...))` refutes the heap-reference augmented-assignment alternative. No heap or exception operation is introduced. |
| `str.k` | lines 8–10 iteration; 13–17 ASCII literal conversion; 20–24 concatenation | String iteration yields one-character strings and the remaining suffix. All source literals in the body are ASCII, so `strToCodes` is defined. Concatenation is a structurally recursive append. |
| `operators.k` | `BinOp` dispatch | Both operands evaluate before the fixed `applyBin("+", str, str)` rule; no reference-dereference priority matches. |
| `methods.k` | `applyMethod` declaration; lines 15 and 21 (`isalpha`, `swapcase`); 52–55 reverse; 112–119 classification; 132–134 `allAlpha`; 149–164 case maps | The fixed character model is ASCII. Guards/ranges and structural recursions are disjoint, exhaustive, and descending. This is precisely the documented supplied-model boundary. |
| `controls.k` | lines 9–23 assignment/augmented assignment; 48 expression discard; 51–54 `If`; 65–74 `For` | Only plain local-name assignments occur, so closure-cell/reference priorities cannot match. The loop evaluates its iterable once, binds each character, executes the body, and re-enters `#loop` with the exact remainder. |
| `tuple.k` | lines 31–34 `#bindTgt(Name, value)` | Each string-loop yield is written to the real local `c`; tuple/ref alternatives are disjoint. |
| `call.k` | lines 16, 19–24 callee/method routing; lines 69–74 user-closure entry | Callee is evaluated before arguments; method binding keeps the actual receiver; user call pushes the exact caller continuation and a fresh local scope. Heap-object and annotated-closure alternatives cannot match. |
| `functions.k` | lines 14–20 function binding; 63–66 parameter binding; 78–90 return/pop | The real body is stored in the closure, `s` is bound to the symbolic input, return discards only the remaining callee body, and pop restores the caller continuation/environment while removing the callee frame. |
| `verification.k` | all 21 inventory records | Expanded below. |

The reachable fixed-rule path reads/writes only `k`, `env`, `scopes`,
`scopeLoc`, `stack`, and `ret`; it preserves the empty heap/heap counter and
`NoExc`/exit 0. Calls to string methods are pure fixed-function dispatches, not
user-function frames.

## Every proof-local record

| Lines | Declaration/rule | Class and decision |
|---|---|---|
| 8–9 | `iCons(C,.IntSeq) ==K .IntSeq => false [simplification]` | Derived constructor-disjointness lemma. The bridge-free `LEMMA-SPEC` proof closes with `#Top`; it has no cells or control footprint. |
| 12 | `loopBody [macro]` | Compile-time syntax alias. |
| 13–27 | `loopBody => ...` | Exact generated loop AST. It never rewrites a runtime computation after macro expansion. |
| 29 | `solveBody [macro]` | Compile-time syntax alias. |
| 30–44 | `solveBody => ...` | Exact generated function-body AST. Fresh `kast --expand-macros` JSON is byte-identical to trusted regenerated `solution.mpy`. |
| 46 | `charAlpha(Int) [function,total]` | Pure total definition. |
| 47–49 | `charAlpha(C)` equation | Exactly the fixed one-character `isalpha` expression. The independent constructor lemma reduces nonemptiness; `allAlpha` then reduces to `isAlphaC(C)`. |
| 51 | `alphaAcc(IntSeq,Bool) [function,total]` | Pure total fold declaration. |
| 52 | `alphaAcc(.IntSeq,FOUND) => FOUND` | Correct empty suffix; disjoint from `iCons`. |
| 53–56 | alphabetic `alphaAcc` step | Guarded by `charAlpha(C)`, sets the flag to true, and strictly descends to `REST`. |
| 57–60 | nonalphabetic `alphaAcc` step | Guarded by the Boolean complement, preserves the prior flag, and strictly descends. The two guards cannot overlap and cover every Boolean result. |
| 63 | `toggleAcc(IntSeq,IntSeq) [function,total]` | Pure total fold declaration. |
| 64 | `toggleAcc(.IntSeq,OUT) => OUT` | Correct empty suffix; disjoint from `iCons`. |
| 65–70 | alphabetic `toggleAcc` step | Appends exactly fixed `swapC(C)` and descends to `REST`. |
| 71–76 | nonalphabetic `toggleAcc` step | Appends exactly `C`; complement guard is disjoint/exhaustive with the prior rule and recursion descends. |
| 79 | `lastChar(IntSeq,Str) [function,total]` | Pure total fold declaration. |
| 80 | empty `lastChar` | Preserves the initialized/previous loop target when there are no iterations. |
| 81–83 | nonempty `lastChar` | Replaces the target with each yielded one-character string; structural descent returns the last code. |
| 85 | `solveResult(IntSeq) [function,total]` | Pure result-name declaration; it does not replace execution. |
| 86–87 | alphabetic `solveResult` | Exact output `toggleAcc(INPUT,.IntSeq)` under the proved any-letter condition. |
| 88–89 | no-letter `solveResult` | Exact fixed `revIS(INPUT)` under the complementary condition. The guards are disjoint/exhaustive after total `alphaAcc`. |

The two reachability claims are not axiomatic rewrite rules. The loop claim is
checked as a circularity from the exact `#loop(str(REST), Name("c"),
loopBody)` context and summarizes all four modified accumulators plus `c`; the
whole-program claim executes function binding, lookup, argument evaluation,
the exact closure body, return, pop, and final assignment.

## False-conclusion witness requirement

No candidate-authored unsound rule was found, so there is no claimed
false-conclusion witness. The narrower fixed-model gap has a concrete
model-vs-CPython witness (`"é1"`), but it is not labeled an unsound proof rule:
the model rejects the non-ASCII source literal, while the formal arbitrary
`IntSeq` summary treats code 233 as nonalphabetic; CPython returns `"É1"`.
