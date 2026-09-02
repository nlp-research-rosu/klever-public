VALIDATED

# What is proven

Under the supplied `MPY` reference semantics, for every pair of string values
`str(A)` and `str(B)`, loading the exact translated body of
`cycpattern_check`, calling it with those values, and terminating produces
`cycPattern(A, B)`.  The final configuration restores the caller environment,
scope allocation counter, empty heap and stack, return cell, exception cell,
and exit code.  This is a partial-correctness reachability theorem.

`cycPattern(A, B)` starts with `strContains(B, A)`, then folds over the exact
reference-semantics value of `B[:-1]`.  On each character it performs the
normalized value of `rotation[1:] + c` and ORs
`strContains(rotation, A)` into the result.  Thus it checks `B` and every
non-identity left rotation of `B`.  For empty `B`, it returns true because the
empty string itself is a substring.

# Formal claims

- `SPEC.cyc-loop` is the circularity for the exact `#loop` term and exact loop
  body.  It accounts for the final values of `c`, `rotation`, and `result`.
- `SPEC.cycpattern-check` begins at `#loadAll(Module(FuncDef(...)))`, contains
  the exact body translated from `solution.py`, resolves the exact function
  binding, executes the call, and reaches `cycPattern(A, B)`.
- The formal input domain is all `IntSeq` values wrapped as semantic strings.
  Non-string Python arguments are outside the claim.
- The observed result is the returned Boolean.  The whole-program claim also
  fixes all final configuration cells.

# Proof-extension inventory

There are no operational bridges, priority rules, simplification axioms,
opaque values, or trusted proof-local primitives.

## `rotateWith`

- Class: definitional summary.
- Role and domain: for every `ROT:IntSeq` and `C:Int`, names the value of the
  source update `rotation[1:] + c`.
- Matched context: none; it never matches or replaces an operational
  configuration.
- Definition: one unconditional equation to the exact normalized
  `seqConcat(buildIS(... clampHi ...), iCons(C, .IntSeq))` value produced by
  the supplied slice and string-concatenation semantics.
- Context containment and footprint: not applicable to a pure term; it reads
  only its arguments and writes no cell.
- Value influence: affects the summarized final rotation and Boolean result.
- Justification and dependents: the universal `SPEC.cyc-loop` claim executes
  the real slice and concatenation rules for arbitrary `ROT` and `C`, reaching
  this exact value.  `cycScan` and `finalRotation` depend on it.
- Validation: the loop claim printed `#Top`; concrete true and false witnesses,
  the false-result probe, and the body mutation all behaved discriminatingly.

## `cycScan`

- Class: definitional summary.
- Role and domain: exact Boolean fold for all `A`, remaining iterator
  sequences, rotations, and accumulated Booleans.
- Definition: disjoint, exhaustive `.IntSeq` and `iCons` equations.  The step
  recurses on the proper tail `REST`, so it terminates structurally.
- Matched context and footprint: no operational context or cells; arguments
  only.
- Value influence: it is the loop result and ultimately the returned Boolean.
- Justification and dependents: its base and step are exactly the two
  `#iterNext` outcomes proved by `SPEC.cyc-loop`; `cycPattern` and both positive
  claims depend on it.
- Validation: fixed-semantics execution re-establishes the circularity after
  one constructor step, and the false-result probe rejects the opposite value.

## `finalRotation` and `finalChar`

- Class: definitional summaries.
- Role and domain: name the final local values for every remaining iterator
  sequence and current local value.
- Definition: each has disjoint, exhaustive `.IntSeq` and `iCons` equations
  and recurses on `REST`.
- Matched context and footprint: no operational context or cell replacement.
  Their values account for, rather than abstract away, the two locals written
  by the loop.
- Value influence: `finalRotation` also feeds the execution characterization;
  `finalChar` only constrains an otherwise unobservable local that is removed
  when the call frame pops.
- Justification and dependents: `SPEC.cyc-loop` proves both summaries while
  executing the actual target binding and assignments.  The loop claim is
  their only dependent.
- Validation: exhaustive constructor coverage, structural descent, and
  `SPEC.cyc-loop` output `#Top`.

## `cycPattern`

- Class: definitional summary.
- Role and domain: the intended result for all `A:IntSeq` and `B:IntSeq`.
- Definition: one unconditional equation instantiating `cycScan` with `B`,
  `strContains(B, A)`, and the exact normalized reference value of `B[:-1]`.
- Matched context and footprint: no operational context and no state.
- Value influence: it is the whole-program postcondition.
- Justification and dependents: the entry claim reaches the same normalized
  slice through fixed execution, then applies the proved loop claim.  The
  whole-program claim depends on it.
- Validation: all-claims `kprove` output `#Top`, the false-result probe stopped
  at `true` against `false`, and the independent oracle had zero mismatches.

## `SPEC.cyc-loop`

- Class: derived reachability lemma/circularity.
- Semantic role: executes the fixed `#loop`, iterator, target binding, slice,
  concatenation, substring test, Boolean short-circuit, assignments, and loop
  control.  It is not a rule and does not preempt execution.
- Domain: arbitrary semantic strings `A` and `B`, arbitrary `REMAIN`, `ROT`,
  `CURRENT`, and `FOUND`, in the exact ordinary function-local scope.  The
  module and builtin scopes are pinned, preventing shadow or closure-cell
  branches.
- Matched context: exact loop body at the head of `<k>` with an arbitrary
  continuation; exact local/module/builtin scope structure; other
  configuration cells are universally framed.
- Justification scope and containment: `kprove` proves that same universal
  framed configuration directly from the fixed semantics.  The body has no
  `return`, `break`, exception, or cleanup effect, so the continuation frame is
  preserved.
- State footprint: reads `a`, `c`, `rotation`, and `result`; writes `c`,
  `rotation`, and `result`; preserves `b`, environment, module/builtin scopes,
  heap, stack, return, exception, exit code, and continuation.
- Value/control justification: each iterator constructor executes once before
  the circularity is reapplied; the empty iterator exits normally.
- Dependents: `SPEC.cycpattern-check`.
- Validation: the focused claim and the final all-claims command both printed
  `#Top`.  The mutated program body is rejected.

# Exact commands and actual results

The complete reproducible workflow is `./prove.sh`.  Its final run exited 0.
The script contains these positive commands:

```sh
python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py smoke.py > smoke.mpy
python3 smoke.py
krun smoke.mpy --definition runtime-kompiled
python3 differential_test.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual final results:

- Translator regeneration exited 0, and an independent
  `python3 py2mpy.py solution.py | cmp -s - solution.mpy` exited 0.
- CPython smoke assertions exited 0.
- LLVM `krun` ended with `<k> .K </k>`, `<exc> NoExc </exc>`, and
  `<exit-code> 0 </exit-code>`.
- `python3 differential_test.py` printed
  `cases=967 mismatches=0` and exited 0.
- Haskell compilation exited 0.
- The all-claims `kprove` printed `#Top` and exited 0.
- Compiler warnings came from unchanged reference modules: unused variables in
  `strLt` and non-exhaustive declarations in unrelated float/list/method
  helpers.  No warning identifies a proof-local equation or a used missing
  case.

The Gate A negative commands were:

```sh
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity-probe.log 2>&1
vacuity_status=$?

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > body-mutation-probe.log 2>&1
body_status=$?
set -e
```

Both exited 1 as expected.  Their complete outputs are preserved in
`vacuity-probe.log` and `body-mutation-probe.log`.

- The false-result residual contains `<k> true ~> .K </k>` while the claim
  requires `false`.
- The body mutation replaces the exact function body with `return False`; its
  residual contains `<k> false ~> .K </k>` while the witness claim requires
  `true`.

# Gate results

## Gate A — PASS

- A1: the entry claim loads and calls the exact translated function body; all
  program-defined code executes under fixed semantics.  The material body
  mutation is rejected with exit 1.
- A2: there is no operational bridge.  The loop claim accounts for every local
  write, and the entry claim constrains every final configuration cell.
- A3: fixed rules perform function lookup, left-to-right argument evaluation,
  local binding, loop control, return, frame pop, and exceptional-state
  preservation.  No summary pins or skips those operations.
- A4: all summary equations are exhaustive and non-overlapping.  Recursive
  equations descend on an `IntSeq` tail; unconditional equations cover their
  full declared domains.
- A5: `("hello", "ell")` is a realizable true witness.  The false
  postcondition mutation fails at the opposite concrete result.  The smoke
  suite also includes false witnesses such as `("abcd", "abd")`.

## Gate B — PASS

- The prompt speaks of two words; the formal domain is exactly two semantic
  string values.  Non-string calls are explicitly excluded.
- `B[:-1]` supplies the first `len(B)-1` characters.  Starting from `B`, each
  update drops the current first character and appends the corresponding
  original character.  Finite-sequence induction therefore yields each left
  rotation exactly once, while the initial `strContains(B, A)` covers the
  identity rotation.
- `strContains` is the supplied contiguous-subsequence definition, so the
  summary matches “is a substring”.
- All six prompt examples pass under both CPython and LLVM `krun`.  Empty `B`
  is true because the contract explicitly includes the second word itself.
- The fixed semantics models strings as integer-code sequences and only loads
  concrete source literals with ASCII codes.  The symbolic theorem itself is
  code-independent and quantifies over arbitrary `IntSeq`; Python behavior
  outside the supplied string subset is not claimed.

## Gate C — PASS

- Trust ledger: there is no unproved proof-local primitive, oracle, rewrite, or
  bridge.  The trust boundary is the user-supplied `reference-semantics/`, K
  compiler/prover/backend, and the partial-correctness interpretation of K
  reachability.
- Reproducible artifacts exist for every claimed check:
  `smoke.py`/`smoke.mpy`, `differential_test.py`,
  `spec-vacuity.k`/`vacuity-probe.log`, and
  `spec-body-mutation.k`/`body-mutation-probe.log`.
- The independent oracle directly enumerates rotations with slicing and
  `any`; it does not reuse the implementation's rotating accumulator or the K
  summary equations.  It covers the six examples and all 961 pairs of binary
  words of lengths 0 through 4.
- Formal, empirical, and excluded conclusions are separated here.

# Trust boundary and excluded behavior

Formally established: partial correctness of the exact translated program for
all semantic string pairs, including the complete fixed-semantics state
transition.

Empirically supported: agreement with CPython examples and an independent
oracle on 967 finite cases, plus successful LLVM concrete execution.

Trusted: the supplied reference semantics, K toolchain, and backend
implementation.  No task-local value computation is trusted.

Excluded: non-string inputs; CPython features outside the supplied semantics;
concrete non-ASCII source-literal loading; and a machine-checked liveness or
resource bound.  The structural iterator decreases on finite `IntSeq` values,
but the K claims are reported only as partial correctness.
