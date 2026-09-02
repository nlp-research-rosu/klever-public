# Used-construct and rule-path map

This map covers every source construct in the submitted `solution.mpy` and the
rules exercised by the two entry claims. Line numbers refer to the trusted,
scratch-copied source tree.

## Submitted syntax

| Submitted construct | Declaration |
|---|---|
| `Module` | `semantics/syntax.k:61` |
| `FuncDef` | `semantics/syntax.k:53` |
| `Params` / parameter-name list | `semantics/syntax.k:57`, `:60` |
| statement sequence | `semantics/syntax.k:56` |
| `If` | `semantics/syntax.k:49` |
| `Compare` / `CmpOp` | `semantics/syntax.k:30`, `:32` |
| `Name` | `semantics/syntax.k:12` |
| `Int` | `semantics/syntax.k:9` |
| `Return` | `semantics/syntax.k:50` |
| `ListExpr` | `semantics/syntax.k:17` |
| `Subscript` | `semantics/syntax.k:22` |
| `Call` / expression list | `semantics/syntax.k:28`, `:37` |
| `Slice` / `NoBound` | `semantics/syntax.k:38`, `:39` |
| unary minus | `semantics/syntax.k:14` |

The scratch `krun solution.mpy` output records a `closureVal` whose parameter
names and body are the same AST as the `maximumBody` macro. The trusted
translator also regenerated the submitted file byte-identically.

## Entry-call execution

1. `call.k:20-21` evaluates the callee and arguments left-to-right. `core.k`
   name lookup resolves `maximum` in scope 0.
2. `call.k:69-74` invokes the exact `closureVal`, pushes the continuation,
   allocates scope 1, and changes `<env>` to 1. `functions.k:63-66` binds
   `arr=list(VS)` and `k=K`.
3. `operators.k` evaluates the comparison in order; `int.k` interprets
   integer equality. `controls.k` selects the `If` branch.
4. For `k=0`, `list.k` evaluates the empty literal and `core.k` allocates it
   at heap location 0. `functions.k:78-90` returns `ref(0)`, consumes the
   trailing statement, pops the call frame, restores scope/env/stack/ret, and
   leaves the allocated result live.
5. For `k>0`, normal lookup reaches the supplied builtins frame and resolves
   `sorted`. `sort.k:36-37` allocates `list(sortVS(VS))` at heap location 0.
6. `subscript.k:31-33` dereferences that list. Slice-bound rules at
   `subscript.k:50-61` evaluate `-k`, the omitted high bound, and the omitted
   step in order. The list-specific priority-45 rule preserves Python's fresh
   slice allocation.
7. `subscript.k:63-114` reduces the slice to
   `buildVS(sortVS(VS), len(VS)-K, len(VS), 1)`. The only proof-local
   simplification, `verification.k:22`, supplies length preservation for the
   externally trusted sorting permutation.
8. The new slice occupies heap location 1 and returns as `ref(1)`;
   `functions.k` pops the frame without deallocating heap objects.

## Configuration, overlap, and totality review

- `core.k` supplies the complete cells used by the claims. All observable
  cells affected by the call are pinned: `<k>`, `<env>`, `<scopes>`,
  `<scopeLoc>`, `<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, and `<exc>`.
  `<exit-code>` is framed and remains unchanged because no used rule writes it.
- Call lookup and dispatch are not bypassed. The closure, builtin, argument,
  frame, return, sorting-allocation, dereference, slice, and allocation rules
  all execute.
- Relevant overlaps are resolved by the supplied priorities/`owise`: builtin
  `sorted` precedes generic builtin dispatch; reference dereference precedes
  generic subscript; list slicing's allocation rule precedes value-only
  slicing. No proof-local priority rule exists.
- On the positive-claim guard `0 < K <= vsLen(VS)`, the slice step is 1 and
  every `valSeqAt` index ranges from `vsLen(VS)-K` through
  `vsLen(VS)-1`. Thus the intentionally abstract total `valSeqAt` is never
  asked for an out-of-bounds intended-domain index.
- The compiler reports several supplied-semantics totality warnings. Only
  `valSeqAt` is on this proof path; its symbolic result is deliberately kept
  in both execution and postcondition. Float, `mapStrVS`, and `joinCodes`
  warnings are unreachable from this program.
- The formal positive claim is broader than the natural contract: it accepts
  arbitrary `ValSeq` elements, while the task specifies bounded integers. The
  result is sound on the intended integer domain; behavior of Python-invalid
  heterogeneous lists is not an intent claim.

## Proof-local extension decisions

| Extension | Class | Context/state footprint | Decision |
|---|---|---|---|
| `maximumBody` declaration and expansion (`verification.k:8-17`) | Exact program-body macro | Pure syntax expansion; no cells, continuation, binding, or result are replaced | Sound. It matches the translated body. A reviewer mutation of the body made the positive proof reach the wrong `ref(0)`/heap and fail with a genuine stuck claim. |
| `vsLen(sortVS(VS)) => vsLen(VS)` (`verification.k:22`) | Definitional lemma about a supplied trusted primitive | Rewrites only a mathematical length term; no operational cell or continuation | Sound conditional on the supplied contract that `sortVS` is a sorting permutation. It is not a K proof that `sortVS` implements Python sorting. |

There is no proof-local operational bridge, fresh oracle, result-return rewrite,
priority rule, helper function, `total` declaration, loop claim, or auxiliary
reachability claim.
