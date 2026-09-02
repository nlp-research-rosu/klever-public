# Static soundness assessment

This is the reviewer’s compact decision record for the exhaustive source/index
artifacts `05_numbered_k_sources.txt` and `05_rule_inventory.tsv`.

## Inventory coverage and provenance decision

- Supplied baseline: 1 configuration, 227 `syntax` declaration starts, 5
  contexts, and 695 rule starts across 24 `.k` files (2,211 lines).
- Candidate-local proof theory: 3 syntax/function declarations and 6 equations
  in `verification.k`, plus 2 reachability claims in `spec.k`.
- There are no candidate-local priority, `owise`, `concrete`,
  `simplification`, `functional`, `symbol`, or `no-evaluators` attributes.
- The supplied baseline has 50 priority annotations and 25 explicit
  `symbol(...)` declarations. Every supplied entry is accepted as
  `TRUSTED_SUPPLIED_BASELINE` because the candidate tree is recursively and
  byte-for-byte identical to `/reference/reference-semantics`; this is a
  provenance decision under `SUPPLIED_SEMANTICS`, not a proof that the whole
  baseline equals CPython.
- No baseline file contains task-specific terms `intersection`, `noDivisors`,
  `primeResult`, `is_prime`, `"YES"`, or `"NO"`.

## Candidate-local rule decisions

| Extension | Class and decision | Guard/coverage/termination | Value/control impact |
|---|---|---|---|
| `intersectionBody` and its equation | Definitional abbreviation; sound | Zero-argument function with one unconditional equation. Independent constructor comparison found exact identity with the trusted translation’s function body. | Supplies the body of the closure pinned in the entry claim; does not skip execution. |
| `noDivisors(N,I)`, `I < 2` | Definitional equation; sound | Redirects once to lower bound 2. Disjoint from both `I >= 2` equations. | Mathematical summary only. |
| `noDivisors(N,I)`, `I >= 2 and I >= N` | Definitional equation; sound | Empty half-open divisor range, so result `true`; disjoint and terminating. | Mathematical summary only. |
| `noDivisors(N,I)`, `I >= 2 and I < N` | Definitional recursion; sound | Checks positive divisor `I`, then increases `I` by one. Together the three guards cover all integer pairs and overlap nowhere. | Fixes the loop flag summary; does not rewrite Python syntax. |
| `primeResult(N)`, prime guard | Definitional equation; sound | `N >= 2 and noDivisors(N,2)`. | Fixes the result to `"YES"`. |
| `primeResult(N)`, non-prime guard | Definitional equation; sound | `N < 2 or not noDivisors(N,2)`. This is the disjoint Boolean complement of the prime guard. | Fixes the result to `"NO"`. |
| `SPEC.divisor-loop` | Derived reachability circularity; sound | Precondition `2 <= I <= N` is satisfiable. One real loop iteration changes `(I,P)` to `(I+1, P and pyMod(N,I) =/= 0)`, exactly the recursive `noDivisors` equation; at `I=N`, the empty-range equation is `true`. | Matches the real `#while` head and exact body; writes only `divisor` and `is_prime`; framed continuation and omitted cells are preserved. |
| `SPEC.intersection` | Entry theorem; sound and result-constraining | Ordered endpoints are a satisfiable precondition. | Calls the pinned closure under fixed call/frame rules. Destination is the total, exhaustive `primeResult` function, not a free variable or implication. |

No operational bridge, opaque result oracle, answer-encoding rewrite,
simplification lemma, or displaced program-defined operation exists in the
candidate-local theory.

## Used-construct path

| Submitted constructor/operation | Supplied declaration and behavior used |
|---|---|
| `Module`, `FuncDef`, `Params` | `semantics/syntax.k`; module sequencing and function binding in `core.k`/`functions.k` |
| `Call`, `Name`, two arguments | `call.k` evaluates callee then arguments; `core.k` performs scope-chain lookup and left-to-right argument accumulation |
| Function invocation and return | `call.k` allocates the exact plain frame; `functions.k` binds both parameters, records return, pops the frame, and restores caller cells |
| `Subscript(..., Int(0/1))` on two-element tuples | `subscript.k` plus tuple/sequence helpers; both indices are provably in bounds, so the baseline’s underspecified out-of-bounds totality is unreachable |
| `max`/`min` with two integer arguments | builtins scope lookup; generic call dispatch; `applyBuiltin`, `maxVals`, and `minVals` in `builtins.k` |
| assignments and statement lists | strict RHS evaluation and local map updates in `syntax.k`, `core.k`, and `controls.k` |
| integer `-`, `+`, `%`, `<`, `==` | dispatch in `operators.k`; exact integer equations and `pyMod` in `int.k`; divisor is always at least 2 |
| `If`, `While`, Boolean flag | strict guards, `truthy`, `#branch`, `#while`, `#whileCond`, and `#loopLbl` in `core.k`/`controls.k` |
| `Str("YES"/"NO")` | ASCII `strToCodes` rules in `str.k` |

All state relevant to this path is explicit: current environment, scopes and
allocator, heap and allocator, call stack, return state, exception state, and
exit code. The entry claim fixes them before and after the call; the loop claim
frames the nonlocal cells and its continuation.

## Supplied opaque and priority boundaries

The 25 explicit supplied opaque symbols are:
`sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, and `md5hexCodes`.

None is syntactically reachable from this integer/tuple/max/min/loop program or
appears in either proof-local helper or postcondition. The baseline priority
rules concern cell references, heap objects, special calls, collection
allocation/mutation, float/math/hashlib calls, and concrete sort/deep-equality
legs. The target’s used path has plain frames, bare tuple values, integer
operators, and generic calls; no task-local priority rule preempts fixed
execution.

The compile-time non-exhaustiveness warnings concern supplied helpers
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and out-of-bounds/opaque
`valSeqAt`. All except `valSeqAt` are unreachable here; `valSeqAt` is reached
only at indices 0 and 1 of explicit two-element tuples, where its ordinary
equations reduce exactly.
