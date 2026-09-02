VALIDATED

## What is proven

Under the supplied MPY semantics, `max_fill` is partially correct for every
finite grid whose rows are finite lists of Python integers `0` and `1`, and for
every positive integer `capacity`. Starting from the normal module binding for
the exact translated function body, ordinary lookup, argument evaluation,
parameter binding, loop execution, `sum`, return, and frame popping produce
`gridCost(GS, C)`.

This domain strictly contains the HumanEval domain: the prompt's nonempty
rectangular grids of sizes 1 through 100 and capacities 1 through 10 are all
included. The theorem also permits empty or ragged finite grids, longer grids,
and capacities greater than 10; proving a safe superset does not exclude any
prompt-valid input.

For a row containing `n` water units and positive capacity `c`,
`bucketCost` is the exact MPY integer-floor result of
`(n + c - 1) // c`. This equals `ceil(n / c)`: writing
`n = qc + r`, with `0 <= r < c`, gives `q` when `r = 0` and `q + 1`
otherwise. Summing this quantity over the rows is exactly the number of bucket
lowerings required by the prompt.

The result is a partial-correctness theorem in the Kit sense. It does not make
a separate liveness claim.

## Formal claims

`spec.k` contains three claims, proved together:

- `sum-loop`: the fixed `#sumAcc` fold over any finite binary `ValSeq`
  produces `A + rowSum(VS)`.
- `grid-loop`: the exact translated `for` body transforms the running total by
  `gridCost(GS, C)` while preserving the exact local/module/builtins scope
  chain and recording the final loop target.
- `max-fill`: lookup selects the exact closure body from `solution.mpy`;
  MPY-CALL binds `grid` and `capacity`; the body executes; return/pop restores
  the initial caller configuration and leaves `gridCost(GS, C)` in `<k>`.

The target precondition is:

```k
C >Int 0 andBool allRows(GS)
```

`allRows` recursively requires each element to be exactly
`list(rowVals(V))`; `allBinary` recursively requires each row element to be an
integer whose exact projection is either `0` or `1`.

## Proof-extension inventory

| Extension | Class | Semantic role and complete domain | Justification and dependents |
|---|---|---|---|
| `definedProjectInt`, `projectInt`, and their cast/collapse rules | Definitional summary / derived projection lemmas | Exact projection from `Val` to `Int`; the cast orientations fire only when `isInt(V)`. No configuration cell is read or changed. | The `#Ceil` characterization, guarded partial-cast orientations, and `projectInt(I:Int) => I` fix the value. Used by `allBinary` and the guarded `intOf` twin. The wrong value `projectInt(1) == 0` is rejected. |
| `rowVals` and `isListVal` | Definitional summary | `rowVals(list(VS)) = VS`; off-list projection values are opaque, but every value-affecting use is guarded by `isListVal(V)`, defined as the exact equality `V ==K list(rowVals(V))`. No state is accessed. | Constructor equality pins the unique row sequence. Used by `allRows`, `gridCost`, and the `sum` dispatch twin. The opposite ground projection is rejected. |
| `allBinary`, `allRows` | Definitional summaries | Total structural predicates over all `ValSeq` values; base/step equations are disjoint and structurally descending. | They state, rather than assume, the target input domain. Used by all three positive claims. |
| `rowSum`, `bucketCost`, `gridCost`, `finalRow` | Definitional summaries | Total, structurally recursive mathematical summaries. `bucketCost` splits on the exhaustive disjoint guards `C > 0` and `C <= 0`; only the positive branch is used by the target. They do not rewrite program control. | Their equations mirror `#sumAcc`, MPY-INT's exact `//` equation, the outer fold, and Python's retained `for` target. Used by the loop claims and final postcondition. |
| `intOf(V) => projectInt(V)` under `isInt(V)` | Derived static-dispatch lemma | Simplifies a result-bearing fixed function value but changes no cell or continuation. Domain is exactly the `Int` subsort selected by the guard. | `connection-spec.k` proves the bridge-free fixed equation `intOf(I:Int) => I`; the total projection connects a guarded `V` to that exact `I`. Used by `sum-loop`. |
| Guarded `sum` `#applyK` rule | Operational bridge / guarded dispatch twin | Exact match: `#applyK(toCall(builtinV("sum")), (V, .Vals)) ~> KREST`, under `isListVal(V)`. It preserves arbitrary `KREST`; reads/writes no environment, scope, heap, stack, return, exception, or exit cell; introduces no abrupt control. | `isListVal(V)` is definitionally `V ==K list(rowVals(V))`. Instantiating bridge-free `fixed-sum-dispatch` with `VS = rowVals(V)` gives the identical RHS. Used by `grid-loop` after normal callee and argument evaluation. |
| `sum-loop`, `grid-loop` | Derived auxiliary reachability claims | Coinductive circularities over the exact fixed fold and exact translated program loop. Their contexts and scope cells are stated in the claims. | Both are machine-checked with the target. They execute the fixed semantics; neither replaces a program-defined body. |

### Operational-bridge record

- Matched context: the `sum` twin matches only the already-evaluated
  `#applyK(toCall(builtinV("sum")), (V, .Vals))` redex and frames the complete
  arbitrary continuation with `...`.
- Justification scope: `fixed-sum-dispatch` in `connection-spec.k` universally
  proves the supplied MPY-CALL step for `list(VS)` without importing
  `MAX-FILL-VERIFICATION`. The guard equates every matched `V` with exactly
  `list(rowVals(V))`, so the bridge domain is contained in that theorem.
- State footprint: only the leading `<k>` redex changes. All other cells and
  the continuation are preserved. The bridge performs no lookup, argument
  evaluation, allocation, mutation, return, exception, or control transfer.
- Value influence: the resulting `#sumAcc` value affects the returned total.
  Value fidelity follows from the connection theorem plus the separately
  proved `sum-loop`; it is not an unconstrained oracle.
- Control validation: fixed LLVM execution and bridge-enabled Haskell
  execution both consume all three example programs to `.K`, with identical
  final cells and exit code 0.
- Value validation: the prompt examples agree in both executions; wrong
  integer and row projections are rejected with exit 1.

## Exact commands and observed results

The complete reproducible command sequence is executable as:

```sh
./prove.sh > prove.log 2>&1
```

Observed result: exit 0. The exact individual commands and expected-failure
handling are recorded in `prove.sh`.

The required target build and proof were:

```sh
kompile --backend haskell verification.k \
  --main-module MAX-FILL-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC
```

Observed: `#Top`, exit 0. This single invocation proves all three claims
together, so the auxiliary circularities are available to the claims that
depend on them.

The bridge-free connection build and proof were:

```sh
kompile --backend haskell verification.k \
  --main-module MAX-FILL-SUMMARY \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module MAX-FILL-CONNECTION-SPEC
```

Observed: `#Top`, exit 0. `MAX-FILL-SUMMARY` does not import either dispatch
twin from `MAX-FILL-VERIFICATION`.

Concrete fixed-semantics execution used the required LLVM modules:

```sh
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Observed: `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code 0 for the three
prompt examples. `krun smoke.mpy --definition verification-kompiled` produced
the same complete final configuration with the dispatch twins enabled.

The independent differential command:

```sh
python3 differential_test.py
```

observed:

```text
cases=20466 mismatches=0
```

The oracle simulates bucket lowering with a `while water > 0` loop; it does not
reuse the proof's floor-division equation. The tested scope is every binary
grid through 3 by 4 for capacities 1 through 4, three 100 by 100 boundary
cases, and 250 seeded cases over the prompt's full stated bounds.

Four negative probes were run by `prove.sh`:

- `spec-vacuity.k`: original body on `[[1]], 1`, mutated expected result `2`.
  Exit 1; residual result was `1`.
- `spec-body-mutation.k`: `total = 0` changed to `total = 1` on the empty-grid
  witness while retaining the original expected result `0`. Exit 1; residual
  result was `1`.
- `projection-mutation-spec.k`, `wrong-int`: demanded
  `projectInt(1) == 0`. Exit 1 with a bottom RHS/stuck implication.
- `projection-mutation-spec.k`, `wrong-row`: demanded
  `rowVals([1]) == []`. Exit 1 with a bottom RHS/stuck implication.

The complete actual output, including the two `#Top` lines and all four
expected-failure residuals, is preserved in `prove.log`. Compiler warnings in
the log originate in the supplied reference semantics (unused variables and
LLVM exhaustiveness warnings); all relevant compile commands exit 0.

## Gate results

### Gate A — PASS

- A1: `max-fill` uses normal name lookup and an exact closure body identical to
  `solution.mpy`; no program-defined operation is summarized away. Regeneration
  with `python3 py2mpy.py solution.py` is part of `prove.sh`. The body mutation
  is rejected.
- A2/A3: the only operational twin is connected to the exact fixed
  `#applyK` rule, after lookup and argument evaluation. Its arbitrary
  continuation and every omitted state cell are preserved.
- A4: recursive equations have disjoint constructor cases and descend;
  `bucketCost` guards are disjoint and exhaustive; guarded projections are
  value-pinned on every use that can affect the result.
- A5: `[[1]], capacity=1` is a realizable witness. The correct result is 1,
  and the false result 2 is rejected.

### Gate B — PASS

The symbolic theorem covers arbitrary finite binary grids and every positive
capacity, not finitely many sizes. Thus it covers the prompt's entire bounded
rectangular domain. The reference semantics explicitly permits unboxed
`list(ValSeq)` values as read-only claim inputs; `max_fill` does not mutate or
observe list identity. The formal aggregate is the bucket-lowering quantity
specified by the prompt, and there is no implementation/specification
discrepancy.

### Gate C — PASS

All build, proof, concrete, differential, connection, and mutation artifacts
exist in this directory and are run by `prove.sh`. Evidence scope, oracle,
commands, outputs, and expected nonzero exits are recorded above and in
`prove.log`.

## Trust boundary and excluded behavior

Trusted components are the supplied read-only MPY semantics, K v7.1.293 and
its Haskell/LLVM backends, the backend's integer/Boolean theories, and the
underlying solver. There is no additional trusted result-bearing primitive in
`verification.k`; the two opaque total projections are connected to exact
casts or constructor equalities before their values can affect a result.

Inputs with non-list rows, elements other than integer `0` or `1`, or
nonpositive capacities are outside the HumanEval contract and outside the
positive target claim. The `bucketCost` nonpositive branch only totalizes a
proof function; no target theorem depends on it. Python features absent from
the supplied MPY subset and observable aliasing/mutation behavior are also not
claimed.
