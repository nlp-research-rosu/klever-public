VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every K integer `N` satisfying
`N >Int 0`, calling the exact `get_max_triples` closure translated from
`solution.py` returns

```text
chooseThree(zeroResidueCount(N))
+ chooseThree(N - zeroResidueCount(N))
```

and restores the caller environment, scope allocator, empty heap, empty stack,
return cell, exception cell, and zero exit code. This is a partial-correctness
claim: it constrains every terminating execution in the stated domain and does
not separately prove termination.

## Formal claim

The sole positive target claim is `SPEC.get-max-triples` in `spec.k`.

- Program boundary: the entry call after the module-level function definition
  has bound the exact translated closure in scope 0. Lookup, argument
  evaluation, parameter binding, the complete function body, return, and frame
  cleanup execute under the fixed semantics.
- Input domain: arbitrary unbounded `Int` values with `N >Int 0`.
- Observable final state: the returned integer and every reference-semantics
  state cell. No cell is omitted or framed.
- Postcondition: the result is `expectedTriples(N)`.

For `i` modulo 3, `i*i - i + 1` has residue 0 exactly when `i` has residue 2;
otherwise it has residue 1. Therefore a three-element sum is divisible by 3
exactly when the triple contains either zero or three residue-1 elements. There
are `z = floor((N + 1) / 3)` residue-0 elements and `N - z` residue-1 elements,
so the requested count is `C(z, 3) + C(N - z, 3)`. The proof-side definitions
encode exactly that formula using the supplied semantics' Python-floor-division
normal form.

## Proof-extension inventory

There are no operational bridges, derived lemmas, trusted proof-local
primitives, auxiliary claims, opaque symbols, priority rules, or
simplification rules.

### `zeroResidueCount`

- Extension/class: `zeroResidueCount(Int)`, a `[function, total]` definitional
  summary with one unguarded equation.
- Semantic role: names an arithmetic value on the postcondition side; it does
  not match or replace a program operation.
- Domain and context: every K `Int`, in any term context. The justification
  domain is identical, so context containment is exact.
- State footprint/control: reads or writes no cells and changes no control.
- Value influence: feeds both arguments of `chooseThree` in
  `expectedTriples`, hence the final result.
- Value justification: its exhaustive equation is the reference semantics'
  floor-division form for `(N + 1) // 3`.
- Dependents/validation: `expectedTriples` and `SPEC.get-max-triples`;
  fixed-semantics execution reaches the same expression, the source/spec
  identity check passes, and the independent oracle has zero mismatches.

### `chooseThree`

- Extension/class: `chooseThree(Int)`, a `[function, total]` definitional
  summary with one unguarded equation.
- Semantic role: names `X*(X-1)*(X-2)//6`; it does not replace execution.
- Domain and context: every K `Int`, in any term context, exactly matching its
  justification scope.
- State footprint/control: none.
- Value influence: determines both summands in the final result.
- Value justification: the equation expands to the same `pyMod` and `/Int`
  form produced by fixed execution of Python `//`. Its combination
  interpretation is used only at nonnegative counts, as ensured by `N > 0`.
- Dependents/validation: `expectedTriples` and the target claim; symbolic
  execution connects the program's arithmetic to this expansion, and the
  independent brute-force test supports its intended interpretation.

### `expectedTriples`

- Extension/class: `expectedTriples(Int)`, a `[function, total]` definitional
  summary with one unguarded equation.
- Semantic role: names the sum of the two counts and does not replace
  execution.
- Domain and context: every K `Int`, in any term context; match and
  justification scopes coincide.
- State footprint/control: none.
- Value influence: it is the exact target result.
- Value justification: its sole equation composes the two exhaustive
  definitions above. The dependency graph is acyclic, all equation groups
  cover their declared domains, and no guards overlap.
- Dependents/validation: `SPEC.get-max-triples`; `kprove` connects it to exact
  body execution, while the false-postcondition probe rejects an off-by-one
  result.

## Exact commands and actual outputs

The complete recorded command is:

```bash
./prove.sh
```

It exited 0 and runs these substantive commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 check_artifacts.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC

kprove spec-vacuity.k \
  --definition verification-kompiled --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled --spec-module SPEC-BODY-MUTATION

python3 validate.py
```

Actual results from the final run:

- Artifact check, exit 0:
  `artifact-identity=PASS; solution.mpy body equals spec.k closure body and
  smoke.py function AST`.
- LLVM compilation, exit 0. It emitted supplied-semantics non-exhaustive-match
  warnings for unrelated helper cases and unused-variable warnings in
  `str.k`.
- `krun`, exit 0: final `<k>` was `.K`, `<exit-code>` was 0, and scope 0
  contained `result_1 |-> 0`, `result_5 |-> 1`, and
  `result_10 |-> 36`.
- Haskell compilation, exit 0. It emitted four supplied `str.k`
  unused-variable warnings.
- Positive `kprove`, exit 0: exactly one `#Top` line. It also emitted six
  `DecidePredicateUnknown` diagnostics while exploring builtin arithmetic;
  these were non-fatal and the complete proof result was `#Top`.
- False-postcondition probe, expected exit 1 with
  `WarnStuckClaimState`: at satisfiable witness `N = 4`, execution returned 1
  while the mutation required `expectedTriples(4) + 1 = 2`.
- Changed-body probe, expected exit 1 with `WarnStuckClaimState`: at
  `N = 4`, the mutated `Return(Int(0))` body returned 0 while the unchanged
  postcondition required 1.
- Independent oracle, exit 0:
  `oracle=direct array construction + itertools.combinations; inputs=1..100;
  example_n=5; mismatches=0`.

The complete positive and negative prover outputs are retained in
`kprove-positive.out`, `kprove-vacuity.out`, and
`kprove-body-mutation.out`; the concrete configuration is retained in
`krun-smoke.out`.

## Gate results

- Gate A — PASS. The exact program-defined body executes under fixed
  semantics. The binding, argument, continuation, and every state cell are
  explicit. There is no execution-bypassing rule. All proof-local equations
  are exhaustive, non-overlapping, acyclic definitions. `N = 4` is a
  realizable precondition witness; both the result mutation and body mutation
  are rejected.
- Gate B — PASS. The formal domain is exactly the prompt's positive-integer
  domain. K `Int` and Python integers are unbounded for the operations used.
  The residue argument above derives the closed form from the natural-language
  contract, and the supplied example is reproduced. Materializing the array is
  not observable, so computing its count algebraically preserves the requested
  result.
- Gate C — PASS. All assumptions and dependents are listed below. Every claimed
  concrete, mutation, artifact-identity, and differential check has an
  existing artifact, exact command, input scope, oracle, and recorded result.
  Finite checks are reported only as evidence, not as universal proofs.

## Trust boundary

- The supplied files under `reference-semantics/` are trusted to model the
  stated Python subset. Every formal claim depends on this assumption; they
  were imported unchanged.
- `py2mpy.py` is trusted as the supplied CPython-AST transliterator.
  `SPEC.get-max-triples` depends on the source-to-MPY link. `check_artifacts.py`
  reproducibly confirms that regenerated `solution.mpy`, the closure body in
  `spec.k`, and the function copied into the concrete smoke program are
  structurally identical.
- K v7.1.293, its LLVM and Haskell backends, integer hooks, and the backend
  solver are trusted proof infrastructure. All formal and mutation claims
  depend on them.
- The elementary residue/combinations argument connects the formally proven
  arithmetic summary to the HumanEval prose. `validate.py` provides independent
  finite evidence for that adequacy connection but is not a universal theorem.

No unproved program-derived primitive or operational abstraction lies inside
the proof theory.

## Empirically supported facts

- `smoke.py`/`smoke.mpy` execute the exact function body under LLVM at inputs
  1, 5, and 10, producing 0, 1, and 36.
- `validate.py` independently constructs the requested array and enumerates
  triples with `itertools.combinations` for every input from 1 through 100.
  It does not reuse the proof equations and found zero mismatches.
- The expected-failure artifacts demonstrate result sensitivity and body
  sensitivity at the explicit witness `N = 4`.

## Excluded behavior

- Inputs that are zero, negative, non-integer, or otherwise outside
  `N >Int 0`.
- Total-correctness, time bounds, memory bounds, and behavior under resource
  exhaustion.
- Any Python behavior not modeled by the supplied reference semantics.
- Module import/loading behavior before the exact function closure has been
  bound; the theorem begins at the entry call. The artifact-identity check
  covers the source/closure correspondence but is not itself a K theorem.
- Universal conclusions from the finite concrete and differential tests.
