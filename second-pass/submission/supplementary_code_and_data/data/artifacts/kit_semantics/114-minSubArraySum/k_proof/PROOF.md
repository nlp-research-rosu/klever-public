VALIDATED

## What is proven

Under the supplied `MPY` semantics, invoking the exact closure translated from
`solution.py` on any non-empty finite list of K `Int` values returns the minimum
sum of a non-empty contiguous subarray. This is a partial-correctness result:
the reachability theorem states the returned value if the invocation
terminates.

The implementation is Kadane's recurrence:

- `current` is the minimum sum of a non-empty subarray ending at the most
  recently processed element.
- `minimum` is the minimum sum of any non-empty subarray in the processed
  prefix.
- For the next element `x`, the new ending sum is
  `min(x, current + x)`, and the new overall minimum is the minimum of the old
  overall minimum and that new ending sum.

For the first element `H`, initialization plus the first loop update gives
`current = H` and `minimum = H`. Induction on the remaining list therefore
establishes the prompt's minimum-contiguous-subarray property.

## Formal claim and scope

The positive proof command proves every claim in `spec.k`.

The target claim quantifies over:

```k
H:Int
XS:ValSeq
requires allInts(XS)
```

Its input is the non-empty list `list(vCons(H, XS))`. The exact program closure
is bound to `"minSubArraySum"` in the module scope. The return value is:

```k
kadaneMinimum(vCons(H, XS), 0, H)
```

The loop claim summarizes the supplied semantics' real `#loop` execution. For
an arbitrary integer suffix `VS`, starting `current = C`, and starting
`minimum = B`, it establishes:

```k
current = kadaneCurrent(VS, C)
minimum = kadaneMinimum(VS, C, B)
```

The claim executes the source loop body, name lookup, argument evaluation,
builtin calls, assignments, iterator steps, and loop control. It frames an
arbitrary continuation and stack, preserves the input and module state, and
abstracts only the final local loop-target value, which is neither read after
the loop nor observable after the function frame is popped.

Program boundary: the theorem starts at invocation with the exact closure
already bound. Concrete `krun` evidence separately exercises module loading.
The observable final state is the returned `Int`; heap, exception, return,
stack, environment, allocation counter, and exit-code cells are constrained by
the configurations in `spec.k`.

## Proof-extension inventory

### `allInts`

- **Class:** Definitional summary.
- **Semantic role:** Defines the formal input-domain predicate; it does not
  replace execution.
- **Domain:** Every `ValSeq`.
- **Matched context / justification scope:** Pure terms
  `allInts(.ValSeq)` and `allInts(vCons(V, XS))`; no continuation, bindings, or
  cells are matched.
- **Context containment:** The definition is context-free and is used only as
  a claim precondition.
- **State footprint:** None.
- **Value influence:** Restricts list elements to `Int`, enabling the exact
  integer operator cases.
- **Value justification:** Exhaustive structural equations: empty is true;
  a cons is integer-valued exactly when `isInt(head)` and the tail is
  integer-valued.
- **Dependents:** Both claims and the guarded summary equations.
- **Control/value validation:** Constructor cases are disjoint, exhaustive,
  and structurally decreasing. Concrete and differential tests cover empty
  tails and many non-empty integer tails.

### Guarded `applyBin("+", I, V)` simplification

- **Class:** Derived lemma.
- **Semantic role:** A sort-specialization of the supplied pure integer
  dispatch equation; it does not rewrite `<k>`, skip operand evaluation, or
  change state/control.
- **Domain:** `I:Int`, `V:Val`, guarded by `isInt(V)`.
- **Matched context / justification scope:** The pure value term
  `applyBin("+", I, V)` after the supplied semantics has completed operand
  evaluation. It is independent of continuation and cells.
- **Context containment:** `isInt(V)` is precisely the supplied semantics'
  guard for safely using `{V}:>Int`; the reference semantics uses this same
  guard/cast discipline in integer folds.
- **State footprint:** None.
- **Value influence:** Computes the symbolic `current + value` integer.
- **Value justification:** The supplied `MPY-INT` equation is
  `applyBin("+", I1:Int, I2:Int) => I1 +Int I2`. On the overlap, the cast is
  the same `Int`, so both right-hand sides agree.
- **Dependents:** `SPEC.loop-invariant`, and through it `SPEC.target`.
- **Control/value validation:** No binding or control is affected. Ground LLVM
  smoke tests and the body-sensitivity probe exercise the fixed concrete
  equation; the positive proof exercises the guarded symbolic form.

### Guarded two-argument `applyBuiltin("min", V, I, .Vals)` simplification

- **Class:** Derived lemma.
- **Semantic role:** A sort-specialization and folding lemma for the supplied
  pure builtin result; call lookup, callee selection, argument order, and call
  routing still execute under fixed semantics.
- **Domain:** `V:Val`, `I:Int`, guarded by `isInt(V)`.
- **Matched context / justification scope:** The pure `applyBuiltin` value term
  after the supplied call machinery has selected `builtinV("min")` and
  evaluated both arguments.
- **Context containment:** The loop invariant requires `"min"` absent from the
  module frame, so lookup selects the supplied builtin. The guard restricts
  `V` to the reference equation's `Int` domain.
- **State footprint:** None.
- **Value influence:** Computes both result-bearing minima.
- **Value justification:** In the supplied rules,
  `applyBuiltin("min", M:Int, REST)` reduces to `minVals(M, REST)`;
  for the one-element rest `(I, .Vals)`, this reduces exactly to
  `minInt(M, I)`. The guarded cast gives that same `M`.
- **Dependents:** `SPEC.loop-invariant`, and through it `SPEC.target`.
- **Control/value validation:** The exact builtin binding is pinned and all
  call/evaluation machinery remains active. LLVM tests and 137,256
  differential cases agree with an independent oracle.

### `kadaneCurrent` and `kadaneMinimum`

- **Class:** Definitional summaries.
- **Semantic role:** Name the mathematical state transformer computed by the
  loop; they never replace a program term.
- **Domain:** Empty suffixes and cons suffixes whose head satisfies `isInt`;
  every use is under `allInts`.
- **Matched context / justification scope:** Pure mathematical terms only.
- **Context containment:** Base and recursive equations cover every suffix
  admitted by the claims. Recursive calls consume one `vCons`.
- **State footprint:** None.
- **Value influence:** They define the result-bearing `current` and `minimum`
  post-state values.
- **Value justification:** The equations exactly reproduce the two source
  assignments using `minInt`.
- **Dependents:** Loop post-state and target return postcondition.
- **Control/value validation:** Equations have disjoint empty/cons cases,
  terminate structurally, and have no conflicting overlap. The machine-checked
  loop claim connects fixed execution to these exact values.

### `SPEC.loop-invariant`

- **Class:** Derived reachability lemma/circularity.
- **Semantic role:** Executes and summarizes the real source loop; it is not an
  ordinary rewrite in `verification.k`.
- **Domain:** `allInts(VS)`, with module binding guard
  `"min" not in_keys(MODULE)`.
- **Matched context:** Exact `#loop(list(VS), Name("value"), BODY)` at the head
  of an arbitrary continuation; environment `1`; supplied builtin scope;
  arbitrary module map satisfying the binding guard; exact four-key local
  frame; empty heap; `scopeLoc = 2`, `heapLoc = 0`; arbitrary stack; `noRet`,
  `NoExc`, and exit code `0`.
- **Justification scope / context containment:** The claim itself is proved by
  fixed-semantics symbolic execution. The target invocation reaches this exact
  configuration after its first iterator binding; its module contains only the
  program closure and therefore cannot shadow `"min"`.
- **State footprint:** Reads module/local scopes and builtin scope; writes
  local `"current"`, `"minimum"`, and `"value"`; preserves input, heap,
  allocation counters, stack, return state, exception state, and exit code.
- **Value influence:** Its two summary values determine the target return.
- **Value justification:** `kadaneCurrent`/`kadaneMinimum` equations plus the
  machine-checked fixed-execution connection.
- **Dependents:** `SPEC.target`.
- **Control/value validation:** The complete positive proof is `#Top`. The
  body mutation changes the result from `-5` to `-3` and is rejected.

There are no opaque symbols, trusted problem primitives, priority rules,
source-level operational bridges, abrupt-control shortcuts, or rules that
discard a continuation.

## Exact commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh
```

It ran the following exact stages and exited `0`:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled
python3 differential_test.py

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual positive results:

- LLVM `kompile`: exit `0` (with warnings originating in the supplied
  reference semantics).
- `krun`: exit `0`, final `<k> .K </k>`, `<exc> NoExc </exc>`, and
  `<exit-code> 0 </exit-code>`.
- Differential test: `checked=137256 mismatches=0`, exit `0`.
- Haskell `kompile`: exit `0` (with unused-variable warnings in the supplied
  semantics).
- Positive `kprove`: output `#Top`, exit `0`.

The A5 non-vacuity command was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1`, `WarnStuckClaimState`, with final `<k> 5 ~> .K </k>`
against the deliberately false expected result `6`. `prove.sh` printed:

```text
EXPECTED FAILURE: false-result mutation was rejected
```

The A1 body-sensitivity command was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1`, `WarnStuckClaimState`, with final
`<k> -3 ~> .K </k>` against expected `-5`. The mutation replaced the
restart-capable update with accumulation on input `[2, -5, 3]`. `prove.sh`
printed:

```text
EXPECTED FAILURE: body mutation was rejected
```

## Gate results

### Gate A — PASS

- **A1 program identity/body sensitivity:** The target pins the exact
  translated closure body. `solution.py`, `solution.mpy`, `smoke.py`, and the
  closure in `spec.k` agree. The material body mutation is rejected.
- **A2 operational state preservation:** No source execution is bridged. The
  loop claim executes the supplied rules and constrains or frames every active
  cell. The only abstracted local value is dead after the loop.
- **A3 binding/evaluation/control fidelity:** The module guard excludes a
  shadowing `"min"` binding; the builtin scope is exact. Lookup, left-to-right
  call argument evaluation, assignments, iteration, return, and frame popping
  execute normally.
- **A4 consistency/rule validity:** `allInts` is total. Summary functions cover
  every admitted use and recurse on a strict tail. Both simplification lemmas
  agree with supplied equations throughout their guards and on overlaps. No
  opaque value or contradictory equation exists.
- **A5 result constraint/non-vacuity:** `[5]` is a realizable witness. The false
  result `6` is rejected with actual result `5`. Distinct-result witnesses in
  the smoke suite include `[5] -> 5`, `[-1,-2,-3] -> -6`, and a mixed-sign
  case.

### Gate B — PASS

- **B1 input domain:** The formal domain is exactly non-empty finite lists of
  mathematical integers, matching the prompt's non-empty array of integers.
- **B2 language model:** K `Int` and Python integers are unbounded; list order,
  integer addition, integer comparison inside `minInt`, and non-mutating
  iteration are material and modeled. Empty input is intentionally excluded.
- **B3 summary/property:** The Kadane recurrence has the ending-subarray and
  processed-prefix induction stated above. The K proof formally connects the
  real program to the recurrence; the recurrence-to-prompt interpretation is
  mathematically derived and independently tested against exhaustive
  enumeration for the recorded finite domain.
- **B4 implementation alignment:** Prompt examples and independent tests agree;
  no implementation/specification discrepancy was found.

### Gate C — PASS

- All referenced artifacts exist in the workspace.
- `prove.sh` records the exact build, concrete, positive-proof, and negative
  probe commands and checks their expected exit behavior.
- `smoke.py`/`smoke.mpy` exercise prompt examples and boundary/mixed-sign
  cases under the supplied LLVM semantics.
- `differential_test.py` uses a separately implemented nested-loop
  brute-force oracle over every list of lengths `1..6` with values `-3..3`;
  the recorded run checked 137,256 inputs with zero mismatches.
- Finite evidence is reported only as evidence; the universal result comes
  from `kprove`.

## Trust boundary

- The supplied, unmodified `reference-semantics/` definition, including K
  builtin sort predicates/casts, `minInt`, integer hooks, and the Python subset
  modeled there.
- The K v7.1.293 compiler, LLVM/Haskell backends, solver, and reachability
  prover.
- The fixed, unmodified `py2mpy.py` transliterator and CPython AST parsing.
- Manual syntactic alignment between the generated `solution.mpy` body and the
  closure term in `spec.k`, supported by the concrete translated smoke module
  and body mutation probe.
- The mathematical induction relating the Kadane recurrence to the phrase
  “minimum sum of any non-empty sub-array”; this intent bridge is independently
  supported by the brute-force differential test but is not a separate
  machine-checked combinatorial theorem.

No task-specific external primitive or opaque result is trusted.

## Empirically supported facts

- All five K smoke assertions terminate without exception.
- Both prompt examples produce the specified values.
- Singleton, zero-only, all-negative, and mixed-sign examples agree.
- The independent brute-force differential sample has zero mismatches over
  137,256 arrays.
- A material body mutation changes an observable result and is rejected.
- A false postcondition on a satisfiable input is rejected.

## Excluded behavior

- Empty lists, non-integer elements, mutation/aliasing of the input, and Python
  constructs outside the supplied semantics.
- Total-correctness/liveness as a formal claim; K reachability here proves
  partial correctness. Operationally, the supplied finite-list iterator
  consumes one constructor per iteration.
- Correctness of the supplied semantics, translator, K implementation, and
  solver themselves.

The runner marker is therefore `KPROVE_PASSED`: every required positive target
proof command in `prove.sh` printed `#Top` and exited `0`. This marker is
separate from the `VALIDATED` proof-quality headline above.
