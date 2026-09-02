VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact `sum_to_n` closure translated
from `solution.py` has the following partial-correctness behavior for every
symbolic K integer `N`:

- If `N <= 0`, a call returns `0`.
- If `N >= 1`, a call returns `N *Int (N +Int 1) /Int 2`.

Thus the theorem covers the full annotated `int` input domain, not fixed sizes
or bounded unrollings. For positive inputs the result is the triangular-number
identity for the inclusive sum from 1 through `N`; for non-positive inputs the
loop sums the empty range and returns zero. This is a partial-correctness proof:
termination is not a separate proved liveness theorem.

## Formal claim and scope

The theorem consists of all three claims in `spec.k`:

1. `SPEC.sum-loop` is the loop circularity. At the stable internal
   `#while` head, from locals `n = N` and `total = S`, with `N >= 0`, it
   reaches `n = 0` and `total = S +Int sumToN(N)`.
2. `SPEC.sum-to-n-empty-range` covers every `N <= 0` and returns `0`.
3. `SPEC.sum-to-n-positive` covers every `N >= 1` and returns `sumToN(N)`.

The entry claims begin at function invocation. The module scope binds
`"sum_to_n"` to a closure containing the exact parameter list and translated
body. `artifact_checks.py` mechanically confirms that both closure bodies in
`spec.k` match the freshly translated `solution.mpy` body.

The observed state is the return value plus normal restoration of `env`,
`scopes`, `scopeLoc`, `heap`, `heapLoc`, `stack`, `ret`, `exc`, and
`exit-code`. The loop claim frames the continuation and unrelated state cells;
its matched and proved domain are equally general, while its current local
scope is explicit.

The loop obligations are:

- Base: at `N = 0`, the guard is false and `sumToN(0) = 0`.
- Step: for `N > 0`, one body execution changes
  `(S, N)` to `(S +Int N, N -Int 1)`; the circularity and the closed form
  establish the same final accumulator.
- Entry: the call binds `n = N`, initializes `total = 0`, reaches the loop
  head, and returns the final accumulator.

## Proof-extension inventory

### `sumToN`

- Class: definitional summary.
- Rules: `sumToN(N) => N *Int (N +Int 1) /Int 2` for `N >= 0`, and
  `sumToN(N) => 0` for `N < 0`.
- Semantic role: names the mathematical result; it does not match or replace
  any program computation.
- Domain: all K integers. The guards are disjoint and exhaustive, and there is
  no recursive descent or overlap.
- Matched context and state footprint: only a `sumToN(Int)` term; no
  continuation, binding, control stack, or state cell is read or changed.
- Value influence: the loop post-state and positive entry postcondition.
- Value justification: the equations define the triangular closed form, while
  `SPEC.sum-loop` machine-checks that fixed loop execution produces it.
- Dependents: `SPEC.sum-loop` and `SPEC.sum-to-n-positive`.
- Validation: the positive target proof closes; the off-by-one mutation is
  rejected; the independent Python range-sum oracle has zero mismatches.

### `SPEC.sum-loop`

- Class: derived auxiliary reachability claim/circularity.
- Semantic role: summarizes repeated fixed-semantics execution after proving
  the base and inductive paths; it is not an ordinary rewrite rule or an
  operational bridge.
- Domain and matched context: `N >= 0`, exact `#while` condition/body, local
  scope at environment 1, and an arbitrary framed continuation and unrelated
  configuration cells.
- Justification scope and containment: the claim itself is universally proved
  over exactly that framed domain. The recurring fixed-semantics configuration
  has the same `#while` head and local bindings.
- State footprint: reads and writes only local `"n"` and `"total"`; all framed
  state and the continuation are preserved.
- Value influence: supplies the accumulator returned by both entry paths.
- Dependents: `SPEC.sum-to-n-positive`; the empty-range claim can execute the
  false guard directly.
- Validation: `kprove` proves the circularity and the full spec together.

There are no proof-local operational bridges, opaque result symbols,
simplification lemmas, priority rules, or newly trusted primitives.

## Exact commands and actual outputs

The complete reproducible command sequence is `./prove.sh`:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 artifact_checks.py
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual final run:

- `./prove.sh`: exit `0`.
- `artifact_checks.py`: exit `0`,
  `function_ast_match=true solution_mpy_current=true spec_closure_matches=2`.
- `differential_test.py`: exit `0`, `inputs=2001 mismatches=0`.
- LLVM `kompile`: exit `0`, with supplied-semantics warnings about unrelated
  non-exhaustive helpers.
- `krun smoke.mpy`: exit `0`; final `<k>` is `.K`, `<exc>` is `NoExc`, and
  `<exit-code>` is `0`.
- Haskell `kompile`: exit `0`, with unused-variable warnings from the supplied
  `str.k`.
- Positive target `kprove spec.k`: exit `0`, output `#Top`.
- False-postcondition `kprove spec-vacuity.k`: exit `1` with
  `WarnStuckClaimState`; the residual requires the impossible equality
  `N*(N+1)/2 + 1 == N*(N+1)/2`.
- Body-sensitivity `kprove spec-body-mutation.k`: exit `1` with
  `WarnStuckClaimState`; for witness `N = 1`, the changed body returns `2`
  instead of `1`.

The expected failures are handled by `prove.sh`, which prints
`EXPECTED FAILURE` only after observing each non-zero exit.

## Gate results

- Gate A — PASS. The exact program-defined body executes under fixed
  semantics; there is no operational bridge; summary equations are total,
  disjoint, and truthful; realizable witnesses include `N = 0` and `N = 1`;
  both postcondition and body mutations are rejected.
- Gate B — PASS. The two entry preconditions partition all K integers and the
  postconditions match the HumanEval contract and every stated example. No
  bounded-size restriction is used.
- Gate C — PASS. Commands, artifacts, scopes, oracle, mutation witnesses,
  outputs, and trust assumptions are reproducible and recorded.

## Trust boundary

The trusted base is the supplied read-only `reference-semantics/`, K's
integer/Boolean/map/list hooks, the Haskell and LLVM backends, and the supplied
`py2mpy.py` transliterator. `artifact_checks.py` verifies translation freshness
and theorem/body identity, but does not re-prove those trusted tools.

No supplied opaque arithmetic primitive affects this theorem. The formal input
sort is K `Int`, corresponding to the prompt's `int` annotation. The reference
semantics and the theorem model mathematical arbitrary-precision integers; they
do not model finite machine resource exhaustion.

## Empirically supported facts

- `smoke.mpy` runs the five prompt examples plus `0` and `-3` through the LLVM
  semantics, with assertions as the oracle and no exception.
- `differential_test.py` compares `solution.sum_to_n` with the independently
  implemented `sum(range(1, n + 1))` oracle for every integer from `-1000`
  through `1000`, including all prompt examples: 2,001 inputs and zero
  mismatches.
- These finite tests support translation and model adequacy; the universal
  result comes from `kprove`, not from testing.

## Excluded behavior

Inputs outside the annotated `int` contract are not claimed. Python annotation
enforcement, resource exhaustion, and a separate total-correctness/termination
theorem are outside the formal claim. Module loading is exercised concretely;
the symbolic theorem starts at the exact post-load function binding and proves
the complete call and body behavior.
