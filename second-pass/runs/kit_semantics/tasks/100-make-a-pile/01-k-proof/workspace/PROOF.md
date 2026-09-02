VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, `make_a_pile` is partially
correct for every symbolic integer `N > 0`.  Starting from the standard fresh
module configuration, the proof loads the exact generated function body, binds
`N` to parameter `n`, executes the body, and returns `ref(0)`.  The referenced
heap object is:

```k
list(finishPile(.ValSeq, N, 0))
```

where `finishPile` appends `N + 2*I` for successive indices `I = 0, ..., N-1`.
Thus the returned Python list has exactly `N` elements:

```text
[N, N + 2, N + 4, ..., N + 2*(N - 1)]
```

The theorem also constrains frame cleanup, the module binding, heap allocation,
the absence of an exception, and exit code 0.  As prescribed by the kit, this
is a partial-correctness theorem: termination is not itself a reachability
claim.

## Formal claims

`spec.k` contains exactly the two positive claims required by this one-loop
program:

1. `pile-loop` is a circularity at the semantics' actual recurring control
   point, `#while`.  For `N >= 0` and `0 <= I <= N`, it changes local `i` from
   `I` to `N` and heap list `A` to `finishPile(A, N, I)`, while preserving the
   arbitrary continuation and framed configuration.
2. `make-a-pile` starts with
   `#loadAll(Module(FuncDef(...))) ~> Call(Name("make_a_pile"), N)`.  The
   `FuncDef` body is the body generated in `solution.mpy`.  For `N > 0`, it
   returns `ref(0)` whose heap value is
   `list(finishPile(.ValSeq, N, 0))`.

The summary is defined by the exhaustive equations:

```k
finishPile(A, N, I) = A                                      if I >= N
finishPile(A, N, I) =
  finishPile(A ++ [N + 2*I], N, I + 1)                      if I < N
```

The guards are disjoint and cover all integer `I, N`.  Recursion terminates
because `N-I` strictly decreases in the recursive case.

## Proof-extension inventory

### `finishPile(ValSeq, Int, Int)`

- **Class:** Definitional summary.
- **Semantic role:** Names the final list sequence; it does not match a
  `<k>` term and does not replace Python execution.
- **Domain:** All `ValSeq A` and integers `N, I`; guards `I >= N` and `I < N`.
- **Matched context:** A pure function term only.  It accepts no continuation,
  control stack, binding, or configuration-cell frame.
- **Justification scope:** The two equations define the value over the complete
  domain.  Their guards are exhaustive, disjoint, and recursively descending.
- **Context containment:** Trivial because there is no operational context.
- **State footprint:** Reads and writes no configuration cells.
- **Value influence:** Determines the loop claim's final heap value and the
  entry claim's returned list contents.
- **Value justification:** The recursive step appends precisely the expression
  executed by the program, `N + 2*I`, and increments precisely the loop index.
- **Justification:** Truthful total recursive definition.
- **Dependents:** `pile-loop` and `make-a-pile`.
- **Control validation:** Not applicable; this is not an operational bridge.
- **Value validation:** The positive proof, ground K smoke cases, the rejected
  changed-body probe, and the independent CPython differential test.
- **Validation:** Gate A equation coverage/overlap/descent audit passed.

### `SPEC.pile-loop`

- **Class:** Derived reachability lemma, used coinductively as a loop
  circularity.
- **Semantic role:** Reasons about fixed-semantics execution of `#while`; it
  adds no ordinary rewrite rule and skips no program operation.
- **Domain:** `N >= 0`, `0 <= I <= N`, exact local bindings for `n`, `pile`,
  and `i`, with the heap object at `H`.
- **Matched context:** Exact `#while` condition and body; environment `L`;
  local scope with parent 0; heap entry `H |-> list(A)`; an arbitrary preserved
  `<k>` suffix and framed unrelated scopes, heap entries, and cells.
- **Justification scope:** The claim itself is machine-checked over that same
  universally quantified configuration.  The entry theorem instantiates it
  with `L=1`, `H=0`, `A=.ValSeq`, and `I=0`.
- **Context containment:** The arbitrary continuation is quantified by the
  claim's own `<k>` frame, and fixed semantics returns to it after the loop.
  No broader rewrite rule is introduced.
- **State footprint:** Reads `n`, `i`, `pile`, and heap entry `H`; writes `i`
  and heap entry `H`; preserves environment, other scope/heap entries, stack,
  return state, exception state, exit code, and the continuation.
- **Value influence:** Establishes every returned list element and the final
  heap sequence used by the entry claim.
- **Value justification:** Direct symbolic execution of lookup, comparison,
  method binding, argument evaluation, integer arithmetic, `append`, increment,
  and loop control under the fixed semantics.
- **Justification:** `kprove` closes the base and step paths and prints `#Top`.
- **Dependents:** `SPEC.make-a-pile`.
- **Control validation:** No bridge exists.  The claim is anchored on the
  residual's exact `#while` head, and the body-sensitivity mutation is rejected.
- **Value validation:** Concrete results for `N=1,3,5`; changed multiplier
  produces the rejected result `[3,6,9]`; 1,000 CPython oracle comparisons have
  zero mismatches.
- **Validation:** Gates A, B, and C passed.

There are no proof-local operational bridges, simplification lemmas, priority
rules, trusted primitives, or opaque result-bearing symbols.

## Exact commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh
```

It exited 0.  `prove.sh` records and runs these positive proof commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 -m py_compile solution.py validate.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

The positive proof's complete stdout is stored in `proof.out`:

```text
#Top
```

The command exited 0.  Compiler warnings in the run concern unused variables
and unrelated non-exhaustive functions in the supplied reference semantics;
neither `solution.py` nor the proof calls those unrelated functions.

The concrete K output is stored in `smoke.out`.  It exited 0 and ended with:

```text
<k> .K </k>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

Its heap includes the checked results `[1]`, `[3,5,7]`, and
`[5,7,9,11,13]`.

The non-vacuity command was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited 1 as expected.  `vacuity.out` shows the actual final result
`ref(0)`, while the mutation demands `ref(1)`; `vacuity.err` contains
`WarnStuckClaimState`.

The body-sensitivity command was:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

It exited 1 as expected.  `body-mutation.out` shows that changing `2*i` to
`3*i` yields:

```text
0 |-> list(vCons(3, vCons(6, vCons(9, .ValSeq))))
```

which does not satisfy the original `N=3` result; `body-mutation.err` contains
`WarnStuckClaimState`.

The independent finite validation command and complete output were:

```bash
python3 validate.py
```

```text
CPython differential validation: 1000 inputs, 0 mismatches
```

## Gate results

### Gate A — PASS

- **A1:** The entry claim loads and executes the exact program-defined body.
  It includes real definition binding, lookup, argument binding, body,
  return, and frame cleanup.  The `2*i` to `3*i` body mutation exits 1 and
  exposes `[3,6,9]`.
- **A2:** No operational bridge exists.  The claims constrain the returned
  reference, list heap object, heap location, scopes, environment, stack,
  return state, exception state, and exit code.
- **A3:** Fixed semantics performs lookup, left-to-right call evaluation,
  bound-method selection, return control, and loop control.  The loop lemma's
  arbitrary continuation is within its own quantified proof scope.
- **A4:** `finishPile` has true definitional equations with disjoint,
  exhaustive guards and strict recursive descent.
- **A5:** `N=1` is a realizable precondition witness and passes concrete K
  execution.  The false returned-reference mutation exits 1 with a stuck
  residual showing `ref(0)`.

### Gate B — PASS

- **B1:** The formal domain `N:Int` with `N > 0` exactly matches the prompt's
  positive-integer domain.
- **B2:** The used subset—unbounded integers, lists, `while`, comparison,
  arithmetic, method call/append, assignment, function binding, and return—is
  modeled by the supplied semantics.  K integers match Python's unbounded
  integer behavior for these operations.
- **B3:** The summary's equations formally state the requested sequence:
  append `N + 2*I` for each `I` from 0 through `N-1`.
- **B4:** The implementation and theorem agree with the prompt example and
  the independent oracle.

### Gate C — PASS

All claimed evidence is reproducible from existing files through `prove.sh`.
Positive proof output, concrete output, both negative residuals, and
differential output are preserved in the corresponding `.out`/`.err` files.
Finite tests are reported only as empirical support, not as universal proofs.

## Trust boundary

| Component | Status and effect | Dependents | Evidence |
|---|---|---|---|
| Supplied `reference-semantics/` | Fixed trusted language model; affects value, control, state, and exceptions | Both claims | LLVM smoke run and direct inspection of the used modules |
| Supplied `py2mpy.py` | Fixed translator from CPython AST to K constructors | Program identity | Regenerated by `prove.sh`; generated body is present in the entry claim |
| K v7.1.293 Haskell backend and proof engine | Trusted proof implementation | `#Top` result | Exit 0 and exact `proof.out` |
| CPython and `validate.py` oracle | Empirical adequacy evidence only; not used to close claims | Gate C evidence | Inputs 1 through 1000, zero mismatches |

No unproved proof-local component affects the result.  The correspondence
between the supplied reference semantics and full CPython is necessarily
conditional on the supplied semantics being an adequate model of the used
subset.

## Empirically supported facts

- LLVM execution under the supplied semantics passes `N=1`, `N=3`, and `N=5`.
- CPython execution matches the independently expressed
  `list(range(n, 3*n, 2))` oracle for every `n` in `1..1000`.
- The wrong-return and changed-body negative probes both exit 1 with concrete
  residual evidence.

These finite checks support program identity and intent adequacy; universal
partial correctness comes from the `#Top` symbolic proof.

## Excluded behavior

- Non-integer and non-positive inputs are outside the theorem and outside the
  prompt's stated domain.
- Termination, runtime resource bounds, and behavior of Python constructs not
  used by this implementation are not claimed.
- Correctness with respect to CPython is conditional on the supplied
  reference semantics accurately modeling the used subset.
