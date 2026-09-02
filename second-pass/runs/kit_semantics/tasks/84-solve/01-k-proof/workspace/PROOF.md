VALIDATED

## What is proven

Using the supplied `MPY` semantics, the claims prove partial correctness of the
exact K AST translated from `solution.py`.

For every integer `N` in the prompt domain `0 <= N <= 10000`, `solve(N)`:

- returns an ASCII string containing a canonical binary numeral;
- returns a numeral whose positional base-two value equals the sum of the
  decimal digits of `N`;
- finishes with an empty continuation and call stack, `noRet`, `NoExc`, exit
  code `0`, and unchanged empty heap/resource counters.

The module scope is intentionally not part of the postcondition because module
loading installs the `solve` closure there; the HumanEval contract observes the
function result, not the retained module binding.

## Formal claim

The input is parameterized in Horner form:

```text
N = D0 + 10 * (D1 + 10 * (D2 + 10 * (D3 + 10 * D4)))
S = D0 + D1 + D2 + D3 + D4
```

`digitDomain(D0,D1,D2,D3,D4)` requires `D0..D3` to be decimal
digits and either:

- `D4 = 0`, representing exactly `0..9999`; or
- `D4 = 1` and all lower digits are zero, representing `10000`.

Thus the parameterization covers exactly the complete prompt domain. The
machine-checked `digit-sum-bound` claim proves `0 <= S <= 36`.

The five program claims partition that complete range:

```text
SPEC.solve-sum-00-07
SPEC.solve-sum-08-15
SPEC.solve-sum-16-23
SPEC.solve-sum-24-31
SPEC.solve-sum-32-36
```

Every claim executes:

```k
#loadAll(solutionModule) ~> Call(Name("solve"), N)
```

from the initial MPY configuration and constrains the returned value to
`str(?CODES)` with:

```k
canonicalBin(?CODES)
andBool decodeBin(?CODES) ==Int S
```

Together with `SPEC.digit-sum-bound`, these claims cover the full HumanEval
contract rather than a bounded sample of it.

## Proof-extension inventory

### `solutionModule`

- **Class:** definitional summary.
- **Semantic role:** names the exact `Module(...)` AST; `#loadAll` and all
  program-defined code still execute under fixed semantics.
- **Domain/context:** nullary, unconditional, and total in any pure term
  context.
- **State footprint:** none for the equation itself.
- **Value/control influence:** selects the program body loaded and called by
  every target claim.
- **Justification:** its RHS is the exact `solution.mpy` text embedded between
  the `BEGIN/END SOLUTION MPY` markers.
- **Dependents:** all five program claims and the vacuity/body-mutation probes.
- **Validation:** `prove.sh` regenerates `solution.mpy` and byte-compares it
  with the embedded AST. The check exits `0`. Mutating the digit-sum-6 return
  invalidates the corresponding symbolic proof.

### Decimal remainder simplifier

Exact extension:

```k
rule (((D +Int 10 *Int Q) %Int 10 +Int 10) %Int 10) => D
  requires 0 <=Int D andBool D <Int 10
  [simplification]
```

- **Class:** operational bridge over a pure integer term, justified as a
  derived arithmetic equality.
- **Semantic role:** accelerates the exact expanded `pyMod(D + 10*Q,10)` term
  produced by fixed `MPY-INT`; it does not intercept lookup, `BinOp`, binding,
  assignment, branching, return, or frame handling.
- **Domain/context:** all integers `Q`, decimal digit `D`, and any
  simplification context.
- **Justification scope/containment:** bridge-free claims
  `BRIDGE-SPEC.mod10-horner` and `BRIDGE-SPEC.mod10-expanded` import only
  `MPY`. They quantify an arbitrary continuation `REST:K`. The expanded claim
  establishes the pure term equality universally, so substitutivity contains
  every simplifier context.
- **State footprint:** reads/writes/abstracts no cell and preserves the
  arbitrary continuation.
- **Value influence:** fixes each extracted decimal digit, which affects the
  returned branch and postcondition.
- **Value justification:** the bridge-free claims print `#Top`; the ground
  opposite value `157 % 10 = 8` is rejected and exposes fixed result `7`.
- **Dependents:** all five target program claims.
- **Control validation:** no control effect; fixed evaluation and the lemma
  produce the same integer before the unchanged continuation.

### Decimal quotient simplifier

Exact extension:

```k
rule ((D +Int 10 *Int Q -Int D) /Int 10) => Q
  requires 0 <=Int D andBool D <Int 10
  [simplification]
```

- **Class:** operational bridge over a pure integer term, justified as a
  derived arithmetic equality.
- **Semantic role:** accelerates the exact quotient term left after fixed
  `MPY-INT` expands `// 10`.
- **Domain/context:** all integers `Q`, decimal digit `D`, and any
  simplification context.
- **Justification scope/containment:** bridge-free claims
  `BRIDGE-SPEC.floordiv10-horner` and
  `BRIDGE-SPEC.quotient-expanded` import only `MPY`, quantify arbitrary
  `REST:K`, and establish the universal pure equality.
- **State footprint:** none; continuation and all configuration cells are
  preserved.
- **Value influence:** fixes the successive decimal tails used by later
  digit extractions.
- **Value justification:** the bridge-free claims print `#Top`; the ground
  opposite value `157 // 10 = 16` is rejected and exposes fixed result `15`.
- **Dependents:** all five target program claims.
- **Control validation:** no control effect or exceptional behavior is
  introduced.

The two arithmetic guards are truthful, have no conflicting overlap with one
another, and agree with the fixed MPY equations wherever they overlap them.

### `decodeBin`

- **Class:** definitional summary.
- **Semantic role:** defines positional base-two decoding; it never replaces
  program execution.
- **Domain:** every `IntSeq`.
- **Coverage/descent:** `.IntSeq` is the base case; `iCons(C,R)` recurses on
  the strict tail `R`. The cases are disjoint and exhaustive.
- **Value influence:** states the numeric portion of the postcondition.
- **Justification:** standard positional definition
  `(C-48)*2^len(R)+decodeBin(R)`.
- **Dependents:** all five target claims and the vacuity probe.
- **Validation:** every executed result is ground and reduces through these
  equations; exhaustive Python differential evidence independently agrees.

### `allBinDigits` and `canonicalBin`

- **Class:** definitional summaries.
- **Semantic role:** define binary syntax and exclude empty strings and
  leading zeroes other than the numeral `"0"`.
- **Domain:** every `IntSeq`.
- **Coverage/descent:** `allBinDigits` has disjoint empty/cons cases and
  strictly descends. `canonicalBin` has disjoint `"0"`, leading-`"1"`, and
  `[owise]` cases; together they are total.
- **State footprint:** none.
- **Value influence:** constrain the returned string syntax.
- **Dependents:** all five target claims and the vacuity probe.
- **Validation:** all target claims close; concrete and exhaustive
  differential tests return canonical Python binary strings.

### `digitDomain`

- **Class:** definitional summary.
- **Semantic role:** records the exact symbolic input parameterization.
- **Domain/coverage:** unconditional total equation over five integers.
- **Value influence:** supplies target preconditions and the decimal digit sum.
- **Justification:** positional decimal representation described above.
- **Dependents:** the bound claim and all five target claims.
- **Validation:** `SPEC.digit-sum-bound` prints `#Top`; `test_solution.py`
  independently enumerates 10,001 unique representations and checks that their
  set is exactly `0..10000`.

### Auxiliary claims

- `BRIDGE-SPEC.mod10-horner`, `floordiv10-horner`, `mod10-expanded`, and
  `quotient-expanded` are bridge-free universal connection claims. Their
  definition imports only the supplied `MPY` semantics.
- `SPEC.digit-sum-bound` is a derived Presburger arithmetic claim proving the
  five program ranges cover every possible digit sum.
- None of these claims assumes the requested program result.

There are no opaque program-derived values, trusted result oracles, loop
circularities, or rules that skip the `solve` body.

## Exact commands and actual outputs

Toolchain:

```bash
kompile --version
kprove --version
```

Actual version for both:

```text
K version: v7.1.293
```

Translation, source identity, and independent evidence:

```bash
python3 py2mpy.py solution.py > solution.mpy
cmp -s solution.mpy \
  <(sed -n '/BEGIN SOLUTION MPY/,/END SOLUTION MPY/p' verification.k \
      | sed '1d;$d;s/^    //')
python3 test_solution.py
```

Actual exits: `0`, `0`, `0`. Actual test output:

```text
digit-domain-check: 10001 unique representations cover 0..10000
python-differential-check: 10001/10001 passed; mismatches=0
```

Concrete LLVM build and execution:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun \
  <(sed '$a\
assert solve(1000) == "1"\
assert solve(150) == "110"\
assert solve(147) == "1100"\
assert solve(0) == "0"\
assert solve(9999) == "100100"' solution.py \
    | python3 py2mpy.py /dev/stdin) \
  --definition runtime-kompiled
```

Actual exits: `0`, `0`. `concrete.log` ends with `.K`, `NoExc`, and exit code
`0`. Compiler warnings are inherited reference-semantics coverage/unused
variable warnings and do not change those results.

Bridge-free definition and connection proof:

```bash
kompile --backend haskell bridge-verification.k \
  --main-module BRIDGE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition bridge-verification-kompiled

kprove bridge-spec.k \
  --definition bridge-verification-kompiled \
  --spec-module BRIDGE-SPEC
```

Actual exits: `0`, `0`. Actual proof output:

```text
#Top
```

`WarnTrivialClaim` on these arithmetic claims means the bridge-free backend
discharged their implications without operational rewriting; it is not a
failure.

Main symbolic definition and complete target proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual exits: `0`, `0`. Actual complete target output:

```text
#Top
```

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual exit: `1`, expected. `vacuity.log` contains
`WarnStuckClaimState`; fixed execution returns `"110"` for `N=150`, while the
mutated postcondition requires decoded value `7`.

Opposite arithmetic-value probes:

```bash
kprove bridge-negative-spec.k \
  --definition bridge-verification-kompiled \
  --spec-module BRIDGE-NEGATIVE-SPEC \
  --claims BRIDGE-NEGATIVE-SPEC.wrong-mod

kprove bridge-negative-spec.k \
  --definition bridge-verification-kompiled \
  --spec-module BRIDGE-NEGATIVE-SPEC \
  --claims BRIDGE-NEGATIVE-SPEC.wrong-floordiv
```

Actual exits: `1`, `1`, expected. The residuals expose fixed values `7` and
`15` rather than the requested wrong values `8` and `16`.

Body-sensitivity probe:

```bash
sed '0,/Return(Str("110"))/s//Return(Str("111"))/' \
  verification.k > verification-mutant.k
sed 's/requires "verification.k"/requires "verification-mutant.k"/' \
  spec.k > spec-mutant.k
kompile --backend haskell verification-mutant.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-mutant-kompiled
kprove spec-mutant.k \
  --definition verification-mutant-kompiled \
  --spec-module SPEC \
  --claims SPEC.solve-sum-00-07
```

Actual compile exit: `0`. Actual proof exit: `1`, expected, with
`WarnStuckClaimState`. The mutant returns `"111"` on digit sum `6`, so the
postcondition fails.

All commands, output checks, and expected-failure handling are executable as:

```bash
./prove.sh
```

The end-to-end runner exits `0` only when both positive proof commands contain
`#Top` and every negative probe exits nonzero with a stuck state.

## Gate results

### Gate A — PASS

- A1: the exact translated function body is loaded and executed. Source/AST
  identity passes, and a material return-body mutation makes the symbolic proof
  fail.
- A2: no bridge reads or mutates configuration state. Target claims additionally
  constrain clean return/control/resource cells.
- A3: fixed semantics performs lookup, argument evaluation, frame binding,
  assignments, branches, returns, and frame restoration. Arithmetic
  simplifiers preserve an arbitrary continuation and are universally connected
  to fixed MPY evaluation.
- A4: all definitions have disjoint/exhaustive cases or a single unconditional
  equation; recursive definitions descend structurally. Both arithmetic
  equations are universally proved under their complete guards.
- A5: the precondition is realizable; `N=150` is a witness. The false result,
  two opposite arithmetic values, and body mutation are all rejected.

### Gate B — PASS

- B1: the symbolic digit parameterization covers exactly every integer
  `0..10000`; it is not a sample or bounded unrolling of a broader prompt
  domain.
- B2: MPY integers exactly cover the required bounded arithmetic. Every emitted
  character is ASCII `0` or `1`; the semantics' ASCII string boundary therefore
  creates no missing contract value.
- B3: `canonicalBin` plus `decodeBin` is the formal meaning of the requested
  binary numeral, and the target claims connect fixed execution to that
  property.
- B4: implementation, examples, and the stated contract agree, including
  `N=0` from the explicit `0 <= N` constraint.

### Gate C — PASS

- Every proof extension, assumption, dependent claim, state footprint, and
  value influence is recorded above.
- All named evidence has a checked-in artifact or exact command in `prove.sh`.
- Universal connections are machine-checked; finite evidence is reported only
  as evidence, not as a replacement for proof.
- Formal results, expected-failure probes, trust assumptions, and excluded
  behavior are separated.

## Trust boundary

| Component | Role and influence | Dependents | Evidence/handling |
|---|---|---|---|
| Supplied `reference-semantics/` | Fixed model of Python evaluation; affects value, control, state, and exceptions | All K executions and proofs | Used read-only and imported unchanged |
| K v7.1.293 Haskell backend and SMT reasoning | Establishes reachability and arithmetic implications | All `#Top` results | Exact build/proof commands and logs |
| K LLVM backend | Concrete MPY execution | Concrete examples only | `.K`, `NoExc`, exit `0` in `concrete.log` |
| Supplied `py2mpy.py` | Translates CPython AST to MPY AST | Program identity | Regenerated output byte-matches `solutionModule` |
| CPython built-ins in `test_solution.py` | Independent executable oracle | Empirical validation only | Exhaustive 10,001-input run, zero mismatches |

No external primitive or opaque value is assumed to determine the returned
result.

## Empirically supported facts

- `test_solution.py` exhaustively checks all 10,001 permitted inputs against an
  oracle implemented with CPython `str`, `int`, `sum`, and `format(...,"b")`.
  Result: zero mismatches.
- The same artifact exhaustively checks that the formal digit tuples give
  exactly 10,001 unique values equal to `set(range(10001))`.
- Concrete LLVM/MPY execution checks the three prompt examples and boundary
  witnesses `0` and `9999`, with no exception.

These runs validate the implementation and model alignment on their stated
finite scopes; the universal K claims provide the formal proof.

## Excluded behavior

- Inputs outside `0..10000`.
- Non-integer Python inputs and Python subclass/identity behavior not present in
  the prompt's integer contract.
- Total-correctness/liveness beyond the Kit's stated partial-correctness
  theorem. The implementation is straight-line with finite conditionals, but
  termination is not a separate K liveness claim.
- The final module-scope map is not constrained because loading the module
  intentionally installs the `solve` closure; it is not part of the HumanEval
  observable result.
