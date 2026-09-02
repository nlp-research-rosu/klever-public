VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every K integer `N >= 0`, calling the
exact closure body translated from `solution.py` returns a reference to a list
described by:

```k
resultRun(.ValSeq, 1, N, 1, 0)
```

The call starts in the module environment with `f` bound to the exact
`closureVal` in `spec.k`. It returns `ref(0)`; heap location `0` contains that
list; allocation advances `heapLoc` from `0` to `1`; the caller environment,
scope store, empty stack, `noRet`, `NoExc`, and exit code `0` are restored or
preserved as stated by the claim.

This is a partial-correctness result. The K claims do not establish a separate
total-correctness theorem.

## Formal claims and intent

`spec.k` contains exactly two claims:

1. `SPEC.loop-invariant` starts at the real internal `#while` term with the
   exact source guard and body. For `I >= 1` and `N >= I - 1`, it updates:
   `i` to `N + 1`, `fact` to `factRun(I,N,F)`, `total` to
   `totalRun(I,N,T)`, and the heap list to
   `resultRun(VS,I,N,F,T)`. It is the loop circularity.
2. `SPEC.f-correct` invokes the exact closure with arbitrary `N >= 0` from the
   initial caller state and constrains the returned reference and complete
   observable heap list.

The plain-language connection is by induction on the source loop. Before
iteration `i`, `fact` is the product through `i-1` and `total` is the sum
through `i-1`. The two updates therefore make them `i!` and
`1 + ... + i`. The branch appends the former for even `i` and the latter for
odd `i`. Exactly one value is appended for every `i` from `1` through `N`, so
the returned list has length `N` and the requested value at every
one-based position. At `N = 0`, no iteration occurs and the result is empty.

Program boundary: module loading itself is outside the entry claim. The claim
starts immediately before lookup and call, with `f` bound to its exact
parameter list, body, and defining environment. Lookup, argument evaluation,
frame creation, parameter binding, every body operation, return, and frame pop
all execute under the fixed supplied semantics.

## Proof-extension inventory

No proof-local rule matches a `<k>` cell, rewrites a program term, skips a
program-defined operation, changes rule priority, or introduces abrupt control.
There is no operational bridge and no trusted result-bearing primitive.

### `factRun` and `totalRun`

- Extension/class: `factRun(Int,Int,Int)` and
  `totalRun(Int,Int,Int)` with their concrete base/step equations are
  definitional summaries.
- Semantic role: they name final accumulator values; they never replace source
  execution.
- Domain: all K integers. `I <= N` and `I > N` are exhaustive and disjoint.
- Matched context: pure terms only; no continuation, binding, or cell is
  matched.
- Justification scope/context containment: the equations define exactly the
  complete integer domain they accept, so matched and justified domains are
  identical.
- State footprint: none.
- Value influence: `factRun` constrains the final local factorial accumulator;
  `totalRun` constrains the final local sum accumulator. Their carried values
  also determine entries summarized by `resultRun`.
- Value justification: the step equations are precisely `F := F*I` and
  `T := T+I`; base equations return the accumulator when `I > N`.
- Termination/totality: on a concrete recursive case, `I` increases by one;
  the measure `max(N-I+1,0)` decreases. The two guarded cases cover all
  integers. `[no-evaluators]` is metadata, not a trust assumption.
- Dependents: `SPEC.loop-invariant`, then `SPEC.f-correct`.
- Control validation: not applicable; these are pure summaries.
- Value validation: fixed program execution is connected universally by the
  loop and entry claims; concrete and independent tests are recorded below.

### `resultRun`

- Extension/class: `resultRun(ValSeq,Int,Int,Int,Int)` and its concrete
  equations are a definitional summary.
- Semantic role: it names the final list value after fixed execution; it does
  not intercept list construction, `append`, a branch, or the loop.
- Domain: every `ValSeq` and all integer arguments. The cases are
  `I > N`, `I <= N` with `pyMod(I,2) == 0`, and `I <= N` with
  `pyMod(I,2) != 0`. They are exhaustive and pairwise disjoint.
- Matched context: pure terms only.
- Justification scope/context containment: its exact recursive equations cover
  every matched term.
- State footprint: none; its value describes the heap cell tracked by the
  claims.
- Value influence: it is the complete observable returned list.
- Value justification: its even step appends `F*I`; its odd step appends
  `T+I`; both advance `I`, `F`, and `T` exactly like one source iteration.
  Its base case returns the accumulated sequence.
- Termination/totality: the same decreasing measure as above.
- Dependents: both claims.
- Control validation: not applicable.
- Value validation: the universal connection is machine-checked by the
  reachability claims. The false-result mutation and concrete tests below
  independently show result sensitivity.

### Folding simplification rules

- Extension/class: the reverse-step rules for `factRun`, `totalRun`, and the
  even/odd `resultRun` cases are derived lemmas; the base simplifications
  repeat the corresponding base equations.
- Semantic role: they fold a post-iteration summary back to the
  pre-iteration summary so the circularity can close. They do not rewrite
  source AST or operational control.
- Domain: exactly the guards on the corresponding defining equations.
- Matched context: pure summary terms only.
- Justification scope/context containment: each fold is the symmetric equality
  of its exact guarded defining step. There are no extra frames or wildcards.
- State footprint: none.
- Value influence: they normalize the summary values used in the invariant
  and final postcondition.
- Value justification: direct substitution into the concrete recursive
  definitions.
- Dependents: the inductive branch of `SPEC.loop-invariant`.
- Control validation: not applicable.
- Value validation: exhaustive/disjoint guards were audited; the base rules
  agree on overlaps; both negative probes remain rejected.

### `SPEC.loop-invariant`

- Extension/class: derived auxiliary reachability claim/circularity.
- Semantic role: it reasons about the actual fixed-semantics `#while`; it is
  not an ordinary rewrite in `verification.k`.
- Domain: the exact loop body and exact local map containing `n`, `result`,
  `fact`, `total`, and `i`, with `I >= 1` and `N >= I-1`.
- Matched context: current environment `L`, exact local scope, heap object `H`,
  and a universally quantified trailing computation plus framed unrelated
  scope/heap entries and configuration cells.
- Justification scope/context containment: the claim itself proves the same
  universally quantified continuation and frames it matches. The body has no
  `return`, `break`, `continue`, exception, or cleanup construct; fixed
  `#loopLbl` control preserves the suffix.
- State footprint: reads `n`, `i`, `fact`, `total`, and `result`; writes
  `i`, `fact`, `total`, and heap entry `H`; preserves the result reference,
  `n`, environment, other scope/heap entries, heap location, stack, return,
  exception, exit code, and continuation.
- Value influence/justification: its RHS summaries constrain every modified
  local and the full heap list. Base and inductive obligations close through
  fixed execution and the truthful equations above.
- Dependents: `SPEC.f-correct`.
- Control validation: the focused invariant proof prints `#Top`; LLVM runs
  reach normal control state; the body mutation is rejected.
- Value validation: the full proof prints `#Top`; the false postcondition is
  rejected; independent oracle tests have zero mismatches.

## Exact commands and actual results

Tool version:

```text
kompile/kprove: K version v7.1.293
```

The complete reproducible command is:

```bash
./prove.sh
```

Actual result: exit `0`. `prove.sh` contains and ran these exact positive
commands:

```bash
python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 make_smoke.py 0 > smoke-0.mpy
python3 make_smoke.py 5 > smoke-5.mpy
krun smoke-0.mpy --definition runtime-kompiled --output pretty > smoke-0.out
krun smoke-5.mpy --definition runtime-kompiled --output pretty > smoke-5.out
python3 test_solution.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual decisive outputs and exits:

```text
LLVM kompile: exit 0
smoke-0 heap: 0 |-> list ( .ValSeq )
smoke-5 heap: 0 |-> list ( vCons ( 1 , vCons ( 2 , vCons ( 6 , vCons ( 24 , vCons ( 15 , .ValSeq ) ) ) ) ) )
native differential: 51 cases, 0 mismatches
Haskell kompile: exit 0
focused loop kprove: #Top, exit 0
full two-claim kprove: #Top, exit 0
prove.sh: exit 0
```

Both compilations emitted warnings from untouched supplied semantics. LLVM
reported non-exhaustive matches in unrelated general helpers and unused
variables in `str.k`; Haskell reported only the same unused `str.k` variables.
Neither compilation emitted an error.

Gate A negative commands are also exact in `prove.sh`. Their generated
artifacts are `spec-vacuity.k` and `spec-body-mutation.k`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual results:

```text
false-postcondition mutation: WarnStuckClaimState, exit 1
residual: resultRun(.ValSeq,1,N,1,0)
          = vCons(999,resultRun(.ValSeq,1,N,1,0))

body mutation total=0 -> total=100: WarnStuckClaimState, exit 1
residual: resultRun(.ValSeq,1,N,1,0)
          = resultRun(.ValSeq,1,N,1,100)
```

The satisfiable witness `N=0` already distinguishes the false prepended
element. The body mutation is distinguished, for example, by `N=1`.

## Gate results

### Gate A — PASS

- A1: the exact bound closure body executes under fixed semantics. Changing
  `total = 0` to `total = 100` invalidates the connection proof.
- A2: there is no operational bridge. The claims explicitly track the mutable
  heap list, local bindings, allocation, and restored call state.
- A3: fixed semantics performs lookup, argument evaluation, binding,
  arithmetic, branching, method dispatch, append, loop control, return, and
  frame pop. No proof-local rule preempts them.
- A4: all summary guards are exhaustive/disjoint, recursion descends on
  concrete inputs, overlapping base equations agree, and each folding lemma is
  the exact reverse of a defining step under the same guard.
- A5: `N=0` and `N=5` realize the precondition. The final heap list is
  constrained, and the deliberate false list is rejected with exit `1`.

### Gate B — PASS

- B1: the formal domain is unbounded integer `N >= 0`. This matches the
  meaningful domain of a requested list of size `n`; negative sizes and
  non-integer Python values are not part of the prompt-level contract.
- B2: exercised behavior uses unbounded integers, lists, mutation, function
  calls, and structured control supported by the supplied semantics. Unbounded
  K integers align with CPython integers for these operations.
- B3: the accumulator induction above connects the machine-checked execution
  summary to factorial and `1+...+i`; the source example and finite oracle
  tests agree.
- B4: the implementation returns the requested sequence, including the empty
  `N=0` boundary and the prompt's `N=5` example.

### Gate C — PASS

- C1: every trust assumption and dependent is listed below; there is no hidden
  proof-local oracle.
- C2: all cited translation, build, proof, mutation, LLVM, and differential
  artifacts exist in this directory, and `prove.sh` reproduces their commands
  and checks.
- C3: formal facts, finite evidence, assumptions, and exclusions are separated
  in this report.

## Trust boundary

1. Supplied `reference-semantics/` is trusted to model the exercised Python
   subset faithfully. It affects value, control, state, and every claim.
   Evidence: LLVM execution agrees at `N=0` and `N=5` with CPython and the
   independent oracle. The supplied files were not modified.
2. `py2mpy.py` is trusted as the fixed AST translator. It affects program
   identity. `solution.mpy` was regenerated with the required command, and a
   final regeneration compared byte-for-byte equal.
3. K v7.1.293, its LLVM/Haskell backends, and the host arithmetic/runtime are
   trusted to implement K correctly. Every formal conclusion depends on this
   standard toolchain boundary.

There are no external primitives or proof-local opaque values whose
interpretation can select a result, branch, state change, or exception.

## Empirically supported facts

- `smoke-0.mpy` is generated from the exact `solution.py` AST plus
  `answer = f(0)`. LLVM produced an empty list.
- `smoke-5.mpy` is generated the same way with `f(5)`. LLVM produced
  `[1, 2, 6, 24, 15]`.
- `test_solution.py` compares `solution.f` for every `n` in `0..50` with an
  independently written oracle using `math.factorial` for even indices and
  `sum(range(1,i+1))` for odd indices. Output: `51 cases, 0 mismatches`.

These finite checks support semantic adequacy; they do not replace the
universal K reachability proof.

## Excluded behavior

- Inputs outside integer `N >= 0`, including negative integers and non-integer
  Python objects.
- A proof that the supplied reference semantics is equivalent to all of
  CPython.
- Python features and exceptions outside the exercised reference-semantics
  subset.
- Resource bounds, performance, and a separate machine-checked termination
  theorem.
- Any inference that `#Top` alone establishes validation; the `VALIDATED`
  headline additionally reflects the Gate A/B/C audit above.
