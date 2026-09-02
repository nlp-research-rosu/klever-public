VALIDATED

## What is proven

For every arbitrary finite `ValSeq` whose elements are K `Int` values, loading
the translated `next_smallest` definition and calling it under the supplied MPY
semantics returns:

- `noneV` when the input has fewer than two distinct integers; and
- the least integer strictly greater than the input minimum otherwise.

This is the second-smallest distinct element required by the HumanEval prompt.
The theorem has no list-length or integer-magnitude bound. As prescribed by the
Kit, this is a partial-correctness reachability proof. The loop consumes one
`ValSeq` constructor per iteration, but termination is not a separate liveness
claim.

## Formal claim and invariant

`SPEC.next-smallest` starts with the default module/builtins state and the exact
computation
`#loadAll(solutionProgram) ~> Call(Name("next_smallest"), ...)`. The fixed
semantics performs module loading, name lookup, argument evaluation, frame
creation, parameter binding, every statement, return, and frame teardown. Its
RHS is `nextSmallestSpec(VS)` under `allInts(VS)`.

`SPEC.loop-invariant` is the unbounded circularity. `scanVS` folds the remaining
sequence into `(smallest, found-smallest, second, found-second)`. Starting with
`scanState(0, false, 0, false)`, its inductive meaning is:

- `found-smallest` is false exactly for an empty processed prefix; otherwise
  `smallest` is that prefix's minimum;
- `found-second` is false exactly when the prefix has at most one distinct
  value; otherwise `second` is the least value strictly greater than
  `smallest`.

The `scanStep` cases preserve this statement: a new lower value shifts the old
minimum to second; an equal value changes nothing; a greater value initializes
or lowers second when appropriate. Thus `nextSmallestSpec` is a direct
inductive formalization of the natural-language property, not merely the
prompt's finite examples.

## Proof-extension inventory

There are no operational bridges and no new trusted primitives.

### `nextSmallestLoopBody`, `nextSmallestBody`, `solutionProgram`

- Class: definitional summaries (constructor aliases).
- Semantic role: name exact syntax; after expansion, all execution is by MPY.
- Domain and matched context: unconditional, constructor-valued functions only.
- Justification scope/context containment: each RHS is the corresponding
  constructor sequence in `solution.mpy`; `solutionProgram` expands to the
  entire translated module.
- State footprint: none. The aliases neither read nor write configuration
  cells.
- Value/control influence: they select the body executed by the target claim.
- Dependents: both claims.
- Validation: `solution.mpy` was regenerated from `solution.py`; the target
  starts at module load, LLVM executes the same translated program, and the
  always-`None` body mutation is rejected.

### `allInts`, `definedProjectInt`, `projectIntTotal`, and projection equations

- Class: definitional domain predicate plus derived sort-refinement lemmas.
- Semantic role: reason about dynamic `Val` heads known to be integers; they do
  not skip a K computation.
- Domain: every `ValSeq` for `allInts`; projection orientation/collapse is used
  only when `isInt(V)` holds. Outside that guard `projectIntTotal` has no
  evaluator and cannot manufacture an integer.
- Matched/justification context: pure terms only, with no continuation or cells.
  The guarded projection equals the built-in partial cast `{V}:>Int`; the
  `#Ceil` rule characterizes that same definedness condition.
- State footprint: none.
- Value influence: integer normalization and all comparisons in the fold.
- Dependents: the guarded dispatch twins, `scanVS`, `lastInt`, and both claims.
- Validation: integer collapse is exact; every result-bearing use is guarded by
  `isInt` derived from `allInts`. The positive proof covers negative, zero, and
  arbitrary-magnitude integers, and the negative result mutation is rejected.

### Guarded `applyBin("+")`, `applyCmp("<")`, and `applyCmp("!=")` twins

- Class: derived lemmas restating frozen MPY integer equations over the dynamic
  `Val` supersort.
- Semantic role: solver-side sort refinement of the exact operation; no lookup,
  evaluation order, control, exception, or cell transition is displaced.
- Complete domain: `isInt(V) andBool isInt(W)`.
- Matched context/containment: pure `applyBin`/`applyCmp` terms. The domain is
  exactly the existing `Int, Int` rule domain after guarded projection.
- State footprint: none.
- Value influence: loop-variable `x + 0`, branch conditions, accumulator result.
- Value justification: the RHSs are exactly `+Int`, `<Int`, and `=/=Int`, as in
  `MPY-INT`; overlap with the original static rules agrees because
  `projectIntTotal(I) = I`.
- Dependents: the loop circularity and target claim.
- Validation: fixed-semantics LLVM execution of the same body agrees with the
  independent oracle on the recorded cases; the proof's false-result probe is
  rejected. No opposite integer interpretation is admitted by the collapse
  equation.

### `scanStep`, `scanAfter`, `scanVS`

- Class: definitional summaries.
- Semantic role: name the mathematical accumulator result; they never rewrite
  an operational `<k>` term.
- Domain: total. `scanStep` partitions Boolean flags and integer trichotomy into
  disjoint cases. `scanVS` partitions empty, integer-head, and non-integer-head
  sequences; the non-integer totalization stops and preserves the accumulator,
  and is unreachable under the target's `allInts` precondition.
- Matched context/state footprint: pure terms only; no cells or continuation.
- Value influence: all four final accumulator fields and the returned value.
- Value justification: the integer-head equation exactly applies `scanStep`
  and structurally descends on the tail. Guards are complementary; recursive
  calls strictly shorten the sequence.
- Dependents: both claims and `nextSmallestSpec`.
- Validation: the loop claim proves fixed execution produces exactly this fold
  for an arbitrary suffix. The accumulator invariant above connects the fold
  to the second-distinct-minimum property.

### Accessors, `lastInt`, and `nextSmallestSpec`

- Class: definitional summaries.
- Semantic role: project fold fields, characterize the final local `x`, and
  choose `second` or `noneV`; no execution is replaced.
- Domain: total. Accessors cover the sole `ScanState` constructor. `lastInt`
  covers empty, integer-head, and non-integer-head sequences with disjoint
  guards. `nextSmallestSpec` is unconditional.
- Matched context/state footprint: pure terms only; none.
- Value influence: target return value and exact final loop-local state.
- Value justification: exhaustive constructor equations and the same
  `found-second` flag that fixed execution tests before returning.
- Dependents: loop and target claims.
- Validation: `SPEC.next-smallest` connects module load and complete fixed
  execution to this value; the `[1, 2] -> noneV` mutation reaches `2` and fails.

### `SPEC.loop-invariant`

- Class: derived reachability lemma/circularity.
- Semantic role: executes the fixed `#loop`, exact loop body, binding, and
  iteration protocol; it is not an operational rewrite in `verification.k`.
- Domain: every finite integer `ValSeq`, arbitrary integer accumulators and
  Boolean flags, and the exact local scope layout.
- Matched context: arbitrary trailing `<k>` continuation, current function
  environment, exact local bindings, and framed unrelated scopes/cells. This
  framing is valid because the body contains only assignments and conditionals;
  it has no return, exception, break, continue, allocation, or heap operation.
- State footprint: updates only `x`, the two flags, and the two integer
  accumulators; preserves `lst`, environment, heap, stack, return, exception,
  exit code, and the continuation.
- Value/control validation: base and step branches execute through MPY; the
  combined proof uses this claim to close the full program. The body mutation
  and false-result mutation both fail.
- Dependents: `SPEC.next-smallest`.

## Exact commands and actual results

The complete reproducible command is:

```sh
./prove.sh
```

It exited `0`. The positive target-proof commands inside it are:

```sh
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual proof output: `#Top`; actual `kprove` exit: `0`. This single proof command
proves every claim in `spec.k`, including the unbounded circularity and target
claim. Compiler warnings shown by the run originate in the supplied reference
semantics or unused pattern variables; none is a stuck proof state.

Concrete execution used the required LLVM modules:

```sh
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
```

Actual checks: solution load `PASS`; eight K assertions `PASS`; final K is
`.K`, exception is `NoExc`, and exit code is `0`.

The A5 mutation command was:

```sh
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual exit: `1` (expected). `WarnStuckClaimState` shows actual `<k> 2 ~> .K`
against the deliberately false `noneV` target for `[1, 2]`.

The body-sensitivity mutation command was:

```sh
kprove spec-body-mutation.k \
  --definition mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual exit: `1` (expected). `WarnStuckClaimState` shows actual
`<k> noneV ~> .K` against target `2` after mutating the body to always return
`None`.

## Gate results

- Gate A — PASS. The exact translated module is loaded and executed under the
  fixed semantics. All extensions are definitions or guarded derived lemmas;
  there is no execution-bypassing bridge or unconstrained result oracle.
  Equations have disjoint/agreeing coverage, the precondition is satisfiable,
  and both result and body mutations are rejected.
- Gate B — PASS. The theorem covers arbitrary finite lists of mathematical
  integers, including duplicates and negative/unbounded values, with no size
  bound. The accumulator invariant directly states and preserves the second
  distinct minimum property. This matches all prompt examples and the stated
  `None` behavior.
- Gate C — PASS. The trust boundary, commands, artifacts, actual outputs,
  mutation residuals, and finite differential scope are recorded and
  reproducible.

## Trust boundary

Trusted components are the supplied read-only MPY semantics, K's reachability
logic/Haskell backend, SMT integer reasoning, LLVM concrete backend, CPython AST
translation by the supplied `py2mpy.py`, and the ordinary correspondence of K
unbounded `Int` with Python arbitrary-precision integers. No opaque supplied
primitive such as `sortVS` is used by this proof. `projectIntTotal` is not an
external value oracle on the theorem domain: it collapses to the exact integer
under the proved `isInt` guard.

The reference semantics explicitly permits bare `list(VS)` values as read-only
claim inputs. The implementation never mutates `lst`; the LLVM assertions also
exercise the heap-reference path produced by concrete `ListExpr` construction.

## Empirical evidence

`prove.sh` uses the independent Python oracle `sorted(set(values))[1]` when two
distinct values exist, otherwise `None`. Actual result: zero mismatches over
all 19,531 lists of lengths 0 through 6 over `{-2,-1,0,1,2}`, plus 10,000
seeded random lists of lengths 0 through 40 with values in
`[-10^12, 10^12]`. These finite tests support intent validation; they do not
replace the unbounded K proof.

`concrete_tests.py` contains the prompt examples plus negative duplicates,
ordering duplicates, zero, and large-magnitude cases. Its function AST is
checked against `solution.py` before translation. The K LLVM execution passed
all assertions.

## Excluded behavior

- Lists containing non-integer MPY values are outside the prompt's promised
  input domain. In particular, MPY models `Bool` separately from mathematical
  `Int`.
- Non-list arguments and behaviors outside the supplied MPY subset are not
  claimed.
- Resource exhaustion and a standalone termination/liveness theorem are not
  part of this partial-correctness proof.

Artifact hashes from the validated run:

```text
0b6c340a4a0853b202320855642ff605dc7ab0a0f7a36c18b64da6d646877087  solution.py
d50c03b82c246ac26874ef0ca7badc663d13a1ba922ac325f5caf13a3d46f313  solution.mpy
39ef1863ae8c319165119661dba9507a3e58f9d177eba0f59b3d9df4420a3f3f  verification.k
36d62ac3f4a2933153f6f4c784bc77aedb3c3ef864ec74a9af76d3875169f023  spec.k
b0fd85e2be12ae2b155216c7040e336bd1fc315766c71c18cdd9d8b9f99ff953  prove.sh
```
