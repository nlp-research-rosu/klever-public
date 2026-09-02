VALIDATED

## What is proven

Under the supplied MPY semantics, for every K string value `str(TEXT)` with
`TEXT:IntSeq`, loading the exact translated `remove_vowels` definition and
calling `remove_vowels(str(TEXT))` reaches
`str(removeVowelsFrom(TEXT, .IntSeq))`.

`removeVowelsFrom` is a stable left-to-right filter: it drops a code exactly
when the fixed-semantics singleton-string membership predicate says that code
occurs in `aeiouAEIOU`, and otherwise appends the code to the accumulator.
Thus the returned string contains the input characters in order with lowercase
and uppercase English vowels removed.

This is a partial-correctness reachability theorem. The entry claim also
observes the final operational state: environment `0`, the exact module
function binding, scope location `1`, empty heap, heap location `0`, empty call
stack, `noRet`, `NoExc`, and exit code `0`. The loop-local `char` value is
existential only in the auxiliary loop claim and is destroyed when the
function frame is popped.

## Formal claims

`SPEC.loop-invariant` states that, at the real `#loop` head, a local result
`str(ACC)` and remaining iterator `str(REST)` finish with result
`str(removeVowelsFrom(REST, ACC))`. It is parameterized over the input binding,
current loop-character binding, environment location, parent, other scopes,
continuation, and all other configuration cells.

Its obligations are:

- Base: `.IntSeq` leaves the accumulator unchanged.
- Vowel step: fixed execution binds the one-character string, takes the
  false `not in` branch, and the summary drops the same code.
- Non-vowel step: fixed execution performs the real `AugAssign` and
  `seqConcat`; the summary makes the identical accumulator update.
- Circular step: the fixed `#loopLbl` reconstruction matches the same
  `#loop` claim over the remaining `IntSeq`.

`SPEC.remove-vowels` starts from the complete initial MPY configuration,
executes `#loadAll` on the exact `solution.mpy` function body, performs ordinary
name lookup, argument evaluation and binding, executes the loop, returns its
value, pops the frame, and reaches the result and final state above.

There is no input guard: the formal domain is every `str(TEXT)` represented by
the supplied semantics.

## Proof-extension inventory

### `removeVowelsFrom`

- Extension: the `[function, total]` symbol and its three rules in
  `verification.k`; the two constructor-step equations are also marked
  `[simplification]`.
- Class: definitional summary.
- Semantic role: names the mathematical output; it never matches `<k>` and
  never replaces Python execution.
- Domain: all pairs `(REST:IntSeq, ACC:IntSeq)`.
- Matched context: only a `removeVowelsFrom` term. It has no continuation,
  binding, control-stack, or configuration-cell match.
- Justification scope: the empty case and both complementary outcomes of
  `strContains(iCons(C, .IntSeq), VOWEL_CODES)`, where
  `VOWEL_CODES = [97,101,105,111,117,65,69,73,79,85]`.
- Context containment: the equations have no operational context, so their
  match domain equals their justification domain.
- State footprint: none.
- Value influence: the loop claim's final `result` binding and the entry
  claim's returned value.
- Value justification: base returns `ACC`; a vowel recurses without changing
  it; a non-vowel recurses with
  `seqConcat(ACC, iCons(C, .IntSeq))`.
- Logical checks: the empty/constructor shapes are disjoint; the two
  constructor guards are exact Boolean complements; together they cover every
  constructor case; recursion descends structurally on `REST`. The
  `[simplification]` attributes assert the same equations and add no broader
  fact.
- Dependents: `SPEC.loop-invariant`, `SPEC.remove-vowels`, and both validation
  probes.
- Control validation: not applicable because no operational term is matched.
- Value validation: universally connected to actual loop execution by
  `SPEC.loop-invariant`; the complete entry theorem then connects the exact
  function call to the summary. The false-result and body-mutation probes were
  both rejected.

### `SPEC.loop-invariant`

- Extension: the reachability circularity over the exact fixed-semantics
  `#loop` term.
- Class: derived lemma (auxiliary execution claim).
- Semantic role: proves and summarizes repeated fixed-semantics execution; it
  is not an unproved operational rewrite.
- Domain and matched context: all `REST`, `ACC`, input and old-character code
  sequences, all environment locations and parents, every framed continuation,
  other scopes, and all automatically framed configuration cells, with an
  exact three-binding local scope for `text`, `result`, and `char`.
- Justification scope: identical to the claimed match domain; `kprove` proves
  the claim universally rather than assuming a narrower trailing computation.
- Context containment: the claim itself quantifies over the framed
  continuation and omitted cells. Its body has no `return`, `break`,
  `continue`, exception, allocation, output, or other abrupt effect.
- State footprint: reads `env` and the local scope; preserves `text`; updates
  `result` and `char`; frames other scopes and runtime cells; preserves the
  active continuation.
- Value influence and justification: determines the local `result` by the
  exhaustive equations above. The final `char` is deliberately unconstrained
  because it is unobservable after frame pop.
- Dependents: `SPEC.remove-vowels`.
- Validation: the complete two-claim proof is `#Top`; changing the program
  body to always return `""` makes the consonant witness `"b"` fail.

### Other audited constructs

There are no proof-local ordinary `<k>` rewrites, priority rules, operational
bridges, opaque values, trusted primitives, or program-call interceptions.
The target entry claim is the theorem being proved, not an added execution
rule. Its exact closure body is present on both sides of the module-scope
transition.

## Commands and actual results

The reproducible runner is `./prove.sh` (exit `0`). Its exact positive build and
proof commands are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 validate_artifacts.py
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output none

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual significant output and status:

```text
artifact checks: function bodies match; translations are current
differential checks=4622 exhaustive=3616 random=1000 mismatches=0
concrete krun: PASS
#Top
prove.sh exit: 0
```

The LLVM build exited `0` with supplied-semantics warnings about unused
non-exhaustive domains of `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`,
and `valSeqAt`, plus unused variables in `strLt`. The Haskell build and proof
exited `0` with the supplied `strLt` unused-variable warnings. None of those
symbols is on this program's execution or proof path.

Gate A5 uses the exact command:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1`, `WarnStuckClaimState`, with final
`<k> str(.IntSeq) ~> .K </k>` unable to unify with the deliberately false
`str(iCons(88, .IntSeq))` target for the satisfiable empty-string witness.
`prove.sh` reports `false-postcondition mutation: EXPECTED FAILURE`.

Body sensitivity uses:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1`, `WarnStuckClaimState`, with final
`<k> str(.IntSeq) ~> .K </k>` unable to unify with the expected consonant
result for input `"b"` after the body was changed to always return `""`.
`prove.sh` reports `changed-body mutation: EXPECTED FAILURE`.

## Gate results

### Gate A — PASS

- A1: the exact program-defined body executes through fixed semantics. The
  changed-body probe is rejected.
- A2: no operational bridge exists. The entry theorem observes the result,
  binding, environment, scope allocation/deallocation, heap, stack, return,
  exception, and exit-code cells.
- A3: fixed rules perform module binding, lookup, left-to-right call argument
  evaluation, parameter binding, iteration, branching, return, and frame pop.
  No proof-local rule changes control or exceptional behavior.
- A4: the only proof-local function is exhaustive, disjoint, truthful, and
  structurally terminating. The simplification equations have exactly the
  function equations' guards.
- A5: the empty-string initial configuration is realizable, the returned value
  is constrained, and the false `"X"` postcondition is rejected with a stuck
  residual.

### Gate B — PASS

- Input alignment: `text` is formally a K `str(IntSeq)`, matching the prompt's
  string domain; non-string calls are excluded.
- Model alignment: MPY represents strings as finite integer-code sequences.
  The operations material here—iteration into one-code strings, membership in
  the ASCII literal `aeiouAEIOU`, concatenation, and return—preserve the
  requested behavior for Python strings. The theorem is about the supplied MPY
  model, not a proof of all CPython behavior.
- Summary alignment: `removeVowelsFrom` directly defines the stable filter
  using the same fixed-semantics membership predicate exercised by the source
  branch. The loop claim formally connects this definition to execution.
- Implementation alignment: all six prompt examples pass in CPython and in the
  LLVM MPY smoke artifact.

### Gate C — PASS

- Every artifact and command named here exists and is executed by `prove.sh`.
- The supplied translator is checked by regenerating and comparing both
  persisted `.mpy` files. The duplicated function in `concrete-tests.py` is
  AST-compared with `solution.py`.
- The independent executable oracle is Python's `str.translate`, not the K
  proof equations. It checks the six prompt cases, all 3,616 strings of length
  0 through 3 over `aAeEiIoOuUbZ0 \n`, and 1,000 deterministic strings of
  lengths 0 through 80 sampled from ASCII plus `é`, `Ω`, `中`, and `🙂`.
  Actual result: 4,622 comparisons and zero mismatches.
- Finite tests are reported only as evidence; universal correctness in the MPY
  model comes from the two reachability claims.

## Trust boundary

The proof trusts K v7.1.293 and its Haskell prover, the supplied read-only MPY
semantics, and the supplied `py2mpy.py` AST transliterator. The artifact check
detects stale translations but does not prove the translator or the supplied
semantics equivalent to CPython. No opaque or externally trusted operation
affects this task's branch or result. Unused opaque float/sort/digest facilities
imported by MPY are outside the dependency path.

## Empirically supported facts

LLVM `krun` executes the exact AST-matched implementation on the six prompt
examples with no assertion, exception, or nonzero exit. CPython agrees with the
independent oracle on the documented 4,622-case sample. These facts support
translator/model adequacy over those finite inputs; they are not substituted
for the universal K proof.

## Excluded behavior

The theorem excludes non-string arguments, behavior outside the supplied MPY
language subset, equivalence of the full MPY model to every CPython feature,
resource bounds, and a separate liveness claim. It proves filtering only the
ten English vowel characters explicitly listed by the prompt implementation;
accented letters such as `é` are preserved.
