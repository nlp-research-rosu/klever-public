# Target-path semantics map and static rule judgments

This map complements `K-INVENTORY.md`, whose 705 parsed rule blocks, 233
syntax blocks, 45 priority rules, 22 `no-evaluators` declarations, and six
claims have complete source text and a per-entry disposition.

## Constructor-to-declaration map

The trusted regenerated `solution.mpy` uses only these MPY constructors:

| Construct | Declaration |
|---|---|
| `Module`, `FuncDef`, `Params`, statement sequencing | `semantics/syntax.k:53-61` |
| `Assign`, `AugAssign`, `While`, `If`, `Return`, `Expr` | `semantics/syntax.k:41-54` |
| `Name`, `Int`, `BinOp`, `ListExpr`, `Call`, `Attribute`, `Compare` | `semantics/syntax.k:9-30` |
| `CmpOp`, `Exprs` | `semantics/syntax.k:32,37` |

The candidate macros add no executable constructor. With `kast
--expand-macros`, `Module(triDefinition)` and trusted regenerated
`solution.mpy` have byte-identical JSON KAST
(`pinning-claim.ast.json`, `pinning-solution.ast.json`).

## Exact execution path

| Phase/operation | Fixed-semantics declarations and rules |
|---|---|
| Initial cells and builtins | `core.k:44-60`, `core.k:156-181` |
| Load module and sequence statements | `core.k:123-127` |
| Bind the function closure | `functions.k:13-20` |
| Resolve `tri` and local names | `core.k:129-154` |
| Evaluate the call and argument left-to-right | `call.k:18-21`, `core.k:183-191` |
| Create/bind/pop the call frame | `call.k:69-75`, `functions.k:62-90` |
| Evaluate integer literals | `core.k:193-196` |
| Allocate `[]` and return its reference | `list.k:12-15`, `core.k:117-121` |
| Assign `values` and `i` | `controls.k:8-31` |
| Execute/re-enter/exit the `while` | `controls.k:65-82`, `controls.k:85` |
| Evaluate `<=` and `==` guards | `operators.k:14-17`, `int.k:22-27` |
| Select nested branches | `controls.k:50-54`, `core.k:198-205` |
| Evaluate `%`, `//`, `+`, and `*` | `operators.k:10-12`, `int.k:9-20` |
| Bind and dispatch `values.append(...)` | `call.k:15-24`, `call.k:52-60`, `list.k:52-55` |
| Discard the append result | `controls.k:46-48` |
| Increment `i` | `controls.k:20-23`, `int.k:9` |
| Return the list reference and restore the caller | `functions.k:77-90` |

The relevant priorities are containment rules, not answer-bearing bridges:
list `append` at priority 40 preempts generic pure-method application;
heap-reference dereferences preempt generic value dispatch; cell-variable
priorities are inapplicable because the target frame has no `$cells` entry.
`BinOp`'s `seqstrict(2,3)`, `Assign`'s `strict(2)`, `AugAssign`'s `strict(3)`,
`If`'s `strict(1)`, `Return`'s strictness, and the explicit comparison
contexts preserve the source evaluation order.

## Per-module rule decision

Every rule block in these modules has an individual `ACCEPT`/boundary
disposition in `K-INVENTORY.md`; the grouped rationale below states the
selected-semantics judgment applied to all entries in each module.

| Module | Rules | Judgment |
|---|---:|---|
| `assert.k` | 3 | Accept for the MPY subset; ordinary success/failure assertion control. Concrete smoke only. |
| `bool.k` | 13 | Accept; disjoint short-circuit equations and correct reference-preserving truthiness. Unused by target except K Bool guard results. |
| `builtins.k` | 137 | Accept as supplied partial builtin model. Recursive equations descend and guarded cases are disjoint on their stated subset. `md5hexCodes` is an explicit opaque boundary, unreachable here. |
| `call.k` | 21 | Accept; callee then arguments, binding, allocation, and stack restoration match the target call. Priority dereferences are state-preserving on their guarded forms. |
| `comprehension.k` | 7 | Accept as syntax macros over fixed loops; unreachable here. |
| `concrete.k` | 16 | Accept as LLVM-only concrete support. It is imported by `MPY-KRUN` and not by the Haskell proof module `MPY`. |
| `controls.k` | 34 | Accept on the declared MPY subset. Target rules preserve name binding, branch order, loop continuation, mutation, and abrupt-control framing. Import no-ops and iterator snapshot limitations are unused modeling exclusions. |
| `core.k` | 46 | Accept; configuration, lookup, sequencing, allocation, literals, and structural helpers are truthful. Cell/keyword rules are guarded and unreachable in this capture-free target. |
| `dict.k` | 28 | Accept for well-formed ordered parallel key/value sequences; malformed/OOB and Python exception behavior are outside the subset and unreachable. |
| `float.k` | 121 | Boundary accepted but unused. The Haskell proof leaves named float operations opaque while LLVM has concrete equations; no float term can be produced on the target path. |
| `functions.k` | 15 | Accept for the documented non-escaping-closure subset. The target module-level closure, one parameter, return, and frame pop exactly satisfy that subset. |
| `int.k` | 16 | Accept on nonzero divisors. Target divisors are the literal 2; floor division, modulo, comparisons, addition, and multiplication agree with Python and integer mathematics. |
| `iter.k` | 0 | Protocol declarations only; unused. |
| `list.k` | 27 | Accept. Target uses literal allocation and the in-place append rule; sequence concatenation is structurally recursive and total. Deep equality is not used by the proof. |
| `methods.k` | 75 | Accept on the documented ASCII/single-separator subset; all unused by target. |
| `operators.k` | 10 | Accept; strict/contextual dispatch and structural heap dereference. Used integer cases resolve without overlap. |
| `range.k` | 6 | Accept for nonzero steps; unused by target. |
| `set.k` | 12 | Accept for the code-sequence set model; unused. |
| `sort.k` | 19 | Explicit opaque sort boundary for Haskell and concrete insertion sort for LLVM; unreachable here. |
| `str.k` | 28 | Accept for the documented ASCII code model; unused. |
| `subscript.k` | 40 | Accept on the stated valid/in-bounds, nonzero-step subset. OOB totalization is a documented modeling limitation and unreachable. |
| `syntax.k` | 0 | Constructor declarations and strictness/context attributes only. |
| `tuple.k` | 21 | Accept for exact-length valid unpacking; unused. |

No supplied or proof-local rule pattern-matches this task’s function call or
loop and replaces it with a task answer. No local rule has `priority`,
`simplification`, `concrete`, or `no-evaluators`; no local operational bridge
or opaque result symbol exists.

## Proof-local rules

| Extension | Decision |
|---|---|
| `triLoopCondition`, `triLoopBody`, `triFunctionBody`, `triDefinition` | Accept: parse-time macros only; expanded constructor identity is machine-checked. |
| `triValue(I<0)=0` | Accept: totalizes an excluded region and cannot affect an entry with `N>=0`, `I>=0`. |
| odd `triValue` equation | Accept: for `I=2k+1>=1`, gives `(k+1)(k+3)`, exactly the odd source branch. |
| even `triValue` equation | Accept: for `I=2k>=0`, gives `1+k`, exactly the even source branch and index-zero value. |
| `triComplete` base and step | Accept: guards `I>N` and `I<=N` are disjoint/exhaustive; the step increases `I`, so `N-I+1` decreases while active. |
| `triResult` | Accept: definitionally completes the empty prefix from index 0 through `N`. |

The odd recurrence claim is ordinary algebra: for `N=2k+1>=3`,
`triValue(N-1)+triValue(N-2)+triValue(N+1) =
(k+1)+k(k+2)+(k+2) = (k+1)(k+3) = triValue(N)`.
