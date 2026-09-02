VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every mathematical integer `N >= 0`,
if calling the exact `fib` closure translated from `solution.py` terminates,
its partially-correct result is:

```k
fibFrom(0, 1, N)
```

in `<k>`.  `fibFrom(A,B,N)` is the first component after `N` applications of
the standard Fibonacci state transition `(A,B) -> (B,A+B)`.  Thus
`fibFrom(0,1,N)` is the zero-indexed `N`-th Fibonacci number.

This is a partial-correctness reachability result: termination is not a
separate liveness theorem.  The entry claim also fixes and restores the caller
environment, module scope, scope allocator, empty heap, stack, return state,
exception state, and exit code shown in `spec.k`.

## Formal claims

- `SPEC.loop-inv`: from a loop head with local values `n=N`, `a=A`, and
  `b=B`, where `N >= 0`, the fixed loop semantics reaches `n=0` and
  `a=fibFrom(A,B,N)`.  The final local `b` is existential because that local
  frame is deallocated on return and its value is not observable.
- `SPEC.fib-call`: with `"fib"` bound to the exact parameter list and body from
  `solution.mpy`, `Call(Name("fib"), Int(N))` reaches
  `fibFrom(0,1,N)` for every `N >= 0`.

The three proof obligations are: the `N=0` loop base case; the `N>0` step,
which changes `(A,B,N)` to `(B,A+B,N-1)`; and the entry discharge from
`(A,B)=(0,1)`.  The complete `kprove` run closes all three.

## Proof-extension inventory

This inventory was rebuilt from `verification.k` and `spec.k`.

### `fibFrom(Int,Int,Int)` and its two equations

- Class: definitional summary.
- Semantic role: names a mathematical value in claims; it never matches or
  replaces a Python term, call, loop, continuation, or configuration.
- Domain: all K `Int` triples.  `N <= 0` returns `A`; `N > 0` recurses on
  `(B,A+B,N-1)`.  The guards are disjoint and exhaustive, and recursion
  strictly decreases positive `N`.
- Matched context / containment: only `fibFrom` terms, with no configuration
  cells or continuation.  Its use is contained in the stated equation domain.
- State footprint: none.
- Value influence: it specifies the final `a` and returned result.
- Value justification: exhaustive defining equations plus the bridge-free
  `SPEC.loop-inv` and `SPEC.fib-call` connection claims, both proved by
  executing the fixed semantics.
- Dependents: both positive claims.
- Control/value validation: K examples produce distinct results for
  `0,1,2,8,10`; the opposite result `fib(0)=1` is rejected by
  `spec-vacuity.k`.

### `(A +Int B) -Int A => B [simplification]`

- Class: derived lemma.
- Semantic role: simplifies the integer equality exposed after executing the
  two assignments; it does not replace execution.
- Domain: all mathematical K integers, without a guard.  It is the additive
  group identity `(A+B)-A=B`.
- Matched context / containment: any occurrence of exactly that integer term;
  the justification is equally universal.
- State footprint: none.
- Value influence: permits the loop step's new `a` to match `B`.
- Dependents: `SPEC.loop-inv`, and transitively `SPEC.fib-call`.
- Validation: the initial bridge-free proof residual contained exactly
  `fibFrom(A+B-A,A+B,N-1) = fibFrom(B,A+B,N-1)`; after adding this identity
  the loop and complete spec both print `#Top`.

### `SPEC.loop-inv`

- Class: derived auxiliary reachability claim (the loop circularity).
- Semantic role: establishes and then reuses the exact loop execution theorem;
  it introduces no ordinary rewrite rule.
- Domain: exact `#while` condition/body, environment `1`, an exact local
  `n/a/b` scope, arbitrary preserved outer scope `SC`, arbitrary preserved
  continuation, and `N >= 0`.
- Matched context / containment: its use in the entry proof reaches precisely
  that loop, local scope, environment, and body.  The continuation frame is
  preserved by the loop and is quantified equally on both sides.
- State footprint: reads/writes local `n`, `a`, and `b`; preserves outer
  scopes, control continuation, and every omitted completed configuration
  cell.  It abstracts only final local `b`.
- Value influence: fixes final local `a`; the entry's real return then reads
  that value under the fixed semantics.
- Justification and dependents: base/step symbolic execution under `MPY`,
  printing `#Top`; used by `SPEC.fib-call`.
- Control/value validation: no return, pop, exception, or continuation is
  introduced by a proof rule.  The fixed semantics executes the loop and the
  subsequent fixed return/frame-pop rules.

There are no operational bridges, trusted primitives, opaque result oracles,
priority rules, call interceptions, or execution-bypassing ordinary rewrites
in the proof extension.

## Commands and actual results

`prove.sh` contains the exact reproducible sequence.  The recorded end-to-end
run exited 0.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 differential_test.py
```

Actual differential output, exit 0:

```text
cases=0..30
mismatches=0
```

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled --output none
```

Actual result: both commands exited 0, and the runner printed
`KRUN_TESTS_PASSED`.  The compiler also printed pre-existing
non-exhaustiveness/unused-variable warnings from the supplied semantics.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-inv
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual results:

```text
loop-inv: #Top   exit 0
all claims: #Top exit 0
```

The Haskell build and proof parsing also printed only pre-existing unused
variable warnings from `reference-semantics/semantics/str.k` plus harmless
unused-frame/existential warnings for `SC` and `?BFinal` in `spec.k`.

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual results:

```text
false postcondition: exit 1, WarnStuckClaimState, actual <k> result 0
mutated body:       exit 1, WarnStuckClaimState, actual <k> result 1
```

`prove.sh` checks these non-zero exits and prints
`EXPECTED_FAILURE: false-postcondition probe` and
`EXPECTED_FAILURE: body-mutation probe`.

## Gate results

### Gate A — PASS

- A1: the entry claim pins the exact `"fib"` binding, parameter, body,
  argument, module parent, and environment.  All lookup, call, body, loop,
  return, and frame-pop behavior executes under `MPY`.  Changing `a = 0` to
  `a = 1` makes the original ground result claim fail.
- A2/A3: there is no operational bridge.  The entry claim explicitly observes
  the returned value and all configuration cells relevant to call control and
  state restoration.
- A4: `fibFrom` guards are disjoint/exhaustive and decrease; the sole algebraic
  lemma is universally valid.
- A5: `N=0` is a realizable pre-state.  The deliberately false result `1` is
  rejected with the residual actual result `0`.

### Gate B — PASS

- Formal domain: K integers `N >= 0`, matching the natural-number domain of an
  `N`-th Fibonacci number.  Negative integers, booleans, and non-integers are
  excluded.
- K integers and CPython integers are both unbounded mathematical integers for
  all operations used here.  The implementation has no I/O, collections,
  exceptions on the formal domain, or implementation-defined arithmetic.
- `fibFrom(0,1,N)` uses the canonical consecutive-Fibonacci initialization and
  recurrence.  Prompt examples `fib(1)=1`, `fib(8)=21`, and `fib(10)=55`
  execute successfully in both the K test fixture and CPython.
- The implementation and the formal postcondition agree on the stated domain.

### Gate C — PASS

The trust ledger is explicit:

- The supplied read-only `reference-semantics/` is the language-model trust
  base for every claim.
- K v7.1.293, its Haskell/LLVM backends, SMT reasoning, and host integer hooks
  are trusted for compilation, execution, and proof checking.
- The fixed `py2mpy.py` translator is trusted for source-to-constructor
  transliteration; regeneration is part of `prove.sh`, and the exact emitted
  body is pinned in `SPEC.fib-call`.
- The elementary integer simplification lemma is an admitted proof equation,
  audited above over its complete domain.

Reproducible evidence consists of `concrete-tests.py`/`.mpy`,
`differential_test.py`, `spec-vacuity.k`, `spec-body-mutation.k`, and
`prove.sh`.  The independent oracle is a memoized textbook recursive
definition, not the iterative state transition used by the implementation or
the K summary.  It checked every input `0..30` with zero mismatches.  These
finite tests support intent and tooling evidence; they are not presented as a
universal proof.

## Excluded behavior

- Inputs outside integer `N >= 0`.
- A separate total-termination/liveness theorem.
- Correctness of CPython, K, the supplied semantics, or `py2mpy.py` themselves.
- Loading the module-level `FuncDef` as a separate theorem; the proved call
  starts with its exact translated closure already bound, while LLVM tests
  exercise module loading and calls together.
