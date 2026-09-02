VALIDATED

## What is proven

Under the supplied, unmodified `reference-semantics`, the exact translated
definition of `decode_cyclic` returns the string obtained by rotating every
complete three-code group right once and leaving the final group of length zero,
one, or two unchanged. This is the inverse of the `encode_cyclic` rotation in
`prompt.py`.

The machine proof covers every symbolic `str(INPUT)` where `INPUT` is a finite
`IntSeq`. The successful `kprove` execution and this validation judgment are
separate facts: `#Top` establishes closure under the theory, while the Gate
A/B/C audit below establishes the `VALIDATED` headline.

## Formal claim

The entry claim loads the exact `FuncDef`, resolves `decode_cyclic` through the
module environment, calls it with `str(INPUT)`, and reaches:

```k
str(decodeCodes(INPUT))
```

The structural definition is:

```text
decodedResult(acc, [])        = acc
decodedResult(acc, [x])       = acc
decodedResult(acc, [x,y])     = acc
decodedResult(acc, [x,y,z]+r) = decodedResult(acc+[z,x,y], r)

decodeCodes(input) =
  decodedResult([], input) + the final zero-to-two-code tail
```

Claims `loop-empty`, `loop-one`, and `loop-two` cover the three possible buffer
lengths at the loop head. They constrain the final `result`, `group`, and
`char` locals exactly and preserve `s`, the environment chain, heap, stack,
allocation counters, return state, exception state, and exit code. Claim
`decode-entry` connects those invariants to exact module loading, binding,
function-call control, frame cleanup, and the returned value.

## Proof-extension inventory

There are no proof-local operational bridge rules, opaque result oracles,
trusted primitives, priority rules, concrete rules, or simplification lemmas.
Every program-defined statement executes under the fixed semantics.

### `decodeLoopBody` and `decodeFunctionBody`

- Class: definitional syntax abbreviations.
- Semantic role: parse-time macros only; they do not rewrite runtime execution.
- Domain and matched context: the two exact AST fragments generated from
  `solution.py`; no operational configuration is matched.
- State footprint and value influence: none independently. Expansion exposes
  the exact fixed-semantics program body.
- Justification and dependents: direct transcription of `solution.mpy`; all
  loop claims and `decode-entry` depend on the expansion.
- Validation: `diff -u solution.mpy <(python3 py2mpy.py solution.py)` produced
  no output and exited 0. The changed-body probe was rejected.

### `decodedResult`

- Class: definitional summary.
- Semantic role: names the accumulator value; it never replaces a program term.
- Domain: every pair of finite `IntSeq` values. Its four constructor cases are
  disjoint and exhaustive; recursion removes exactly three input constructors.
- Matched context: none.
- State footprint: none.
- Value influence: fixes the loop claims' final `result` and therefore the entry
  result.
- Value justification: the base cases preserve the accumulator; the step adds
  `[z,x,y]`, exactly matching the fixed execution of the parenthesized source
  expression.
- Dependents: all three loop claims, `decodeCodes`, and `decode-entry`.
- Validation: fixed-semantics loop proofs reached `#Top`; the false-result and
  changed-body probes both exited 1 with distinct actual values.

### `decodedTail`

- Class: definitional summary.
- Semantic role: names the zero-to-two-code buffer left after complete groups;
  it does not replace execution.
- Domain: every finite `IntSeq`. The zero-, one-, two-, and at-least-three-code
  cases are disjoint and exhaustive; the recursive case removes three codes.
- Matched context and state footprint: none.
- Value influence: fixes final `group` and the suffix of `decodeCodes`.
- Value justification: its equations are the source loop's buffer/reset cases.
- Dependents: all three loop claims and `decodeCodes`.
- Validation: the concrete zero-, one-, two-, three-, multi-group, and trailing
  fragment tests passed; the symbolic phase claims reached `#Top`.

### `finalLoopChar`

- Class: definitional summary.
- Semantic role: exactly records the loop-target local; it does not replace
  iteration.
- Domain: every finite `IntSeq` and old `Val`. Empty iteration preserves the
  old value; each constructor replaces it with the current one-character
  string and recurses on a strictly smaller sequence.
- Matched context: none.
- State footprint: specifies only the local `char` value.
- Value influence: it does not affect the returned value, but removes an
  otherwise unconstrained state component from the loop claims.
- Dependents: the three loop claims.
- Validation: the equations follow the fixed `#iterYield`/`#bindTgt` rules and
  were exercised by all three symbolic phase proofs.

### `loop-empty`, `loop-one`, and `loop-two`

- Class: derived reachability claims used as circular loop invariants.
- Semantic role: reason about fixed execution; they add no rewrite to
  `verification.k` and do not bypass an iteration.
- Domain: every finite remaining `IntSeq`, arbitrary accumulator and source
  sequences, arbitrary old loop-target value, and local environment location
  `L >= 1`.
- Matched context: exact `#loop(str(IS), Name("char"), decodeLoopBody)`, exact
  local bindings, module binding chain through scope 0 to `builtinsScope` at
  -1, and all configuration cells. The continuation is framed, but the loop
  body has no return, break, exception, allocation, or other abrupt effect, and
  every local observable—including `char`—is specified.
- Justification scope and context containment: each claim is itself proved by
  fixed semantics. Empty iteration is the base case; three iterations return
  to the same buffer phase on a smaller sequence. The claim preserves the
  continuation and every non-local state cell, so its framed context is within
  that compositional scope.
- State footprint: reads `env` and `scopes`; updates only `result`, `group`, and
  `char`; preserves `s`, heap, allocation counters, stack, return, exception,
  and exit cells.
- Value influence: `result` and `group` determine the final return.
- Dependents: `decode-entry`.
- Control and value validation: all claims were selected in the unfiltered
  positive proof. Concrete LLVM execution agreed with expected control/state.
  The changed-body probe demonstrates operational sensitivity, and the
  false-result probe demonstrates value sensitivity.

## Exact commands and actual outputs

Tool version:

```text
K version: v7.1.293
```

Translation:

```bash
python3 py2mpy.py solution.py > solution.mpy
diff -u solution.mpy <(python3 py2mpy.py solution.py)
```

Actual result: both commands exited 0; `diff` printed no output.

Concrete build and execution:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py smoke.py |
  krun /dev/stdin --definition runtime-kompiled
```

Actual result: both commands exited 0. `krun` ended with `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`. LLVM compilation
printed pre-existing coverage warnings for unrelated reference symbols such as
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`; none is on
this program's execution path.

Independent CPython differential test:

```bash
python3 differential_test.py
```

Actual output and exit:

```text
cases=87387
mismatches=0
Exit: 0
```

Symbolic build and complete positive proof:

```bash
kompile --backend haskell verification.k \
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

The unfiltered command is intentional: in this K release, selecting only
`decode-entry` omits the auxiliary loop claims from that proof. The unfiltered
command selects and proves every claim in `SPEC` together.

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`. The residual result was
`str(iCons(97, iCons(98, iCons(99, .IntSeq))))` (`"abc"`), while the mutated
destination required `"abd"`.

Changed-body probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`. The mutated body returned
`str(iCons(98, iCons(99, iCons(97, .IntSeq))))` (`"bca"`), while the unchanged
destination required `"abc"`.

The exact end-to-end command was:

```bash
./prove.sh
```

Actual result: exit 0 after the positive `#Top` and both expected-failure
messages.

## Gate results

### Gate A — PASS

- A1: the entry claim loads, binds, and calls the exact body. No program
  operation is intercepted. The changed-body probe materially changes the
  result and is rejected.
- A2: there is no operational bridge. Loop claims specify all modified locals
  and preserve every other active state cell.
- A3: the local and module maps contain no shadowing `len`; lookup reaches the
  pinned `builtinsScope`. Fixed semantics performs callee and argument
  evaluation, indexing, slicing, concatenation, loop control, return, and frame
  cleanup in order.
- A4: every proof-local function has exhaustive, pairwise-disjoint constructor
  cases and structurally decreasing recursion. There are no proof-local opaque
  functions or simplification equations.
- A5: `"bca"` is a realizable witness. The false `"abd"` postcondition was
  rejected and exposed the actual `"abc"` result.

### Gate B — PASS

- Input domain: the prompt requires `s: str`; the formal input is exactly
  `str(INPUT:IntSeq)`. Non-string calls are excluded.
- Property: `[x,y,z]` is mapped to `[z,x,y]`, and a final group shorter than
  three is unchanged. This is the inverse of the prompt's left rotation.
- Language model: the reference represents strings as sequences of integer
  codes. This task observes only sequence length, iteration, indexing, slicing,
  and concatenation, so code values are never interpreted. Concrete K literals
  are ASCII-only, while the symbolic theorem is parametric in arbitrary integer
  codes and therefore includes valid non-ASCII code sequences.
- Implementation and intent agree on all boundary cases and tested examples.

### Gate C — PASS

- Every claimed artifact exists, every command is in `prove.sh`, and an
  end-to-end run completed with exit 0.
- The concrete test oracle consists of six explicit expected results in
  `smoke.py`.
- `differential_test.py` independently uses the supplied `encode_cyclic` as the
  oracle and checks all strings of lengths 0 through 8 over `"aB0!"`, plus six
  Unicode cases: 87,387 cases and zero mismatches.
- Both negative probes are preserved as reproducible artifacts and produced the
  expected non-zero outcomes.

## Trust boundary

- Trusted: K v7.1.293, its Haskell prover/SMT integration, its LLVM executor,
  the fixed `py2mpy.py` translator, and the supplied reference semantics.
- Evidence: the generated `solution.mpy` exactly matches a fresh translator
  run; concrete and differential tests agree with independent expected values;
  both mutations are rejected.
- No task-local trusted primitive or opaque value is used. Opaque float, sort,
  and digest facilities elsewhere in the supplied semantics are unreachable
  and no claim depends on them.
- The supplied semantics itself is the user-designated reference model; this
  work proves the program relative to that model rather than proving the model
  correct with respect to CPython.

## Empirically supported facts

- Six concrete translated programs execute successfully through the LLVM
  semantics, covering lengths 0, 1, 2, 3, 7, and 9.
- CPython execution satisfies
  `decode_cyclic(encode_cyclic(original)) == original` on 87,387 documented
  cases with zero mismatches.
- These finite runs support model and intent adequacy; the universal result
  comes from the symbolic K proof, not from testing.

## Excluded behavior

- Calls where `s` is not a string are outside the formal input domain.
- This is a partial-correctness result under the Kit contract; it does not make
  a separate liveness claim.
- Python behaviors absent from this program—mutation, I/O, concurrency,
  exceptions from invalid indexing, and unrelated builtins—are not claimed.
- Correctness of the supplied reference semantics, translator, K backend, and
  SMT solver remains within the stated trust boundary.
