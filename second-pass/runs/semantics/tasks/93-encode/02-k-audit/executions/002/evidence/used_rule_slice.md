# Reachable rule slice for `solution.mpy`

This is a reviewer-authored dependency slice of the complete line-addressed
inventory in `k_rule_inventory.txt`. Entries not listed here are dormant:
their left-hand-side constructors, callable names, value sorts, or continuation
markers are absent from every reachable configuration of the submitted
program and its three claims.

## Submitted constructors and syntax

- `semantics/syntax.k:9-30`: `Int`, `Name`, `Str`, `BoolOp`, `BinOp`,
  `Call`, `Attribute`, and `Compare`.
- `semantics/syntax.k:32,37`: `CmpOp` and `Exprs`.
- `semantics/syntax.k:41-54`: `Assign`, `AugAssign`, `For`, `If`, `Return`,
  and `FuncDef`.
- `semantics/syntax.k:56-61`: statement lists, parameters, parameter names,
  and `Module`.
- `semantics/core.k:13-42`: `IntSeq`, `str`, values, scopes, result sorts,
  exception state, and return state.

## Entry, call, binding, and return

- `semantics/core.k:49-60`: initial configuration (concrete module run).
- `semantics/core.k:68-70`: the non-reference discriminator used to refute
  heap-reference priority alternatives.
- `semantics/core.k:124-127`: module loading and statement sequencing.
- `semantics/core.k:130-154`: lexical lookup; the cell-specific priority
  branch is refuted because the reachable frames have no `"$cells"` entry.
- `semantics/core.k:157-181`: the concrete builtins scope.
- `semantics/core.k:185-191`: left-to-right argument evaluation.
- `semantics/core.k:213-215`: order-preserving append to the evaluated
  argument sequence.
- `semantics/functions.k:14-16`: creation of the concrete module binding.
- `semantics/functions.k:63-75`: parameter binding; the cell-specific priority
  branch is refuted by the plain frame.
- `semantics/call.k:16-24`: attribute cooling, callee evaluation, argument
  evaluation, and bound-method dispatch.
- `semantics/call.k:31-32`: generic builtin/type dispatch.
- `semantics/call.k:69-75`: exact user-closure frame creation and continuation
  capture.
- `semantics/functions.k:78-90`: return, frame pop, environment restoration,
  and result delivery.

## Loop and state

- `semantics/controls.k:9-18`: assignment to the current local frame; the
  cell-specific priority branch is refuted.
- `semantics/controls.k:20-23`: non-reference augmented assignment.
- `semantics/controls.k:51-54`: Boolean branch selection.
- `semantics/controls.k:65-74`: `For` desugaring, iterator step, target bind,
  body execution, and recursive loop continuation.
- `semantics/controls.k:85`: loop-label continuation.
- `semantics/tuple.k:31-41`: binding the one-character iteration result to
  local name `char`; the cell-specific branch is refuted.
- `semantics/iter.k:8`: iterator protocol declarations.
- `semantics/str.k:8-10`: string iterator completion and one-character yield.

## Expression evaluation and primitives

- `semantics/core.k:194-205`: integer/Boolean literals and Boolean truth.
- `semantics/operators.k:12,15-17`: binary dispatch and left-to-right
  comparison evaluation.
- `semantics/int.k:9,26`: integer addition and equality.
- `semantics/bool.k:16-25`: left-to-right, value-returning short-circuit `or`.
- `semantics/str.k:13-17`: the reachable empty string literal.
- `semantics/str.k:20-24`: string concatenation and its structural recursion.
- `semantics/methods.k:10,21`: bound `swapcase` dispatch.
- `semantics/methods.k:112-119,149-152,162-164`: ASCII case predicates,
  per-code-point case swap, and structural string map.
- `semantics/builtins.k:17,143-145`: `ord` on exactly one code point and
  `chr` on a proved ASCII result.

## Proof-local definitions

- `verification.k:8-56`: two syntax macros only. Macro expansion is
  constructor-identical to the submitted module, as checked in
  `pinning.log`.
- `verification.k:59-64`: a closed Boolean equation for the ten ASCII vowel
  code points.
- `verification.k:66-70`: two disjoint, exhaustive `encodeCode` equations.
- `verification.k:74-82`: structurally descending accumulator equations and
  the empty-accumulator wrapper.
- `spec.k:8-98`: end-to-end, initialization, and loop reachability claims.

## Static decisions

- The reachable rules preserve evaluation order, local bindings, scopes,
  heap/stack state, call/return control, exceptions, and exit status.
- Every reachable priority rule is either refuted by a concrete no-cell/no-ref
  frame shape or is the intended exact dispatch for the matching receiver.
- Every reachable total function has constructor-complete, disjoint equations.
- No reachable `[no-evaluators]`, opaque sort/digest/float symbol,
  `[simplification]`, `[anywhere]`, or proof-local operational bridge exists.
- All remaining inventory records are dormant for this theorem. Since none of
  their constructors or markers can be produced by the reachable slice, they
  cannot enable a conclusion—true or false—in any submitted claim.
