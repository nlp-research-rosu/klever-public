VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, `solution.py` is partially
correct for every finite list whose elements are `Float` values.

The target claim starts by loading the exact translated module shape
(`ImportFrom("typing", "List")` followed by the target `FuncDef`), resolves
`mean_absolute_deviation` through the module scope, binds the `numbers`
argument, executes the function body, and returns:

- `0.0` for the empty list; and
- for a nonempty list `VS`,
  `divFloatIntV(deviationFloatVS(VS, MEAN, 0.0), vsLen(VS))`, where
  `MEAN` is
  `divFloatIntV(sumFloatVS(VS, 0.0), vsLen(VS))`.

`sumFloatVS` is the left fold using the supplied `addF`.
`deviationFloatVS` is the left fold using the supplied
`addF(_, absF(subF(_, MEAN)))`. Thus the returned term is the direct
structural encoding of the prompt's
`average(abs(x - average(numbers)))`.

This is a partial-correctness reachability theorem. It does not separately
claim a liveness theorem, although both loop claims structurally consume a
finite `ValSeq`.

## Formal claim

The required target is `SPEC.mean-absolute-deviation` in `spec.k`.
Its precondition is:

```k
requires allFloatVS(VS)
```

The domain predicate has exhaustive constructor equations:

```k
allFloatVS(.ValSeq) = true
allFloatVS(vCons(V, R)) = isFloat(V) andBool allFloatVS(R)
```

Therefore the claim covers arbitrary finite lengths, including zero; it is not
a bounded unrolling or a collection of fixed-size examples. The two supporting
claims `SPEC.sum-loop` and `SPEC.deviation-loop` are universal circularities
over an arbitrary remaining suffix `VS`.

The observed final state includes the returned `<k>` value, module scope,
environment, heap, allocation counters, call stack, return state, exception
state, and exit code. The loop-local variable `number` is existentially framed
only in the loop lemmas because it is overwritten before any later read and is
not observable at function return.

## Proof-extension inventory

There are no proof-local trusted primitives and no operational bridge rules.
Program-defined code is not intercepted. The following extensions contribute
to closure.

### `madBody`

- Class: definitional summary (syntax macro).
- Semantic role: names the exact `Stmts` tree emitted in `solution.mpy`; macro
  expansion leaves no runtime summary symbol.
- Domain and matched context: every syntactic occurrence of `madBody`.
- Justification scope and context containment: textual constructor-for-
  constructor match with the translated function body.
- State footprint and value influence: none by the macro itself; the expanded
  fixed semantics reads and writes the normal function cells.
- Dependents: all three positive claims.
- Validation: `spec-body-mutation.k` changes the empty return from `0.0` to
  `1.0`; `kprove` exits 1 with `WarnStuckClaimState` and a residual return
  value of `1.0` against expected `0.0`.

### `allFloatVS`

- Class: definitional summary.
- Semantic role: names the input-domain predicate; it does not replace
  execution.
- Domain: all `ValSeq` terms. The empty and cons equations are exhaustive and
  disjoint, and recursion descends to the tail.
- Matched context/state footprint: a pure function term; no configuration
  cells.
- Value influence: restricts the theorem to the signature's `List[float]`
  domain and guards dynamic-to-static projection.
- Dependents: both loop claims and the entry claim.
- Validation: the universal claims close on symbolic `VS`; LLVM and
  differential tests include empty, singleton, and multiple nonempty sizes.

### `projectFloat`, its `#Ceil` characterization, orientation rules, and collapse

- Class: derived lemmas implementing the guarded total-projection idiom.
- Semantic role: refines a dynamic `Val` known by `isFloat` to the existing
  `Float` subsort. It does not manufacture a float value.
- Domain: the orientation rules require `isFloat(V)`; the collapse rule is
  `projectFloat(F:Float) => F`. Outside that guard the total symbol has no
  evaluator and remains uninterpreted.
- Matched context: pure projection/cast terms; no continuation, binding, or
  cells are matched.
- Justification scope and containment: the `#Ceil` equation characterizes the
  partial cast's definedness by the exact generated sort predicate. Every
  proof use is under `allFloatVS`, which entails the head guard.
- State footprint: none.
- Value influence: supplies the exact list element to `addF` and `subF`.
- Dependents: the two dispatch twins, folds, loop claims, and entry claim.
- Value validation: on every actual `Float`, the collapse equation fixes the
  projection to that same value. Concrete float witnesses in `smoke.py` and
  `test_solution.py` exercise distinct positive, negative, small, and large
  values; no opposite value is admitted by the collapse equation.

### Guarded `applyBin` dispatch twins

The exact rules are:

```k
applyBin("+", A:Float, V:Val)
  => addF(A, projectFloat(V)) requires isFloat(V)
applyBin("-", V:Val, M:Float)
  => subF(projectFloat(V), M) requires isFloat(V)
```

- Class: derived lemmas.
- Semantic role: restate the supplied `MPY-FLOAT` equations over a dynamic
  supersort after guarded projection. They do not alter `<k>`, control, scopes,
  heap, stack, exceptions, or output.
- Domain and matched context: only pure `applyBin` terms under the exact
  `isFloat` guard.
- Justification and containment: on the overlap where `V` is statically a
  `Float`, `projectFloat(V)` collapses to `V`, so both twins have exactly the
  supplied typed rule's right-hand side. No wider unguarded case exists.
- Value influence: addition builds both accumulators; subtraction feeds
  `absF`, so both influence the final result.
- Dependents: `sum-loop`, `deviation-loop`, and the entry claim.
- Validation: each universal loop claim closes by fixed-semantics execution of
  one head step and circular application on the tail. The 267-case
  differential run reports zero mismatches.

### `sumFloatVS`, `deviationFloatVS`, and `madResult`

- Class: definitional summaries.
- Semantic role: name mathematical values without rewriting an operational
  program term.
- Domain: both folds have exhaustive, disjoint empty/cons equations and descend
  to the tail. `madResult` has disjoint `vsLen(VS) ==Int 0` and
  `vsLen(VS) =/=Int 0` guards, exhaustive for an integer length.
- Matched context/state footprint: pure function terms; no configuration
  cells.
- Value influence: these symbols state the exact returned value.
- Justification: their equations mirror, in order, the two accumulator
  assignments and the two divisions in the expanded body.
- Dependents: loop postconditions and the target postcondition.
- Validation: the loop claims prove the execution-to-fold connection.
  `spec-vacuity.k` replaces the realizable empty result `0.0` with `1.0` and is
  rejected.

### `SPEC.sum-loop` and `SPEC.deviation-loop`

- Class: derived reachability lemmas (loop circularities).
- Semantic role: universally characterize fixed-semantics execution of each
  `#loop`; they are not ordinary rewrite rules.
- Domain: arbitrary finite remaining `VS` with `allFloatVS(VS)`, arbitrary
  accumulator and preserved caller cells.
- Matched context: each claim quantifies over the complete trailing `<k>`
  continuation, fixes `env` to the real callee frame, fixes module and builtin
  bindings, gives the exact callee-scope keys, and explicitly carries
  `scopeLoc`, heap, `heapLoc`, stack, return, exception, and exit-code cells.
- Justification scope and containment: the claim itself has the same universal
  framed continuation and cells as every use in the entry proof. Its base and
  step cases execute only supplied semantics; the recursive tail is discharged
  coinductively by the same claim.
- State footprint: each loop reads `numbers`, its accumulator, and (for the
  second loop) `mean`; it writes the accumulator and `number`; all other listed
  cells are preserved. No exceptions or abrupt control are introduced.
- Value influence: `sum-loop` determines `mean`; `deviation-loop` determines
  the numerator of the return.
- Dependents: the entry claim.
- Control/value validation: each claim independently printed `#Top`, and the
  full-spec command printed `#Top` while using both claims. No operational
  bridge exists whose context is broader than these proved configurations.

## Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`. The final
end-to-end run was:

```text
./prove.sh
Exit: 0
```

Key commands and actual results from that run:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
```

Output: none. Exit: 0 for both.

```bash
kompile reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit: 0. The actual compiler warnings are preserved in `llvm-build.out`; they
are pre-existing non-exhaustive/unused-variable warnings in the supplied
semantics.

```bash
krun smoke.mpy --definition runtime-kompiled
```

Exit: 0. `krun-smoke.out` ends with `<k> .K </k>`, `<stack> .List </stack>`,
`<ret> noRet </ret>`, `<exc> NoExc </exc>`, and exit code `0`. The program
contains assertions for `[]`, `[1.0]`, and the prompt example
`[1.0, 2.0, 3.0, 4.0]`.

```bash
kompile verification.k \
  --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual positive proof output:

```text
#Top
```

Both commands exited 0. The complete outputs are in `haskell-build.out` and
`kprove-positive.out`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual `<k>` value is
`0.0` while the destination requires `1.0`. Full output: `vacuity.out`.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`; the mutated residual `<k>`
value is `1.0` while the destination requires `0.0`. Full output:
`body-mutation.out`.

```bash
python3 test_solution.py
```

Actual output and exit:

```text
differential-cases=267 mismatches=0
Exit: 0
```

## Gate results

### Gate A — PASS

- A1: the target begins at the full module load, pins the real function
  binding, and executes the exact translated body. The body mutation is
  rejected.
- A2: there are no operational bridges. The universal loop claims explicitly
  preserve or characterize every active configuration cell.
- A3: module lookup, builtin lookup, argument evaluation, parameter binding,
  loop control, return, and frame popping all execute under fixed semantics.
  Guarded projection preserves the selected float value.
- A4: local function equations are disjoint/exhaustive over their stated
  domains, descend structurally, and agree with the supplied typed equations on
  every overlap.
- A5: `[]` is a realizable witness. The false postcondition probe exits 1 with
  a stuck residual, so the target constrains the returned value.

### Gate B — PASS

- B1: the formal domain is every finite `List[float]`, with no size bound. The
  implementation defines the prompt-silent empty case as `0.0`; nonempty lists
  satisfy the stated MAD formula.
- B2: collection order, length, name lookup, control, and state follow the
  supplied Python subset. Symbolic IEEE-754 arithmetic is intentionally opaque
  in that reference semantics and is named as a conditional trust boundary
  below.
- B3: the folds formally characterize execution. Their interpretation as MAD
  is the direct source-level formula, conditional only on the supplied float
  primitives implementing Python float operations.
- B4: the implementation and prompt agree for all nonempty typed inputs, and
  the additional empty behavior is explicit rather than hidden by a stronger
  precondition.

### Gate C — PASS

Every unproved component is listed below with its influence and dependents.
All cited test and mutation artifacts exist, exact commands are in `prove.sh`,
and their full outputs are retained. Formal, conditional, empirical, and
excluded conclusions are separated in this report.

## Trust boundary

The fixed inputs `py2mpy.py` and `reference-semantics/` are supplied by the
task and are outside the theorem.

The following fixed `MPY-FLOAT` symbols are intentionally opaque to `kprove`:

| Symbol | Effect | Dependents | Evidence |
|---|---|---|---|
| `addF` | Returned float value | both folds and target | LLVM smoke; 267-case differential |
| `subF` | Deviation value | deviation fold and target | LLVM smoke; differential |
| `absF` | Deviation magnitude | deviation fold and target | LLVM smoke; differential |
| `divFloatIntV` | Mean and final average | `madResult` and target | LLVM smoke; differential |

These primitives affect values but not binding, control, heap, exceptions, or
output in this program. The formal result is the exact term built from them;
the claim that those terms equal CPython numerical operations is conditional on
the supplied primitive contracts.

No proof-local symbol is trusted as an external primitive.

## Empirically supported facts

- `smoke.py` is translated by the fixed translator and executed by the LLVM
  backend. Its three assertions cover the empty boundary, singleton boundary,
  and prompt example.
- `test_solution.py` uses `math.fsum` as an independently implemented oracle.
  It checks 267 deterministic cases: seven named boundary/representative cases
  plus 20 seeded random lists for every length from 0 through 12. The observed
  mismatch count is zero.
- These finite tests support the concrete float boundary and intent alignment;
  they are not used as a universal proof.

## Excluded behavior

- Inputs containing non-float elements are outside the annotated
  `List[float]` domain.
- Lists or values outside the supplied MPY representation are outside the
  theorem.
- The report does not prove total correctness or independent correctness of
  the supplied translator, fixed semantics, K backend, or opaque float hooks.
- It does not assert a mathematical MAD value for the empty dataset beyond the
  implementation's explicit `0.0` convention.
