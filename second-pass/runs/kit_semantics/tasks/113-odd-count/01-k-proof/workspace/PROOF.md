VALIDATED

## What is proven

Under the supplied `MPY` semantics, `solution.py` is partially correct for every
finite list of finite digit strings representable by that semantics. If
`odd_count` terminates, it returns a fresh list with one output string for each
input string, in the same order. For an input string `s`, let

```text
n = s.count("1") + s.count("3") + s.count("5")
    + s.count("7") + s.count("9")
```

The corresponding output is:

```text
"the number of odd elements " + str(n)
+ "n the str" + str(n)
+ "ng " + str(n)
+ " of the " + str(n)
+ "nput."
```

Because the formal input predicate admits exactly strings whose codes are
digits `0` through `9`, this `n` is the number of odd digits. The proof is over
symbolic, unbounded `ValSeq` and `IntSeq` structures, not finitely many lengths
or examples.

This is a partial-correctness result. Termination is not a conclusion of
`kprove`.

## Formal claims

`spec.k` partitions all finite input lists by their constructors:

- `SPEC.odd-count-empty` proves the entry computation for `.ValSeq`.
- `SPEC.odd-count-cons` proves it for
  `vCons(HEAD, REST)` under
  `allDigitStrings(vCons(HEAD, REST))`. `REST` is symbolic and unbounded.
- `SPEC.outer-loop-cons` is the circularity for the nonempty outer loop. Its
  recursive use handles every later constructor, while the fixed semantics
  handles the empty tail.

The two entry claims therefore cover every finite list: every list is either
empty or a head followed by an arbitrary finite rest.

The observable post-state is:

- `<k>` contains the returned `ref(0)`;
- heap location `0` contains
  `list(oddLinesAcc(.ValSeq, INPUT))`;
- the caller environment, scopes, stack, return state, exception state, and
  exit code have their stated final values.

The function-local `s`, `count`, and `count_string` values are observed by the
loop circularity because they are needed to connect iterations, but they are
deallocated when the call returns.

The loop invariant is accumulator based:

```text
heap[0] = list(ACC)
remaining input = VS
eventual heap[0] = list(oddLinesAcc(ACC, VS))
```

`oddLinesAcc` recurses on the remaining list. Its step uses the exact
`valSeqConcat` update performed by `list.append`, so no associativity axiom is
needed.

## Proof-extension inventory

No proof-local rule intercepts `Call`, `For`, `#loop`, return, frame popping,
lookup, allocation, or heap update. All program-defined code executes under the
fixed semantics.

### `ODD-COUNT-BODY` and `ODD-COUNT-LOOP-BODY`

- **Extension / class:** exact syntax macros; definitional abbreviations.
- **Semantic role:** compile-time names for the translated function body and
  loop body. They do not rewrite runtime execution.
- **Domain / matched context:** the two literal macro tokens only.
- **Justification scope / containment:** each occurrence expands to the exact
  `Stmts` tree in `solution.mpy`; the match and justification domains are
  identical.
- **State footprint:** none at the macro level. The expanded fixed-semantics
  program has the state footprint recorded by the claims.
- **Value influence / justification:** pins the called closure to the submitted
  program. `validation.py` compares the `solution.py` and
  `concrete-smoke.py` function ASTs.
- **Dependents:** all three claims in `spec.k`.
- **Control and value validation:** `spec-body-mutation.k` replaces this body
  with “allocate and return an empty list”; `kprove` exits 1 with a stuck claim.

### `isStringVal` and `allDigitStrings`

- **Extension / class:** definitional domain predicates.
- **Semantic role:** constrain inputs; they do not replace execution.
- **Domain / matched context:** all `Val` and all `ValSeq`, respectively.
- **Equations:** `isStringVal` has the `str` case plus disjoint `[owise]`;
  `allDigitStrings` has disjoint empty/cons cases and recurses on the strict
  tail.
- **Justification scope / containment:** constructor-exhaustive over their
  declared domains.
- **State footprint:** none.
- **Value influence:** establishes that every input element is a string and
  every code is in `48..57`.
- **Value justification:** the supplied `allDigit` equations and the exact
  `str` constructor.
- **Dependents:** entry preconditions, loop precondition, and the guarded count
  dispatch.
- **Validation:** satisfiable witnesses include `[]`, `[""]`, and `["1"]`;
  concrete and differential tests include all of them.

### `stringCodes`

- **Extension / class:** guarded total projection; definitional summary.
- **Semantic role:** exposes the code sequence of a value already known to be a
  `str`. It does not create a string or skip program execution.
- **Domain / matched context:** all `Val`; the only reducing equation is
  `stringCodes(str(CS)) => CS`.
- **Justification scope / containment:** exact for every string constructor.
  It is deliberately opaque off-domain, and every target use is beneath
  `allDigitStrings`, which entails `isStringVal`.
- **State footprint:** none.
- **Value influence:** supplies codes to `cntSub` and `oddLine`.
- **Value justification:** constructor projection; no fresh result is invented
  on the target domain.
- **Dependents:** `allDigitStrings`, the guarded dispatch twin, and
  `oddLinesAcc`.
- **Control validation:** not applicable; it has no operational/control rule.
- **Value validation:** collapse is exact on every `str(CS)`;
  `projection-spec.k` proves the source `str.count` equation without importing
  this projection.

### Guarded `applyMethod(..., "count", ...)` dispatch twin

- **Extension / class:** derived lemma.
- **Exact rule:** for
  `applyMethod(V, "count", str(PATTERN), .Vals)` under
  `isStringVal(V)`, return `cntSub(stringCodes(V), PATTERN)`.
- **Semantic role:** restates a fixed semantic equation over a dynamic
  supersort after normal call lookup, receiver evaluation, argument evaluation,
  and method routing have executed. It is not a `Call` or `<k>` bridge.
- **Domain / matched context:** exactly the displayed `applyMethod` term, exact
  method name and arity, with the string guard. There is no continuation,
  binding, control-stack, or cell wildcard in this term-local lemma.
- **Justification scope / containment:** when the guard is true,
  `V = str(CS)` for some `CS`; projection gives `CS`, and the supplied
  `methods.k` rule gives `cntSub(CS, PATTERN)`. The rule's match domain is
  therefore contained in the fixed equation's domain.
- **State footprint:** none.
- **Value influence:** determines each of the five counts and therefore the
  returned text.
- **Value justification:** the supplied `str.count` rule plus the exact
  projection collapse.
- **Dependents:** `SPEC.outer-loop-cons` and `SPEC.odd-count-cons`.
- **Control validation:** no control is changed. Fixed call routing remains in
  the proof trace.
- **Value validation:** the bridge-free universal static-string claim in
  `projection-spec.k` prints `#Top`; the false ground interpretation
  `"11".count("1") == 1` in `spec-count-mutation.k` exits 1; the differential
  test has zero mismatches.

### `oddDigitCount`, `oddLine`, and `oddLinesAcc`

- **Extension / class:** definitional summaries.
- **Semantic role:** name the exact value computed by fixed execution; they
  never match program syntax or a `<k>` computation.
- **Domain / matched context:** all `IntSeq` for the first two and all pairs of
  `ValSeq` for `oddLinesAcc`.
- **Equations and coverage:** `oddDigitCount` and `oddLine` each have one
  unguarded equation. `oddLinesAcc` has disjoint empty/cons equations and
  strictly recurses on the second argument's tail.
- **Justification scope / containment:** complete declared domains.
- **State footprint:** none.
- **Value influence:** these summaries characterize the final heap list.
- **Value justification:** five supplied `cntSub` applications, supplied
  integer-to-string conversion, supplied string concatenation, and the exact
  accumulator update.
- **Dependents:** the loop postcondition and both entry postconditions.
- **Control validation:** not applicable.
- **Value validation:** LLVM examples include counts `0`, `1`, `4`, `8`, and
  `12`; `validation.py` checks 11,611 strings with an independent oracle.

### `SPEC.outer-loop-cons`

- **Extension / class:** derived auxiliary reachability claim (loop
  circularity).
- **Semantic role:** proves the fixed loop by coinduction; it does not add an
  operational rewrite to `verification.k`.
- **Domain:** a nonempty remaining `ValSeq` satisfying `allDigitStrings`.
- **Matched context:** exact `#loop` target and body; exact environment `1`;
  exact local, module, and builtin scopes; exact result heap location `0`;
  exact heap counter, scope counter, call frame, return state, exception state,
  and exit code. The `<k>` suffix is framed because fixed loop execution
  preserves it.
- **Justification scope / containment:** the claim proves precisely that
  framed loop-head domain. Recursive applications use the same domain after
  one fixed iteration; the empty tail executes directly.
- **State footprint:** local `s`, `count`, and `count_string` may change; heap
  location `0` changes by the exact append; all other stated cells are
  preserved.
- **Value influence / justification:** `oddLinesAcc` is the inductive summary.
  Base is the empty tail; step is one fixed body execution followed by the same
  circularity on the tail.
- **Dependents:** `SPEC.odd-count-cons`.
- **Control validation:** the loop body has no break, continue, return, or
  exception rule. The exact call frame and continuation remain fixed.
- **Value validation:** the full combined proof prints `#Top`; body and
  postcondition mutations are rejected.

## Exact commands and actual results

Tool version:

```text
K version: v7.1.293
```

The final complete replay was:

```bash
./prove.sh > prove-run.out 2>&1
```

It exited `0`. `prove.sh` contains the exact commands; the material commands
are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
python3 validation.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-smoke.mpy --definition runtime-kompiled > concrete-smoke.out

kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition reference-proof-kompiled
kprove projection-spec.k \
  --definition reference-proof-kompiled \
  --spec-module PROJECTION-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
kprove spec-count-mutation.k \
  --definition reference-proof-kompiled \
  --spec-module SPEC-COUNT-MUTATION
```

Actual positive outputs:

```text
projection-spec.k: #Top   Exit: 0
spec.k:            #Top   Exit: 0
```

The target `kprove spec.k` invocation contains all three claims together, so
the entry claims can use the loop circularity. It is the required positive
target-proof command.

Actual concrete/differential markers:

```text
DIFFERENTIAL_OK cases=11611 mismatches=0
SMOKE_BODY_MATCH
KRUN_SMOKE_OK
```

Actual negative-probe results:

```text
spec-vacuity.k:        WarnStuckClaimState   Exit: 1
spec-body-mutation.k:  WarnStuckClaimState   Exit: 1
spec-count-mutation.k: WarnStuckClaimState   Exit: 1
```

The vacuity residual contains `ref(0)` while the false destination requests
`ref(1)`. The body-mutation residual has an empty returned heap list while the
destination requires the nonempty transformed list. The count mutation rejects
the false value `1` for `"11".count("1")`.

The LLVM compiler emitted supplied-semantics exhaustiveness warnings, and both
backends emitted unused-variable warnings from supplied `str.k`; all compile
commands nevertheless exited `0`. The base connection claim also emitted
`WarnTrivialClaim` because simplification establishes the supplied equation
before an operational rewrite; it printed `#Top` and exited `0`.

Evidence files are `target-proof.out`, `projection-proof.out`,
`concrete-smoke.out`, `vacuity.out`, `body-mutation.out`,
`count-mutation.out`, and `prove-run.out`.

## Gate results

### Gate A — PASS

- A1: the exact translated body is bound in the closure and executes under
  fixed semantics. The AST identity check passes; the changed-body claim fails.
- A2: there are no operational bridges. The loop claim explicitly tracks every
  state cell it reads or changes.
- A3: module and builtin bindings, evaluation, call frame, continuation, and
  return behavior are pinned. The guarded dispatch is term-local after fixed
  call routing and has an independently checked fixed equation.
- A4: every proof-local total function has constructor-exhaustive or unguarded
  coverage. Guards are disjoint or overlapping equations agree. Structural
  recursions descend.
- A5: realizable witnesses include empty input and `["1"]`; false result, body,
  and count interpretations are all rejected.

### Gate B — PASS

- B1: the empty/nonempty entry partition and recursive circularity cover every
  finite list and every finite digit-string length. There is no chosen bound.
- B2: the contract uses only digit input and ASCII output, all represented by
  the supplied code-sequence model. K integers and CPython integers are
  unbounded for this task.
- B3: the execution summary is connected directly to supplied `str.count`,
  integer-to-string conversion, string concatenation, and list append. On a
  digit-only string, the five counted characters are exactly the odd digits.
- B4: the implementation matches the prompt's examples, including repeated
  substitution and a multi-digit count.

### Gate C — PASS

- All proof-local extensions and trust assumptions are inventoried.
- Every reported command, output, mutation, and differential result has an
  existing artifact and is replayed by `prove.sh`.
- Formal proof, fixed-semantics assumptions, finite evidence, and excluded
  behavior are separated here.

## Trust boundary

- The supplied read-only `reference-semantics/` definition is trusted as the
  Python subset model. In particular, `cntSub`, `strToCodes`, `Int2String`,
  `seqConcat`, `valSeqConcat`, call routing, scoping, allocation, and append are
  outside this theorem's rederivation. They affect values, control, and state;
  all target claims depend on them.
- The K compiler, Haskell backend, LLVM backend, SMT reasoning, and host
  runtime are trusted.
- `Int2String` is a fixed K hook used by the supplied `str(int)` rule. It
  affects the returned decimal text. Concrete and differential evidence checks
  relevant values, including a count greater than 9, but finite tests are not a
  universal proof of the hook.
- The theorem is conditional on normal termination, as required by the Kit's
  partial-correctness model.

No additional trusted primitive or result-bearing oracle was introduced in
`verification.k`.

## Empirically supported facts

`validation.py` uses an independent CPython oracle:

```python
odd_digits = sum(character in "13579" for character in text)
TEMPLATE.replace("i", str(odd_digits))
```

It checks every decimal string of length `0` through `4` plus 500 deterministic
random strings of length up to `80`: 11,611 strings total, zero mismatches. This
supports implementation-to-intent alignment and the fixed primitive behavior
on those cases; it is not used as universal proof.

`concrete-smoke.py` executes the prompt examples plus empty-string and
multi-digit-count cases under LLVM. Its function AST is checked against
`solution.py` before translation.

## Excluded behavior

- Inputs that are not finite lists of finite strings containing only decimal
  digits are outside the HumanEval contract and outside the entry
  preconditions.
- Exceptional behavior outside the supplied semantic subset is not claimed.
- Total correctness and resource bounds are not claimed.
