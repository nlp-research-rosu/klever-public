VALIDATED

## What is proven

Under the supplied MPY reference semantics, executing the exact translated
`valid_date` module on a string has the behavior required by `prompt.py`:

- every string whose length is not 10 returns `false`;
- a ten-character string returns `true` exactly when positions 2 and 5 are
  hyphens, the other positions are ASCII decimal digits, and the decoded
  month/day pair satisfies the prompt's 31-day, 30-day, or February-29 limit;
- function execution returns with environment 0, scope location 1, empty heap,
  heap location 0, empty call stack, `noRet`, `NoExc`, and exit code 0.

This is a partial-correctness result in the Kit sense. The program is loop-free,
so no loop invariant or circularity is present. The final module-scope map is
intentionally existential: loading the function changes that internal map, but
the prompt observes only the returned Boolean. Call-control and exception cells
are constrained.

## Formal claims

`SPEC.valid-date-10` quantifies independently over all ten character codes and
proves that fixed MPY execution returns `validDateResult` for that exact
ten-constructor `IntSeq`.

`SPEC.valid-date-non10` quantifies over every `IntSeq` satisfying
`isLen(CS) =/=Int 10` and proves that fixed MPY execution returns `false`.

These disjoint claims cover every concrete MPY string. A length-10 ground
`IntSeq` has exactly ten constructors; every other ground `IntSeq` satisfies
the second claim's precondition.

## Proof-extension inventory

There are no operational bridges, trusted result oracles, simplification
lemmas, priority overrides, or auxiliary circularity claims.

### `validDateProgram`

- **Class / role:** definitional summary used only as an exact name for the
  source AST. It expands to a `Module`; MPY still performs module loading, name
  lookup, argument evaluation, frame creation, every body statement, return
  unwinding, and frame cleanup.
- **Domain / matched context:** unconditional and total at every occurrence of
  the nullary `Module` symbol. It accepts no continuation, binding, control
  stack, or framed state.
- **Justification scope / containment:** its right-hand side is the exact parsed
  `solution.mpy` term. `kast` produced 37,017-byte KORE terms for both copies,
  and `cmp` exited 0. Since this is a context-independent source constant, its
  match and justification domains coincide.
- **State footprint:** none. Expansion only constructs syntax.
- **Value and control influence:** it selects the program whose execution
  produces the result and control behavior.
- **Justification / dependents:** exact AST identity; both target claims depend
  on it.
- **Validation:** concrete fixed-semantics execution passed. Mutating the
  executed February bound from 29 to 28 made the unchanged universal claim
  fail at the explicit `<= 28` versus `<= 29` obligation.

### `asciiDigit(Int)`

- **Class / role:** definitional summary; it never rewrites an MPY execution
  term.
- **Domain:** all mathematical integers, with one unconditional equation.
- **Matched context / state footprint:** only summary expressions; no cells,
  continuations, bindings, or control state.
- **Value influence:** the ten-character postcondition's Boolean.
- **Justification:** definition `48 <= C <= 57`, exactly the ASCII codes for
  `0` through `9`.
- **Coverage / overlap:** one unconditional equation, so total and
  non-overlapping.
- **Dependents / validation:** `validDateResult` and `valid-date-10`; checked by
  the universal proof, concrete MPY cases, and the differential suite.

### `validMonthDay(Int, Int)`

- **Class / role:** definitional summary; it does not replace execution.
- **Domain:** all integer month/day pairs, with one unconditional equation.
- **Matched context / state footprint:** summary expressions only; no
  operational context or cells.
- **Value influence:** the returned-result postcondition.
- **Justification:** a direct disjoint union of month 2 with days 1..29,
  months 4/6/9/11 with days 1..30, and months
  1/3/5/7/8/10/12 with days 1..31.
- **Coverage / overlap:** the equation is unconditional; the three month
  classes are pairwise disjoint.
- **Dependents / validation:** `validDateResult` and `valid-date-10`; the
  body-sensitivity mutation exposes the February boundary.

### `validDateResult(IntSeq)`

- **Class / role:** definitional result summary appearing only in the
  postcondition; it does not intercept calls, indexing, or returns.
- **Domain:** all `IntSeq` values. The guards `isLen(CS) =/=Int 10` and
  `isLen(CS) ==Int 10` are disjoint and exhaustive.
- **Matched context / state footprint:** summary expressions only; no state or
  control cells.
- **Value influence:** fixes the target result of `valid-date-10`.
- **Value justification:** the non-10 equation is `false`; the length-10
  equation checks the two separators, all eight digit positions, and the
  decoded month/day formula. Its indexed accesses are used by the proof only
  on the structurally ten-element input.
- **Dependents / validation:** `valid-date-10`; universally connected to the
  executed body by `#Top`, rejected after the body mutation, and supported by
  ground tests.

The two declarations in `spec.k` are target theorems, not assumptions used to
close one another.

## Exact commands and actual results

The complete reproducible command sequence is in `prove.sh`; its captured
output is in `prove.log`. The end-to-end command was:

```bash
bash -o pipefail -c './prove.sh 2>&1 | tee prove.log'
```

Actual result: exit 0.

The construction and positive proof commands were:

```bash
python3 py2mpy.py solution.py > solution.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
python3 test_solution.py
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.valid-date-10
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.valid-date-non10
```

Actual results:

- translation: exit 0;
- LLVM compilation: exit 0, with warnings from supplied unrelated generic
  definitions;
- `krun`: exit 0, final `<k> .K </k>`, `NoExc`, and exit code 0;
- differential test: exit 0,
  `tested=30010 mismatches=0`;
- Haskell compilation: exit 0, with unused-variable warnings from supplied
  `str.k`;
- `SPEC.valid-date-10`: `#Top`, exit 0;
- `SPEC.valid-date-non10`: `#Top`, exit 0.

The AST identity check used:

```bash
sed -n '13,166p' verification.k \
  | sed -e '1s/^[[:space:]]*=> //' -e 's/\.Stmts//g' \
  > verification-program.mpy
kast solution.mpy --definition runtime-kompiled \
  --module MPY-SYNTAX --sort Module --output kore \
  --output-file /tmp/solution.kore
kast verification-program.mpy --definition runtime-kompiled \
  --module MPY-SYNTAX --sort Module --output kore \
  --output-file /tmp/verification-program.kore
cmp /tmp/solution.kore /tmp/verification-program.kore
```

Actual result: both `kast` commands and `cmp` exited 0.

Gate A5 used:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual had
`<k> true ~> .K </k>` while the deliberately false destination required
`false`.

Body sensitivity used:

```bash
sed '137s/Int(29)/Int(28)/' verification.k > verification-mutant.k
sed -e '1s/verification.k/verification-mutant.k/' \
    -e 's/^module SPEC$/module SPEC-MUTANT/' \
    spec.k > spec-mutant.k
kompile verification-mutant.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-mutant-kompiled
kprove spec-mutant.k --definition verification-mutant-kompiled \
  --spec-module SPEC-MUTANT \
  --claims SPEC-MUTANT.valid-date-10
```

Actual result: mutant compilation exited 0; mutant proof exited 1 with
`WarnStuckClaimState`. The residual explicitly compared the executed
`day <= 28` result with the unchanged summary's `day <= 29`.

## Gate results

### Gate A — PASS

- **A1:** the parsed proof AST equals `solution.mpy`; fixed semantics executes
  the real definition, lookup, body, and return. The February body mutation
  invalidated the connection.
- **A2:** no operational bridge exists. The claims constrain result,
  environment, allocation counters, heap, stack, return state, exception
  state, and exit code.
- **A3:** lookup, argument order, indexing, frame control, short-circuiting,
  and return unwinding all execute under the supplied semantics.
- **A4:** all proof-local equations are truthful on their complete domains;
  total equations have exhaustive, non-overlapping coverage.
- **A5:** `03-11-2000` is a realizable witness. The false-result mutation was
  rejected with the real result `true`.

### Gate B — PASS

- **B1:** the formal domain is exactly the prompt's stated string domain.
  Non-string arguments are not claimed.
- **B2:** every construct used by the implementation is present in the
  supplied semantics. Character positions are modeled as integer code points;
  the implementation deliberately recognizes ASCII digits, the conventional
  meaning of the literal `mm-dd-yyyy` format.
- **B3:** `validDateResult` directly states separator, digit, month, and day
  constraints rather than merely naming an opaque execution result.
- **B4:** the implementation, formal property, prompt examples, and stated
  February rule agree. The prompt intentionally permits February 29 for every
  four-digit year; no leap-year rule was added.

### Gate C — PASS

The trust ledger is explicit below, every cited artifact exists, commands and
actual results are recorded, and formal conclusions are separated from finite
evidence and exclusions.

## Trust boundary

- **Supplied MPY reference semantics:** trusted as the execution model required
  by the task. It affects value, state, control, and exception behavior; both
  claims depend on it. LLVM smoke execution and the negative probes provide
  finite/path-sensitive evidence, not a universal proof that MPY equals all of
  CPython.
- **`py2mpy.py` and CPython AST parsing:** supplied and unmodified. They connect
  `solution.py` to `solution.mpy`; the generation command and parsed-KORE
  identity check provide reproducible evidence.
- **K toolchain, Haskell backend, SMT reasoning, and LLVM backend:** trusted
  proof/execution infrastructure. Version observed:
  `K v7.1.293` (build date 2025-10-03).

There is no proof-local trusted primitive or opaque result-bearing symbol.
Compiler warnings in `prove.log` concern generic supplied definitions not used
on this task's paths (float helpers, generic list/join/map cases, and unused
string-rule variables); they did not create proof-local assumptions.

## Empirically supported facts

- `concrete-tests.mpy` executes the exact translated body and asserts all five
  prompt examples plus `02-29-0000` and `02-30-2000`. LLVM execution ended in
  `.K` with no exception.
- `test_solution.py` uses an independently structured ASCII regular-expression
  parser and month-limit table. It checked every two-digit month/day pair for
  years `0000`, `2000`, and `9999`, plus malformed and Unicode-digit cases:
  30,010 inputs, zero mismatches.
- Parsed KORE equality connects the AST constant used in proof to the generated
  `solution.mpy`.

These finite checks support adequacy and identity; the universal result comes
from the two `#Top` proof commands.

## Excluded behavior

- Arguments that are not strings.
- Full CPython behavior outside the supplied MPY subset.
- Side effects in the final module-scope map, which are setup artifacts and not
  observable in the HumanEval contract.
- Termination as a separately proved liveness theorem; the reported K theorem
  is partial correctness, although this implementation is loop-free.
- Gregorian leap-year validation, because `prompt.py` explicitly gives
  February a maximum of 29 without a leap-year condition.
