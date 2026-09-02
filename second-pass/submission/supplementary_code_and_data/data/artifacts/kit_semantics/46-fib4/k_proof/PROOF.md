VALIDATED

## What is proven

For every mathematical K integer `N >= 0`, under the supplied MPY semantics,
the exact translated `fib4` closure in `solution.mpy`, when invoked with `N`,
returns `fib4Spec(N)`.  `fib4Spec` is defined by the prompt's base values
`0, 0, 2, 0` and its four-term recurrence.

This is a partial-correctness reachability proof: it proves the returned value
for terminating executions in the stated domain.  It does not claim a separate
machine-checked liveness or asymptotic-complexity theorem.

## Formal claim and scope

- Program boundary: `Call(Name("fib4"), Int(N))` with name lookup pinned to the
  exact translated closure body in `spec.k`.  Module loading and the correctness
  of `py2mpy.py` itself are outside the reachability claim.
- Input domain: unbounded K integers satisfying `N >=Int 0`.
- Observable final state: the returned `<k>` value is `fib4Spec(N)`.  The entry
  claim also fixes and preserves the caller environment, module/builtin scopes,
  scope allocator, empty heap, heap allocator, empty stack, return state,
  exception state, and exit code.  The callee's local scope is deallocated by
  the supplied call semantics.
- Intended property: `fib4Spec(0..3) = 0, 0, 2, 0`, and for `N >= 4`,
  `fib4Spec(N)` is the sum of the preceding four values.
- Intentionally unobserved state: the loop claim existentially frames the final
  local values of `b`, `c`, `d`, and `e`; the entry point returns only `a`, and
  the supplied semantics deallocates all of those locals on return.

The loop-head invariant is:

```text
0 <= I <= N
i = I
a = fib4Spec(I)
b = fib4Spec(I + 1)
c = fib4Spec(I + 2)
d = fib4Spec(I + 3)
```

One body execution shifts these four values left, sets the new `d` to their
sum, and increments `i`.  The `fib4Spec(I + 4)` recurrence re-establishes the
invariant.  When the guard is false, `I <= N` and `not(I < N)` imply `I = N`,
so `a = fib4Spec(N)`.  Instantiating the invariant at `I = 0` discharges the
whole function claim.

## Proof-extension inventory

### `fib4Spec`

- Extension: the `[function, total]` symbol and five rules in
  `verification.k`.
- Class: definitional summary.
- Semantic role: names the requested mathematical sequence; it does not match,
  skip, intercept, or replace a program term.
- Domain: every K `Int`.  `N <= 0` is totalized to `0`; the target theorem uses
  only `N >= 0`.
- Matched context and state footprint: none; these are pure equations with no
  configuration cells.
- Justification scope and context containment: the guards `N <= 0`, exact
  cases `1`, `2`, `3`, and `N >= 4` are exhaustive and pairwise disjoint.
  Recursive calls strictly decrease positive `N`.
- Value influence: fixes the invariant values and the entry claim's returned
  value.
- Value justification: the equations are exactly the prompt's four base cases
  and recurrence (with an explicit, unused negative-input totalization).
- Dependents: `SPEC.loop-invariant` and `SPEC.fib4-correct`.
- Control validation: not applicable; no control or operational rule is added.
- Value validation: both positive claims close; K smoke tests cover distinct
  values including `0`, `2`, `4`, `8`, `14`, and `104`; the independent
  CPython oracle has zero mismatches on `0..200`.

### `SPEC.loop-invariant`

- Extension: the auxiliary reachability circularity at the exact internal
  `#while` head.
- Class: derived lemma (machine-checked auxiliary reachability claim).
- Semantic role: summarizes the fixed-semantics loop after proving its base and
  inductive cases; there is no ordinary rewrite or priority rule in
  `verification.k` that preempts execution.
- Domain: `I >= 0 andBool I <= N`, with an exact integer local scope containing
  `n`, `i`, `a`, `b`, `c`, `d`, and `e`.
- Matched context: the exact guard and exact six-statement body at the front of
  `<k>`, arbitrary trailing continuation, active environment `L`, exact active
  local map, arbitrary parent, and framed remaining scopes/configuration cells.
- Justification scope: the focused universal `kprove` command proves this same
  complete match domain using the supplied MPY rules and `fib4Spec`.
- Context containment: matched and justified domains are identical; the claim
  consumes only the loop and preserves the arbitrary continuation via
  `=> .K ...`.
- State footprint: `n` is preserved; `i` becomes `N`; `a` becomes
  `fib4Spec(N)`; final `b`, `c`, `d`, and `e` exist but are unobserved; every
  other cell is preserved.
- Value influence and justification: `a` becomes the entry result.  Its value
  follows from fixed assignment/arithmetic execution plus the exhaustive
  `fib4Spec` recurrence.
- Dependents: `SPEC.fib4-correct`.
- Control validation: the claim introduces no return, exception, frame pop,
  break, or continuation discard.
- Validation: the focused proof prints `#Top`; the full entry proof uses it;
  the material body mutation is rejected with actual result `3`.

### `SPEC.fib4-correct`

- Extension: the target reachability theorem.
- Class: derived reachability claim.
- Semantic role: executes fixed name lookup, argument evaluation, frame
  creation, all assignments, the loop, return, and frame pop.
- Domain and matched context: exact `fib4` binding/body, exact caller state, and
  `N >= 0`.
- Justification and dependents: closed by fixed MPY execution, the proved loop
  circularity, and `fib4Spec`; it is not used to justify another positive target
  theorem.
- State/control/value validation: all caller-visible cells are constrained; the
  false-result mutation and body mutation both fail.

There are no simplification lemmas, opaque values, trusted primitives,
operational bridges, problem-local priority rules, or concrete-only proof rules.

## Exact commands and actual outputs

The recorded runner is `./prove.sh`; its final execution exited `0`.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 -m py_compile solution.py smoke.py test_solution.py
head -n 17 smoke.py | cmp solution.py -
```

Actual result: all commands exited `0`; `cmp` produced no output.

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Actual result: exit `0`.  The compiler printed supplied-semantics warnings about
several unrelated non-exhaustive helpers and unused string-rule variables.

```bash
krun smoke.mpy --definition runtime-kompiled
```

Actual result: exit `0`, final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`.  All assertions in `smoke.py` therefore passed.

```bash
python3 test_solution.py
```

Actual output and exit:

```text
domain: n = 0..200
oracle: direct prompt recurrence with stored prefix
mismatches: 0
Exit: 0
```

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
```

Actual result: exit `0`; only supplied `str.k` unused-variable warnings were
printed.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
```

Actual proof result:

```text
#Top
Exit: 0
```

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual proof result:

```text
#Top
Exit: 0
```

False-result non-vacuity probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1` with `WarnStuckClaimState`; its residual contains:

```text
<k>
  0 ~> .K
</k>
```

The mutation demanded `1` at the satisfiable witness `n = 0`.

Body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1` with `WarnStuckClaimState`; its residual contains:

```text
<k>
  3 ~> .K
</k>
```

The mutation changed the initializer `c = 2` to `c = 3` and still demanded the
original result `2` at `n = 2`.

## Gate results

### Gate A — PASS

- A1: the entry claim pins name lookup to the complete translated closure body;
  fixed semantics executes it.  The body mutation is rejected.
- A2/A3: no operational bridge exists.  Lookup, argument order, arithmetic,
  sequential assignments, loop control, return, frame pop, and caller state are
  handled by the supplied semantics.  The circularity preserves its arbitrary
  continuation and does not add abrupt control.
- A4: `fib4Spec` has exhaustive, disjoint guards and descending recursion.
- A5: `n = 0` satisfies the precondition; the returned value is constrained;
  the false-result mutation exits `1` with actual result `0`.

### Gate B — PASS

- The formal `N >= 0` domain matches the indices for which the prompt defines
  Fib4.
- K integers and the relevant supplied rules model the program's unbounded
  integer arithmetic, comparison, sequential assignment, loop, and function
  behavior without a material discrepancy for this program.
- The formal postcondition uses the prompt's base cases and recurrence directly,
  rather than an unrelated or opaque execution oracle.
- The implementation is iterative and contains no recursive call, as required.

### Gate C — PASS

- Every assumption is listed below with its dependents.
- `smoke.py`, `smoke.mpy`, `test_solution.py`, `spec-vacuity.k`, and
  `spec-body-mutation.k` exist; their commands, scopes, oracles, and actual
  results are recorded above.
- The LLVM smoke artifact's first 17 lines are byte-identical to `solution.py`
  and add only assertions.
- Finite testing is reported only as evidence; universal program-to-recurrence
  correspondence comes from the positive reachability proof.

## Trust boundary

- Supplied `reference-semantics/`: trusted as the fixed model of the relevant
  Python subset.  Both positive claims depend on it.
- Supplied `py2mpy.py`: trusted to transliterate the accepted CPython AST
  constructors faithfully.  `solution.mpy` is regenerated by `prove.sh`, and
  the exact constructor body is pinned in the entry claim.
- K v7.1.293, its Haskell/LLVM backends, SMT reasoning, and host execution:
  trusted proof/execution infrastructure.  All formal and empirical results
  depend on the relevant components.
- Ordinary mathematical reading of nonnegative sequence indices: used to align
  the prompt's “n-th element” wording with the formal `N >= 0` domain.

No unproved program-local primitive or opaque result affects the theorem.

## Empirically supported facts

- `smoke.py` checks K execution at `n = 0, 1, 2, 3, 5, 6, 7, 10` against fixed
  expected values and finishes with no exception.
- `test_solution.py` independently builds the sequence from the prompt's stored
  prefix recurrence and compares the actual CPython `solution.fib4` result for
  every `n` in `0..200`; mismatch count is zero.
- These tests support translator/semantics/CPython alignment on their finite
  inputs; they do not replace the universal K proof.

## Excluded behavior

- Negative indices, non-integer arguments, Python subclass/boolean corner
  cases, and behavior outside the supplied MPY subset are outside the theorem.
- Correctness of module loading and a general proof of `py2mpy.py` are outside
  the reachability claim.
- Termination, time complexity, memory complexity, and integer resource limits
  are not separately formalized.  Inspection shows one incrementing loop and a
  constant number of integer locals, but that observation is not a K theorem.
