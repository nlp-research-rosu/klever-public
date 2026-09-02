VALIDATED

## What is proven

Under the supplied `MPY` symbolic semantics, for every two finite `ValSeq`
values whose elements are modeled strings:

- if the total string length of the first list is less than or equal to the
  total string length of the second, executing the exact translated module and
  calling `total_match` returns the first list;
- if the first total is greater, execution returns the second list.

The equality case is therefore proved to select the first list. This is a
partial-correctness result: termination is not a separate theorem.

`solution.mpy` was regenerated from `solution.py` and compared byte-for-byte
successfully (`cmp` exit `0`). The entry claims contain the exact two function
bodies and begin with `#loadAll(Module(...))`, so lookup, binding, both helper
calls, the comparison, branch selection, returns, and frame cleanup all execute
under the fixed semantics.

## Formal claims

`spec.k` contains three claims:

1. `SPEC.sum-loop` is the loop circularity. In the exact reachable helper
   frame, it consumes
   `#loop(list(ITEMS), Name("string"), AugAssign(... len(string)))`. Under
   `onlyStrings(ITEMS)`, it changes `total` from `ACC` to
   `totalLenFrom(ACC, ITEMS)` and changes `string` to
   `lastLoopValue(ITEMS, OLD)`. It preserves the continuation and every other
   configuration cell.
2. `SPEC.entry-first` loads the exact module and proves a result of `list(A)`
   when `onlyStrings(A)`, `onlyStrings(B)`, and
   `totalLen(A) <=Int totalLen(B)`.
3. `SPEC.entry-second` loads the exact module and proves a result of `list(B)`
   under the same input domain when `totalLen(A) >Int totalLen(B)`.

The two numeric guards are disjoint and exhaustive.

## Proof-extension inventory

There are no operational bridges, priority shortcuts, opaque
program-derived values, or proof-local trusted primitives.

### `onlyStrings`

- **Extension/class:** `onlyStrings(ValSeq)` and its two equations;
  definitional summary.
- **Semantic role:** Defines the formal input domain; it does not replace
  execution.
- **Domain:** Every `ValSeq`. `.ValSeq` and `vCons` are exhaustive and
  disjoint.
- **Matched context / containment:** No operational context is matched.
- **State footprint:** None.
- **Value influence:** Restricts the loop and both entry claims to lists whose
  elements satisfy the fixed-semantics `isStrV`.
- **Value justification:** Its recursive equation uses the supplied
  `isStrV`, whose true case is exactly `str(IntSeq)`.
- **Dependents:** All three claims.
- **Validation:** Empty, singleton, and longer lists occur in the K smoke and
  differential tests; the universal loop proof unfolds the predicate at every
  constructor.

### `stringCodes`

- **Extension/class:** `stringCodes(Val)` with a string equation and an
  `[owise]` non-string equation; total definitional summary.
- **Semantic role:** Projects the `IntSeq` from a string; it does not replace a
  program step.
- **Domain:** Every `Val`. On `str(CS)` it returns `CS`; otherwise it returns
  `.IntSeq`. The `[owise]` case does not overlap the string case.
- **Matched context / containment:** No operational context is matched.
- **State footprint:** None.
- **Value influence:** It contributes to summarized lengths only under
  `isStrV`, so its non-string value cannot affect a target claim.
- **Value justification:** Exhaustive defining equations.
- **Dependents:** The guarded length lemma and `totalLenFrom`.
- **Validation:** The fixed-semantics loop theorem connects the projected
  length to actual `len` execution throughout the formal domain.

### Guarded `seqLen` simplification

- **Extension/class:**  
  `seqLen(V) => isLen(stringCodes(V)) requires isStrV(V)
  [simplification]`; derived lemma.
- **Semantic role:** Simplifies a fixed-semantics length result; it is not a
  `<k>` rewrite and does not skip lookup, calls, or control.
- **Domain:** Exactly values for which fixed `isStrV(V)` is true.
- **Matched context / containment:** Any occurrence of `seqLen(V)` under that
  guard. The derivation has the identical domain.
- **State footprint:** None.
- **Value influence:** Fixes the integer added to the helper accumulator and
  hence the final comparison.
- **Value justification:** In the guard domain, `V = str(CS)`;
  `stringCodes(str(CS)) = CS`, while the supplied semantics already states
  `seqLen(str(CS)) = isLen(CS)`.
- **Dependents:** `SPEC.sum-loop`, then both entry claims.
- **Control/value validation:** The universal loop claim prints `#Top`; the
  false-result and reversed-comparison probes are rejected.

### `totalLen` and `totalLenFrom`

- **Extension/class:** Total definitional summaries over `ValSeq`, using a
  left fold.
- **Semantic role:** Name the mathematical accumulator value; they do not
  replace program execution.
- **Domain:** Every integer accumulator and every `ValSeq`; the empty and
  `vCons` equations are exhaustive and disjoint, and recursion descends on the
  tail.
- **Matched context / containment:** No operational match.
- **State footprint:** None.
- **Value influence:** Their values determine the formal branch guards and
  the loop post-state.
- **Value justification:** `SPEC.sum-loop` is the bridge-free universal
  execution theorem under `onlyStrings`; its base case preserves `ACC`, and
  its step executes one real iteration and recurs with
  `ACC +Int isLen(stringCodes(V))`.
- **Dependents:** All claims.
- **Validation:** The unfiltered proof, five K examples, 7,230 differential
  cases, and rejected result/body mutations.

### `lastLoopValue`

- **Extension/class:** Total definitional summary.
- **Semantic role:** Describes the exact value left in the Python `for` target;
  it does not replace execution.
- **Domain:** Every `ValSeq` and old target value. Empty and `vCons` equations
  are exhaustive, disjoint, and descending.
- **Matched context / containment:** No operational match.
- **State footprint:** None itself; it describes only the helper's local
  `string` binding.
- **Value influence:** It affects the loop claim's local-state postcondition,
  but neither entry result reads that local after the helper returns.
- **Value justification:** Empty iteration preserves the old target; each
  nonempty step binds the head and recurses on the tail. `SPEC.sum-loop`
  machine-checks that execution universally.
- **Dependents:** `SPEC.sum-loop`.
- **Validation:** The K proof executes the real target binding and the full
  helper frame is then removed by the fixed call semantics.

### `SPEC.sum-loop`

- **Extension/class:** Derived reachability lemma/circularity.
- **Semantic role:** Reasons coinductively about fixed loop execution. It is
  not an ordinary rewrite rule or operational bridge.
- **Domain:** `L >Int 0`; `onlyStrings(ITEMS)`; an exact plain helper frame
  containing only `strings`, `total`, and `string`, with parent `0`; module
  scope `0` has parent `-1` and no local `len`; scope `-1` is
  `builtinsScope`.
- **Matched context:** The exact `#loop` prefix with an arbitrary continuation
  that is preserved by `=> .K ...`; exact environment and helper scope; framed
  unrelated scopes; and preserved `scopeLoc`, heap, `heapLoc`, stack, return,
  exception, and exit-code cells.
- **Justification scope / containment:** The claim proves exactly that matched
  domain. No broader operational rule is created.
- **State footprint:** Reads environment/scopes and builtin `len`; writes only
  local `string` and `total`; preserves all other cells and the continuation.
- **Value influence:** Supplies both helper totals used by the comparison.
- **Value justification:** Fixed-semantics base and inductive execution in the
  successful `#Top` proof.
- **Dependents:** `SPEC.entry-first` and `SPEC.entry-second`.
- **Control validation:** No control is skipped. The body mutation changing
  `<=` to `>` reaches `["b"]` and is rejected against the expected `["a"]`.
- **Value validation:** The false-result mutation reaches `list(.ValSeq)`
  rather than `noneV` and is rejected.

## Exact commands and actual outputs

The complete recorded workflow is executable as:

```bash
./prove.sh
```

Actual final result: exit `0`. The script contains these substantive commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 -m py_compile solution.py differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
python3 differential_test.py

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Observed outputs and exits:

- LLVM compilation: exit `0`; warnings were from non-exhaustive functions in
  the supplied semantics.
- `krun`: exit `0`; final `<k>` was `.K`, `<exc>` was `NoExc`, and
  `<exit-code>` was `0`.
- Haskell compilation: exit `0`.
- Unfiltered `kprove spec.k`: `#Top`, exit `0`.
- `python3 differential_test.py`:
  `tested=7230 mismatches=0`, exit `0`.
- False-result mutation: `WarnStuckClaimState`, exit `1`; residual result was
  `list(.ValSeq)` rather than `noneV`.
- Reversed-comparison body mutation: `WarnStuckClaimState`, exit `1`; residual
  result was the modeled `["b"]` rather than `["a"]`.

Artifact hashes at validation time:

```text
1d2b5b54bcd51e7ce63a0ea7e2529dd3f538a99acfa7fb589156b986195deccc  solution.py
852197320f51a13d590ee2626ddcc6c0af36bfca9bed3dc371b2a93e87a144cd  solution.mpy
faca9c79e3e682c7c55c83a5a3d8488cd94981b6a0a22672628775aaed76ac9e  verification.k
7e88841f165d367df30000dbd03555267e39d4ab4bbf94f1921e9a1a4c65ffc9  spec.k
57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97  reference-semantics/semantics.k
```

## Gate results

### Gate A — PASS

- **A1:** The exact module is loaded and its program-defined bodies execute.
  Regeneration matches `solution.mpy`. Reversing the comparison invalidates
  the expected result on a concrete equal-length witness.
- **A2:** The loop claim accounts for its two local writes and preserves all
  other cells. Entry claims constrain the result and exact final module/frame,
  heap, exception, and exit state.
- **A3:** Fixed semantics performs all lookup, argument evaluation, calls,
  loop control, return, and cleanup. The invariant pins the reachable plain
  frame and builtin lookup chain. No operational bridge exists.
- **A4:** Every proof-local function has exhaustive, disjoint, descending
  equations. The only simplification lemma is true over its complete guard.
- **A5:** Empty lists satisfy the precondition (`0 <= 0`). The deliberately
  false `noneV` result is rejected with the real empty-list result visible in
  the residual.

### Gate B — PASS

The formal domain is exactly two finite modeled lists of strings, matching the
prompt. The postcondition compares the sum of every string's modeled length
and explicitly chooses the first list on equality. The five prompt examples
pass under concrete K execution and CPython.

The symbolic claims use the semantics-supported unboxed read-only list inputs;
the implementation does not mutate them. The result is the exact selected
input list value. This is adequate for the HumanEval list-result property.

### Gate C — PASS

All commands, artifacts, scopes, oracles, exits, and residual outcomes are
recorded and reproducible. The proof-local trust ledger contains no opaque or
unproved primitive. Positive K execution, negative mutation probes, K prompt
examples, and independent differential evidence are separated above.

## Trust boundary

Trusted components are the supplied read-only `reference-semantics/`, the
supplied `py2mpy.py` translator, the K frontend/backend and its logical
implementation, and the backend arithmetic/SMT reasoning. The entry theorem is
conditional on those components faithfully implementing their stated
semantics. No proof-local rule is treated as an external primitive.

CPython and the independently written differential oracle are empirical
evidence, not axioms used to close `kprove`.

## Empirically supported facts

- `smoke.py` contains the exact implementation plus all five prompt examples;
  its translated K program terminates successfully.
- `differential_test.py` compares object selection against an independent
  `len("".join(...))` oracle over all pairs of lists of length zero through
  three drawn from `("", "a", "bc", "XYZ")`, plus the five prompt examples:
  7,230 checks and zero mismatches.
- The two mutation artifacts both fail for their documented ground witnesses.

## Excluded behavior

- Inputs other than two finite lists of strings are outside the formal
  precondition; their Python exceptions are not modeled by this theorem.
- Total correctness, resource bounds, and termination are not claimed.
- The concrete string-literal path in the supplied semantics is ASCII-only;
  the symbolic theorem ranges over modeled `IntSeq` strings, while concrete
  validation uses ASCII examples.
- Behaviors absent from the supplied subset, and correctness of the supplied
  semantics or K implementation relative to CPython, remain in the trust
  boundary.
