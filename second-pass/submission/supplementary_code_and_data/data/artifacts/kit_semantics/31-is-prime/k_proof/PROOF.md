VALIDATED

# Proof report

## What is proven

Under the supplied `MPY` reference semantics, the exact `is_prime` closure
translated from `solution.py`, when called with any K `Int` value `N` from the
clean HumanEval entry configuration, returns:

- `false` when `N < 2`; and
- `true` exactly when no integer in `[2, N)` divides `N`, when `N >= 2`.

For integers at least two, absence of a proper divisor in `[2, N)` is
equivalent to the standard definition of primality. The result is therefore
`true` exactly for prime integer inputs.

This is a K reachability proof of partial correctness. The reachability theorem
does not itself prove termination. The source loop nevertheless has the
ordinary natural-number variant `N - divisor`: for `N >= 2`, `divisor` starts
at 2, increases by one, and stops at `N`; inputs below 2 return before the loop.

## Formal claim and scope

The program boundary in `SPEC.is-prime` is an exact
`Call(Name("is_prime"), (Int(N), .Exprs))`. The module scope binds that name to
the exact parameter list and statement body in `solution.mpy`. Thus lookup,
argument evaluation, parameter binding, frame allocation, every source
statement, return, and frame pop execute under the fixed semantics.

There is no input precondition: `N` ranges over all K integers.

The postcondition is:

```k
ensures ?R ==Bool primeResult(N)
```

where:

```text
primeResult(N) = false                 if N < 2
primeResult(N) = primeScan(N, 2)       if N >= 2
```

and `primeScan(N,D)` states that no integer in `[D,N)` divides `N`.

The loop circularity `SPEC.prime-loop` begins at the fixed semantics' actual
recurring `#while` term. With `D >= 2`, `D <= N`, `n = N`,
`divisor = D`, and `result = A`, it establishes:

```text
divisor = N
result  = A and primeScan(N,D)
```

The claim observes the returned Boolean and fixes the entry/final environment,
scope allocation, heap, stack, return state, exception state, and exit code.
The loop claim preserves its framed continuation, caller module map, and caller
frame item. Output, files, networking, and other external state do not exist in
the active semantics for this program.

## Proof-extension inventory

### `primeScan(Int, Int)`

- Extension: the four equations at `verification.k:12-24`.
- Class: definitional summary.
- Semantic role: names a mathematical Boolean; it never matches or replaces a
  Python expression, statement, call, loop, continuation, or configuration.
- Domain: all integer pairs. `D < 2` is totalized to `false`. For `D >= 2`,
  the cases are `D >= N`, or `D < N` split by `pyMod(N,D) == 0` versus
  `pyMod(N,D) != 0`.
- Matched context: only the term `primeScan(N,D)`; there are no cells,
  continuations, bindings, frames, or wildcards.
- Justification scope and context containment: exactly the same term/guard
  domains as the equations. The four guards are exhaustive and pairwise
  disjoint. Remainder is defined in every recursive case because `D >= 2`.
- State footprint: none.
- Value influence: determines the loop's final `result` binding and the entry
  claim's returned Boolean.
- Value justification: the base case describes an empty interval; a divisor
  makes the result false; otherwise removing the lower non-divisor changes the
  lower bound from `D` to `D + 1`. The recursion descends on the finite measure
  `N - D` in its only proof-relevant domain, `2 <= D < N`.
- Dependents: `SPEC.prime-loop`, `primeResult`, and `SPEC.is-prime`.
- Control validation: not applicable; this summary performs no control step.
- Value validation: the circularity proves the fixed loop computes it.
  Ground witnesses include `4 -> false`, `11 -> true`, and `13441 -> true`.
  The body mutation and false-result probes both reject the opposite result.
- Validation: Gate A equation coverage/descent checks pass; the LLVM
  differential run reports zero mismatches.

### `primeResult(Int)`

- Extension: the two equations at `verification.k:26-30`.
- Class: definitional summary.
- Semantic role: names the expected entry-point result and replaces no
  execution.
- Domain: all integers, split disjointly and exhaustively at `N < 2` /
  `N >= 2`.
- Matched context: only `primeResult(N)`.
- Justification scope and context containment: identical to those two guards.
- State footprint: none.
- Value influence: constrains the returned Boolean in `SPEC.is-prime`.
- Value justification: integers below two are not prime; all other integers
  are characterized by `primeScan(N,2)`.
- Dependents: `SPEC.is-prime`.
- Control validation: not applicable.
- Value validation: fixed execution proves the equality for symbolic `N`;
  the `N = 2` false-postcondition mutation is rejected.
- Validation: all Gate A/B/C checks pass.

### `SPEC.prime-loop`

- Extension: the auxiliary reachability claim at `spec.k:6-40`.
- Class: derived lemma / loop circularity.
- Semantic role: proves the fixed `#while` execution; it is not an ordinary K
  rule and does not preempt a fixed-semantics step.
- Domain: `D >= 2 andBool D <= N`.
- Matched context: the exact loop condition and body at `#while`, an arbitrary
  framed K suffix, `env = 1`, module scope `M`, the exact local bindings
  `n/divisor/result`, `scopeLoc = 2`, empty heap, one framed stack item,
  `noRet`, `NoExc`, and exit code zero.
- Justification scope: the machine-checked claim quantifies over the same
  `M`, stack item, Boolean accumulator, integers, and K suffix.
- Context containment: every frame accepted by the circularity is quantified
  by the claim itself; no narrower continuation theorem is generalized into a
  broader rewrite.
- State footprint: reads `n`, `divisor`, and `result`; writes `divisor` and
  possibly `result`; preserves the module map, environment, scope allocation,
  heap, heap allocation counter, caller stack item, return state, exception,
  exit code, and continuation.
- Value influence: establishes the accumulator/remaining-interval result used
  by the entry claim.
- Value justification: fixed semantics executes the comparison, remainder,
  branch, assignment, increment, and loop re-entry. `primeScan` supplies only
  the corresponding mathematical recurrence.
- Dependents: `SPEC.is-prime`.
- Control validation: the loop body contains no `return`, `break`, `continue`,
  exception, allocation, or external effect. The claim proves the exact
  `#while` control configuration and preserves the arbitrary suffix.
- Value validation: base, divisor, and non-divisor paths close in the combined
  `#Top` proof. A mutated source body is rejected.
- Validation: Gate A passes.

There are no proof-local operational bridges, trusted primitives, opaque
result-bearing symbols, `[simplification]` axioms, `[concrete]` proof rules, or
priority rules.

## Exact commands and actual results

The complete reproducible command sequence is in `prove.sh`. It was run as:

```bash
./prove.sh
```

Actual overall result:

```text
exit 0
```

The positive target-proof commands were:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual target-proof output and status:

```text
#Top
exit 0
```

The LLVM definition and concrete exercise used:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled
```

The result list was:

```text
[false, false, false, true, true, false, false,
 false, true, false, true, true, true]
```

for inputs:

```text
[-7, 0, 1, 2, 3, 4, 6, 9, 11, 25, 61, 101, 13441]
```

The body-sensitivity command was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result:

```text
exit 1
WarnStuckClaimState
final <k>: false ~> .K
```

The mutation changes `result = True` to `result = False`; the satisfiable
witness is `N = 2`, for which the expected result is `true`.

The false-postcondition command was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result:

```text
exit 1
WarnStuckClaimState
final <k>: true ~> .K
```

This probe deliberately demands `false` for the original body at `N = 2`.

The independent differential command was:

```bash
python3 differential_test.py
```

Actual output:

```text
inputs=1102 range=-100..1000 extras=[13441]
cpython_mismatches=0
k_mismatches=0
```

The script executes LLVM/K in batches of at most 100 inputs to stay below the
memory limit. Its independent oracle tests trial divisors only through
`math.isqrt(n)` and does not import or restate the K proof equations.

## Gate results

### Gate A — PASS

- A1: `SPEC.is-prime` binds `is_prime` to the exact translated closure body;
  the body executes under fixed semantics. Regenerating with
  `python3 py2mpy.py solution.py` exactly matches `solution.mpy`. The material
  body mutation fails with exit 1.
- A2: no operational bridge skips state or control. The exact entry
  configuration and loop state footprint are stated above.
- A3: lookup selects the exact closure binding; the fixed call semantics
  evaluates the argument, binds `n`, allocates/pops the frame, and preserves
  the caller state. The loop circularity is proved for the complete framed
  suffix it accepts.
- A4: `primeScan` and `primeResult` have exhaustive, disjoint guards.
  Recursive descent is by increasing `D` while `D < N`; remainder divisors are
  nonzero. No false or overlapping proof rule was found.
- A5: `N = 2` realizes the entry configuration. The result is constrained, and
  both the false-postcondition and body mutations are rejected.

### Gate B — PASS

- Input domain: all mathematical integers. This matches the integer primality
  domain implied by the prompt and all supplied examples. Non-integer Python
  values are outside the theorem.
- Language model: K integers are unbounded, matching CPython integers for this
  task. Every remainder uses a positive divisor, so supplied `pyMod` agrees
  with Python `%`. The program uses no feature outside the modeled subset.
- Summary-to-property: for `N >= 2`, `primeScan(N,2)` is true exactly when no
  proper positive divisor exists. That is the standard primality criterion.
- Implementation-to-intent: the implementation returns false below two and
  tests every candidate proper divisor otherwise, matching the prompt.

The formal result is partial correctness; machine-checked liveness is excluded
as required by the Kit workflow.

### Gate C — PASS

- Every proof-local extension and every trusted base is listed here.
- `prove.sh`, both mutation specs, concrete test artifacts, differential test,
  and output logs exist in the workspace.
- Commands, input scopes, oracle construction, outputs, and exit statuses are
  reproducible.
- Finite tests are reported only as empirical evidence, not as universal
  proof.

## Trust boundary

- The supplied, read-only `reference-semantics/` modules are trusted to model
  the intended Python subset. They affect all execution and proof claims.
- The supplied `py2mpy.py` translator is trusted to transliterate CPython ASTs
  as documented. `solution.mpy` was regenerated from `solution.py`.
- K v7.1.293, its Haskell/LLVM backends, SMT reasoning, and the host runtime
  are trusted.
- The proof-local summary equations are audited mathematical definitions, not
  trusted external primitives. There is no program-derived oracle or
  execution-bypassing rule.

## Empirically supported facts

- LLVM execution agrees with the 13 boundary/example/composite values listed
  above.
- LLVM/K and CPython execution both agree with the independent square-root
  trial-division oracle on all integers from `-100` through `1000`, plus
  `13441`: 1,102 total inputs and zero mismatches.
- These finite runs support translator/semantics adequacy on the tested inputs;
  the universal result comes from `kprove`, not from testing.

## Excluded behavior

- Non-`Int` K/Python inputs, including floats, strings, collections, and K
  `Bool` values, are outside the formal domain.
- The theorem starts at the clean entry configuration with the exact closure
  already bound; module-definition loading and arbitrary surrounding caller
  heaps/scopes are not part of the claim.
- Termination and resource bounds are not K reachability conclusions.
- Behavior outside the supplied Python subset or under a different Python
  semantics is not claimed.
