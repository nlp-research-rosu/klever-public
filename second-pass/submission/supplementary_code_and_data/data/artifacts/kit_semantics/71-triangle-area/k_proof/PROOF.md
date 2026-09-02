VALIDATED

# What is proven

Under the supplied MPY reference semantics, `solution.py` implements the
three-side triangle-area contract for every represented numeric input triple.
The proof covers all 27 combinations of symbolic, unbounded `Int`, `Float`, and
`Bool` arguments. `Bool` is included because the reference semantics, like
Python, treats it as a numeric subtype.

The result is:

- `-1` when `(a + b <= c) or (a + c <= b) or (b + c <= a)`;
- otherwise, `round(sqrt(s * (s-a) * (s-b) * (s-c)), 2)`, where
  `s = (a + b + c) / 2`.

This is a partial-correctness result under the fixed semantics and the named
float-primitive trust boundary below. It is not a separate liveness theorem.

# Formal claim

`spec.k` contains one entry claim for each member of
`{Int, Float, Bool}^3`. Each starts from the exact initial MPY configuration,
loads `triangleProgram()`, resolves and calls `triangle_area` with three
symbolic values of the selected sorts, and reaches
`triangleAreaSpec(A, B, C)`.

The module scope on the destination is existential because loading the module
intentionally leaves the function definition there; it is not observable in
the HumanEval contract. The result, environment, scope allocator, heap, heap
allocator, call stack, return cell, exception cell, and exit code are
constrained.

There are no loops and therefore no loop circularities or bounded unrollings.
Every claim ranges over the complete unbounded K sort named in that claim.

# Proof-extension inventory

## `proofIntToF` and `intToF(I) => proofIntToF(I)`

- **Class:** trusted primitive reification.
- **Semantic role:** replaces only the proof representation of the supplied
  `intToF` primitive; it does not replace Python code or control flow.
- **Domain:** every `I:Int`, with no additional guard.
- **Matched context:** any pure `intToF(I)` subterm during simplification.
  Continuation, bindings, stack, and state cells are not matched or changed.
- **Justification scope and containment:** MPY-FLOAT already declares
  `intToF(Int)` total, opaque to proofs, and gives its concrete LLVM equation.
  The reification has exactly that `Int` domain and retains `I` as an argument.
- **State footprint:** none.
- **Value influence:** mixed arithmetic, some validity branches, and the final
  Heron value.
- **Value justification:** conditional trust assumption T1: for every integer
  `I`, `proofIntToF(I)` denotes the same binary float as MPY's `intToF(I)`.
  The theorem remains parametric in this term and asserts no independent
  bit-level fact about it.
- **Dependents:** all valid-area claims containing an `Int` or `Bool`; pure
  invalid integer paths may return before using it.
- **Control validation:** not applicable to the pure primitive itself. The
  complete function body and its control flow still execute.
- **Value validation:** the untouched LLVM definition passes mixed witnesses
  in `smoke.mpy`; this is finite evidence, not the universal justification.
- **Validation:** required because Haskell lacks `FLOAT.int2float`; without
  reification, mixed symbolic proof execution reports that missing hook.

## `triangleProgram()`

- **Class:** definitional quotation.
- **Semantic role:** names the exact `solution.mpy` module as data; fixed
  `#loadAll`, function-definition, lookup, call, and return rules consume it.
- **Domain:** its single nullary equation.
- **Matched context:** no operational context is matched.
- **Justification scope and containment:** the complete generated module.
  `check_artifacts.py` whitespace-normalizes the explicit empty `.Stmts` form
  and checks equality with `solution.mpy`.
- **State footprint:** none in the equation; executing the quoted module uses
  the ordinary MPY state transitions.
- **Value influence:** selects the exact program body being proved.
- **Value justification:** direct structural identity with the translator
  output.
- **Dependents:** all 27 positive claims.
- **Control/value validation:** the invalid-branch mutation in
  `spec-body-mutation.k` is rejected.

## `invalidTriangle`

- **Class:** definitional summary.
- **Role/domain:** names the three contract inequalities for all `Val` triples.
- **Context/state:** pure, context independent, and reads or changes no cells.
- **Justification:** its single, unguarded equation is the literal invalidity
  predicate. It is total as a K term even where an underlying operator remains
  uninterpreted; positive claims use only numeric sorts.
- **Dependents:** `triangleAreaSpec` and every positive claim.
- **Validation:** the program evaluates the three source comparisons itself;
  no call or branch is rewritten to this summary.

## `semiPerimeter`

- **Class:** definitional summary.
- **Role/domain:** names `((A + B) + C) / 2` for all `Val` triples, preserving
  Python's left association.
- **Context/state:** pure and context independent; no cells.
- **Justification:** one exhaustive, nonrecursive equation using fixed MPY
  operator dispatch.
- **Dependents:** `heronProduct`.
- **Validation:** the source assignment executes independently and reaches the
  same fixed-operation term.

## `heronProduct`

- **Class:** definitional summary.
- **Role/domain:** names `s*(s-A)*(s-B)*(s-C)` for all `Val` triples.
- **Context/state:** pure and context independent; no cells.
- **Justification:** one exhaustive, terminating equation, with the same
  multiplication association as `solution.py`.
- **Dependents:** `triangleAreaSpec`.
- **Validation:** the source multiplication and subtraction AST executes under
  MPY; there is no operational shortcut.

## `triangleAreaSpec`

- **Class:** definitional summary.
- **Role/domain:** names the complete contract result for all `Val` triples.
- **Context/state:** pure and context independent; no cells.
- **Justification:** one exhaustive equation: invalid inputs map to `-1`;
  otherwise the fixed `sqrtF` and two-digit `round` primitive are applied to
  `heronProduct`.
- **Dependents:** all 27 target claims and the body-mutation probe.
- **Validation:** the source body, `math.sqrt` interception, builtin lookup for
  `round`, and return all execute. The false-postcondition mutation is rejected.

All summary symbols have one equation, so there are no pairwise guard overlaps.
Their dependency graph is acyclic. No proof-local rule rewrites a user-defined
call, return, branch, assignment, continuation, frame, or state cell.

# Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`. The final run of:

```bash
./prove.sh
```

exited 0. Its material commands and observed results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 test_solution.py
# CPython cases passed: 6

python3 check_artifacts.py
# Artifact identity checks passed: solution/smoke AST and solution.mpy/K quote

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# Exit: 0

python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
# Final <k>: .K; <exit-code>: 0; process exit: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# Output: #Top
# Exit: 0
```

The positive proof command checks all 27 claims together. Its complete captured
output is `kprove-all.log`.

The A5 non-vacuity probe was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# WarnStuckClaimState
# Exit: 1 (expected)
```

It changes the required result to `-2` under the satisfiable precondition
`A +Int B <=Int C`; witness `(1, 2, 10)` satisfies the precondition and the
real result is `-1`. The residual is in `kprove-vacuity.log`.

The body-sensitivity probe was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# WarnStuckClaimState
# Exit: 1 (expected)
```

It changes the invalid branch from `return -1` to `return -2` while retaining
the original postcondition under the same satisfiable symbolic precondition.
The residual is in `kprove-body-mutation.log`. Neither negative probe contains
the earlier missing-hook diagnostic.

# Gate results

## Gate A — PASS

- **A1:** `triangleProgram()` is structurally identical to `solution.mpy`;
  module loading, binding, and the exact function body execute. The body
  mutation is rejected.
- **A2:** there is no bridge over program execution. All non-scope operational
  cells are constrained; the persistent module-definition scope is deliberately
  unobserved.
- **A3:** the proof starts at module load, so normal MPY name lookup selects the
  just-created closure. Argument order, short-circuit evaluation, returns, and
  frame cleanup execute under fixed rules.
- **A4:** the definitional summaries are exhaustive, nonoverlapping, and
  terminating. The sole external-value reification is explicitly conditional
  on T1 and has the exact supplied primitive domain.
- **A5:** `(1, 2, 10)` is a realizable witness. Both the false result and the
  mutated body produce clean stuck claims and nonzero exits.

## Gate B — PASS

The source contract concerns side lengths, so its material domain is ordered
numeric values. The claims cover every numeric class represented by MPY
(`Int`, IEEE-style `Float`, and numeric-subtype `Bool`), all mixed-type triples,
and every value in those unbounded sorts. There is no size, magnitude, sign, or
finite-enumeration restriction.

Complex numbers and nonnumeric containers are not ordered side lengths and the
specified comparison/formula is not generally defined on them. `Decimal`,
`Fraction`, custom numeric classes, and other CPython values are not represented
by MPY and are recorded as fixed-model boundaries rather than candidate
narrowing.

The formal summary is exactly the invalidity test plus Heron's formula and
two-digit rounding requested by the prompt. The implementation and formal
intent agree.

MPY's float `<=` is encoded as negated `>`. On NaN this differs from CPython:
`model-boundary.py` establishes that CPython returns NaN for
`triangle_area(NaN, 3.0, 4.0)`, while `model-boundary.mpy` establishes that the
untouched MPY LLVM execution returns `-1`. The theorem covers the MPY NaN value;
the discrepancy is an explicit fixed-semantics adequacy boundary.

## Gate C — PASS

Every proof-local equation and every supplied opaque value primitive affecting
the result is inventoried here. Commands, test programs, positive output,
negative residuals, and the concrete model-boundary witness exist in the
workspace. Formal results, conditional primitive assumptions, finite evidence,
and excluded behavior are separated.

# Trust boundary

| Assumption/component | Outside theorem because | Influence | Dependents | Evidence |
|---|---|---|---|---|
| T1: `proofIntToF(I)` denotes MPY/Python integer-to-binary-float conversion | Haskell has no `FLOAT.int2float` evaluator; MPY itself marks the proof-side operation opaque | Values in mixed arithmetic, branches, and final area; no state/control effects | Claims whose path uses an integer or bool conversion | MPY-FLOAT's concrete equation; mixed LLVM smoke cases; input `I` remains explicit |
| Supplied `divII`, `divFloatIntV`, `addF`, `subF`, `mulF`, `gtF`, `ltIF`, `ltFI`, `sqrtF`, and `roundFN` contracts | They are fixed MPY proof-domain primitives intentionally opaque to symbolic IEEE evaluation | Validity branches and returned value; no state effects | Claims using the corresponding numeric sort combinations | Untouched LLVM smoke execution and the contracts in `reference-semantics/semantics/float.k` |
| Partial-correctness interpretation | The Kit reachability workflow does not separately prove liveness | Termination only | All claims | Program is straight-line; concrete runs terminate, but this remains finite evidence |

No user-defined helper or body fragment is trusted.

# Empirically supported facts

- `test_solution.py` checks six CPython cases: both prompt examples, a
  nonintegral rounded area, a mixed numeric case, a degenerate triangle, and a
  Bool-numeric case. It reports six passes.
- `smoke.mpy`, generated through the fixed translator from `smoke.py`, checks
  five corresponding cases under untouched LLVM MPY semantics. It terminates
  with `.K`, exit code 0, and no assertion exception.
- `check_artifacts.py` independently checks the Python AST identity of the
  solution and smoke function and the structural identity of `solution.mpy`
  with `triangleProgram()`.
- `model-boundary.py` and `model-boundary.mpy` reproducibly expose the NaN
  difference described under Gate B.

These are finite evidence only. Universal coverage comes from the 27 symbolic
claims, conditional on the trust boundary.

# Excluded behavior

- Values outside MPY's represented ordered numeric classes.
- Fidelity to CPython on NaN and any other float edge where the supplied model
  differs; the concrete NaN divergence is explicit above.
- Numerical interpretation of opaque float primitives beyond their named MPY
  contracts and T1.
- The final persistent module-scope map, which is internal loader state and not
  an observable of the HumanEval result.
- A separate total-termination theorem.
