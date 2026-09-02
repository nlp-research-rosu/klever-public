# Used-construct and proof-path map

All paths below are relative to the clean scratch source root. The entire
`reference-semantics/` tree is byte-identical to the trusted supplied tree.

| Submitted construct / proof term | Declaration | Executing rules | Audit decision |
|---|---|---|---|
| `Module(Stmts)` and statement sequence | `semantics/syntax.k:61`, `semantics/core.k:124` | `core.k:125-127` loads and sequences the exact module | Sound for this use; no source statement is skipped. |
| `FuncDef`, `Params` | `syntax.k:53,57` | `functions.k:12-14` stores `closureVal` in the current module scope | Exact unannotated function body and defining environment are retained. |
| `Call(Name("intersection"), ...)` | `syntax.k:28` | `call.k:19-21` evaluates callee then arguments; `core.k:189-192` evaluates arguments left-to-right; `call.k:69-74` creates the callee frame; `functions.k:64-91` binds, returns, and pops | Exact closure lookup, arity-two binding, body execution, return, stack restoration, and scope deallocation execute. No proof-local call interception exists. |
| `Name` | `syntax.k:12` | `core.k:131-155` walks scope parents | Every used lookup resolves in the exact plain callee frame; cell-reference priority rules are inapplicable because the frame has no `$cells` marker. |
| `Int`, `Bool` literals | `syntax.k:9,11` | `core.k:194-196` | Exact K `Int`/`Bool` values. |
| `Assign(Name, rhs)` | `syntax.k:41` (`strict(2)`) | `controls.k:9-18` | RHS evaluates first, then the plain local map is updated. Cell-write alternative is inapplicable. |
| `Subscript(tuple, 0/1)` | `syntax.k:22`; helpers `subscript.k:11,21,37` | `subscript.k:27-40`; `core.k:223-225` computes tuple length | Inputs are exactly `vCons(A,vCons(B,.ValSeq))`; indexes 0 and 1 reduce to A/B. The supplied semantics' opaque out-of-bounds totalization of `valSeqAt` is unreachable. |
| `If` | `syntax.k:48` (`strict(1)`) | `controls.k:51-54` | Condition evaluates before exactly one branch. Used conditions are Bool, so `truthy` is exact. |
| `Compare`/`CmpOp` | `syntax.k:30,32` | `operators.k:15-20`, then integer cases `int.k:22-27` | Left then right evaluation is fixed by contexts; all submitted comparisons are integer comparisons with nonoverlapping exact cases. |
| `BinOp` `-`, `*`, `%`, `+` | `syntax.k:15` (`seqstrict(2,3)`) | `operators.k:12`; integer cases `int.k:9-20` | Left-to-right integer arithmetic. `%` uses `pyMod`; every reached divisor is at least 2, so zero-divisor behavior is irrelevant. |
| `BoolOp("and", ...)` | `syntax.k:16` | `bool.k:13-25` | Head-only context implements short-circuit order. Both reached operands are Bool. Heap-ref priority alternatives are inapplicable. |
| `While` and loop continuation | `syntax.k:45` | `controls.k:65-92` | Guard reevaluates at each `#while`; true runs body then `#loopLbl`, false exits. No break/continue/call is present in the body. |
| `Return` | `syntax.k:50` (`strict`) | `functions.k:78-91` | Exact string value is stored in `ret`, the rest of the function body is discarded, then the caller frame and cells are restored. |
| `Str("YES")`, `Str("NO")` | `syntax.k:13` | `str.k:13-17` | ASCII code sequences reduce exactly to 89,69,83 and 78,79. Both strings satisfy the ASCII guard. |
| Tuple inputs in claims | value declaration `core.k:17-20` | no construction rule is needed; claims inject exact two-element tuple values | Shape and integer element sorts exactly formalize the stated interval-pair domain. |
| Configuration/cells | `core.k:49-61` | rules above read/write `k`, `env`, `scopes`, `scopeLoc`, `heap`, `heapLoc`, `stack`, `ret`, `exc`, `exit-code` | Entry claims pin all cells; the loop claim pins all except it soundly frames stack and the `<k>` continuation, neither of which its body changes. |
| `PRIME-LOOP-COND`, `PRIME-LOOP-BODY`, `INTERSECTION-BODY`, `SOLUTION-MODULE` | `verification.k:9,17,25,45`, each `[macro]` | macro expansions at `verification.k:10-48` | Syntactic abbreviations only. Fresh `kast --expand-macros` output is byte-identical to parsing submitted `solution.mpy`. |
| `trialPrime(N,D)` | `verification.k:53` `[function,total]` | four equations `verification.k:54-63` | True definitions: first separates `N<2 or D<2`; otherwise `D^2>N` versus `D^2<=N`; the latter splits remainder zero/nonzero. Guards are exhaustive and pairwise disjoint. Recursive case raises D and reaches the square bound. |
| `primeAnswer(N)` | `verification.k:65` `[function,total]` | two equations `verification.k:66-69` | Exhaustive, disjoint Bool split; returns exact YES/NO values. |

## Overlap, priority, opacity, and global-rule review

- The proof definition imports `MPY`, not `MPY-KRUN`, so the 16 rules in
  `semantics/concrete.k` are absent from symbolic proof execution. The fresh
  LLVM definition intentionally imports them only for concrete testing.
- No audited source has a `[simplification]` rule or a `functional`
  declaration. The only proof-local functions are `trialPrime` and
  `primeAnswer`; the only proof-local syntax rules before them are macros.
- Relevant supplied priority rules are the cell, heap-ref, and subscript
  alternatives described above. Their guards or constructor patterns are false
  on the exact plain-frame, unboxed-tuple proof path, so they do not overlap the
  selected generic rules. Generic `Call` and `Compare` rules marked `[owise]`
  are reached only after no specialized pattern matches.
- The supplied semantics contains opaque or partially evaluated total symbols
  for unrelated language features (notably floats, sorting, MD5, and the
  out-of-bounds branch of `valSeqAt`). None occurs in the submitted AST or can
  be produced on the exact entry-claim path. `valSeqAt` does occur but reduces
  through its concrete in-bounds equations before any opaque case.
- No rule in `verification.k` rewrites `Call`, `#applyK`, `While`, `#while`,
  `Return`, or any configuration cell. Thus there is no operational bridge,
  oracle, fabricated return, priority override, or execution bypass.
