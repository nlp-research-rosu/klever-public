VALIDATED

## What is proven

Under the supplied MPY semantics, the translated `skjkasdkd` definition is
partially correct for every finite symbolic `ValSeq` satisfying `allInts`.
There is no bound on list length or integer magnitude.

The target claim loads the exact function body, calls
`skjkasdkd(list(VS))`, and proves that the returned value is:

```k
digitSum(largestPrime(VS, 0))
```

`largestPrime` scans every element, retains an element exactly when it is
larger than the current accumulator and `isPrime`, and starts at zero.
`isPrime(N)` means `N >= 2` and no integer divisor in `[2, N)` divides `N`.
`digitSum` is decimal decomposition by Python/K `% 10` and `// 10`.
Consequently the expression is the sum of the decimal digits of the largest
prime in the input. If the list has no prime, the initialized accumulator is
zero and the function returns zero.

This is a partial-correctness theorem in the sense of the Kit workflow. It does
not separately assert a liveness theorem.

## Formal claim and scope

- Program boundary: `#loadAll(Module(FuncDef("skjkasdkd", ...)))` followed by
  `Call(Name("skjkasdkd"), list(VS))`; see `SPEC.target`.
- Input domain: every finite `ValSeq` whose elements have MPY sort `Int`,
  expressed by the recursive precondition `allInts(VS)`.
- Observable final state: the returned `<k>` value is constrained to
  `digitSum(largestPrime(VS, 0))`. The target also restores the caller
  environment, empty stack, `noRet`, `NoExc`, unchanged empty heap, and exit
  code zero.
- Intended property: decimal digit sum of the largest prime integer.
- Unboundedness: `SPEC.scan-loop` is a circularity over symbolic `VS`; it is
  not a bounded unrolling or a collection of fixed-size cases.
- Loop obligations:
  - `SPEC.prime-loop` proves the complete symbolic divisor scan.
  - `SPEC.scan-loop` proves the complete symbolic list scan and uses the
    proved prime-loop circularity.
  - `SPEC.digit-loop` proves the decimal digit decomposition.
  - `SPEC.target` connects module loading and real function execution to those
    loop theorems.

## Proof-extension inventory

No proof rule skips a source statement, function call, loop, return, frame
transition, or heap transition. There are no operational bridges and no opaque
program-derived result symbols.

### Exact body aliases: `primeLoopBody`, `scanBody`, `digitLoopBody`, `targetBody`

- Class: definitional summaries.
- Semantic role: names exact MPY syntax; they do not replace execution.
- Domain and context: zero-argument syntax constants, used only where the
  corresponding translated `Stmts` occur.
- Matched context and justification scope: the right-hand sides are the exact
  constructors in `solution.mpy`; `targetBody` includes every translated
  assignment, both `While` loops, the `For`, and `Return`.
- State footprint and value influence: none by the aliases themselves; the
  fixed MPY rules execute the expanded statements and perform all state and
  control changes.
- Dependents: all four claims.
- Validation: regeneration with
  `python3 py2mpy.py solution.py > solution.mpy`; a separate regeneration
  compared byte-for-byte with `solution.mpy` using `cmp` and exited zero.
  The material body-mutation probe is described below.

### `allInts`

- Class: definitional summary.
- Semantic role: recursive domain predicate over the supplied `ValSeq`
  constructors.
- Domain: all `ValSeq`; empty and `vCons` cases are exhaustive and disjoint.
- Matched context: a mathematical term only; no configuration cells.
- State footprint: none.
- Value influence: enables the guarded projection and integer dispatch used by
  the list scan.
- Value justification: `true` on `.ValSeq`; `isInt(V) andBool allInts(R)` on
  `vCons(V,R)`.
- Dependents: `SPEC.scan-loop` and `SPEC.target`.
- Validation: the target proof ranges over symbolic `VS`, and the concrete
  smoke tests include empty, negative, composite, and prime-containing lists.

### `definedProjectInt`, `projectIntTotal`, and the cast/ceil equations

- Class: definitional summary plus derived sort-orientation equations.
- Semantic role: converts a dynamically sorted `Val` to `Int` only under the
  generated predicate `isInt(V)`.
- Domain: every use is guarded by `definedProjectInt(V) == isInt(V)`.
- Matched context and justification scope: only the K subsort cast
  `{V:Val}:>Int`; there is no `<k>` continuation or operational cell match.
  The match domain equals the generated `Int < Val` sort domain.
- State footprint: none.
- Value influence: supplies the exact integer used by comparisons, modulo,
  addition, primality, and the result summary.
- Value justification: the guarded cast, collapse on `I:Int`, idempotence,
  and the `#Ceil` characterization. No rule can produce a projection value
  without `isInt`.
- Dependents: dispatch twins, `prime-loop`, `scan-loop`, and `largestPrime`.
- Control/value validation: ground integer execution in the LLVM smoke test;
  distinct prime/composite summary probes (`181` and `4`); false result and
  body mutations are rejected.

### Guarded MPY-INT dispatch twins

Exact twins are supplied for:

```text
applyCmp(">",  V:Val, I:Int)
applyCmp(">=", V:Val, I:Int)
applyCmp("<",  I:Int, V:Val)
applyBin("%",  V:Val, I:Int)
applyBin("+",  V:Val, I:Int)
```

- Class: derived lemmas.
- Semantic role: restates the supplied MPY-INT equations after guarded total
  projection; it does not intercept source syntax, binding, evaluation order,
  or control.
- Domain: exactly `isInt(V)`, the static match domain of the original
  `Int`-operand equations.
- Matched context: an already evaluated `applyCmp` or `applyBin` mathematical
  term. No continuation, stack, binding, heap, exception, or output cell is
  matched or omitted.
- Justification scope and containment: projection is equal to the original
  `Int` on the complete guard. The right-hand sides are the same MPY-INT
  operations: `>Int`, `>=Int`, `<Int`, `pyMod`, and `+Int`.
- State footprint: none.
- Value influence: program branches, the stored largest integer, and the
  summaries.
- Dependents: `prime-loop`, `scan-loop`, and `target`.
- Validation: fixed MPY execution remains responsible for expression
  evaluation; the full target closes only with `allInts`. Concrete MPY and
  CPython evidence agree, and both wrong-result probes are rejected.

### `primeTail` and `isPrime`

- Class: definitional summaries.
- Semantic role: mathematical primality specification and the exact loop
  summary.
- Domain: all integer pairs. `D < 2` is the unused totalization case. For
  `D >= 2`, the base `D >= N` and step `D < N` cases are exhaustive and
  disjoint.
- Matched context: mathematical terms only.
- State footprint: none.
- Value influence: the candidate branch and selected maximum.
- Value justification: on the step domain, the concrete equation is
  `not (N % D == 0) and primeTail(N,D+1)`. The divisor-zero simplification and
  the symbolic fold toward `D-1` are the two corresponding orientations of
  this same equation. The symbolic fold is marked `symbolic`, while the
  forward evaluator is `concrete`, avoiding a ground rewrite cycle.
- Dependents: `SPEC.prime-loop`, `selectPrime`, `largestPrime`,
  `SPEC.scan-loop`, and `SPEC.target`.
- Validation: `SPEC.prime-loop` executes the real source loop and prints
  `#Top`; `SPEC-SUMMARY` checks `isPrime(181) == true` and
  `isPrime(4) == false`; LLVM and differential tests cover additional values.

### `selectPrime` and `largestPrime`

- Class: definitional summaries.
- Semantic role: the mathematical left-to-right maximum-prime fold.
- Domain: `selectPrime` covers the Boolean condition and its negation;
  `largestPrime` covers empty, integer-head, and non-integer-head sequences.
  The theorem uses only the integer-head cases through `allInts`.
- Matched context: mathematical terms over the raw MPY `ValSeq`
  constructors; no operational list wrapper or iterator is replaced.
- State footprint: none.
- Value influence: directly characterizes the largest accumulator in the
  target postcondition.
- Value justification: the equations retain `M` unless `X > M` and
  `isPrime(X)`, in which case they retain `X`; recursion processes every raw
  constructor once.
- Dependents: `SPEC.scan-loop` and `SPEC.target`.
- Validation: `SPEC.scan-loop` executes the real `#loop` and closes
  coinductively for arbitrary `VS`; `SPEC-SUMMARY` returns `181` for a ground
  mixed prime/composite list; the independent differential oracle reports no
  mismatches.

### `digitSum` and symbolic fold equations

- Class: definitional summary and algebraic orientations of its defining
  equation.
- Semantic role: exact decimal decomposition for the nonnegative largest
  accumulator.
- Domain: `N <= 0` and `N > 0` are exhaustive and disjoint. The target reaches
  `digitSum` only with a nonnegative accumulator.
- Matched context: mathematical integer terms only.
- State footprint: none.
- Value influence: directly characterizes the returned integer.
- Value justification: the positive equation is
  `N % 10 + digitSum(N // 10)`, written with MPY's exact `pyMod` and quotient.
  The normalized and accumulator-lifted rules are the same equality after
  expanding `pyMod` and integer addition congruence. They are `symbolic`;
  the terminating ground evaluator is `concrete`.
- Dependents: `SPEC.digit-loop` and `SPEC.target`.
- Validation: `SPEC.digit-loop` executes both source `AugAssign` statements
  and prints `#Top`; `SPEC-SUMMARY` proves `digitSum(181) == 10`; prompt
  examples and differential tests agree.

### Reachability circularities and target

- Class: machine-checked auxiliary theorems (`prime-loop`, `scan-loop`,
  `digit-loop`) and the target theorem.
- Semantic role: execute the fixed semantics at the exact loop heads and
  function entry; no claim is an operational rewrite in `verification.k`.
- Domain and context: each loop claim pins the exact plain function scope,
  local keys, `parent(0)`, loop syntax, and relevant continuation frame. This
  rules out the impossible closure-cell branch and contains the claim to the
  real target frame.
- State footprint:
  - prime loop changes only `candidate` and `divisor`;
  - scan loop changes `largest` and scratch locals, preserving `lst`;
  - digit loop changes only `largest` and `total`;
  - target checks the complete entry/return frame lifecycle and unchanged heap.
- Value influence: the auxiliary postconditions compose to the target result.
- Justification: all four claims are proved together by `kprove`; the outer
  scan uses the independently included inner prime circularity.
- Validation: full proof `#Top`; false-postcondition and body mutations both
  exit nonzero with concrete contradictory results.

## Exact commands and actual outputs

The delivered `prove.sh` ran end to end and exited 0. Its material commands are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
python3 concrete-smoke.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual positive target output:

```text
#Top
Exit: 0
```

The read-only reference definition emitted warnings about unused variables and
non-exhaustive functions in unrelated semantics modules. Both kompile commands
exited zero. The concrete MPY smoke run ended with:

```text
<k> .K </k>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
Exit: 0
```

Supporting summary command:

```bash
kprove spec-summary.k \
  --definition verification-kompiled \
  --spec-module SPEC-SUMMARY
```

Actual output:

```text
#Top
Exit: 0
```

False-postcondition command:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual output and status:

```text
WarnStuckClaimState
actual <k>: 2
required <k>: 3
Exit: 1 (expected)
```

Body-sensitivity command:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

The mutation changes `total = 0` to `total = 1` on input `[2]`.

```text
WarnStuckClaimState
actual <k>: 3
required <k>: 2
Exit: 1 (expected)
```

Independent differential command:

```bash
python3 differential_test.py
```

Actual output:

```text
tested=54741
mismatches=0
Exit: 0
```

## Gate results

### Gate A — PASS

- A1: the exact translated function, all source loops, assignments, lookup,
  return, and frame lifecycle execute under the fixed semantics. No
  program-defined operation is replaced. The material body mutation is
  rejected with actual result 3 instead of 2.
- A2: there are no operational bridges. Each invariant pins the real plain
  local scope and records every modified local; the target pins heap, stack,
  return, exception, and exit cells.
- A3: name lookup, argument evaluation, list iteration, loop control, and return
  use the supplied MPY rules. Dynamic integer reasoning is guarded by the exact
  generated `isInt` predicate and total cast.
- A4: definition cases were checked for coverage and overlap. Overlaps between
  concrete and symbolic summary orientations state the same recurrence.
  Symbolic folds and concrete evaluators are separated to avoid rewrite cycles.
- A5: `[2]` is a realizable witness. The off-by-one target mutation exits 1
  with actual 2 versus required 3.

### Gate B — PASS

- The source contract says the list elements are integers. The theorem covers
  every finite MPY list of arbitrary mathematical integers, including empty
  lists, negative values, zero, one, composites, and arbitrary primes.
- There is no size bound, value bound, example-only proof, or bounded
  unrolling.
- `isPrime`, `largestPrime`, and `digitSum` are exhaustive mathematical
  definitions of primality, maximum-prime selection, and decimal digit sum.
- MPY `Int`, `%`, and `//` match the operations used by the implementation on
  this domain. The source expression `value + 0` is identity on integers and
  makes the stored accumulator statically integer-valued in the model.
- Values of other MPY sorts, including `Bool`, are outside the prompt's stated
  integer-element domain rather than a proof-created length or value
  restriction.

### Gate C — PASS

- The trust ledger below names the complete boundary.
- `prove.sh`, all smoke/mutation/summary specs, logs, and the differential test
  exist in the workspace and reproduce the reported evidence.
- Formal results, negative probes, finite empirical evidence, and excluded
  behavior are separated explicitly.

## Trust boundary

- Trusted fixed basis: the supplied read-only `reference-semantics/`, K
  toolchain v7.1.293, K's integer/Boolean/Map theories and SMT reasoning, and
  the supplied `py2mpy.py` transliterator.
- The proof is conditional on those components faithfully modeling the
  represented Python subset. They affect value, control, state, and the target
  claim.
- Translation evidence: `solution.mpy` was regenerated from `solution.py`;
  a second regeneration compared byte-for-byte equal with `cmp`.
- There are no proof-local trusted primitives, opaque values, execution
  accelerators, or operational bridges.
- The theorem is about MPY arbitrary-precision `Int` values. Python behaviors
  for non-integer list elements, exceptions from mixed types, mutation by
  concurrent aliases, and resource exhaustion are outside the stated contract
  and theorem.

## Empirically supported facts

- `concrete-smoke.py` contains all six prompt examples plus `[]` and a
  negative/no-prime list. CPython assertions pass.
- Translating the same smoke program and running it with the LLVM MPY
  definition terminates at `.K`, `NoExc`, exit code zero.
- `differential_test.py` uses an independently written oracle based on
  `all(value % divisor for divisor in range(2, value))`, `max`, string
  conversion, and digit summation. It exhaustively covers lengths 0 through 4
  over values `-2..12` (54,241 lists), plus 500 deterministic random lists with
  values `-100..6000`; zero mismatches occurred.
- These finite checks support implementation/model alignment. The universal
  result comes from `SPEC.target`, not from testing.

## Excluded behavior

- Lists containing non-`Int` MPY values are outside the prompt's
  integer-element contract.
- The report does not prove wall-clock/resource termination or CPython
  implementation limits.
- Behavior outside the constructs modeled by the supplied reference semantics
  is not claimed.

The proof-quality headline `VALIDATED` is distinct from the runner marker.
The positive target proof printed `#Top` and Gate B covers the full HumanEval
contract, so the runner marker is `KPROVE_PASSED`.
