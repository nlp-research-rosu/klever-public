VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every pair of K integers `A` and `B`
such that `A >Int 0` and `B >Int 0`, calling the exact loaded
`generate_integers` closure terminates with a reference to a list containing,
in ascending order, exactly those members of `2, 4, 6, 8` that lie in the
inclusive interval with endpoints `A` and `B`.

This is a K reachability proof under the supplied semantics. The kit's general
guarantee is partial correctness; the proved execution here is loop-free and
the symbolic claim reaches the stated final configuration on every explored
path.

## Formal claim

`SPEC.generate-integers` in `spec.k` starts with:

- the exact function binding and translated body from `solution.mpy`;
- source-level argument expressions `Int(A)` and `Int(B)`;
- the initial module environment, empty heap, empty call stack, `NoExc`, and
  exit code 0; and
- the precondition `A >Int 0 andBool B >Int 0`.

It proves that the call returns `ref(0)`, whose heap object is
`list(expectedDigits(A, B))`. It also proves that `heapLoc` changes from 0 to
1 while `env`, `scopeLoc`, `stack`, `ret`, `exc`, and `exit-code` have their
expected restored/final values. There are no source loops, so no loop
circularity claim is required. `spec.k` contains exactly this one target claim.

`expectedDigits(A, B)` is the ordered sequence obtained by conditionally
keeping 2, then 4, then 6, then 8. `inClosedSpan(A, B, D)` accepts either
endpoint order and is inclusive at both ends.

## Proof-extension inventory

The inventory below was rebuilt from `verification.k` and `spec.k`. There are
no operational bridges, derived lemmas, auxiliary claims, simplification
rules, priority rules, opaque values, or trusted primitives in the proof-local
theory.

### `inClosedSpan(Int, Int, Int)`

- **Class:** definitional summary.
- **Semantic role:** defines the mathematical inclusive-between predicate; it
  never matches or replaces a program computation.
- **Domain and equations:** one unconditional equation over all K integers, so
  coverage is total and there is no overlap.
- **Matched context / justification scope / containment:** only the pure term
  `inClosedSpan(A, B, D)`; the unconditional Boolean formula justifies the
  complete match domain. No continuation, binding, or configuration cell is
  matched.
- **State footprint and control validation:** none; no state or control is
  read, written, preserved, discarded, or abstracted.
- **Value influence and justification:** affects which digits occur in the
  postcondition. Its value is fixed by
  `(A <= D <= B) or (B <= D <= A)` using the fixed integer/Boolean theory.
- **Dependents / validation:** `expectedDigits` and the target claim. The
  positive universal proof connects fixed execution to this value; concrete
  and differential evidence is recorded below.

### `keepDigit(Bool, Int, ValSeq)`

- **Class:** definitional summary.
- **Semantic role:** conditionally prepends one digit to a mathematical
  sequence; it does not replace execution.
- **Domain and equations:** the `true` and `false` rules are disjoint and
  exhaustive over `Bool`; neither recurses.
- **Matched context / justification scope / containment:** only
  `keepDigit(B, D, REST)` for `B:Bool`; the two constructor cases cover exactly
  that domain.
- **State footprint and control validation:** none.
- **Value influence and justification:** directly fixes the postcondition
  sequence, with constructor-exact right-hand sides.
- **Dependents / validation:** `expectedDigits` and the target claim; exercised
  by the universal proof and both inclusion and exclusion concrete cases.

### `expectedDigits(Int, Int)`

- **Class:** definitional summary.
- **Semantic role:** names the requested mathematical result without replacing
  lookup, argument evaluation, calls, branches, list allocation, appends, or
  return execution.
- **Domain and equations:** one unconditional, non-recursive equation over all
  K integers. It performs four finite `keepDigit` applications in ascending
  digit order.
- **Matched context / justification scope / containment:** only the pure term
  `expectedDigits(A, B)`; the unconditional equation has the same domain.
- **State footprint and control validation:** none.
- **Value influence and justification:** determines the final heap list.
  `inClosedSpan` fixes every inclusion decision and `keepDigit` fixes every
  sequence constructor.
- **Dependents / validation:** `SPEC.generate-integers`. Fixed-semantics
  execution is universally connected to this exact value by that target
  claim. The false-postcondition and body-mutation probes were both rejected.

## Commands and actual results

The complete executable record is `prove.sh`. It was rerun from start to finish
and exited 0.

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 test_solution.py
```

Actual result: all commands exited 0; the test printed:

```text
PASS: 10000 positive-input pairs; 0 mismatches
```

The generated `solution.mpy` also compared byte-for-byte equal to fresh
translator output (`cmp` exit 0).

```bash
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
```

Actual result: all commands exited 0. `krun` ended with `.K`, `NoExc`, and
`<exit-code> 0 </exit-code>`. The five assertions exercised `(2,8)`, `(8,2)`,
`(10,14)`, `(3,7)`, and `(6,6)`. The LLVM compiler emitted non-exhaustiveness
warnings for unrelated supplied functions and unused-variable warnings in
`str.k`; none of the warned functions is on this program's execution path.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual result: compilation exited 0. The required positive target proof printed
exactly `#Top` as its proof result and exited 0. The only reported compiler
warnings were unused variables in the supplied `str.k`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: expected exit 1 with `WarnStuckClaimState`. The mutation prefixes
the required result with `0`. The residual includes a realizable positive-input
region with both inputs above 8 and the actual heap list empty, so it cannot
unify with the false prefixed result. The concrete witness `(10,14)` is in that
region.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: expected exit 1 with `WarnStuckClaimState`. The mutation changes
the final program append from `8` to `7`; the residual contains
`list(vCons(7, .ValSeq))` in a satisfiable region that requires the correct
result to contain 8. This independently demonstrates body sensitivity.

## Gate results

### Gate A — PASS

- **A1:** The exact loaded closure binding, parameter list, body, arguments, and
  environment occur in the claim. All program-defined code executes under the
  fixed semantics. The material body mutation is rejected.
- **A2:** No operational bridge exists. The claim observes the returned
  reference and heap contents and constrains every supplied operational cell,
  including allocation state, call stack, return state, exception state, and
  exit code.
- **A3:** Fixed rules perform name lookup, left-to-right argument evaluation,
  frame creation and parameter binding, Boolean short-circuiting, attribute and
  method-call dispatch, mutation, return, and frame restoration. No proof-local
  rule preempts them.
- **A4:** Every proof-local equation is unconditional or split into disjoint,
  exhaustive Boolean constructor cases. All definitions terminate and no
  inconsistent overlap exists.
- **A5:** `(2,8)` is a satisfiable witness producing `[2,4,6,8]`; `(10,14)` is a
  satisfiable empty-result witness. The false-postcondition mutation is
  rejected with exit 1.

### Gate B — PASS

- The formal domain is exactly two positive mathematical integers, matching the
  prompt.
- The inclusive, endpoint-order-independent definition matches all prompt
  examples and the ordinary meaning of “even digits”: the possible returned
  values are exactly `2, 4, 6, 8`.
- K integers and Python integers are both unbounded for the relevant
  operations. The fixed semantics models every exercised construct: function
  call/binding, integer comparison, Boolean short-circuiting, list allocation,
  `append`, and return.
- The implementation and formal postcondition agree. The natural-language
  reading of the definitional summary is additionally supported by the
  independent oracle run.

### Gate C — PASS

- Every proof-local extension and every external trust dependency is identified.
- All proof, mutation, concrete, and differential commands are reproducible
  from existing files and are enforced by `prove.sh`.
- Formal proof results, expected negative results, finite evidence, and trust
  assumptions are separated in this report.

## Trust boundary

The proof trusts the supplied, unmodified `reference-semantics/` definition,
K v7.1.293, the Haskell backend and its solver, the LLVM backend for concrete
evidence, and `py2mpy.py` as the fixed source-to-constructor translator.
`cmp` confirms that the delivered `solution.mpy` is current translator output.
The proof is a theorem about execution under that supplied semantics; fidelity
of the supplied subset semantics to CPython remains an external assumption.

No external primitive, opaque proof value, or proof-local operational rule is
trusted for the result.

## Empirically supported facts

`test_solution.py` uses an independently structured oracle based on
`range(min(a,b), max(a,b)+1)`, parity modulo 2, and the `< 10` digit bound. It
checks every ordered pair in `[1,100] x [1,100]`: 10,000 cases, zero
mismatches. It also checks that the function AST used by `concrete-tests.py` is
identical to the delivered function AST.

`concrete-tests.mpy` runs five boundary and representative assertions through
the required LLVM definition. These finite tests support translator/semantics
adequacy; they are not used as a substitute for the universal K proof.

## Excluded behavior

- Zero, negative, non-integer, and exceptional inputs are outside the formal
  precondition.
- Python's `bool` subtype behavior is outside the K `Int` input domain.
- No claim is made about constructs absent from this function or about warned,
  unrelated partial helpers elsewhere in the supplied semantics.
- No separate general theorem of CPython/MPY equivalence or independent
  termination theorem is claimed.
