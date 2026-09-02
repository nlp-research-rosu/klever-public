# Exhaustive local declaration and rule inventory

Source basis: scratch copies of `semantic.k`, `verification.k`, and `spec.k`.
There are no additional candidate-authored `.k` source files. Imported
`domains.md` modules are K's trusted builtin domains, not local rules.

## `semantic.k` declarations

- Lines 12–37 (`MPY-SYNTAX`): `Program = Module(Stmts)`; separatorless
  `Stmts`; exactly-two-name `Params`; comma-list `Exprs`; comma-list `CmpOps`;
  statement forms `FuncDef`, `Assign [strict(2)]`, `AugAssign [strict(3)]`,
  `If [strict(1)]`, `For [strict(2)]`, and `Return [strict]`; expression forms
  `Int`, `Str`, `Name`, `BinOp [strict(2,3)]`, `Compare [strict(1)]`,
  `Subscript [strict(1)]`, `Slice`, `Attribute [strict(1)]`, and
  `Call [strict(1)]`; plus `CmpOp` and `Bound = Expr | NoBound`.
- Lines 49–59 (`MPY-SEMANTIC`): value forms `intVal`, `strVal`, `listVal`,
  `boolVal`, and `boundStringMethod`; semicolon-list `Values`; every `Value`
  is a `KResult` and an `Expr`; `Function = function(Params, Stmts)`; and
  `Result = noResult | returned(Value)`.
- Lines 61–69: configuration `<py>` with `<k>`, `<env>`, `<functions>`,
  `<inputClass>`, `<inputExtensions>`, and `<result>`. There is no heap,
  call stack, exception cell, allocation state, or I/O state.
- Lines 71–75: internal K items `exec`, `setVar`, `loopValues`, `loopString`,
  and `#start`.
- Lines 132–133: `isUpperChar(String)` and `isLowerChar(String)`, both
  `[function, total]`.
- No local `[functional]`, `[simplification]`, `[priority]`, `[owise]`,
  `[anywhere]`, or opaque declarations occur. The `strict` attributes generate
  K heating/cooling machinery for the positions listed above.

## `semantic.k` rules

| ID | Line | Rule role | Static assessment |
|---|---:|---|---|
| S01 | 78 | `Module(S) => exec(S)` | Faithful module sequencing for this source. |
| S02 | 79 | empty `exec` disappears | Faithful. |
| S03 | 80 | split statement head and tail | Faithful left-to-right statement order. |
| S04 | 82–83 | register `FuncDef` in `<functions>` | Faithful for the target's capture-free, default-free top-level definition. |
| S05 | 87–92 | `#start` invokes exact named/bound function and binds two inputs | A task-specific driver, not a result oracle. It is faithful to a fresh call of this target, which has no globals or nested calls. |
| S06 | 95 | integer literal to `intVal` | Faithful. |
| S07 | 96 | string literal to `strVal` | Faithful. |
| S08 | 97–98 | `Name` lookup | Faithful for the target's local environment. |
| S09 | 100–101 | assign a value to a name | Faithful for the target's name assignments. |
| S10 | 102–103 | internal `setVar` update | Faithful loop-variable update. |
| S11 | 105–106 | integer `+=` | Faithful for the target. |
| S12 | 107–108 | integer `-=` | Faithful for the target. |
| S13 | 111 | nonempty-list index zero | Faithful on the target's nonempty-list normal domain; empty-list exception behavior is unmodeled. |
| S14 | 112–113 | nonempty-list slice `[1:]` | Faithful on every state reaching it in the target. |
| S15 | 117 | begin list iteration | Faithful. |
| S16 | 118 | finish empty list iteration | Faithful. |
| S17 | 119–120 | one list iteration then recurse | Faithful order and loop-variable persistence. |
| S18 | 122 | begin string iteration at index zero | Faithful subject to the K string-hook boundary. |
| S19 | 123–124 | stop string iteration at length | Faithful for nonnegative indices reached here. |
| S20 | 125–128 | expose substring `[I:I+1]`, execute body, increment | Faithful for tested K strings; K's string hooks are a builtin trust boundary. |
| S21 | 134 | `isUpperChar` iff code point is ASCII `A`–`Z` | **Unsound as Python `str.isupper` semantics on intended string inputs.** Witness U1 proves the K program returns `C.--` for `["--","É"]`, while both Python programs return `C.É`. The rule is also declared total without restricting `S` to the one-character strings on which `ordChar` is meaningful. |
| S22 | 135 | `isLowerChar` iff code point is ASCII `a`–`z` | **Unsound as Python `str.islower` semantics on intended string inputs.** Witness U2 proves the K program returns `C.é` for `["é","--"]`, while both Python programs return `C.--`. It has the same over-broad totality issue. |
| S23 | 137 | bind any named string attribute | Over-broad but produces no answer by itself; only the two target method names can subsequently reduce. |
| S24 | 138–139 | zero-argument `isupper` call uses S21 | Operational plumbing is exact, but it inherits S21's false value conclusion; witness U1. |
| S25 | 140–141 | zero-argument `islower` call uses S22 | Operational plumbing is exact, but it inherits S22's false value conclusion; witness U2. |
| S26 | 143 | true `If` executes then branch | Faithful. |
| S27 | 144 | false `If` executes else branch | Faithful. |
| S28 | 146 | integer `+` | Mathematically sound; unused by this submitted tree. |
| S29 | 147 | string concatenation | Faithful subject to K string representation. |
| S30 | 148–149 | target's single `>` comparison with RHS name lookup | Faithful for the exact translated comparison; intentionally not general comparison semantics. |
| S31 | 151–152 | terminal `Return` sets result | Faithful at the target's final-statement context. It does not model abrupt return through an arbitrary continuation, so the semantics is not reusable for a body with statements after `Return`; no such context is reachable in the submitted program. |

`BinOp [strict(2,3)]` does not enforce Python's left-to-right operand order, but
the submitted additions contain only side-effect-free names/literals/nested
concatenation, so no false target-program conclusion follows from that
over-breadth. `Compare` deliberately evaluates only its left operand because
S30 performs the exact right-name lookup; that is sound for the submitted
comparison and not a general comparison implementation.

## `verification.k` declarations and rules

- Lines 9–40: macro declaration `StrongestProgram` and macro rule V01, whose
  RHS is the full submitted constructor tree. Fresh `kast` results for the
  macro and `solution.mpy` are byte-identical.
- Lines 46–50: non-total `[function]` declarations `refDelta`,
  `refStrength`, `refStrengthAt`, `refStrongest`, and `refSelect`.
- V02–V04 (lines 52–57): three disjoint/exhaustive cases for `refDelta`
  relative to the Boolean outputs of `isUpperChar`/`isLowerChar`. They are
  mathematically consistent with those predicates but inherit S21/S22's
  mismatch with Python; the postcondition is therefore not independent at
  this primitive.
- V05 (line 59): `refStrength(S) = refStrengthAt(S,0)`.
- V06–V07 (lines 60–65): disjoint/exhaustive base and recursive character
  sum; recursion increments toward `lengthString(S)`.
- V08 (lines 67–68): initialize selection from a nonempty `strVal` list.
- V09 (line 69): return the best string at end of list.
- V10–V11 (lines 70–75): disjoint/exhaustive strict-greater replacement and
  less-or-equal retention. Strict comparison correctly keeps the first tie.
- There are no local simplification rules, priorities, ordinary
  execution-bypass bridges, opaque result symbols, or auxiliary reachability
  claims. The reference functions are definitional summaries, not operational
  rewrites of the submitted body.

## `spec.k` claims

There are seven entry claims (lines 7, 24, 37, 50, 63, 75, 87). Each starts
the exact macro program with empty environment/function maps and `noResult`,
and each requires normal completion to `.K` with a specific
`returned(strVal(... refStrongest(FIXED_LIST)))`. Only the class string is
symbolic in claims 2–7. No claim quantifies over an arbitrary extension list.
