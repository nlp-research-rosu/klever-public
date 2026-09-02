VALIDATED

# Proof report

## What is proven

Under the supplied MPY semantics, `solution.py` is partially correct for the
full material HumanEval contract:

- `arr` is a non-empty finite list of integers;
- `1 <= len(arr) <= 100`;
- `1 <= k <= len(arr)`; and
- the returned integer is the sum of exactly those values among the first `k`
  list positions whose decimal magnitude has at most two digits.

The last condition is formalized as `-99 <= value <= 99`. A minus sign is not a
digit, so values such as `-99` qualify and `-100` does not.

The theorem is symbolic in both the complete input sequence `INPUT:ValSeq` and
`K:Int`; it does not enumerate list sizes or unroll to a fixed bound.

## Formal claim

`SPEC.add-elements` executes the exact translated function definition, performs
an exact call with `list(INPUT)` and `K`, and reaches:

```k
qualifyingPrefix(INPUT, K)
```

under:

```k
allInts(INPUT)
andBool 1 <=Int vsLen(INPUT)
andBool vsLen(INPUT) <=Int 100
andBool 1 <=Int K
andBool K <=Int vsLen(INPUT)
```

`qualifyingPrefix(VS, N)` is a total structural fold. It returns zero for
nonpositive `N` or an exhausted sequence. For a nonempty sequence and positive
`N`, it adds `qualifyingVal(head)` and recurses on the tail and `N - 1`.
`qualifyingVal` returns the integer only in `[-99, 99]`, otherwise zero.

The claim observes the returned value and also requires normal control/state:
the caller environment is restored, the function frame is removed, the stack
and return cells are reset, no exception is present, the exit code is zero, and
the heap remains unchanged. The module-level function binding is the exact
closure translated from `solution.py`.

## Proof obligations

The bridge-free claim `LOOP-SPEC.loop-connection` establishes the invariant:

```text
starting total S
+ qualifying values in the first N positions of the remaining sequence VS
= final returned value
```

Its cases are:

- `N == 0`: `break` exits the loop and returns `S`;
- `N > 0`, qualifying head: one iteration adds the head, decrements `N`, and
  applies the circularity to the tail;
- `N > 0`, nonqualifying head: one iteration preserves the total, decrements
  `N`, and applies the circularity to the tail; and
- the sequence-exhaustion case, which is compatible with `N <= len(VS)`.

The entry theorem initializes `total = 0` and `remaining = k`, then applies the
exact connected loop summary. Thus its result is
`qualifyingPrefix(INPUT, K)`.

## Proof-extension inventory

### Domain and mathematical definitions

`allInts`, `qualifyingValue`, `qualifyingVal`, and `qualifyingPrefix` are
definitional summaries.

- Domain: their equations cover all constructor cases. The guarded cases for
  `qualifyingVal` are disjoint (`isInt` versus its negation). The
  `qualifyingPrefix` cases are disjoint and exhaustive over the sign of `N` and
  the empty/nonempty sequence constructors.
- Descent: the positive recursive case consumes one sequence constructor and
  decrements `N`.
- Semantic role: they describe the mathematical result and input domain; they
  do not rewrite source-program syntax.
- Value influence: `qualifyingPrefix` is the target postcondition and the loop
  summary.
- Justification: direct structural definitions of “sum qualifying values in
  the first N positions.”
- Dependents: the loop connection and `SPEC.add-elements`.

### Guarded dynamic-to-static integer projection

`definedProjectInt`, `projectIntTotal`, its `#Ceil` characterization,
orientation/collapse rules, and the guarded `applyCmp`/`applyBin` twins are
derived sort lemmas.

- Domain: every operational use is guarded by `isInt(V)`.
- Derivation: in MPY, `Int` is a subsort of `Val`; `isInt(V)` states that `V`
  is an injected integer. Under that guard the partial cast is defined and
  returns the same integer. The dispatch twins then reproduce the existing
  MPY-INT equations for integer comparison and integer addition.
- Overlap: on a statically typed `I:Int`, the projection collapses to `I`, so
  the twins agree with the supplied rules. No off-domain projected value
  influences a branch or result.
- Matched context/state footprint: only pure `applyCmp` and `applyBin` terms;
  no configuration cell or control behavior is changed.
- Value influence: integer range branches and accumulator addition.
- Dependents: the bridge-free loop connection.
- Validation: the universal connection theorem closes; boundary witnesses at
  `99` and `-100` agree; changing the body bound from `99` to `98` is rejected.

### Exact loop operational summary

The single ordinary rule in `verification.k` is an operational bridge.

- Replaced execution: the exact translated `#loop`, singleton
  `Return(Name("total")) .Stmts`, `#endcall`, and frame pop.
- Match domain: arbitrary symbolic `VS`, `S`, `N`, globals, builtins, original
  argument values, old loop-target value, heap, and heap location, subject to
  `allInts(VS)`, `0 <= N`, and `N <= vsLen(VS)`.
- Exact context: environment `1`; exact five-key local frame; parent `0`;
  scope location `2`; exactly one stack frame with continuation `.K`, caller
  environment `0`, and saved location `1`; normal return/exception/exit cells;
  no framed K continuation.
- State footprint: returns `S + qualifyingPrefix(VS,N)`, restores environment
  `0`, deletes the callee scope, resets scope location to `1`, pops the frame,
  and preserves globals, builtins, heap, heap location, return state,
  exception state, and exit code.
- Control: the bridge includes `break`, the singleton return-statement
  sequence, `#endcall`, and the exact frame pop. It cannot match a different
  continuation or stack.
- Universal justification: `LOOP-SPEC.loop-connection` has the identical LHS,
  RHS, guards, continuation, bindings, and cells. It is proved using
  `verification-base.k`, which does not contain or import the bridge.
- Context containment: the bridge and connection theorem are textually
  identical over every operational field; the bridge accepts no wider suffix,
  frame, binding map, or guard.
- Dependents: `SPEC.add-elements`.
- Validation: bridge-free and bridge-enabled ground witnesses both produce
  `104` with identical final control/state. The body mutation fails.

There are no trusted result oracles, trusted program helpers, or unproved
program-defined operations.

## Exact commands and actual results

The complete reproducible command sequence is in `prove.sh`. It was executed
from `/workspace` as:

```bash
./prove.sh
```

Actual overall result: exit `0`.

Key commands and decisive actual outputs:

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Output: none; exit `0`.

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Exit `0`. The final concrete configuration contains:

```text
"result" |-> 24
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The compiler also printed non-exhaustiveness/unused-variable warnings from the
supplied read-only semantics; compilation succeeded.

```bash
kompile verification-base.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove loop-spec.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC
```

Actual proof output: `#Top`; exit `0`.

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual target-proof output: `#Top`; exit `0`.

```bash
kprove loop-witness-base.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-WITNESS-BASE
kprove loop-witness-extended.k \
  --definition verification-kompiled \
  --spec-module LOOP-WITNESS-EXTENDED
```

Actual outputs: `#Top` and `#Top`; both exit `0`. The witness starts with
`total = 5`, sequence `[99, -100, 7]`, and `N = 2`, and reaches result `104`
with the same final control/state.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1`, `WarnStuckClaimState`. The residual rejects:

```text
qualifyingPrefix(INPUT, K) +Int 1
#Equals
qualifyingPrefix(INPUT, K)
```

This is the deliberate false-postcondition mutation. A concrete satisfiable
witness is `INPUT = [1]`, `K = 1`.

```bash
kprove loop-spec-body-mutation.k \
  --definition verification-base-kompiled \
  --spec-module LOOP-SPEC-BODY-MUTATION
```

Actual result: exit `1`, `WarnStuckClaimState`. This probe changes the program
body’s upper inclusion check from `99` to `98` while retaining the original
summary; the residual exposes the disagreement at that boundary.

```bash
python3 differential_test.py
```

Actual output:

```text
cases=5051 mismatches=0
```

The installed toolchain reported K version `v7.1.293`.

## Gate results

### Gate A — PASS

- The exact program body loads and executes under the supplied semantics.
- The only execution bridge has a bridge-free universal connection theorem
  over its complete match domain.
- Binding, evaluation, `break`, return, frame popping, and all modeled state
  cells are included in that connection.
- All equations are guarded, exhaustive over their claimed domains, and
  consistent on overlaps.
- Fixed and extended boundary witnesses agree.
- The changed-body probe and false-postcondition probe both fail as required.

### Gate B — PASS

The formal domain exactly matches the prompt: integer lists of lengths
`1..100`, with `k` in `1..len(arr)`. The theorem is symbolic over the whole
domain. The formal result is exactly the sum of values in the first `k`
positions that lie in `[-99,99]`, matching the literal digit contract and the
worked example. No valid list size, `k`, or integer magnitude is omitted.

### Gate C — PASS

All proof extensions, assumptions, commands, witnesses, mutations, and
empirical checks are recorded in existing artifacts and reproduced by
`prove.sh`. Finite differential evidence is reported only as evidence, not as
the universal proof.

## Trust boundary

The proof relies on:

- the supplied read-only MPY semantics as the intended model;
- the K compiler/prover and SMT-backed integer reasoning;
- the fixed `py2mpy.py` translator; and
- K’s standard `Int < Val` subsort predicate/cast relationship used by the
  guarded projection lemmas.

These affect both positive claims. No task-local primitive is accepted on
trust. `solution.mpy` is regenerated from `solution.py` by `prove.sh`.

## Empirically supported facts

`differential_test.py` compares the implementation against an independent
slice-and-generator oracle. It covers every allowed length `1..100`, every
allowed `k` for each generated list, the prompt example, and repeated boundary
values around `-100`, `-99`, `99`, and `100`: 5,051 cases, zero mismatches.

The LLVM smoke artifact executes the translated implementation on the prompt
example and records result `24`.

## Excluded behavior

- Inputs outside the stated HumanEval constraints are not part of the target
  theorem.
- Non-integer list elements are excluded exactly because the prompt specifies
  an array of integers.
- The report establishes partial correctness under the supplied semantics; it
  does not claim a separate liveness theorem or correctness of the K toolchain
  itself.
