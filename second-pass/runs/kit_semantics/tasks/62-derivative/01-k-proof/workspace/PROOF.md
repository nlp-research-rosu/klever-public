VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, the exact translated body in
`solution.mpy` is partially correct for every arbitrary finite, self-contained
modeled input list. The function returns a fresh list whose elements are the
original coefficients after the constant coefficient, each multiplied by its
original zero-based index:

```text
[x0, x1, x2, ...]  ↦  [applyBin("*", 1, x1),
                         applyBin("*", 2, x2), ...]
```

For integer coefficients, the fixed `applyBin` equations reduce those terms to
ordinary K integer multiplication. Supported float multiplication remains at
the supplied semantics' explicitly opaque float boundary during proof and is
executed concretely by the LLVM backend.

This is a partial-correctness theorem. K reachability does not separately prove
termination, although the source loop consumes one finite `ValSeq` constructor
per iteration.

## Formal claim and scope

Program boundary:

- `derivative-entry` loads the exact `FuncDef` AST from `solution.mpy`, resolves
  `derivative` through the module scope, calls it, and executes its body,
  including allocation, iteration, lookup, `append`, return, and frame pop.
- `derivative-loop` begins at the fixed semantics' actual
  `#loop(list(VS), Name("x"), BODY)` control point and proves the loop's
  arbitrary-length circularity.

The definitional summary is:

```text
derivAcc(A, [], i)                 = A
derivAcc(A, v :: r, i), i <= 0    = derivAcc(A, r, i + 1)
derivAcc(A, v :: r, i), i > 0     =
  derivAcc(A ++ [applyBin("*", i, v)], r, i + 1)
```

The entry claim starts with `A = .ValSeq` and `i = 0`. Its precondition
`noRefsVS(INPUT)` excludes heap handles from a configuration whose initial heap
is empty. This is a representation well-formedness condition: all
self-contained `Val` constructors, including inline modeled collections, are
admitted. It places no bound on list length, integer magnitude, or coefficient
constructor.

The observable post-state is `ref(0)` in `<k>` and
`0 |-> list(derivAcc(.ValSeq, INPUT, 0))` in `<heap>`, with `heapLoc = 1`,
the caller environment restored, an empty call stack, `noRet`, `NoExc`, and
exit code 0. The final module-scope map is existential because the prompt
observes only the return value and function-local scopes are deallocated.

## Proof-extension inventory

### `derivAcc`

- **Class:** Definitional summary.
- **Semantic role:** Reasons about the result; it never matches or replaces a
  program control term.
- **Domain:** All `ValSeq` accumulators and remainders and all `Int` indices.
  Empty/cons patterns are disjoint. On cons inputs, `notBool (I >Int 0)` and
  `I >Int 0` are disjoint and exhaustive.
- **Matched context:** Any mathematical `derivAcc(ACC, VS, I)` term. It matches
  no `<k>` term, continuation, binding, frame, or operational cell.
- **Justification scope and containment:** Its equations are exactly the
  source loop's empty, skipped-constant, and append steps. Every rewrite
  strictly shortens `VS`; its match domain is identical to that recursive
  definition.
- **State footprint:** None.
- **Value influence:** Defines the list asserted in the loop and entry
  postconditions.
- **Value justification:** It uses the fixed semantics' own
  `applyBin("*", I, V)`, rather than a fresh multiplication oracle. The
  `derivative-loop` reachability claim machine-checks the connection from the
  executed loop body to this value.
- **Dependents:** `derivative-loop` and `derivative-entry`.
- **Control validation:** Not applicable; no execution is replaced.
- **Value validation:** The target proof closed; the `[1,2,3] -> [2,7]`
  mutation was rejected with actual heap `[2,6]`; LLVM and Python evidence are
  recorded below.
- **Validation:** Guard overlap, coverage, and structural descent pass Gate A4.

### `noRefsVS`

- **Class:** Definitional summary/predicate.
- **Semantic role:** States input representation well-formedness; it replaces
  no execution.
- **Domain:** All `ValSeq`; empty and cons cases are disjoint and exhaustive.
- **Matched context:** Predicate terms only, with no operational context.
- **Justification scope and containment:** The cons equation uses the supplied
  total `isRefV`; recursion strictly shortens the sequence.
- **State footprint:** None.
- **Value influence:** It affects only claim applicability, not the returned
  value or a program branch.
- **Value justification:** Direct exhaustive definition.
- **Dependents:** Both positive claims.
- **Control/value validation:** The LLVM witnesses use realizable reference-free
  inputs; the predicate adds no control or value rule.
- **Validation:** Totality and equation overlap pass Gate A4.

### `derivative-loop`

- **Class:** Derived reachability lemma (coinductive loop circularity).
- **Semantic role:** Executes the real `#loop`, branch, multiplication,
  `append`, and index update. Once proved, it summarizes that same exact loop
  for `derivative-entry`; it is not an ordinary rewrite rule.
- **Domain:** `I >=Int 0`, `noRefsVS(VS)`, the exact four local bindings
  (`xs`, `result`, `i`, `x`), a heap list at `H`, and arbitrary finite `VS`.
- **Matched context:** The exact loop body and target `Name("x")`, under an
  arbitrary framed continuation (`...`), fixed function environment 1,
  arbitrary preserved outer scopes, arbitrary preserved non-result heap,
  arbitrary `heapLoc` and stack, `noRet`, `NoExc`, and exit code 0.
- **Justification scope and containment:** The claim itself quantifies over
  precisely that arbitrary continuation and framed state, so its later use in
  the entry claim lies inside its proved domain.
- **State footprint:** Reads `i`, `x`, `result`, `xs`, and heap entry `H`;
  changes local `i` and `x` and the list stored at `H`; preserves the
  `result`/`xs` bindings, outer scopes, other heap entries, heap location,
  stack, return state, exception state, and exit code. Final `i` and `x` are
  existential because they are function-local and unobserved.
- **Value influence:** Establishes the complete result list.
- **Value justification:** Its base and both guard branches close using the
  exhaustive `derivAcc` equations and fixed semantics execution.
- **Dependents:** `derivative-entry`.
- **Control validation:** The exact continuation is quantified rather than
  discarded. A mutated final return is rejected and leaves the distinct
  observable `ref(1)`/empty-list state.
- **Value validation:** The false postcondition is rejected and exposes the
  actual `[2,6]` heap.
- **Validation:** The claim prints `#Top` as part of the full target proof.

There are no proof-local operational bridges, priority rules, opaque fresh
result symbols, or rules intercepting the function call or body.

## Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`. The final run:

```bash
./prove.sh
```

exited 0. Its material component results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
# Exit 0

python3 test_solution.py
# differential cases: 4912; mismatches: 0
# Exit 0

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# Exit 0 (supplied-semantics warnings only)

krun smoke.mpy --definition runtime-kompiled
# Exit 0; final <k> is .K, <exc> is NoExc, and <exit-code> is 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# Exit 0 (supplied-semantics unused-variable warnings only)

kprove spec.k --definition verification-kompiled --spec-module SPEC
# #Top
# Exit 0

kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# WarnStuckClaimState; actual heap is [2,6], not [2,7]
# Exit 1 (expected)

kprove spec-body-mutant.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTANT
# WarnStuckClaimState; actual result is ref(1) to a fresh empty list
# Exit 1 (expected)
```

The exact outputs are preserved in `python-differential.out`,
`krun-smoke.out`, `target-proof.out`, `vacuity-proof.out`, and
`body-mutant-proof.out`. The tools reported K version `v7.1.293`.

## Gate results

### Gate A — PASS

- **A1:** The entry claim contains and executes the exact translated function
  body. No function-call or body shortcut exists. Replacing the final return
  with a fresh empty-list return makes the proof fail and exposes the changed
  return reference and heap.
- **A2:** There is no operational bridge. The loop theorem accounts for the
  result heap update and preserves or explicitly abstracts every framed cell.
- **A3:** Lookup, callee/argument evaluation, binding, append, loop control,
  return, and frame pop all execute under fixed semantics. The loop claim is
  quantified over every continuation it accepts.
- **A4:** Both helper definitions are exhaustive on their declared use domain,
  have disjoint cases, and structurally descend. No inconsistent or
  execution-bypassing rule is present.
- **A5:** Empty and `[1,2,3]` are realizable witnesses. The false
  `[1,2,3] -> [2,7]` postcondition exits 1 and shows `[2,6]`.

### Gate B — PASS

- **B1:** The circularity covers arbitrary finite input length, not fixed sizes
  or bounded unrollings. The formal input admits every self-contained value
  constructor in the supplied model rather than silently restricting the
  prompt's unparameterized `list` to integer examples.
- **B2:** The theorem covers all such modeled values. CPython object kinds and
  operator behaviors absent from the fixed semantics are recorded below as a
  model boundary, not excluded by an extra candidate length/type bound.
- **B3:** `derivAcc` states the requested coefficient/index multiplication
  position by position. The loop claim formally connects actual execution to
  that summary. Integer values are fully reduced; supplied opaque float values
  are conditional on their named fixed-semantics primitives.
- **B4:** The implementation matches both prompt examples and the independent
  executable oracle.

### Gate C — PASS

Every non-proved boundary is named in the trust ledger, all cited evidence
artifacts exist with exact commands and outcomes, and finite evidence is not
presented as a universal proof.

## Trust boundary

| Component | Why outside this theorem | Influence and dependents | Evidence |
|---|---|---|---|
| Supplied `reference-semantics/` and K backend | Fixed by the task and imported read-only | Defines all control, state, integer operations, and therefore both claims | LLVM smoke run; Haskell `#Top`; K v7.1.293 |
| `intToF` and `mulF` in supplied `MPY-FLOAT` | Intentionally opaque under `kprove`, concrete under LLVM | Determines float result values in `applyBin`; both positive claims depend on it for floats | Float LLVM assertion and Python differential cases |
| Uncovered fixed-semantics `applyBin("*", Int, Val)` cases | The supplied subset has no CPython operator rules for every modeled nonnumeric constructor | Such result terms are structurally threaded into `derivAcc`; no concrete CPython value or exception is claimed for them | No value claim is made; this is an explicit model boundary |
| Termination | Reachability proves partial correctness | Does not affect the proved postcondition on terminating executions | Source/semantic loop consumes one sequence constructor per iteration; not a K liveness theorem |

## Empirically supported facts

- `test_solution.py` uses an independently written enumerate/comprehension
  oracle. It checks all lists of lengths 0 through 5 over `[-2,2]`, 1,000
  deterministic random integer lists up to length 25, both prompt examples,
  boundary examples, negative coefficients, and a float example: 4,912 cases,
  zero mismatches.
- `smoke.mpy` executes the same function body under the required LLVM
  `MPY-KRUN` definition. Six assertions cover empty, singleton, both prompt
  examples, negatives/zero, and floats; execution ends with `NoExc` and exit
  code 0.
- These finite checks support implementation/model alignment. The universal
  arbitrary-length fact comes from the `#Top` reachability proof, not testing.

## Excluded behavior

- The proof does not establish total correctness or a termination theorem.
- A raw `ref` inside `INPUT` is excluded because the entry configuration's
  heap is empty, so it would be a dangling operational handle rather than a
  self-contained input value. Inline modeled collections remain admitted.
- CPython object kinds, user-defined `__mul__`/`__rmul__`, aliasing, exception
  behavior, and sequence-repetition behavior not modeled by the supplied
  semantics are not claimed. For such cases, the theorem is only the
  structural statement containing the fixed `applyBin` term.
- Function-local final `i`/`x` values and the final module-scope representation
  are unobserved by the HumanEval return-value contract.
