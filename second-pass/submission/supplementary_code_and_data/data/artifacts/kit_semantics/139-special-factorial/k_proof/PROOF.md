VALIDATED

## What is proven

For every K integer `N >= 1`, loading the exact translated
`special_factorial` definition and calling it with `N` reaches the integer
`productAfter(1, N, 1, 1)` under the supplied MPY semantics.  The proof
executes name lookup, argument binding, the function body, every loop-body
statement, return, frame restoration, and frame deallocation through the
reference rules.

This is a partial-correctness result in the Kit sense.  It does not separately
claim a liveness theorem about CPython execution.

## Formal claim

The entry claim `SPEC.special-factorial` starts from the standard empty module
scope and builtins scope, loads the exact `FuncDef` emitted in `solution.mpy`,
and calls the resulting binding with symbolic `N`.  Its precondition is
`N >=Int 1`.  Its result is:

```k
productAfter(1, N, 1, 1)
```

The claim also requires the final environment, scope allocator, heap, stack,
return state, exception state, and exit code to have their expected restored
values.  In particular, the call ends with `NoExc` and exit code `0`.

The circularity `SPEC.loop-invariant` is stated at the semantics' actual
recurring loop head, `#while(...)`.  For symbolic loop-head values `I`, `F`,
and `R`, it proves:

```text
i         becomes N + 1
factorial becomes factorialAfter(I, N, F)
result    becomes productAfter(I, N, F, R)
```

under `N >= 1`, `I >= 1`, and `I <= N + 1`.

At the function entry, `I = F = R = 1`.  At a loop head, the ordinary
mathematical invariant is:

```text
F = (I - 1)!
R = product(k!, k = 1 .. I - 1)
```

One iteration sets `F' = F * I = I!` and
`R' = R * F' = product(k!, k = 1 .. I)`.  At exit, `I = N + 1`, so the return
is exactly `N! * (N-1)! * ... * 1!`.  This last summary-to-contract connection
is an explicit mathematical induction used for intent validation; the K entry
postcondition itself is written with the equivalent accumulator recurrence.

## Proof-extension inventory

### `factorialAfter`

- Class: definitional summary.
- Semantic role: names the final `factorial` accumulator; it does not match or
  replace a program term.
- Domain: all triples of K integers `(I, N, F)`.
- Equations: return `F` when `I > N`; otherwise recur with
  `(I + 1, N, F * I)`.
- Coverage and overlap: `I > N` and `I <= N` are exhaustive and disjoint.
- Descent: the step decreases the nonnegative measure
  `max(N - I + 1, 0)`.
- Matched context and state footprint: none; the equations are pure and read or
  write no MPY cells.
- Value influence: constrains the loop claim's final local `factorial`; that
  local is deallocated before the entry claim returns.
- Justification and dependents: exact fold equation for the first source
  assignment; used by `SPEC.loop-invariant`.

### `productAfter`

- Class: definitional summary.
- Semantic role: names the final `result` accumulator without replacing MPY
  execution.
- Domain: all quadruples of K integers `(I, N, F, R)`.
- Equations: return `R` when `I > N`; otherwise recur with
  `(I + 1, N, F * I, R * (F * I))`.
- Coverage and overlap: `I > N` and `I <= N` are exhaustive and disjoint.
- Descent: the same `max(N - I + 1, 0)` measure.
- Matched context and state footprint: none; the equations are pure.
- Value influence: fixes the loop's final `result` and the entry claim's
  returned value.
- Value justification: exhaustive equations mirror the two accumulator
  updates in one source iteration.  `SPEC.loop-invariant` machine-connects
  those equations to fixed execution for the full symbolic domain.
- Dependents: both claims in `SPEC`.

### `SPEC.loop-invariant`

- Class: derived lemma (coinductive loop circularity).
- Semantic role: proves the exact MPY loop; it adds no operational rewrite to
  `verification.k`.
- Matched context: the exact `#while` guard and exact three-statement body,
  followed by an arbitrary continuation that is preserved.  It matches the
  current environment `L`, an exact four-binding local scope with arbitrary
  parent, an arbitrary surrounding scope map, and arbitrary omitted
  configuration cells.
- Justification scope and containment: the claim is universally proved over
  those same frames by fixed MPY rules.  Therefore every context in which the
  circularity can apply is within its machine-checked claim domain.
- State footprint: `i`, `factorial`, and `result` change; `n`, the environment,
  parent, surrounding scopes, continuation, heap, stack, return state,
  exception state, allocator cells, and exit code are preserved.
- Control validation: the body contains no abrupt control.  The claim consumes
  only the loop and preserves its continuation.
- Dependents: `SPEC.special-factorial`.
- Validation: the target proof is `#Top`, while the changed-body probe fails on
  the unequal `productAfter` arguments.

There are no operational bridges, priority rules, opaque result symbols,
trusted proof-local primitives, simplification lemmas, or proof-local rules
that intercept `Call`, `While`, `Return`, or any source expression.

## Exact commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh
```

Its final run exited `0`.  It executes these material commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py body-mutation.py > body-mutation.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled
python3 test_solution.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kprove summary-test.k \
  --definition verification-kompiled \
  --spec-module SUMMARY-TEST
```

Actual target-proof output:

```text
#Top
Exit: 0
```

Actual ground-summary-check output:

```text
#Top
Exit: 0
```

The ground summary claims also print `WarnTrivialClaim`: their ground
functions simplify to the expected integers before reachability rewriting.

Actual concrete result:

```text
<k> .K </k>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
Exit: 0
```

Actual independent differential output:

```text
oracle_1_to_6=[1, 2, 12, 288, 34560, 24883200]
inputs=1..20 mismatches=0
Exit: 0
```

The LLVM build reports non-exhaustiveness warnings in unused supplied helpers
(`mapStrVS`, float helpers, `joinCodes`, and out-of-bounds `valSeqAt`).  The
Haskell build reports unused-variable warnings in the supplied string-order
rules.  Both builds exit `0`; none of those constructs is reached by this
integer-only program.

Construction diagnostics, not positive target-proof commands:

- A bounded proof of an earlier invariant beginning with source `While`
  repeatedly reached the semantic loop head `#while`; the invariant was
  corrected to the exact recurring term.  The repaired invariant and combined
  target proof both produce `#Top`.
- Filtering with only `--claims SPEC.special-factorial` excludes the companion
  circularity and expands the loop.  The required command proves the complete
  `SPEC` module so both claims are present.
- Bare functional ground claims are unsupported by this Haskell backend; the
  retained `summary-test.k` uses supported `<k>` reachability claims.

## Gate results

### Gate A — PASS

- A1 program identity: `solution.mpy` is regenerated from `solution.py`; the
  entry claim contains that exact `FuncDef`, binding, body, and argument.  No
  rule skips program-defined code.
- A1 body sensitivity: `body-mutation.py` changes the result update to add one.
  The exact command
  `kprove spec-body-mutation.k --definition verification-kompiled --spec-module SPEC-BODY-MUTATION`
  exits `1` with `WarnStuckClaimState`.  Its residual requires equality between
  `productAfter(..., R * (F * I) + 1)` and
  `productAfter(..., R * (F * I))`.
- A2/A3 state, binding, evaluation, and control: fixed MPY rules perform
  lookup, parameter binding, ordered assignments, loop control, return, and
  frame pop.  No operational bridge exists.
- A4 consistency: both summary equation pairs have disjoint, exhaustive guards
  and a decreasing integer measure.
- A5 satisfiability: `N = 4` satisfies the precondition and the concrete K
  harness checks return `288`.
- A5 result constraint: the off-by-one spec in `spec-vacuity.k` is false.  The
  exact command
  `kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY`
  exits `1` with `WarnStuckClaimState`; the residual requires
  `productAfter(2, N, 1, 1) + 1 = productAfter(2, N, 1, 1)`.

### Gate B — PASS

- Input domain: K integer `N >= 1`, exactly the prompt's positive-integer
  domain.  Boolean, float, zero, negative, and non-integer inputs are excluded.
- Language model: only arbitrary-precision integer arithmetic and structured
  function/loop control are used.  These are the relevant supplied MPY
  constructs, and K integers align with Python's unbounded integer results for
  this program.
- Summary-to-property adequacy: the induction above establishes that the
  accumulator recurrence is the prompt's product of factorials.
- Implementation alignment: concrete checks include the stated `N = 4`
  example and agree with the contract.

### Gate C — PASS

- Every proof-local extension and named trust item is listed in this report.
- `smoke.py` / `smoke.mpy` checks exact results for `N = 1..6` under LLVM MPY
  execution.
- `summary-test.k` checks both proof summaries against independently obtained
  factorial/product constants for `N = 1..6`.
- `test_solution.py` uses Python's independently implemented `math.factorial`
  and `math.prod` as its oracle over every integer `N = 1..20`; it reports zero
  mismatches.
- Both mutation artifacts, exact commands, expected nonzero outcomes, and
  residual obligations are preserved.

## Trust boundary

- Correctness of K v7.1.293, its LLVM/Haskell backends, and the integer hooks.
- Correctness of the supplied read-only MPY semantics for literals, integer
  operations, comparison, assignment, `while`, function definition/call,
  lookup, return, and frame handling.
- Correctness of the supplied `py2mpy.py` transliteration.  Its generated
  `solution.mpy` is checked into the workspace and regenerated by `prove.sh`.
- The short mathematical induction connecting the accumulator recurrence to
  the natural-language product.  It is transparent and independently tested,
  but is not a separate K claim.

No opaque primitive imported elsewhere in MPY is invoked by this program.

## Empirically supported facts

- LLVM MPY execution satisfies all six ground assertions in `smoke.py`.
- The Python implementation and the independent standard-library oracle agree
  on all inputs `1..20`.
- The K summary functions reduce to the same independent oracle constants for
  inputs `1..6`.
- These finite checks support intent and toolchain adequacy; they are not
  presented as universal proofs.

## Excluded behavior

- Inputs outside positive K integers, including Python `bool`, are outside the
  formal precondition.
- Exceptional behavior and resource exhaustion outside that domain are not
  modeled or claimed.
- Total-correctness/termination of CPython execution and equivalence of the
  entire supplied MPY semantics to CPython are outside this theorem.
