VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact bound body of
`reverse_delete(s, c)` is partially correct for every pair of symbolic string
values `str(S)` and `str(C)`, where `S` and `C` are arbitrary `IntSeq` values.
If the call terminates normally, it returns:

```k
tuple(vCons(
  str(deleteAcc(S, C, .IntSeq)),
  vCons(
    deleteAcc(S, C, .IntSeq)
      ==K reverseDeleteAcc(S, C, .IntSeq),
    .ValSeq)))
```

`deleteAcc` retains, in order, exactly the characters of `S` whose one-character
string is not contained in `C`. `reverseDeleteAcc` retains the same characters
in reverse order. Thus the first component is the requested deletion result,
and the second is true exactly when that result reads the same forward and
backward.

This is a K reachability proof of partial correctness. Termination is not a
separate proved liveness theorem.

## Formal claims and scope

`SPEC.reverse-delete-loop` is the loop circularity. From a loop head with
remaining input `S`, result accumulator `A`, and reverse accumulator `R`, it
proves that fixed execution leaves:

```k
"result"          |-> str(deleteAcc(S, C, A))
"reversed_result" |-> str(reverseDeleteAcc(S, C, R))
```

It also frames the continuation, original input binding, environment, heap,
allocation counters, stack, return state, exception state, and exit code. The
only intentionally unconstrained final local is `ch`, which is not observable
after the function frame is popped.

`SPEC.reverse-delete-entry` starts at ordinary `Call` evaluation with the
module binding pinned to the exact parameter list and body from `solution.mpy`.
It constrains the returned tuple and preserves the initial module environment,
empty heap, allocation counters, empty stack, normal return state, `NoExc`, and
exit code `0`.

The formal input domain is exactly two `str(IntSeq)` values, with no additional
precondition. Non-string Python objects are outside the theorem.

## Proof-extension inventory

### `deleteAcc`

- **Class:** Definitional summary.
- **Semantic role:** Names the result accumulator after the remaining loop
  iterations; it never matches or rewrites a program computation.
- **Domain:** All triples `(S, C, ACC)` of sort `IntSeq`.
- **Matched context:** A pure `deleteAcc` term only; no continuation, binding,
  control stack, or configuration cell is matched.
- **Justification scope and containment:** `.IntSeq` and `iCons` exhaust
  `IntSeq`. The step uses an explicit Boolean conditional on the same
  `strContains(iCons(X, .IntSeq), C)` computed by fixed string membership.
  Every use is inside this complete domain.
- **State footprint:** None.
- **Value influence:** The first tuple component and, through equality with
  `reverseDeleteAcc`, the Boolean result.
- **Value justification:** The base returns the existing accumulator. The step
  either skips a deleted code or appends the retained code with the supplied
  `seqConcat`.
- **Justification:** Structural recursion on the strict suffix `XS`; constructor
  coverage is exhaustive and the conditional cases are disjoint.
- **Dependents:** `reverse-delete-loop` and `reverse-delete-entry`.
- **Control/value validation:** No control effect. The positive proof connects
  it to fixed loop execution; the false-result probe and differential tests
  discriminate its value.

### `reverseDeleteAcc`

- **Class:** Definitional summary.
- **Semantic role:** Names the reverse accumulator after the remaining loop
  iterations; it does not replace execution.
- **Domain:** All triples `(S, C, ACC)` of sort `IntSeq`.
- **Matched context:** A pure `reverseDeleteAcc` term only.
- **Justification scope and containment:** The same exhaustive `.IntSeq` /
  `iCons` split and the same fixed-semantics membership condition as
  `deleteAcc`.
- **State footprint:** None.
- **Value influence:** The returned palindrome Boolean.
- **Value justification:** A retained code is prepended to the accumulator,
  exactly matching `ch + reversed_result`; a deleted code leaves it unchanged.
- **Justification:** Structural recursion on `XS`, with total constructor
  coverage and a total Boolean conditional.
- **Dependents:** `reverse-delete-loop` and `reverse-delete-entry`.
- **Control/value validation:** No control effect. Fixed execution, the
  false-result probe, and differential tests validate the affected value.

### `SPEC.reverse-delete-loop`

- **Class:** Derived lemma (loop circularity).
- **Semantic role:** States the partial-correctness summary of the fixed
  `#loop`; it is a reachability claim, not an ordinary rewrite or operational
  bridge.
- **Domain:** All symbolic remaining strings and accumulators in the exact
  normal loop-head configuration, with `L` fresh from `REST`.
- **Matched context:** The exact `#loop(str(S), Name("ch"), BODY)` term, the
  exact local bindings and parent, an arbitrary framed continuation, and every
  configuration cell.
- **Justification scope and containment:** Its match domain and proved claim
  domain are identical. No weaker guard, omitted cell, abrupt control, or
  broader continuation is introduced.
- **State footprint:** Reads `c`; writes `ch`, `result`, and
  `reversed_result`; preserves all framed cells and bindings.
- **Value influence:** Both returned tuple components through the two
  accumulators.
- **Value justification:** The two total summaries above.
- **Justification:** `kprove` closes the empty case and both membership step
  cases coinductively under fixed semantics.
- **Dependents:** `SPEC.reverse-delete-entry`.
- **Control/value validation:** The changed-body probe no longer matches the
  original behavior and is rejected; the false-result probe is also rejected.

There are no proof-local opaque symbols, `[simplification]` axioms, priority
rules, concrete rules, or operational bridges.

## Commands and actual results

The complete reproducible command is:

```bash
./prove.sh
```

It exited `0`. The script contains and ran these positive build/proof commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 check_identity.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
python3 differential.py --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual relevant output and process status:

```text
Program identity: prompt signature, solution.mpy, and spec body match
krun: <k> .K </k>, <exc> NoExc </exc>, <exit-code> 0 </exit-code>
CPython oracle cases: 113; mismatches: 0
K differential cases: 110; mismatches: 0
kprove: #Top
kprove exit: 0
```

Both `kompile` commands exited `0`. LLVM emitted non-exhaustiveness warnings
from unrelated supplied builtin/float/subscript functions, and both builds
emitted the supplied `strLt` unused-variable warnings. None of those operations
is used by this target proof.

The A5 mutation command was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited `1` with `WarnStuckClaimState`; its residual contained the actual
result:

```text
tuple ( vCons ( str ( .IntSeq ) , vCons ( true , .ValSeq ) ) )
```

This contradicts the deliberately requested `("", false)` result.

The body-sensitivity command was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

It exited `1` with `WarnStuckClaimState`; after removing the result update, its
residual contained:

```text
tuple ( vCons ( str ( .IntSeq ) , vCons ( false , .ValSeq ) ) )
```

This contradicts the original expected `("bcd", false)` for
`("abcde", "ae")`.

The complete outputs are preserved in `smoke.out`, `identity.out`,
`differential.out`, `proof-positive.out`, `proof-vacuity.out`, and
`proof-body-mutation.out`.

## Gate results

### Gate A — PASS

- **A1:** `check_identity.py` confirms the prompt signature, regenerated
  `solution.mpy`, and exact closure body embedded in `spec.k`. The material body
  mutation is rejected with exit `1`.
- **A2:** No operational bridge exists. Fixed semantics executes every
  assignment, membership test, concatenation, tuple construction, comparison,
  return, and frame pop. All configuration cells are represented in the loop
  claim and entry claim.
- **A3:** The entry state pins the exact binding and body. Normal name lookup,
  left-to-right argument evaluation, call frame creation, loop control, return,
  and frame restoration execute under `MPY`.
- **A4:** Both proof-local functions cover the two `IntSeq` constructors, use a
  total Boolean conditional, and recurse on a strict suffix. There are no
  overlapping equations with inconsistent right-hand sides.
- **A5:** Empty strings realize the precondition. The entry claim constrains
  both tuple fields, and `spec-vacuity.k` rejects the false Boolean result.

### Gate B — PASS

- **B1:** The prompt requires strings; the theorem quantifies over exactly two
  semantic string values and imposes no silent content or length restriction.
- **B2:** The reference model represents a string as a sequence of integer
  character codes. Iteration, one-character membership, concatenation, and
  equality are the material operations, and their modeled behavior matches the
  task. Concrete K string literals are ASCII-only; the symbolic theorem itself
  is over arbitrary `IntSeq`.
- **B3:** Fixed execution is formally connected to both summaries by the loop
  claim. Structurally, `deleteAcc` is the order-preserving deletion fold and
  `reverseDeleteAcc` is the same fold with retained characters prepended.
  Equality of those two empty-accumulator results is exactly the palindrome
  condition. This intent bridge is also independently supported by the
  differential tests.
- **B4:** The implementation agrees with all prompt examples and the broader
  oracle sample.

### Gate C — PASS

- **C1:** The trust ledger below names every component outside the target
  theorem. No unrecorded proof-local primitive is used.
- **C2:** All reported artifacts exist, all commands are in `prove.sh`, and
  the final integrated run exited `0`. Positive and expected-failure outputs
  are preserved separately.
- **C3:** `#Top` is reported only as target-proof execution. The formal theorem,
  empirical evidence, trust assumptions, and exclusions are kept distinct.

## Trust boundary

| Component | Effect | Dependents | Evidence |
|---|---|---|---|
| Supplied `reference-semantics/` | Defines Python execution and string representation | Both claims | Required fixed reference; LLVM smoke and K differential execution |
| Supplied `py2mpy.py` | Maps CPython AST to the `.mpy` term | Program identity | `check_identity.py` regenerates and byte-compares `solution.mpy` |
| K compiler, Haskell backend, LLVM backend, and solver | Execute and prove the K definitions | All formal results | Version `v7.1.293`; reproducible successful run |
| Abstract `IntSeq`/Python-string correspondence | Connects the model to the prompt's notion of string | Gate B interpretation | Operation-by-operation inspection; ASCII K tests and Unicode CPython tests |

No float, sort, digest, or other opaque primitive in the supplied semantics is
reachable from this program.

## Empirical evidence

`smoke.py` runs all three prompt examples plus empty and unchanged-palindrome
edge cases through LLVM `krun`.

`differential.py` uses an independent oracle based on a deletion set,
`join`, and slicing. It checked 113 CPython cases with zero mismatches,
including three Unicode examples. It also generated one translated K program
covering 110 ASCII cases and observed normal completion with zero assertion
failures. These are finite validation results, not universal proofs.

## Excluded behavior

- Calls with non-string arguments.
- CPython implementation details not represented by the supplied semantics,
  including concrete non-ASCII literal decoding and exception behavior outside
  the modeled operations.
- A separate total-correctness or resource-bound theorem.
- Correctness of the supplied translator, reference semantics, K backends, and
  solver themselves; these are the explicit trust base.
- The expected-failure mutation claims as positive target proofs.
