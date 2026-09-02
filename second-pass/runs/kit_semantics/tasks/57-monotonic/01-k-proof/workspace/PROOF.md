VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact translated body of
`monotonic` is symbolically executed after normal module loading, name lookup,
argument evaluation, function-frame creation, parameter binding, return, frame
pop, and assignment to `result`.

The proved partial-correctness result is, for every symbolic `VS:ValSeq`:

```text
result ==
  (VS ==K sortVS(VS))
  orBool
  (VS ==K revVS(sortVS(VS)))
```

The final claim also requires `.K`, the module environment, an empty call
stack, `noRet`, `NoExc`, and exit code `0`. The heap and heap counter are
existential because the temporary lists allocated by `sorted` are not
observable in the HumanEval contract. As required for a reachability proof,
this is a partial-correctness statement and does not separately claim
termination.

Given the supplied trust contract that `sortVS` is ascending sort, the first
disjunct says the input is nondecreasing and the second says it is
nonincreasing. Equality is intentionally allowed, matching the usual
non-strict meaning and the duplicate-value tests.

## Formal claim and validation scope

- Program boundary: the `Module` contains the exact `FuncDef` emitted in
  `solution.mpy`, followed by a synthetic call that stores the returned value
  in `result`.
- Formal input domain: every finite `ValSeq`, with no `requires` clause.
- Intended adequacy domain: lists of mutually comparable values; the supplied
  symbolic sort contract is specifically documented for integer lists, while
  its concrete implementation also covers homogeneous strings.
- Observable final state: returned Boolean plus normal control completion
  (`.K`, empty stack, `noRet`, `NoExc`, exit code `0`). Temporary sort
  allocations are deliberately unobserved.
- Intended property: true exactly when the list is nondecreasing or
  nonincreasing.
- Positive target claim: `SPEC.monotonic` in `spec.k`.

## Proof-extension inventory

### Supplied `sortVS` boundary and `sorted` dispatch

- Extension: imported `sortVS(ValSeq)` and the `sorted` dispatch rules in
  `reference-semantics/semantics/sort.k`.
- Class: trusted primitive supplied as part of the fixed semantics, not a
  proof-local extension.
- Semantic role: represents Python's external sorting operation. The program
  still executes lookup, call dispatch, argument evaluation, allocation,
  comparison, short-circuit control, and return under fixed semantics.
- Domain: the formal equation is interpretation-parametric over every
  `ValSeq`; its monotonicity interpretation is conditional on the documented
  ascending-sort contract for homogeneous comparable values.
- Matched context: the fixed rules match
  `#applyK(toCall(builtinV("sorted")), (list(VS), .Vals))` or the exact
  `kwV("reverse", RB)` variant in `<k>`, with the continuation framed by the
  semantics. Lookup and argument evaluation have already selected that builtin
  and produced those values.
- Justification scope: the explicit trusted contract in the supplied
  `sort.k`. Symbolic `sortVS` is intentionally opaque; LLVM uses its concrete
  insertion-sort equations.
- Context containment: the dispatch rules are owned by the fixed semantics and
  match only the selected builtin with the listed evaluated arguments. No
  proof-local rule broadens their continuation, binding, or state domain.
- State footprint: dispatch changes `<k>` to `#alloc`; fixed `#alloc` reads and
  writes `<heap>` and `<heapLoc>`. Scopes, stack, return state, exception state,
  and exit code are preserved.
- Value influence: the sorted value controls list equality, short-circuiting,
  the returned Boolean, and whether a second temporary list is allocated.
- Value justification: conditional on the named ascending-sort contract,
  supported by the LLVM and CPython differential evidence below.
- Justification: explicit task-supplied trusted primitive.
- Dependents: `SPEC.monotonic`.
- Control validation: the LLVM example suite and the 781-case generated
  K-side differential corpus both complete with `NoExc`/exit `0`.
- Value validation: the K corpus covers both Boolean outcomes; the independent
  CPython adjacent-pair oracle reports zero mismatches over 137,257 inputs.
- Validation: accepted as an explicit external trust boundary, not presented
  as a K proof of sorting correctness.

### Guarded true-branch Boolean lemma

- Extension:
  `rule A:Bool ==Bool (A orBool B:Bool) => true requires A [simplification]`.
- Class: derived lemma.
- Semantic role: normalizes the final proof obligation; it does not replace
  program execution.
- Domain: all Booleans `A` and `B` with `A = true`.
- Matched context: exactly the displayed Boolean equality term; no K cell,
  continuation, binding, or framed state is matched.
- Justification scope and context containment: when `A` is true,
  `A orBool B` is true, so the equality is true for both values of `B`.
  The guard is exactly that derivation's domain.
- State footprint: none.
- Value influence: only discharge of the postcondition equality; it does not
  create or change the program result.
- Value justification: exhaustive two-row Boolean truth table under `A`.
- Justification: Boolean algebra.
- Dependents: `SPEC.monotonic`.
- Control validation: not applicable; this is not an operational bridge.
- Value validation: the false-result mutation is rejected, showing the lemma
  does not make the result unconstrained.
- Validation: guards are truthful; overlap with the second lemma is possible
  only when both operands coincide, where the complementary guards are
  disjoint and both conclusions are `true`.

### Guarded false-branch Boolean lemma

- Extension:
  `rule B:Bool ==Bool (A:Bool orBool B) => true requires notBool A
  [simplification]`.
- Class: derived lemma.
- Semantic role: normalizes the final proof obligation; it does not replace
  program execution.
- Domain: all Booleans `A` and `B` with `A = false`.
- Matched context: exactly the displayed Boolean equality term; no K cell,
  continuation, binding, or framed state is matched.
- Justification scope and context containment: when `A` is false,
  `A orBool B` equals `B`, so the equality is true for both values of `B`.
  The guard is exactly that derivation's domain.
- State footprint: none.
- Value influence: only discharge of the postcondition equality.
- Value justification: exhaustive two-row Boolean truth table under
  `notBool A`.
- Justification: Boolean algebra.
- Dependents: `SPEC.monotonic`.
- Control validation: not applicable.
- Value validation: both negative probes remain stuck as intended.
- Validation: the guard complements the first lemma's guard; no inconsistent
  overlap exists.

There are no proof-local operational bridges, opaque result oracles, priority
rules, auxiliary claims, or program-execution rewrites.

## Exact commands and actual results

Translation:

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Actual result: exit `0`; `solution.mpy` contains the expected single
`FuncDef`.

Concrete compilation and prompt/boundary examples:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
krun concrete_tests.mpy --definition runtime-kompiled
```

Actual result: all commands exited `0`. `kompile` emitted only warnings from
the supplied semantics. `krun` ended with:

```text
<k> .K </k>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

K-side generated differential evidence:

```bash
for corpus_shard in 0 1 2 3 4
do
  python3 generate_k_differential.py \
    --shard-count 5 \
    --shard-index "$corpus_shard" \
    > "k_differential_tests_${corpus_shard}.py"
  python3 py2mpy.py \
    "k_differential_tests_${corpus_shard}.py" \
    > "k_differential_tests_${corpus_shard}.mpy"
done
for corpus_shard in 0 1 2 3 4
do
  krun "k_differential_tests_${corpus_shard}.mpy" \
    --definition runtime-kompiled \
    --output none
done
```

Actual result: all 781 exhaustive lists of lengths 0 through 4 over `[-2,2]`
were divided into disjoint shards containing 157, 156, 156, 156, and 156
cases. Every `krun` command exited `0`, with no output by request and therefore
no failed assertion. A monolithic 781-case parse was attempted first and
failed before execution with `OutOfMemoryError: Java heap space`; K's parser
JVM remained capped at an 8 GiB Java heap. Sharding changed only packaging,
not the input scope or oracle, and all five shards then passed.

Independent CPython differential evidence:

```bash
python3 differential_test.py
```

Actual output and status:

```text
checked=137257 mismatches=0
```

Exit `0`. The oracle checks adjacent pairs and does not call `sorted` or reuse
the proof equation.

Symbolic definition and positive proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual proof output and status:

```text
#Top
```

Both commands exited `0`; compiler warnings were limited to unused variables
in the supplied semantics/spec and did not affect the result.

False-result mutation:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1` with `WarnStuckClaimState`. The residual terminal
configuration contains `"result" |-> true` while the mutation requires
`false`.

Body-sensitivity mutation:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1` with `WarnStuckClaimState`. Replacing the body by
`Return(Bool(false))` produces `"result" |-> false`, contradicting the
required `true`.

`prove.sh` records and checks all successful commands and treats both mutation
failures as expected.

## Gate results

### Gate A — PASS

- A1: the exact translated function body executes under fixed semantics.
  Changing it to `return False` invalidates the positive witness.
- A2: there is no proof-local operational bridge. Fixed allocation effects are
  executed; only unobservable temporary heap contents are existentially
  framed in the claim.
- A3: module definition, function-name lookup, builtin `sorted` lookup,
  left-to-right argument evaluation, frame binding, short-circuit control,
  return, and frame pop all execute. The only opaque value is the explicitly
  supplied external `sortVS` primitive, and the formal conclusion remains
  conditional on that named value.
- A4: the two proof-local equations are guarded Boolean identities. Their
  domains cover the two short-circuit branches and have no inconsistent
  overlap.
- A5: the initial empty module state with input `[1,2,4,20]` is realizable.
  The false-result mutation exits `1` and exposes the correct result in its
  residual.

### Gate B — PASS

- B1: the formal equation covers every `ValSeq`; its human-facing monotonic
  interpretation is restricted to mutually comparable elements under the
  supplied sort contract. The prompt examples are integer lists.
- B2: K `Int` is arbitrary precision like Python integers for these
  operations. Mixed incomparable Python values and their `TypeError` behavior
  are outside the supplied sort model and are excluded.
- B3: the K proof formally establishes the sort-equality equation. Its
  interpretation as monotonicity is conditional on `sortVS` being ascending
  sort and is independently supported by differential evidence.
- B4: the implementation matches the prompt examples and the adjacent-pair
  contract, including empty/singleton lists and equal adjacent values.

### Gate C — PASS

- C1: the trust ledger below names the opaque symbol and all material effects;
  no proof-local operational bridge or unrecorded oracle exists.
- C2: every claimed test has an existing artifact, exact command, input scope,
  oracle, output, and status above. Finite tests are reported only as evidence,
  not as universal proofs.
- C3: the formal equation, conditional monotonicity interpretation, finite
  evidence, and exclusions are stated separately.

## Trust boundary

- The supplied `reference-semantics/` and K/Haskell/SMT toolchain are the fixed
  theorem base required by the task.
- `sortVS` is the exact intentional opaque value boundary. It affects the
  branch, returned Boolean, and number/content of temporary allocations.
  `SPEC.monotonic` depends on it. Its ascending-sort meaning is conditional on
  the contract in `reference-semantics/semantics/sort.k`; the LLVM corpus and
  independent CPython differential test provide finite supporting evidence.
- The mathematical bridge “equal to ascending sort or its reversal iff
  nondecreasing or nonincreasing” is used only for intent interpretation. It
  assumes a finite sequence over a total order and is not claimed as a
  separate K theorem.

## Empirically supported facts

- All seven concrete K assertions covering the prompt examples, empty and
  singleton lists, and duplicate values completed normally.
- All 781 generated K inputs completed with the adjacent-pair oracle's expected
  Boolean.
- All 137,257 CPython inputs of lengths 0 through 6 over `[-3,3]` matched the
  independently implemented adjacent-pair oracle.

These are finite observations and do not replace the symbolic reachability
proof or the named `sortVS` trust contract.

## Excluded behavior

- Inputs whose elements are not mutually orderable under Python.
- CPython exception details for mixed incomparable values.
- Floating-point ordering, NaNs, user-defined comparison side effects, and
  mutation/concurrency during sorting.
- A proof that the supplied `sortVS` implementation is universally correct.
- A separate termination or complexity theorem.
