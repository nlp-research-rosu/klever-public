# Proof-extension audit

The exhaustive declaration IDs are from `k-rule-inventory.json`.

## `digitSumBuiltins` (IDs 929-930)

- Class: compile-time definitional macro.
- Domain/context: the exact `Scope` token in the claims.
- State/value influence: fixes the root lookup map, including `ord`.
- Review: the 23 bindings and `root` parent agree with the supplied
  `builtinsScope` equation in `semantics/core.k:157-181`. Map order is not
  observable. It performs no operational rewrite and contains no task answer.
- Decision: sound at the selected semantics level.

## `digitSumLoopBody` (IDs 931-932)

- Class: compile-time definitional macro.
- Domain/context: the exact macro token.
- State/value influence: assigns `code`, tests inclusive bounds 65 and 90, and
  conditionally augments `result`.
- Review: after list-sugar normalization, it is the exact `For` body in
  `solution.mpy:7-13`. It contains no opaque value.
- Decision: truthful syntactic copy, but the theorem still does not depend on
  the submitted file; see the separate pinning failure.

## `digitSumBody` (IDs 933-934)

- Class: compile-time definitional macro.
- Domain/context: the exact macro token.
- State/value influence: the complete copied function body.
- Review: after expanding `digitSumLoopBody`, it matches
  `solution.mpy:3-14`: initialize `result`, `char`, and `code`; run the loop;
  return `result`.
- Decision: truthful syntactic copy, with the same artifact-pinning caveat.

## `digitSumSpec` (IDs 935-937)

- Class: result-bearing definitional summary.
- Domain: every freely generated finite `IntSeq`.
- Coverage/overlap/descent: `.IntSeq` and `iCons(C, REST)` are disjoint and
  exhaustive; the recursive call is on the structural tail.
- Value influence: it is the final result of the loop and entry claims.
- Value justification: its two equations define exactly the sum of those code
  points in inclusive range 65..90. There is no opaque or fresh symbol.
- Decision: mathematically valid and total. It characterizes the submitted
  copied algorithm, but not the trusted canonical behavior for non-ASCII
  uppercase characters.

## Initialization operational lemma (ID 938)

- Class: derived operational bridge.
- Complete matched context: a direct call of the exact closure and exact
  singleton argument list; no trailing `<k>` continuation; environment 0;
  exact module and builtin scopes; `scopeLoc=1`; empty heap; `heapLoc=0`;
  empty stack; `noRet`; `NoExc`; exit code 0.
- State footprint: creates scope 1 with `s`, `result`, `char`, and `code`;
  moves environment to 1; increments `scopeLoc`; pushes the exact empty
  continuation frame. Heap, return, exception, and exit cells are preserved.
- Justification scope and containment: `spec.k:46-82` is the same transition,
  proved against main module `DIGIT-SUM-VERIFICATION`, which does not import
  either operational lemma. Evidence `03_prove_initialization.log` is exit 0
  and `#Top`. The rule's complete match is the theorem's complete domain.
- Decision: sound derived rewrite on its exact domain.

## Loop operational lemma (ID 939)

- Class: result-bearing derived operational bridge.
- Complete matched context: the exact `#loop` token over `str(S)`, target
  `char`, copied body, and exact suffix `Return(result) ~> #endcall`;
  environment 1; exact scopes 0/-1/1; `scopeLoc=2`; empty heap;
  `heapLoc=0`; exact single frame with empty continuation; `noRet`; `NoExc`;
  exit code 0.
- State footprint: consumes the loop and return, restores environment 0,
  removes scope 1, restores `scopeLoc=1`, pops the frame, and returns the
  integer `A + digitSumSpec(S)`. Heap, return, exception, and exit cells end in
  their stated values.
- Value influence: it supplies the entry claim's final result.
- Justification scope and containment: `spec.k:6-39` is the same universal
  transition and proves against `DIGIT-SUM-VERIFICATION`, with no operational
  lemma imported. `03_prove_loop.log` is exit 0 and `#Top`; K's circularity is
  the induction over the structurally shorter string iterator. The rule admits
  no broader continuation or framed cells.
- Decision: sound derived rewrite on its exact domain. The priority affects
  selection only after this exact match and does not expand it.

## Opaque, simplification, and ordinary-rule conclusion

`verification.k` introduces no opaque symbol, simplification rule, or
unconstrained oracle. The supplied semantics contains 22 `no-evaluators`
symbols (float, sorting, and MD5 boundaries), all enumerated in
`05_special_inventory_python.log`; none occurs in the submitted AST, either
auxiliary proof, either operational lemma, or the final result.

No reviewed candidate-local rule enables a false conclusion on its declared
domain. Accordingly, no rule is labeled unsound. The decisive defect is
instead theorem-to-artifact pinning: a body mutation does not change the
theorem term or invalidate the proof.
