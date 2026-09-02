VALIDATED

# Proof report

## What is proven

Under the supplied `MPY` semantics, the exact `how_many_times` closure in
`solution.mpy` has the following partial-correctness property:

> For every semantic string `str(S)` and substring `str(P)`, if the call
> terminates, its result is `overlapCount(S, P)`.

`overlapCount` tests the pattern at every successive suffix, so matches may
overlap.  The empty pattern has `isLen(S) + 1` matches, one at every boundary.
The theorem covers arbitrary `IntSeq` values, not only the concrete ASCII
literals accepted by the supplied literal loader.

The theorem executes the pinned closure body, name lookup, argument binding,
conditionals, `len`, `startswith`, slicing, assignments, loop control, return,
and frame pop through the supplied semantics.  The observable result is
constrained by the `ensures` clause.  The entry configuration also fixes the
global binding, builtins scope, environment, heap, stack, return state,
exception state, and exit code.

This is partial correctness.  `kprove` does not establish termination, although
the source loop removes one code point from a nonempty string on each iteration.

## Formal claims and validation scope

- Program boundary: the exact closure invocation in `SPEC.target`, including
  the body transliterated in `solution.mpy`.
- Input domain: two values of the semantic string form `str(IntSeq)`.  Python
  calls with non-string values are outside the theorem.
- Observable final state: the returned integer.  The entry claim also preserves
  all explicitly listed nonlocal operational cells.
- Intended property: the number of starting positions at which `substring`
  equals a contiguous part of `string`, with overlapping starts counted.
- `SPEC.loop-inv`: for a nonempty pattern, starting with remaining suffix `S`
  and count `C`, the exact loop terminates with an empty suffix and count
  `C + overlapCount(S, P)`.
- `SPEC.target`: the exact function call returns `overlapCount(S, P)`.

The loop obligations are:

1. Base: an empty remaining suffix exits immediately and
   `overlapCount(.IntSeq, P) = 0` for nonempty `P`.
2. Step: the real `startswith` result contributes either zero or one; the real
   `[1:]` operation yields the next suffix; the circularity applies there.
3. Entry: the empty-pattern branch returns `isLen(S) + 1`; otherwise the
   initialized count `0` instantiates the loop claim.

## Proof-extension inventory

### `tailIS`

- Class: definitional summary.
- Semantic role: names the algebraic tail of an `IntSeq`; it does not replace
  program execution.
- Domain: all `IntSeq` values.  The `.IntSeq` and `iCons` equations are
  disjoint, exhaustive, and structurally terminating.
- Matched context and justification scope: a pure `tailIS(S)` term in any
  context; its two equations cover the complete free-algebra domain.
- State footprint: none.
- Value influence: the recursive argument of `overlapCount` and the right side
  of the slice lemma.
- Value justification: constructor equations
  `tailIS(.IntSeq) = .IntSeq` and
  `tailIS(iCons(_, CS)) = CS`.
- Dependents: `overlapCount`, the slice lemma, `SPEC.loop-inv`, and
  `SPEC.target`.
- Validation: equation overlap/coverage audit and the slice evidence below.

### `overlapCount`

- Class: definitional summary.
- Semantic role: defines the requested mathematical result; it does not
  intercept a Python call or K-cell transition.
- Domain: all pairs of `IntSeq`.
- Cases: empty pattern; empty source with nonempty pattern; nonempty source and
  nonempty pattern.
- Coverage and overlap: the three guards are exhaustive and pairwise disjoint.
- Descent: the recursive case uses `tailIS(S)` under `S =/= .IntSeq`, reducing
  source length by one.
- Matched context and justification scope: a pure
  `overlapCount(S, P)` term in any context, over the complete stated domain.
- State footprint: none.
- Value influence: the loop post-state and final result.
- Value justification: one contribution for `startsWith(P, S)`, then the count
  over the next suffix; the empty-pattern case counts all `n + 1` boundaries.
- Dependents: both claims.
- Validation: formal loop proof, the prompt examples, and 1,905 exhaustive
  differential cases against an independently written position/slice oracle.

### `buildIS(... [1:] ...) => tailIS(S)` simplification

- Class: derived lemma.
- Semantic role: normalizes the pure value returned by the supplied slice
  helper.  It does not rewrite the `<k>` cell, skip lookup, alter control, or
  abstract state.
- Complete domain: every nonempty `S:IntSeq`; the exact left side is
  `buildIS(S, clampHi(1, isLen(S), 1), isLen(S), 1)`.
- Matched context: any term context.  Because this is equality of a pure total
  function, its justification is context-independent and covers every
  continuation and configuration in which the term can occur.
- State footprint: none read, written, preserved, or abstracted.
- Value influence: the next loop suffix, and therefore later branches and the
  returned count.
- Value justification: let `n = isLen(S) >= 1`.  `clampHi(1, n, 1)` is `1`
  (also when `n = 1`).  `buildIS` selects exactly indices `1` through `n - 1`;
  by induction on `n - 1`, that sequence is precisely `tailIS(S)`.
- Equation consistency: where the lemma overlaps the supplied `buildIS`
  equations, both sides select the same sequence.  Its nonempty guard excludes
  the only value without a tail.
- Dependents: `SPEC.loop-inv`, hence `SPEC.target`.
- Control validation: fixed LLVM execution and extended proof execution agree
  on the prompt witnesses; no control-bearing rule is introduced.
- Value validation: 9,840 finite sequences of lengths 1 through 8 over
  `{0,1,2}` produced zero differences between an independent executable
  `buildIS`-shape evaluator and Python tail slicing.

A bridge-free standalone symbolic attempt using only `MPY` was also made:

```bash
kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition lemma-kompiled
kprove slice-lemma-spec.k --definition lemma-kompiled \
  --spec-module SLICE-LEMMA-SPEC
```

The build exited 0, but the proof exited 1 with a residual symbolic `buildIS`;
the backend could not derive the necessary structural length facts.  This is
not a counterexample.  The extension is classified as a derived pure
equational lemma, not an operational bridge, and its complete-domain
derivation is given above.

### `SPEC.loop-inv`

- Class: derived auxiliary reachability claim used coinductively.
- Semantic role: summarizes the exact loop only after its fixed-semantics base
  and one-step obligations have been checked.
- Domain: nonempty `P`, arbitrary remaining suffix `S`, integer count `C`,
  environment `L`, parent `PAR`, outer scopes, continuation, and framed cells.
- Matched context: the exact `#while` guard and body, with the arbitrary
  continuation represented by the `<k>` frame.  The proof itself is equally
  general over that frame.
- State footprint: updates only local `"string"` and `"count"`; preserves
  `"substring"`, environment selection, outer scopes, and every framed cell.
- Control: the exact while guard, branch, assignments, and loop label execute.
  There is no return, break, exception, or frame pop in the summarized body.
- Value influence: supplies the count returned by `SPEC.target`.
- Justification and validation: `kprove` prints `#Top` for the focused claim and
  again when all claims are proved together.

There are no opaque result oracles, trusted primitives, priority rules, or
program-call interception rules in `verification.k`.

## Reproducible commands and actual outputs

Tool version:

```text
K version: v7.1.293
```

The complete final workflow is `./prove.sh`, which exited 0.  Its substantive
commands and outputs were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
```

Both commands exited 0.  The final module scope contained:

```text
"example_empty" |-> 0
"example_single" |-> 3
"example_overlap" |-> 3
"empty_substring" |-> 4
```

```bash
python3 validate.py
```

Output and exit:

```text
CASES=1905
MISMATCHES=0
SLICE_CASES=9840
SLICE_MISMATCHES=0
Exit: 0
```

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-inv
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The build exited 0.  Both positive proof commands printed:

```text
#Top
Exit: 0
```

The supplied semantics emitted only compiler warnings about unrelated
nonexhaustive helpers and unused variables.

False-result mutation:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result:

```text
WarnStuckClaimState
<k> 3 ~> .K </k>
Exit: 1 (expected)
```

Body-sensitivity mutation (`count` initialized to `1`):

```bash
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result:

```text
WarnStuckClaimState
<k> 4 ~> .K </k>
Exit: 1 (expected)
```

The complete outputs are preserved in `concrete-output.txt`,
`differential-output.txt`, `loop-proof-output.txt`,
`target-proof-output.txt`, `vacuity-output.txt`, and
`body-mutation-output.txt`.

## Gate results

### Gate A — PASS

- A1: the target pins the exact function binding and body.  All
  program-defined code executes.  Initializing `count` to `1` changes the
  concrete symbolic result from `3` to `4`, and the original target is rejected.
- A2: there is no operational state bridge.  The only value lemma is pure and
  has no cell footprint.
- A3: the supplied semantics performs name lookup, left-to-right argument
  evaluation, parameter binding, loop control, return, and frame restoration.
  The entry scope selects the intended closure.  The slice equality is
  context-independent and introduces no abrupt control.
- A4: `tailIS` and `overlapCount` have exhaustive, disjoint, terminating
  equations.  The guarded slice lemma is true on its complete domain and
  agrees with the supplied equations on overlap.
- A5: `("aaaa", "aa")` is a realizable witness.  The real result is `3`; the
  claim demanding `4` exits 1 with residual `3`.

### Gate B — PASS

- The formal domain matches the two `str` parameters in the prompt.
- The recursive summary counts every starting suffix and therefore counts
  overlapping matches.
- The three stated examples match concrete execution.
- Empty substring behavior is made explicit as `len(string) + 1`, the number
  of string boundaries.
- K integers are unbounded, matching Python integer results for this task.
- The supplied model represents strings as integer code sequences.  Its
  concrete literal loader is ASCII-only, but the symbolic theorem is over
  arbitrary code sequences and uses only code-point equality, prefix, length,
  and slicing.

### Gate C — PASS

- Every proof-local function, equation, simplification, and auxiliary claim is
  inventoried above.
- Exact commands, artifacts, input scopes, outputs, and exit codes are
  preserved.
- Finite tests are reported only as evidence; universal closure is attributed
  to `kprove` plus the audited theory.
- Formal facts, manually derived equational facts, empirical evidence, and
  excluded behavior are separated.

## Trust boundary

- The supplied read-only `reference-semantics/` definition is trusted as the
  intended Python subset.
- `py2mpy.py` is trusted for CPython-AST-to-constructor transliteration; the
  generated `solution.mpy` was regenerated by `prove.sh` and its body matches
  the closure pinned in `SPEC.target`.
- K v7.1.293, the Haskell backend, LLVM backend, and their solver/runtime are
  trusted.
- K accepts proof-local equations as theory.  The only nontrivial such equality
  is the complete-domain slice lemma, whose derivation and finite differential
  evidence are recorded above.
- No external primitive or opaque value affects the returned result.

## Empirically supported facts

- The four concrete K executions agree with the prompt examples and the
  documented empty-pattern boundary.
- `solution.py` agrees with the independent slice-position oracle on all 1,905
  pairs over alphabet `{a,b}` with source length at most 6 and pattern length
  at most 3.
- The slice lemma agrees with its executable oracle on 9,840 nonempty code
  sequences over `{0,1,2}` of lengths 1 through 8.
- These finite checks support, but do not replace, the formal proof and the
  mathematical derivation.

## Excluded behavior

- Termination is not a conclusion of the reachability proof.
- Calls with non-string arguments, Python exception behavior outside the typed
  contract, resource usage, and performance are not proved.
- Full CPython behavior outside the supplied semantics is not claimed.
- Concrete non-ASCII literal loading is not exercised by the supplied
  ASCII-only literal rule, although the symbolic theorem itself accepts
  arbitrary `IntSeq` strings.
