# Static rule decisions

The complete machine-generated inventory is `static-rule-inventory.tsv`. It
contains 941 entries: 1 configuration, 231 syntax declarations, 5 contexts,
and 704 rules. The inventory found 148 function-bearing entries, 111
totality-bearing entries, 36 priority rules, 29 `owise` rules, 25 inventory
blocks mentioning `no-evaluators`, 5 macro-bearing entries, and no
`functional` or `simplification` attributes.

## Supplied-semantics files

Every entry below is byte-identical to the launcher-mounted trusted
`/reference/reference-semantics` tree. “Used” means that at least one entry in
the file is on the submitted program/proof path. “Inactive” means no symbol
from the file can be reached from that path. Fixed, inactive rules cannot
contribute to claim closure.

| File | Entries | Path status | Rule-by-rule decision |
|---|---:|---|---|
| `assert.k` | 3 | Inactive in proof; concrete smoke tests only | Accepted fixed semantics; no proof dependency. |
| `bool.k` | 14 | Inactive (the program uses `is None`, not `and`/`or`) | Accepted fixed semantics; no proof dependency. |
| `builtins.k` | 175 | Used only by `applyBuiltin("len",...)`, `seqLen(str(...))`, and `isLen` | The used rules exactly compute string length. All other entries are fixed and inactive. |
| `call.k` | 24 | Used | Callee/name and argument evaluation, closure dispatch, and builtin dispatch preserve left-to-right evaluation, bindings, frame state, and continuation for this program. |
| `comprehension.k` | 10 | Inactive | Accepted fixed semantics; no proof dependency. |
| `concrete.k` | 21 | Not imported by the Haskell proof definition | Accepted only as runtime smoke-test semantics; cannot contribute to symbolic claim closure. |
| `controls.k` | 37 | Used | The used import no-op, assignment, `If`, `For`, loop protocol, and dereference rules match the submitted control flow and state effects. |
| `core.k` | 84 | Used | Configuration, module loading, sequencing, lookup, literals, truthiness, argument evaluation, and `isLen` are coherent on the formal domain. |
| `dict.k` | 40 | Inactive | Accepted fixed semantics; no proof dependency. |
| `float.k` | 155 | Inactive | Accepted fixed semantics; all opaque float primitives are unreachable. |
| `functions.k` | 19 | Used | Function binding, parameter binding, return, frame pop, environment restore, and scope deletion match the submitted call. |
| `int.k` | 17 | Used only by integer `<=` and `>` | The used comparison rules are ordinary integer comparisons and are disjoint. |
| `iter.k` | 1 | Used | Declares the iterator protocol; behavior is supplied by iterable modules and the two local bridge rules. |
| `list.k` | 32 | Used by list values and iterator behavior | The fixed empty/cons iterator rules are correct; the submitted abstract `stringVals` term needs its local bridges before these patterns can match. |
| `methods.k` | 102 | Inactive | Accepted fixed semantics; no proof dependency. |
| `operators.k` | 12 | Used by comparisons and `is None` | Evaluation contexts and dispatch preserve operand order; the `is None`, `<=`, and `>` cases used here are correct. |
| `range.k` | 8 | Inactive | Accepted fixed semantics; no proof dependency. |
| `set.k` | 18 | Inactive | Accepted fixed semantics; no proof dependency. |
| `sort.k` | 25 | Inactive | Accepted fixed semantics; both opaque sort primitives are unreachable. |
| `str.k` | 33 | String values are used; string operations are otherwise inactive | The proof uses the `str(IntSeq)` value representation; `len` delegates to `isLen`. ASCII literal decoding is not used for symbolic inputs. |
| `subscript.k` | 57 | Inactive | Accepted fixed semantics; no proof dependency. |
| `syntax.k` | 16 | Used | Declares every submitted constructor; strictness annotations give the intended RHS/condition/iterable/return evaluation. |
| `tuple.k` | 25 | Used only by `#bindTgt(Name(...),...)` | The used rule updates the current local binding and is correct. |

The fixed 22 declarations carrying `no-evaluators` are `sortVS`, `sortKeyVS`,
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, and `md5hexCodes`.
The higher block count comes from nearby comments captured with preceding
multiline entries.
None is reachable from `solution.mpy` or any submitted claim.

## Submitted `verification.k`

The 13 local entries are decided individually:

| Lines | Entry | Class and decision |
|---|---|---|
| 8–9 | `StringSeq` syntax | Proof-domain inductive representation of arbitrary finite sequences of string-code sequences. Sound and unbounded. |
| 11 | `stringVals` syntax | Representation constructor from `StringSeq` to `ValSeq`. Sound declaration. |
| 12 | Empty `stringVals` equation | Truthful base representation equation. |
| 13–14 | Cons `stringVals` equation | Truthful constructor-by-constructor embedding. |
| 18–19 | Empty iterator bridge | Operational bridge. Its result and full state footprint agree with empty list iteration under the declared representation. |
| 20–22 | Cons iterator bridge | Operational bridge. It yields the head string and residual represented list, preserving the arbitrary continuation and every other cell. |
| 26 | `longestAcc` function/total declaration | Definitional summary. Uses are limited to `noneV` or `str(...)`; other `Val` cases remain uninterpreted despite `total` and contribute no equality. |
| 27 | `longestAcc` empty equation | Truthful base equation for every accumulator value. |
| 28–29 | `noneV` cons equation | Truthful first-element initialization and structural descent. |
| 30–32 | Strictly-longer equation | Truthful update, guarded by `>` and structurally descending. |
| 33–35 | Shorter-or-tied equation | Truthful retention, guarded by `<=` and structurally descending. The two integer guards are disjoint and exhaustive. |
| 39 | `longestSolution` macro syntax | Definitional name only. |
| 40–57 | `longestSolution` expansion | Constructor-identical to regenerated `solution.mpy`; it does not summarize or skip the body. |

The two iterator bridges are the only local priority rules and the only local
operational bridges. A bridge-free proof attempt in
`verification-no-iter-bridge.k`/`spec-iter-connection.k` did not close:
ordinary `stringVals` equations do not contextually reduce under
`#iterNext(list(...))`. Thus there is no machine-checked universal connection
theorem in the submission. This is an evidence gap, not a witnessed false
rule: on both constructor cases the bridge is exactly the intended list
iterator transition, accepts the same arbitrary continuation as the fixed
rules, and touches no other cell.

No local rule encodes the requested answer, introduces an oracle, fabricates a
program result, or overlaps with a contradictory local equation. The nonempty
entry claim stops at dispatch, but its exact destination is connected by the
fixed deterministic parameter-binding/initialization/`For`-lowering rules to
the source shape of the submitted result-bearing loop claims. Reachability
transitivity therefore composes the claims. The absence of a single submitted
assembled entry claim remains an auditability limitation, not a witnessed
soundness failure.
