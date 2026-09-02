VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, for every K integer `N0 >= 2`,
loading the exact translated `largest_prime_factor` function and calling it with
`N0` returns an integer equal to `lpfFrom(N0, 2)`. The function lookup,
argument evaluation, call-frame creation, loop, local assignments, return,
frame pop, and final result all execute through the fixed semantics.

The source prompt assumes the smaller domain where `N0` is composite. The K
claim proves the execution summary on the broader domain `N0 >= 2`, which
contains every prompt input. A separate number-theoretic argument below
establishes that `lpfFrom(N0, 2)` is the largest prime factor of `N0`.

`kprove` establishes partial correctness. Termination on `N0 >= 2` is justified
separately by the well-founded measure described below.

## Formal claim

The target claim `SPEC.entry` starts from the standard empty module
configuration, loads the `FuncDef` term appearing in `solution.mpy`, and calls
the selected binding:

```text
Call(Name("largest_prime_factor"), Int(N0), .Exprs)
```

Its precondition and result postcondition are:

```text
requires N0 >=Int 2
ensures  ?RESULT ==Int lpfFrom(N0, 2)
```

The auxiliary circularity `SPEC.loop` starts at the exact internal `#while`
configuration produced inside that call, including the concrete continuation
`Return(Name("n")) .Stmts ~> #endcall ~> .K`, caller frame, environments, and
all configuration cells. For symbolic local values `N` and `F`, with
`F >=Int 2`, it returns `lpfFrom(N, F)`.

The three equations defining the summary are:

```text
lpfFrom(N,F) = N                         if F >= 2 and N <= F
lpfFrom(N,F) = lpfFrom(N / F,F)          if F >= 2, N > F, and N % F = 0
lpfFrom(N,F) = lpfFrom(N,F + 1)          if F >= 2, N > F, and N % F != 0
```

The division equation uses the reference semantics' exact positive-integer
form `(N - pyMod(N,F)) /Int F`.

## Proof-extension inventory

### `lpfFrom` and its three equations

- **Class:** Definitional summary.
- **Semantic role:** Names the mathematical value of the loop; it does not
  match or replace any program term.
- **Domain:** All integer pairs with `F >= 2`. The three guards are pairwise
  disjoint and cover this domain.
- **Matched context:** Only terms of the form `lpfFrom(N,F)` in claim
  postconditions. No continuation, binding, control stack, or state cell is
  matched.
- **Justification scope and containment:** Exactly the stated domain. The exit,
  divisible, and non-divisible equations reproduce the three source-level loop
  cases. Every use in `spec.k` has `F >= 2`.
- **State footprint:** None.
- **Value influence:** Determines the returned integer constrained by both
  positive claims.
- **Value justification:** Exhaustive guarded equations. Recursion terminates
  lexicographically: increment keeps `N` and decreases `N-F`; division occurs
  only for `N > F >= 2` and strictly decreases `N`.
- **Dependents:** `SPEC.loop` and `SPEC.entry`.
- **Control/value validation:** Fixed execution was retained. The ground false
  postcondition in `SPEC-NEGATIVE.false-post` was rejected with actual result
  `2`, and the independent differential test reported zero mismatches.

### `SPEC.loop`

- **Class:** Derived lemma (a proved reachability circularity).
- **Semantic role:** Symbolically executes the real loop and exact return
  continuation. It is not an ordinary rewrite rule and does not preempt the
  semantics.
- **Domain:** Symbolic `N:Int`, `F:Int`, with `F >= 2`.
- **Matched context:** Exact loop syntax, exact function closure and binding,
  `env = 1`, local scope at location 1, `scopeLoc = 2`, empty heap, caller
  frame `frame(.K,0,1)`, `noRet`, `NoExc`, and exit code 0.
- **Justification scope and containment:** The claim proves the same complete
  configuration it accepts. The entry trace reaches this exact configuration.
- **State footprint:** Reads and writes the local `n` and `factor` bindings;
  returns a value; restores environment 0; removes scope 1; restores
  `scopeLoc` to 1; pops the stack; preserves the empty heap, heap location,
  exception, and exit-code cells.
- **Value influence:** Its result supplies the result of `SPEC.entry`.
- **Value justification:** The `lpfFrom` equations above.
- **Dependents:** `SPEC.entry`.
- **Validation:** The focused loop proof and complete proof set both printed
  `#Top`. Changing the immediate continuation shape prevented claim reuse
  during construction; the final claim uses the exact continuation emitted by
  the fixed semantics.

There are no operational bridges, priority rules, opaque result symbols,
trusted proof-local primitives, or execution-bypassing rewrites in
`verification.k` or `spec.k`.

## Exact commands and observed outputs

The reproducible command sequence is in `prove.sh`.

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Observed exit: 0. The generated term is a single
`Module(FuncDef("largest_prime_factor", ...))` with the factor initialization,
while loop, conditional division/increment, and return from `solution.py`.

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Observed exit: 0. The compiler printed supplied-semantics warnings about
unrelated non-exhaustive helper matches and unused string-rule variables.

```bash
krun concrete-tests.mpy --definition runtime-kompiled
```

Observed exit: 0. The final `<k>` cell was `.K`; the module scope contained:

```text
"example_13195" |-> 29
"example_2048"  |-> 2
"boundary_4"    |-> 2
```

The final environment was 0, heap and stack were empty, return state was
`noRet`, exception state was `NoExc`, and exit code was 0.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Observed exit: 0. The only warnings were unused variables in supplied
`reference-semantics/semantics/str.k` rules.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop
```

Observed output: `#Top`. Observed exit: 0.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Observed output: `#Top`. Observed exit: 0. This is the positive target-proof
command covering every claim in `spec.k`.

```bash
python3 differential_test.py
```

Observed output:

```text
cases=4331 mismatches=0
```

Observed exit: 0.

```bash
kprove spec-negative.k \
  --definition verification-kompiled \
  --spec-module SPEC-NEGATIVE \
  --claims SPEC-NEGATIVE.false-post
```

Observed exit: 1 with `WarnStuckClaimState`; the residual final `<k>` value was
`2 ~> .K`, contradicting the mutated postcondition `RESULT == 3`.

```bash
kprove spec-negative.k \
  --definition verification-kompiled \
  --spec-module SPEC-NEGATIVE \
  --claims SPEC-NEGATIVE.body-mutation
```

Observed exit: 1 with `WarnStuckClaimState`; after changing the initialized
factor from 2 to 3, the residual final `<k>` value was `4 ~> .K`, contradicting
the original expected value 2.

## Gate results

### Gate A — PASS

- **A1:** `SPEC.entry` contains the exact translated function body and fixed
  binding. The body executes normally. The material factor-initialization
  mutation is rejected and changes the result from 2 to 4 for input 4.
- **A2:** No execution is skipped. The claims account for the result,
  environments, scopes, heap, allocation counter, stack, return state,
  exception state, and exit code.
- **A3:** Fixed rules perform name lookup, left-to-right call evaluation,
  operator dispatch, loop control, return, and frame restoration. There is no
  operational bridge requiring a connection theorem.
- **A4:** The `lpfFrom` guards are disjoint and exhaustive over every use
  (`F >= 2`), division is guarded by nonzero `F`, and the recursion has a
  well-founded lexicographic descent.
- **A5:** Input 4 realizes the precondition. The false result mutation was
  rejected with an explicit result-2 residual.

### Gate B — PASS

- **B1:** The formal input domain `N0 >= 2` is broader than the prompt's
  composite-only domain, so it does not exclude a required input.
- **B2:** For this program, K `Int` arithmetic models Python's unbounded
  integers; every divisor is at least 2, so modulo and floor division cannot
  divide by zero. No collection, text, I/O, or implementation-defined behavior
  is involved.
- **B3:** The execution summary and human-facing property are distinct. Their
  connection follows from the following number-theoretic invariant at every
  reachable loop head, where `X` is the original input:
  `n >= factor >= 2`; no integer in `[2,factor)` divides `n`; and the largest
  prime factor of `n` equals that of `X`.

  Initially the claims are immediate. If `factor` does not divide `n`,
  incrementing it establishes the larger excluded-divisor interval. If it
  divides `n`, the excluded-divisor invariant makes `factor` prime. Writing
  `n = factor*q`, the same invariant forces `q >= factor`; otherwise `q` would
  be a forbidden smaller divisor. Replacing `n` by `q` therefore removes no
  largest prime factor and preserves the excluded-divisor invariant. At loop
  exit, `n <= factor` combines with `n >= factor` to give `n = factor`; the
  absence of smaller divisors makes this value prime, and the preserved
  largest-factor invariant makes it the largest prime factor of `X`.

  This is a formal paper-level derivation over standard integer divisibility;
  K machine-checks the execution-to-`lpfFrom` part. The independent differential
  oracle supplies finite corroboration, not universal proof.
- **B4:** The implementation, recursive summary, examples, and source contract
  agree.

The same invariant gives termination: while the guard is true, an increment
decreases `n-factor`, while a division strictly decreases `n`; ordered
lexicographically by `(n, n-factor)`, these nonnegative measures cannot descend
forever.

### Gate C — PASS

- **C1:** The trust ledger below names every component outside the target K
  theorem and its influence.
- **C2:** All claimed concrete, differential, false-postcondition, and
  body-mutation evidence has an existing artifact, exact command, input scope,
  oracle, and observed result.
- **C3:** This report separates K-checked partial correctness, the standard
  number-theoretic adequacy argument, finite testing, and excluded behavior.

## Trust boundary

- **Supplied `reference-semantics/`:** Trusted as the task's fixed model of the
  Python subset. Its operator, control, function-call, and configuration rules
  affect value, state, control, and exceptions for both positive claims.
  Evidence: successful concrete execution of the supplied examples and the
  body-sensitive negative probes.
- **`py2mpy.py`:** Trusted fixed AST transliterator supplied by the task. It
  determines the program term. Evidence: `solution.mpy` is regenerated by
  `prove.sh`, and the entry claim contains the same constructor tree.
- **K Haskell backend and its SMT reasoning:** Trusted proof engine for `#Top`.
- **Standard integer number theory:** The Fundamental Theorem of Arithmetic and
  elementary divisibility facts support the summary-to-largest-prime-factor
  argument. This bridge affects the human-facing interpretation of the result,
  not fixed-semantics execution. It is derived explicitly above and
  independently tested; it is not encoded as another K reachability claim.

No proof-local trusted primitive or unproved operational bridge is present.

## Empirically supported facts

- `concrete-tests.py` is independently translated to `concrete-tests.mpy` and
  run on the LLVM semantics. It covers both prompt examples and the smallest
  composite boundary case.
- `differential_test.py` imports the implementation but constructs its oracle
  independently by enumerating divisors and testing primality by trial
  division. Its complete scope is every composite integer from 2 through 5000,
  plus 13195: 4,331 cases, zero mismatches.
- `spec-negative.k` contains the exact two negative probes and preserves their
  nonzero K results.

These finite observations support semantics adequacy and catch mutations; they
do not replace the universal K reachability proof or the number-theoretic
argument.

## Excluded behavior

- Inputs below 2 and non-integer Python values are outside the formal
  precondition.
- The prompt excludes prime inputs, although the K theorem safely covers them
  and returns the prime itself.
- K proves partial correctness; termination is established by the separate
  well-founded-measure argument above rather than by `kprove`.
- Behavior of Python features absent from this implementation is irrelevant to
  the theorem.
