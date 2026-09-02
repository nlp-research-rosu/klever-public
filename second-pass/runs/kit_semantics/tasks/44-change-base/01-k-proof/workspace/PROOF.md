VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, `change_base(x, base)` is
partially correct for every symbolic K/Python integer `x` and every valid
one-digit positional base satisfying `2 <= base < 10`.

The returned string is:

- `"0"` when `x == 0`;
- the usual most-significant-first base-`base` digits when `x > 0`; and
- `"-"` followed by the magnitude's base-`base` digits when `x < 0`.

This is an unbounded symbolic theorem. It is not a finite-size claim or a
bounded loop unrolling. As a K reachability proof it establishes partial
correctness, not a separate liveness theorem.

## Formal claim

The target claim is `SPEC.change-base` in `spec.k`. Its precondition is:

```k
B >=Int 2 andBool B <Int 10
```

`X:Int` is otherwise unrestricted. The claim invokes the exact translated
closure through the fixed name-lookup, argument-binding, call-frame, return,
and frame-pop semantics and establishes:

```k
Call(Name("change_base"), (X:Int, B:Int, .Exprs))
  => str(changeBaseCodes(X, B))
```

`SPEC.loop-invariant` is the symbolic circularity. At the exact loop head, for
arbitrary nonnegative remaining magnitude `X`, arbitrary accumulator codes
`ACC`, and arbitrary preserved sign codes, it establishes:

```text
x      : X   -> 0
result : ACC -> baseAcc(X, B, ACC)
```

while preserving the exact return continuation, call frame, bindings, heap,
exception state, and other configuration cells.

`baseAcc` is the canonical repeated-division definition: prepend the digit
`48 + (N mod B)` and recurse on `N // B`. `changeBaseCodes` adds the zero and
negative-sign cases.

## Proof-extension inventory

There are no proof-local operational bridges, call interceptions, opaque
oracles, trusted primitives, priority rewrites, or rules that rewrite `<k>`.
All program-defined code executes under the fixed semantics.

### `baseAcc(Int, Int, IntSeq)`

- **Class:** Definitional summary.
- **Semantic role:** Names the mathematical digit accumulator; it does not
  replace execution.
- **Domain:** All `Int × Int × IntSeq`. The guards are the disjoint, exhaustive
  cases `(N <= 0)`, `(N > 0 and B < 2)`, and
  `(N > 0 and B >= 2)`.
- **Matched context:** A pure `baseAcc(N, B, ACC)` term only. It accepts no
  continuation, control stack, binding, or configuration-cell context.
- **Justification scope:** All declared arguments. On the target domain only
  the `N <= 0` and `N > 0, B >= 2` equations are reachable.
- **Context containment:** The equations inspect exactly their three explicit
  arguments and no ambient state.
- **State footprint:** None.
- **Value influence:** It determines the loop invariant's final `result` and
  therefore the function result.
- **Value justification:** The base case returns the accumulated suffix. The
  step uses the supplied Python `pyMod`/floor-division definition and prepends
  the corresponding ASCII digit. For `N > 0` and `B >= 2`, the recursive
  quotient is nonnegative and strictly less than `N`.
- **Justification:** Truthful terminating equations for the standard
  repeated-division conversion algorithm.
- **Dependents:** `SPEC.loop-invariant`, `changeBaseCodes`, and
  `SPEC.change-base`.
- **Control validation:** Not applicable; no execution or control is replaced.
- **Value validation:** The standalone loop claim and full entry claim both
  print `#Top`; the false-result and body-sensitivity probes are rejected.
- **Validation:** Guards are pairwise disjoint and exhaustive, recursive
  descent holds on its only recursive guard, and no off-domain equation is
  globally false.

### `changeBaseCodes(Int, Int)`

- **Class:** Definitional summary.
- **Semantic role:** Defines the complete signed output representation without
  replacing execution.
- **Domain:** All `Int × Int`, split into the disjoint, exhaustive cases
  `N == 0`, `N > 0`, and `N < 0`.
- **Matched context:** A pure `changeBaseCodes(N, B)` term only.
- **Justification scope:** All declared arguments.
- **Context containment:** No framed computation or state is matched.
- **State footprint:** None.
- **Value influence:** It is the target claim's returned `IntSeq`.
- **Value justification:** Zero maps to code 48 (`"0"`), positive values use
  `baseAcc`, and negative values prefix code 45 (`"-"`) to the positive
  magnitude's digits.
- **Justification:** Exhaustive definition of signed positional notation.
- **Dependents:** `SPEC.change-base`.
- **Control validation:** Not applicable.
- **Value validation:** Universal connection to fixed execution is the
  machine-checked `SPEC.change-base` theorem. Concrete and differential
  evidence exercise zero, positive, and negative branches.
- **Validation:** Equations are total, non-overlapping, and consistent.

### `SPEC.loop-invariant`

- **Class:** Derived reachability lemma/circularity.
- **Semantic role:** Proves the exact fixed-semantics loop execution and is used
  by the whole-function claim; it is not an ordinary rewrite in
  `verification.k`.
- **Domain:** `X >= 0` and `2 <= B < 10`, with arbitrary `ACC` and sign codes.
- **Matched context:** The exact `#while` body followed by the exact remaining
  `Return(sign + result)` statement list and `#endcall`; environment 1; exact
  builtins, module closure, and callee scopes; scope location 2; empty heap;
  exact frame `frame(.K, 0, 1)`; `noRet`, `NoExc`, and exit code 0.
- **Justification scope:** Exactly that configuration and symbolic domain.
- **Context containment:** No continuation or cell wildcard broadens the
  theorem. The continuation, stack, bindings, and all configuration cells are
  pinned.
- **State footprint:** Reads `x`, `base`, `result`, and builtin `chr`; writes
  only local `x` and `result`; preserves `sign`, `base`, scopes outside those
  bindings, heap, frame, return state, exception state, and exit code.
- **Value influence:** Establishes the accumulated digit string consumed by
  the final return.
- **Value justification:** Each iteration executes fixed lookup, `%`, `chr`,
  string concatenation, assignment, and `//` rules. Its state transition
  matches one `baseAcc` equation.
- **Justification:** Standalone unbounded symbolic proof:
  `kprove ... --claims SPEC.loop-invariant` prints `#Top`.
- **Dependents:** `SPEC.change-base`.
- **Control validation:** The exact continuation is preserved. A material
  digit-body mutation is executed with fixed semantics and rejected.
- **Value validation:** Prompt examples pass under LLVM; wrong-result and
  wrong-body probes fail; differential evidence has distinct signed and zero
  outcomes.
- **Validation:** Base, inductive, and whole-program obligations all close.

## Exact commands and actual results

`prove.sh` records and executes the complete workflow. The final command:

```bash
./prove.sh
```

exited 0.

Translation and concrete execution:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 concrete_tests.py
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
```

All exited 0. `krun` ended with `.K`, `NoExc`, and exit code 0. Compiler
warnings came from unused/non-exhaustive cases in the supplied read-only
semantics; none affected this program's path.

Symbolic build and proof:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

The build exited 0. Both `kprove` commands printed:

```text
#Top
```

and exited 0.

False-result mutation:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

This exited 1 as expected with `WarnStuckClaimState`. The displayed realizable
branch had `X == 0` and actual result `"0"`, which did not unify with the
deliberately prefixed `"!0"` result.

Body-sensitivity mutation:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

This exited 1 as expected with `WarnStuckClaimState`. Changing the digit offset
from 48 to 49 made the fixed semantics compute code sequence `[51, 51]`
(`"33"`) for `(8, 3)`, which did not unify with `[50, 50]` (`"22"`).

Independent differential evidence:

```bash
python3 differential_test.py
```

exited 0 and printed:

```text
domain: x=-250..250, base=2..9
cases: 4008
mismatches: 0
```

## Gate results

### Gate A — PASS

- **A1:** The target scope binds `change_base` to the exact translated closure
  body. Lookup, argument binding, both conditionals, the loop, and return all
  execute under fixed semantics. The body mutation changes the outcome and is
  rejected.
- **A2:** There are no operational bridges. Every active configuration cell is
  present in the claims, and transient call-frame/scope changes return to the
  stated final configuration.
- **A3:** The exact module binding selects the program closure; builtin lookup
  selects the supplied `chr`; fixed semantics performs left-to-right argument
  evaluation, control transfer, early return, and frame restoration.
- **A4:** Both proof-local functions have exhaustive, disjoint equations.
  Recursive descent is strict on the only recursive domain.
- **A5:** Preconditions are satisfiable (for example `x = 0, base = 2` and
  `x = 8, base = 3`). The false-result and body mutations both exit nonzero
  with concrete mismatching residuals.

### Gate B — PASS

- **B1:** The theorem covers every symbolic integer `x`, not only examples or
  fixed magnitudes. The base domain is exactly the standard valid positional
  bases below 10: `2..9`. Values below 2 are not valid positional bases for the
  stated conversion; values 10 and above are excluded by the prompt.
- **B2:** K `Int` and Python integers are both unbounded mathematical integers.
  The reference string model is ASCII-only, but every possible output here is
  among `'-'` and `'0'..'9'`, so the model boundary excludes no result.
- **B3:** `baseAcc` definitionally states the standard quotient/remainder digit
  expansion, and the symbolic loop theorem connects it to execution. The
  independent most-significant-place oracle supplies additional finite
  evidence for the human-facing interpretation.
- **B4:** The implementation agrees with the contract and additionally handles
  zero and signed integers explicitly.

### Gate C — PASS

- Every proof-local extension and dependency is inventoried above.
- Every concrete, differential, and mutation claim names an existing artifact,
  exact command, scope, oracle, exit status, and observed result.
- Formal proof, conditional infrastructure trust, and finite empirical evidence
  are separated.

## Trust boundary

The result is conditional on the supplied read-only `reference-semantics/`,
the fixed `py2mpy.py` translation, K's reachability logic/Haskell backend, its
SMT reasoning, and the LLVM backend used for concrete evidence. No additional
operation is trusted by `verification.k`; in particular, there is no opaque
proof-local function and no rule that bypasses the program.

The supplied semantics models only an ASCII subset of Python strings, but that
boundary is immaterial here because the program can emit only ASCII sign and
digit characters.

## Empirically supported facts

- `concrete_tests.py` covers all three prompt examples plus zero, negative
  values, and a larger base-9 value under CPython and LLVM K execution.
- `differential_test.py` uses an independently written most-significant-place
  oracle over 4,008 cases. This supports the implementation-to-intent and
  model-to-CPython correspondence only for that finite sample; it is not used
  in place of the universal K proof.
- The two negative K artifacts demonstrate result and body sensitivity.

## Excluded behavior

- Bases below 2 are excluded because they are not valid positional numeral
  bases for this contract. In CPython, base 0 raises on `%`/`//`, while base 1
  does not decrease a positive magnitude; neither is silently assigned a
  conversion result.
- Bases 10 and above are excluded by the prompt's “less than 10” condition and
  would require a digit alphabet beyond the single decimal characters used
  here.
- Termination is not separately proved; the K theorem is a partial-correctness
  reachability proof.
