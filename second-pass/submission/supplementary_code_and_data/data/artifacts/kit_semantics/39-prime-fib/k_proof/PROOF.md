VALIDATED

# What is proven

For every K integer `N >= 1`, if the call to the exact `prime_fib` closure
terminates under the supplied `MPY` semantics, it returns
`primeFibSearch(N, 0, 0, 1)`.

`primeFibSearch(N, 0, 0, 1)` is the recursively characterized search that
starts from Fibonacci state `(0, 1)`, advances to `(B, A + B)`, increments its
count exactly when `B` passes trial division, and stops when the count reaches
`N`. Thus it denotes the N-th Fibonacci number that is prime.

This is a partial-correctness theorem. It does not prove termination or the
existence of arbitrarily many Fibonacci primes.

# Formal claims and scope

The program boundary begins immediately before
`Call(Name("prime_fib"), (Int(N), .Exprs))`. The module scope already contains
the exact translated closure body. Name lookup, argument evaluation, parameter
binding, frame creation, every assignment, both loops, return, frame pop, and
restoration of the caller configuration all execute under the supplied
semantics.

The formal input domain is K integers satisfying `N >=Int 1`. The observable
final state is the returned integer in `<k>`. Function-local variables are not
observed after return because the supplied call semantics pops the local scope.
The entry claim also fixes and restores the environment, scopes, scope
allocator, heap, heap allocator, stack, return state, exception state, and exit
code.

The three claims in `spec.k` are:

1. `SPEC.inner-loop`: the internal `#while` divisor loop leaves
   `is_prime = primeScan(A,D,P)`.
2. `SPEC.outer-loop`: the internal Fibonacci/search `#while` leaves
   `a = primeFibSearch(N,C,A,B)`.
3. `SPEC.prime-fib`: the exact function call returns
   `primeFibSearch(N,0,0,1)`.

# Proof-extension inventory

The `primeFibBody`, `primeFibOuter`, `primeFibInner`,
`primeFibOuterCore`, and `primeFibInnerCore` productions are compile-time
macros. They only expand to the constructors in `solution.mpy`; they add no
runtime or proof rewrite.

## `primeScan`

- Class: definitional summary, plus derived folding and absorption lemmas.
- Semantic role: reasons about the result of the divisor loop; it does not
  match or replace a Python or MPY execution term.
- Domain: the loop claims use `A >= 0` and `D >= 2`. The guarded equations
  split on `D*D > A`, divisibility at `D`, and non-divisibility at `D`.
- Matched context: summary terms only; no `<k>` continuation, bindings, or
  state cells are matched.
- Justification scope and containment: trial division checks every integer
  from `D` through `floor(sqrt(A))`. If the current divisor divides `A`, the
  flag is false. Otherwise the next scan has the same flag. Once false, the
  flag can never become true. Every equation is restricted to this domain.
- State footprint: none.
- Value influence: `primeScan` determines `is_prime`, the Boolean-as-integer
  count increment, and therefore the returned Fibonacci candidate.
- Value justification: the inner-loop reachability claim executes the actual
  multiplication, comparison, modulo, conditional assignment, and divisor
  increment, and connects the resulting flag to `primeScan`.
- Dependents: all three claims.
- Control validation: not applicable; these equations do not replace control.
- Value validation: the inner claim proves `#Top`; the false-result probe is
  rejected; the independent Python oracle agrees for `n=1..10`.
- Coverage and overlap: for `D >= 2`, either `D*D > A` or `D*D <= A`; in the
  second case the modulo is zero or nonzero. Overlaps with the false-flag
  absorption rule all yield false. Division by zero is excluded by `D >= 2`.

`primeScan(A,2,A>=2)` is exactly the usual trial-division definition. The
standard divisor-pair fact—every composite `A >= 2` has a factor no larger
than `sqrt(A)`—connects this definition to mathematical primality.

## `primeFibSearch`

- Class: definitional summary plus derived base, boundary, and fold lemmas.
- Semantic role: characterizes the remaining outer-loop search without
  replacing any source execution.
- Domain: `N >= 1`, `A >= 0`, and `B >= 1` on inductive uses. The base covers
  `C >= N`; the fold covers `C < N`; the boundary lemma covers the overlapping
  case where the next Boolean increment exits the loop.
- Matched context: summary terms only; no configuration cell is matched.
- Justification scope and containment: one source iteration changes
  `(C,A,B)` to `(C + primeBit(B), B, A+B)`, where `primeBit(B)` is the
  `#if primeScan(B,2,B>=2) #then 1 #else 0 #fi` term produced by the supplied
  integer-plus-Boolean rule. The fold lemma is this equality oriented toward
  the current summary. The boundary rule is the same step followed by the
  base case.
- State footprint: none.
- Value influence: it is the exact result constrained by the outer and entry
  claims.
- Value justification: the outer-loop claim executes the Fibonacci update,
  the proved inner loop, and the count update before applying its circularity.
- Dependents: `SPEC.outer-loop` and `SPEC.prime-fib`.
- Control validation: not applicable; no operational term is replaced.
- Value validation: prompt examples, an independent oracle for `n=1..10`, the
  false-result mutation, and the changed-body mutation.
- Coverage and overlap: `C >= N` and `C < N` cover integer counts. On the exit
  overlap, the fold followed by the base case and the boundary rule both
  produce `B`.

## Loop reachability claims used as staged lemmas

- Class: derived reachability lemmas/circularities.
- Semantic role: execute fixed-semantics loop steps and summarize their
  reached states. They are not ordinary rewrite rules in `verification.k`.
- Matched inner context: `primeFibInnerCore ~> KREST`, the active environment
  location, and the complete local map entries used by the loop. Other
  configuration cells and `KREST` are framed.
- Matched outer context: `primeFibOuterCore ~> KREST` with all function-local
  bindings. Other configuration cells and `KREST` are framed.
- Justification scope and containment: both loops contain only normal
  assignments and conditionals. They have no return, break, continue,
  exception, heap, stack, output, or frame-pop effect, so an arbitrary inactive
  suffix is preserved. The inner result needed by the outer continuation is
  constrained; auxiliary final locals are existential because the entry
  continuation observes only `a`.
- State footprint: the local scope map only. The environment location and all
  omitted cells are preserved.
- Dependents: the outer command stages the separately proved inner claim; the
  entry command stages the separately proved inner and outer claims.
- Validation: each staged claim has its own prior `#Top`/exit-0 command, so
  `--trusted` introduces no unproved lemma into the proof chain.

There are no operational bridges, result-bearing oracles, proof-local priority
rules, or trusted opaque primitives.

# Reproducible commands and actual results

The complete runner is:

```bash
./prove.sh
```

It exited 0. Its constituent commands are recorded verbatim in `prove.sh`.

Translation:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
```

Both exited 0. `solution.mpy` contains the exact nested-loop body represented
by the proof macros.

Independent executable evidence:

```bash
python3 test_solution.py
```

Actual output, exit 0:

```text
prompt examples: [2, 3, 5, 13, 89]
differential inputs: n=1..10
oracle values: [2, 3, 5, 13, 89, 233, 1597, 28657, 514229, 433494437]
mismatches: 0
```

Concrete LLVM build and execution:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Both exited 0. The final `krun` configuration had `<k> .K </k>`,
`"result" |-> 89`, `NoExc`, and exit code 0. The compiler printed only warnings
from the supplied reference semantics.

Symbolic definition:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
```

Actual result: exit 0, with only unused-variable warnings from the supplied
semantics.

Positive target 1:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop
```

Actual proof result: `#Top`, exit 0.

Positive target 2:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop \
  --trusted SPEC.inner-loop
```

Actual proof result: `#Top`, exit 0. The trusted label is exactly the claim
proved by positive target 1.

Positive target 3:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC.prime-fib \
  --trusted SPEC.inner-loop,SPEC.outer-loop
```

Actual proof result: `#Top`, exit 0. The trusted labels are exactly the claims
proved by positive targets 1 and 2.

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC-VACUITY.false-result \
  --trusted SPEC.inner-loop,SPEC.outer-loop
```

Actual result: exit 1 with `WarnStuckClaimState`. The residual contains:

```text
primeFibSearch(N, 0, 0, 1)
```

versus the false destination:

```text
primeFibSearch(N, 0, 0, 1) +Int 1
```

Body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC.inner-loop,SPEC.outer-loop,SPEC-BODY-MUTATION.changed-initial-b \
  --trusted SPEC.inner-loop,SPEC.outer-loop
```

Actual result: exit 1 with `WarnStuckClaimState`. Changing only the initial
`b = 1` to `b = 2` produces
`primeFibSearch(N,0,0,2)`, which does not satisfy the original
`primeFibSearch(N,0,0,1)` destination.

# Gate results

## Gate A — PASS

- A1: the exact program-defined body executes. The changed-body mutation is
  rejected.
- A2: there is no operational bridge. The entry claim restores every
  nonlocal configuration cell; unobserved function locals are removed by the
  fixed frame-pop rule.
- A3: fixed semantics performs lookup, argument evaluation, binding, ordering,
  loop control, return, and frame pop. No abrupt control is abstracted.
- A4: summary equations are guarded, their cases cover every use, their
  overlaps agree, divisor recursion progresses because `D` increases, and
  modulo uses only `D >= 2`.
- A5: `N=5` is a realizable witness; LLVM execution returns 89. The
  false-result mutation is rejected.

## Gate B — PASS

- The formal domain `N >= 1` matches the positive ordinal implied by “N-th”
  and the `int` annotation.
- The supplied semantics uses mathematical integers, matching CPython's
  unbounded integer behavior for this program.
- The Fibonacci-state update and trial-division definition directly express
  the requested property, and all five prompt examples agree.
- The theorem is intentionally partial correctness; termination and the
  existence of arbitrarily many Fibonacci primes are excluded rather than
  claimed.

## Gate C — PASS

Trust ledger:

- The supplied read-only `reference-semantics/` is the fixed language model.
- K v7.1.293, its Haskell/LLVM backends, the SMT solver, and integer hooks are
  trusted tooling.
- The standard divisor-pair theorem connects trial division through
  `sqrt(A)` to mathematical primality.
- Staged `--trusted` labels are not residual assumptions: each exact claim is
  proved by an earlier recorded positive command.
- Unused opaque facilities imported by the broad reference `MPY` module do
  not occur on any proof path or in any postcondition.

All claimed executable evidence has an existing artifact and an exact command.
The finite differential test is evidence for `n=1..10`, not a substitute for
the universal reachability proof. Formal, conditional, empirical, and excluded
facts are separated above.

# Excluded behavior

- Inputs outside K integers `N >= 1`.
- A total-correctness or termination theorem.
- A theorem that infinitely many Fibonacci primes exist.
- Behavior under Python features not modeled by the supplied MPY semantics.
