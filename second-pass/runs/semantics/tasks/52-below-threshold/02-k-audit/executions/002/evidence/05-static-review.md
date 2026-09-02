# Static soundness assessment

The complete machine-generated inventory is `04-pinning-and-inventory.log`.
It enumerates every declaration block from the 24 supplied-semantics files,
`verification.k`, and `spec.k`: 703 rules, 232 syntax blocks, 5 contexts, one
configuration, and two claims. No `functional` or `simplification` declaration
occurs. There are 108 `total`, 48 `priority`, 36 `concrete`, 26 `owise`, 25
`symbol`, and 22 `no-evaluators` blocks.

## Rule-by-rule decision method

Every supplied declaration in the inventory was checked in source order.
Declarations on the target execution slice were compared with the submitted
constructor term and their complete cell effects. Declarations outside that
slice are marked **fixed/unreachable for this theorem**: their labels or sorted
arguments cannot occur while this submitted program executes, so they neither
contribute to closure nor enable a target conclusion. This is not a claim that
the unused minimal semantics is a full model of arbitrary Python. It is the
selected supplied semantics level, and its unmodeled/error behavior is outside
this theorem.

The fixed target slice is:

- `syntax.k`: `Module`, `FuncDef`, `Params`, `Expr(Str)`, `For`, `Name`, `If`,
  `Compare/CmpOp`, `Return`, `Bool`, and their `strict`/context declarations.
- `core.k`: statement sequencing, scope lookup, argument evaluation, Int/Bool
  literals, `truthy(Bool)`, `appendVal`, and the complete configuration cells.
- `str.k`: ASCII docstring construction.
- `operators.k` and `int.k`: left/right comparison evaluation and exact integer
  `>=`.
- `controls.k`: expression discard, branch selection, `For/#loop`,
  `#iterYield/#iterDone`, target binding continuation, and loop continuation.
- `tuple.k`: binding the loop target `Name("number")`.
- `call.k`, `functions.k`: direct closure call, left-to-right parameter
  binding, exact body execution, early/normal return, frame pop, scope cleanup,
  and result restoration.
- `verification.k`: the proof representation, mathematical result, exact body
  macros, and derived loop summary described below.

All used fixed rules preserve the observed state expected by the claims:
the callee frame is allocated at scope 1, parameters bind left-to-right, the
loop target updates only that frame, early `Return(false)` discards the
remaining function continuation, normal exhaustion reaches `Return(true)`,
and `#pop` restores environment 0, removes scope 1, restores `scopeLoc` 1,
empties the stack and `ret`, and leaves heap, exception, and exit code as
claimed. Integer comparison is mathematical K `>=Int`, so it agrees with
Python integers.

The other supplied modules (`range`, float operations, set, list construction
and mutation, tuple unpacking, subscript/slice, comprehension, methods,
builtins, sorting, assertions, dictionaries, and concrete-only keyed sorting)
are label/sort-unreachable on this target. Their rules remain listed
individually in the inventory. The Haskell proof excludes `MPY-CONCRETE`.
None of the 25 opaque supplied symbols is reached by the integer-domain proof.

The LLVM compiler reported non-exhaustive `[total]` coverage for supplied,
unused `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`
patterns involving values such as `cellsMark`. These are evidence limitations
in unused fixed semantics, not witnessed false equations and not used to close
either claim. They are therefore not labeled unsound. The target-local total
function `belowThresholdSpec` is constructor-exhaustive, disjoint, and
structurally descending.

## Complete local extension decisions

| Extension | Class and complete decision |
|---|---|
| `intsToVals(IntSeq)` | Fresh proof representation, not a function or oracle. It has no equations and cannot fabricate a value. |
| Empty `#iterNext(list(intsToVals(.IntSeq)))` | Operational representation bridge. It changes only `<k>`, exactly matching fixed `#iterNext(list(.ValSeq))`; its fresh constructor makes overlaps impossible. |
| Cons `#iterNext(list(intsToVals(iCons(I,R))))` | Operational representation bridge. It yields exactly `I` and the structurally smaller remainder, matching fixed `vCons` iteration. The two cases exhaust `IntSeq`, are disjoint, and preserve every other cell. |
| `belowThresholdSpec` base/step | Definitional summary. It is total over `IntSeq`, disjoint by constructor, structurally descending, and equals `all(I < T)`. It introduces no opaque result. |
| `belowThresholdLoopBody` | Macro only. Expanded KAST is constructor-identical to the translated `If` body. |
| `belowThresholdBody` | Macro only. Expanded KAST is constructor-identical to the translated function body, including the docstring and final return. |
| `#belowThresholdCall` | Macro only. The callee closure has exactly the translated parameter and body KAST and module environment 0. Fixed `FuncDef` creates the same closure; the initial empty module scope excludes shadowing. |
| `VERIFICATION` loop summary | Derived operational bridge/result summary. Its entire configuration, continuation, state footprint, and result are text-identical to the separately proved `LOOP-SPEC` claim after removing the label/priority attributes. `LOOP-SPEC` imports only `VERIFICATION-BASE`, so the proof is bridge-free and non-circular. No `<k>` ellipsis admits an extra suffix. |

The summary rule reads/writes all active cells rather than framing hidden state:
`k`, `env`, `scopes`, `scopeLoc`, `heap`, `heapLoc`, `stack`, `ret`, `exc`,
and `exit-code`. It accepts exactly the continuation
`Return(true) .Stmts ~> #endcall`, an empty heap, the exact single frame, and
the exact callee/module scope layout. Its only abstract frame content is
`BUILTINS:Scope`, preserved unchanged and irrelevant to the body. Priority 40
does not broaden this match domain.

Body sensitivity independently changed the macro-expanded branch result; the
bridge-free claim then failed on the reachable `I >= T` branch. The fresh
negated-result mutation also failed on the empty-list branch. Thus neither the
body bridge nor result summary is vacuous.

## Domain decision

The formal entry variable is `IS:IntSeq`; `intsToVals` therefore represents
only lists whose elements are K `Int`, and `T:Int` restricts the threshold to
an integer. The source annotation says only `l: list`, and its contract says
"all numbers"; the trusted canonical implementation has defined behavior for
numeric floats. For example, `[4.5], 5` returns true and `[5.0], 5` returns
false in both Python implementations, but neither list has an `IS:IntSeq`
instance. This is a material source-contract restriction, not a false local
rule. Under the benchmark decision mapping, this sound integer-only theorem is
not a legitimate proof of the full requested contract.
