VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, calling the exact translated
`string_xor` closure on two bit strings terminates with the pairwise XOR string.
Pairing uses the supplied `zip` behavior, so unequal inputs are truncated to
the shorter length.

This is a partial-correctness reachability proof.  The entry theorem assumes
the arguments have the K values `str(A)` and `str(B)` and requires
`bitString(A) andBool bitString(B)`.  It proves a returned value `str(OUT)` with

```k
OUT ==K xorAcc(.IntSeq, A, B)
```

`xorAcc` appends code 48 (`"0"`) when a paired pair of bits is equal and code
49 (`"1"`) when it is unequal, stopping when either input is empty.  On the
formal bit-string domain, this is exactly the binary XOR truth table.

## Formal claims

`LOOP-SPEC.loop-invariant` is proved against the bridge-free
`VERIFICATION-BASE` definition.  For an arbitrary continuation and arbitrary
outer configuration cells, it executes the actual `#loop(zipObjS(A,B),...)`
with the exact source target and body.  The active plain local frame contains
exactly `a`, `b`, `result`, `x`, and `y`.  The theorem:

- changes `result` from `str(R)` to `str(xorAcc(R,A,B))`;
- changes `x` and `y` to their exact final loop-target values `lastX(...)` and
  `lastY(...)`;
- preserves `a`, `b`, the parent, outer scopes, all other cells, and the
  arbitrary continuation.

`SPEC.string-xor` is proved against `VERIFICATION`.  Its initial module scope
pins the name `string_xor` to a closure whose parameters and body are the exact
translation of `solution.py`.  Normal lookup, argument binding, frame
creation, initialization, return, and frame popping execute under the fixed
semantics.  The loop is discharged by an operational rule derived from the
separately proved loop theorem.

## Proof-extension inventory

### `xorAcc`

- Class: definitional summary.
- Semantic role: names the accumulated result; it does not match or replace a
  program term.
- Domain: every triple of `IntSeq` values.
- Matched context/state footprint: none; it is a pure function.
- Coverage: first sequence empty; first nonempty and second empty; or both
  nonempty split by integer equality/inequality.  These cases are exhaustive
  and pairwise disjoint.
- Termination: each recursive rule removes one constructor from both input
  sequences.
- Value influence: fixes the loop result and entry postcondition.
- Justification: the four guarded equations are the definition of the
  equality/inequality encoding performed by the source body.  Their
  `[simplification]` attributes expose the same equations to the implication
  checker and add no new equation.
- Dependents: both formal claims.

### `bitString`

- Class: definitional summary/predicate.
- Semantic role: states the HumanEval input domain; it replaces no execution.
- Domain: every `IntSeq`.
- Coverage and overlap: empty versus `iCons`, which are exhaustive and
  disjoint.
- Termination: structural recursion on the tail.
- Value influence: restricts only the entry theorem to codes 48 and 49.
- Justification: direct structural definition.
- Dependent: `SPEC.string-xor`.

### `lastX` and `lastY`

- Class: definitional summaries.
- Semantic role: describe the exact final values of the two Python loop-target
  bindings; they replace no execution.
- Domain: every initial `Val` and pair of `IntSeq` values.
- Coverage: first sequence empty; first nonempty and second empty; or both
  nonempty.  The cases are exhaustive and disjoint.
- Termination: the recursive case removes one constructor from each sequence.
- State/value influence: only the proof of the final local `x` and `y`
  bindings.
- Justification: direct definition of the last pair yielded by truncating
  `zip`; the bridge-free loop theorem independently checks these values.
- Dependent: `LOOP-SPEC.loop-invariant` and the derived loop rule.

### Derived loop operational rule

- Class: operational bridge.
- Semantic role: replaces execution of the exact source `#loop` after `zip`
  has already evaluated to `zipObjS(A,B)`.
- Complete matched context: the exact tuple target, exact `if`/`AugAssign`
  body, arbitrary active continuation, active environment `L`, an exact plain
  local map with keys `a`, `b`, `result`, `x`, and `y`, arbitrary parent, and
  framed outer scopes and other configuration cells.
- Justification scope: `LOOP-SPEC.loop-invariant` has textually identical LHS,
  RHS, frames, and domain and is proved universally using
  `verification-base-kompiled`, which does not import the bridge.
- Context containment: `check_artifacts.py` compares normalized bridge and
  connection-claim text and reports
  `bridge_matches_connection_claim=true`; therefore the rule accepts no
  configuration outside the proved domain.
- State footprint: reads `env` and the active scope; preserves `a`, `b`,
  parent, outer scopes, arbitrary continuation, and every omitted cell;
  writes exactly `result`, `x`, and `y` as proved by the connection theorem.
- Control: consumes only the loop and preserves the arbitrary continuation.
  It introduces no return, frame pop, exception, break, or continue.
- Value influence: `xorAcc` determines the eventual returned result;
  `lastX/lastY` determine otherwise unobservable locals.
- Validation: the bridge-free universal connection proof prints `#Top`; fixed
  LLVM and bridge-enabled Haskell runs pass the same concrete assertion
  harness; swapping the source branches while retaining the summary is
  rejected.
- Dependent: `SPEC.string-xor`.

There are no opaque result symbols or trusted program-defined primitives.

## Exact commands and actual results

The complete executable record is [prove.sh](prove.sh).  Its positive target
proof commands are:

```bash
kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-invariant
```

Actual output: `#Top`. Exit status: `0`.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.string-xor
```

Actual output: `#Top`. Exit status: `0`.

The build and concrete-execution commands are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 check_artifacts.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete_tests.mpy --definition runtime-kompiled --output none

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

krun concrete_tests.mpy \
  --definition verification-kompiled \
  --output none
```

All three `kompile` commands exited `0`.  They printed only pre-existing
exhaustiveness/unused-variable warnings from the supplied semantics and unused
proof framing variables.  Both `krun` commands
exited `0`; output was intentionally suppressed, while failed assertions would
set the modeled exit code and make the command fail.

`python3 check_artifacts.py` exited `0` and printed:

```text
translation_matches=true
concrete_function_matches=true
entry_closure_matches=true
bridge_matches_connection_claim=true
```

`python3 validation_test.py` exited `0` and printed:

```text
pairs=3969 mismatches=0
```

The A5 false-postcondition command was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited `1` with `WarnStuckClaimState`.  The residual result was
`str(.IntSeq)` while the deliberately false destination was
`str(iCons(48,.IntSeq))`.

The body-sensitivity command was:

```bash
kprove spec-body-mutation.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC-BODY-MUTATION
```

It exited `1` with `WarnStuckClaimState`.  The residual showed the unequal
obligation between the original `"0"` append summary and the mutated `"1"`
append execution.

## Gate results

### Gate A — PASS

- A1: `solution.mpy` is regenerated from `solution.py`; the exact closure in
  the entry claim is mechanically checked against that term.  Function lookup,
  binding, initialization, and return execute normally.  The only displaced
  code is covered by the bridge-free universal loop theorem.  The swapped-body
  mutation fails.
- A2: the bridge changes exactly `result`, `x`, and `y`; the connection theorem
  proves those values and preservation of all framed state.
- A3: `zip` and arguments execute before the bridge.  Target binding, branch
  selection, evaluation order, arbitrary continuation preservation, and local
  updates are covered by the exact connection theorem.  The bridge introduces
  no abrupt control.
- A4: all equations have exhaustive, non-overlapping constructor/guard cases
  and structurally descend.  The bridge match domain is identical to its
  justification domain.
- A5: empty strings realize the precondition.  The entry postcondition
  constrains the returned codes, and the false `"0"` result mutation is
  rejected with a meaningful residual.

### Gate B — PASS

- B1: the formal domain is exactly two strings made only from `"0"` and `"1"`;
  lengths may differ.
- B2: for this domain, the supplied ASCII `IntSeq` string model, string
  equality, and truncating `zip` agree with the relevant CPython behavior.
- B3: the `xorAcc` cases formally encode the four bit-XOR cases.  Independent
  differential testing supplies finite additional evidence.
- B4: the implementation and theorem produce the prompt example `"100"` and
  agree on empty, unequal-length, and differing-bit boundary cases.

### Gate C — PASS

- C1: no unproved proof-local primitive remains.  The operational bridge is
  backed by a bridge-free universal theorem.  The remaining trust boundary is
  listed below.
- C2: all claimed artifacts exist, and `prove.sh` records builds, positive
  proofs, concrete tests, differential tests, and both expected-failure probes.
- C3: formal results, finite evidence, trust, and exclusions are separated in
  this report.

## Trust boundary

- The supplied, read-only `reference-semantics/` definition is trusted as the
  intended Python subset model.
- The K compiler, Haskell/LLVM backends, solver integration, and their runtime
  are trusted.
- The supplied `py2mpy.py` translator is trusted to map CPython AST syntax to
  the documented constructors.  Regeneration and entry-closure checks prevent
  accidental artifact drift but do not prove the translator implementation.
- The CPython differential oracle in `validation_test.py` is independent test
  evidence, not an axiom in either K proof.

## Empirically supported facts

- Fixed LLVM semantics and bridge-enabled Haskell semantics both pass:
  `("010","110") -> "100"`, `("","") -> ""`,
  `("1","0") -> "1"`, and `("1011","01") -> "11"`.
- The independent oracle uses Python integer XOR on each pair from Python
  `zip`.  Exhausting all two-bit-alphabet strings of lengths zero through five
  gives 3,969 input pairs and zero mismatches.
- Artifact checks show that the translated program, concrete harness function,
  entry closure, bridge, and connection theorem have not drifted apart.

## Excluded behavior

- Inputs containing characters other than `"0"` and `"1"` and non-string
  arguments are outside the entry theorem.
- Behavior not modeled by the supplied Python subset is not claimed.
- The theorem intentionally uses truncating `zip` for unequal lengths.
- This is a partial-correctness proof; it does not separately establish a
  liveness/termination theorem.
