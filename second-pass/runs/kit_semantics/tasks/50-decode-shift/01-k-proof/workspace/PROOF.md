VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, `decode_shift` is partially
correct for every finite string whose character codes are all in `97..122`.
Starting with the exact translated function closure and the standard module and
builtins scopes, calling `decode_shift(str(CS))` returns
`str(decodeAcc(CS, .IntSeq))`, where `decodeAcc` shifts each code backward by
five modulo 26 in order.

The proof also establishes, for every lowercase code `C`,
`decodeCode(encodeCode(C)) = C`, where `encodeCode` is the arithmetic in the
prompt's supplied `encode_shift`. Thus the result is the pointwise inverse of
that encoder on the lowercase alphabet.

This is a partial-correctness result in the Kit sense. It does not independently
claim total correctness.

## Formal claims

`spec.k` contains three positive claims, all proved together:

1. `character-inverse`: for `97 <= C <= 122`,
   `decodeCode(encodeCode(C))` reaches `C`.
2. `loop-invariant`: with remaining input `CS` and accumulated codes `ACC`,
   the exact source loop updates `result` from `str(ACC)` to
   `str(decodeAcc(CS, ACC))`. The claim pins the ordinary local frame, exact
   module binding, exact builtins frame, and preserves the continuation and
   all unmentioned configuration cells.
3. `decode-shift`: from the exact translated `decode_shift` closure,
   `Call(Name("decode_shift"), str(CS))` reaches
   `str(decodeAcc(CS, .IntSeq))` when `lowerCodes(CS)` holds, with the initial
   module state restored after the call.

The formal domain is exactly:

```k
lowerCodes(.IntSeq) = true
lowerCodes(iCons(C, REST)) =
  (97 <=Int C andBool C <=Int 122) andBool lowerCodes(REST)
```

The observable final state is the returned `str` value. The entry claim also
constrains the environment, scopes, heap, allocation counter, stack, return
state, exception state, and exit code to their restored values.

## Proof-extension inventory

There are no operational bridges, trusted proof-local primitives, opaque
result oracles, priority rules, or proof-local simplification lemmas.
Program-defined code executes under the fixed semantics.

### `decodeCode(Int)`

- Class: definitional summary.
- Domain and context: every mathematical `Int`; it does not match an
  operational configuration or continuation.
- Definition: `pyMod(C -Int 102, 26) +Int 97`.
- Coverage/overlap/descent: one unconditional equation; exhaustive and
  overlap-free; nonrecursive.
- State footprint/control: none.
- Value influence: each returned code and the target postcondition.
- Value justification: this is exactly
  `((ord(ch) - 5 - ord("a")) % 26) + ord("a")`, using code 97 for `"a"`;
  the fixed semantics executes the source expression and the loop claim
  connects that execution to `decodeAcc`.
- Dependents: `decodeAcc`, `character-inverse`, `loop-invariant`,
  `decode-shift`.
- Validation: positive `#Top`; the `5 -> 4` body mutation is rejected.

### `encodeCode(Int)`

- Class: definitional summary.
- Domain and context: every mathematical `Int`; no operational match.
- Definition: `pyMod(C -Int 92, 26) +Int 97`, the supplied encoder's
  `((C + 5 - 97) % 26) + 97`.
- Coverage/overlap/descent: one unconditional, exhaustive, nonrecursive
  equation.
- State footprint/control: none.
- Value influence: only the intent-adequacy claim.
- Dependents: `character-inverse`.
- Validation: `character-inverse` proves the inverse equation over `97..122`;
  the CPython differential test supplies finite independent evidence.

### `decodeAcc(IntSeq, IntSeq)`

- Class: definitional summary.
- Domain and context: every pair of code sequences; no operational match.
- Equations: empty input returns the accumulator; a constructor input recurs
  on its strict tail after appending `decodeCode(C)`.
- Coverage/overlap/descent: the empty and `iCons` cases are disjoint and
  exhaustive; recursion strictly shortens the first argument.
- State footprint/control: none.
- Value influence: loop result and entry postcondition.
- Value justification: the machine-checked `loop-invariant` connects the exact
  fixed-semantics loop execution to this value for its complete matched
  context.
- Dependents: `loop-invariant`, `decode-shift`.
- Validation: positive `#Top`; false-postcondition and body-mutation probes
  both fail as expected.

### `lowerCodes(IntSeq)`

- Class: definitional predicate.
- Domain and context: every code sequence; no operational match.
- Coverage/overlap/descent: disjoint, exhaustive empty/constructor equations,
  recursively descending on the tail.
- State footprint/control: none.
- Value influence: restricts all positive claims to lowercase ASCII.
- Dependents: `loop-invariant` and `decode-shift`.
- Validation: `.IntSeq` is an explicit satisfiable witness; concrete and
  differential tests cover boundary letters and wraparound.

### `loop-invariant` claim

- Class: derived reachability lemma/circularity, not an operational rewrite.
- Complete matched context: the exact `#loop` body; environment 1; a plain
  local frame containing `s`, `result`, and `ch`; the exact module closure at
  scope 0; the exact builtins scope at -1; and an arbitrary preserved
  continuation. All other configuration cells are framed unchanged.
- Justification scope/context containment: the claim itself is proved by
  fixed-semantics symbolic execution for that complete context. There is no
  broader bridge rule.
- State footprint: `result` is constrained to `decodeAcc(CS, ACC)` and final
  `ch` is existentially unconstrained; `s`, bindings, control continuation,
  heap, stack, return state, exception state, and exit code are preserved.
- Value/control validation: the exact claim closes with `#Top`; changing every
  loop/body shift literal from 5 to 4 makes the inductive step stuck. No abrupt
  control is introduced.
- Dependents: `decode-shift`.

## Exact commands and actual outputs

The complete reproducible run is in `prove.sh`; its final execution exited 0.
The commands are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_test.py > concrete_test.mpy
python3 -m py_compile solution.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_test.mpy --definition runtime-kompiled
python3 test_solution.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual results from the final `./prove.sh` run:

- Translation and `py_compile`: exit 0.
- LLVM `kompile`: exit 0. It printed non-exhaustiveness warnings in unrelated
  imported functions (`mapStrVS`, float helpers, `joinCodes`, and
  `valSeqAt`).
- `krun`: exit 0 with `<k> .K </k>`, `<exc> NoExc </exc>`, and
  `<exit-code> 0 </exit-code>` after all four assertions.
- CPython differential: `cases=18279 mismatches=0`, exit 0.
- Haskell `kompile`: exit 0, with only the supplied `str.k` unused-variable
  warnings.
- Positive `kprove`: printed `#Top` and exited 0. It also printed
  `WarnTrivialClaim` for `character-inverse`, which the simplifier and solver
  discharged without operational rewriting.
- False-postcondition probe: exited 1 as expected with
  `WarnStuckClaimState`; the residual required the false equality
  `decodeAcc(CS,.IntSeq) =
  seqConcat(decodeAcc(CS,.IntSeq),iCons(97,.IntSeq))`.
- Body mutation probe: exited 1 as expected with `WarnStuckClaimState`; its
  residual contrasted the original `C - 102` inverse shift with the mutated
  `C - 101` shift.

The final script converted both expected nonzero probe results into successful
`EXPECTED FAILURE` checks and itself exited 0.

## Gate results

### Gate A — PASS

- A1: the entry and loop claims pin the exact translated closure body,
  parameter, binding, scopes, and builtins. No program-defined operation is
  summarized away. The `5 -> 4` mutation invalidates the loop proof.
- A2: there are no operational bridges. Fixed execution restores the call
  frame and all entry-state cells; the loop claim explicitly accounts for its
  two local writes.
- A3: lookup, argument evaluation, loop control, `ord`, modulo, `chr`, return,
  and frame restoration all execute under fixed semantics. Exact scopes rule
  out shadow bindings. The arbitrary continuation is preserved.
- A4: every proof-local equation is exhaustive, overlap-free, and either
  nonrecursive or structurally decreasing. No false off-domain equation or
  opaque value is present.
- A5: `CS = .IntSeq` satisfies the precondition. The entry postcondition
  constrains the returned string. Appending code 97 to that result in
  `spec-vacuity.k` is rejected with exit 1.

### Gate B — PASS

- The prompt's encoded-string domain is the lowercase alphabet; the formal
  predicate includes every such finite string and adds no hidden restriction.
- On this domain the supplied semantics' ASCII code model agrees with CPython
  for the operations used here.
- `character-inverse` formally proves the backward character formula is the
  inverse of the prompt's forward formula. `decodeAcc` preserves order and the
  loop claim connects it to the implementation.
- The empty string and modulo wraparound are included.

### Gate C — PASS

- All assumptions and exclusions are recorded below.
- Every claimed concrete, differential, false-postcondition, and body-mutation
  check has an existing artifact and exact command in `prove.sh`.
- Formal proof, conditional trust, finite evidence, and excluded behavior are
  distinguished here.

## Trust boundary

- The supplied read-only `reference-semantics/` definition is trusted as the
  task's Python model. Every positive claim depends on its relevant function,
  call, loop, string, integer, `ord`, and `chr` rules.
- The supplied `py2mpy.py` translator is trusted to transliterate CPython AST
  nodes correctly. `solution.mpy` is regenerated by `prove.sh`, and the spec
  pins the resulting function body.
- K version `v7.1.293`, its LLVM and Haskell backends, the SMT solver used by
  `kprove`, and the host Python interpreter are trusted toolchain components.
- No proof-local trusted primitive or opaque value affects the result, control,
  state, or claims. Opaque facilities imported but unused from the broad
  reference semantics are not on this proof's execution path.

## Empirically supported facts

- `concrete_test.py`/`concrete_test.mpy` checks the empty input, a simple
  sequence, wraparound (`"c" -> "x"`), and a full rotated alphabet using LLVM
  `krun`; all assertions terminate with `NoExc` and exit code 0.
- `test_solution.py` uses the prompt's independently supplied `encode_shift`
  as its oracle and checks every lowercase string of lengths 0 through 3:
  18,279 cases, zero mismatches.
- `spec-vacuity.k` and `spec-body-mutation.k` are negative validation
  artifacts. Their finite/negative evidence supports non-vacuity and body
  sensitivity; it does not replace the universal positive proof.

## Excluded behavior

- Inputs containing characters outside lowercase ASCII are outside the formal
  precondition, even though the implementation may return a value for some of
  them.
- Unicode behavior, Python exceptions outside the proved domain, resource
  bounds, and performance are not modeled by this theorem.
- The theorem does not prove the supplied reference semantics or translator
  correct with respect to all of CPython.
- As a Kit reachability proof, the reported result is partial correctness, not
  a separate total-correctness theorem.
