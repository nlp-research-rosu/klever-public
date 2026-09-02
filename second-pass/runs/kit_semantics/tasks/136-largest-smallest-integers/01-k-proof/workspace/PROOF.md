VALIDATED

## What is proven

For every finite list of mathematical integers, loading the exact translated
definition of `largest_smallest_integers` and calling it terminates, under the
supplied semantics and proof extensions described below, with a two-element
tuple:

- the largest negative integer (the negative integer closest to zero), or
  `None` when no negative integer occurs; and
- the smallest positive integer, or `None` when no positive integer occurs.

The K reachability claims establish partial correctness. The concrete and
differential tests provide additional termination and intent evidence for the
tested inputs; they are not substitutes for the universal K claims.

## Formal claim

`spec.k` uses `IS:IntSeq` to range over every finite sequence of K integers.
`intVals(IS)` is a structural, one-for-one embedding into the reference
semantics' `ValSeq`. The entry claim starts from the reference initial state,
loads the exact function body represented by `lsiBody`, resolves the function
name, creates and pops the call frame, and returns:

```k
tuple(vCons(negativeResult(scanNeg(IS, 0)),
       vCons(positiveResult(scanPos(IS, 0)), .ValSeq)))
```

It also constrains the final environment, module binding, scope allocator,
heap, heap allocator, stack, return cell, exception cell, and exit code.

The separately compiled `loop-spec.k` claim proves the loop transition without
the loop-summary rule. It is the universal connection theorem for the
operational bridge in `verification.k`.

## Proof-extension inventory

### Syntactic aliases

`lsiLoopBody` and `lsiBody` are compile-time macros. They do not rewrite a
running configuration. Their expansions are the constructor tree emitted for
`solution.py`; regeneration comparison exits 0:

```text
cmp solution.mpy <(python3 py2mpy.py solution.py)
Exit: 0
```

The body includes lookup, iteration, comparisons, branches, assignments,
tuple construction, return, and call-frame cleanup from the supplied
semantics.

### `intVals` representation

- **Extension:** `intVals`, its `.IntSeq` and `iCons` equations, and the two
  exact `#iterNext(list(intVals(...)))` exposure rules in `representation.k`.
- **Class:** Definitional representation.
- **Semantic role:** Represents an arbitrary finite integer input list. The
  exposure rules reveal one constructor; they then leave the actual
  `#iterNext(list(.ValSeq))` or `#iterNext(list(vCons(...)))` step to the
  supplied semantics.
- **Domain:** Exactly `.IntSeq` or `iCons(I, IS)`, which are disjoint and
  exhaustive for `IntSeq`.
- **Matched context:** Only
  `#iterNext(list(intVals(...))) ~> KREST`; all configuration cells are framed.
- **Justification scope and containment:** The two cases preserve the same
  arbitrary continuation and all cells. `connection-spec.k` checks both
  resulting supplied-iterator behaviors and closes with `#Top`.
- **State footprint:** No state cell is read or written. Only the represented
  iterator argument is exposed.
- **Value influence:** Determines the successive integer values supplied to
  the loop.
- **Value justification:** The constructor equations are a one-for-one,
  order-preserving structural embedding with no opaque values.
- **Dependents:** `loop-spec.k`, the loop bridge, and both claims in `spec.k`.
- **Validation:** The empty/cons connection claims pass; concrete K tests use
  ordinary allocated lists; the Python differential test covers 19,608 lists.

### Mathematical summaries

- **Extensions:** `takeNeg`, `takePos`, `nextNeg`, `nextPos`, `scanNeg`,
  `scanPos`, `lastValue`, `negativeResult`, and `positiveResult`.
- **Class:** Definitional summaries.
- **Semantic role:** They name final candidate values; they do not intercept a
  Python expression or replace program execution.
- **Domain and equations:** `takeNeg`/`takePos` have unconditional equations.
  Each `next` function splits on a predicate and its negation. Each `scan` and
  `lastValue` function splits on the two `IntSeq` constructors and decreases
  structurally. Each result function splits on zero versus nonzero.
- **Overlap and coverage:** All guarded pairs are disjoint and exhaustive;
  all recursive calls use a strict sequence tail. Every `[total]` declaration
  is therefore covered.
- **Matched context and state footprint:** Equational terms only; no
  continuation, binding, or state cell is matched or changed.
- **Value influence:** They determine the loop bridge's final locals and the
  entry claim's returned tuple.
- **Value justification:** `nextNeg` replaces the candidate exactly when the
  current integer is negative and either no candidate exists or it is larger.
  `nextPos` is the dual rule for the smallest positive integer. Structural
  induction over `IntSeq` gives the stated meanings of `scanNeg` and
  `scanPos`. `lastValue` precisely accounts for the loop-target local even
  though that local is deallocated on return.
- **Dependents:** The bridge-free loop claim, the operational loop bridge, and
  the target claims.
- **Validation:** The bridge-free loop theorem, false-result mutation,
  concrete K assertions, and independent Python oracle all agree.

### Loop-summary rule

- **Extension:** The single priority-40 rule in `verification.k`.
- **Class:** Operational bridge.
- **Semantic role:** Replaces execution of the exact loop after that execution
  has been universally connected to the stated scope update.
- **Domain:** `N <=Int 0`, `P >=Int 0`, exact `lsiLoopBody`, exact environment
  location 1, exact local keys and types, exact module binding and function
  body, an arbitrary builtins scope, and an arbitrary continuation.
- **Matched context:** The rule and `loop-spec.k` both match
  `#loop(list(intVals(IS)), Name("value"), lsiLoopBody) ~> KREST`, the same
  scope maps, and the same framed/omitted cells.
- **Justification scope:** `loop-spec.k` imports `verification-core.k`, which
  contains no loop-summary rule. Its `loop-connection` claim is textually the
  same transition and guard and prints `#Top`.
- **Context containment:** The connection theorem is quantified over the same
  arbitrary continuation and the same omitted cells; the bridge is not more
  general.
- **State footprint:** Reads the current negative candidate, positive
  candidate, current loop-target value, and remaining sequence. Writes exactly
  those three locals to `scanNeg`, `scanPos`, and `lastValue`. It preserves
  `lst`, module and builtins scopes, environment, heap, allocators, stack,
  return state, exception state, exit code, and continuation.
- **Control fidelity:** The bridge rewrites only the loop to `.K` and preserves
  the continuation. It does not return, pop a frame, throw, break, or discard a
  suffix.
- **Value influence:** Its candidate summaries determine both returned tuple
  elements.
- **Value justification:** The bridge-free connection theorem executes the
  actual comparisons, Boolean short-circuiting, assignments, and iterator
  steps and proves exactly these values.
- **Dependents:** Both claims in `spec.k`, especially `entry`.
- **Control/value validation:** `loop-spec.k` is the universal bridge-free
  check. `body-mutation-spec.k` changes the negative update and is rejected,
  producing `(-3, None)` instead of `(-1, None)`. `spec-vacuity.k` is also
  rejected on `[-1]`.

## Exact commands and actual outputs

The complete reproducible run is:

```bash
./prove.sh > prove.log 2>&1
```

Actual result: exit 0. The script records these commands:

```bash
kompile --version
krun --version
kprove --version

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 -m py_compile solution.py
cmp solution.mpy <(python3 py2mpy.py solution.py)

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell connection.k \
  --main-module CONNECTION --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled --spec-module CONNECTION-SPEC

kompile --backend haskell verification-core.k \
  --main-module VERIFICATION-CORE --syntax-module MPY-SYNTAX \
  --output-definition verification-core-kompiled
kprove loop-spec.k \
  --definition verification-core-kompiled --spec-module LOOP-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled --spec-module SPEC
```

Actual tool version for all three K commands:

```text
K version: v7.1.293
Build date: Fri Oct 03 13:32:35 CDT 2025
```

Actual positive outputs and exits:

```text
connection-spec.k: #Top   Exit: 0
loop-spec.k:       #Top   Exit: 0
spec.k:            #Top   Exit: 0
```

`krun solution.mpy` ended with `<k> .K </k>`, `NoExc`, and exit code 0.
`krun concrete-tests.mpy` ran six calls/assertions and ended with `<k> .K
</k>`, `NoExc`, and exit code 0.

The negative commands are also in `prove.sh`:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled --spec-module SPEC-VACUITY
kprove body-mutation-spec.k \
  --definition body-mutation-kompiled --spec-module BODY-MUTATION-SPEC
```

Actual `spec-vacuity.k` result: exit 1 with `WarnStuckClaimState`; the residual
contains the actual `tuple(vCons(-1, vCons(noneV, .ValSeq)))`, which cannot
match the false `(None, None)` destination.

Actual body-mutation result: exit 1 with `WarnStuckClaimState`; the residual
contains `tuple(vCons(-3, vCons(noneV, .ValSeq)))`, which cannot match the
correct `(-1, None)` destination.

The independent test command and output are:

```bash
python3 differential_test.py
# checked=19608 mismatches=0
# Exit: 0
```

The complete captured output is in `prove.log`.

## Gate results

### Gate A — PASS

- **A1:** The entry claim loads the exact function body. All program-defined
  code executes under the supplied semantics except the loop summary, whose
  exact body/binding/state transition is proved by bridge-free
  `loop-spec.k`. The material body mutation is rejected and exposes the wrong
  concrete result.
- **A2:** The loop theorem and bridge have identical cell patterns. Candidate
  and loop-target updates are explicit; all other state is preserved.
- **A3:** The entry claim fixes module binding, closure body, argument, and
  call-frame state. The bridge fixes the active environment and exact local
  scope and preserves an arbitrary suffix without abrupt control.
- **A4:** All equations have exhaustive, disjoint guards and terminating
  structural recursion. No opaque result-bearing symbol occurs in the proof.
- **A5:** `[-1]` is a realizable witness. The false `(None, None)`
  postcondition is rejected, and the residual shows the real `(-1, None)`
  value.

### Gate B — PASS

- **B1:** `IS:IntSeq` covers every finite list of mathematical integers and
  imposes no value or length bound. Mixed-type lists and booleans are excluded,
  consistently with the task's integer-list contract.
- **B2:** K `Int` is unbounded, matching the relevant Python integer
  arithmetic and comparisons. The supplied list iteration, tuple, `None`,
  function, and control rules cover every construct used.
- **B3:** The recursive summaries apply exactly the closest-to-zero negative
  and smallest-positive candidate updates. Their structural meaning matches
  the natural-language contract, and the independent oracle reports zero
  mismatches.
- **B4:** The implementation returns all three prompt examples and the
  additional negative-only, positive-only, and mixed-sign cases.

### Gate C — PASS

Every proof extension and named assumption is listed here. Every stated
machine result is reproducible through `prove.sh`; `prove.log` contains the
actual output. Positive proof exits, expected negative exits, concrete K
execution, body sensitivity, and differential evidence are kept distinct.

## Trust boundary

- The supplied `reference-semantics/` definition is trusted as the Python
  execution model; no file under it was modified.
- `py2mpy.py` is trusted as the fixed CPython-AST transliterator; it was not
  modified, and regeneration matches `solution.mpy` byte-for-byte.
- K v7.1.293, its Haskell/LLVM backends, SMT reasoning, and the host runtime
  are trusted.
- `intVals` is a proof-input representation defined by exhaustive structural
  equations and checked one constructor at a time. It contains no fresh or
  opaque element oracle.
- There are no trusted result-bearing primitives, unproved program helpers,
  float operations, sorting oracles, or external calls in this proof.

## Empirically supported facts

- Six K/LLVM assertions cover the three prompt examples plus negative-only,
  positive-only, and mixed-sign lists.
- `differential_test.py` uses an independent `max`/`min`-based oracle and
  exhaustively checks all 19,608 lists of lengths 0 through 5 over
  `{-3, -2, -1, 0, 1, 2, 3}` with zero mismatches.
- These finite tests support implementation/intent and concrete-semantics
  alignment; universal correctness comes from the K claims, not from testing.

## Excluded behavior

- Inputs containing non-integers or booleans are outside the formal input
  domain.
- Resource exhaustion and implementation bugs in K, the SMT solver, CPython,
  or the supplied semantics are outside the theorem.
- The formal result is a reachability/partial-correctness theorem. Although
  finite-list iteration consumes one constructor per step and all tested calls
  terminate, a separate liveness theorem is not claimed.
