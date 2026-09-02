VALIDATED

# What is proven

Under the supplied MPY semantics, the exact translated body of
`choose_num` returns the greatest even integer in the inclusive interval
`[x, y]`, or `-1` when no such integer exists, for every symbolic pair of
positive integers `x` and `y`.  The domain is unbounded: the proof has no
finite-size, finite-value, or unrolling restriction.

This is a K partial-correctness result.  The implementation is straight-line,
so there is no loop invariant or bounded execution argument.

# Formal claims

`spec.k` contains two claims, and the target `kprove` command proves both in
one run.

1. `SPEC.load-choose-num` symbolically executes `#loadAll` on the exact
   `Module(FuncDef(...))` term emitted in `solution.mpy`.  It proves that MPY
   installs the exact function body and parameter list as the
   `"choose_num"` closure in the module scope while preserving the remaining
   initial configuration.
2. `SPEC.choose-num` invokes that exact closure with unconstrained
   `X:Int` and `Y:Int`, subject only to
   `X >Int 0 andBool Y >Int 0`.  It consumes the call and leaves
   `?R:Int`, with
   `?R ==Int chooseNumSpec(X, Y)`.  The environment, scopes, allocation
   counters, heap, stack, return state, exception state, and exit code are
   explicitly constrained.

`chooseNumSpec` is the following exhaustive result characterization:

- `-1` when `X > Y`;
- `Y` when `X <= Y` and `Y` is even;
- `Y - 1` when `X <= Y`, `Y` is odd, and `Y - 1 >= X`;
- `-1` when `X <= Y`, `Y` is odd, and `Y - 1 < X`.

For integer endpoints this is exactly the requested greatest-even property.
If the interval is nonempty and `Y` is even, no integer in it is greater than
`Y`.  If `Y` is odd, `Y - 1` is the immediately preceding integer and is
even; it is therefore the greatest even candidate when it lies in the
interval.  If it lies below `X`, integrality implies `X = Y`, so the interval
contains only the odd value `Y` and has no even member.

# Proof-extension inventory

## `chooseNumSpec` and its four equations

- **Class:** Definitional summary.
- **Semantic role:** Names the mathematical returned value; it never rewrites
  `Call`, `FuncDef`, a source AST node, a continuation, or any MPY execution
  step.
- **Domain:** All pairs in `Int × Int`.  The outer guards `X > Y` and
  `X <= Y` are exhaustive and disjoint.  In the latter region,
  `pyMod(Y, 2) == 0` and `pyMod(Y, 2) =/= 0` are exhaustive and disjoint.
  In the odd region, `Y - 1 >= X` and `Y - 1 < X` are exhaustive and
  disjoint.  Thus `[total]` is justified, and no pair of rules overlaps.
- **Matched context:** Pure `chooseNumSpec(X, Y)` terms only; there is no
  active continuation, binding lookup, control stack, wildcard cell, or
  omitted operational cell.
- **Justification scope and containment:** The exhaustive integer case split
  above applies to every term matched by the equations.
- **State footprint:** Reads and writes no MPY cell.
- **Value influence:** Its value occurs only in the target claim's final
  equality.
- **Value justification:** The four equations are the case definition proved
  equivalent to the greatest-even contract by the integer argument above.
  Program execution is independently performed by fixed MPY rules.
- **Dependents:** `SPEC.choose-num`.
- **Control validation:** Not applicable; this is not an operational bridge.
- **Value validation:** `SPEC.choose-num` machine-connects fixed execution to
  the summary for all positive integer inputs.  `differential_test.py`
  independently compares the Python implementation with a descending-domain
  brute-force oracle over 40,000 pairs.  The false-result mutation is rejected.
- **Validation:** Exhaustiveness and overlap were audited; Gate A4 and A5 pass.

## `SPEC.load-choose-num`

- **Class:** Derived auxiliary execution claim.
- **Semantic role:** Executes the supplied `#loadAll` and `FuncDef` rules; it
  does not add a rewrite or replace execution.
- **Domain and context:** The exact `solution.mpy` module in the complete
  initial MPY configuration.
- **Justification scope and containment:** Exactly the configuration stated
  by the claim; no continuation or cell frame is widened.
- **State footprint:** The fixed semantics adds the closure to module scope.
  All other cells are explicitly preserved.
- **Value/control justification:** Machine-checked by `kprove` using only MPY
  plus the independently audited `chooseNumSpec` definition, which this claim
  does not use.
- **Dependents:** It connects the translated source module to the exact closure
  used by `SPEC.choose-num`.
- **Validation:** The target run proves it.  The separately corrupted closure
  in `spec-body-mutation.k` is rejected by the result theorem.

There are no proof-local operational bridges, simplification rules, priority
rules, opaque values, or trusted primitives.

# Exact commands and actual results

The complete executable record is `prove.sh`.  It was run as:

```bash
chmod +x prove.sh
./prove.sh
```

The script exited `0`.  Its component commands and observed results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
```

Both exited `0`.  The final `solution.mpy` contains the exact function term
used by `SPEC.load-choose-num`.

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit `0`.  The compiler emitted supplied-semantics warnings about
non-exhaustive functions in unrelated float/string/list helpers and unused
`As`/`Bs` variables in `str.k`; it emitted no error.

```bash
krun smoke.mpy --definition runtime-kompiled
```

Exit `0`.  The actual final configuration had `<k> .K </k>`,
`<ret> noRet </ret>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`.  Thus all seven MPY `Assert` statements passed,
including the two prompt examples and the odd singleton boundary `(1, 1)`.

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit `0`.  The only output was the supplied `str.k` unused-variable warnings.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Exit `0`.  Actual proof result:

```text
#Top
```

The compiler also repeated the supplied `str.k` unused-variable warnings.

```bash
python3 differential_test.py
```

Exit `0`.  Actual output:

```text
differential: 40000 positive-integer pairs, 0 mismatches
```

The oracle constructs every integer in `[x, y]`, filters for even values, and
takes `max`, returning `-1` for an empty candidate set.  The tested scope was
the Cartesian product `1 <= x <= 200`, `1 <= y <= 200`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual exit `1`, as required.  The stuck residual contained `<k> 14 ~> .K
</k>` while the deliberately false postcondition required `15`, followed by
`[Error] Prover: backend terminated because the configuration cannot be
rewritten further.`

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual exit `1`, as required.  The mutation changed the even branch to return
`y + 2`; the witness call `(12, 14)` reached the stuck residual
`<k> 16 ~> .K </k>` instead of the required `14`.

# Gate results

## Gate A — PASS

- **A1:** The exact program-defined body executes under fixed MPY semantics.
  The source-loading claim connects the translated `FuncDef` to the closure.
  The body-sensitivity mutation is rejected.
- **A2:** No execution is skipped.  The target claim explicitly constrains
  every MPY state cell before and after the call.
- **A3:** Fixed MPY rules perform name lookup, left-to-right argument
  evaluation, parameter binding, branching, return, frame popping, and scope
  restoration.  There is no bridge whose match context could be wider than a
  connection theorem.
- **A4:** The only new equations are truthful, terminating, exhaustive, and
  pairwise disjoint over all integers.
- **A5:** `(X, Y) = (12, 15)` is a realizable positive witness.  The false
  result `15` is rejected with an observed result of `14`.

## Gate B — PASS

- **B1:** The formal domain is every positive integer pair, matching the
  contract's integer/parity domain.  There is no bound on values or interval
  width.  The prompt examples are included.
- **B2:** MPY `Int` uses mathematical unbounded integers, matching Python's
  relevant integer behavior here.  Positive inputs avoid type and exceptional
  cases, and modulo is the supplied Python-style `pyMod`.
- **B3:** The exhaustive case argument above connects the execution summary
  to “greatest even integer in `[x, y]`, else `-1`.”  The independent
  brute-force differential test supplies additional finite evidence.
- **B4:** The implementation and the stated property agree, including the
  empty interval and odd-singleton cases.

## Gate C — PASS

- Every unproved boundary is listed below with its dependents.
- Every concrete, differential, and mutation statement above names an
  existing artifact, exact command, input scope, oracle where applicable, and
  actual result.
- Formal proof, mathematical adequacy reasoning, finite evidence, and excluded
  behavior are kept distinct.

# Trust boundary

- **Supplied MPY semantics:** `reference-semantics/semantics.k` and its imported
  modules are fixed and read-only.  The claims depend on their modeling of
  module loading, integer operations, comparison, calls, conditionals, return,
  and frames.  The proof does not establish that the supplied semantics is a
  complete model of CPython.
- **Translator:** `py2mpy.py` is supplied and fixed.  The loading claim proves
  the emitted constructor term under MPY; fidelity of the supplied
  CPython-AST-to-constructor translator is outside the K theorem.
- **Toolchain:** K v7.1.293, the Haskell backend, its integer reasoning, and
  the LLVM backend are trusted implementations.  `SPEC.choose-num` depends on
  them for symbolic closure; the smoke run depends on LLVM execution.
- **Partial correctness:** The K result is a reachability/partial-correctness
  theorem.  Source termination is evident from the finite straight-line
  control flow, but no separate liveness theorem is claimed.

The supplied compiler warnings concern fixed-semantics symbols not reached by
this integer-only function.  No proof-local assumption depends on those
symbols.

# Empirically supported facts

- LLVM MPY execution passed seven concrete assertions.
- CPython execution agreed with an independent brute-force oracle for 40,000
  positive integer pairs.
- The target is result-sensitive and body-sensitive on the recorded ground
  witnesses.

These finite results support translation/model adequacy and sensitivity; they
are not used as a substitute for the universal symbolic K proof.

# Excluded behavior

- Zero and negative endpoints are outside the prompt's positive-input
  precondition.
- Non-integer Python values are outside the integer/parity input domain used by
  this HumanEval contract.
- Behavior outside the supplied MPY subset, arbitrary rebinding of
  `choose_num`, CPython implementation details, and resource exhaustion are not
  claimed.
