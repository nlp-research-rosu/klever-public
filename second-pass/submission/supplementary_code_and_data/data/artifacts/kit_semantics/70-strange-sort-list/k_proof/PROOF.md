VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every modeled finite `ValSeq` satisfying
`allInts(VS)`, calling the exact `strange_sort_list` closure from `solution.mpy`
terminates only in the claimed final configuration:

- the returned value is `ref(1)`;
- heap location `0` contains `list(sortVS(VS))`;
- heap location `1` contains
  `list(strangeAcc(.ValSeq, sortVS(VS), 0,
  vsLen(sortVS(VS)) -Int 1))`;
- the caller environment, scope stack, return state, exception state, and exit
  code are restored as stated in `SPEC.entry-point`.

This is a partial-correctness reachability theorem. The human-facing statement
that this sequence alternates the minimum and maximum remaining integers is
conditional on the supplied reference primitive's contract that `sortVS(VS)`
is the ascending permutation of an integer sequence. K does not prove that
sorting contract here; the formal result deliberately retains `sortVS(VS)`.

## Formal claims

`SPEC.loop-invariant` is an exact loop-tail connection theorem. At the real
`#while` loop head, with accumulator `A`, sorted sequence `S`, nonnegative
`left = L`, and `right = R`, it executes the loop, the following midpoint
`if`, the `return`, and `#endcall`. It returns the same result reference with
heap contents `strangeAcc(A, S, L, R)` and restores the exact caller control
state.

`SPEC.entry-point` executes lookup, argument evaluation, the exact translated
function body, allocation, sorting, the loop, midpoint handling, return, and
frame pop. Its precondition is precisely `allInts(VS)`.

The recursive result characterization is:

- `L > R`: return accumulator `A`;
- `L == R`: append the sole middle element `S[L]`;
- `L < R`: append `S[L]`, append `S[R]`, then continue with
  `L + 1` and `R - 1`.

These cases are exactly the minimum/maximum alternation when `S` is an
ascending permutation.

## Proof-extension inventory

### `allInts`

- Class: definitional summary.
- Semantic role: input-domain predicate; it replaces no execution.
- Domain: every finite `ValSeq`.
- Matched context and justification scope: function terms only; no
  configuration, continuation, binding, or framed cells.
- State footprint: none.
- Value influence: enables `SPEC.entry-point`; it does not determine output.
- Value justification: exhaustive structural equations for empty and
  nonempty sequences using the built-in sort predicate `isInt`.
- Dependents: `SPEC.entry-point`.
- Validation: equations are disjoint, cover every `ValSeq`, and recurse on the
  strict tail. The empty sequence is a concrete satisfiable witness.

### `strangeAcc`

- Class: definitional summary.
- Semantic role: names the mathematical sequence accumulated by the loop; it
  does not rewrite or skip a Python term.
- Domain: all `A, S : ValSeq` and all `L, R : Int`.
- Matched context and justification scope: function terms only; no operational
  context or cells.
- State footprint: none.
- Value influence: fixes the returned list contents in both claims.
- Value justification: the three guarded equations mirror the actual append
  order. Their `>Int`, `==Int`, and `<Int` guards are exhaustive and pairwise
  disjoint. The recursive case decreases `R - L` by two.
- Dependents: `SPEC.loop-invariant` and `SPEC.entry-point`.
- Validation: the loop connection theorem proves that fixed execution produces
  this exact value. Concrete K and CPython differential runs give independent
  finite evidence.

### Symbolic Map deletion simplification

- Extension:
  `(M:Map K:Int |-> V:Scope)[K <- undef] => M`
  when `K` is not already a key of `M`.
- Class: derived lemma.
- Semantic role: canonicalizes the Map update emitted after the fixed `#pop`
  rule has executed; it replaces no program step.
- Domain and context: exactly a disjoint Map fragment plus one known-present
  integer key, immediately updated to `undef`.
- State footprint: none beyond equality-normalization of the already-computed
  scope Map.
- Value influence: none on the result; it lets caller scopes compare in a
  canonical form.
- Justification: deleting the displayed binding from a fragment known not to
  contain its key leaves exactly that fragment.
- Dependents: `SPEC.loop-invariant` and its use by `SPEC.entry-point`.
- Validation: the guard prevents overlap or key loss from `M`; removing this
  lemma left the genuine symbolic Map-update residual, while adding it made the
  unchanged fixed execution close.

### `SPEC.loop-invariant` used as a composed theorem

- Class: derived lemma / exact auxiliary execution claim.
- Semantic role: summarizes fixed execution only after being independently
  proved; it is not a proof-local operational rewrite.
- Domain: `L >=Int 0`, exact local bindings, two exact heap objects, exact
  `env = 1`, `scopeLoc = 2`, stack
  `ListItem(frame(.K, 0, 1))`, `noRet`, `NoExc`, and exit code `0`.
- Matched context: the actual `#while` term followed by the exact remaining
  `Stmts` containing the midpoint `If` and `Return`, then `#endcall`. The base
  scope fragment `SC` is framed only where the theorem is universally
  quantified over it. No arbitrary K continuation is accepted.
- Justification scope and context containment: identical to the match domain.
  The claim was first proved bridge-free with fixed `MPY` execution. The
  second proof command marks this already-proved claim trusted only so kprove
  can use it as a circularity while proving the entry claim.
- State footprint: reads all named locals and the two heap objects; updates
  `left`, `right`, and the result heap; preserves the sorted heap and heap
  location; pops the callee scope and stack frame; restores the caller
  environment and scope location; returns `ref(HR)`; preserves `ret`, `exc`,
  and exit code as claimed.
- Value influence: fixes the complete returned sequence.
- Dependents: `SPEC.entry-point`.
- Control and value validation: the first positive command proves the exact
  connection theorem without `--trusted`; the changed-body probe is rejected.

### Supplied `sortVS`

- Class: trusted primitive in the fixed reference semantics, not a proof-local
  extension.
- Semantic role: models Python's external `sorted` builtin symbolically and
  has a concrete insertion-sort implementation in `MPY-KRUN`.
- Domain used here: finite lists of integers (`allInts(VS)`).
- Matched context: the supplied `sorted` call route, argument evaluation, and
  `#alloc` rules; no local rule broadens that context.
- State footprint: allocates a new sorted-list heap object and increments
  `heapLoc` through fixed semantics; the source input value is preserved.
- Value influence: every selected output element ultimately comes from
  `sortVS(VS)`.
- Value justification: named assumption `SORT` — `sortVS(VS)` is an ascending
  permutation of integer sequence `VS`. The K theorem is
  interpretation-parametric in this value and states the intended
  minimum/maximum conclusion only conditionally on `SORT`.
- Dependents: the human-facing interpretation of `SPEC.entry-point`; formal
  execution closure itself needs no ordering axiom.
- Validation: 124 K/LLVM cases were checked against independently generated
  literal oracle results, including empty, duplicates, negative values, and
  all prompt examples. This is finite evidence, not a universal proof of
  `SORT`.

There are no proof-local operational bridges.

## Exact commands and actual results

The complete recorded run was:

```sh
./prove.sh > prove.log 2>&1
```

Actual result: exit `0`.

Translation:

```sh
python3 py2mpy.py solution.py > solution.mpy
```

Actual result: exit `0`; SHA-256 of the generated `solution.mpy` was
`48f23c44f76daad6a3893e5f76052fb5294b0c80fc385617399084cfe46d60d2`.

Concrete build and execution:

```sh
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled
python3 differential_test.py
```

Actual results: all commands exited `0`; `krun` ended with `.K`, `NoExc`, and
exit code `0`. The differential output was exactly:

```text
CPython cases=19531 mismatches=0 input-mutations=0
K/LLVM cases=124 mismatches=0
```

Symbolic build:

```sh
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Actual result: exit `0`. Compiler warnings were confined to the supplied
reference definition.

Bridge-free loop-tail proof:

```sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
```

Actual output and status:

```text
#Top
Exit: 0
```

Composed entry proof:

```sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --trusted SPEC.loop-invariant
```

Actual output and status:

```text
#Top
Exit: 0
```

False-result mutation:

```sh
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1` with `WarnStuckClaimState`. The realizable witness is
the empty integer list. Fixed execution ended with heap location `1` equal to
`list(.ValSeq)`, which did not unify with the deliberately false expected
`list(vCons(0, .ValSeq))`. Full output is in `vacuity.log`.

Changed-body mutation:

```sh
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1` with `WarnStuckClaimState`. On input `[1, 2]`, the
mutated second append produced `[1, 1]`, which did not unify with the original
`[1, 2]` postcondition. Full output is in `body-mutation.log`.

## Gate results

### Gate A — PASS

- A1: the entry claim contains the exact translated closure body and executes
  it under fixed semantics. The loop-tail claim is independently proved before
  composition. The changed-body probe failed as required.
- A2: no operational bridge skips state. The claims expose environment,
  scopes, heap, heap location, stack, return, exception, and exit-code effects.
- A3: module binding, argument evaluation, exact remaining `Stmts`, return,
  and frame pop are all present. The loop theorem accepts no arbitrary K
  suffix.
- A4: all proof-local equations have exhaustive, disjoint cases or a narrow
  valid guard; recursion descends.
- A5: `VS = .ValSeq` satisfies the precondition, and the false `[0]`
  postcondition was rejected with the expected residual.

### Gate B — PASS

- Input domain matches the prompt's finite lists of integers, including empty
  lists, duplicates, and negative integers.
- The postcondition's recursive left/right extraction is the stated strange
  order when `SORT` holds.
- Mathematical K integers match Python's unbounded integer behavior relevant
  here. The supplied model intentionally abstracts exceptions and symbolic
  sorting; valid integer-list executions exercise no exceptional behavior.
- The implementation and prompt examples agree. The conditional sorting
  boundary is explicit rather than silently treated as K-proved.

### Gate C — PASS

- The trust ledger below names every unproved component and dependent
  conclusion.
- `prove.sh`, both mutation specs, both residual logs, the concrete smoke
  artifact, the differential harness, and `prove.log` exist and reproduce the
  stated evidence.
- Formal closure, conditional intent interpretation, and finite empirical
  support are kept separate.

## Trust boundary

- `SORT`: the supplied `sortVS` denotes the ascending permutation of an integer
  sequence. This affects returned values and the minimum/maximum
  interpretation. It is not universally proved in this K development.
- The supplied `MPY` rules, K toolchain, Haskell backend, LLVM backend, and
  integer/collection hooks are trusted as the verification and execution
  infrastructure.
- `py2mpy.py` is trusted as the fixed AST-to-constructor translator. It is
  regenerated in `prove.sh`, and neither it nor the reference semantics was
  modified.
- `--trusted SPEC.loop-invariant` is only a composition mechanism. Its exact
  claim is discharged immediately beforehand by the bridge-free `#Top`
  command; `prove.sh` stops if that independent proof fails.

## Empirically supported facts

- `smoke.py` exercises the three prompt examples plus a negative/duplicate
  example under `MPY-KRUN`.
- `differential_test.py` uses an independent oracle that repeatedly removes
  the current minimum or maximum. It checked 19,531 CPython inputs (all lengths
  0 through 6 over `{-2,-1,0,1,2}`) and observed no result mismatch or input
  mutation.
- The same harness generated literal oracle assertions for 124 K/LLVM cases:
  all lengths 0 through 4 over `{-1,0,1}`, plus the nonredundant prompt and
  negative/duplicate cases. It observed zero mismatches.
- These finite checks support implementation adequacy and `SORT`; they do not
  replace the symbolic program proof or universally prove sorting.

## Excluded behavior

- Total correctness and termination are not established by this
  partial-correctness proof.
- Inputs that are not modeled finite lists of integers are outside the formal
  domain.
- A universal ordering/permutation theorem for `sortVS` is outside this proof.
- Resource exhaustion, implementation limits, and CPython behavior absent from
  the supplied subset semantics are not modeled.
- Caller-visible aliasing or input-mutation properties are not part of the
  formal postcondition, although the CPython differential run observed no
  input mutation.
