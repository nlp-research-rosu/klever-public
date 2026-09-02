# Static rule assessment

The exhaustive source inventory is `rule-inventory.txt`: 26 K files, 708
ordinary rules, 235 syntax declarations, five contexts, one configuration, and
three candidate claims. There are no local `[simplification]` rules and no
`[functional]` claims. This assessment partitions every inventoried item into
the material execution slice or the imported-but-inert slice.

## Candidate proof extensions

| Extension | Class and disposition |
|---|---|
| `isStringValue(str(_)) => true` | Definitional discriminator; true. |
| `isStringValue(_:Val) => false [owise]` | Definitional discriminator; disjoint fallback and exhaustive over ground `Val`; true. |
| `allStringValues(.ValSeq) => true` | Definitional fold base; true. |
| recursive `allStringValues` | Definitional fold; strict structural descent and total coverage; true. |
| `stringCodes(str(S)) => S` | Definitional projection; true on its equation domain. The declaration is marked `[total]` although no equation covers non-string `Val`; this is an over-broad totality annotation, but every theorem use is guarded by `allStringValues`. It fixes all intended-domain ground values and does not admit an opposite result there. |
| guarded `applyBin("+", str(A), V)` | Operational symbolic bridge. On every ground state satisfying `isStringValue(V)`, exhaustive discriminator equations force `V = str(B)` and the RHS normalizes to the supplied `applyBin("+", str(A), str(B))` result. It reads/writes no cells and does not alter continuation or control. The bridge-free constructor-domain theorem and ground witnesses close with `#Top`; the logically equivalent guard-form theorem remains stuck because the backend does not invert the discriminator constraint. No false intended-domain witness exists, but the candidate itself omitted a bridge-free theorem. |
| two `concatenateValues` equations | Definitional left fold by `seqConcat`; exhaustive structural cases and descent; true. Non-string meaning is irrelevant to guarded theorem uses. |
| two `finalLoopValue` equations | Definitional last-element fold; exhaustive structural cases and descent; true. |
| `concatenateLoopBody` | Constructor abbreviation only; expands to the exact translated `AugAssign` body. |
| `concatenateBody` | Constructor abbreviation only; expands to the exact translated function body. |
| `concatenateModule` | Constructor abbreviation only; expands to the exact translated module and binding. |

There are no candidate priority, simplification, concrete, opaque-symbol, or
`no-evaluators` declarations.

## Material supplied-semantics slice

The following supplied declarations/rules are reachable from the submitted
constructor term and were checked against the modeled Python subset:

- `semantics/syntax.k`: `Module`, `ImportFrom`, `FuncDef`, `Params`, `Assign`,
  `Name`, `Str`, `For`, `AugAssign`, `Return`, `ListExpr`, and `Call`, including
  strict/seqstrict evaluation attributes. These are syntax/evaluation-order
  declarations, not task-answer rules.
- `semantics/core.k`: configuration; `#loadAll`; statement sequencing; name and
  parent-scope lookup; `builtinsScope`; left-to-right `#evalArgs`; `#alloc`;
  `appendVal`; `vals2valSeq`; and literal/value subsorts. They preserve the
  heap, allocation counters, stack, return, exception, and exit cells except
  where their stated operation requires a change.
- `semantics/str.k`: ASCII source-literal conversion, `seqConcat`, and supplied
  string `applyBin("+", str(A), str(B))`. `seqConcat` is the ordinary
  structurally recursive sequence append. The literal conversion is sound on
  its explicit ASCII subset but does not cover a Unicode source literal.
- `semantics/list.k`: list iterator base/step, list literal left-to-right
  construction, and allocation. The list iterator yields each element once in
  order.
- `semantics/operators.k`: cooled binary dispatch to `applyBin`; no relevant
  reference-dereference rule is bypassed for string operands.
- `semantics/controls.k`: ordinary local assignment, ordinary `AugAssign`,
  inert `ImportFrom("typing", "List")`, `For` lowering, list-loop base/step
  continuation, and the one-time heap-reference dereference at loop start.
- `semantics/tuple.k`: `#bindTgt(Name, V)` updates the current function scope;
  the cell-variable priority alternative is refuted because this unannotated
  function frame has no `"$cells"` marker.
- `semantics/functions.k`: unannotated function binding, parameter binding,
  `Return`, `#endcall`, and `#pop`. The frame, environment, scope, and return
  state transitions match the actual call.
- `semantics/call.k`: callee lookup, left-to-right argument evaluation,
  unannotated closure call, frame allocation, and continuation restoration.
- `semantics.k`: `MPY` imports the proof semantics; `MPY-KRUN` adds only
  concrete rules for the fresh LLVM run.

The candidate loop claim frames every cell not mentioned. Its body touches only
the current scope map. Its arbitrary `CONT` is preserved rather than discarded,
and the actual continuation after the loop is the fixed `Return`/`#endcall`
path. No rule introduces an exception, output, or abrupt loop control on this
program.

## Imported-but-inert slice

Every other inventoried supplied rule is classified `INERT_FOR_THIS_THEOREM`.
This includes the remainder of the above material files and every rule in
`assert.k`, `bool.k`, `builtins.k`, `comprehension.k`, `concrete.k` (for the
Haskell proof), `dict.k`, `float.k`, `int.k`, `methods.k`, `range.k`, `set.k`,
`sort.k`, `subscript.k`, and the unused portions of `tuple.k`.

This partition is by rewrite-head reachability, not by an assumption that the
supplied semantics is a full Python semantics. The submitted term contains none
of those constructs, and their priority rules and function equations do not
overlap any reachable material redex. In particular, imported opaque
`sortVS`/`sortKeyVS`, float operators, and `md5hexCodes` never influence a
branch, result, cell, exception, or claim. The compiler's non-exhaustive-total
warnings for `mapStrVS`, several float conversions, `joinCodes`, and `valSeqAt`
are likewise outside the reachable slice.

No imported rule encodes this task's concatenation answer. The only
task-specific result summary is `concatenateValues`, whose exhaustive equations
literally define left-to-right `seqConcat` and do not replace the loop
execution.
