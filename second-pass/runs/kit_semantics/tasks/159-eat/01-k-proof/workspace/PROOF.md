VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, both claims in `spec.k` prove
partial correctness of the exact translated body of:

```python
def eat(number, need, remaining):
    if need <= remaining:
        return [number + need, remaining - need]
    return [number + remaining, 0]
```

For every integer `number`, `need`, and `remaining` in the prompt's inclusive
range 0 through 1000, the call returns a reference to a newly allocated
two-element list:

- if `need <= remaining`, the list is
  `[number + need, remaining - need]`;
- if `need > remaining`, the list is
  `[number + remaining, 0]`.

The claims also constrain the complete modeled call configuration: name lookup
selects the exact `eat` closure, the caller environment and scope survive, the
callee frame is removed, one list is allocated at heap location 0, `heapLoc`
advances from 0 to 1, the stack is empty, return state is `noRet`, no modeled
exception is present, and the exit code remains 0.

This is a reachability/partial-correctness result. It is not a separate
liveness theorem, although the branch-only function concretely terminates in
the supplied semantics.

## Formal claim

`SPEC.eat-enough` covers:

```text
0 <= number, need, remaining <= 1000
need <= remaining
result heap value = [number + need, remaining - need]
```

`SPEC.eat-insufficient` covers:

```text
0 <= number, need, remaining <= 1000
need > remaining
result heap value = [number + remaining, 0]
```

The branch guards are disjoint and exhaustive over the formal domain. There is
no loop, so no loop-invariant circularity is required. The invocation
configuration in each claim pins the function name, parameters, translated
body, defining environment, arguments, and every configuration cell.

## Proof-extension inventory

The independently rebuilt inventory is empty.

`verification.k` only imports the supplied `MPY` module. It adds no function,
equation, totality attribute, simplification rule, concrete rule, priority
rule, ordinary rewrite, operational bridge, trusted primitive, opaque result,
or auxiliary claim. `spec.k` contains only the two target reachability claims.
Their computation does not recur to either claim's left-hand side, so claim
circularity contributes nothing to closure.

Consequently, the fixed semantics executes lookup, argument evaluation,
parameter binding, comparison, branching, integer arithmetic, list allocation,
return, and frame cleanup. There is no skipped program execution and no fresh
result-bearing abstraction to connect.

## Exact commands and actual outputs

The complete reproducible command sequence is executable as `./prove.sh`.

### Translation

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
```

Actual result: both commands exited 0. The target translation is:

```text
Module(
  FuncDef("eat", Params("number", "need", "remaining"),
    If(Compare(Name("need"), CmpOp("<=", Name("remaining"))),
      Return(
        ListExpr(
          BinOp("+", Name("number"), Name("need")),
          BinOp("-", Name("remaining"), Name("need")))),
      )
    Return(
      ListExpr(BinOp("+", Name("number"), Name("remaining")), Int(0)))))
```

### Concrete LLVM execution

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy --definition runtime-kompiled
```

Actual result: both commands exited 0. `krun` terminated at `.K`, with
`NoExc`, exit code 0, and this actual heap:

```text
0 |-> list(vCons(11, vCons(4, .ValSeq)))
1 |-> list(vCons(12, vCons(1, .ValSeq)))
2 |-> list(vCons(11, vCons(0, .ValSeq)))
3 |-> list(vCons(7,  vCons(0, .ValSeq)))
4 |-> list(vCons(7,  vCons(3, .ValSeq)))
5 |-> list(vCons(7,  vCons(0, .ValSeq)))
```

These entries respectively represent the four prompt examples,
`eat(7, 0, 3)`, and `eat(7, 3, 0)`. The compiler also emitted existing
warnings from the supplied semantics about unused variables and non-exhaustive
matches in unrelated helper domains; compilation and execution still exited 0.

### Positive symbolic proof

```bash
kompile verification.k \
  --backend haskell \
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

The build and proof also repeated the supplied `str.k` unused-variable
warnings. They did not alter the `#Top` result or exit status.

### False-postcondition mutation

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`. For the satisfiable witness
`eat(5, 6, 10)`, the residual heap contained
`list(vCons(11, vCons(4, .ValSeq)))`, which did not unify with the deliberately
false expected value `list(vCons(12, vCons(4, .ValSeq)))`.

### Changed-body mutation

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`. The mutated enough-stock body
adds one extra carrot. For `eat(5, 6, 10)`, the residual heap contained
`list(vCons(12, vCons(4, .ValSeq)))`, which did not unify with the original
expected value `list(vCons(11, vCons(4, .ValSeq)))`.

### Differential evidence

```bash
python3 differential_test.py
```

Actual output and status:

```text
differential cases: 10347 mismatches: 0
exit 0
```

Finally, running the recorded workflow itself:

```bash
./prove.sh
```

Actual result: exit 0. Its positive target-proof leg printed `#Top`; its two
negative legs printed their `EXPECTED FAILURE` markers.

## Gate results

### Gate A — PASS

- A1: The exact program-defined body executes under fixed semantics. No
  operation is intercepted. The changed-body probe is rejected and exposes
  the changed result.
- A2: There is no operational bridge. All modeled state cells are explicit in
  both claims, including heap allocation, scope, stack, return state,
  exception state, and exit code.
- A3: Fixed rules perform lookup, left-to-right argument evaluation, binding,
  branching, return, and frame popping. There is no bridge context, abrupt
  control abstraction, or exceptional-behavior shortcut to validate.
- A4: No proof-local equations, total functions, simplifications, or opaque
  symbols exist, so there are no proof-extension overlap, coverage, descent,
  or consistency obligations.
- A5: The preconditions have concrete witnesses in both branches, including
  `(5, 6, 10)` and `(2, 11, 5)`. The result is constrained through both the
  returned `ref(0)` and its exact heap value. The false-result mutation exits 1
  with the actual contradictory heap visible.

### Gate B — PASS

- B1: The formal input types and inclusive 0-to-1000 bounds exactly match the
  prompt. The two claims exhaust the domain without strengthening it.
- B2: For this construct subset, the supplied model uses unbounded integers,
  deterministic comparison/arithmetic, ordered two-element lists, ordinary
  call/return behavior, and explicit exception state. These are materially
  aligned with the intended CPython behavior on the stated inputs.
- B3: Each formal heap postcondition directly decodes to the prompt's required
  returned array. No unconnected mathematical summary is used.
- B4: The implementation and theorem agree with all four prompt examples and
  both stock-availability branches.

### Gate C — PASS

- C1: The trust ledger below names the supplied semantics, translator,
  toolchain, and manual source-to-claim identity check. There are no hidden
  proof-local assumptions.
- C2: Every concrete, mutation, and differential artifact exists, with its
  exact command, input scope, oracle, and actual result recorded above.
- C3: This report separates the machine-checked reachability theorem, the
  externally trusted tool/model boundary, finite empirical evidence, and
  excluded behavior.

## Trust boundary

1. The supplied read-only `reference-semantics/` is trusted to model the
   exercised CPython subset faithfully. This assumption affects the
   interpretation of both formal claims as statements about Python; the K
   reachability result itself is relative to those fixed rules.
2. `py2mpy.py` is trusted as the supplied CPython-AST transliterator.
   `solution.mpy` was regenerated by the recorded command, and its body was
   checked constructor-for-constructor against the closure body in both target
   claims.
3. K v7.1.293's parser, compiler, LLVM backend, Haskell backend, SMT
   integration, and prover are trusted implementations. All formal results
   depend on this toolchain.
4. Python 3 and its standard library are trusted for the finite differential
   test only. They are not used as axioms in the K proof.

No program-derived operation, result, or branch condition is classified as an
external primitive.

## Empirically supported facts

`concrete-tests.mpy` executes the four prompt examples and two boundary cases
under the LLVM reference semantics. All six terminate with the expected heap
values and no modeled exception.

`differential_test.py` uses an independently written oracle:

```python
consumed = min(need, remaining)
[number + consumed, remaining - consumed]
```

It checks the four prompt examples, all 343 combinations over
`{0, 1, 2, 5, 10, 999, 1000}`, and 10,000 deterministic pseudorandom triples
from the complete stated domain. The run found zero mismatches. This is finite
evidence for implementation-to-intent alignment, not a replacement for the
universal K claims.

The two proof mutations empirically and machine-checkably demonstrate
postcondition sensitivity and body sensitivity at a realizable witness.

## Excluded behavior

- Inputs that are not integers or are outside the inclusive 0-to-1000 bounds.
- Python behaviors outside the supplied semantics and the constructs exercised
  by this function.
- A standalone proof of translator correctness, reference-semantics
  equivalence to all of CPython, backend correctness, or SMT-solver
  correctness.
- A separate total-correctness/liveness theorem.
- Resource bounds, performance, concurrency, I/O, and external state; the
  target function uses none of them.
