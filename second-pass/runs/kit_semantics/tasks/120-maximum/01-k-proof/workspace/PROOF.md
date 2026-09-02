VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact module term generated from
`solution.py` is loaded, binds `maximum`, and the call
`maximum(list(VS), K)` symbolically executes to a returned heap reference whose
pointee is:

```k
maximumResult(VS, K)
```

for every `VS:ValSeq` and `K:Int` satisfying:

```k
1 <=Int vsLen(VS)
andBool vsLen(VS) <=Int 1000
andBool 0 <=Int K
andBool K <=Int vsLen(VS)
```

The intermediate sorted list is also present in the final heap, all call-frame
state is restored, no exception is raised, and the exit code remains zero. This
is a partial-correctness theorem: it does not prove termination.

For the prompt's integer-list domain, the HumanEval conclusion follows
conditionally on the supplied semantics' named `sortVS` contract: `sortVS(VS)`
is the ascending permutation of `VS`. The suffix beginning at
`len(arr) - k` is therefore a sorted list containing the greatest `k` elements,
with multiplicity. The symbolic proof is interpretation-parametric in
`sortVS`; the ascending-permutation contract is an explicit trust boundary, not
a theorem proved in this K development.

## Formal claim

The only positive target claim is `SPEC.maximum-correct` in `spec.k`. Its left
side begins with:

```k
#loadAll(Module(FuncDef("maximum", Params("arr", "k"), ...)))
~> Call(Name("maximum"), list(VS), K)
```

The embedded `Module(...)` is the exact whitespace-normalized content of
`solution.mpy`. The right side requires:

```k
<k> ref(1) </k>
<heap>
  0 |-> list(sortVS(VS))
  1 |-> maximumResult(VS, K)
</heap>
<heapLoc> 2 </heapLoc>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The formal theorem is slightly broader than the prompt because `VS` is any
`ValSeq`; it does not encode the element type or `[-1000, 1000]` bound. The
prompt's integer domain is a subset of the proved execution domain. The
human-facing “greatest integers” interpretation is asserted only on that
intended subset.

## Proof-extension inventory

### `maximumResult`

- **Extension:** `syntax Val ::= maximumResult(ValSeq, Int) [function, total]`
  and its single unconditional equation in `verification.k`.
- **Class:** Definitional summary.
- **Semantic role:** Names the returned value after fixed-semantics execution;
  it does not match or replace a source term or operational configuration.
- **Domain:** Every `VS:ValSeq` and `K:Int`.
- **Matched context:** Only the pure term `maximumResult(VS, K)`. It accepts no
  continuation, stack, binding, or framed state cell.
- **Justification scope:** All arguments in its declared domain.
- **Context containment:** Exact, because the equation has no operational
  context and the justification covers its whole unguarded domain.
- **State footprint:** Reads and writes no cells and abstracts no state.
- **Value influence:** Names the value stored at final heap location `1`, hence
  the returned reference's pointee.
- **Value justification:** Its sole equation expands to
  `doSlice(list(sortVS(VS)), someB(vsLen(VS) -Int K), noB, noB)`, exactly the
  value produced after fixed semantics evaluates `sorted(arr)`,
  `len(arr) - k`, and the slice.
- **Justification:** Direct definitional expansion following the supplied
  `sorted`, `len`, subtraction, slice, and allocation rules.
- **Dependents:** `SPEC.maximum-correct` and the correct postcondition retained
  by `SPEC-BODY-MUTATION`.
- **Control validation:** Not applicable; it is not an operational bridge.
- **Value validation:** The positive proof closes; the ground false-result
  mutation is rejected with actual returned list `[2]`; 61 independent
  differential cases and the concrete boundary tests agree.
- **Validation:** The equation is unconditional, nonrecursive, exhaustive, has
  no competing equation, and terminates after one expansion.

There are no proof-local derived lemmas, simplification rules, operational
bridges, priorities, or opaque result oracles. The reachability claim is the
target theorem, not an assumed auxiliary circularity.

## Exact commands and actual outputs

All reproducible commands are in `prove.sh`. The final complete run was:

```bash
./prove.sh
```

It exited `0`. Its significant output was:

```text
IDENTITY_CHECK_PASSED: exact whitespace-normalized solution.mpy term found in spec.k
#Top
EXPECTED_FAILURE: false-result mutation was rejected
EXPECTED_FAILURE: body mutation was rejected
DIFFERENTIAL_PASSED: 61 cases; CPython mismatches=0; K exit=0
```

The individual commands and observed results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 identity_check.py
```

Output and exit:

```text
IDENTITY_CHECK_PASSED: exact whitespace-normalized solution.mpy term found in spec.k
Exit: 0
```

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Output and exit: exit `0`; the compiler reported supplied-semantics warnings
about non-exhaustive `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`, plus unused `As`/`Bs` variables in `str.k`.

```bash
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled --output none
python3 py2mpy.py boundary-test.py > boundary-test.mpy
krun boundary-test.mpy --definition runtime-kompiled --output none
```

Output and exit: both `krun` commands produced no output under `--output none`
and exited `0`. An earlier pretty-output run of `concrete-tests.mpy` ended with
`.K`, `NoExc`, and `<exit-code> 0 </exit-code>`.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Output and exit:

```text
#Top
Exit: 0
```

The Haskell build and proof also repeat the supplied `str.k` unused-variable
warnings; they do not affect the exit status.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1` with `WarnStuckClaimState`. For the realizable witness
`arr = [1, 2]`, `k = 1`, the residual heap contains:

```text
1 |-> list ( vCons ( 2 , .ValSeq ) )
```

which cannot unify with the deliberately false empty-list destination.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1` with `WarnStuckClaimState`. Mutating the lower bound to
`len(arr) - k - 1` makes the witness return `[1, 2]`, which cannot unify with
the correct `[2]` destination.

```bash
python3 differential_test.py
```

Output and exit:

```text
DIFFERENTIAL_PASSED: 61 cases; CPython mismatches=0; K exit=0
Exit: 0
```

## Gate results

### Gate A — PASS

- **A1 program identity/body sensitivity:** `spec.k` executes `#loadAll` on
  the exact translated module. `identity_check.py` confirms exact
  whitespace-normalized inclusion. The independent body mutation is rejected
  and exposes the changed `[1, 2]` result.
- **A2 operational state:** No proof-local operational bridge exists. The
  target observes the returned reference, both allocated heap objects,
  `heapLoc`, restored environment and scope allocator, empty stack, return
  state, exception state, and exit code.
- **A3 binding/evaluation/control:** The initial module scope is empty,
  `#loadAll` creates the `maximum` closure, `Name("maximum")` selects that exact
  binding, arguments evaluate under the fixed call rules, and the exact body
  returns through the fixed frame/pop rules.
- **A4 logical consistency:** `maximumResult` has one unconditional,
  exhaustive, non-overlapping, nonrecursive equation. No false or broadened
  proof rewrite was added.
- **A5 non-vacuity:** `VS = [1, 2]`, `K = 1` satisfies the precondition. The
  false empty-result mutation exits `1` with the concrete unmet result `[2]`.

### Gate B — PASS

- The formal length and `k` bounds match the prompt. The theorem is broader in
  element sort/range, so it does not silently strengthen or exclude any prompt
  input.
- On the intended integer subset, K `Int`, list slicing, multiplicities, and
  the bounds used here align with Python behavior. No exception is expected in
  the stated domain.
- `maximumResult` is formally connected to execution. Its interpretation as
  the sorted greatest `k` integers is conditional on the named
  ascending-permutation contract for `sortVS`, and is empirically supported
  rather than claimed as a new K theorem.
- All prompt examples and boundary behavior agree with the implementation.

### Gate C — PASS

- The trust ledger below names every material unproved boundary and its
  dependents.
- All claimed identity, concrete, differential, false-result, and body-mutation
  evidence has a checked-in artifact, exact command, scope, oracle, and actual
  result.
- Formal, conditional, empirical, and excluded conclusions are separated in
  this report.

## Trust boundary

### Supplied `sortVS`

- **Exact component:** `sortVS(ValSeq)` and the `sorted(list)` allocation rule
  in `reference-semantics/semantics/sort.k`.
- **Why outside the theorem:** The supplied symbolic semantics intentionally
  leaves sorting opaque and declares it a trusted primitive.
- **Influence:** Its value determines the intermediate sorted heap object and
  the final sliced list; it therefore affects the observable return value and
  heap, but does not bypass the program-defined function body or its call/return
  control.
- **Dependents:** `maximumResult` and `SPEC.maximum-correct`.
- **Assumption:** On lists of integers, `sortVS(VS)` is an ascending
  permutation of `VS`.
- **Evidence:** The LLVM semantics implements concrete insertion sort.
  `concrete-tests.py`, `boundary-test.py`, and `differential_test.py` all pass.
  This finite evidence does not prove the universal sort contract.

### Base trust

The K implementation, the supplied read-only `MPY` semantics, and
`py2mpy.py` are trusted infrastructure required by the task. The exact
translator output is preserved as `solution.mpy`, and `identity_check.py`
checks that the proof embeds that output. No file under `reference-semantics/`
and neither supplied Python input was modified.

## Empirically supported facts

- `concrete-tests.py` checks all three prompt examples, `k = 0`, singleton,
  duplicates, and element bounds `-1000`/`1000` under the LLVM semantics.
- `boundary-test.py` compactly constructs a 1,000-element list, calls
  `maximum(arr, 1000)`, and checks the input/output lengths and endpoint
  values. It exits `0` under LLVM.
- `differential_test.py` uses the independent oracle
  `sorted(heapq.nlargest(k, arr))`, seed `20260725`, all prompt examples,
  `k = 0`, `k = len(arr)`, duplicates, element bounds, 48 generated lists of
  lengths 1 through 12, and one length-50 list at five `k` values. All 61
  CPython comparisons match; the exact `solution.py` body with the same
  assertions exits `0` under LLVM.
- The ground false-result and body-mutation probes both fail for the intended
  semantic reason, not a parser or compilation error.

These are finite validation results, not replacements for the symbolic target
proof or a universal proof of sorting.

## Excluded behavior

- Termination and complexity are not proved.
- The human-facing maximum claim is not made for non-integer elements,
  out-of-range elements, invalid lengths, or `k` outside `0..len(arr)`.
- Python behaviors absent from the supplied subset, resource exhaustion, and
  implementation-specific CPython internals are outside the theorem.
- The universal ascending-permutation property of `sortVS` is not proved here;
  conclusions requiring that meaning remain conditional on the named trusted
  primitive contract.
