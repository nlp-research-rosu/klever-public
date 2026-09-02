# Static soundness analysis

## Inventory basis

`rule_inventory.md` enumerates every local `syntax`, `configuration`,
`context`, `rule`, and `claim` in the 24-file trusted supplied-semantics tree,
`semantics.k`, candidate `verification.k`, and candidate `spec.k`. It contains:

- 232 syntax declarations;
- 704 rules (465 equations and 239 operational rules);
- 5 contexts, 1 configuration, and 4 reachability claims;
- 150 `[function]`, 111 `[total]`, 25 `[symbol]`, 22
  `[no-evaluators]`, 54 `[concrete]`, 53 priority, and 29 `[owise]`
  occurrences;
- no local `[simplification]` rule and no `[functional]` declaration.

Every inventory entry was checked under one of these decisions:

- **USED / faithful**: reached by the submitted body and faithful to its Python
  operation on non-negative integer lists.
- **TRUSTED primitive**: deliberately opaque, external to the
  program-defined function, with the resulting theorem stated conditionally.
- **UNUSED / inert**: cannot be reached from any constructor in
  `solution.mpy`; no overlapping equation or global simplification can inject
  it into the task path.
- **PROOF helper**: structural definition checked for coverage, overlap, and
  descent.
- **EVIDENCE GAP**: plausible and true on every intended ground instance, but
  lacking the bridge-free universal K connection required for full validation.

## Used constructor-to-rule map

| Submitted constructor/operation | Declaration and rules | Decision |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement sequence | `syntax.k:41-61`; `core.k:124-127`; `functions.k:14-16` | USED / faithful. Full-module execution installs the same closure later used by the claims. |
| Direct entry call and `sort_array` binding | `call.k:19-21,69-75`; `functions.k:63-66,78-90`; `core.k:130-154` | USED / faithful. Callee lookup precedes left-to-right argument evaluation; the exact entry scope selects the closure, and return pops/restores the frame. |
| `Name("array")`, input `ref(0)` | `core.k:130-154`; ref dereference rules in `operators.k`, `subscript.k`, and `call.k` | USED / faithful. The input heap object is read, never written. |
| Empty test `if not array` | strict `If` syntax; `operators.k:10,44-46`; `bool.k:8`; `core.k:199-205`; `controls.k:51-54,95-97` | USED / faithful. A list reference is dereferenced for truthiness, and only the chosen branch executes. |
| Empty result `[]` | `list.k:13-15`; `core.k:183-191,117-121` | USED / faithful. A fresh heap list is allocated. |
| `array[0]` | `subscript.k:27-41`, `core.k:223-225` | USED / faithful. The nonempty preconditions make index zero in bounds. |
| `array[-1]` | fixed subscript rules plus candidate `verification.k:50-62` | EVIDENCE GAP for the candidate operational bridge; detailed below. |
| Integer `+`, unary `-`, `% 2`, and `== 1` | `operators.k:10-17`; `int.k:7-27` | USED / faithful. `pyMod` is used only with positive divisor 2. |
| `KwArg("reverse", true)` | `syntax.k:25`; `core.k:95-102` | USED / faithful. Keyword evaluation preserves argument order and produces `kwV`. |
| Builtin `sorted` lookup/call/allocation | `core.k:156-181`; `call.k:20-21,31,38-46`; `sort.k:18-24,34-37,51-66` | TRUSTED primitive for `sortVS`; allocation, input preservation, and reverse selection are formally executed. |

The proof path does not use `assert`, comprehensions, dictionaries, floats,
iterators, ranges, sets, strings, tuples, methods, closures with captured cells,
keyed sorting, or any other builtin. Their inventoried declarations/rules are
UNUSED / inert for this theorem. They contain no `[simplification]` rules that
can rewrite the task term globally. Inspection found no task-answer encoding
or overlap with the used constructor signatures.

The LLVM compiler reported incomplete `[total]` coverage for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. The first five are
unreachable here. `valSeqAt` is intentionally abstract for opaque/out-of-bounds
sequences; its actual first-index use is on `vCons` at index zero and reduces by
`subscript.k:12`. The entry preconditions exclude out-of-bounds execution. The
warnings expose partial/opaque cases, not a false equality used by the proof.

All used priority rules were checked against their lower-priority competitors:
ref dereference happens before generic operator/subscript/builtin dispatch, and
the sorted rules happen after the ordinary `Name("sorted")` lookup. Thus the
proof does not route a textual call name around binding or argument evaluation.

## Candidate verification declarations and rules, one by one

1. `sortArrayBody : Stmts [function,total]` and its sole equation
   (`verification.k:9-31`) are a constant definitional summary. Trusted
   translation, K parsing, and the generated pinning claim establish
   constructor identity with the submitted body.
2. `sortArrayClosure : Val [function,total]` and its sole equation
   (`verification.k:33-35`) bind exactly parameter `array`, the pinned body, and
   defining environment 0. This is the closure installed by full-module
   execution.
3. `intsVS : IntSeq -> ValSeq [function,total]` and its two equations
   (`verification.k:38-40`) are exhaustive, disjoint, structurally descending,
   and preserve every integer in order.
4. `nonNegativeIS : IntSeq -> Bool [function,total]` and its two equations
   (`verification.k:42-45`) are exhaustive, disjoint, structurally descending,
   and state elementwise non-negativity.
5. `snocVS : ValSeq × Val -> Val` and its two equations
   (`verification.k:50-53`) are the usual append-one definition over concrete
   constructor sequences; equations are disjoint and descend on the first
   argument. It is not declared `[function]`, so it remains a proof
   representation under an abstract middle.
6. The priority-40 last-index rule (`verification.k:55-62`) is an operational
   bridge. It reads no cell, writes no cell, preserves the entire continuation,
   and introduces no return/exception/frame effect. Its object is already a
   `list` value; the only skipped evaluation is the pure expression
   `UnaryOp("-", Int(1))`. Its value `L` controls the parity branch and
   therefore the final sort direction.

The bridge is the ordinary mathematical lemma
`last(F :: (M ++ [L])) = L`. Ground fixed-semantics constructor lists and
bridge-enabled `snocVS` representations agree for empty and one-element
middles, including an observable `+ 10` continuation. No false conclusion
witness exists on a finite non-negative integer list. However, removing the
bridge leaves both the exact `intsVS(MIDDLE)` claim and the broader admitted
`MIDDLE:ValSeq` claim stuck at the residual
`valSeqAt(vCons(F,snocVS(...,L)),vsLen(snocVS(...,L))) = L`. The candidate
provides no bridge-free universal connection theorem, and the bridge's
`ValSeq` match is broader than the entry claims' `intsVS` domain. This is an
EVIDENCE GAP, not an asserted semantic counterexample.

## Result-bearing opaque boundary

`sortVS` is declared by the supplied semantics as a total, no-evaluator symbol
for symbolic proof and has concrete insertion-sort equations for homogeneous
integer lists. It is a fixed external Python builtin, not program-defined code.
The symbolic theorem is interpretation-parametric: it proves that the odd path
returns a fresh `list(sortVS(input))`, and the even path returns a fresh reverse
of that value. It does not prove in K that `sortVS` is an ordered permutation.

The concrete LLVM run exercises the integer insertion-sort twin, and the
independent differential suite gives finite support over 9,649 cases. That
evidence supports—but does not universally prove—the named contract
“`sortVS(VS)` is Python's ascending `sorted` result.” No opposite
interpretation is ruled out by the K theory itself. This is an explicit trusted
primitive boundary, not an unconstrained program-derived oracle: all claims
remain conditional on the same fixed builtin contract.
