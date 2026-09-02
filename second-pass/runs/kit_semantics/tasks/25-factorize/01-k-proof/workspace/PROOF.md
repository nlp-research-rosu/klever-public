VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every mathematical integer `N >= 1`,
calling the exact translated body of `factorize(N)` from its normal module
binding, if execution terminates, returns the reference to a list whose value is
`factorAcc(.ValSeq, N, 2)`.  The call restores the caller environment and stack,
leaves `NoExc`, leaves exit code `0`, and accounts exactly for the one allocated
result list.

`factorAcc(A, N, D)` is the unbounded canonical trial-division specification:

- if `N < D`, it returns `A`;
- if `D <= N` and `D` divides `N`, it appends `D`, replaces `N` by `N // D`,
  and continues with the same divisor;
- otherwise it continues with `D + 1`.

Starting with an empty list and divisor `2`, this recurrence is equivalent to
the HumanEval contract.  Candidates are examined in increasing order.  A
candidate that is appended cannot be composite: a smaller prime divisor would
also divide the current remainder and would already have been processed.
Keeping the divisor after division and only incrementing it makes the output
nondecreasing.  The invariant
`original input = product(accumulated factors) * current remainder` is
preserved by every division.  On a reachable loop exit the remainder is `1`,
so the output product is the original input.  The empty product handles
`factorize(1) == []`.

This is a partial-correctness reachability proof, as specified by the Kit.
Termination on `N >= 1` additionally follows from the usual well-founded
trial-division argument: a failed test advances the divisor toward the current
remainder, while a successful test divides the positive remainder by at least
`2`.

## Formal claims

`SPEC.factor-loop` is the loop circularity.  Its domain is symbolic and
unbounded (`N >= 1`, `D >= 2`, and arbitrary accumulated `ValSeq A`).  It
matches the exact function frame, continuation, closure binding, local scope,
heap object, return state, exception state, and exit code reached by the real
call.

Its three proof branches are:

1. `N < D`: the loop guard is false and the base equation returns `A`.
2. `D <= N` and `pyMod(N,D) == 0`: fixed semantics executes lookup, `append`,
   heap mutation, floor division, assignment, and loop control; the recursive
   summary has exactly the resulting accumulator, quotient, and divisor.
3. `D <= N` and `pyMod(N,D) != 0`: fixed semantics increments the divisor and
   the recursive summary takes the same step.

`SPEC.factorize` invokes the exact closure after normal module loading has
bound it.  It starts with an empty heap and an arbitrary `N >= 1`, reaches the
loop claim after the two initial assignments, returns `ref(0)`, and leaves
`0 |-> list(factorAcc(.ValSeq, N, 2))` in the heap.

The observable state is the returned reference, its list value, allocation
counter, restored environment/scope stack, return state, exception state, and
exit code.  No output or external state exists in the exercised subset.

## Proof-extension inventory

### `factorAcc` and its three guarded equations

- **Class:** Definitional summary.
- **Semantic role:** Names the mathematical final sequence; it does not match a
  `<k>` term and cannot replace program execution.
- **Domain:** Every proof use has `N >= 1` and `D >= 2`.  On that domain the
  guards `N < D`, `D <= N and mod == 0`, and
  `D <= N and mod != 0` are exhaustive and pairwise disjoint.
- **Matched context:** Pure `factorAcc(A,N,D)` terms only; no continuation,
  binding, control stack, or configuration cell is matched.
- **Justification scope / containment:** The equations are the exact
  recurrence of the source loop.  `SPEC.factor-loop` is the machine-checked
  universal connection for every use domain and in the exact runtime context.
- **State footprint:** None directly.  The named value characterizes the
  `ValSeq` stored in heap location `0`.
- **Value influence:** It determines the final list in both claims.
- **Value justification:** The base/divisible/non-divisible equations plus the
  fixed-semantics loop claim.  The symbol is neither opaque nor totalized.
- **Dependents:** `SPEC.factor-loop` and `SPEC.factorize`.
- **Control validation:** No operational bridge exists.  LLVM execution reaches
  `.K`; the divisor-initialization body mutation is rejected.
- **Value validation:** Ground witnesses produce distinct values for `1`, `2`,
  `8`, `25`, `70`, and `97`; the false `[999]` interpretation for input `1` is
  rejected; the independent differential run reports zero mismatches.

### `SPEC.factor-loop`

- **Class:** Derived auxiliary reachability claim (loop-invariant
  circularity).
- **Semantic role:** Proves the loop summary by executing the fixed semantics;
  it is a `claim`, not an operational `rule`.
- **Domain:** `N >= 1`, `D >= 2`, arbitrary accumulated `A`.
- **Matched context:** Exact `#while` term; exact trailing
  `Return(Name("factors")) .Stmts ~> #endcall`; environment `1`; the exact
  module closure and local map; heap location `0`; heap/scope counters; the
  exact caller frame; `noRet`; `NoExc`; exit code `0`.  There are no cell
  frames, ellipses, wildcards, or arbitrary continuations.
- **Justification scope / containment:** Identical to the claim's match domain,
  so the entry configuration is contained without widening.
- **State footprint:** Reads `n`, `divisor`, and `factors`; may update `n`,
  `divisor`, and heap location `0`; preserves the closure binding, list
  identity, environment, counters, stack, return state, exception state, exit
  code, and trailing return continuation.
- **Value influence:** Establishes the final `factorAcc` list used by the entry
  claim.
- **Value justification:** The three factor-summary equations and one genuine
  fixed-semantics loop iteration before circularity is reapplied.
- **Dependents:** `SPEC.factorize`.
- **Control validation:** The claim itself closed with `#Top`; the exact
  continuation remains present on both sides.  No return, frame pop, or
  exception is skipped.
- **Value validation:** The false-result and body-sensitivity probes both
  terminate stuck with the actual empty heap list visible.

There are no proof-local simplification rules, `[total]` assumptions,
`[concrete]` proof rules, priorities, operational bridges, opaque values, or
trusted primitives.

## Exact commands and actual results

The complete recorded workflow is:

```bash
./prove.sh
```

It exited `0`.  Its substantive commands and results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
```

Both exited `0`.  Regenerating `solution.mpy` into a temporary file and running
`cmp -s` exited `0`.

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled
```

Both exited `0`.  `krun` ended with `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`.  Its heap contained the expected sequences for
`1`, `2`, `8`, `25`, `70`, and `97`.

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

Compilation exited `0`.  `kprove` printed exactly `#Top` as its proof result and
exited `0`, proving every claim in `SPEC`.  Compiler warnings concern unused
pattern variables in the supplied `str.k`, the existential final local values
in the loop claim, and unrelated non-exhaustive supplied functions; none is
reachable as an unproved operation in this task.

The A5 mutation command was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

The underlying command exited `1`, printed `WarnStuckClaimState`, and exposed
the actual result `0 |-> list(.ValSeq)` rather than the deliberately requested
`0 |-> list(vCons(999,.ValSeq))`.  `prove.sh` recorded
`EXPECTED FAILURE: false-postcondition probe rejected`.

The body-sensitivity command was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

The underlying command exited `1`, printed `WarnStuckClaimState`, and exposed
the mutated program's empty list rather than `[2]`.  `prove.sh` recorded
`EXPECTED FAILURE: body-mutation probe rejected`.

```bash
python3 test_solution.py
```

This exited `0` and printed:

```text
differential inputs=2003 mismatches=0
```

## Gate results

### Gate A — PASS

- **A1:** `solution.mpy` is freshly generated from `solution.py`; the entry
  binding contains the same translated body and fixed semantics executes it.
  Changing the initial divisor from `2` to `3` invalidates the `n = 2` result.
- **A2:** There are no operational bridges.  The claims explicitly account for
  the list heap update, allocation counter, local scope, caller frame, return
  state, exception state, and exit code.
- **A3:** Name lookup selects the exact closure, arguments are evaluated by the
  supplied call machinery, and the exact return continuation and caller frame
  are retained.  No abrupt control is abstracted.
- **A4:** The new equations are disjoint and exhaustive on every use domain,
  use the supplied `pyMod` and integer division, and introduce no totality or
  opacity assumption.
- **A5:** `N = 1` is a realizable boundary witness.  The false `[999]`
  postcondition exits nonzero with the actual empty result visible.

### Gate B — PASS

- **B1:** The theorem covers every positive integer symbolically; it has no
  list-size, value, iteration, or unrolling bound.  Inputs `N <= 0` are excluded
  because the stated positive-prime-factor/product contract is inherently
  undefined there.  `N = 1` is included.
- **B2:** K `Int` and Python `int` are unbounded mathematical integers for all
  exercised operations.  Heap-backed list allocation and `append`, lookup,
  functions, comparisons, modulo, floor division, loops, and return are all
  supplied semantics rules.  The positive domain prevents zero division.
- **B3:** Machine checking connects the real program to the complete
  trial-division recurrence.  The increasing-candidate, divisibility, product,
  and remainder arguments above establish that this recurrence denotes exactly
  the ordered prime-factor list.  Independent property checks support that
  adequacy bridge but are not presented as universal proof.
- **B4:** The implementation agrees with all prompt examples and the boundary
  value `1`.

### Gate C — PASS

- **C1:** The trust ledger below names every boundary; no hidden proof-local
  primitive or bridge exists.
- **C2:** All cited artifacts exist, all commands are in `prove.sh`, and the
  exact input scope, oracle, output, and mismatch count are recorded.
- **C3:** Machine-checked partial correctness, mathematical termination/intent
  reasoning, finite empirical evidence, and excluded inputs are separated.

## Trust boundary

- **Supplied `MPY` semantics and K backend:** Trusted foundation for value,
  control, state, and proof execution.  Every target claim depends on it.
  Evidence is the successful LLVM execution, Haskell proof, and negative
  probes.
- **`py2mpy.py`:** Mandated translator outside the theorem.  It affects program
  identity.  `solution.mpy` is reproducibly generated, and the proof's closure
  body was audited constructor-for-constructor against it.
- **Trial-division meaning and termination:** These are mathematical adequacy
  arguments, not extra K rewrite axioms.  They affect interpretation and
  total-correctness language, not Gate A closure.  Evidence is the derivation
  above plus the independent differential/property test.

No opaque sorting, floating-point, string, digest, assertion-oracle, or other
reference-semantics primitive is reached by the symbolic target claims.

## Empirically supported facts

`concrete-tests.py` is translated by the same fixed translator and run with the
required LLVM `MPY-KRUN` definition.  It checks `1`, `2`, every prompt example,
and prime `97`.

`test_solution.py` uses an independently structured square-root trial-division
oracle.  It checks every input `1..2000` plus `9973`, `65536`, and `99991`.
For each input it compares the entire returned list and separately checks
nondecreasing order, primality of every element, and product equality.  The
recorded result is 2,003 inputs and zero mismatches.  These finite results
support validation; they do not replace the unbounded K claims.

## Excluded behavior

- Integers `N <= 0`, for which the prompt's finite positive-prime-factor
  product contract has no result.
- Non-integer Python values, excluded by the required `n: int` signature and
  the formal `Int` input.
- A machine-checked termination theorem; K reachability here proves partial
  correctness.  Termination on the included domain is supplied by the
  well-founded mathematical argument above.
