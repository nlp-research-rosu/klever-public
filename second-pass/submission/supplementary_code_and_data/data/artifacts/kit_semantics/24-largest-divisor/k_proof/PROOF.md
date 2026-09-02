VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every mathematical integer `N >= 2`,
if the exact `largest_divisor` closure from `solution.py` terminates, it returns
`largestDivisorAtOrBelow(N, N -Int 1)`.  That summary is the first positive
divisor encountered by descending from `N - 1`, hence the largest positive
divisor of `N` that is strictly smaller than `N`.

This is a K partial-correctness result.  The simple decreasing-loop termination
argument is recorded below as validation evidence, but termination is not a
liveness theorem proved by `kprove`.

## Formal claim

The validation scope is:

- Program boundary: `Call(Name("largest_divisor"), Int(N))` with the module
  binding pinned to the exact parameter list and constructor body emitted in
  `solution.mpy`.  Lookup, argument evaluation, frame creation, parameter
  binding, the assignment, every loop test and iteration, return, and frame
  cleanup all execute under the fixed semantics.
- Input domain: unbounded integers satisfying `N >=Int 2`.
- Observable final state: the returned integer.  The claim also fixes the
  module environment, scopes, heap, allocation counters, stack, return state,
  exception state, and exit code before and after the call.
- Intended property: return the largest positive divisor of `N` below `N`.

The target claim is `SPEC.largest-divisor` in `spec.k`:

```k
Call(Name("largest_divisor"), Int(N))
  => largestDivisorAtOrBelow(N, N -Int 1)
requires N >=Int 2
```

The helper is defined by descending search:

```text
L(N,D) = D          when D >= 1 and N mod D = 0
L(N,D) = L(N,D-1)   when D > 1 and N mod D != 0
```

Starting at `D = N - 1`, the first case returns a positive proper divisor.
Every larger candidate has already failed the divisibility test, which makes
the returned divisor maximal.  The search cannot pass `1`, because
`pyMod(N, 1) = 0`.

`SPEC.loop-invariant` is the coinductive loop lemma.  At a loop head with
`n = N` and `divisor = D`, where `N >= 2` and `D >= 1`, it executes the exact
loop, exact return suffix, and exact call-frame cleanup, returning `L(N,D)`.
Its false-guard case uses the first equation; its true-guard case decrements
`D`, uses the second equation, and re-establishes the same loop-head claim.
The target claim instantiates it with `D = N - 1`.

## Proof-extension inventory

### `largestDivisorAtOrBelow` and its two equations

- Extension: the `[function]` symbol and the two guarded rules in
  `verification.k`.
- Class: definitional summary.
- Semantic role: names a mathematical result; it does not match or replace any
  Python expression, statement, call, loop, return, or configuration.
- Domain: every proof use has `N >= 2` and `D >= 1`.  The first guard is
  `D >= 1 and pyMod(N,D) == 0`; the second is
  `D > 1 and pyMod(N,D) != 0`.
- Matched context: only a term `largestDivisorAtOrBelow(N,D)`, never an
  operational cell or continuation.
- Justification scope: descending search over positive candidate divisors.
- Context containment: no operational context is matched.  All summary uses
  lie in the guarded domain.
- State footprint: none.
- Value influence: fixes the loop lemma's return value and the target
  postcondition.
- Value justification: the guards select exactly “return this divisor” or
  “continue at the next lower candidate.”  They are disjoint.  They cover all
  uses because `D = 1` always satisfies the divisibility rule.  Recursive
  applications strictly decrease `D` while `D > 1`.  The symbol is
  intentionally not declared `[total]` outside this use domain.
- Justification: the direct recursive definition of the first divisor at or
  below `D`.
- Dependents: `SPEC.loop-invariant` and `SPEC.largest-divisor`.
- Control validation: not applicable to the equations; they replace no
  execution.  The fixed-semantics program/body sensitivity probe is recorded
  below.
- Value validation: the universal entry claim connects fixed execution to the
  summary; `largest_divisor(15)` concretely produces `5`; the opposite result
  `6` is rejected; independent brute force has zero mismatches for
  `2 <= n <= 1000`.
- Validation: guard disjointness, use-domain coverage, and recursive descent
  were audited from the final file.

### `SPEC.loop-invariant`

- Extension: the auxiliary reachability claim labeled `loop-invariant`.
- Class: derived lemma (a fixed-semantics execution circularity).
- Semantic role: reasons about the real loop; it adds no ordinary rewrite and
  skips no source operation.
- Domain: `N >= 2` and `D >= 1`.
- Matched context: the exact internal `#while` term, exact
  `Return(Name("divisor")) .Stmts ~> #endcall` suffix, exact function closure
  and local bindings, arbitrary caller continuation `CONT` stored in the exact
  call frame, and closed values for every configuration cell.
- Justification scope: exactly those configurations quantified by the claim.
- Context containment: there are no ellipses, wildcards, weakened suffixes, or
  omitted cells in the claim.  `CONT` is quantified in both the saved frame
  and restored right-hand continuation.
- State footprint: reads the loop computation, `n`, `divisor`, environment,
  scopes, frame, return/exception state, and counters; updates `divisor`;
  preserves `n`, heap, heap counter, exception, and exit code; then performs
  the fixed return and restores the caller environment, scope counter, scope
  map, and stack.
- Value influence: establishes the returned integer used by the target claim.
- Value justification: the guarded summary equations align one-for-one with
  the fixed loop's false and true paths.
- Justification: `kprove` closes the claim by fixed-semantics symbolic
  execution and coinduction.
- Dependents: `SPEC.largest-divisor`.
- Control validation: the combined target proof executes lookup, call setup,
  loop, return, and frame pop.  The body-mutation probe changes the return
  expression and is rejected at concrete result `4`.
- Value validation: the combined universal connection claim prints `#Top`;
  the false-result probe is rejected at concrete result `5`.
- Validation: focused and combined proof commands both print `#Top` and exit
  zero.

There are no proof-local operational bridges, trusted primitives,
`[simplification]` rules, priority rules, opaque values, or `owise` rules.

## Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`.  Running:

```bash
./prove.sh
```

exited `0`.  Its constituent commands and actual results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 differential_test.py
```

Output:

```text
python differential: 999/999 passed; mismatches=0
```

```bash
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
```

LLVM compilation exited `0` with warnings in unused portions of the supplied
semantics.  `krun` exited `0`; the final configuration contained:

```text
<k> .K </k>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Haskell compilation exited `0` with only unused-variable warnings originating
in the supplied `str.k`.  The focused and combined proof commands each exited
`0` and printed:

```text
#Top
```

The required negative probes were:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual results:

```text
spec-vacuity.k: WarnStuckClaimState with <k> 5 ~> .K </k>
spec-vacuity.k exit: 1 (expected non-zero)
spec-body-mutation.k: WarnStuckClaimState with <k> 4 ~> .K </k>
spec-body-mutation.k exit: 1 (expected non-zero)
```

Artifact-identity audit:

```bash
python3 py2mpy.py solution.py | cmp -s - solution.mpy
```

exited `0`; the regenerated `solution.mpy` was byte-identical.  The K tools
reported version `v7.1.293`.

## Gate results

### Gate A — PASS

- A1: the exact function binding and body execute.  Changing the return from
  `divisor` to `divisor - 1` makes the old ground theorem fail with result `4`
  instead of `5`.
- A2: no operational bridge exists.  The claims explicitly preserve or restore
  every configuration cell and expose the real call-frame transitions.
- A3: fixed lookup, argument evaluation, binding, loop control, return, and
  frame-pop rules execute.  The loop lemma has an exact suffix and exact saved
  continuation.
- A4: the two summary guards are disjoint, cover their complete use domain, and
  recursive descent is strict.  No false off-domain totalization rule exists.
- A5: `N = 15` is a realizable witness.  The true result is `5`; the deliberately
  false result `6` is rejected with exit `1`.

### Gate B — PASS

- B1: the formal domain is `n >= 2`, the conventional domain on which a
  positive proper divisor exists.  Inputs below `2` are explicitly excluded.
- B2: the supplied model uses unbounded integers and defines `pyMod` with
  Python's floored-modulo behavior.  For this positive-divisor domain it agrees
  with CPython for every used operation.
- B3: the summary is a direct descending definition of the first divisor, and
  maximality follows because all larger candidates have already failed.
- B4: the implementation performs exactly that descending search; the prompt's
  example `15 -> 5` and independent tests agree.

### Gate C — PASS

The trust ledger is explicit below; all claimed concrete, differential,
identity, and mutation evidence has an existing artifact and exact command.
Formal, mathematical, empirical, and excluded conclusions are separated.

## Trust boundary

- Supplied `reference-semantics/`: trusted fixed model of the Python subset.
  It affects value, control, state, and exceptional behavior of both claims.
  It is not modified.  Concrete LLVM execution and source inspection support
  the used paths, but this task does not prove the semantics itself.
- `py2mpy.py`: trusted fixed syntactic translator connecting `solution.py` to
  `solution.mpy`.  Regeneration is byte-identical, and the closure constructor
  in `spec.k` matches that generated body.  Translator correctness is not a
  theorem of this proof.
- K `v7.1.293`, its Haskell/LLVM backends, SMT reasoning, and host runtime:
  trusted proof/execution infrastructure on which every machine result depends.
- No application operation is treated as a trusted primitive.  In particular,
  `%`, comparison, assignment, loop control, calls, and return all use supplied
  fixed-semantics rules.

## Empirically supported facts

- `concrete-tests.py` uses the same function AST as `solution.py` and checks
  `15 -> 5`, prime input `7 -> 1`, composite input `100 -> 50`, and boundary
  input `2 -> 1`.  LLVM `krun` ended with no exception and exit code zero.
- `differential_test.py` compares `solution.largest_divisor` with an independent
  brute-force `max` over all positive proper divisors for every integer from
  `2` through `1000`: 999 cases, zero mismatches.
- `spec-vacuity.k` and `spec-body-mutation.k` are persistent negative evidence,
  not universal proofs.  Their non-zero results support non-vacuity and body
  sensitivity.

## Excluded behavior

- Inputs `n < 2`, for which the positive-proper-divisor contract has no result,
  are outside the formal theorem and the implementation may reach division by
  zero.
- K reachability proves partial correctness, not total correctness.  Separately,
  for `n >= 2`, `divisor` starts at `n - 1`, decreases by one only after a
  failed test, and must stop at `1`, which divides every integer.
- Module-loading syntax is not part of the entry claim; the claim begins after
  the module has established the exact `largest_divisor` closure binding.
- Behavior of unrelated Python features and differences between the supplied
  subset semantics and full CPython are outside the theorem.
