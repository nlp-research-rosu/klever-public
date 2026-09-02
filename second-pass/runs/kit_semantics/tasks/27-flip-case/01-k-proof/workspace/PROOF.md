VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, for every symbolic finite
`CS:IntSeq`, loading the exact translated definition of `flip_case` and invoking
it on `str(CS)` rewrites to `str(mapSwap(CS))`. The claim has no length bound,
no enumeration of fixed sizes, and no precondition restricting `CS`.

The reference semantics defines `mapSwap` structurally over the complete
sequence and defines `swapC` as:

- ASCII uppercase codes 65 through 90 map to the corresponding lowercase code
  by adding 32;
- ASCII lowercase codes 97 through 122 map to the corresponding uppercase code
  by subtracting 32;
- every other modeled code is unchanged.

This is a partial-correctness reachability theorem. It covers the full symbolic
string domain of the supplied model, not merely the examples.

## Formal claim

The target is `SPEC.flip-case` in `spec.k`. Its entry configuration starts from
the pristine module and builtins scopes, loads the exact `solution.mpy`
`FuncDef`, and invokes the resulting binding with `str(CS:IntSeq)`. Its
destination requires:

- the result `str(mapSwap(CS))` in `<k>`;
- the caller environment and all control cells restored;
- the temporary call frame removed;
- no heap allocation or mutation;
- `NoExc` and exit code 0; and
- only the expected module-level `flip_case` closure added to the scopes.

There is no loop in the implementation, so no loop-invariant claim is needed.

## Proof-extension inventory

There are no proof extensions. `verification.k` only imports the supplied
`MPY` module. It declares no syntax, function, totality assertion, equation,
simplification rule, ordinary rewrite, priority rule, operational bridge,
trusted primitive, or auxiliary claim. `spec.k` contains only the target
reachability claim, which is not used as a loop circularity by this
straight-line execution.

Consequently, every contract field concerning an added extension—matched
context, justification scope, context containment, state footprint, value
influence, dependents, and bridge validation—is not applicable. In particular,
no rule intercepts the call, replaces the program-defined body, or introduces
an opaque result shared with the postcondition.

## Exact commands and actual outputs

Translation:

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Exit 0. The generated term is:

```text
Module(
  FuncDef("flip_case", Params("string"),
    Return(Call(Attribute(Name("string"), "swapcase"), ))))
```

Concrete build and execution:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

All three commands exited 0. Both `krun` commands produced a final
`<generatedTop>` with `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. The smoke program checks the prompt example,
empty input, and mixed letters/digits/punctuation.

Independent executable checks:

```bash
python3 test_solution.py
```

Exit 0, exact output:

```text
PASS: 5 ASCII cases and 2 Unicode witnesses
```

The ASCII oracle is independently implemented with ordinal ranges and does not
call `swapcase`.

Symbolic build and required positive target proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Both commands exited 0. The target proof's success output was:

```text
#Top
```

The compiler also repeated four non-fatal unused-variable warnings originating
in the supplied `reference-semantics/semantics/str.k`; no warning originates in
the proof files.

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Expected exit 1. The residual contains the actual result
`str(iCons(97, .IntSeq))` (`"a"`) while the mutated destination demands
`str(iCons(65, .IntSeq))` (`"A"`), followed by
`WarnStuckClaimState` and the prover's cannot-rewrite-further error.

Body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Expected exit 1. Replacing the body with `return string` leaves the residual
`str(iCons(65, .IntSeq))` while the destination demands lowercase code 97.
The output contains `WarnStuckClaimState`.

Reference-model boundary probe:

```bash
krun model_boundary.mpy --definition runtime-kompiled
python3 -c 'print("CPython boundary:", "é".swapcase(), [ord(c) for c in "é".swapcase()])'
```

The K command has expected exit 113 and stops at:

```text
applyBuiltin ( "chr" , 233 , .Vals )
```

The CPython command exits 0 with exact output:

```text
CPython boundary: É [201]
```

`prove.sh` records and checks this entire workflow, including the expected
non-zero results of all three negative probes.

## Gate A — PASS

- **A1 program identity/body sensitivity:** The claim loads the exact translated
  function body. Fixed semantics performs definition binding, lookup, parameter
  binding, body execution, and return. The identity-body mutation is rejected.
- **A2 operational state preservation:** There is no operational bridge. The
  destination explicitly checks the environment, scopes, allocation counters,
  heap, call stack, return state, exception state, and exit code.
- **A3 binding/evaluation/control fidelity:** The fixed `MPY` call, attribute,
  method-dispatch, function-frame, return, and pop rules execute without
  interception.
- **A4 consistency/rule validity:** No proof-local equation or rule exists to
  audit.
- **A5 result constraint/non-vacuity:** Input `"A"` is realizable in the supplied
  semantics. The deliberately wrong `"A"` result is rejected with exit 1 after
  execution computes `"a"`.

## Gate B — PASS

- **B1 input-domain alignment:** The prompt's annotated input is `str`. The
  claim quantifies over an unconstrained `CS:IntSeq`, covering every finite
  string structure in the fixed model with no size bound.
- **B2 language-model adequacy:** The implementation is the ordinary CPython
  `str.swapcase()` operation and is faithful to the HumanEval contract. The
  supplied semantics intentionally models string literals and `chr` only for
  ASCII and defines case ranges only for ASCII. This is a fixed-model text
  boundary, not a candidate-imposed domain restriction. The theorem quantifies
  over every internal `IntSeq`; the inability to construct U+00E9 and CPython's
  differing Unicode result are recorded above as a concrete boundary witness.
- **B3 summary-to-property adequacy:** `mapSwap` is not a new summary axiom; it
  is the supplied semantics' recursive definition of `swapcase`, with the
  uppercase, lowercase, and unchanged cases explicit and exhaustive for the
  reference model.
- **B4 implementation-to-intent alignment:** The source implementation directly
  invokes `string.swapcase()`, matching the requested flip-case behavior.

Thus the formal result covers the full HumanEval string domain represented by
the required reference model. Its extrapolation to CPython Unicode behavior is
conditional on the explicitly recorded model boundary, as required by Gate B2.

## Gate C — PASS

### Trust ledger

| Component | Role and influence | Dependents | Evidence/boundary |
|---|---|---|---|
| Supplied `reference-semantics/` and its fixed `mapSwap`/`swapC` rules | Defines Python binding, control, state, and the returned value | Target and mutation claims | Required trusted semantics; imported unchanged; concrete smoke tests |
| Fixed `py2mpy.py` translator | Connects `solution.py` syntax to `solution.mpy` | Program identity | Reproducible translation command and displayed exact term |
| K v7.1.293 compiler/prover/backend | Executes and proves the reachability claim | All machine-checked evidence | LLVM and Haskell builds, `krun`, target `#Top`, and rejected mutations |
| ASCII-only string model (`strToCodes`, guarded `chr`, ASCII `swapC`) | Limits source-level Unicode adequacy; affects non-ASCII values, not the unbounded structural target claim | Any interpretation as full CPython Unicode | Expected K boundary failure at code 233 and independent CPython result `É` |

There is no unproved proof-local component and no hidden result-bearing
abstraction.

### Reproducible evidence

All named artifacts exist: `smoke.py`, `smoke.mpy`, `test_solution.py`,
`model_boundary.py`, `model_boundary.mpy`, `spec-vacuity.k`, and
`spec-body-mutation.k`. `prove.sh` gives their exact commands, scopes, expected
oracles, and status checks. Finite tests are reported only as evidence; the
universal result comes from the symbolic `CS:IntSeq` target claim.

## Excluded or conditional behavior

- Inputs that are not strings are outside the prompt's annotated contract.
- CPython's non-ASCII Unicode case tables are outside the supplied ASCII
  reference semantics. The Python implementation handles them through
  `str.swapcase()`; the K theorem is conditional on the fixed model boundary
  documented above.
- The Kit reachability theorem is a partial-correctness statement and does not
  separately assert a liveness theorem.
