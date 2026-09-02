VALIDATED

# What is proven

Under the supplied `MPY` semantics, for every mathematical integer `N >= 0`,
executing the exact translated definition of `count_up_to` and calling it with
`N` reaches a normal return containing one freshly allocated list whose
contents are exactly the prime integers less than `N`, in ascending order.

This is a partial-correctness reachability theorem. It does not separately
prove termination.

# Formal claim

The target claim is `SPEC.count-up-to` in `spec.k`. It starts from a fresh
module configuration, executes the exact `FuncDef` binding, resolves
`Name("count_up_to")`, evaluates the integer argument, and executes the
program-defined body. Its precondition is:

```k
requires N >=Int 0
```

Its final observable state is:

```k
<k> ref(0) </k>
<heap> 0 |-> list(primesBelow(N)) </heap>
<heapLoc> 1 </heapLoc>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

`noDivisors(C,D)` states that no integer in `[max(2,D), C)` divides
`C`. `primesBetween(C,N)` skips values below 2 and then includes exactly each
`C < N` satisfying `noDivisors(C,2)`. `primesBelow(N)` is empty for
`N <= 2` and otherwise is `primesBetween(2,N)`.

The auxiliary claims are:

- `SPEC.inner-loop`: from divisor `D`, the fixed inner loop finishes at
  divisor `C` with a Boolean `?PB` satisfying
  `?PB ==Bool (B andBool noDivisors(C,D))`.
- `SPEC.outer-loop`: from candidate `C`, the fixed outer loop finishes at
  candidate `N` and changes heap sequence `P` to
  `valSeqConcat(P, primesBetween(C,N))`.

# Proof-extension inventory

## Exact AST macros

- Extension: `innerBody`, `outerBody`, `countBody`; `countBodyStart3` is
  validation-only.
- Class: definitional summary.
- Semantic role: syntax abbreviation only. Macro expansion happens before
  execution and adds no operational rule to the proof definition.
- Domain and matched context: the exact `.mpy` constructor terms shown in
  `verification.k`; no wildcard program body is accepted.
- Justification scope and containment: `kast --expand-macros` produces the
  same KORE for `countBody` and `solution.mpy`, byte for byte.
- State footprint and value influence: those of the expanded fixed program;
  the macros themselves read or write no cells and compute no value.
- Dependents: all three positive claims use the exact body macros.
- Control/value validation: the parsed KORE hashes match, concrete K execution
  passes all examples, and changing the initial candidate from 2 to 3 makes
  `SPEC-BODY-MUTATION.skip-two` fail.

## `noDivisors`

- Extension: four guarded equations for
  `noDivisors(Int,Int) [function,total]`.
- Class: definitional summary.
- Semantic role: mathematical characterization; it does not rewrite a program
  term or bypass execution.
- Domain: all integer pairs. `D < 2` normalizes to 2; for `D >= 2`, the
  `D >= C`, divisible, and non-divisible cases are exhaustive and pairwise
  disjoint.
- Matched context/state footprint: pure terms only; no continuation, binding,
  or configuration cell is matched.
- Justification scope and containment: exactly the complete equation domain.
  The recursive case increments `D` and reaches `D >= C`.
- Value influence: fixes the inner-loop result Boolean, the append branch, and
  the final sequence.
- Value justification: the equations directly encode absence of a divisor.
  `SPEC.inner-loop` is the bridge-free universal connection theorem from the
  exact fixed-semantics loop to that value for
  `C >= 2` and `2 <= D <= C`.
- Dependents: `inner-loop`, `outer-loop`, `count-up-to`,
  `primesBetween`.
- Control/value validation: the ground opposite interpretations are rejected:
  candidate 3 actually leaves `prime=true`, while candidate 4 actually leaves
  `prime=false`.

## `primesBetween` and `primesBelow`

- Extension: guarded total defining equations in `verification.k`.
- Class: definitional summary.
- Semantic role: names the mathematical output sequence; does not replace
  program execution.
- Domain: all integers. `primesBetween` splits into `C >= N`,
  `C < N and C < 2`, and the disjoint prime/non-prime cases for `C >= 2`.
  `primesBelow` splits on `N <= 2` versus `N > 2`.
- Matched context/state footprint: pure terms only.
- Justification scope and containment: exact complete guards. Recursive calls
  increase `C`, so they reach `C >= N`.
- Value influence: fixes every final list element and its order.
- Value justification: inclusion is exactly `noDivisors(C,2)` and iteration is
  in increasing candidate order.
- Dependents: `outer-loop` and `count-up-to`.
- Validation: prompt examples pass in CPython and LLVM K; the independent
  oracle has zero mismatches for bounds 0 through 200.

## List-concatenation lemmas

- Extension:
  `valSeqConcat(valSeqConcat(A,B),C) =>
  valSeqConcat(A,valSeqConcat(B,C))` and
  `valSeqConcat(A,.ValSeq) => A`, both `[simplification]`.
- Class: derived lemma.
- Semantic role: canonicalizes pure list-summary terms; it does not replace
  program execution.
- Domain: all `ValSeq` values, without guards.
- Matched context/state footprint/value influence: pure terms only; the lemmas
  preserve the exact sequence.
- Justification: structural induction on `A` using the two supplied defining
  equations for `valSeqConcat`. Critical overlaps with the supplied equations
  normalize to the same result.
- Dependents: the `outer-loop` accumulator obligation and therefore
  `count-up-to`.
- Validation: the full proof closes after canonicalization; neither lemma
  introduces control, allocation, or an opaque value.

## Reachability circularities

- Extension: `SPEC.inner-loop` and `SPEC.outer-loop`.
- Class: derived lemma.
- Semantic role: machine-checked auxiliary execution theorems over the exact
  recurring `#while` configurations.
- Domain: the complete configurations and guards written in `spec.k`.
- Matched context: exact loop body and local binding names, with the same
  framed continuation on both sides. Environment, scopes, heap, heap location,
  stack, return state, exception state, and exit code are present.
- Justification scope and containment: match domain and theorem domain are
  identical. The bodies contain no `return`, `break`, `continue`, or exception
  action that could discard the arbitrary continuation.
- State footprint: the inner theorem reads candidate/divisor/prime and writes
  divisor/prime while preserving the heap. The outer theorem additionally
  writes candidate and the list at heap location `H`; it preserves all other
  represented state. Its final local `prime` value is existential because the
  function frame is immediately deallocated and that local is unobservable.
- Value influence and justification: `inner-loop` universally connects fixed
  execution to `noDivisors`; `outer-loop` then connects the fixed append branch
  and heap mutation to `primesBetween`.
- Dependents: `outer-loop` depends on `inner-loop`; `count-up-to` depends on
  both.
- Control/value validation: both claims are included in the single successful
  `kprove spec.k` run. The body, postcondition, and opposite-Boolean mutation
  probes all fail as required.

There are no proof-local operational bridges and no proof-local trusted
primitives.

# Commands and actual outputs

All commands are executable in order via `./prove.sh`.

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Actual result: exit 0; `solution.mpy` contains the translated
`FuncDef("count_up_to", Params("n"), ...)`.

```bash
python3 differential_test.py
```

Actual output and exit:

```text
differential inputs: 0..200; mismatches: 0
Exit: 0
```

The six direct CPython examples print:

```text
CPython examples: 6 passed
Exit: 0
```

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
```

Actual result: compile exit 0 with warnings from the supplied semantics;
`krun` exit 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. The heap contains the expected lists for all six
prompt assertions, including `[2,3]`, `[2,3,5,7]`,
`[2,3,5,7,11,13,17,19]`, and the empty boundary results.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Actual result: exit 0; only unused-variable warnings originate from the
supplied `str.k`.

```bash
kast --definition verification-kompiled \
  --module VERIFICATION-SYNTAX --sort Module --expand-macros \
  --output kore \
  --expression 'Module(FuncDef("count_up_to", Params("n"), countBody))' \
  > /tmp/count-up-to-proof-program.kore
kast --definition verification-kompiled \
  --module MPY-SYNTAX --sort Module --expand-macros --output kore \
  solution.mpy > /tmp/count-up-to-solution-program.kore
cmp /tmp/count-up-to-proof-program.kore \
    /tmp/count-up-to-solution-program.kore
sha256sum /tmp/count-up-to-proof-program.kore \
          /tmp/count-up-to-solution-program.kore
```

Actual output and exit:

```text
609116d2f00f00798834a3ef45563bcbaa075fc0d07ad7a665cc4e54e838ba04  /tmp/count-up-to-proof-program.kore
609116d2f00f00798834a3ef45563bcbaa075fc0d07ad7a665cc4e54e838ba04  /tmp/count-up-to-solution-program.kore
Exit: 0
```

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual proof signal and exit:

```text
#Top
Exit: 0
```

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: `WarnStuckClaimState`, exit 1. The residual heap is
`0 |-> list(.ValSeq)`, which does not match the mutated `[0]` result.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: `WarnStuckClaimState`, exit 1. The start-at-3 body produces
`0 |-> list(vCons(3,.ValSeq))` for input 5 and cannot match
`primesBelow(5)`.

```bash
kprove spec-value-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION-PRIME
kprove spec-value-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-MUTATION-COMPOSITE
```

Actual results: both print `WarnStuckClaimState` and exit 1. Their residuals
show candidate 3 finishing with `prime=true` and candidate 4 finishing with
`prime=false`, rejecting both opposite interpretations.

# Gate results

## Gate A — PASS

- A1: the expanded proof body and generated `solution.mpy` have identical
  parsed KORE and hashes. The material start-at-3 body mutation invalidates the
  unchanged theorem.
- A2: no operational bridge exists. Fixed semantics executes lookup, calls,
  both loops, mutation, allocation, and return. All affected heap/control cells
  are represented by the claims.
- A3: the entry claim fixes the `count_up_to` binding to the exact closure body.
  Arguments and the receiver of `append` execute through supplied rules.
  Loop claims preserve their arbitrary continuation and contain no abrupt
  control.
- A4: proof-local total functions have exhaustive disjoint guards and
  terminating recursion. The two simplification lemmas are globally valid by
  structural induction and have consistent overlaps.
- A5: `N = 0` realizes the precondition. The false `[0]` postcondition is
  rejected, as are both opposite Boolean interpretations.

## Gate B — PASS

- Input domain matches the prompt: non-negative mathematical integers.
- The formal output is exactly every integer `C` with `2 <= C < N` and no
  divisor in `[2,C)`, in increasing order. This is the standard definition of
  the prime integers below `N` and matches every prompt example.
- The exercised semantics use arbitrary-precision integers, positive-divisor
  Python modulo, ordered lists, ordinary call binding, and list mutation. No
  material modeled behavior differs from CPython on this program/domain.
- The implementation and contract agree.

## Gate C — PASS

- Every claimed command, mutation, and differential artifact exists and is
  recorded in `prove.sh`.
- The independent oracle in `differential_test.py` uses `math.isqrt` and a
  generator-based divisibility check, not the implementation loops or K
  summary equations. Bounds 0 through 200 have zero mismatches.
- Concrete LLVM execution independently covers all six prompt examples.
- Formal proof, conditional trust, empirical evidence, and excluded behavior
  are separated below.

# Trust boundary

- The supplied immutable `reference-semantics/` definition is the semantic
  foundation. All positive claims depend on its integer, Boolean, list, call,
  control, allocation, and return rules. Evidence: successful LLVM executions
  of the prompt examples.
- The supplied immutable `py2mpy.py` is trusted to transliterate CPython AST
  nodes as documented. The generated program is then compared to the proof
  body after both are parsed and macro-expanded by K.
- The K v7.1.293 compiler, Haskell backend, SMT reasoning, and `kprove` checker
  are part of the formal toolchain trust base.
- Opaque float, sorting, digest, and other unrelated facilities imported by
  the broad reference `MPY` module are never reached and do not influence any
  branch, value, state, or postcondition in this proof.
- There is no proof-local trusted value or execution rule.

# Empirically supported facts

- CPython passes all six supplied examples.
- The independent CPython differential run over every bound from 0 through
  200 reports zero mismatches.
- LLVM K execution of the AST-identical smoke function passes all six examples
  with normal exit.

These finite checks support semantics/intent adequacy; they are not used as a
substitute for the universal reachability proof.

# Excluded behavior

- Negative inputs, non-integer inputs, and Python subclasses of `int` are
  outside the formal precondition.
- Resource exhaustion and implementation-specific performance are excluded.
- Total termination is not a conclusion of this partial-correctness proof.
