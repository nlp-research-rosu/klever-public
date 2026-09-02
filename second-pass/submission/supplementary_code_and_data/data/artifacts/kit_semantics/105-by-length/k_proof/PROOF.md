VALIDATED

## What is proven

Under the supplied `MPY` semantics, `by_length` is partially correct for every
finite `ValSeq` whose elements are K `Int` values. Starting in the ordinary
module environment with the exact translated `collect_digit` and `by_length`
bodies, an empty heap, empty call stack, `NoExc`, and exit code `0`, the call

```k
Call(Name("by_length"), (list(VS), .Exprs))
```

returns a fresh reference to `list(byLengthVS(VS))`, restores the module
environment and empty call stack, leaves `NoExc`, and preserves exit code `0`.
Intermediate heap objects and the final allocation counter are intentionally
existential because they are not source-observable through the returned value.

`byLengthVS` concatenates nine groups. Group `d`, for `d = 9, ..., 1`, contains
one corresponding English name for every occurrence of `d` in the input.
Therefore out-of-range integers are absent, duplicates are preserved, and the
result is in descending numeric order before the digit-to-name conversion.

This is a partial-correctness result in the Kit sense. No separate liveness
theorem is claimed.

## Formal claims

`spec.k` contains:

- `SPEC.collect-loop`: for an all-integer remaining sequence `VS`, the exact
  `collect_digit` loop transforms accumulator `ACC` into
  `collectAcc(VS, D, N, ACC)`. The local loop variable may change to an
  existential final value, matching Python `for` behavior.
- `SPEC.by-length`: the whole entry call returns a reference whose heap object
  is exactly `list(byLengthVS(VS))`.

The loop obligations are:

1. Base: `.ValSeq` performs no iteration and `collectAcc` returns `ACC`.
2. Step: an integer head equal to `D` appends `N`; a different head leaves the
   accumulator unchanged. Both cases recur on the strict tail.
3. Entry discharge: the nine helper calls instantiate the loop theorem at
   digits 9 through 1; the fixed list-concatenation semantics constructs
   `byLengthVS(VS)`.

The formal input representation is the semantics' designated bare
`list(ValSeq)` form for read-only claim inputs. The implementation never mutates
or observes the identity of `arr`.

## Proof-extension inventory

### Exact-body macros

- **Extension:** `collectLoopBody`, `collectDigitBody`, `byLengthBody`, and
  `solutionModule`.
- **Class:** Definitional summary (compile-time syntax abbreviation).
- **Semantic role:** They name constructor syntax and are expanded before
  execution; they do not replace a fixed-semantics step.
- **Domain / matched context:** Closed AST-constructor terms only; no runtime
  match context, guard, continuation, control stack, or framed state.
- **Justification scope / containment:** `kast --expand-macros` produces the
  exact same KORE term for `solutionModule` as parsing `solution.mpy`; both
  artifacts are 11,953 bytes and `cmp` exits `0`.
- **State footprint:** None at macro expansion time.
- **Value influence:** The expanded bodies determine all target and helper
  execution.
- **Value justification:** Exact constructor identity with the translator
  output, not an opaque value.
- **Justification / dependents:** Syntactic equality; both positive claims
  depend on these bodies.
- **Control validation:** `spec-body-mutation.k` replaces the target body with
  `return []` for input `[1]`; the claim becomes stuck and exits nonzero.
- **Value validation:** The same mutation returns an empty heap list where the
  postcondition requires `"One"`.

### `allInts`

- **Class:** Definitional summary.
- **Semantic role:** Defines the formal input-domain predicate; it does not
  replace execution.
- **Domain:** Every `ValSeq`. The `.ValSeq` and `vCons` equations are disjoint
  and exhaustive, and recursion descends on the tail.
- **Matched context / containment:** Function terms only; no operational
  context or state.
- **State footprint:** None.
- **Value influence:** Restricts the claims to integer-array inputs and refutes
  non-integer comparison branches.
- **Value justification:** The generated sort predicate `isInt(V)` fixes each
  head's classification.
- **Justification / dependents:** Structural definition; `collect-loop` and
  `by-length`.
- **Control and value validation:** Concrete and differential evidence uses
  only integer arrays, including negative and out-of-range values.

### Guarded integer-comparison simplification

- **Extension:** `applyCmp("==", V:Val, I:Int) => {V}:>Int ==Int I`
  when `isInt(V)`.
- **Class:** Derived lemma.
- **Semantic role:** Refines the existing `MPY-INT` equality equation after
  operand evaluation. It does not skip lookup, operand evaluation, a Python
  statement, control transfer, or state.
- **Domain:** Exactly values satisfying the K `Int` sort predicate. On the
  overlap with the reference equation for `I1:Int`, both right-hand sides are
  `I1 ==Int I`; outside the guard it is inapplicable.
- **Matched context:** An `applyCmp` function term; arbitrary surrounding
  logical context, but no operational cells or continuation are matched.
- **Justification scope / containment:** Sort refinement reduces `V` to the
  same `Int` accepted by the supplied `MPY-INT` rule, so the lemma's complete
  guard is contained in that equation's domain.
- **State footprint:** None.
- **Value influence:** Resolves the loop branch and hence whether a name is
  appended.
- **Value justification:** The supplied rule
  `applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2`.
- **Justification / dependents:** Direct case derivation from that fixed rule;
  `collect-loop` and transitively `by-length`.
- **Control validation:** Branching still occurs through `Compare`, `If`, and
  `#branch` under fixed semantics.
- **Value validation:** Equal and unequal symbolic branches both close in the
  universal loop proof; the false-result mutation is rejected.

### `collectAcc`

- **Class:** Definitional summary.
- **Semantic role:** Names the mathematical accumulator after processing a
  sequence; it does not rewrite a program term.
- **Domain:** Every `ValSeq`, `Int`, `Val`, and accumulator `ValSeq`. Base and
  constructor equations are disjoint and exhaustive; recursion strictly
  descends on the sequence. The explicit off-domain totalization ignores a
  non-`Int` head. Claims require `allInts`, so that case cannot affect the
  theorem.
- **Matched context / containment:** Function term only; no operational
  context.
- **State footprint:** None directly. Its value specifies the helper result
  heap object.
- **Value influence:** Determines every helper result and the final
  postcondition.
- **Value justification:** On integer heads, its nested condition exactly
  matches the fixed integer equality and fixed list `append` update.
- **Justification / dependents:** Structural recursion; `collect-loop`,
  `byLengthVS`, and `by-length`.
- **Control validation:** `SPEC.collect-loop` is the universal
  fixed-semantics connection theorem.
- **Value validation:** LLVM examples cover empty, equal, unequal, duplicate,
  negative, and out-of-range cases; the independent differential run reports
  zero mismatches.

### `byLengthVS`

- **Class:** Definitional summary.
- **Semantic role:** Names the target mathematical list; it does not replace
  program execution.
- **Domain:** Every `ValSeq`; one unguarded exhaustive equation.
- **Matched context / containment:** Function term only; no operational
  context.
- **State footprint:** None directly. It constrains the returned heap object.
- **Value influence:** It is the whole-entry postcondition.
- **Value justification:** Nine `collectAcc` groups at digits 9 through 1 with
  the exact ASCII names, combined by the supplied `valSeqConcat`.
- **Justification / dependents:** Definition plus the elementary grouping
  argument above; `SPEC.by-length`.
- **Control validation:** All nine program helper calls and eight program list
  concatenations execute under fixed semantics.
- **Value validation:** The off-by-extra-element mutation is rejected, and
  4,801 independent oracle comparisons have zero mismatches.

### `SPEC.collect-loop`

- **Class:** Derived lemma (machine-checked auxiliary execution theorem and
  loop circularity).
- **Semantic role:** Universally characterizes exact fixed-semantics loop
  execution. Once proved, it summarizes that execution for the entry claim.
- **Domain:** `allInts(VS)`; arbitrary digit `D`, name `N`, accumulator `ACC`,
  environment location `L`, input snapshot `WHOLE`, heap location `H`, and
  framed external configuration.
- **Matched context:** Exact
  `#loop(list(VS), Name("value"), collectLoopBody)` with arbitrary trailing
  continuation; an exact plain five-key helper scope with `parent(0)`; heap
  entry `H |-> list(ACC)`; and framed unrelated scopes, heap entries, and
  configuration cells.
- **Justification scope:** The claim itself is proved bridge-free using only
  `MPY`, the truthful definitions above, and the derived integer sort
  refinement.
- **Context containment:** The actual helper call creates exactly that plain
  scope and loop body. The claim preserves the arbitrary trailing
  continuation and all framed cells, while existentially allowing only the
  loop variable's final value.
- **State footprint:** Reads `digit`, `name`, `result`, `value`, and heap object
  `H`; writes `value` and the list at `H`; preserves `arr`, `digit`, `name`,
  scope parent, unrelated scopes and heap objects, stack, return state,
  exception state, and exit code.
- **Value influence:** Fixes the helper list used by all nine calls.
- **Value justification:** `collectAcc` equations and fixed `append` semantics.
- **Justification / dependents:** Focused `kprove` returns `#Top`;
  `SPEC.by-length` depends on it.
- **Control validation:** No abrupt control is introduced. Fixed `#iterNext`,
  target binding, `If`, method call, `#loopLbl`, and loop exit execute before
  circularity closes the tail.
- **Value validation:** Equal and unequal cases are both symbolic proof
  branches; result and body mutations are independently rejected.

There are no proof-local operational rewrite bridges and no proof-local trusted
primitives.

## Exact commands and actual outputs

The complete reproducible command record is `prove.sh`. Its final run exited
`0`. The principal commands were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
head -n 21 concrete_tests.py | cmp solution.py -

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output-file concrete-krun.out

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kast solution.mpy \
  --definition verification-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file solution-parsed.kore
kast --expression solutionModule \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file claimed-solution.kore
cmp solution-parsed.kore claimed-solution.kore

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.collect-loop
# Output: #Top
# Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# Output: #Top
# Exit: 0

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# Output includes: Warning (WarnStuckClaimState)
# Exit: 1 (expected)

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# Output includes: Warning (WarnStuckClaimState)
# Exit: 1 (expected)

python3 differential_tests.py
# Output: checked=4801 mismatches=0
# Exit: 0
```

The LLVM final configuration contains:

```text
<k> .K </k>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The compiler warnings in the logs are unused-variable and pre-existing
non-exhaustive-match warnings from the supplied reference semantics. Neither
positive proof emitted a stuck-claim warning.

Full outputs are in `proof-logs/`, with the LLVM final configuration in
`concrete-krun.out`.

## Gate results

### Gate A — PASS

- **A1:** The entry claim binds the exact translated function bodies.
  Macro-expanded KORE equals parsed `solution.mpy`. Program-defined functions,
  loop bodies, calls, and list operations execute under fixed semantics. The
  empty-body target mutation invalidates the claim.
- **A2:** There are no operational bridges. The auxiliary loop theorem records
  its complete read/write footprint, including the changed loop variable and
  accumulator heap object.
- **A3:** The entry and loop claims pin the real module and helper bindings,
  exact plain helper frame, argument order, continuation, call stack, return
  state, exception state, and exit code. No rule discards or invents control.
- **A4:** `allInts`, `collectAcc`, and `byLengthVS` have exhaustive,
  non-overlapping equations and structurally descending recursion. The single
  simplification lemma has the exact `isInt` guard and agrees with the
  reference equation on its complete domain.
- **A5:** Realizable witnesses include `[]` and `[1]`. The added-`"Wrong"`
  postcondition fails with `WarnStuckClaimState`; the ground body mutation also
  fails.

### Gate B — PASS

- **B1:** The formal domain is exactly finite arrays of mathematical integers.
  Negative, zero, and out-of-range integers are included. Non-integer Python
  values are excluded consistently with the prompt's “array of integers.”
- **B2:** K `Int` is unbounded like Python integers for the used operations.
  Lists, function calls, loops, equality, append, concatenation, ASCII string
  literals, return, and exceptions used here are modeled by the supplied
  semantics. Bare `list(VS)` is the semantics' documented read-only input form.
- **B3:** `byLengthVS` groups all 9s, then 8s, through 1s, preserving
  multiplicity. This is mathematically the same result as filtering to
  `[1,9]`, sorting ascending, reversing, and mapping each digit to its name.
  The correspondence is also independently tested.
- **B4:** The implementation agrees with all prompt examples and the universal
  formal summary.

### Gate C — PASS

- The trust ledger below names every unproved boundary.
- Every concrete, identity, mutation, and differential statement above has an
  existing artifact, exact command, actual result, and log.
- Formal facts, mathematical interpretation, finite evidence, and exclusions
  are separated.

## Trust boundary

- K v7.1.293, its Haskell/LLVM backends, SMT reasoning, and the supplied
  reference semantics are trusted. All positive claims depend on them.
- `py2mpy.py` is the supplied translator and is trusted to represent the
  accepted Python AST faithfully. The generated `solution.mpy` is regenerated
  in `prove.sh`, and its parsed KORE is checked exactly against the bodies used
  by the proof; this checks identity, not the translator's general correctness.
- The elementary statement that digit groups ordered 9 through 1 equal a
  descending sort/filter/map is a mathematical intent bridge, not a separate K
  theorem. Its structural derivation is given above and it has independent
  finite differential evidence.
- No opaque `sortVS`, keyed sort, external oracle, or program-derived opaque
  value is used by the positive K proof.

## Empirically supported facts

- `concrete_tests.py` has an exact 21-line implementation prefix equal to
  `solution.py`. LLVM executes four assertions: the two main prompt examples,
  the empty input, and a duplicate/boundary case. The final state is `.K`,
  `NoExc`, exit code `0`.
- `differential_tests.py` uses Python's `sorted(..., reverse=True)` and an
  independent name dictionary as its oracle. It checks all arrays of lengths
  0 through 4 over `(-2, 0, 1, 2, 8, 9, 10)` (2,801 cases), plus 2,000
  deterministic random arrays of lengths 0 through 30 over `[-100,100]`.
  Result: `checked=4801 mismatches=0`.
- These finite tests support the intent bridge and concrete execution; they do
  not replace the universal K reachability proof.

## Excluded behavior

- Inputs that are not finite lists of K integers, including booleans, floats,
  strings, and nested lists.
- Behavior of unsupported Python constructs or CPython features outside the
  supplied semantics.
- A separate total-correctness/liveness theorem.
- Exact identities or counts of unreachable intermediate heap allocations;
  only the returned reference's list, restored call state, exception state, and
  exit code are specified.
