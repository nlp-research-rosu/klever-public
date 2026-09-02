# Used-semantics dependency and soundness review

This review is keyed to the fresh scratch sources at
`/tmp/audit-work/75-is-multiply-prime`. The exhaustive 1,255-entry inventory is
in `rule-inventory.md`; this file traces the dependency slice that can actually
contribute to the eleven target claims.

## Constructor-to-semantics map

| Submitted/wrapper construct | Declaration | Executed fixed rules | Soundness decision on the complete used domain |
|---|---|---|---|
| `Module(Stmts)` and statement lists | `semantics/syntax.k:56-61` | `semantics/core.k:124-127` | Accept. `#loadAll` exposes the exact statement list; list sequencing preserves source order and the empty list terminates. |
| `FuncDef`, `Params` | `semantics/syntax.k:53,57,60` | `semantics/functions.k:14-16` | Accept. The rule installs a closure containing the exact body and defining scope. The submitted unannotated form cannot overlap the annotated closure rules. |
| Docstring `Expr(Str(...))` | `semantics/syntax.k:13,52` | `semantics/str.k:13-17`; `semantics/controls.k:48` | Accept. The ASCII docstring converts to a string value, then the expression-statement rule discards only that value. It has no state effect. |
| `Assign(Name, rhs)` | `semantics/syntax.k:12,41` with RHS strictness | `semantics/core.k:194`; `semantics/controls.k:9-18` | Accept. Both initial integer RHSs evaluate before assignment. The cell-writing priority alternative has a false `$cells` guard in these ordinary call frames, so the plain scope update is selected. |
| `While(condition, body)` | `semantics/syntax.k:46` | `semantics/controls.k:65-82,85` | Accept. Each iteration reevaluates the source condition, branches on its truth value, executes the body in order, and returns to the same loop head. The true and false guards are complementary. |
| `If(condition, then, else)` | `semantics/syntax.k:49` with condition strictness | `semantics/controls.k:51-54` | Accept. The condition evaluates first and the Boolean branch rules are disjoint. |
| `AugAssign(Name, op, rhs)` | `semantics/syntax.k:44` with RHS strictness | `semantics/controls.k:20-31`; `semantics/int.k:9-20` | Accept for these simple-name integer targets. The binding is read, the integer operation is computed, and the binding is updated. The ref-special priority rule is inapplicable because every target value is an integer. `factor` starts at 2 and only increases, so `%` and `//` never use a zero divisor. |
| `BinOp("*",...)`, `BinOp("%",...)` | `semantics/syntax.k:15` with left-to-right `seqstrict` | `semantics/operators.k:12`; `semantics/int.k:14-16,19-20` | Accept. The exact mathematical integer operations are used. `pyMod` agrees with Python's floored remainder for the positive divisor in all reachable calls. |
| Integer comparisons `<=`, `==`, `>` | `semantics/syntax.k:30,32`; comparison contexts at `semantics/operators.k:14-17` | `semantics/int.k:22-27` | Accept. Both operands evaluate in order and dispatch to the matching mathematical integer comparison. Operator-string cases used here are disjoint. |
| `Name` reads | `semantics/syntax.k:12` | `semantics/core.k:130-154` | Accept. Lookup starts in the current frame and follows its parent. All program locals are bound in the call frame. The priority cell-dereference rule is inapplicable because the frame contains no `$cells` marker. |
| Integer and Boolean truthiness | `semantics/core.k:25-42,199` | `semantics/core.k:200-205` | Accept. Loop/if comparison results are Booleans; the two Boolean outcomes are exact. |
| `Return(compare)` | `semantics/syntax.k:50` with strictness | `semantics/functions.k:77-90` | Accept. The expression evaluates first; return sets `retV`, discards the remainder of the callee body, and `#pop` restores the saved continuation, caller environment, frame map, and scope allocator. No heap state is touched. |
| Wrapper `Call(Name("is_multiply_prime"), Int(A))` | `semantics/syntax.k:28` | `semantics/call.k:18-21,69-75`; `semantics/core.k:183-196`; `semantics/functions.k:62-66,77-90` | Accept. It performs ordinary name lookup, evaluates the single argument, selects the installed closure by value, creates a fresh call frame, binds `a`, executes the exact closure body, then returns to the wrapper continuation. No call-result oracle or name-based shortcut exists. |
| Initial configuration and cells | `semantics/core.k:44-60` | Map/list hooks plus the call/return rules above | Accept. Claims instantiate module scope 0, builtins scope -1, empty heap/stack, `noRet`, `NoExc`, and exit code 0. A call temporarily uses scope 1 and restores all cells on return. |
| `#runIsMultiplyPrime(A)` | `verification.k:9-11` | `verification.k:17-48` | Accept as a proof-harness expansion. It loads the mechanically pinned exact submitted `Module`, then uses ordinary fixed lookup/call execution. It neither summarizes nor replaces the program-defined body. |
| `#forgetEntryPoint` | `verification.k:10`; rule at `verification.k:50-57` | Candidate-local cleanup rule | Accept as ghost bookkeeping. It runs only after a Boolean call result, requires the wrapper-installed binding to exist, removes exactly that global key using a K map update to `undef`, and preserves all other cells and any trailing continuation. It introduces no abrupt control or value equation. |
| `#expect(expected)` | `verification.k:11`; rule at `verification.k:15` | Candidate-local equality checkpoint | Accept. The same K variable occurs in the computed Boolean and expected position; unequal Booleans cannot match. No `owise`, totalization, priority, or oracle rule can erase a mismatch. |

## Evaluation, state, control, and overlap checks

- Evaluation order comes from `seqstrict` on integer binary operations, explicit
  comparison contexts, strict RHS/condition/return attributes, and the explicit
  left-to-right call-argument loop. Program operands are side-effect-free, but
  the fixed rules still preserve their source order.
- The only mutable state is the integer local-variable map in the fresh call
  frame. The heap remains empty. Call setup pushes one continuation frame;
  return removes it, restores environment 0 and `scopeLoc` 1, and leaves
  `NoExc`/exit code 0 unchanged.
- The used true/false guards (`truthy` versus `notBool truthy`) and integer
  operator strings are disjoint or complementary. Cell/ref priority rules have
  guards false in the submitted program's ordinary integer frames. The generic
  `Call` rule is `[owise]`, but none of the supplied special-call rules matches
  a call whose callee is the user closure obtained from the ordinary name.
- The used fragment has no candidate-local `[function]`, `[total]`,
  `[functional]`, `[simplification]`, `[concrete]`, opaque symbol, priority
  rule, or `owise` rule. `builtinsScope` is the only used supplied total
  function, and its single equation fixes the complete ground scope value.
- The proof imports `MPY`, not `MPY-KRUN`; therefore concrete-only float/sort
  evaluators and `MPY-CONCRETE` are absent from symbolic proof execution.

## Unused fixed-semantics boundaries

The exhaustive inventory exposes the supplied semantics' partial-language
boundaries: opaque float operations, opaque `sortVS`/`sortKeyVS`, opaque
`md5hexCodes`, total-but-partial sequence access, concrete-only evaluator rules,
and subset models for imports, strings, collections, builtins, methods,
comprehensions, and dictionaries. None of their constructors or dispatch
symbols occurs in the submitted module or wrapper (apart from the ordinary
ASCII docstring path described above), and none is reachable from a target
claim. They consequently supply no result, branch, state transition, lemma, or
logical axiom used to close this proof. They remain limitations of the supplied
language definition, not assumptions in this theorem.

## Task-answer encoding check

`verification.k` contains no prime predicate, factor-count summary, result
table, input case split, loop shortcut, or body-replacing operational bridge.
The true/false table appears only in `spec.k`, where each value is an obligation
behind `#expect`; it does not rewrite execution. Each ground obligation
therefore closes only after the actual function body computes the same Boolean.
The source contract's finite nonnegative portion is legitimately exhaustive:
2 through 99 are all present exactly once. The unbounded negative tail and
0/1 are not replaced by finite examples; they are covered by the symbolic
`A <Int 2` claim.
