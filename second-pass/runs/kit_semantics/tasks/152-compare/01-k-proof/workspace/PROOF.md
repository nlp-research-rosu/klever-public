VALIDATED

## What is proven

Under the supplied `MPY` semantics, the implementation in `solution.py` is
partially correct for two equal-length lists of integer match scores. If the
call terminates, it returns a freshly allocated list whose element at every
position is the absolute difference between the score and the prediction at
that position.

The theorem includes loading the exact translated function, resolving and
calling `compare`, binding both parameters, allocating the result list,
executing tuple unpacking and the `for` loop, resolving the builtin `abs`,
dispatching `list.append`, returning through the function frame, and restoring
the caller environment. The final claims also require an empty stack,
`noRet`, `NoExc`, and exit code `0`.

This is partial correctness. The reachability proof does not separately prove
termination.

## Formal claim

`spec.k` partitions the stated equal-length integer domain into exhaustive
structural cases:

- `compare-entry-empty` proves `compare([], [])` returns the fresh empty list.
- `compare-entry-step` proves every nonempty pair of equal-length integer lists.
  The current heads satisfy the generated `isInt` predicate and the remaining
  tails satisfy the recursive `sameIntLists` predicate.
- `compare-loop-step` is the loop circularity. Starting with output prefix
  `PREFIX` at heap location `0`, it executes the remaining zipped pairs and
  leaves `compareAcc(PREFIX, scores, predictions)` at the same location.

For integers, the fixed reference rules reduce
`applyBuiltin("abs", applyBin("-", SCORE, PREDICTED), .Vals)` to
`absInt(SCORE -Int PREDICTED)`. Thus `compareAcc` is the elementwise absolute
difference sequence, accumulated in source execution order.

The additional `not isRefV` conjuncts in the formal domain make explicit facts
already true of K integers and integer subtraction results. They prevent the
symbolic backend from considering impossible aliases with the output heap
reference; they exclude no concrete integer input.

## Proof-extension inventory

There are no proof-local operational bridges, priority rewrites,
simplification axioms, trusted primitives, or opaque result oracles.

### `sameIntLists` and its three equations

- **Class:** Definitional summary.
- **Semantic role:** Defines the formal input domain; it does not replace
  execution.
- **Domain:** Every pair of `ValSeq` terms. The first equation covers a left
  empty sequence, the second covers left nonempty/right empty, and the third
  covers two nonempty sequences.
- **Matched context:** Only the function term `sameIntLists(A, B)`; no
  continuation, binding, or state cell is matched.
- **Justification scope and containment:** Constructor coverage is exhaustive
  and disjoint. The recursive case descends on both tails. `isInt` is the
  generated sort predicate; `isRefV` and `applyBin` are supplied semantic
  symbols. Every use is within this complete definition.
- **State footprint:** None.
- **Value influence:** It restricts the loop and nonempty entry claims to
  equal-length integer lists and excludes impossible reference-alias branches.
- **Value justification:** Direct structural definition. Empty/nonempty
  mismatches are false; paired heads are integers and the tails recursively
  satisfy the same property.
- **Dependents:** `compare-loop-step` and `compare-entry-step`.
- **Control/value validation:** Concrete witnesses include the empty input and
  both prompt examples. The false-result and body-mutation probes below are
  rejected.

### `compareAcc` and its two equations

- **Class:** Definitional summary.
- **Semantic role:** Names the list value produced by the loop; it appears in
  post-state heap patterns and never rewrites a program computation.
- **Domain:** Equal-shape paired sequences used under `sameIntLists`. The base
  equation handles two empty tails. The step equation consumes one pair and
  appends the exact supplied-semantics term for `abs(score - predicted)`.
- **Matched context:** Only `compareAcc(ACC, SCORES, PREDICTIONS)`; no
  continuation, binding, or state cell is matched.
- **Justification scope and containment:** The equations are disjoint and
  recursive descent removes one element from both input tails. Mismatched
  shapes are intentionally outside its uses.
- **State footprint:** None.
- **Value influence:** Determines the list stored at output heap location `0`.
- **Value justification:** Its recurrence is exactly the fixed semantics'
  in-place `append` recurrence. It reuses `valSeqConcat`, `applyBin`, and
  `applyBuiltin` from the reference semantics rather than introducing an
  arithmetic oracle.
- **Dependents:** All three positive claims.
- **Control/value validation:** The full proof closes; the LLVM prompt tests
  and the independent differential test have zero mismatches; deliberate
  false output and body mutation are rejected.

### `compare-loop-step`

- **Class:** Derived reachability lemma/circularity.
- **Semantic role:** Reasons about fixed execution; it is not installed as an
  operational rewrite.
- **Domain:** A nonempty zipped pair followed by tails satisfying
  `sameIntLists`, with the current pair satisfying the explicit integer and
  non-alias constraints. The module scope must not shadow `abs`.
- **Matched context:** The exact source loop body at `#loop`, an arbitrary
  framed continuation preserved by `<k> ... => .K ... </k>`, environment `1`,
  builtins at `-1`, module scope at `0`, the exact function locals at `1`,
  output list at heap location `0`, and heap location counter `1`.
- **Justification scope and containment:** The machine-checked circularity has
  the same complete context it later supplies to `compare-entry-step`. No
  broader continuation, scope chain, binding, heap, or control effect is
  admitted.
- **State footprint:** Reads `score`, `predicted`, `result`, the module/builtin
  scope chain, and heap location `0`; updates `score`, `predicted`, and the
  list at location `0`; preserves `game`, `guess`, the result reference,
  module/builtin scopes, heap location counter, continuation, stack, return
  state, exception state, and exit code.
- **Value influence:** Supplies the remaining suffix of the returned list.
- **Value justification:** Fixed semantics executes tuple binding, subtraction,
  builtin lookup/call, bound-method lookup/call, and `append`; `compareAcc`
  matches the resulting heap recurrence exactly.
- **Dependents:** `compare-entry-step`.
- **Control validation:** The claim itself prints `#Top`; it preserves the
  framed continuation. There is no operational bridge requiring a
  fixed-versus-extended comparison.
- **Value validation:** Ground prompt examples pass under LLVM. Mutating the
  loop body to append `abs(...) + 1` produces `[4]` instead of `[3]` for
  `[5]` and `[2]`, and the original-result connection claim is rejected.

The two entry claims are theorem targets, not execution shortcuts. They contain
the same AST as `solution.mpy` and execute the program-defined body under the
fixed semantics.

## Exact commands and actual outputs

The reproducible driver is:

```bash
./prove.sh > prove.log 2>&1
```

Actual exit: `0`.

Its positive build and proof commands are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_test.py > concrete_test.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_test.mpy --definition runtime-kompiled
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual relevant output:

```text
<k>
  .K
</k>
...
<exc>
  NoExc
</exc>
<exit-code>
  0
</exit-code>
#Top
```

The full-spec `kprove` command exited `0`; its single `#Top` covers every claim
in `SPEC`. Compiler warnings in `prove.log` originate in the supplied
read-only reference semantics and do not change the exit status.

The A5 false-result command is:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual exit: `1`. The residual has result `ref(0)` and heap
`0 |-> list(.ValSeq)`, which cannot match the deliberately false required
`0 |-> list(vCons(1, .ValSeq))`. `prove.sh` records:

```text
EXPECTED_FAILURE: false-result mutation was rejected
```

The body-sensitivity command is:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual exit: `1`. The residual heap contains
`0 |-> list(vCons(4, .ValSeq))`, not the original required singleton `[3]`.
`prove.sh` records:

```text
EXPECTED_FAILURE: body mutation was rejected
```

The independent differential command is:

```bash
python3 differential_test.py
```

Actual output and exit:

```text
DIFFERENTIAL_TESTS_PASS=120100
```

Exit `0`. The complete combined output is preserved in `prove.log`.

## Gate results

### Gate A — PASS

- **A1:** Both entry claims load, bind, and execute the exact translated
  program body. The material `+1` body mutation invalidates the original-result
  connection and exits `1`.
- **A2:** No operational bridge skips state. The loop claim explicitly tracks
  the output heap mutation and preserves the remaining operational cells.
- **A3:** Function, builtin, and method lookup execute under fixed semantics.
  The invariant pins the actual scope chain and rules out module shadowing of
  `abs`; it preserves the arbitrary continuation.
- **A4:** `sameIntLists` is total with disjoint exhaustive cases.
  `compareAcc` is intentionally partial but covers every use under the formal
  domain; its recursion strictly descends. There are no overlapping or false
  proof-local equations.
- **A5:** The empty input is a realizable witness. The false `[1]`
  post-state is rejected with a stuck residual showing the actual empty list.
  The nonempty domain is realizable, for example heads `5` and `2` with empty
  tails.

### Gate B — PASS

- **Input domain:** Equal-length lists of integer match scores. This follows
  the match-score context and every prompt example. Unequal lengths and
  non-integer elements are explicitly excluded rather than silently modeled.
- **Language model:** K integers are unbounded, matching CPython integer
  arithmetic for subtraction and absolute value. Inputs are read-only bare
  list values, an intentional facility documented by the supplied semantics;
  aliasing is unobservable because the function never mutates either input.
- **Property adequacy:** `compareAcc` uses the supplied operator terms and,
  for K integers, reduces to the requested absolute difference at every
  position.
- **Implementation alignment:** The implementation returns exactly this list
  for the empty case and for every nonempty formal input.

### Gate C — PASS

- Every proof-local equation and claim is inventoried above.
- `prove.sh`, `prove.log`, `concrete_test.py`, `spec-vacuity.k`,
  `spec-body-mutation.k`, and `differential_test.py` exist and record the
  commands, scopes, oracles, outputs, and exit behavior cited here.
- Formal proof, expected-failure mutation evidence, and finite empirical
  evidence are labeled separately.

## Trust boundary

The theorem trusts the supplied read-only `reference-semantics/` definition,
including its implementations of integer subtraction, integer absolute value,
`zip`, tuple binding, function calls, name lookup, list allocation, and
`append`; it also trusts the K parser/compiler, Haskell backend, SMT solving,
and reachability-logic implementation. `py2mpy.py` is trusted to translate the
Python AST faithfully, and its output is preserved as `solution.mpy`.

There is no proof-local trusted primitive or operational bridge. The CPython
oracle and LLVM runs are evidence, not axioms used by `kprove`.

## Empirically supported facts

- `concrete_test.py` runs the two prompt examples and the empty boundary under
  the required LLVM `MPY-KRUN` semantics. The final state is `.K`, `NoExc`,
  exit code `0`.
- `differential_test.py` uses an independently written indexed loop, manual
  sign correction, and no proof equations. It exhaustively checks every pair
  of equal-length sequences for lengths `0` through `3` and values `-3`
  through `3`: `120100` cases and zero mismatches.
- The two negative K artifacts independently demonstrate result sensitivity
  and source-body sensitivity.

These finite checks support implementation and model adequacy; they are not
used as universal proof.

## Excluded behavior

The formal claims exclude unequal-length lists, non-integer elements (including
floats and booleans), exceptions outside the modeled domain, input mutation,
concurrency, external state, resource exhaustion, and CPython behaviors absent
from the supplied subset semantics. They do not assert total correctness or a
runtime bound.
