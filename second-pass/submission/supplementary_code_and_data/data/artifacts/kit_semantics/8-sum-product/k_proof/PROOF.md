VALIDATED

# What is proven

Under the supplied `reference-semantics`, `spec.k` proves partial correctness of
the exact translated `sum_product` implementation for every finite semantic
Python list whose elements are `Int` values. There is no list-length or
integer-magnitude bound.

For every `VS:ValSeq` satisfying `allInts(VS)`, the `sum-product` claim starts
from the semantics' initial configuration, executes `#loadAll` on the exact
`solution.mpy` module, resolves and calls the resulting `sum_product` closure,
executes the function body, and returns

```k
tuple(vCons(sumFrom(VS, 0),
      vCons(productFrom(VS, 1), .ValSeq)))
```

`sumFrom` and `productFrom` are recursive left folds. Their empty equations
give `0` and `1`, respectively, and their step equations add or multiply the
next integer. Thus the result is the tuple containing the mathematical sum and
product required by `prompt.py`.

# Formal claims

- `SPEC.loop-invariant` covers an arbitrary recursive `ValSeq` suffix at the
  exact recurring `#loop` head. It keeps the continuation, environment,
  original `numbers` value, outer scopes, heap, stack, return state, exception
  state, and exit code framed. It updates only the loop local `number` and the
  `total` and `product` accumulators.
- `SPEC.sum-product` is the full entry theorem. It includes the exact
  `ImportFrom`, `FuncDef`, function body, module binding, call, frame lifecycle,
  loop, return, and final configuration.

The invariant obligations are:

1. Base: `.ValSeq` performs no body step, so `sumFrom(.ValSeq,S) = S` and
   `productFrom(.ValSeq,P) = P`.
2. Step: one fixed-semantics iteration binds the head, performs the two exact
   `AugAssign` statements, and reuses the circularity on the arbitrary tail.
   The accumulator-form fold equations make the resulting values identical.
3. Entry: the entry claim executes the first iteration directly because the
   `number` local does not yet exist, then applies the recurring invariant.

# Proof-extension inventory

There are no rules that intercept a program call, replace the function body,
skip the loop, return a summary, pop a frame, or alter control/state. There are
no trusted external primitives in the proof-local theory.

All term-level helpers below match only their displayed term. They have no
continuation, control-stack, binding, or state-cell match and read/write no
configuration cells.

| Extension | Class and complete domain | Value/control role and justification | Dependents and validation |
|---|---|---|---|
| `allInts(.ValSeq) => true`; `allInts(vCons(V,VS)) => isInt(V) andBool allInts(VS)` | Definitional summary over all `ValSeq`. The base/constructor cases are disjoint, exhaustive, and recursive descent is strict. | Defines the exact K-`Int` element domain. It affects only claim preconditions and does not replace execution. | Both claims. Empty, nonempty, signed, zero, and exhaustive differential witnesses are realizable. |
| `definedProjectInt(V) => isInt(V)` | Definitional summary over every `Val`. | Names exactly the generated sort predicate used as the projection-definedness guard. No state/control effect. | Projection rules and both claims. |
| `#Ceil({@V:Val}:>Int) => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V))` | Derived lemma over every partial `Val`-to-`Int` cast. | Standard definedness characterization: the subsort cast is defined exactly on `Int` inhabitants. | Projection orientation; checked by successful symbolic proof and ground integer collapse. |
| `projectIntTotal(V) => {V}:>Int` under `definedProjectInt(V)` and the reverse symbolic orientation | Derived orientation pair on exactly the `isInt` domain; both rules carry `preserves-definedness`. | Relates the total projection symbol to K's built-in partial subsort cast. It cannot produce a value when the guard is false. The two directions state one equality and affect no control/state. | Dispatch twins and fold summaries. The `[2,3]` negative probe reaches the fixed value `(5,6)`, rejecting an opposite sum. |
| `projectIntTotal(I:Int) => I` and `projectIntTotal(projectIntTotal(V)) => projectIntTotal(V)` | Derived simplifications. The first is the entire static `Int` domain; the second is globally valid because the inner result has sort `Int`. | Fixes every projected integer to that same integer and makes repeated projection idempotent. | Dispatch twins and summaries. Ground LLVM and CPython evidence includes positive, negative, zero, and large integers. |
| Guarded `applyBin("+",V,W)` twin | Derived lemma under exactly `isInt(V) andBool isInt(W)`. | Restates the supplied `MPY-INT` equation `applyBin("+", I1:Int, I2:Int) => I1 +Int I2` after guarded projection. Its overlap with the original static rule has the same RHS after projection collapse. It affects accumulator values only, not control or state matching. | Loop and entry claims. `spec-vacuity.k` exercises addition on `[2,3]` and exposes the actual sum `5`. |
| Guarded `applyBin("*",V,W)` twin | Derived lemma under exactly `isInt(V) andBool isInt(W)`. | Restates the supplied `MPY-INT` multiplication equation. Its overlap with the original rule agrees after projection collapse. It affects accumulator values only. | Loop and entry claims. The same probe exposes product `6`; LLVM smoke covers signs and zero. |
| `sumFrom` base and constructor equations | Definitional summary over all `(ValSeq,Int)` pairs; disjoint/exhaustive constructors and strict tail descent. Its HumanEval meaning is asserted only under `allInts`. | Exact left fold `A := A + head`; result-bearing in the invariant and final postcondition, but it does not replace execution. | Both claims. The fixed execution is connected one iteration at a time by the loop claim; the independent oracle found zero mismatches. |
| `productFrom` base and constructor equations | Definitional summary over all `(ValSeq,Int)` pairs; disjoint/exhaustive constructors and strict tail descent. Its HumanEval meaning is asserted only under `allInts`. | Exact left fold `A := A * head`, with empty identity `1`; it does not replace execution. | Both claims. Connected by fixed loop execution; body and postcondition mutations are rejected. |
| `SPEC.loop-invariant` | Derived reachability/circularity claim under `allInts(VS)`. | Complete matched context: exact `#loop(list(VS), Name("number"), BODY)` with the exact two-statement body; arbitrary suffix preserved by the `<k> ... </k>` frame; environment `L`; exact plain function scope containing only `numbers`, `number`, `total`, and `product`, with parent `0`; arbitrary outer scopes and all omitted cells preserved. It reads the iterator and locals, writes only `number`, `total`, and `product`, and introduces no abrupt control. | `SPEC.sum-product`. It is proved as a claim by the same all-claims `kprove` run; body and false-result probes reject changed behavior. |

The target `SPEC.sum-product` claim is not used as an axiom or helper. It is the
theorem closed by fixed semantics, the proved loop circularity, and the
classified term-level equations above.

# Reproducible commands and actual results

The complete transcript is `prove.log`. The delivered runner was executed as:

```bash
./prove.sh > prove.log 2>&1
```

Actual exit: `0`.

The commands in `prove.sh` include:

```bash
python3 py2mpy.py solution.py > solution.mpy
cmp solution.mpy <(python3 py2mpy.py solution.py)
```

Actual result: exit `0`; the checked-in `solution.mpy` is exactly reproducible
from `solution.py`.

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition semantics-kompiled
krun smoke.mpy --definition semantics-kompiled
```

Actual exit: `0`. Relevant final bindings were:

```text
empty_result   = tuple(0, 1)
example_result = tuple(10, 24)
signed_result  = tuple(-3, 24)
zero_result    = tuple(99, 0)
```

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output: `#Top`. Actual exit: `0`. This single required target-proof
command proves every claim in `SPEC`, including the unbounded entry theorem.
Compiler warnings in the transcript concern unused variables in the supplied
`reference-semantics/semantics/str.k` and unused framed locals in `spec.k`; they
are not stuck claims or proof failures.

```bash
python3 test_solution.py
```

Actual output:

```text
checked=19611 mismatches=0
```

The independent oracle is CPython's built-in `sum` plus `math.prod`, not the K
fold equations. The complete finite sample is every list of length 0 through 5
over `[-3,3]`, plus three large-integer cases.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Expected and actual exit: `1`. The residual contains the fixed result
`tuple(5,6)` and rejects the deliberately false `tuple(6,6)`.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Expected and actual exit: `1`. With `product` initialized to `2`, the residual
contains `tuple(0,2)` and rejects the contract result `tuple(0,1)`.

# Gate results

## Gate A — PASS

- A1: The exact module, closure binding, arguments, body, and return execute
  under the fixed semantics. No program-defined operation is replaced. The
  body mutation changes the observed result and invalidates the claim.
- A2: No operational bridge skips state. The loop claim's exact state
  footprint and preserved cells are recorded above.
- A3: Module loading, LEGB lookup, left-to-right argument evaluation, loop
  target binding, both assignments, return, and frame pop all execute under the
  supplied rules. The invariant preserves its arbitrary continuation rather
  than discarding or unwinding it.
- A4: Total definitions have exhaustive disjoint constructors or a single
  complete equation. Projection use is guarded by definedness. Overlaps of the
  dispatch twins with the supplied static rules agree. Recursive helpers
  descend structurally.
- A5: `.ValSeq` and `[2,3]` are realizable inputs. The false-postcondition
  mutation and body-sensitivity mutation both fail with the expected concrete
  residuals.

## Gate B — PASS

- Input domain: every arbitrary finite `ValSeq` satisfying `allInts`; this is
  exactly the prompt's arbitrary finite list of integers, not a bounded set of
  sizes or examples.
- Postcondition: a two-element tuple containing the recursive mathematical sum
  and product, with empty identities `0` and `1`.
- The implementation matches the prompt and examples.
- K `Int` and Python `int` both model unbounded mathematical integers for these
  operations. The theorem uses the semantics' read-only bare-list claim
  representation; the implementation does not mutate its input, so this has no
  observable difference.

## Gate C — PASS

- Every proof-local symbol, equation, simplification, and auxiliary claim is
  inventoried above.
- All cited artifacts exist and all exact commands and outcomes are preserved
  in `prove.sh` and `prove.log`.
- Positive concrete evidence, an independent differential oracle, a
  false-postcondition probe, and an implementation-body mutation are recorded.
- Formal, trusted, empirical, and excluded facts are separated below.

# Trust boundary

- The theorem is relative to the supplied read-only K semantics and trusts the
  K toolchain, Haskell backend, SMT reasoning, K integer/map/list hooks,
  generated sort predicate `isInt`, and K's subsort-cast definedness.
- The fixed `py2mpy.py` translator is outside the reachability theorem.
  Reproducible translation, direct inspection of `solution.mpy`, LLVM execution,
  and CPython differential testing provide evidence for this boundary.
- `prompt.py`, `py2mpy.py`, and every file under `reference-semantics/` were
  left unchanged.
- There is no proof-local trusted primitive and no unproved
  program-result oracle.

# Empirically supported facts

- LLVM execution under the required `MPY-KRUN` module agrees with the prompt
  examples and signed/zero cases.
- CPython execution agrees with an independent standard-library oracle on
  19,611 documented inputs.
- These finite observations support the translator/model adequacy boundary;
  they are not used as a substitute for the unbounded symbolic K theorem.

# Excluded behavior

- As specified by the prompt, the theorem excludes list elements that are not
  semantic integers (including K `Bool`, floats, strings, and nested lists).
- The K result is a partial-correctness theorem: it establishes the returned
  value whenever execution terminates; a separate liveness theorem is not
  claimed.
- Python features outside the supplied subset, annotation evaluation details,
  and behavior of unrelated builtins are outside this theorem. The ignored
  `typing` import and annotations do not affect the function on the stated
  domain.

The `VALIDATED` headline is the proof-quality result from Gates A/B/C. The
runner's `KPROVE_PASSED` marker separately reports that the required positive
target-proof command printed `#Top`, exited `0`, and Gate B covers the full
HumanEval contract.
