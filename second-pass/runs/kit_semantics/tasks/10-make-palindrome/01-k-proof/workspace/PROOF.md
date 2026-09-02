VALIDATED

## What is proven

For every finite symbolic input `S:IntSeq`, the exact translated
`make_palindrome` body executes under the supplied `MPY` semantics and returns
`str(completePal(S))`. The proof is not bounded by examples, string length, or
an alphabet.

The theorem is partial correctness in the Kit sense. Termination is also
supported independently by the source structure: both `for` loops consume the
same finite input string once, and their bodies contain no loop or recursion.

## Formal claim

`SPEC.make-palindrome-entry` starts from the complete initial MPY
configuration, loads `solutionModule`, resolves and calls
`make_palindrome(str(S))`, and reaches:

```k
<k> str(completePal(S)) </k>
```

with the module environment installed, the call frame popped, no exception,
exit code zero, empty heap, and all other initial cells restored.

The two circularity claims establish the loop summaries:

- `SPEC.reverse-loop`: iterating over `R` with accumulator `A` leaves
  `reverse_string = reverseAcc(R, A)`.
- `SPEC.search-loop`: iterating over `R` leaves `result` equal to
  `searchResult(S, R, P, RP, REV, F, RESULT)`. Other final loop locals are
  existential because they are not subsequently observed.

The summary has the HumanEval meaning. Let `P_k` be the length-`k` prefix of
`S`, `R = reverse(S)`, and `C_k = S · reverse(P_k)`.

1. `reverse(C_k) = P_k · R`, so the source comparison
   `S + reverse_prefix == prefix + reverse_string` holds exactly when `C_k`
   is a palindrome.
2. `searchResult` examines prefixes in increasing `k` and retains the first
   match. The `found` branch prevents later changes.
3. `k = |S|` always matches, since both sides are `S · reverse(S)`.
4. Therefore the result is a palindrome beginning with `S`.
5. Any shortest palindromic extension `S · X` has `|X| <= |S|` because the
   full-prefix candidate exists. If `|X| = j`, palindrome symmetry forces
   `X = reverse(P_j)`, so `C_j` would pass the source comparison. The first
   passing `k` is therefore minimal.

Thus `completePal(S)` is exactly the shortest palindrome beginning with `S`.

## Proof-extension inventory

There are no proof-local rules that rewrite a source operation, call, loop,
return, binding, or configuration. In particular, the final proof contains no
slice bridge, call bridge, opaque oracle, trusted primitive, priority rule, or
proof-local operational `<k>` rule.

### Exact AST abbreviations

- **Extension:** `isPalindromeBody`, `makePalindromeBody`,
  `reverseLoopBody`, `searchLoopBody`, `isPalindromeClosure`,
  `makePalindromeClosure`, and `solutionModule`.
- **Class:** Definitional summaries (compile-time macros).
- **Semantic role:** Names exact AST terms; does not replace execution.
- **Domain:** The single constant expansion of each macro.
- **Matched context:** None at runtime; expansion occurs before execution.
- **Justification scope:** The corresponding terms in `solution.mpy`.
- **Context containment:** Exact syntactic equality.
- **State footprint:** None.
- **Value influence:** Fixes which real body the entry and loop claims execute.
- **Value justification:** Line-for-line transcription of generated
  `solution.mpy`.
- **Justification:** `python3 py2mpy.py solution.py > solution.mpy`.
- **Dependents:** All three target claims.
- **Control validation:** The exact body executes in the entry claim; the
  material body mutation returns `""` and is rejected.
- **Value validation:** Concrete K smoke tests and the body mutation probe.
- **Validation:** Gate A1–A3 PASS.

### `reverseAcc`

- **Class:** Definitional summary.
- **Semantic role:** Mathematical loop accumulator; no execution replacement.
- **Domain:** Every finite `IntSeq × IntSeq`.
- **Matched context:** Only terms `reverseAcc(R, A)`; no cells or continuation.
- **Justification scope / containment:** Exactly its two exhaustive constructor
  equations.
- **State footprint:** None.
- **Value influence:** Determines `reverse_string`, `palIS`, and the result.
- **Value justification:** Base returns `A`; step moves the head of `R` to the
  front of `A`. The recursion strictly decreases `R`.
- **Justification:** Structural definition of reversal with an accumulator.
- **Dependents:** `reverse-loop`, `palIS`, `seedResult`, `completePal`.
- **Control validation:** Not applicable; it does not rewrite control.
- **Value validation:** `reverse-loop` prints `#Top`; differential tests include
  ASCII and Unicode inputs.
- **Validation:** Equations are total, disjoint, terminating, and non-overlapping.

### `palIS`, `seedResult`, and `completePal`

- **Class:** Definitional summaries.
- **Semantic role:** Name the palindrome test, initial fallback, and final
  mathematical result; they do not intercept execution.
- **Domain:** Every finite `IntSeq`.
- **Matched context:** Their own mathematical terms only.
- **Justification scope / containment:** Exact function arguments, with no
  framed cells.
- **State footprint:** None.
- **Value influence:** Final postcondition.
- **Value justification:** `palIS(S)` is equality with
  `reverseAcc(S, .IntSeq)`; `seedResult` has complementary `palIS` guards;
  `completePal` instantiates `searchResult` with the exact initial values.
- **Justification:** Exhaustive definitions matching the source assignments.
- **Dependents:** `searchResult` initialization and the entry claim.
- **Control validation:** Not applicable.
- **Value validation:** Entry `#Top`, false-result mutation rejection, and
  differential tests.
- **Validation:** `seedResult` guards are disjoint and exhaustive; all equations
  terminate.

### `searchResult`

- **Class:** Definitional summary.
- **Semantic role:** Structural summary of the second fixed-semantics loop; it
  does not rewrite the loop.
- **Domain:** All finite string-code sequences, Boolean `found`, and accumulator
  sequences.
- **Matched context:** `searchResult(S,R,P,RP,REV,F,RESULT)` only; no control or
  state cells.
- **Justification scope / containment:** Its complete algebraic domain.
- **State footprint:** None.
- **Value influence:** Determines the returned result.
- **Value justification:** `found=true` and `R=.IntSeq` return `RESULT`.
  Otherwise one head is consumed and the same equality used by the source
  selects either the current candidate or the recursive tail summary.
- **Justification:** Structural recursion matching one source loop iteration.
- **Dependents:** `search-loop`, `completePal`, entry claim.
- **Control validation:** The source `#loop` executes; no summary rule matches
  `<k>`.
- **Value validation:** `search-loop` and the combined target proof print
  `#Top`; the false-result mutation is rejected.
- **Validation:** The two base equations overlap only at
  `R=.IntSeq, found=true`, where both return the same `RESULT`; the remaining
  constructor case is disjoint and strictly decreases `R`.

### Reachability claims

- **Extension:** `SPEC.reverse-loop`, `SPEC.search-loop`, and
  `SPEC.make-palindrome-entry`.
- **Class:** Derived reachability claims/circularities.
- **Semantic role:** Execute fixed MPY control and summarize its reached state;
  they are not semantic rewrite rules in `verification.k`.
- **Domain:** Arbitrary finite `IntSeq` values and the exact configurations
  shown in `spec.k`.
- **Matched context:** The loop claims match the exact `#loop`, target,
  body, environment `1`, global bindings, local frame, `scopeLoc=2`, and all
  framed cells. Their `<k>` suffix is universally quantified and preserved.
  The entry claim matches the complete initial configuration and exact module
  load/call.
- **Justification scope:** The same complete configurations proved by `kprove`.
- **Context containment:** Exact equality between claim match domain and proof
  domain; no separately admitted operational rule widens it.
- **State footprint:** Reverse loop writes `char` and `reverse_string`; search
  loop writes `char`, `prefix`, `reverse_prefix`, `found`, and `result`.
  The entry allocates and pops one call frame. Heap, heap location, exception,
  exit code, and unrelated continuation/state are preserved.
- **Value influence:** `reverse_string` feeds the search; `result` is returned.
- **Value justification:** Fixed execution plus the total summary equations.
- **Justification:** Machine-checked reachability under `MPY`.
- **Dependents:** The entry claim depends on both loop circularities.
- **Control validation:** Both isolated loop claims and the combined claim print
  `#Top`; the material body mutation exits 1.
- **Value validation:** The wrong empty-input output exits 1 with a residual
  `str(.IntSeq)`, and 1,531 oracle comparisons have zero mismatches.
- **Validation:** Gate A1–A5 PASS.

## Exact commands and actual outputs

The complete recorded run is `./prove.sh > prove-run.out 2>&1`.
The script exited 0.

```bash
python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
```

Actual concrete result: final `<k>` was `.K`, `<exit-code>` was `0`, and the
command exited 0. The supplied semantics emitted its existing non-exhaustive
function warnings during LLVM compilation.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.reverse-loop
# Output: #Top
# Exit: 0

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.search-loop
# Output: #Top
# Exit: 0

kprove spec.k --definition verification-kompiled --spec-module SPEC
# Output: #Top
# Exit: 0
```

The last command proves all three claims, including the required symbolic
entry theorem.

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# Output: WarnStuckClaimState; residual result str(.IntSeq)
# Exit: 1 (expected)

kompile --backend haskell verification-mutant.k \
  --main-module VERIFICATION-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled
kprove spec-body-mutation.k --definition mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION
# Output: WarnStuckClaimState; mutated body result str(.IntSeq)
# Exit: 1 (expected)

python3 test_solution.py
# Output: cases=1531 mismatches=0
# Exit: 0
```

`prove-run.out` contains three `#Top` lines, both expected-failure markers, and
the differential-test count.

## Gate results

### Gate A — PASS

- **A1:** Exact source AST and bindings execute. The target body is not replaced
  by a result oracle. Changing it to `return ""` makes the ground `"cat"`
  theorem fail with exit 1.
- **A2:** The claims preserve all modeled state outside the explicitly written
  locals. The call frame is popped and heap/exception/exit cells are unchanged.
- **A3:** Fixed name lookup, argument evaluation, `for` control, assignments,
  branches, return, and frame control execute. There is no operational bridge
  requiring a connection theorem.
- **A4:** Every proof-local function is exhaustively defined. Recursive
  equations decrease a finite `IntSeq`; overlapping `searchResult` base cases
  agree.
- **A5:** The empty input is realizable. Mutating its required result from `""`
  to the one-code string `[0]` is rejected with exit 1.

### Gate B — PASS

- **B1:** `S:IntSeq` is an arbitrary finite symbolic sequence. There is no
  fixed-size, bounded-unrolling, alphabet, or example restriction.
- **B2:** The used MPY operations—string iteration, one-character yields,
  concatenation, equality, Boolean branching, assignment, calls, and returns—
  match the relevant Python behavior. Symbolic codes are unrestricted, so the
  theorem is not limited by the concrete literal parser's ASCII check.
- **B3:** The first-match characterization and minimality derivation are given
  above. It connects the execution summary to “shortest palindrome beginning
  with the supplied string.”
- **B4:** The implementation and prompt examples agree.

### Gate C — PASS

- The trust boundary and all proof-local equations are inventoried.
- Positive, negative, concrete, mutation, and differential evidence are
  reproducible from existing artifacts and exact commands.
- Machine-checked facts, the mathematical adequacy argument, finite evidence,
  and excluded properties are stated separately.

## Trust boundary

- Trusted inputs: the supplied read-only `reference-semantics/`, the fixed
  `py2mpy.py` translator, K's parser/compiler/backends, and the SMT reasoning
  used by `kprove`.
- Program identity: `solution.mpy` is regenerated from `solution.py`; the
  `solutionModule` macros reproduce that generated AST. The mutation probe
  independently establishes body sensitivity.
- There are no trusted proof-local primitives, opaque result symbols, or
  operational bridges.
- The short summary-to-English minimality theorem above is a mathematical
  derivation; `kprove` machine-checks execution to the fully defined
  `completePal`, while the derivation establishes that summary's intended
  meaning.

## Empirically supported facts

- `smoke.py` runs the prompt examples plus `"race"` and `"abba"` through the
  LLVM MPY semantics; it finishes with `.K` and exit code cell zero.
- `test_solution.py` compares against an independently written
  shortest-candidate oracle on 1,531 cases: exhaustive binary strings of
  lengths 0–9, examples and Unicode cases, plus 500 deterministic random
  strings of lengths 0–24. It reports zero mismatches.
- These tests support implementation/model adequacy only; the arbitrary-domain
  theorem comes from `kprove`.

## Excluded behavior

- The Kit reachability result is a partial-correctness theorem; termination is
  justified separately by the two finite structural `for` loops.
- Inputs outside Python's `str` contract are excluded. The K theorem uses the
  corresponding finite code-sequence representation.
- Behavior of unused Python features and unused MPY semantic modules is not
  claimed.
