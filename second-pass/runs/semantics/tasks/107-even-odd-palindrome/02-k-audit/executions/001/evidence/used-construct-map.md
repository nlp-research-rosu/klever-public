# Submitted-program construct and execution map

The trusted translator output and the proof's expanded program parse to the
same KORE term (`regenerated-solution.kore` and
`verification-expanded.kore`, SHA-256
`6769acba55c58bacf72b53cb6d7f7b1f024cef4f01c061256593fc7bff5bb102`).

| Used construct / phase | Declaration | Rules exercised | Static review |
|---|---|---|---|
| Initial state | `semantics/core.k:49` | Configuration cells at `core.k:50-61` | Exact claims initialize module scope `0`, builtins scope `-1`, allocation counters, heap, stack, return, exception, and exit-code cells consistently with the supplied configuration. |
| `Module` and statement sequence | `semantics/syntax.k:61` | `core.k:125-127` | `#loadAll` exposes the real statement list; statements run left-to-right through `~>`. Empty lists disappear. |
| `FuncDef` | `semantics/syntax.k:53` | `functions.k:14-16` | Loading installs `closureVal("n", BODY, 0)` under the exact entry name in module scope; the body is not summarized. |
| Audit wrapper call | `verification.k:68` | `verification.k:69-71`; `call.k:20-21,69-75` | Fresh `#runEvenOdd` expands to load plus a real `Call`. Callee lookup and argument evaluation occur before the closure call. The closure rule allocates a callee scope and pushes the exact continuation. |
| Parameter binding and name reads | `syntax.k:12`; `functions.k:9`; `core.k:130` | `functions.k:63-66`; `core.k:131-154` | The single value argument binds to `n` in the new frame; `Name` follows the active scope/parent chain. No rule pins a result-bearing name to an oracle. |
| Integer literals | `syntax.k:9` | `core.k:194` | `Int(I)` becomes the same unbounded K integer. Inputs are within `1..1000`, so Python big-integer behavior and K integer behavior coincide. |
| `BinOp` | `syntax.k:15` with `seqstrict(2,3)` | `operators.k:12`; `int.k:9,13-16,19-20` | Operands evaluate left-to-right. Used operations are `+`, `-`, `*`, `%`, and `//`. `pyMod` plus `(a-pyMod(a,b))/b` implements Python floor division for the positive divisors `2,10,11,100`; no division by zero is reachable. |
| `Compare` / `CmpOp` | `syntax.k:30,32` | `operators.k:15-17`; `int.k:22,26` | Left then right evaluation; used comparisons are integer `<` and `==`, mapped directly to K integer predicates. |
| `If` | `syntax.k:49` with `strict(1)` | `controls.k:51-54`; `core.k:199-205` | Only the selected branch is placed in `<k>`. All reachable guards reduce to Boolean integer comparisons. |
| `Assign(Name, ...)` | `syntax.k:41` with `strict(2)` | `controls.k:9-11` | RHS is evaluated first, then the active callee scope is updated. The cell-specific priority rule is inapplicable because this function has no closure-cell annotation. |
| `AugAssign(Name, "+", ...)` | `syntax.k:44` with `strict(3)` | `controls.k:20-23`; `int.k:9` | RHS evaluates first, then current integer binding plus RHS replaces the binding. The heap-ref priority alternative is inapplicable to `even` and `odd`. |
| `TupleExpr` | `syntax.k:19` | `tuple.k:14-16`; `core.k:186-191,213-220` | Elements evaluate left-to-right and become an exact two-element `tuple(vCons(...))`; no allocation or opaque summary is used. |
| `Return` and frame restoration | `syntax.k:50` with `strict` | `functions.k:78-89` | Return evaluates its tuple, records it, discards the remaining function body, pops the one call frame, restores environment/scope location, deletes the callee scope, and resumes the saved continuation with that same tuple. Heap, exception, and exit code remain unchanged. |

No loop, collection heap allocation, string/float/sort/MD5 primitive,
exception, assertion, method, comprehension, or concrete-only rule occurs in
the submitted AST or the `#runEvenOdd` execution path. In particular,
`VERIFICATION` imports `MPY`, not `MPY-CONCRETE`.

## Proof-local declarations

- `solutionBody` and its sole equation (`verification.k:8-56`) are a
  definitional AST macro. Parser-level KORE identity connects it to the trusted
  translation.
- `solutionModule` and its sole equation (`verification.k:58-64`) bind that body
  to exactly `even_odd_palindrome(n)`.
- `#runEvenOdd` (`verification.k:68-71`) is a fresh wrapper and does not
  preempt a supplied semantic rule.
- `leadingDigit` and `currentBlock` (`verification.k:75-80`) are total
  arithmetic helpers with constant nonzero divisors.
- `evenPalindromes` and `oddPalindromes` (`verification.k:82-107`) occur only
  in the destination postcondition. Their four guards are pairwise disjoint
  over `1..1000` and jointly cover that domain; they never rewrite program
  execution. Their counting interpretation is:
  one-digit base counts `(4,5)`, two-digit palindrome counts split by the
  repeated digit, ten palindromes for every completed hundred-leading block,
  and `currentBlock` palindromes of the form `H?H` in the current block.

There are no proof-local priority, simplification, `owise`, `concrete`,
functional, no-evaluator, or opaque declarations, and no auxiliary loop/helper
claims.
