VALIDATED

## What is proven

Under the supplied `MPY` semantics, all nine claims in `spec.k` prove the
partial correctness of the translated `compare_one` body for every pairing of
the three permitted modeled input kinds:

- arbitrary `Int` with `Int`, `Float`, or `str(IntSeq)`;
- arbitrary `Float` with `Int`, `Float`, or `str(IntSeq)`; and
- arbitrary finite modeled string code sequence with `Int`, `Float`, or another
  arbitrary finite modeled string code sequence.

These are symbolic, unbounded domains. They are not fixed examples, fixed
string lengths, or bounded unrollings. The claims execute module loading,
ordinary name lookup, argument evaluation, parameter binding, both
`isinstance` calls, both optional `replace`/`float` conversions, both
comparisons, the selected return, frame popping, and restoration of the
control cells under the unmodified reference semantics.

The observable return is:

```text
value(x) = x                                      for modeled Int/Float x
value(str(C)) = decStrToF(replaceC(C, ',', '.'))  for modeled strings

compare_one(a,b) =
    a     if value(a) > value(b)
    b     if not(value(a) > value(b)) and value(b) > value(a)
    None  otherwise
```

For real numbers, trichotomy makes the final case exactly numeric equality.
The two-direction formulation avoids the unavailable Haskell `FLOAT.eq` hook
while preserving the HumanEval contract on its stated real-number domain.
NaN is not a real number and is outside the source contract.

This is a reachability proof of partial correctness. It is not a separate
liveness theorem, although every modeled path in these straight-line claims
does reach its stated result.

## Formal claims and scope

`spec.k` contains the following target claims:

```text
SPEC.int-int       SPEC.int-float       SPEC.float-int
SPEC.float-float   SPEC.int-str         SPEC.str-int
SPEC.float-str     SPEC.str-float       SPEC.str-str
```

Together they cover the full Cartesian product of the three contract types.
Every claim starts from the exact initial MPY configuration, loads the exact
module represented by `solution.mpy`, and calls `compare_one` with symbolic
arguments. The final return is `expectedCompare(A, B)`. The environment,
heap, heap counter, scope counter, call stack, return state, exception state,
and exit code are constrained to their expected restored values. The final
scope map is existential because loading the function intentionally adds its
global closure and the contract observes the return rather than the module
namespace.

The program boundary is the complete translated `compare_one` function. There
are no helper functions and no loops. The intended property is that the
original argument having the greater numeric interpretation is returned in its
original type, or `None` is returned when the two real values are equal.

## Proof-extension inventory

There are no operational bridges, invocation intercepts, execution
accelerators, added algebraic lemmas, or auxiliary circularities.

### `solutionModule()`

- Class: definitional summary (a nullary syntactic abbreviation).
- Semantic role: names the exact `Module(...)` constructor tree generated in
  `solution.mpy`; fixed `#loadAll` and function-call rules still execute it.
- Domain and context: the one nullary term, used only as the argument of
  `#loadAll` in the nine claims.
- State footprint: none. Its equation only constructs syntax.
- Value/control influence: selects the program body executed by every claim.
- Justification: direct execution of `solution.mpy` and execution of
  `solutionModule()` produce byte-identical final KORE configurations.
- Dependents: all nine target claims.
- Validation: `cmp solution-direct.kore solution-named.kore` exits 0. A
  material body mutation is independently rejected by
  `SPEC-BODY-MUTATION.changed-body`.

### `numericValue(Val)`

- Class: definitional summary.
- Semantic role: postcondition-only name for the numeric value constructed by
  the program. It never rewrites an operational `<k>` term.
- Complete domain used by the proof: `Int`, `Float`, and `str(IntSeq)`.
- Equations: identity on `Int` and `Float`; on strings,
  `decStrToF(replaceC(C, 44, 46))`.
- Guard coverage and overlap: the three constructor domains are disjoint and
  cover every use in the target claims. The symbol is deliberately not marked
  `total` over unrelated `Val` constructors.
- State footprint: none.
- Value influence: supplies the two comparisons in the postcondition.
- Justification: these equations are the normal forms produced by the fixed
  assignment, `str.replace`, and `float(str)` rules.
- Dependents: `expectedCompare` and all nine target claims.
- Validation: fixed program execution closes all nine claims; concrete LLVM
  tests exercise each type pairing.

### `expectedCompare(Val, Val)`

- Class: definitional summary of the requested result.
- Semantic role: postcondition only; it does not replace function execution.
- Complete used domain: pairs whose members are `Int`, `Float`, or
  `str(IntSeq)`.
- Equations: return `A` under the first greater-than guard; return `B` under
  its negation and the reverse greater-than guard; otherwise return `noneV`.
- Guard coverage and overlap: `P`, `not P and Q`, and
  `not P and not Q` are exhaustive and pairwise disjoint.
- State footprint: none.
- Value influence: fixes the target return.
- Justification: direct formalization of greater/or-reverse-greater/equal over
  real numbers.
- Dependents: all nine target claims.
- Validation: all claims print `#Top`; the false result mutation and body
  mutation both stop with the opposite concrete value visible in `<k>`.

Because none of these extensions replaces fixed execution, operational-bridge
context-containment and state-preservation obligations are not applicable.

## Exact commands and actual outputs

The complete reproducible runner is:

```bash
./prove.sh
```

It exited 0. Its relevant output was:

```text
AST IDENTITY: solutionModule() matches solution.mpy
cases=289 mismatches=0
#Top
EXPECTED FAILURE: false-postcondition mutation
EXPECTED FAILURE: changed-body mutation
EXPECTED FAILURE: supplied decimal parser differs on exponent notation
```

The positive build and proof commands run by that script are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual positive proof output:

```text
#Top
```

The proof command exited 0. Compiler warnings concern unused variables in the
supplied `str.k` rules and unconstrained final scope-map variables; there were
no compile or proof errors.

The A5 false-postcondition command was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited 1 with `WarnStuckClaimState`; its residual has `2 ~> .K` while the
mutated destination requires `1`.

The body-sensitivity command was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

It exited 1 with `WarnStuckClaimState`; after changing the first greater
branch from `return a` to `return b`, its residual has `1 ~> .K` while the
destination requires `2`.

The AST-identity commands execute the generated term and the named proof term
under the same definition:

```bash
krun solution.mpy \
  --definition verification-kompiled \
  --output kore > solution-direct.kore
krun solution-module.term \
  --definition verification-kompiled \
  --parser ./parse-verification-module.sh \
  --output kore > solution-named.kore
cmp solution-direct.kore solution-named.kore
```

`cmp` exited 0.

## Gate results

### Gate A — PASS

- A1: the exact program body executes under fixed semantics. The KORE identity
  check ties the abbreviation to `solution.mpy`; a material body mutation is
  rejected.
- A2: no operational bridge skips state transitions. Claims constrain the
  heap, environment, counters, stack, return state, exception state, and exit
  code.
- A3: fixed lookup, left-to-right argument evaluation, binding, branch
  control, return, and frame-pop rules execute. No proof rule pins or bypasses
  a binding or continuation.
- A4: all proof-local equations are truthful on their constructor domains.
  `expectedCompare` has disjoint, exhaustive Boolean guards. No false
  simplification or global axiom was added.
- A5: `(1, 2)` realizes the precondition. The false result claim is rejected
  at result `2`, and every target result is constrained by
  `expectedCompare`.

### Gate B — PASS

- B1: the nine claims cover every pairing of the three source-contract types
  over unbounded modeled values. No size bound, finite enumeration, or
  candidate-added domain restriction appears in the theorem.
- B2: the theorem covers every value represented by the fixed model. The
  supplied model's ASCII and decimal-parser limits, opaque symbolic IEEE
  comparisons, and CPython edge differences are recorded below rather than
  hidden as theorem restrictions.
- B3: the formal theorem proves the exact execution/result relationship under
  MPY. Its interpretation as ordering of real values is conditional on the
  named supplied numeric primitives.
- B4: the Python implementation matches the contract on real-number inputs.
  It returns one of the original arguments and uses neither conversion result
  as the returned object.

### Gate C — PASS

Every unproved primitive is listed in the trust ledger with its value/control
influence and dependents. Every claimed concrete, differential, mutation, and
model-boundary check has an artifact, command, actual exit status, and result.
Finite evidence is reported only as evidence, not as a universal proof.

## Trust boundary

| Component | Why unproved here | Influence | Dependent claims | Evidence |
|---|---|---|---|---|
| Supplied `decStrToF(IntSeq)` | Fixed MPY external decimal parser; opaque under `kprove` | Numeric value and branches for every string argument | The five claims with at least one string argument | LLVM smoke cases with dot/comma, signs, and ties; explicit exponent divergence probe |
| Supplied `gtF(Float,Float)` | Fixed opaque symbolic float ordering primitive | Branch and returned original value | `float-float` and string-derived float comparisons | LLVM smoke tests and CPython differential sample |
| Supplied `ltIF(Int,Float)` / `ltFI(Float,Int)` | Fixed opaque exact mixed-order primitives | Branch and returned original value | Mixed int/float and int/string claims | LLVM mixed-type smoke tests and CPython differential sample |
| K Float/LLVM hooks and MPY runtime | External execution platform supplied by the task | Concrete numeric evaluation and testing | Concrete evidence only; symbolic claims remain conditional on named primitives | Required LLVM build, successful smoke run, and documented model-boundary failure |

`replaceC`, integer comparisons, name lookup, calls, assignments, branches,
and returns are defined by ordinary fixed semantics rules and are not added
trust assumptions.

## Empirically supported facts

`smoke.py` contains 16 LLVM assertions: all four prompt examples plus negative,
equal, dot/comma, both-string, int/float, float/int, string/int, int/string,
string/float, and float/string cases. The exact command

```bash
krun smoke.mpy --definition runtime-kompiled
```

exited 0 and ended with `.K`, `NoExc`, and exit code 0.

`differential_test.py` uses an independently written direct Python oracle
(`==` followed by `>`), not the proof equations. It compares all ordered pairs
from 17 representative integers, finite floats, and dot/comma strings:

```bash
python3 differential_test.py
```

Actual output:

```text
cases=289 mismatches=0
```

This is finite adequacy evidence, not a universal equivalence theorem.

For the model boundary, `model_boundary_probe.py` checks exponent notation:
CPython evaluates `compare_one("1e2", 500.0)` as `500.0` and exits 0. The same
translated assertion under the supplied MPY decimal parser exits 113. This
concrete disagreement is intentionally retained in `model-boundary.out`.

## Excluded behavior and model limits

- The source contract permits strings representing real numbers. Invalid
  numeric strings, strings made invalid by replacing every comma with a dot,
  and their CPython `ValueError` behavior are outside that contract.
- NaN is not a real number. The two-direction comparison returns `None` when
  both order tests are false, so no claim is made that this matches a hidden
  reference implementation on NaN.
- The supplied string-literal semantics is ASCII-only. The symbolic theorem
  ranges over arbitrary `IntSeq` values, but this does not establish CPython
  Unicode parsing fidelity.
- The supplied `decStrToF` concrete rule models a decimal subset and differs
  from CPython on accepted forms such as exponent notation. The candidate
  program itself accepts those forms correctly in CPython; the divergence is a
  fixed-semantics boundary, not a theorem restriction introduced by the
  candidate.
- Symbolic float ordering is intentionally opaque in the supplied semantics.
  The proof establishes program structure and result selection conditional on
  the named primitive contracts; it does not prove IEEE-754 or real-analysis
  properties from first principles.

The `VALIDATED` headline reports the Gate A/B/C proof-quality audit. It is
separate from the runner's `KPROVE_PASSED` marker, which reports successful
positive target-proof execution plus full-contract Gate B coverage.
