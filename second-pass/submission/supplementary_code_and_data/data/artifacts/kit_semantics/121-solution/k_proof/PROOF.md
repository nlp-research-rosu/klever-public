VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact translated body of
`solution.py` is partially correct for every non-empty finite list whose
elements are K integers. Starting from the standard empty module state, the
claim loads the `solution` definition, resolves and calls that binding, executes
the initialization and return machinery, and produces

```k
oddAtEvenSum(vCons(HEAD, TAIL), 0)
```

where `oddAtEvenSum` adds exactly those integer elements whose zero-based
position is even and whose value is odd. There is no bound on `TAIL`, list
length, or integer magnitude.

The proof is a partial-correctness proof, as specified by the Kit workflow. It
does not assert a separate total-correctness or complexity theorem.

## Formal claims

The target claim is `SPEC.solution` in `spec.k`:

```text
allInts(vCons(HEAD, TAIL))
  implies
solution(list(vCons(HEAD, TAIL)))
  => oddAtEvenSum(vCons(HEAD, TAIL), 0)
```

Its initial and final configuration cells additionally require:

- module loading of the exact `FuncDef` translated from `solution.py`;
- normal function lookup, argument binding, frame creation, return, and pop;
- empty heap and stack at the external boundary;
- `NoExc` and exit code `0`; and
- preservation of the installed `solution` closure in module scope.

`CONNECTION-SPEC.loop` is the bridge-free universal loop theorem. For any
integer-only remaining sequence, nonnegative current position, current
accumulator, loop-target value, enclosing scope, and continuation, it proves:

- `position` becomes `POSITION +Int vsLen(REST)`;
- `result` becomes
  `ACC +Int oddAtEvenSum(REST, POSITION)`;
- `value` becomes `lastAfter(REST, CURRENT)`;
- the loop computation is consumed; and
- the continuation, environment, `lst`, parent scope, outer scopes, and every
  omitted configuration cell are preserved.

## Proof-extension inventory

### Pure definitions and derived refinement rules

All entries in this subsection have no state footprint and do not replace a
program statement, call, binding, continuation, exception, or configuration
transition.

| Extension | Class | Complete domain and equations | Value influence and justification | Dependents and validation |
|---|---|---|---|---|
| `allInts` | Definitional summary | All `ValSeq`; `.ValSeq` and `vCons` equations are constructor-disjoint and exhaustive; recursion is on the tail. | Fixes the exact target input domain. It is true exactly when each represented element satisfies the fixed sort predicate `isInt`. | Guards the loop theorem, bridge, and target claim. The unbounded connection and target claims both print `#Top`. |
| `definedProjectInt`, `projectIntTotal`, the `#Ceil` characterization, cast orientation, collapse, and idempotence rules | Derived refinement/definitional projection | All `Val`; every cast orientation is guarded by `definedProjectInt(V) = isInt(V)`. The projection is used only where that guard is entailed. On an `Int`, the cast and collapse rules agree; idempotence agrees on overlaps. | Refines a dynamically sorted semantic `Val` to its existing integer value. The partial-cast orientation and `#Ceil` rule connect it to K's sort cast; it does not manufacture a fresh value. | Used by the dispatch twins and mathematical sum. `PROJECTION-POSITIVE` prints `#Top` for `5` and `-7`; `PROJECTION-MUTATION` rejects `5 => 6` with exit `1`. |
| Guarded `applyBin("%", V:Val, I:Int)` twin | Derived lemma | Guard `isInt(V)`; RHS is `pyMod(projectIntTotal(V), I)`. | Restates the fixed `MPY-INT` modulo equation over the dynamic supersort after guarded projection. It affects the oddness branch but reads/writes no cells. | Used by the bridge-free loop proof. Ground projection collapse agrees with fixed integer execution; the false projection interpretation is rejected. |
| Guarded `applyBin("+", I:Int, V:Val)` twin | Derived lemma | Guard `isInt(V)`; RHS is `I +Int projectIntTotal(V)`. | Restates the fixed `MPY-INT` addition equation over the dynamic supersort. It fixes the accumulator value without changing evaluation order or state behavior. | Used by the bridge-free loop proof. The concrete K run includes positive and negative selected values with no assertion failures. |
| `oddContribution` | Definitional summary | All pairs of K integers. The two guards are a Boolean condition and its negation, so they are disjoint and exhaustive. | Returns the value exactly when the position is even and the value is odd under Python's fixed `pyMod(_, 2)` behavior; otherwise returns zero. | Defines the intended mathematical property used by `oddAtEvenSum`. Differential testing includes negative integers. |
| `oddAtEvenSum` | Definitional summary | All `ValSeq` and positions. Empty/cons cases are disjoint; cons cases split on `isInt(V)` and its negation; recursion is on the tail. | On the guarded target domain it is exactly the contract sum. The non-integer branch only totalizes the helper outside the target domain and is never used to admit a target input. | Appears in the loop theorem, bridge, and target postcondition. The bridge-free loop theorem and target theorem both print `#Top`. |
| `lastAfter` | Definitional summary | All `ValSeq × Val`; empty/cons cases are constructor-disjoint and exhaustive; recursion is on the tail. | Describes the final loop-target local solely so the loop connection preserves every written local. It does not affect the returned result. | Used only by the loop theorem and its exact bridge. |

For these pure terms, the matched context is the displayed function or cast
term in any expression context; the justification scope is the same complete
term domain. Context containment is therefore immediate, and control
validation is not applicable.

### Loop connection claim

- Extension: `CONNECTION-SPEC.loop`.
- Class: auxiliary reachability theorem / loop-invariant circularity.
- Semantic role: executes the exact fixed-semantics `#loop`; it is not an
  operational rule in `verification-base.k`.
- Domain: arbitrary finite `REST:ValSeq` satisfying `allInts(REST)`, arbitrary
  `POSITION >=Int 0`, accumulator, current target value, `lst`, environment,
  parent scope, outer scopes, continuation, and omitted cells.
- Matched context: the exact loop syntax from `solution.mpy`, with an arbitrary
  framed `<k>` continuation. The local scope contains exactly `lst`,
  `position`, `result`, and `value`; outer scopes and other cells are framed.
- State footprint: reads the remaining list and three current locals; writes
  `position`, `result`, and `value`; preserves `lst`, environment, parent and
  outer scopes, continuation, heap, stack, return, exception, exit, allocation,
  and all other omitted cells.
- Value justification: the loop is symbolically executed with the fixed rules.
  Its recursive step uses the guarded integer twins; its result follows the
  structurally recursive definitions.
- Validation: bridge-free compilation plus `kprove connection-spec.k ...`
  prints `#Top` and exits `0`.

### Loop operational bridge

- Extension: the priority-40 rule in `verification.k`.
- Class: operational bridge.
- Semantic role: replaces only the exact loop computation already established
  by `CONNECTION-SPEC.loop`.
- Domain and matched context: identical term, local scope, frames, and guards
  to the bridge-free connection theorem. The arbitrary continuation and
  omitted cells are present with the same generality in both artifacts.
- Context containment: every bridge match is a connection-theorem match; the
  bridge has no weaker guard, extra wildcard, broader continuation, abrupt
  return, frame pop, or omitted state not also framed by the theorem.
- State footprint: identical to the connection theorem. It updates only
  `position`, `result`, and `value`; all other cells and the continuation are
  preserved.
- Value influence: it supplies the accumulator value subsequently returned by
  the actual fixed return/pop rules.
- Value justification: the bridge-free universal `#Top` connection theorem.
- Dependents: `SPEC.solution`.
- Priority: `priority(40)` preempts the fixed one-step loop rule only inside the
  proved match domain, preventing an otherwise redundant unbounded proof-search
  branch.
- Control validation: the theorem quantifies over the same arbitrary
  continuation. The mutated subtraction body is rejected both without and with
  the bridge; the latter ends with `result = -1`, demonstrating that the bridge
  does not match or discard the changed computation.
- Value validation: concrete K assertions, exhaustive differential tests, the
  off-by-one mutation, and projection probes described below.

## Exact commands and actual outputs

All commands are recorded in `prove.sh`. A complete run was executed as:

```bash
./prove.sh > prove.out 2>&1
```

Actual result: exit `0`.

Concrete execution:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual `krun` result: exit `0`, `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`.

Bridge-free positive proof:

```bash
kompile --backend haskell verification-base.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kprove connection-spec.k \
  --definition verification-base-kompiled \
  --spec-module CONNECTION-SPEC
```

Actual output: `#Top`. Exit: `0`.

Target positive proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output: `#Top`. Exit: `0`.

Supporting projection proof:

```bash
kprove projection-positive.k \
  --definition verification-base-kompiled \
  --spec-module PROJECTION-POSITIVE
```

Actual output: `#Top`. Exit: `0`.

Negative probes:

- `kprove spec-vacuity.k --definition verification-kompiled --spec-module
  SPEC-VACUITY` exited `1`; the residual requires the impossible equality
  `SUM +Int 1 ==Int SUM`.
- `kprove connection-mutation.k --definition
  verification-base-kompiled --spec-module CONNECTION-MUTATION` exited `1`;
  the grounded mutated subtraction body ended with `result = -1`, not `1`.
- The same mutation command with `--definition verification-kompiled` exited
  `1` with the same `result = -1`, showing the loop bridge does not match the
  mutated body.
- `kprove projection-mutation.k --definition
  verification-base-kompiled --spec-module PROJECTION-MUTATION` exited `1`;
  the residual contains `5`, not the false destination `6`.

The supplied semantics emits unrelated unused-variable and non-exhaustive
compiler warnings. They did not change any exit status or positive `#Top`
result.

## Gate results

### Gate A — PASS

- A1: `spec.k` loads, binds, and calls the exact translated function body.
  Program initialization, lookup, call, return, and frame behavior execute under
  the fixed semantics. The only operational bridge has an independent
  bridge-free universal connection theorem.
- A2: the bridge theorem and rule have identical state footprints and preserve
  the arbitrary continuation plus all omitted cells.
- A3: the bridge begins only at the post-binding semantic `#loop`; it does not
  intercept function lookup, argument evaluation, target binding, condition
  evaluation, return, or pop. Its continuation scope is identical to the
  theorem's.
- A4: all total definitions have constructor-disjoint or complementary cases,
  structural descent, and agreeing overlaps. Projection and dispatch rules use
  the exact `isInt` guard.
- A5: realizable witnesses include all five K smoke cases. The off-by-one
  postcondition is rejected, as are the body and projection mutations.

### Gate B — PASS

- Input domain: `vCons(HEAD, TAIL)` is exactly non-empty, while
  `allInts(vCons(HEAD, TAIL))` admits every finite semantic list of K integers.
  `TAIL` is symbolic and unbounded.
- Numeric domain: K `Int` is arbitrary precision, matching the material integer
  domain of the HumanEval task.
- Property: `oddAtEvenSum(_, 0)` uses zero-based positions, includes only even
  positions, and includes only values with nonzero Python remainder modulo
  two. Negative odd integers are covered.
- Implementation alignment: the function's counter begins at zero, advances
  once per element, and updates the result exactly under those two tests.

### Gate C — PASS

- Every proof-local symbol and rule is inventoried above.
- The operational bridge has a separately compiled bridge-free connection
  theorem over the same match domain.
- All claimed commands, outputs, mutations, and test artifacts exist and are
  reproduced by `prove.sh`.
- Formal proof facts, trust assumptions, finite evidence, and exclusions are
  separated below.

## Trust boundary

- Trusted fixed input: the supplied read-only `reference-semantics/` definition.
  All theorem conclusions are relative to that semantics.
- Trusted proof engine: K `v7.1.293`, its Haskell backend, and its underlying
  logical decision procedures.
- Trusted front end: the supplied `py2mpy.py` transliterator. `solution.mpy` was
  regenerated from `solution.py` by the required command.
- No proof-local external primitive or unconstrained result-bearing oracle is
  assumed. The guarded projection is connected to K's partial sort cast, and
  the loop bridge is connected to fixed execution by a machine-checked theorem.

## Empirically supported facts

`python3 differential_test.py` compares `solution` with an independent
`enumerate`/generator-expression oracle for every list of length 1 through 5
over values `-3` through `3`.

Actual output:

```text
Differential cases: 19607; mismatches: 0
```

`smoke.py` runs the three prompt examples plus `[-5, 2, -7]` and `[2]` under
the LLVM reference semantics. All assertions complete with `NoExc` and exit
code `0`.

These finite tests support implementation and model adequacy; the universal
result comes from the two positive K proofs, not from testing.

## Excluded behavior

- Empty lists are outside the source contract and the target claim.
- Non-integer elements, including semantic `Bool` values, are outside the
  prompt's stated integer-list domain.
- The theorem uses the supplied semantics' canonical unboxed representation
  for read-only list inputs; heap allocation behavior for list literals is
  exercised separately by the concrete K tests.
- No claim is made for Python constructs or exceptional behaviors absent from
  this program or unsupported by the supplied partial Python semantics.
- No separate termination-rate, resource-use, or complexity theorem is claimed.
