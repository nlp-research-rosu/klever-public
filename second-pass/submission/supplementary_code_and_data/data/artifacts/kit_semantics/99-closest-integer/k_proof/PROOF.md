VALIDATED

# What is proven

Under the supplied `MPY` semantics, calling the exact translated body of
`closest_integer` on an arbitrary symbolic `str(CS:IntSeq)` returns the lower
or upper adjacent integer selected by the program's sign and distance tests.
The four claims in `spec.k` collectively cover every `IntSeq`, with no bound on
the number of characters.

This is a partial-correctness theorem. Its interpretation as the HumanEval
"closest integer, ties away from zero" property is conditional on the named
supplied float primitives having the contracts in the trust ledger below.

# Formal claim

For an arbitrary `CS:IntSeq`, define:

```text
F = decStrToF(CS)
L = floorFI(F)
U = ceilF(F)
DL = subF(F, intToF(L))
DU = subF(intToF(U), F)
```

`spec.k` proves these four complementary execution cases:

| Claim | Guard | Returned value |
|---|---|---|
| `closest-positive-lower` | `ltIF(0,F)` and `floatLt(DL,0.5)` | `L` |
| `closest-positive-upper` | `ltIF(0,F)` and not `floatLt(DL,0.5)` | `U` |
| `closest-nonpositive-upper` | not `ltIF(0,F)` and `floatLt(DU,0.5)` | `U` |
| `closest-nonpositive-lower` | not `ltIF(0,F)` and not `floatLt(DU,0.5)` | `L` |

Each Boolean and its negation form a complete partition. Therefore these
claims cover the full symbolic structural domain rather than examples, fixed
lengths, or bounded unrollings.

The invocation configuration pins:

- the `closest_integer` binding to a closure containing the exact body in
  `solution.mpy`;
- the argument binding, module parent, and builtins scope;
- empty heap and call stack, `NoExc`, and exit code 0;
- restoration of all those observable cells after return.

The theorem boundary is the entry-point call after module loading. The
module-level `Import("math")` is a no-op in the supplied semantics, and the
fixed `math.floor`/`math.ceil` call rules intercept their exact syntax.

# Proof-extension inventory

`verification.k` only imports the supplied `MPY` module. It adds no syntax,
function, totality declaration, equation, simplification rule, priority rule,
ordinary rewrite, operational bridge, or trusted primitive.

`spec.k` contains only the four reachability claims above. Program-defined code
executes through the fixed semantics. Consequently there is no proof-local
extension that bypasses the body or assumes the requested result.

The opaque symbols imported from the read-only reference semantics are listed
separately in the trust ledger; they were not added or changed by this proof.

# Reproduction and actual results

The complete executable record is `prove.sh`. It regenerates all `.mpy`
artifacts before compiling or running them.

## Translation and independent differential test

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 py2mpy.py model_boundary.py > model_boundary.mpy
python3 differential_test.py
```

Actual result:

```text
Differential cases: 5019; mismatches: 0
```

Exit status: 0.

The independent oracle first parses with CPython `float`, converts that binary
float exactly with `Decimal.from_float`, and applies
`ROUND_HALF_UP`, which is ties-away-from-zero. It does not reuse the
implementation's floor/ceiling distance equations.

## Concrete LLVM execution

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
krun model_boundary.mpy --definition runtime-kompiled
python3 model_boundary_cpython.py
```

Actual results:

- LLVM compilation exited 0, with warnings from the supplied definition.
- `krun solution.mpy` exited 0 with final `<k> .K </k>`,
  `<exc> NoExc </exc>`, and exit code 0.
- `krun concrete_tests.mpy` exercised 23 assertions and exited 0 with the same
  successful final control and exception state.
- `krun model_boundary.mpy` exited 0, establishing that the supplied model
  returns 632 for `"1e2"`.
- CPython printed
  `CPython float("1e2") boundary witness: 100` and exited 0.

## Symbolic build and target proof

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual target-proof output:

```text
#Top
```

Both commands exited 0. The compiler also emitted only unused-variable warnings
from `reference-semantics/semantics/str.k`.

## False-result non-vacuity probe

`spec-vacuity.k` changes the positive-upper postcondition from `U` to `U + 1`.
The exact command is:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual status: 1, as expected. `vacuity-probe.log` records
`WarnStuckClaimState` and the failed obligation:

```text
ceilF(decStrToF(CS)) +Int 1 #Equals ceilF(decStrToF(CS))
```

The realizable ground witness is `"14.5"`: LLVM concrete execution returns 15,
whereas the mutated postcondition requires 16.

## Body-sensitivity probe

`spec-body-mutation.k` materially changes the positive far/tie branch from
`return upper` to `return lower` while retaining the original result
postcondition. The exact command is:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual status: 1, as expected. `body-mutation-probe.log` records
`WarnStuckClaimState`; execution reaches `floorFI(decStrToF(CS))` but the
destination requires `ceilF(decStrToF(CS))`.

# Gate results

## Gate A — PASS

- **A1, identity and body sensitivity:** the claims bind the exact translated
  closure body and let the fixed call, assignment, branch, return, and frame
  rules execute. The body mutation is rejected with a result-sensitive
  residual.
- **A2, state preservation:** no operational bridge exists. The claims pin the
  environment, scopes, scope allocator, heap, heap allocator, stack, return,
  exception, and exit-code cells before and after execution.
- **A3, binding/evaluation/control fidelity:** the entry binding, argument,
  builtins root, evaluation order, nested returns, and call-frame restoration
  all execute through the fixed semantics.
- **A4, consistency:** there are no proof-local equations or rewrites to audit
  for overlap, coverage, or false cases.
- **A5, non-vacuity:** the preconditions are realizable (including the concrete
  `"14.5"` witness), the false-result mutation is rejected, and each branch is
  exercised by concrete tests.

## Gate B — PASS, conditional on the fixed-model boundary

- **B1, input domain:** `CS:IntSeq` is symbolic and unbounded. The four guards
  collectively cover every representable string sequence. Numeric-string
  well-formedness is the source contract's own precondition, not an added
  fixed-length restriction.
- **B2, model adequacy:** the supplied parser documents only decimal digits,
  an optional decimal point, and an optional leading minus. Exponent notation
  is a concrete model boundary: `"1e2"` produces 632 in the supplied LLVM
  model and 100 in CPython. ASCII-only literal handling is another stated
  reference-model boundary. These are recorded boundaries of the fixed model,
  not restrictions introduced by the program or theorem.
- **B3, property adequacy:** conditional on the primitive contracts below, the
  branch equations implement nearest-integer rounding: positive ties select
  `ceil`, negative ties select `floor`, and strict distances below one half
  select the nearer endpoint.
- **B4, implementation alignment:** the implementation matches the prompt's
  examples and tie rule. The differential run found zero mismatches. It also
  caught and caused removal of an earlier add-0.5 implementation that failed
  at `±0.49999999999999994`.

Strings parsed as NaN or infinity and magnitudes whose conversion makes an
integer result undefined are outside the meaningful "closest integer" contract;
the specified result does not exist for those values. Invalid non-number
strings are likewise outside the source precondition.

## Gate C — PASS

Every unproved value-level component is named below with its influence,
dependents, and evidence. All claimed concrete, differential, boundary, and
mutation artifacts exist in this directory and their exact commands are in
`prove.sh`. The finite evidence is reported only as evidence; it is not used as
a universal proof of the opaque primitives.

# Trust ledger

The following symbols are fixed, supplied primitives intentionally opaque to
the Haskell proof backend. The target proof is interpretation-parametric in
them, and the HumanEval conclusion is conditional on their contracts.

| Symbol | Conditional contract and effects | Dependent claims | Evidence |
|---|---|---|---|
| `decStrToF(IntSeq)` | Parses an in-model finite decimal string to the corresponding binary float. Value affects every branch and result. | All four | 23 LLVM assertions; 5,019 CPython differential cases; explicit `"1e2"` counter-witness bounds the contract |
| `floorFI(Val)` | Returns the mathematical floor of a finite float as an integer. Affects distance tests and returned values. | All four | LLVM assertions at integers, non-integers, signs, and ties |
| `ceilF(Val)` | Returns the mathematical ceiling of a finite float as an integer. Affects distance tests and returned values. | All four | Same LLVM suite |
| `intToF(Int)` | Converts each adjacent endpoint back to the float used by the distance calculation. Affects control. | All four | LLVM suite; the CPython differential evidence separately includes `9007199254740993` |
| `subF(Float,Float)` | Computes the endpoint distance used by the implementation. Affects control. | All four | LLVM cases immediately below, at, and above half distance |
| `ltIF(Int,Float)` | Implements exact integer/float sign ordering. Affects the top-level branch. | All four | Positive, zero, and negative LLVM cases |
| `floatLt(Float,Float)` | Implements the strict distance comparison. Strictness is load-bearing for ties-away-from-zero. | All four | `±0.5`, `±0.49`, `±2.499`, and `±2.501` LLVM cases |

The supplied `math.floor` and `math.ceil` call-interception rules, ordinary
lookup/call/frame rules, and control rules are executed by the proof rather
than replaced by proof-local abstractions.

# Empirically supported and excluded behavior

Formally established:

- exact program execution and final result structure for arbitrary symbolic
  `IntSeq`;
- complete branch coverage under the supplied opaque Boolean/value functions;
- restoration of all modeled operational cells;
- rejection of the false result and changed body.

Conditionally established:

- the returned integer is the closest integer to the finite parsed number,
  with exact ties away from zero, under the trust-ledger contracts.

Empirically supported:

- 23 LLVM assertions spanning examples, signs, zero, ties, near-ties, integer
  spellings, and the original rounding counterexample;
- 5,019 independently generated finite CPython-float cases with zero
  mismatches.

Explicitly outside the fidelity claim:

- exponent, plus-sign, surrounding-whitespace, and other spellings not modeled
  by the supplied decimal parser, with `"1e2"` retained as a concrete witness;
- non-ASCII behavior outside the supplied string-literal model;
- invalid strings, NaN, infinity, and conversions for which no closest integer
  result exists.
