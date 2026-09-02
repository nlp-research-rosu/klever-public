# Exhaustive local K inventory and static decisions

Scope: the clean copies of `semantic.k`, `verification.k`, and `spec.k` in
`/tmp/audit-work/reconstruction`. There are no other candidate K helper files.
The mechanical extraction is in `stage5-static-extraction.log`: 41 semantic
rules, 17 verification rules, and 6 claims. There are no local priority,
`[simplification]`, `[concrete]`, opaque, or `[functional]` declarations.

## Syntax, attributes, configuration, and construct coverage

| Location | Declaration/productions | Decision |
|---|---|---|
| `semantic.k:8` | `Module(Module(Stmts))` | Direct representation of the translator's module constructor; used. |
| `semantic.k:9` | juxtaposed `Stmts` list | Matches translator statement sequences; used. |
| `semantic.k:10-11` | comma-separated `Strings`; `Params(Strings)` | Matches the one parameter list; used. |
| `semantic.k:13-18` | `Stmt`: `FuncDef`, `Return`, `Assign`, `If`, `For`, `Expr` | Every alternative is used by `solution.mpy`; all have an operational path below. |
| `semantic.k:20` | comma-separated `Exprs` | Used for empty list literal and the one append argument. |
| `semantic.k:21-27` | `Expr`: `Name`, `Str`, `Float`, `ListExpr`, `Compare`, `Attribute`, `Call` | Exactly the expression constructors used by `solution.mpy`. |
| `semantic.k:28-29` | `CmpOps`; `CmpOp` | Used for each single comparison. Chained comparisons are syntactically admitted but not semantically covered; none occur. |
| `semantic.k:34-38` | `Value`: rational `num`, `str`, `bool`, `list`, `none` | Adequate value shapes for the submitted body. The bridge from CPython binary floats to `num` is materially wrong, discussed under literal rules. |
| `semantic.k:39-40` | free `Vals` empty/cons datatype | Preserves order and finite list structure. |
| `semantic.k:42` | `Result = noResult \| Value` | Adequate explicit return-result cell value. |
| `semantic.k:52-58` | `<k>`, `<input>`, `<env>`, `<result>` configuration | Every cell is read or written. It omits a general Python call stack/heap but is sufficient as a direct entry harness for this body. |
| `semantic.k:60-71` | 12 internal `KItem`s: `exec`, `eval`, `store`, `discard`, `ifReady`, `forReady`, `loop`, `put`, `cmpRight`, `applyCmp`, `appendTo`, `returnValue` | Each is consumed by a corresponding rule; no opaque runtime term remains on tested executions. |
| `semantic.k:73` | `append(Vals,Value) [function,total]` | Equations cover both constructors of free `Vals`, descend structurally, and are total. |
| `verification.k:9` | `expectedGrade(Int,Int) [function,total]` | Equations are disjoint/exhaustive only for `Q > 0`, the guard of every dependent symbolic claim. The global `[total]` declaration is over-broad. At `(P,Q)=(0,0)`, the A+ and E equations overlap with different results. This invalid encoding is outside the stated positive-denominator representation, so it is a global hygiene gap rather than the intended-domain false-result witness. |
| `verification.k:37` | `expectedGrades(Vals) [function,total]` | The two equations do not cover lists headed by `str`, `bool`, `list`, or `none`; `[total]` is unjustified globally. The symbol is unused by every claim. |
| `verification.k:44` | nullary `gradingBody [function,total]` | Unconditional constructor macro. Its expansion mechanically equals the real loop body. |
| `verification.k:74` | nullary `solutionProgram [function,total]` | Unconditional constructor macro. After expanding `gradingBody` and the internal empty-list spelling, its KORE is byte-identical to parsed `solution.mpy` (`stage4-program-term-compare-success.log`). |

Construct map for `solution.mpy`: `Module` and `FuncDef` enter through
`semantic.k:78`; statement lists through `:84-85`; docstring `Expr/Str`
through `:87-88,:116`; `Assign/Name/ListExpr` through `:90-97,:114,:117`;
`For` through `:103-107`; every `If` through `:99-101`; `Compare/CmpOp/Float`
through `:120-140`; `Call/Attribute/append` through `:144-147`; and `Return`
through `:109-111`.

## `semantic.k` rules (41)

| Location | Rule | Static decision |
|---|---|---|
| `74` | append empty | Sound constructor equation. |
| `75` | append cons | Sound, structurally descending constructor equation. |
| `78-81` | exact module/function/parameter entry to `exec(BODY)` and `"grades"` binding | Faithful direct-call harness for the exact single-function submitted module and empty initial environment. It selects the exact function name/formal and preserves the continuation; no task result is fabricated. It does not model general function-definition/call behavior. |
| `84` | `exec(.Stmts) => .K` | Sound sequence base. |
| `85` | head statement then remaining `exec` | Sound left-to-right statement order. |
| `87` | expression statement evaluates then discards | Sound for the docstring and append calls. |
| `88` | discard any `Value` | Sound for used values (`str` and `none`). |
| `90` | assignment evaluates RHS then stores | Sound evaluation order for the used name target. |
| `91` | evaluated value becomes `put` | Sound. |
| `93-94` | update an existing map key | Sound map update. |
| `95-97` | insert an absent key, guarded by `notBool in_keys` | Sound and disjoint from the update case. |
| `99` | evaluate `If` test before selecting branch | Sound. |
| `100` | true selects `THEN` | Sound. |
| `101` | false selects `ELSE` | Sound. |
| `103` | evaluate `For` iterable before loop setup | Sound for the used name target. |
| `104` | a list value becomes `loop` | Sound for the supported iterator type. |
| `105` | empty loop finishes | Sound. |
| `106-107` | bind/update loop variable, execute body, then continue with tail | Sound order and mutation behavior for the submitted loop. |
| `109` | evaluate return expression | Sound for the used final return. |
| `110-111` | consume returned value and write `<result>` | Sound for this body because `Return` is the last statement. It would not model Python's abrupt return if a continuation followed, but that unused construct context is outside the submitted program. |
| `114-115` | name lookup from `<env>` | Sound binding behavior. |
| `116` | string literal to `str` | Sound. |
| `117` | empty list expression to a fresh empty list value | Sound in this value representation. |
| `120` | `Float(4.0) => num(4,1)` | CPython-faithful because 4.0 is exactly representable. |
| `121` | `Float(3.7) => num(37,10)` | **Unsound for the real generated Python program.** CPython's literal is exactly `4165829655317709/1125899906842624`, which exceeds `37/10` by `1/5629499534213120`. On input Python float `3.7`, this rule makes K return `"A"` while both Python implementations return `"A-"` (`stage3-krun-ieee-3.7-witness.log`, `stage3-ieee-bridge-python-success.log`). |
| `122` | `Float(3.3) => num(33,10)` | Value-incorrect for CPython. The literal witness is `3715469692580659/1125899906842624`, not `33/10`; this exact threshold happens not to change the final branch for the nearest floats. |
| `123` | `Float(3.0) => num(3,1)` | CPython-faithful; exactly representable. |
| `124` | `Float(2.7) => num(27,10)` | Value-incorrect for CPython. Literal witness: `3039929748475085/1125899906842624`, not `27/10`; as with 3.7, the binary value lies above the decimal threshold and changes the equality-threshold branch. |
| `125` | `Float(2.3) => num(23,10)` | Value-incorrect for CPython. Literal witness: `2589569785738035/1125899906842624`, not `23/10`. |
| `126` | `Float(2.0) => num(2,1)` | CPython-faithful; exactly representable. |
| `127` | `Float(1.7) => num(17,10)` | Value-incorrect for CPython. Literal witness: `7656119366529843/4503599627370496`, not `17/10`. |
| `128` | `Float(1.3) => num(13,10)` | Value-incorrect for CPython. Literal witness: `5854679515581645/4503599627370496`, not `13/10`; the binary value lies above the decimal threshold and can change the branch at the threshold. |
| `129` | `Float(1.0) => num(1,1)` | CPython-faithful; exactly representable. |
| `130` | `Float(0.7) => num(7,10)` | Value-incorrect for CPython. Literal witness: `3152519739159347/4503599627370496`, not `7/10`. |
| `131` | `Float(0.0) => num(0,1)` | CPython-faithful for comparisons used here; signed negative zero is an input concern, not this positive literal. |
| `133-134` | evaluate comparison left operand first | Sound Python evaluation order. |
| `135-136` | save left value, then evaluate right operand | Sound Python evaluation order. |
| `137-138` | rational equality by cross multiplication | Sound for positive-denominator `num` values. |
| `139-140` | rational greater-than by cross multiplication | Sound only when both denominators are positive. All claimed current values and literal denominators satisfy that condition, but the rule lacks a guard for the broader syntactic `num` domain. |
| `144-145` | evaluate the single append argument | Sound for the exact `Name(...).append(...)` call shape used. |
| `146-147` | mutate the named list by append and yield `none` | Sound list order, state update, and return value for the used operation. |

## `verification.k` rules (17)

All 13 `expectedGrade` equations are definitional summaries used only in
postconditions; none replaces operational execution:

| Location | Equation | Decision on the dependent domain `Q > 0` |
|---|---|---|
| `10-11` | exact 4.0 -> A+ | True. |
| `12-13` | non-4.0 and >3.7 -> A | True. |
| `14-15` | <=3.7 and >3.3 -> A- | True. |
| `16-17` | <=3.3 and >3.0 -> B+ | True. |
| `18-19` | <=3.0 and >2.7 -> B | True. |
| `20-21` | <=2.7 and >2.3 -> B- | True. |
| `22-23` | <=2.3 and >2.0 -> C+ | True. |
| `24-25` | <=2.0 and >1.7 -> C | True. |
| `26-27` | <=1.7 and >1.3 -> C- | True. |
| `28-29` | <=1.3 and >1.0 -> D+ | True. |
| `30-31` | <=1.0 and >0.7 -> D | True. |
| `32-33` | <=0.7 and >0 -> D- | True. |
| `34-35` | <=0 -> E | True. |
| `38` | `expectedGrades(.Vals)` | True base equation, but unused. |
| `39-40` | map `expectedGrade` over a `num` head | True constructor equation where it matches, but unused and not total over arbitrary `Vals`. |
| `45-70` | `gradingBody` constructor macro | True exact naming of the submitted loop body; not an operational bridge. |
| `75-82` | `solutionProgram` constructor macro | True exact naming of the submitted module after expansion; not an operational bridge. |

For positive denominators, the 13 `expectedGrade` guards are mutually
exclusive and exhaustive. Globally, line 10 and line 34 overlap at
`expectedGrade(0,0)` with different right sides, so the proof-local theory is
not reusable as a globally total function without narrowing.

## Claims (6)

| Claim | Plain-language precondition/postcondition and adequacy |
|---|---|
| `empty-input` | From empty env/input, execute the actual program and finish with empty `grades`, empty `result`, and returned empty list. Satisfiable and exact. |
| `all-single-grades` | For any integers `P,Q` with `Q>0`, a **singleton** input `[P/Q]` returns `[expectedGrade(P,Q)]` and records the exact final env. Satisfiable and result-constraining. Under the candidate K theory it is sound; it is false as a theorem about CPython for the exact binary ratio of input float 3.7 because literal thresholds were modeled as exact decimals. |
| `loop-step-new-variable` | With no existing `grade` key, process exactly one numeric head, append its expected grade, insert `grade`, and leave `loop(...,REST)` at the front. Sound one-step control-flow lemma; it does not process `REST` to a final return. |
| `loop-step-existing-variable` | Same one-step lemma when `grade` already exists; sound and result-constraining for that step only. |
| `loop-empty` | An empty internal loop becomes `.K`; all omitted cells are framed unchanged. Sound base transition, not a whole-program list theorem. |
| `prompt-example` | Exact five-element prompt input returns the five hard-coded expected strings and exact final env. Satisfiable and exact. |

There is no entry claim for an arbitrary finite `Vals` input and no claim from
`loop(...,REST)` to a final list containing `expectedGrades(REST)`.
Consequently, the one-step claims plus `loop-empty` are not a reachability
theorem for unrestricted list length.
