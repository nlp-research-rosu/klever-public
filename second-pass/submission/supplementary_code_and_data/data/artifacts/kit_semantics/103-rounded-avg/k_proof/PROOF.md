VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, `rounded_avg` is partially
correct for the full prompt domain of two arbitrary positive symbolic
integers:

- If `n > m`, it returns `-1`.
- If `n <= m`, it returns a string with the literal prefix `0b`, followed by
  a nonempty canonical binary numeral whose numeric value is the nearest
  integer to the average of all integers from `n` through `m`, inclusive.
  Half-integer ties are rounded to even, as required by the prompt's
  `rounded_avg(20, 33) == "0b11010"` example.

The proof is not a finite-size or bounded-unrolling proof. `N` and `M` are
unbounded K `Int` variables, and the two target claims partition every pair
satisfying `N > 0` and `M > 0`.

## Formal claim

`spec.k` embeds the complete constructor translation of the function body and
then invokes it.

The `rounded-avg-invalid` claim has precondition

```k
N >Int 0 andBool M >Int 0 andBool N >Int M
```

and reaches the result `-1`.

The `rounded-avg-valid` claim has precondition

```k
N >Int 0 andBool M >Int 0 andBool N <=Int M
```

and reaches

```k
str(iCons(48, iCons(98, ?D:IntSeq)))
```

with

```k
bitValue(?D) ==Int roundedInt(N, M)
andBool allBits(?D)
andBool startsOne(?D)
```

Here `48, 98` are the character codes for `0b`. `allBits` restricts every
character of `?D` to `0` or `1`, `startsOne` excludes the empty numeral and
leading zeroes, and `bitValue` gives its positional binary value. Thus the
postcondition characterizes the canonical positive binary representation, not
merely some string with the right numeric interpretation.

For `S = N + M`, `roundedInt` is

```text
floor(S / 2) + (S mod 2) * (floor(S / 2) mod 2).
```

The inclusive arithmetic progression has average `S / 2`. The expression is
exact when `S` is even; when it is odd, it selects the even member of the two
nearest integers. The three exhaustive cases are also stated and proved in
`rounding-spec.k`.

## Proof-extension inventory

### `roundedInt`

- Class: definitional summary.
- Role and domain: names the integer expression computed by the assignment in
  `solution.py`; its single unguarded equation covers all K integers.
- Context and state: it does not rewrite program execution and reads or writes
  no configuration cells.
- Value influence: it appears in the valid target postcondition and the
  rounding claims.
- Justification: direct expansion of the translated integer expression.
  `rounding-spec.k` proves the even-sum, odd-sum/even-quotient, and
  odd-sum/odd-quotient cases. Those guards exhaust positive `N <= M`.

### `bitWeight`, `bitValue`, `allBits`, and `startsOne`

- Class: definitional summaries.
- Role and domain: structural definitions over all `IntSeq` constructors.
  `startsOne` has a first-character-`1` equation and a disjoint `[owise]`
  equation. The other definitions have empty and cons equations.
- Context and state: they only interpret a returned code-point sequence and
  never replace execution.
- Value influence: they define the binary-format and numeric postcondition.
- Justification: exhaustive, terminating structural recursion. Overlap is
  absent except for the deliberately disjoint `startsOne` `[owise]` case.

### `loopDigits`

- Class: definitional summary of the loop result.
- Role and domain: `loopDigits(V, A)` names the accumulator after the exact
  binary-digit loop. The concrete equations split all integers into `V <= 1`
  and `V > 1`. On the recursive branch,
  `(V - pyMod(V, 2)) / 2` is strictly smaller and nonnegative for the target
  domain. The symbolic `V == 1` base agrees with the concrete base. The
  guarded fold
  `loopDigits(Q, iCons(C, A)) =
  loopDigits(2*Q + C-48, A)` applies only for `Q >= 1` and `C` equal to a bit
  code; it is the reverse of one truthful loop step. Its overlaps therefore
  agree with the concrete equations.
- Context and state: the symbol itself does not replace execution. It affects
  the returned digits and all final result predicates.
- Value justification: `LOOP-CONNECTION.binary-loop-exact` in
  `connection-spec.k` is a bridge-free universal reachability proof using the
  fixed semantics plus the independently checked arithmetic equations. It
  proves the exact loop changes `value` from arbitrary `V > 0` to `1`, changes
  `digits` from `A` to `loopDigits(V, A)`, preserves the accepted continuation
  and surrounding configuration, and establishes the numeric and `allBits`
  invariants.

### Euclidean reconstruction equations

- Class: derived arithmetic lemmas.
- Domain:
  `2 * ((V - pyMod(V,2))/2) + pyMod(V,2) = V` for `V >= 0`, plus the same
  equation after the reference semantics expands `pyMod`.
- Role: they let the symbolic loop proof reconstruct the pre-step integer.
- Context and state: simplifications over integers only; no program term or
  configuration cell is replaced.
- Justification: both equations are independently proved by
  `arithmetic-spec.k` against `ARITHMETIC-VERIFICATION`, which imports only the
  supplied `MPY` semantics and does not import either equation.
- Dependents: the loop connection proof, and through it the operational bridge
  and valid target claim.

### Exact binary-loop operational bridge

- Class: operational bridge.
- Match domain: the exact translated `#while` term, an arbitrary framed
  continuation, `<env> 1`, the exact active function scope containing
  `n`, `m`, positive `value = V`, and bit-string `digits = A`, the module
  parent scope, and the supplied builtins scope. The guard also requires
  `allBits(A)` and that the module scope does not shadow `chr`.
- Binding and evaluation: the builtins map is pinned to `builtinsScope`; the
  no-shadowing guard therefore selects the supplied `chr`. Each loop iteration
  evaluates positive-integer comparison, remainder, `chr(48 or 49)`, string
  concatenation, and integer division in the same order as the exact body.
- State footprint: it reads `<k>`, `<env>`, and `<scopes>`; consumes only the
  loop; changes only active-scope `value` and `digits`; preserves `n`, `m`,
  module bindings, parent links, builtins, the arbitrary continuation, and all
  omitted/framed cells. No return, frame pop, break, exception propagation,
  output, heap access, or allocation is introduced.
- Justification scope and containment:
  `connection-spec.k` uses the same loop, continuation frame, scopes, bindings,
  guards, and state transition. It imports `verification-base.k`, not
  `verification.k`, so it cannot use the bridge it justifies. Every bridge
  match is within that universal theorem's domain.
- Control and value validation: fixed and bridge-enabled runs of `smoke.mpy`
  have byte-identical final configurations, including boundary witnesses
  `rounded_avg(1,1)` (`V = 1`) and `rounded_avg(2,2)` (one loop iteration).
  Changing the displaced loop's character base from `48` to `47` in
  `connection-body-mutation.k` makes the bridge-free connection proof get
  stuck and exit 1.
- Dependents: the full valid target claim. The invalid claim returns before the
  loop and does not use it.

### Loop-result simplifications

- Class: derived lemmas.
- Domain: `V > 0 and allBits(A)`, exactly the connection theorem's value
  domain.
- Statements: the binary numeric invariant (including its syntactically
  normalized `1 * bitWeight` form) and
  `allBits(loopDigits(V,A)) = true`.
- Context and state: pure simplifications; no execution term or cell changes.
- Justification: they are orientations of the `ensures` facts proved by the
  bridge-free `LOOP-CONNECTION.binary-loop-exact` claim.
- Dependents: the valid target postcondition.

There are no fresh unconstrained result symbols, opaque program-derived
values, or trusted custom primitives in the target proof.

## Exact commands and actual outputs

Tool versions:

```sh
kompile --version
krun --version
kprove --version
```

All three reported K `v7.1.293`.

Translation and CPython evidence:

```sh
python3 py2mpy.py solution.py > solution.mpy
python3 test_solution.py
```

Actual test output:

```text
CPython examples: 4/4
Independent differential grid: 10000/10000; mismatches: 0
```

A separate regeneration followed by `cmp solution.mpy
/tmp/solution-final.mpy` reported `TRANSLATION_IDENTITY:OK`.

Concrete fixed-semantics execution:

```sh
python3 py2mpy.py smoke.py > smoke.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual result: exit 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. The six assertions include all four prompt
examples and the `V = 1` and `V = 2` bridge-boundary witnesses.

Independent arithmetic-lemma proof:

```sh
kompile --backend haskell arithmetic-verification.k \
  --main-module ARITHMETIC-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition arithmetic-kompiled
kprove arithmetic-spec.k \
  --definition arithmetic-kompiled \
  --spec-module ARITHMETIC-SPEC
```

Actual result: `#Top`, exit 0. The backend also emitted
`WarnTrivialClaim` for the two arithmetic claims.

Bridge-free loop connection and rounding cases:

```sh
kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module LOOP-CONNECTION
kprove rounding-spec.k \
  --definition connection-kompiled \
  --spec-module ROUNDING-SPEC
```

Actual results: `#Top`, exit 0 for the universal loop connection; `#Top`,
exit 0 for all three rounding claims.

Target proof:

```sh
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.rounded-avg-invalid
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.rounded-avg-valid
```

Actual results: invalid claim `#Top`, exit 0; valid claim `#Top`, exit 0.
Compilation and proof emitted only unused-variable warnings originating in the
supplied semantics or framed proof variables.

Fixed-versus-bridged concrete comparison:

```sh
krun smoke.mpy --definition runtime-kompiled > /tmp/runtime-smoke-final.out
krun smoke.mpy --definition verification-kompiled > /tmp/bridge-smoke-final.out
cmp /tmp/runtime-smoke-final.out /tmp/bridge-smoke-final.out
```

Actual result: `cmp` exit 0 (`FIXED_AND_BRIDGED_SMOKE_MATCH:OK`).

Negative validation:

```sh
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
kprove connection-body-mutation.k \
  --definition connection-kompiled \
  --spec-module LOOP-CONNECTION-MUTATION
```

Actual results, in order:

```text
VACUITY_EXIT:1
BODY_MUTATION_EXIT:1
CONNECTION_MUTATION_EXIT:1
```

Each emitted `WarnStuckClaimState` followed by a prover error. The first changes
the satisfiable witness `(1,1)` postcondition from value `1` to value `2`; the
second changes the executed function's returned prefix from `0b` to `0c`; the
third changes the displaced loop's digit base from `48` to `47`.

`prove.sh` records the reproducible build, execution, target-proof, comparison,
and expected-failure commands. Its expected-failure wrapper requires each
negative probe to return nonzero.

## Gate results

- Gate A — PASS. The target claims contain the exact complete translated
  function body. Every result-bearing definition is exhaustive and terminating
  on its use domain. The only operational bridge has a bridge-free universal
  connection theorem over its complete context and state footprint. Arithmetic
  helpers have independent K proofs. A satisfiable ground witness exists, the
  false postcondition is rejected, the material whole-body mutation is
  rejected, and the loop mutation is rejected.
- Gate B — PASS. The two claims cover all unbounded positive integer pairs and
  no fixed sizes are assumed. Their postconditions match the prompt's `-1`,
  inclusive-average, ties-to-even rounding, `0b` prefix, and canonical binary
  behavior. The `(20,33)` example specifically confirms the even choice at
  `26.5`.
- Gate C — PASS. All assumptions and model boundaries are listed below. Every
  claimed proof, concrete comparison, differential test, and mutation has an
  artifact, command, scope, oracle where applicable, actual result, and exit
  status. Finite evidence is not used as a substitute for the universal
  execution-connection theorem.

## Trust boundary

- The supplied, unmodified `reference-semantics/` definition is trusted as the
  Python execution model requested by the benchmark.
- The supplied, unmodified `py2mpy.py` is trusted as the CPython-AST to
  constructor translator. Regeneration is byte-identical, and `spec.k` embeds
  that complete constructor body.
- K `v7.1.293`, its Haskell/LLVM backends, the SMT/arithmetic implementation,
  and the host needed to execute them are trusted.
- The supplied `MPY` integer, string, comparison, call, scope, and `chr`
  definitions are trusted primitives. `chr` is not opaque here: the bridge
  proves the fixed execution, pins its builtins binding, and invokes it only at
  code points 48 and 49.
- No proof-local rule is accepted merely from testing. The execution bridge,
  result-bearing loop summary, and arithmetic reconstruction facts have the
  machine-checked connection or auxiliary claims described above.

## Empirically supported facts

`test_solution.py` independently constructs `range(n, m + 1)`, computes its
sum and length, applies CPython `round`, and then CPython `bin`. It checks every
ordered pair `1 <= n,m <= 100`, including both valid and `n > m` branches:
10,000 cases and zero mismatches. It also checks all four examples explicitly.
This is finite supporting evidence only.

`smoke.py` checks the four prompt examples plus `(1,1)` and `(2,2)` under the
LLVM fixed semantics. The same artifact reaches a byte-identical final
configuration with the proof definition, providing finite boundary evidence
for the operational bridge. The universal bridge-free K claim, not this
comparison, establishes the bridge for arbitrary positive values.

The three negative artifacts establish proof sensitivity at concrete
satisfiable witnesses. They do not establish the positive theorem; the
positive `#Top` runs do.

## Excluded behavior

- Inputs that are zero, negative, non-integer, or missing are outside the
  prompt's positive-integer signature and outside the formal preconditions.
- The theorem is stated in the supplied mathematical K integer/string model.
  CPython implementation resource limits, finite memory, platform behavior,
  and values or exceptions absent from the supplied semantics are not modeled.
- This is a partial-correctness reachability report under the Kit contract. No
  claim is made about wall-clock or memory consumption for concrete enormous
  integers.
