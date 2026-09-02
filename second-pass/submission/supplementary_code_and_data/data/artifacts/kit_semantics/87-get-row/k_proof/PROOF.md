VALIDATED

## What is proven

Under the supplied MPY semantics, for every finite unboxed list whose elements
are unboxed row lists and every integer `x`, the exact `get_row` body:

1. scans rows and columns from left to right;
2. appends exactly the coordinates whose element is K-equal to `x`;
3. applies the supplied opaque stable keyed-sort primitive first with key
   `-column` and then with key `row`; and
4. returns the reference allocated for the second sort.

For the prompt's integer domain, `value in (x,)` is equivalent to
`value == x`. Subject to the named `sortKeyVS` contract below, the two stable
sorts give ascending row order and descending column order within each row.

This is a partial-correctness result. Termination is not a theorem of the
reachability claims.

## Formal claim

`SPEC.get-row` starts from an exact module binding:

- `_column_desc` is bound to its exact function body;
- `_row_asc` is bound to its exact function body;
- `get_row` is bound to `GETROWBODY`, a macro expansion matching
  `solution.mpy`;
- the argument is `list(RS)` and `listRows(RS)` is required; and
- `x` has sort `Int`.

It proves return value `ref(2)`, final `heapLoc` 3, and these three allocations:

```text
0 |-> list(rowsAppend(.ValSeq, RS, X, 0))
1 |-> list(sortKeyVS(rowsAppend(.ValSeq, RS, X, 0), COLUMNCLOSURE))
2 |-> list(sortKeyVS(
              sortKeyVS(rowsAppend(.ValSeq, RS, X, 0), COLUMNCLOSURE),
              ROWCLOSURE))
```

The supporting claims are `SPEC.inner-loop`, `SPEC.outer-loop`,
`SPEC.column-key`, and `SPEC.row-key`.

## Proof-extension inventory

### Definitional summaries

| Extension | Domain and equations | Role, context, state, and justification | Dependents and validation |
|---|---|---|---|
| `rowContents(Val)` | Total: `list(VS) => VS`; every non-list value gives `.ValSeq` by the disjoint `owise` equation. | Pure value projection. It does not rewrite program execution or access cells. | `listRows`, the `For` bridge, `rowsAppend`; equation coverage and overlap audited. |
| `listRows(ValSeq)` | Total structural recursion: empty is true; a head `V` is accepted exactly when `V ==K list(rowContents(V))`, followed by the recursive tail check. | Formal input-shape predicate. It reads no operational state and affects only theorem applicability. | `SPEC.outer-loop`, `SPEC.get-row`; witnesses `.ValSeq` and `vCons(list(vCons(5,.ValSeq)),.ValSeq)` satisfy it. |
| `advanceIndex(Int, ValSeq)` | Total: empty returns the accumulator; a cons increments once and recurses on the tail. | Solver-friendly exact count of loop iterations. No execution is replaced. | Both loop claims; structurally descending and exhaustive. |
| `scanAppend(ValSeq, ValSeq, Int, Int, Int)` | Total: empty returns the accumulator. A cons either appends `(row,column)` or does not, under the disjoint guards `V ==K X` and `notBool (V ==K X)`, then recurses on the tail. | Exact mathematical name for the inner loop's heap value. The two recursive equations are also marked `[simplification]`; the attribute adds no equation beyond the guarded definitions. | Inner/outer/entry claims. Coverage is base plus cons, guards are complements, recursion descends, and the body mutation is rejected. |
| `rowsAppend(ValSeq, ValSeq, Int, Int)` | Empty returns the accumulator. A cons equation applies under `V ==K list(rowContents(V))`, scans that row, and recurses on the tail. It is intentionally partial outside `listRows`. | Exact mathematical name for the nested scan. Its `[simplification]` attribute repeats the same truthful guarded equation. No execution is replaced. | Outer/entry claims; the formal preconditions cover every use. |

`INNERBODY`, `OUTERBODY`, `GETROWBODY`, `COLUMNCLOSURE`, and `ROWCLOSURE`
are compile-time macros. They expand to source constructors and do not remain
as runtime rewrites.

### Operational bridge

The only proof-local execution rewrite is:

```k
rule <k> For(T:Expr, V:Val, B:Stmts)
      => #loop(list(rowContents(V)), T, B) ... </k>
     requires V ==K list(rowContents(V))
     [priority(40)]
```

- Class: operational bridge (one composed `For` setup step).
- Complete matched context: `For(T,V,B)` at the head of `<k>`, arbitrary
  continuation admitted by `...`, and every other configuration cell framed.
- Justification scope: `SHAPE-CONNECTION-SPEC.for-list-shape` has the same
  arbitrary target, body, continuation, and framed cells, with the same guard.
  Its definition imports `ROW-MODEL` and fixed `MPY`, not `VERIFICATION`, so it
  does not import the bridge.
- Context containment: the bridge domain is identical to the connection
  theorem domain.
- State footprint: reads only the `<k>` redex and the pure `rowContents`
  equation; writes only the redex. Environment, scopes, heap, allocator,
  stack, return, exception, exit code, and continuation are preserved.
- Binding/evaluation/control: `V` is already a value, as required by the fixed
  strict `For` rule. The target and body are unchanged, and no return,
  exception, loop control, or continuation is discarded.
- Value influence: none; the guard proves `V` and
  `list(rowContents(V))` are the same K value.
- Connection evidence:
  `kprove shape-connection-spec.k ...` prints `#Top` and exits 0.
- Sensitivity evidence: changing the destination to drop the sole element in
  `shape-connection-bad-spec.k` produces `WarnStuckClaimState` and exits 1.

### Auxiliary reachability claims

- `SPEC.inner-loop` is the inner-loop circularity. It executes the exact
  membership test, append call, and column increment. It updates only
  `column_index`, `value`, and the output heap object as stated.
- `SPEC.outer-loop` is the outer-loop circularity. It executes the exact row
  binding, resets, inner loop, and row increment. It depends on
  `SPEC.inner-loop`.
- `SPEC.column-key` executes the exact `_column_desc` binding/body and proves
  result `0 -Int CI`.
- `SPEC.row-key` executes the exact `_row_asc` binding/body and proves result
  `RI`.

All accept only contexts their claims state; no auxiliary claim is converted
into an ordinary execution rule.

## Exact commands and actual results

The authoritative command sequence is `./prove.sh`; its full captured output
is in `prove.log`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 -m py_compile solution.py smoke.py differential_test.py
python3 smoke.py
python3 differential_test.py
```

Actual differential output, exit 0:

```text
differential: 196923 exhaustive small cases + 2000 seeded larger cases; mismatches=0
```

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled > krun-smoke.out
```

Both commands exited 0. `krun-smoke.out` has final `<k> .K </k>`,
`<exc> NoExc </exc>`, and exit code 0 for the three prompt examples.

```bash
kompile --backend haskell shape-connection.k \
  --main-module SHAPE-CONNECTION \
  --syntax-module ROW-MODEL-SYNTAX \
  --output-definition shape-connection-kompiled
kprove shape-connection-spec.k \
  --definition shape-connection-kompiled \
  --spec-module SHAPE-CONNECTION-SPEC
```

Actual proof output: `#Top`; exit 0.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual target-proof output: `#Top`; exit 0. This single command proves all five
claims in `SPEC`.

The compiler emitted only warnings originating from the supplied semantics
(unused `As`/`Bs` variables and LLVM non-exhaustive-match warnings), not errors.

### Negative probes

Each command below exited 1 with `WarnStuckClaimState`; `prove.sh` recognized
each as an expected failure and itself exited 0.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

The residual returns `ref(2)`, rejecting the false requested `ref(99)`.

```bash
kprove spec-body-mutation.k \
  --definition mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

The mutated body suppresses coordinate appends. On `[[5]], 5`, its residual
heap contains an empty scanned list, rejecting the required `[(0,0)]`.

```bash
kprove shape-connection-bad-spec.k \
  --definition shape-connection-kompiled \
  --spec-module SHAPE-CONNECTION-BAD-SPEC
```

The false bridge mutation drops the value `7`; the residual visibly proceeds
to bind and execute that element, so the mutation is rejected.

## Gate results

### Gate A — PASS

- A1: the exact `get_row` and key bodies are present in the invocation
  configuration. Program-defined loop code executes. Both key functions have
  bridge-free exact execution claims. The append-suppression mutation fails.
- A2: the sole operational bridge preserves every non-`<k>` cell and the
  continuation; the target claim explicitly checks allocations, heap contents,
  return value, frame restoration, exception state, and exit code.
- A3: the bridge applies only after the iterable is a value, preserves target,
  body, and continuation, and has a bridge-free theorem over its complete
  context. The incorrect-result mutation fails.
- A4: all total equations have exhaustive, disjoint cases; recursive equations
  descend; partial `rowsAppend` is guarded by `listRows` at every use.
- A5: `RS = .ValSeq, X = 1` is a realizable witness. The wrong-return mutation
  is rejected with actual result `ref(2)`.

### Gate B — PASS

- B1: the prompt domain (finite ragged lists of integers and integer `x`) is
  included. The formal representation uses the supplied semantics' supported
  unboxed read-only list values; inputs are not mutated. Inner elements are
  actually allowed to be arbitrary `Val`, which is broader than the prompt.
- B2: K `Int` and CPython integers are both unbounded in the relevant sense.
  The theorem excludes malformed non-list rows, exceptions outside the
  supplied subset, alias-sensitive inputs, and termination.
- B3: `rowsAppend` is formally connected to the executed scan. The final
  ordering interpretation is conditional on the named stable `sortKeyVS`
  contract and is independently tested.
- B4: the implementation matches the prompt examples and the independent
  oracle over every tested case.

### Gate C — PASS

Every proof-local extension and unproved boundary is listed here. All cited
artifacts exist, exact commands are in `prove.sh`, actual outputs are retained
in `prove.log`/`krun-smoke.out`, and mutation and differential scopes are
stated. Finite evidence is reported only as evidence, not as a universal proof
of sorting.

## Trust boundary

The value-affecting external boundary is the supplied
`sortKeyVS(ValSeq, Val)` primitive in
`reference-semantics/semantics/sort.k`. Symbolic MPY intentionally leaves it
opaque; `MPY-CONCRETE` executes stable key calls and insertion sorting for
LLVM. `SPEC.get-row` depends on it only by returning the raw nested
`sortKeyVS` term. Interpreting that term as correctly stable-sorted is
conditional on the supplied contract.

`sortKeyVS` affects the returned list value and order, but not the proved scan,
allocation count, frame/control behavior, or the independently proved key
values. The K toolchain and the supplied reference semantics are also trusted
as the fixed verification base.

## Empirically supported facts

- `differential_test.py` uses an independent descending-index oracle. It checks
  all 196,923 matrices with 0–3 rows, row lengths 0–3, values and targets in
  `{-1,0,1}`, plus 2,000 seeded matrices with up to 10 rows, row lengths up to
  12, and values/targets in `[-20,20]`. Mismatches: 0.
- Native CPython executes the three prompt examples successfully.
- LLVM MPY executes the same three examples through the real concrete keyed
  sorter and reaches `.K`, `NoExc`, exit code 0.
- The body, false-return, and bridge-result mutations all fail as intended.

These finite results support implementation intent and the concrete sorter;
they do not prove the opaque sorter universally.

## Excluded behavior

- Termination/liveness is not proved.
- Inputs with a non-list row or a non-integer target are outside the prompt
  theorem.
- Heap aliases, mutation of input rows during iteration, Python exceptions
  outside the supplied subset, and behaviors absent from the reference
  semantics are excluded.
- The universal stable-sorting property of `sortKeyVS` is trusted, not proved
  in K here.

The runner result is `KPROVE_PASSED` because every required positive proof
command printed `#Top` and exited 0. That execution marker is reported
separately from this `VALIDATED` proof-quality headline.
