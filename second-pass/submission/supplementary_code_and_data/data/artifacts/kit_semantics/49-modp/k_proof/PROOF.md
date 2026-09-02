VALIDATED

## What is proven

Under the supplied MPY reference semantics, the translated body of
`modp(n, p)` returns the Python-style residue of `2` raised to `n` for every
symbolic integer pair satisfying:

```text
n >= 0
p != 0
```

The theorem is unbounded in both inputs. It is a partial-correctness theorem:
when the modeled call terminates, its result is
`pyMod(2 ^Int n, p)`. It does not use fixed-size unrolling or a finite
collection of examples as the target proof.

The exact Python implementation is:

```python
def modp(n: int, p: int):
    return 2 ** n % p
```

`solution.mpy` was regenerated from that source by the supplied, unmodified
`py2mpy.py`. A final translator consistency check printed
`TRANSLATION_MATCH`.

## Formal claim

`SPEC.modp` starts with an exact binding of `modp` to the closure body emitted
in `solution.mpy`. It invokes that binding through the fixed semantics'
ordinary `Name` lookup, argument evaluation, frame allocation, parameter
binding, expression evaluation, `Return`, and frame-pop rules.

The claim is:

```text
Call(Name("modp"), Int(N), Int(P))
  => pyMod(2 ^Int N, P)
requires N >=Int 0 andBool P =/=Int 0
```

The complete configuration fixes and observes `env`, `scopes`, `scopeLoc`,
`heap`, `heapLoc`, `stack`, `ret`, `exc`, and `exit-code`. Those cells return
to their original values, so the theorem also checks that the call does not
leave a frame, heap mutation, return marker, or exception behind.

There is no loop in the implementation, so no loop-invariant circularity is
needed.

## Proof-extension inventory

There are no proof-local extensions.

`verification.k` contains no syntax declaration, function, equation,
simplification rule, concrete rule, priority rule, ordinary rewrite,
operational bridge, opaque term, or auxiliary claim. It only imports the
supplied `MPY` module. `spec.k` contains only the target reachability claim.

The `pyMod`, `applyBin("**", ...)`, `^Int`, and `%Int` operations are part of
the supplied fixed semantics or K's fixed integer domain; they were not added
or altered for this proof.

| Extension | Class | Semantic role | Domain/context/state/value justification | Dependents |
|---|---|---|---|---|
| None | N/A | Fixed semantics executes the complete program | No proof-local matched context, skipped state, introduced value, or extra equation exists | None |

## Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`. It was run from
`/workspace` as:

```bash
./prove.sh
```

Actual final result: exit `0`.

The substantive commands and observed results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
```

Both exited `0`. `solution.mpy` contains the exact `FuncDef` with
`Return(BinOp("%", BinOp("**", Int(2), Name("n")), Name("p")))`.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Actual result: exit `0`. The compiler emitted supplied-semantics warnings,
including non-exhaustive matches in `builtins.k`, `float.k`, `methods.k`, and
`subscript.k`, plus unused-variable warnings in `str.k`; there was no compile
error.

```bash
krun smoke.mpy --definition runtime-kompiled
```

Actual result: exit `0`. The final configuration contained:

```text
<k> .K </k>
<env> 0 </env>
<scopeLoc> 1 </scopeLoc>
<heap> .Map </heap>
<heapLoc> 0 </heapLoc>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

All five examples from `prompt.py` were assertions in `smoke.mpy`.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Actual result: exit `0`, with only the supplied `str.k` unused-variable
warnings.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output ended with:

```text
#Top
```

Actual result: exit `0`. Before `#Top`, `kore-exec` emitted
`DecidePredicateUnknown` warnings while attempting optional simplifications of
symbolic integer exponentiation/modulo predicates; the reachability proof
nevertheless closed and returned the required success signal.

The Gate A5 false-result probe was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1` with `WarnStuckClaimState`. For the satisfiable witness
`n = 3, p = 5`, the residual contained `<k> 3 ~> .K </k>` and could not unify
with the deliberately false destination `4`.

The implementation body-sensitivity probe was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1` with `WarnStuckClaimState`. With the implementation's
base changed from `2` to `3`, the witness `n = 1, p = 5` reached
`<k> 3 ~> .K </k>` and could not unify with the required result `2`.

The independent finite differential test was:

```bash
python3 differential_test.py
```

Actual output and result:

```text
cases=32901 mismatches=0
```

Exit `0`.

The model-boundary witnesses in `prove.sh` printed:

```text
negative-exponent-witness: 0.5 float
zero-modulus-witness: ZeroDivisionError integer division or modulo by zero
```

## Gate results

### Gate A — PASS

- **A1 program identity/body sensitivity:** the claim pins the exact
  translated closure body and binding. Fixed semantics executes the complete
  call. Changing the base from `2` to `3` makes the connection fail on
  `(n, p) = (1, 5)`.
- **A2 operational state:** there is no operational bridge. The complete call
  executes normally, and every modeled state/control cell is fixed on both
  sides of the target.
- **A3 binding/evaluation/control:** ordinary fixed-semantics name lookup,
  left-to-right argument evaluation, closure dispatch, parameter binding,
  `Return`, and frame cleanup execute without interception.
- **A4 logical consistency:** no proof-local equation, total function, or
  simplification rule exists to audit. The fixed reference semantics is used
  unchanged.
- **A5 non-vacuity/result constraint:** `(n, p) = (3, 5)` is a realizable
  pre-state and evaluates to `3`. The false destination `4` is rejected with
  exit `1` and a concrete stuck residual.

### Gate B — PASS

- **B1 input domain:** the modular-exponent contract's material domain is a
  nonnegative integer exponent and nonzero integer modulus. `N` and `P` remain
  symbolic and unbounded; negative moduli are also covered. No list size,
  exponent bound, example-only restriction, or bounded unrolling is present.
- **B2 language model:** K `Int` and Python `int` are both unbounded
  mathematical integers for the proved operations. The supplied MPY rule for
  integer `**` intentionally has the guard `N >= 0`. Negative integer
  exponents therefore form an explicit fixed-model behavior boundary; CPython
  evaluates the implementation at `(-1, 5)` to the float `0.5`, while the
  supplied MPY integer-exponent rule has no such case. Modulus zero is
  contract-inherently undefined and CPython raises `ZeroDivisionError`; the
  supplied exception cell does not model that exception. Neither boundary is
  replaced by a fabricated result.
- **B3 property adequacy:** the destination is the contract formula itself,
  using the fixed semantics' exponentiation and Python-style modulo. There is
  no separately asserted summary-to-property bridge.
- **B4 implementation alignment:** the translated implementation is exactly
  `2 ** n % p`, matching the stated result formula.

### Gate C — PASS

- All proof files and validation artifacts exist and are invoked by
  `prove.sh`.
- The positive proof signal, both expected negative proof results, all
  concrete examples, the differential scope/oracle/result, and both model
  boundary witnesses are recorded above.
- Formal proof, fixed-model boundaries, partial-correctness scope, and finite
  empirical evidence are stated separately.

## Trust boundary

| Component | Why it is outside this theorem | Influence | Dependent claim | Evidence |
|---|---|---|---|---|
| Supplied `reference-semantics/` | It is the fixed language definition required by the task | Binding, control, state, integer operations, and result | `SPEC.modp` | LLVM examples, body mutation, false-result mutation; files were not modified |
| K `^Int` and `%Int` hooks | Primitive integer operations beneath the supplied MPY rules | Result value and definedness | `SPEC.modp` | K proof plus 32,901 CPython differential cases |
| `py2mpy.py` | Supplied trusted source-to-constructor translator | Program identity | `SPEC.modp` | Regeneration and byte-for-byte `diff` produced `TRANSLATION_MATCH` |
| K v7.1.293 Haskell prover/backend | Trusted proof engine and SMT/rewrite implementation | Proof closure | `SPEC.modp` | `#Top`, exit `0`; negative probes rejected |

No program-defined operation is trusted or summarized, and no proof-local
assumption affects the result, control, state, exception, or termination
behavior.

## Empirically supported facts

`differential_test.py` uses CPython's independently implemented
three-argument `pow(2, n, p)` as its oracle. It checks every pair with
`0 <= n <= 256` and `-64 <= p <= 64`, excluding zero, then adds all prompt
examples and large-exponent cases at `n = 1101` and `n = 10000`.

It checked 32,901 distinct pairs with zero mismatches. This is finite
validation evidence; it is not used as the universal proof.

The LLVM smoke program independently executed the five examples from
`prompt.py` under the supplied concrete semantics and terminated with `.K`,
`NoExc`, and exit code `0`.

## Excluded behavior

- Negative exponents are outside the nonnegative modular-exponent domain and
  are not modeled by the supplied MPY integer `**` rule. The concrete CPython
  behavior is recorded rather than silently claimed.
- `p = 0` is excluded because modulo zero is undefined and CPython raises
  `ZeroDivisionError`, which this supplied MPY exception model does not
  represent.
- As a partial-correctness result, the proof does not establish resource
  bounds or termination under finite machine memory for exceptionally large
  exponents.
