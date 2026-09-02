VALIDATED

# What is proven

Under the supplied `MPY` reference semantics, for every K integer `N >=Int 0`,
loading the exact translated `fibfib` definition from `solution.mpy` and calling
`fibfib(N)` terminates in the reachability claim with the integer
`fibfibSpec(N)`.  The final entry configuration also has the caller environment
restored, the callee scope removed, an empty heap and stack, `noRet`, `NoExc`,
and exit code zero.

`fibfibSpec` is the mathematical sequence

- `fibfibSpec(0) = 0`
- `fibfibSpec(1) = 0`
- `fibfibSpec(2) = 1`
- `fibfibSpec(n) = fibfibSpec(n-1) + fibfibSpec(n-2) + fibfibSpec(n-3)` for
  `n >= 3`

The theorem is partial correctness.  Termination is not a liveness conclusion
of `kprove`, although the implementation increments `i` once per iteration and
the formal domain has `n >= 0`.

# Formal claims

`spec.k` contains exactly the required whole-program claim and one claim for
the one loop.

1. `fibfib-loop` starts at the real internal `#while` configuration.  At loop
   index `I`, the exact local values are
   `a = F(I)`, `b = F(I+1)`, `c = next_value = F(I+2)`, and `n = N`, with
   `0 <= I <= N`.  It reaches `i = N` with the consecutive triple based at
   `N`.
2. `fibfib-entry` starts from `#loadAll(Module(...))` containing the exact
   translated function body, performs fixed-semantics name lookup, argument
   evaluation, call-frame creation, assignments, loop control, return, and
   frame pop, and reaches `fibfibSpec(N)`.

The proof obligations are:

- Base: when `I = N`, the guard is false and the consecutive triple is already
  the required final triple.
- Step: one fixed-semantics loop iteration changes
  `(F(I), F(I+1), F(I+2))` to
  `(F(I+1), F(I+2), F(I+3))` and increments `I`.
- Entry: the assignments establish the loop claim at
  `(a,b,c,next_value,i) = (F(0),F(1),F(2),F(2),0)`.

# Proof-extension inventory

## `fibfibSpec` and its five equations

- Class: definitional summary.
- Semantic role: names the mathematical result; it does not rewrite or bypass
  a Python computation.
- Domain: all K integers.  The disjoint cases are negative integers, `0`, `1`,
  `2`, and integers at least `3`.  The negative case totalizes the function
  outside the theorem domain.
- Matched context: only a term headed by `fibfibSpec`; no continuation,
  binding, control stack, or configuration cell is matched.
- Justification scope and containment: the three bases and the `n >= 3`
  equation are exactly the prompt's definition.  All uses in the theorem have
  nonnegative arguments.  The cases are exhaustive and pairwise disjoint.
- State footprint: none.
- Value influence: supplies all five loop-invariant values and the target
  return value.
- Value justification: the exhaustive bases and recurrence uniquely determine
  every nonnegative ground value.
- Dependents: `fibfib-loop` and `fibfib-entry`.
- Control validation: not applicable; this is not an operational bridge.
- Value validation: the LLVM examples, the 31-case independent recursive
  oracle, and the rejected false-result claim recorded below.

## Shifted recurrence simplification

- Extension:
  `F(I) + F(I+1) + F(I+2) => F(I+3)` under `I >= 0`.
- Class: derived lemma.
- Semantic role: solver-oriented arithmetic reasoning only; it does not match
  a Python AST constructor or a K configuration.
- Domain: every integer `I >= 0`.
- Matched context: the displayed integer expression only; there are no framed
  cells or continuations.
- Justification scope and containment: substitute `N = I + 3` into the defining
  recurrence.  Its guard becomes `I + 3 >= 3`, and its three right-hand indices
  normalize to `I+2`, `I+1`, and `I`.  Integer addition is commutative and
  associative.  Thus every match is within the defining equation's domain.
- State footprint: none.
- Value influence: establishes `next_value = c = F(I+3)` after one loop step.
- Value justification: direct instance of the defining recurrence.
- Dependents: `fibfib-loop`.
- Termination/overlap: it reduces three `fibfibSpec` occurrences to one and
  does not overlap a rule with the same left-hand head symbol.
- Control and value validation: no control effect; the positive loop proof and
  both rejected mutations exercise the only use.

## `fibfib-loop`

- Class: derived auxiliary reachability claim used coinductively as the loop
  circularity.
- Semantic role: symbolically executes the supplied `#while`, comparison,
  lookup, arithmetic, assignments, and loop-label rules.  It is not an
  operational rewrite and does not preempt fixed execution.
- Domain: `I >= 0 andBool I <= N`.
- Matched context: the exact loop condition and body; environment `1`; exact
  global and callee scopes; scope location `2`; empty heap; heap location `0`;
  stack `ListItem(frame(.K, 0, 1))`; `noRet`; `NoExc`; exit code `0`.  The
  trailing `<k>` continuation is universally framed by `...`.
- Context containment: the claim itself is proved for every accepted trailing
  continuation.  Its body contains no return, break, continue, exception, heap
  operation, or call.
- State footprint: reads `n`, `a`, `b`, `c`, and `i`; writes `next_value`,
  `a`, `b`, `c`, and `i`; preserves the remaining listed cells.
- Value influence: its final `a` value supplies the entry claim's return.
- Value justification: the exact fixed-semantics step plus the shifted
  recurrence above.
- Dependents: `fibfib-entry`.
- Control validation: `kprove` proves the loop claim itself; the changed loop
  body in `spec-body-mutation.k` reaches `2` rather than the original result
  `1` and is rejected.
- Value validation: the false target at `n = 5` reaches `4`, not `5`, and is
  rejected.

There are no operational bridges, call interceptors, trusted primitives,
opaque result oracles, priority rules, or proof-local rules that perform
return/frame popping.

# Exact commands and actual results

The complete reproducible run is [`prove.sh`](./prove.sh):

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_test.py > concrete_test.mpy
python3 artifact_checks.py
python3 concrete_test.py
python3 differential_test.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_test.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
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

```text
artifact_checks.py:
entry-point: fibfib(n)
concrete-harness-body: identical
solution.mpy-in-entry-claim: yes

differential_test.py:
inputs: 0..30
cases: 31
mismatches: 0

LLVM kompile: exit 0
krun: <k> .K </k>, <exit-code> 0 </exit-code>, exit 0
Haskell kompile: exit 0
kprove spec.k: #Top, exit 0

spec-vacuity.k:
WarnStuckClaimState with <k> 4 ~> .K </k>
EXPECTED FAILURE: false-result probe exited 1

spec-body-mutation.k:
WarnStuckClaimState with <k> 2 ~> .K </k>
EXPECTED FAILURE: body-mutation probe exited 1

prove.sh: exit 0
```

The compilers also printed warnings originating in the supplied semantics:
unused `As`/`Bs` variables in `str.k`, and LLVM non-exhaustiveness warnings for
unrelated float/list/string helper cases.  None of those symbols is reached by
this integer-only program.

A focused construction run of `fibfib-loop` also printed `#Top` and exited 0.
An entry-only diagnostic deliberately excluding the loop claim stopped on the
zero-iteration branch; it was not a final target-proof command.  The required
all-claims command above includes the circularity, proves every claim, prints
`#Top`, and exits 0.

# Gate results

## Gate A — PASS

- A1: `artifact_checks.py` confirms that normalized `solution.mpy` occurs
  inside the entry claim and that the concrete harness contains the identical
  Python function AST.  The entry claim loads that module, resolves the exact
  closure, and executes its body.  Adding `1` to every loop recurrence step
  makes the mutation claim fail with actual result `2`.
- A2: no execution is skipped.  The claims explicitly constrain environment,
  scopes, scope allocation, heap, heap allocation, stack, return state,
  exception state, and exit code.
- A3: fixed semantics performs definition binding, name lookup, left-to-right
  argument evaluation, call-frame setup, return, and frame restoration.  There
  is no rule pinning or bypassing the binding.
- A4: the mathematical equations have exhaustive, disjoint guards; the shifted
  recurrence is a valid instance of the defining recurrence and strictly
  reduces its counted summary occurrences.
- A5: `n = 5` is a realizable witness.  The real program reaches `4`; the
  deliberately false postcondition `5` is rejected with exit 1.

## Gate B — PASS

- Input domain: K integers `N >= 0`, matching the domain on which the prompt
  defines an indexed sequence.  Non-integers and negative integers are
  explicitly excluded.
- Model adequacy: the relevant Python behavior is integer comparison, addition,
  assignment, a while loop, a function call, and return.  Both Python and K use
  unbounded integers here; no float, collection, encoding, external-state, or
  implementation-defined behavior is involved.
- Property adequacy: `fibfibSpec` repeats the prompt's three bases and recurrence
  exactly.  The invariant proves the consecutive-triple implementation computes
  that definition.
- Implementation alignment: the examples `fibfib(1) = 0`, `fibfib(5) = 4`,
  and `fibfib(8) = 24` pass under the supplied semantics.

## Gate C — PASS

- Every proof-local extension and dependency is inventoried above.
- `prove.sh` regenerates the translated artifacts, checks program identity,
  compiles both backends, runs the concrete assertions, proves all claims, and
  enforces both expected failures.
- The concrete K harness tests `n = 0, 1, 2, 3, 5, 8, 10`.
- `differential_test.py` compares `solution.fibfib` with an independently
  implemented memoized recursive oracle for every `n` from `0` through `30`;
  all 31 cases agree.
- Finite tests and mutations are reported only as evidence.  Universal
  correctness comes from the `#Top` reachability proof under the stated theory.

# Trust boundary

- Trusted fixed theory: the user-supplied, unmodified modules imported by
  `MPY`.  All target claims depend on their Python AST, integer, control, call,
  scope, and return rules.
- Trusted verification machinery: K v7.1.293, its Haskell/LLVM backends, and
  the backend's SMT reasoning.
- Trusted translation boundary: the supplied, unmodified `py2mpy.py`.
  `artifact_checks.py` establishes artifact identity after translation; it
  does not prove the translator implementation correct.
- There are no proof-local trusted primitives.  The recursive Python oracle is
  independent finite evidence, not part of the theorem.

# Excluded behavior

- Inputs that are negative or are not integers.
- A formal total-correctness/termination theorem.
- Behavior under CPython features outside the supplied reference semantics.
- Performance, resource bounds, integer memory exhaustion, and recursion-stack
  behavior of the independent test oracle.
