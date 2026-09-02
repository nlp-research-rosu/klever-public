VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact translated body of
`x_or_y(n, x, y)` has the following partial-correctness property for every
`N:Int` and every modeled values `X:Val` and `Y:Val`:

- if `N < 2`, the returned value is `Y`;
- if `N >= 2` and some integer `I` with `2 <= I < N` divides `N`, the
  returned value is `Y`;
- otherwise, the returned value is `X`.

For integers, this is exactly “return `x` when `n` is prime and `y`
otherwise.” The reachability proof is a partial-correctness proof; termination
is not a separately proved liveness result.

## Formal claim

The target claim `[x-or-y]` starts from the complete initial MPY configuration,
loads the exact `FuncDef` constructor emitted in `solution.mpy`, resolves and
calls `x_or_y`, executes its body, returns, removes the call frame, and reaches
`?V:Val` with:

```k
ensures ?V ==K xOrYSpec(N, X, Y)
```

The total entry summary is:

```text
xOrYSpec(N, X, Y) = Y                         when N < 2
xOrYSpec(N, X, Y) = trialChoice(N, 2, X, Y)  when N >= 2
```

On its used domain `I >= 2`, `trialChoice(N,I,R,Y)` returns `R` at
`I >= N`. At `I < N`, it advances to `I + 1`, carrying `Y` if `I` divides
`N`, and otherwise carrying `R`. Thus an initial `R = X` survives exactly when
no candidate divisor in `2 .. N-1` divides `N`.

The loop claim `[trial-loop]` supplies the circularity:

- Base: when `I = N`, the guard is false and `trialChoice(N,I,R,Y)` reduces
  to `R`.
- Divisor step: the real `%` comparison assigns `Y`, increments `I`, and
  matches the divisor recurrence.
- Non-divisor step: the real comparison preserves `R`, increments `I`, and
  matches the other recurrence.
- Entry discharge: the function reaches the loop with `I = 2`, `R = X`, and
  `N >= 2`; the early return handles `N < 2`.

## Proof-extension inventory

### `trialChoice` and its three equations

- **Class:** Definitional summary.
- **Semantic role:** Names the mathematical value obtained by the remaining
  divisor scan. It does not match or rewrite `Call`, `While`, `%`, lookup,
  assignment, return, or any other program computation.
- **Domain:** Every use has `I >= 2`. The invariant further has `I <= N`.
  Within that domain, `I >= N` is the base case; for `I < N`, the guards
  `pyMod(N,I) ==Int 0` and `pyMod(N,I) =/=Int 0` are exhaustive and disjoint.
- **Matched context:** Only a term
  `trialChoice(N,I,R,Y)`; no continuation, stack, binding, or framed cell is
  matched.
- **Justification scope:** The exact recurrence over candidate divisors
  `I .. N-1`, with a nonzero divisor because `I >= 2`.
- **Context containment:** There is no operational configuration match.
  Every occurrence is within the stated `I >= 2` domain.
- **State footprint:** None.
- **Value influence:** Determines the final `result` local in `[trial-loop]`
  and the returned value in `[x-or-y]`.
- **Value justification:** The guarded equations are the exhaustive
  definition. Recursion strictly increases `I` while `I < N`, so it reaches
  the base case on every used ground instance.
- **Justification:** Direct mathematical definition of exhaustive trial
  division.
- **Dependents:** `[trial-loop]` and `[x-or-y]`.
- **Control validation:** Not applicable; no execution is replaced.
- **Value validation:** `[trial-loop]` is the bridge-free universal
  reachability connection from the fixed-semantics loop to this value.
  Concrete prime/composite witnesses and the rejected false-result probe
  independently exercise distinct results.
- **Validation:** Equation guards are pairwise disjoint, cover every use, and
  contain no zero divisor. The focused loop proof prints `#Top`.

### `xOrYSpec` and its two equations

- **Class:** Definitional summary.
- **Semantic role:** Selects the early-return case or the loop summary. It
  does not replace execution.
- **Domain:** All `N:Int`, `X:Val`, and `Y:Val`.
- **Matched context:** Only `xOrYSpec(N,X,Y)`.
- **Justification scope:** All integers, split by `N < 2` and `N >= 2`.
- **Context containment:** There is no operational configuration match.
- **State footprint:** None.
- **Value influence:** It is the target claim's complete returned-value
  postcondition.
- **Value justification:** Its two disjoint and exhaustive equations, plus
  the justified `trialChoice` definition.
- **Justification:** Standard integer primality: `N >= 2` with no divisor in
  `2 .. N-1`.
- **Dependents:** `[x-or-y]`.
- **Control validation:** Not applicable; no execution is replaced.
- **Value validation:** The target executes the early return or the connected
  loop claim under fixed semantics. The false-result probe rejects the
  opposite result for `N = 2`.
- **Validation:** The complete target proof prints `#Top`.

### `[trial-loop]`

- **Class:** Derived lemma (loop-invariant reachability claim/circularity).
- **Semantic role:** Proves the result of the real `#while` computation; it is
  machine-checked from fixed MPY steps and is not an assumed rewrite in
  `verification.k`.
- **Domain:** `I >= 2` and `I <= N`, arbitrary `X`, `Y`, and current result
  `R`.
- **Matched context:** Exact `#while` syntax and exact five-entry local frame
  at environment `1`; `scopeLoc` is `2`; the stack is exactly
  `ListItem(frame(.K,0,1))`; return and exception cells are `noRet` and
  `NoExc`. The trailing `<k>` continuation and the base scopes, heap,
  heap location, and exit code are universally framed and preserved.
- **Justification scope:** The claim proves exactly that same universally
  framed context. No narrower trailing continuation or omitted control stack
  is used as justification.
- **Context containment:** Matched and proved contexts are identical.
- **State footprint:** Reads `n`, `i`, `result`, and `y`; writes only `i` and
  `result`; preserves `x`, all other scopes, environment, heap, allocation
  counters, stack, return state, exception state, exit code, and continuation.
- **Value influence:** Computes the live `result` value consumed by the
  function's real `Return`.
- **Value justification:** The `trialChoice` equations match the two `%`
  branches and the false loop guard.
- **Justification:** Focused bridge-free proof under `MPY` prints `#Top`.
- **Dependents:** `[x-or-y]`.
- **Control validation:** The fixed semantics evaluates the guard, body,
  assignments, increment, and loop continuation. There is no abrupt return
  inside the loop claim. The source-body mutation is rejected.
- **Value validation:** Prime and composite concrete tests produce distinct
  selected values; the unchanged-body false-result mutation and changed-body
  mutation both fail with the opposite concrete value in `<k>`.
- **Validation:** Base, divisor, and non-divisor paths close in the focused
  proof; the target closes only when the invariant is included in the full
  spec proof.

There are no operational bridges, trusted primitives, opaque result-bearing
oracles, simplification lemmas, priority rules, or `[concrete]` proof-local
rules in `verification.k` or `spec.k`.

## Commands and actual results

The complete reproducible command is:

```bash
./prove.sh
```

It exited `0`. The script records and runs these exact positive commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 py2mpy.py solution_body_mutant.py > solution_body_mutant.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy --definition runtime-kompiled
python3 test_solution.py

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.trial-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual results:

- Translator commands: exit `0`.
- LLVM `kompile`: exit `0`. It reported only supplied-semantics warnings
  about non-exhaustive unrelated total helpers and unused variables.
- `krun`: exit `0`; final `<k>` was `.K`, `<exc>` was `NoExc`, and the modeled
  `<exit-code>` was `0`.
- `python3 test_solution.py`: exit `0`,
  `cases=223 mismatches=0`.
- Haskell `kompile`: exit `0`; it reported only the supplied `str.k` unused
  variable warnings.
- Focused `[trial-loop]` kprove: output `#Top`, exit `0`.
- Complete-spec kprove (both required claims): output `#Top`, exit `0`.
- The kprove commands also emitted non-fatal unused-variable warnings for
  supplied `str.k` variables and intentionally framed spec cells; neither run
  emitted a stuck-claim warning.

The exact negative commands are also in `prove.sh`:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual negative results:

- False-result mutation: exit `1`, `WarnStuckClaimState`; the residual
  `<k>` value was `10` while the mutated postcondition required `20`.
- Changed-body mutation: exit `1`, `WarnStuckClaimState`; the residual
  `<k>` value was `20` while the original prime-input result required `10`.
- `prove.sh` recognizes those two nonzero exits as expected failures and
  reports both probes as rejected.

## Gate results

### Gate A — PASS

- **A1:** The entry claim contains the exact function signature and constructor
  body generated in `solution.mpy`; all program-defined operations execute
  under fixed semantics. Changing `result = x` to `result = y` changes the
  residual to `20` and invalidates the original result claim.
- **A2:** No operational bridge skips state. The loop claim's read/write and
  preserved cells are enumerated above; the entry claim executes call-frame
  allocation, return, and cleanup.
- **A3:** Fixed semantics performs name lookup, callee and argument evaluation,
  parameter binding, branch evaluation, `%`, assignments, loop control,
  return, and frame pop. No rule pins a textual binding or discards a framed
  continuation.
- **A4:** `trialChoice` is guarded on a nonzero candidate divisor, its terminal
  and recursive cases are disjoint, its divisor/non-divisor cases are
  exhaustive on every use, and recursion descends toward `I = N`.
  `xOrYSpec` is total with two disjoint, exhaustive integer guards.
- **A5:** `N = 2`, `X = 10`, `Y = 20` is realizable. The unchanged program
  returns `10`; the deliberately false `20` postcondition is rejected.

### Gate B — PASS

- **B1:** The formal domain is integer `n` and arbitrary values `x` and `y`
  representable by MPY. This matches the prompt's primality contract and
  integer examples. No positivity precondition is added; integers below `2`
  return `y`.
- **B2:** K `Int` is unbounded, matching Python integer arithmetic for the
  used operations. Divisors are always at least `2`, so `%` has no zero-divisor
  behavior. Inputs outside the supplied MPY value model are excluded.
- **B3:** The execution summary checks every candidate integer in
  `2 .. N-1`. Retaining `X` is therefore equivalent to `N >= 2` having no
  proper divisor, the standard definition of prime. This bridge follows
  directly from the exhaustive recurrence and is independently supported by
  the differential test.
- **B4:** The implementation and prompt agree on the prompt examples and the
  entire formal integer domain.

### Gate C — PASS

- The proof-extension inventory was rebuilt from `verification.k` and
  `spec.k`, including every proof-local function, equation, and claim.
- The trust boundary and every dependent claim are recorded below.
- Concrete, differential, false-result, and source-body mutation artifacts
  exist and are run by exact commands in `prove.sh`.
- Formal results, finite evidence, trust assumptions, and excluded behavior
  are separated in this report.

## Trust boundary

- `reference-semantics/` is supplied and fixed. Its MPY rules and K's built-in
  integer/Boolean theories are trusted by both claims and affect value,
  control, state, and exception behavior.
- K v7.1.293, its Haskell backend, and its SMT/proof implementation are trusted
  for the `#Top` results.
- `py2mpy.py` is supplied and fixed. It is trusted only for the translation
  from `solution.py` to `solution.mpy`; the K theorem itself starts from the
  explicit constructor body shown in `spec.k`.
- CPython 3.10.12 and `math.isqrt` are trusted only as the independent finite
  differential oracle. They are not premises of the K proof.
- No program-defined helper, proof-local operational bridge, or result-bearing
  primitive is trusted.

## Empirically supported facts

- `concrete_tests.py` / `concrete_tests.mpy` exercise nine MPY/LLVM cases:
  negative, zero, one, the smallest primes, composite numbers, and both prompt
  examples. The oracle is the assertions written independently of the proof
  equations. Result: final `.K`, `NoExc`, modeled exit code `0`.
- `test_solution.py` uses CPython's `isqrt` and checks possible divisors only
  through the square root. It tests every `n` from `-20` through `200`, with
  varying `x` and `y`, plus both prompt examples: 223 cases, zero mismatches.
- These finite tests support intent and implementation alignment; they do not
  replace the universal K reachability proof.

## Excluded behavior

- The proof is partial correctness and does not separately establish
  termination, complexity, or resource bounds.
- `n` values that are not K `Int` values and `x`/`y` objects outside the
  supplied MPY `Val` model are outside the theorem.
- Behavior of full CPython features absent from the supplied reference
  semantics is outside the theorem.
- The supplied-semantics compiler warnings concern unrelated helper cases and
  were not suppressed or repaired because `reference-semantics/` is read-only.
