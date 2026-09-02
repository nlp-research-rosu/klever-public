VALIDATED

## What is proven

Under the supplied `MPY` semantics, loading the exact translated definition of
`triangle_area` and calling it terminates with the value constructed by
`a * h / 2.0`. The proof is symbolic and unbounded over every numeric scalar
combination represented by the semantics:

- `Int` × `Int`
- `Int` × `Float`
- `Float` × `Int`
- `Float` × `Float`

There is no positivity or finite-range precondition because `prompt.py` states
none. This is a partial-correctness result: it establishes the returned value
when the modeled call terminates, not a separate liveness theorem.

The program boundary includes module loading, definition of the exact function
body, name lookup, left-to-right argument evaluation, parameter binding,
arithmetic dispatch, return, frame popping, and the complete modeled state.
The observable final state includes the returned value, scopes, environment,
scope and heap locations, heap, stack, return state, exception state, and exit
code.

## Formal claims

`spec.k` contains four required positive target claims. For symbolic inputs
`A` and `H`, their result postconditions are:

```k
Int,   Int   : intFloatDiv(A *Int H, 2.0)
Int,   Float : divF(mulF(intToF(A), H), 2.0)
Float, Int   : divF(mulF(A, intToF(H)), 2.0)
Float, Float : divF(mulF(A, H), 2.0)
```

Each claim starts from the complete initial MPY configuration, executes
`#loadAll` on the same constructor body emitted in `solution.mpy`, invokes the
resulting closure, and constrains both the result and all configuration cells.
Together, the four symbolic claims cover the full material numeric domain of
the HumanEval contract, rather than examples or finitely bounded inputs.

## Proof-extension inventory

`verification.k` only imports the supplied `MPY` modules. It declares no local
function, equation, simplification, ordinary rewrite, priority rule,
operational bridge, macro, or auxiliary claim. Consequently, no
program-defined operation is summarized or skipped.

The following result-bearing opaque functions come from the fixed reference
semantics and are classified as trusted primitives, not local proof
extensions:

| Primitive and fixed dispatch | Class and domain | Context and state footprint | Value influence and justification | Dependent claims |
|---|---|---|---|---|
| `intFloatDiv(I:Int, F:Float)` from `applyBin("/", I, F)` | Trusted primitive; all `Int × Float` values | Arithmetic value position only; no cells or control are read, written, skipped, or abstracted | Determines the returned float. The supplied semantics declares it total/opaque for proof and gives the concrete LLVM equation `Int2Float(I,53,11) /Float F`. | `triangle-area-int-int` |
| `intToF(I:Int)` in the supplied mixed multiplication dispatch | Trusted primitive; all `Int` values | Pure value conversion; no state/control footprint | Determines the promoted multiplication operand. The supplied semantics gives a concrete LLVM `Int2Float` equation. | Both mixed-sort claims |
| `mulF(F1:Float, F2:Float)` from float and mixed `applyBin("*",...)` rules | Trusted primitive; all modeled float operands | Pure arithmetic value position; no state/control footprint | Determines the product. It is opaque under symbolic proof and concretely maps to `F1 *Float F2` under LLVM. | Both mixed-sort and float/float claims |
| `divF(F1:Float, F2:Float)` from `applyBin("/", F1, F2)` | Trusted primitive; all modeled float operands | Pure arithmetic value position; no state/control footprint | Determines the final result. It is opaque under symbolic proof and concretely maps to `F1 /Float F2` under LLVM. Here the divisor is always the nonzero literal `2.0`. | Both mixed-sort and float/float claims |

These primitives do not preempt a program-defined body. The fixed semantics
executes the body and dispatches its arithmetic operations normally. The
claims are interpretation-parametric in the opaque symbols and state the
returned symbolic terms exactly; no theorem about their numerical values is
silently asserted.

## Exact commands and actual outputs

The reproducible command record is executable as `./prove.sh`.

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Actual output: none; exit 0. `solution.mpy` is:

```text
Module(
  FuncDef("triangle_area", Params("a", "h"),
    Return(BinOp("/", BinOp("*", Name("a"), Name("h")), Float(2.0)))))
```

```bash
python3 py2mpy.py smoke.py > smoke.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual results: all commands exited 0. LLVM compilation printed only supplied
semantics warnings about non-exhaustive total helpers and unused variables.
`krun` ended with:

```text
<k> .K </k>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

```bash
python3 differential.py
```

Actual output and exit:

```text
python_cases=49 k_cases=49 oracle=Decimal mismatches=0
Exit: 0
```

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

Actual proof output and exit:

```text
#Top
Exit: 0
```

Haskell compilation exited 0 and printed only the supplied `str.k` unused
variable warnings.

The false-result non-vacuity probe was run as:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`. The residual result was:

```text
<k> intFloatDiv ( A *Int H , 2.0 ) ~> .K </k>
```

which did not unify with the deliberately false `noneV` destination.

The body-sensitivity probe was run as:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`. Changing the divisor in the
program body to `3.0` produced the residual obligation:

```text
#Not ( {
  intFloatDiv ( A *Int H , 2.0 )
#Equals
  intFloatDiv ( A *Int H , 3.0 )
} )
```

Finally, the complete `./prove.sh` replay exited 0 after observing both
expected negative-probe failures.

## Gate results

### Gate A — PASS

- A1: The exact program-defined body executes through the fixed semantics.
  `solution.mpy` and every positive claim contain the same constructor body.
  The divisor mutation makes the original claim fail.
- A2: There are no operational bridges. The claims constrain every active
  state cell before and after execution.
- A3: Fixed name lookup, argument evaluation, closure binding, return, and
  frame-pop rules execute without interception. No abrupt control is added.
- A4: No local equations or total functions exist to create overlap,
  inconsistency, or false off-domain behavior.
- A5: `(a, h) = (5, 3)` is a realizable witness and concretely returns `7.5`.
  The false-result mutation exits 1 at the actual result.

### Gate B — PASS

- B1: The claims are symbolic over all `Int` and `Float` values and all four
  sort combinations. There are no bounds, fixed sizes, examples-as-theorems,
  or strengthened sign guards.
- B2: MPY `Int` models mathematical integers; MPY `Float` is the supplied
  opaque symbolic float domain with LLVM concrete evaluation. This reference
  semantics boundary is explicit.
- B3: The formally proved execution result is the exact symbolic realization
  of base times height divided by two. Its numerical interpretation is
  conditional on the named supplied primitives and empirically checked below.
- B4: `solution.py` implements the stated triangle-area formula and reproduces
  the prompt example.

The absence of Python type annotations does not make arbitrary nonnumeric
objects material length inputs. The modeled numeric scalar domain covers the
ordinary integer and floating-point interpretations of side length and height.

### Gate C — PASS

Every unproved component is named in the trust ledger below. All claimed
concrete, differential, and mutation evidence has an existing artifact, an
exact command, a documented scope and oracle, and an actual result. Formal,
conditional, and finite empirical conclusions are kept separate.

## Trust boundary

| Unproved component | Why outside the theorem | Effect and dependents | Evidence |
|---|---|---|---|
| Supplied `intFloatDiv`, `intToF`, `mulF`, and `divF` numerical interpretation | The reference semantics intentionally keeps symbolic float operations opaque under `kprove` | Affects the returned numeric value in the claims listed in the extension inventory; does not affect control or state | Concrete LLVM rules supplied with MPY; six-case smoke run; 49-case Decimal differential run |
| `py2mpy.py` translation correctness | The translator is a fixed benchmark input, not proved by `spec.k` | Connects `solution.py` to the constructors proved in `spec.k` | Deterministic regeneration of `solution.mpy`; direct constructor-body inspection |
| Correctness of the supplied MPY operational semantics and K toolchain | Granted benchmark foundation | Affects all execution and proof claims | LLVM execution, Haskell `#Top`, negative probes that discriminate body and result |

No program-defined operation, proof-local oracle, or unproved
result-characterizing lemma is trusted.

## Empirically supported facts

- `smoke.py` tests the prompt example, zero, negative, integer/integer,
  integer/float, float/integer, and float/float inputs. The exact translated
  smoke artifact ends in `.K` with `NoExc` and exit code 0 under LLVM.
- `differential.py` reads the actual `solution.py`, generates and translates
  49 calls over the Cartesian grid
  `{-4, -1.5, 0, 0.5, 2, 3.5, 5}²`, and checks both CPython and MPY/LLVM
  against an independently evaluated `Decimal` oracle. It reports zero
  mismatches.
- These 49 cases support the concrete implementation of the supplied opaque
  float primitives. They do not replace or enlarge the universal symbolic
  proof.
- `spec-vacuity.k` and `spec-body-mutation.k` are reproducible negative
  evidence that the positive proof constrains both the return value and the
  actual source body.

## Excluded behavior

- Nonnumeric objects, strings, collections, user-defined operator overloads,
  complex numbers, `Decimal`, and `Fraction` are not material triangle length
  inputs and are not represented by these claims.
- CPython behaviors absent from the supplied MPY subset are outside the
  theorem.
- Numerical facts about the opaque float primitives beyond their named fixed
  contracts are conditional, with finite evidence only.
- Total correctness, resource bounds, and termination outside the modeled
  numeric calls are not claimed.
