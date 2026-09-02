VALIDATED

## What is proven

Under the supplied reference semantics, the exact translated `solve` body is
partially correct for every finite modeled string, represented by an arbitrary
`IntSeq` with no length bound and no restriction on its integer elements.

For input `str(INPUT)`, the result is:

- `str(toggleAcc(INPUT, .IntSeq))` when at least one modeled character is
  alphabetic, where `toggleAcc` case-toggles exactly those characters and
  preserves all others; and
- `str(revIS(INPUT))` otherwise.

The entry claim executes module loading, binding of `solve`, argument
evaluation, the exact function body, every loop iteration, return/control-frame
handling, and assignment of the returned value to `answer`.

## Formal claims

`spec.k` contains:

1. `SPEC.loop-invariant`, an unbounded circularity over arbitrary
   `REST:IntSeq`, arbitrary accumulator values, and an arbitrary continuation.
   It summarizes all loop-modified locals:
   `c`, `has_letter`, `reversed_s`, and `swapped`.
2. `SPEC.solve-full-domain`, the target claim from the exact module load to a
   final `answer |-> solveResult(INPUT)`.

There is no precondition and no finite-size bound. The proof is a K
reachability proof and therefore establishes partial correctness, not a
separate liveness theorem.

## Proof-extension inventory

There are no operational bridges, execution interceptors, priority rules,
opaque result symbols, or proof-local trusted primitives.

### `loopBody` and `solveBody`

- **Class:** Definitional summaries implemented as compile-time macros.
- **Role/domain/context:** They name AST syntax only and never replace an
  executing K term. `solveBody` is the exact `solution.mpy` body, including the
  docstring expression; `loopBody` is its exact `For` body.
- **State/value/control:** None at macro expansion time. After expansion, all
  behavior is supplied by the fixed `MPY` rules.
- **Justification/dependents:** Direct textual comparison with generated
  `solution.mpy`; both positive claims depend on the aliases.
- **Validation:** `python3 py2mpy.py solution.py | cmp - solution.mpy` passed.
  The body mutation in `spec-body-mutation.k` was rejected.

### One-character/nonempty simplification

- **Extension:** `iCons(C, .IntSeq) ==K .IntSeq => false [simplification]`.
- **Class:** Derived lemma.
- **Domain/context:** Every integer `C`; pure `IntSeq` constructor equality,
  independent of continuation, bindings, and state.
- **State footprint/value influence:** Reads and writes no cells. It only
  exposes constructor disjointness needed by the fixed one-character
  `isalpha` computation, and therefore influences the alphabetic branch.
- **Justification/dependents:** Freeness of `.IntSeq` and `iCons`; depended on
  by `alphaAcc` and the loop proof.
- **Validation:** `LEMMA-SPEC.one-char-is-not-empty` imports a definition that
  omits this simplification and proves the statement with `#Top` (the backend
  reports `WarnTrivialClaim`).

### `charAlpha`

- **Class:** Definitional summary.
- **Domain:** Every integer code.
- **Equations:** One unconditional equation, so coverage is total and there is
  no overlap. It is exactly the fixed semantics' `isalpha` expression for the
  one-character `str(iCons(C, .IntSeq))`.
- **Context/state/value:** Pure; no execution is skipped and no cells are
  matched. Its Boolean value updates `has_letter`.
- **Dependents/validation:** `alphaAcc`, `solveResult`, both claims; validated by
  the independent nonempty lemma and by execution of the fixed method call in
  the loop circularity.

### `alphaAcc`

- **Class:** Definitional summary.
- **Domain:** Every finite `IntSeq` and `Bool`.
- **Equations:** Empty/base case plus two nonempty cases guarded by
  `charAlpha(C)` and its negation. The guards are disjoint and exhaustive, and
  both recursive cases descend to `REST`.
- **Context/state/value:** Pure. It summarizes the final `has_letter` value and
  controls which `solveResult` branch is selected.
- **Justification/dependents:** Each equation mirrors the actual loop `if`: set
  the flag to `true` on an alphabetic character, otherwise preserve it. The
  machine-checked loop circularity establishes the execution connection.

### `toggleAcc`

- **Class:** Definitional summary.
- **Domain:** Every finite remaining `IntSeq` and accumulated output `IntSeq`.
- **Equations:** Empty/base case plus complementary alphabetic/non-alphabetic
  cases. Both guarded cases append exactly one transformed or unchanged code
  and structurally descend to `REST`; their guards are disjoint and exhaustive.
- **Context/state/value:** Pure. It summarizes the observable `swapped` local:
  alphabetic characters use the fixed `swapC`, while every other code is
  appended unchanged.
- **Justification/dependents:** Its accumulator transition is exactly the true
  and false branch of `loopBody`. `SPEC.loop-invariant` machine-checks that
  execution connection; `solveResult` and the entry claim depend on it.

### `lastChar`

- **Class:** Definitional summary.
- **Domain/equations:** Every finite `IntSeq` and initial `Str`; disjoint empty
  and `iCons` cases, with structural descent.
- **Context/state/value:** Pure. It records the exact final `for`-target binding
  `c`; that local is later removed when the call frame pops and does not affect
  the returned value.
- **Justification/dependents:** The fixed `For` rule binds each yielded
  one-character string. `SPEC.loop-invariant` proves the connection.

### `solveResult`

- **Class:** Definitional summary of the stated postcondition.
- **Domain/equations:** Every finite `IntSeq`; complementary guards
  `alphaAcc(INPUT, false)` and its negation are disjoint and exhaustive.
- **Context/state/value:** Pure; it replaces no execution. It names the
  observable result and therefore is result-bearing.
- **Justification/dependents:** The true branch is the proved per-character
  `toggleAcc`; the false branch is the fixed `revIS`.
  `SPEC.solve-full-domain`, using the proved loop circularity, establishes that
  exact program execution produces this value. The false-postcondition probe
  rejects the opposite result.

### `SPEC.loop-invariant`

- **Class:** Machine-checked derived reachability lemma/circularity.
- **Matched context:** Exact `#loop(str(REST), Name("c"), loopBody)` at
  environment 1; an exact five-binding local scope with parent 0; arbitrary
  framed outer scopes, heap, heap location, stack, and continuation; fixed
  `scopeLoc`, `ret`, `exc`, and exit-code values as written in `spec.k`.
- **State footprint:** Reads `s` and the four mutable loop locals; writes
  `c`, `has_letter`, `reversed_s`, and `swapped`; preserves every framed cell.
- **Control containment:** The claim itself universally frames the continuation.
  The body contains no return, exception, break, or continue bridge, and no
  operational execution is replaced.
- **Dependents/validation:** `SPEC.solve-full-domain`; focused and complete-spec
  proof runs both returned `#Top`.

## Reproducible commands and actual results

The complete record is executable as:

```bash
./prove.sh
```

Actual result: exit 0. Important commands inside it were:

```bash
python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
```

LLVM compilation exited 0. `krun` reached `.K` with:

- `example_digits = str(52, 51, 50, 49)` (`"4321"`);
- `example_letters = str(65, 66)` (`"AB"`);
- `example_mixed = str(35, 65, 64, 99)` (`"#A@c"`); and
- `empty = str(.IntSeq)`.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual proof output: `#Top`; exit 0. This command proves every claim in
`spec.k`, with the loop circularity available to the entry claim.

```bash
kompile --backend haskell lemma-verification.k \
  --main-module LEMMA-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition lemma-kompiled
kprove lemma-spec.k --definition lemma-kompiled \
  --spec-module LEMMA-SPEC
```

Actual lemma output: `#Top`; exit 0; warning:
`WarnTrivialClaim: Claim proven without rewriting`.

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Both commands exited 1 as expected with `WarnStuckClaimState`. For witness
`"a"`, the first residual contains the actual answer `"A"` while the mutated
postcondition requires `"a"`; the second contains the mutated body's actual
answer `"a"` while the contract requires `"A"`.

```bash
python3 differential.py
```

Actual output: `checked=21517 mismatches=0`. The independent oracle covered
every ASCII string of length 0, 1, or 2 and 5,000 seeded strings of length
0–20 drawn from ASCII plus representative Unicode characters, followed by
four deterministic edge cases. Those edges include characters such as U+2160
and U+0345 that have case mappings but for which `isalpha()` is false.

## Gate results

- **Gate A — PASS.** The exact program executes under fixed semantics; there
  are no operational bridges or opaque program-derived values. All equations
  are truthful, total where marked, guarded with disjoint/exhaustive cases, and
  structurally descending. The derived simplification has an independent
  bridge-free `#Top` claim. The precondition is satisfiable (for example
  `INPUT = iCons(97, .IntSeq)`), and both the false-postcondition and body
  mutations are rejected.
- **Gate B — PASS, conditional on the supplied model boundary.** The theorem
  has no candidate-imposed narrowing and covers arbitrary finite strings in
  the fixed model. Its two result branches directly state the HumanEval
  contract. The implementation itself uses CPython `isalpha` and `swapcase`
  and is faithful for Unicode. The supplied semantics models source strings
  and alphabetic/case behavior only for ASCII; this is a fixed-model boundary,
  recorded below rather than a restriction added by the proof.
- **Gate C — PASS.** The trust ledger, commands, concrete outputs, independent
  lemma proof, mutation residuals, differential scope, and model-boundary
  witness are all present and reproducible.

## Trust boundary

| Component | Assumption/boundary | Influence | Dependents | Evidence |
|---|---|---|---|---|
| Supplied `reference-semantics/` | Its fixed `MPY` rules correctly define the modeled Python subset. | Value, binding, state, control, and partial-correctness interpretation. | All claims. | Concrete `krun` examples and body-sensitive proof probes. |
| K frontend and Haskell backend | Compilation, constructor reasoning, circularity, and `#Top` are implemented correctly. | Proof validity. | All formal results. | K v7.1.293; reproducible builds and proof runs. |
| ASCII character model | `strToCodes`/`chr` and `isAlphaC`/case maps do not model full CPython Unicode behavior. No Unicode-equivalence assumption is made. | Intent adequacy outside modeled characters. | Transfer from the formal theorem to full CPython `str`. | `unicode-boundary.mpy` fails at `applyBuiltin("chr", 233)` with exit 113, while CPython and the differential oracle handle Unicode. |

There are no proof-local trusted primitives. The Unicode boundary is not used
to prove a value; it is an explicitly excluded transfer from the fixed model.

## Empirically supported facts and excluded behavior

Formally established facts are exactly the two claims under the supplied
semantics. Finite evidence additionally supports the examples, body
sensitivity, result non-vacuity, and agreement of `solution.py` with an
independent CPython oracle over the recorded 21,517 cases.

Full Unicode character classification and case mapping are not formalized by
the supplied reference semantics. This behavior is nevertheless implemented
by `solution.py` through CPython's own `str.isalpha` and `str.swapcase`, and the
finite Unicode sample found no mismatch. Exceptions, non-string arguments, and
termination as a separate liveness property are outside the formal claim.
