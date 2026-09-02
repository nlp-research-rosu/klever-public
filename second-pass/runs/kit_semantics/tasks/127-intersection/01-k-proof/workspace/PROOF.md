VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, the exact constructor program
generated from `solution.py` has the following partial-correctness property:
for every pair of integer intervals `(A0, A1)` and `(B0, B1)` satisfying
`A0 <= A1` and `B0 <= B1`, a terminating call to
`intersection((A0, A1), (B0, B1))` returns `"YES"` exactly when

```text
min(A1, B1) - max(A0, B0)
```

is at least 2 and has no proper divisor from 2 through one less than itself.
It returns `"NO"` otherwise. This is the usual definition of primality and
uses geometric interval length, as required by the prompt's examples.

The whole-program claim loads `solutionModule`, which is generated
mechanically from `solution.mpy`; name lookup, argument evaluation, tuple
construction and indexing, comparisons, assignments, the while loop, string
literals, return control, and frame popping all execute through the supplied
semantics.

## Formal claim

`SPEC.intersection-correct` starts from the complete initial MPY
configuration:

```k
<k>
  #loadAll(solutionModule)
  ~> Call(Name("intersection"),
          TupleExpr(Int(A0), Int(A1)),
          TupleExpr(Int(B0), Int(B1)))
  => primeResult(overlapLength(A0, A1, B0, B1))
</k>
requires A0 <=Int A1 andBool B0 <=Int B1
```

The final environment, heap, heap allocator, stack, return state, exception
state, and exit code are constrained. The final scope map is existentially
framed because function/module bindings are internal and are not observable in
the HumanEval contract.

The proof discharges three loop obligations:

1. `divisor-loop-true`: once a divisor has been found, the flag remains true.
2. `divisor-loop-false`: if none has yet been found at candidate `D`, the
   final flag is `scanHasDivisor(false, N, D)`.
3. `intersection-correct`: source setup reaches one of those loop claims and
   the post-loop return agrees with `primeResult`.

The base case is `D == N`. The inductive cases are a zero remainder, which
sets the flag, and a nonzero remainder, which advances from `D` to `D + 1`.

## Proof-extension inventory

### `solutionModule`

- Extension/class: `solutionModule => Module(...)`; definitional source-term
  abbreviation.
- Semantic role: names the exact contents of `solution.mpy`; it does not skip
  program execution.
- Domain and matched context: the single synthetic `solutionModule` term used
  as the argument to `#loadAll`.
- Justification scope/context containment: `solution-module.k` is regenerated
  directly from `solution.mpy` by `make_solution_module.py`. Empty statement
  lists are only respelled from the translator's blank list notation to the
  equivalent explicit `.Stmts`.
- State footprint/value influence: no state transition; expansion supplies the
  function body that fixed semantics subsequently loads and executes.
- Dependents: `intersection-correct` and both negative validation probes.
- Validation: `check_artifacts.py` confirms the LLVM smoke body is AST-identical
  to `solution.py`; the final-return body mutation is rejected by `kprove`.

### `overlapLength`

- Extension/class: unguarded total definitional summary.
- Semantic role: names
  `(#if B1 < A1 #then B1 #else A1) -
   (#if B0 > A0 #then B0 #else A0)`.
- Domain: all four K integers; one exhaustive equation.
- Matched context/state footprint: pure mathematical term; no operational
  cells or continuation.
- Value influence: determines the argument of `primeResult`.
- Value justification: the two conditionals are exactly the source branches
  that compute `end = min(A1, B1)` and `start = max(A0, B0)`.
- Dependents: `intersection-correct`.
- Validation: all 8,281 interval pairs in `validate.py` have zero mismatches
  against an independently written `min`/`max` oracle.

### `scanHasDivisor`

- Extension/class: total definitional summary with ground `[concrete]`
  equations.
- Semantic role: returns true when the incoming flag is true or an integer in
  `[max(2, D), N)` divides `N`; it does not rewrite a source-language term.
- Domain: all `Bool × Int × Int` inputs.
- Coverage/descent:
  - `true` returns `true`;
  - `false` with `D < 2` normalizes to `D = 2`;
  - `D >= 2 && D >= N` returns `false`;
  - `2 <= D < N` splits disjointly on `pyMod(N, D) == 0`;
  - the nonzero case recurses at `D + 1`, which reaches `N`.
- Matched context/state footprint: pure value term; no continuation, binding,
  control, or state cell is matched.
- Value influence: fixes the loop invariant's final Boolean and therefore the
  final `"YES"`/`"NO"` branch.
- Value justification: the equations are the exhaustive trial-divisor
  definition. Their guards are disjoint except where the symbolic lemmas state
  the same mathematical value.
- Dependents: `divisor-loop-false`, `primeResult`, and
  `intersection-correct`.
- Value validation: K ground execution in `summary-smoke.mpy` reaches `.K`;
  `validate.py` compares 23,754 `(seen, N, D)` cases with an independent
  `any(...)` oracle and reports zero mismatches.

### Symbolic `scanHasDivisor` lemmas

- Extension/class: four derived `[simplification]` lemmas for (1) an already
  true flag, (2) the empty range, (3) a divisor at `D`, and (4) folding
  `scan(false, N, D + 1)` to `scan(false, N, D)` when `D` is a non-divisor.
- Semantic role: expose consequences of the ground definition without
  unfolding a symbolic recursive call indefinitely.
- Domain: exactly the guards written in `verification.k`; every use has
  `D >= 2`, so `pyMod` never receives a zero divisor.
- Matched context/state footprint: pure summary terms only. The fold lemma's
  `D + 1` pattern is the syntactic value produced by one source iteration.
- Justification scope/context containment: each lemma is one base or step
  equation of the preceding total definition. No framed operational context is
  accepted.
- Value influence: permits the loop circularity to establish the exact final
  flag.
- Dependents: `divisor-loop-false`.
- Validation: the two loop claims close together; all ground summary and
  differential tests pass. Guard overlap is consistent by the same exhaustive
  definition (for example, if `D + 1` is itself a divisor, both sides of the
  fold are true).

### `primeResult`

- Extension/class: unguarded total definitional summary.
- Semantic role: returns `"NO"` when `N < 2` or
  `scanHasDivisor(false, N, 2)` is true, and `"YES"` otherwise.
- Domain: every K integer.
- Matched context/state footprint: pure term; no operational context.
- Value influence: this is the constrained result of the target claim.
- Value justification: it is exactly the standard proper-divisor definition
  of prime numbers.
- Dependents: `intersection-correct`.
- Validation: prompt examples, broad differential tests, the false-result
  mutation, and the body mutation all discriminate its result.

### Loop claims

- Extension/class: `divisor-loop-true` and `divisor-loop-false`; derived
  reachability lemmas/circularities.
- Semantic role: summarize repeated fixed-semantics execution; they are claims,
  not operational rules.
- Domain: `2 <= D <= N`. The local scope is a closed plain-function map with
  exactly `interval1`, `interval2`, `start`, `end`, `length`, `divisor`, and
  `has_divisor`; this syntactically excludes closure-cell frames.
- Matched context: the exact recurring `#while` term and exact loop body. The
  active continuation and the remaining configuration are framed.
- Context containment/control: the loop body contains no return, break,
  continue, exception, frame pop, heap operation, or output. It changes only
  `divisor` and `has_divisor`, so arbitrary framed continuations and preserved
  cells are valid.
- State footprint: reads `length`, `divisor`, and `has_divisor`; writes
  `divisor` and possibly `has_divisor`; preserves every other local and every
  other cell.
- Value influence: supplies the Boolean consumed by the post-loop branch.
- Justification: symbolic execution of the fixed `MPY` while, comparison,
  modulo, assignment, and loop-label rules plus the classified summary
  equations.
- Dependents: `intersection-correct`; the false-flag claim also uses the
  true-flag claim on its divisor-found branch.
- Validation: both claims are included in the successful unbounded proof. No
  operational bridge or trusted primitive is present.

## Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`; running:

```bash
./prove.sh
```

exited 0.

Translation and generated source identity:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 make_solution_module.py > solution-module.k
```

Both exited 0. Relevant SHA-256 values from the final run:

```text
bad7f11a9862a893af90e25e49f7b1325318b16a73cdae43ccead0a0fbd9831b  solution.py
9392d552bd8b1a10179245ab9ec4be341bcae391aac2eb1241d44cc07a06c6b1  solution.mpy
cbd35e5dfee35031ec2b0a0e0c35d01d123ec96ae7f57f8b253de219fb609588  solution-module.k
e4c76a5ac1411f83937acf6fe5d3a78d6aae812a376a05d51cc597157a46ed64  verification.k
2eec48d98dc0d4e5ff1c670d0b3176e80fc37dc41d99ae30d52dde36c86e0c3c  spec.k
```

Required LLVM execution:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
```

All exited 0. `krun` ended with `<k> .K </k>`, `NoExc`, and exit code 0.
LLVM emitted only the supplied-semantics non-exhaustive/unused-variable
warnings recorded by the run.

Positive symbolic proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Both exited 0. Actual `kprove` output begins:

```text
#Top
```

The remaining output consists only of unused-variable warnings from the
supplied semantics and framed spec variables. The complete captured output is
`proof.out`.

Ground summary and differential evidence:

```bash
krun summary-smoke.mpy \
  --definition verification-kompiled \
  --parser ./parse-verification.sh
python3 validate.py
```

Both exited 0. Actual outputs:

```text
<k> .K </k>
validation: program_cases=8281 program_mismatches=0 summary_cases=23754 summary_mismatches=0
```

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Expected exit: 1. Actual exit: 1. `vacuity.out` contains
`WarnStuckClaimState` and the actual result
`str(iCons(89, iCons(69, iCons(83, .IntSeq))))` (`"YES"`), which cannot match
the mutated `"NO"` destination.

Body-sensitivity probe:

```bash
python3 make_mutant.py > solution-mutant.py
python3 py2mpy.py solution-mutant.py > solution-mutant.mpy
python3 make_solution_module.py solution-mutant.mpy \
  --constant mutantSolutionModule \
  --prefix MUTANT-SOLUTION-MODULE > mutant-solution-module.k
kompile --backend haskell mutation-verification.k \
  --main-module MUTATION-VERIFICATION \
  --syntax-module MUTATION-VERIFICATION-SYNTAX \
  --output-definition mutation-verification-kompiled
kprove spec-body-mutation.k \
  --definition mutation-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

The build exited 0. The final `kprove` expected exit is 1 and actual exit is 1.
`body-mutation.out` contains the actual `"NO"` result and the mutated final
`Return(Str("NO"))`, which cannot match the correct `"YES"` destination.

Tool versions:

```text
kompile/krun/kprove: K v7.1.293, build 2025-10-03
python3: Python 3.10.12
```

## Gate results

### Gate A — PASS

- A1 program identity/body sensitivity: PASS. The claimed module is generated
  from `solution.mpy`; the material final-return mutation invalidates the
  expected claim.
- A2 operational-state preservation: PASS. There is no operational bridge.
  Fixed semantics performs every source step. The loop claims preserve all
  cells outside their stated two-variable footprint.
- A3 binding/evaluation/control fidelity: PASS. Module loading, closure lookup,
  left-to-right arguments, parameter binding, tuple access, return, stack
  restoration, and frame deallocation all execute under `MPY`.
- A4 consistency/rule validity: PASS. The total summary cases cover their
  domains, recursive descent is bounded by `N`, divisor-zero cases are
  excluded before `pyMod`, and symbolic rules are valid consequences of the
  definition.
- A5 result constraint/non-vacuity: PASS. The precondition is realized by
  `(-3, -1)` and `(-5, 5)`; changing its required `"YES"` result to `"NO"`
  produces exit 1 and a stuck residual.

### Gate B — PASS

- B1 domain alignment: PASS. The theorem covers every pair of K-integer
  2-tuples whose starts do not exceed their ends, exactly the prompt's stated
  domain.
- B2 language-model adequacy: PASS for the exercised subset. K integers are
  unbounded like Python integers; tuple indexing, integer arithmetic/modulo,
  control flow, and the ASCII result strings have the required behavior.
- B3 summary/property adequacy: PASS. `scanHasDivisor(false, N, 2)` is
  definitionally true exactly when `N` has a proper divisor; `N >= 2` plus its
  negation is the standard prime definition.
- B4 implementation/intent alignment: PASS. All prompt examples and the broad
  independent oracle agree.

### Gate C — PASS

- C1 trust ledger: complete below; no hidden proof-local oracle or operational
  bridge exists.
- C2 evidence: all named artifacts exist; commands, scopes, oracles, exits, and
  mismatch counts are recorded above and in `prove.sh`.
- C3 result language: formal claims, trusted infrastructure, finite evidence,
  and exclusions are separated in this report.

## Trust boundary

- The supplied read-only reference semantics is trusted as the intended model.
  The combined SHA-256 over its sorted files is
  `2dbb59e14d6666df3ddff4f77802afb3ce81368dbc10d11a2998c82cb4a1ce5b`.
- K v7.1.293, its Haskell/LLVM backends, SMT integration, and Python 3.10.12
  are trusted infrastructure.
- `py2mpy.py` is the supplied fixed translator
  (`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
  The proof uses its generated constructor term directly.
- `[total]` on `scanHasDivisor` is justified by the audited exhaustive cases
  and terminating descent. It is not an unproved external value oracle.
- No external service, floating-point primitive, opaque sort, operational
  bridge, or named mathematical assumption is used.

## Empirically supported facts

- `smoke.py` contains the three prompt examples and four boundary/composite
  cases. Its function AST is checked identical to `solution.py`; LLVM MPY
  execution reaches `.K` with no exception.
- `validate.py` tests all 8,281 ordered pairs drawn from every valid interval
  with endpoints in `[-6, 6]`. Its independent oracle uses Python `min`,
  `max`, and trial division only through `isqrt`; zero mismatches occurred.
- The same artifact tests 23,754 summary cases over both incoming flags,
  `N in [-10, 100]`, and `D in [-3, 103]` against an independently structured
  `any(...)` oracle; zero mismatches occurred.
- `summary-smoke.mpy` executes 13 ground K assertions covering negative and
  boundary values, primes, composites, non-default starts, and an already true
  flag.
- These finite results support adequacy and catch regressions; the universal
  result comes from `kprove`, not from testing.

## Excluded behavior

- Inputs that are not two integer 2-tuples, intervals with `start > end`,
  out-of-bounds tuple access, and the associated Python exceptions are outside
  the theorem.
- Python `bool` values used as integer endpoints and non-integer numeric types
  are outside the formal K-integer domain.
- The theorem uses geometric interval length `end - start`, not the count of
  integer points in a closed interval. This is forced by the prompt examples.
- Final internal scope contents are unobserved; the returned value and all
  other operational cells are constrained.
- This is a partial-correctness reachability proof. It does not separately
  claim a liveness theorem, asymptotic complexity, or behavior for constructs
  outside the supplied Python subset.
