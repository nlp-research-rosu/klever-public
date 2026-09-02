VALIDATED

## What is proven

Under the supplied MPY semantics, calling the exact translated
`rolling_max` closure on any finite MPY list containing only mathematical
integers returns a fresh reference whose heap payload is `rollingMax(input)`.
The definition of `rollingMax` starts with the first element and appends the
larger of the current maximum and each next element, so it is the requested
list of prefix maxima. The empty list returns an empty list.

This is a K reachability proof of partial correctness. Termination is not a
separate theorem.

## Formal claim and scope

- Program boundary: a call through the module binding `"rolling_max"` to a
  `closureVal` containing the function body emitted in `solution.mpy`.
- Input domain: all finite `ValSeq` values that are empty, or have an `Int`
  head and a tail satisfying `allInts`. This is exactly the prompt's
  `List[int]` domain and includes the empty list.
- Observable result: the returned `ref(0)`, its exact heap payload, the final
  heap location, and the restored environment, scopes, stack, return,
  exception, and exit-code cells.
- Postcondition:
  - empty input: `0 |-> list(rollingMax(.ValSeq))`;
  - nonempty input `vCons(H,T)` with `allInts(T)`:
    `0 |-> list(rollingMax(vCons(H,T)))`.
- The loop claim additionally tracks the exact final values of `current`,
  `number`, and the result-list heap payload.

The entry claims are `SPEC.rolling-max-empty` and
`SPEC.rolling-max-nonempty`. Together they cover every finite integer list.
`SPEC.rolling-loop` records the loop theorem also established bridge-free by
`LOOP-SPEC.rolling-loop-connection`.

## Proof-extension inventory

| Extension | Class and semantic role | Domain, context, and state footprint | Value justification and dependents | Validation |
|---|---|---|---|---|
| `allInts` | Definitional summary; does not replace execution | All `ValSeq`; empty/cons equations, structurally decreasing; no state | It is true exactly when every element satisfies K's generated `isInt` predicate. Used by loop and nonempty entry preconditions. | Cases are exhaustive and disjoint. Concrete and differential tests include negative and positive integers. |
| `{true #Equals isInt(V)} => #Exists I:Int . {V #Equals I}` | Derived logical lemma; no operational rewrite | Any `V:Val`; no cells or continuation | This is the defining subsort fact for K's generated `isInt` predicate: truth means that `V` is an injected `Int`. It only removes an impossible non-Int proof branch. | The lemma introduces no value and cannot select a program branch independently of `isInt(V)`. |
| `stepMax` | Definitional summary; no execution replacement | All integer pairs. Guards `I > M` and `I <= M` are disjoint and exhaustive. | Returns exactly the value selected by the source `if number > current`. Used by `rollAcc` and `foldMax`. | Both source branches close in the bridge-free loop proof; the `<` body mutation fails. |
| `rollAcc` | Definitional summary of the result heap | All `ValSeq` values; the intended domain is `allInts`. Empty/int-head/`owise` cases are total and recursive descent is on the tail. No operational cells are rewritten by its equations. | Appends `stepMax(M,I)` exactly as the source `append` call does. Used by loop and entry postconditions. | The universal loop connection proves the heap transition; fixed LLVM runs and 3,906 differential cases agree. |
| `rollingMax` | Definitional summary of the requested result | All `ValSeq`; empty/int-head/`owise` cases are total. No state | Empty maps to empty; a nonempty integer list invokes `rollAcc` with its first value as the initial maximum. Used by entry postconditions. | Prompt example, boundary cases, and differential oracle all agree. |
| `foldMax` | Definitional summary of final local `current` | All `ValSeq`; empty/int-head/`owise` cases are total and descend on the tail. No state | Repeated `stepMax`, matching the source assignment. Used by the loop bridge/claim. | Both comparison branches close in `loop-spec.k`. |
| `lastOr` | Definitional summary of final local `number` | All `ValSeq`; empty/int-head/`owise` cases are total and descend on the tail. No state | A `for` target ends as the last iterated integer, or remains unchanged for an empty remainder. | Established as part of the universal loop connection. |
| Specialized `#bindTgt(Name(X), I:Int)` rule | Operational bridge specializing one fixed MPY rule | Complete match domain: arbitrary continuation, environment `L`, surrounding scope map, plain frame `scope(M,P)` with no `"$cells"`. Reads `env/scopes`; writes only `M[X <- I]`; preserves continuation and every omitted cell. | RHS is byte-for-byte the fixed rule's plain-frame map update. It preserves the exact integer value and introduces no abrupt control. Used by the loop connection. | `bind-spec.k`, compiled without this specialization, proves the same universally framed transition and prints `#Top`. |
| Exact `#loop(...)` rule | Operational bridge used by entry claims | Exact translated loop body, `.Stmts ~> Return(...) .Stmts ~> #endcall` continuation, env `1`, exact function frame keys, arbitrary module/builtins values, heap containing only result ref `0`, heapLoc `1`, exact stack frame, `noRet`, `NoExc`, exit `0`, and `allInts(IS)`. | RHS values are fixed by `foldMax`, `lastOr`, and `rollAcc`. It preserves input/module/builtins, scopeLoc, heapLoc, stack, return, exception, and exit cells. It affects the returned heap through the later real `Return`. | `loop-spec.k` imports `VERIFICATION-CORE`, not the loop bridge, and proves the identical complete transition with `#Top`. Replacing `>` by `<` is rejected. |
| Connection and target claims | Derived reachability claims | Exact configurations shown in `bind-spec.k`, `loop-spec.k`, and `spec.k` | Connection claims justify the two operational bridges; target claims bind the exact source closure and constrain the returned heap. | All positive claim sets print `#Top`; negative mutations exit nonzero. |

### Operational context containment

The binding rule and `BIND-SPEC.bind-int-name` have the same term,
continuation frame, map update, parent, guard, and omitted-cell framing.
`bind-base.k` imports `VERIFICATION-SUMMARIES`, so it does not import the
binding specialization.

The loop rule and `LOOP-SPEC.rolling-loop-connection` have the same term,
continuation, guards, bindings, heap, stack, return, exception, and exit
cells. `loop-base.k` imports `VERIFICATION-CORE`, so it includes only the
separately connected binding specialization and does not import the loop
rule. Thus every configuration matched by either bridge is within its
bridge-free justification domain.

## Exact commands and actual results

The complete recorded command is:

```bash
./prove.sh > proof-run.log 2>&1
```

Actual exit: `0`.

`prove.sh` records every underlying command. The significant actual results
in `proof-run.log` are:

```text
cases=3906 mismatches=0
#Top
#Top
#Top
EXPECTED FAILURE: loop-body mutation was rejected
EXPECTED FAILURE: false-result mutation was rejected
```

The three `#Top` lines, each with exit `0`, are respectively:

```bash
kprove bind-spec.k --definition bind-kompiled --spec-module BIND-SPEC
kprove loop-spec.k --definition loop-kompiled --spec-module LOOP-SPEC
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The last command proves every claim in `spec.k` together.

Concrete execution uses the required reference build:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual `krun` exit: `0`; the final configuration has `.K`, `NoExc`, and exit
code `0`. The assertions cover empty, singleton, prompt example, decreasing,
and negative/duplicate inputs.

The false-result probe uses the satisfiable input `[1]` but demands `[2]`:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual exit: `1`. Its residual heap contains `list(vCons(1,.ValSeq))`, not
the demanded `[2]`.

The body-sensitivity probe replaces the source comparison `>` with `<` while
retaining the rolling-maximum postcondition:

```bash
kprove loop-body-mutation.k \
  --definition loop-kompiled \
  --spec-module LOOP-BODY-MUTATION
```

Actual exit: `1`, with a stuck inductive residual.

The reference semantics emits pre-existing unused-variable and LLVM
non-exhaustive-match warnings in unrelated generic operations. No positive
command emits a stuck-claim error, and every positive `kprove` prints
`#Top`.

## Gate results

### Gate A — PASS

- A1 program identity/body sensitivity: both entry claims bind the exact
  translated closure body. Program-defined code executes under fixed
  semantics except for the loop bridge, whose exact body and complete
  transition are proved bridge-free. The `<` mutation is rejected.
- A2 state preservation: the binding bridge changes only its target map
  entry. The loop connection accounts for current/number bindings, output
  heap mutation, continuation, stack, return, exception, allocation, and
  exit cells.
- A3 binding/evaluation/control fidelity: name binding is connected over the
  full plain-frame domain. The loop bridge matches the exact continuation
  observed in a bounded fixed-semantics trace; it has no continuation frame
  or wildcard beyond the connection theorem.
- A4 consistency: every total function has exhaustive, disjoint cases;
  recursion descends structurally. `stepMax`'s guards partition integer
  order. The sole logical simplification is the generated `isInt` subsort
  fact.
- A5 result constraint/non-vacuity: `[1]` is a realizable witness. Demanding
  `[2]` exits `1` and exposes the real result `[1]`.

### Gate B — PASS

- B1 domain alignment: the prompt requests `List[int]`; the formal claims
  cover exactly all finite integer lists, including empty, without a length
  or value bound.
- B2 language adequacy: MPY models the exercised operations—unbounded
  integers, integer comparison, list iteration, indexing, allocation,
  mutation by `append`, calls, frames, and return. The source does not mutate
  its input, so MPY's list-iteration snapshot is immaterial.
- B3 property adequacy: `rollingMax` is defined by appending the larger of the
  prior maximum and the next element, position by position. This is the
  requested rolling/prefix maximum, not merely an opaque execution result.
- B4 implementation alignment: concrete execution, the formal result, the
  prompt example, and the independent oracle agree.

### Gate C — PASS

- The supplied reference semantics and K toolchain are the fixed trusted
  base requested by the task.
- No opaque primitive, result oracle, or unconnected program-operation rule
  affects the theorem.
- The proof-local `isInt` lemma is explicitly recorded; it is the generated
  K subsort predicate fact and does not invent a value.
- Every operational bridge has a separate machine-checked connection
  artifact and command.
- `smoke.py`, `smoke.mpy`, `differential_test.py`,
  `loop-body-mutation.k`, `spec-vacuity.k`, and `proof-run.log` exist and are
  reproduced by `prove.sh`.

## Trust boundary and excluded behavior

Trusted: the supplied `reference-semantics/`, K compiler/backends/prover,
CPython's parser used by the supplied translator, and the generated meaning
of K's `isInt` subsort predicate.

Finite evidence: `differential_test.py` compares against an independent
prefix-slice/`max` oracle for every list of length `0..5` over `-2..2`
(3,906 cases, zero mismatches). This supports intent alignment but is not
used as a universal proof.

Excluded: non-list inputs, lists containing non-integers, behaviors outside
the supplied MPY subset, resource exhaustion, and a separate liveness or
complexity theorem.
