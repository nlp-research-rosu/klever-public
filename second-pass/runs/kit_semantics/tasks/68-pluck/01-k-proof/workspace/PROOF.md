VALIDATED

## What is proven

The theorem proves partial correctness of `pluck` for every finite list whose
elements are non-negative integers. There is no fixed list-size bound in the K
claim. Empty lists are included.

From an initial call to the exact translated function body, the final result is:

- `[]` when the input contains no even value; or
- `[value, index]`, where `value` is the smallest even input value and `index`
  is its first occurrence.

The theorem also constrains normal function-call completion: the call frame is
popped, the result list is allocated in the initially empty heap, `ret` is
`noRet`, `exc` is `NoExc`, and the exit code remains zero.

This is a reachability/partial-correctness result. It does not separately claim
a liveness theorem, although every concrete finite contract-domain list follows
the structurally decreasing iterator.

## Formal claim

`SPEC.pluck-entry` in `spec.k` starts with:

```k
Call(Name("pluck"), list(INPUT:ValSeq))
```

The module scope pins `"pluck"` to a closure containing the exact body in
`solution.mpy`. Its precondition is:

```k
allNonNegative(INPUT)
```

The destination heap contains:

```k
resultList(
  scanBest(INPUT, 0, -1),
  scanBestIndex(INPUT, 0, -1, 0))
```

The recursive equations have the following meaning:

- `shouldTake(B,V)` is true exactly when `V` is even and either no value has
  been selected (`B < 0`) or `V` is strictly smaller than `B`.
- `nextBest` and `nextBestIndex` perform one source-loop update.
- `scanBest` and `scanBestIndex` fold that update over the complete symbolic
  list while incrementing the source index.
- strict comparison preserves the earlier index on equal values.
- `resultList` maps the negative sentinel to `[]` and a selected pair to
  `[value,index]`.

`SPEC.pluck-loop` is the unbounded circularity. At a nonempty symbolic loop
head it executes one exact source iteration and relates the final locals to the
recursive scans over the complete remaining suffix. The frozen list iterator
handles the empty base case. Its recursive use handles arbitrary finite tails.

The fold-to-contract argument is a structural induction. Initially the sentinel
means no even prefix element has been seen. An odd element preserves the
selection; the first even element replaces the sentinel; a strictly smaller
even element replaces the selection; and every other element, including an
equal even value, preserves it. Therefore after every prefix, the accumulator
is either empty or contains the smallest even prefix value and its least index.

## Proof-extension inventory

No ordinary rule in `verification.k` rewrites a `<k>` computation, call,
return, loop, continuation, scope, heap, stack, exception, or other operational
cell. There is no operational bridge and no trusted result oracle.

### Guarded integer projection

Extensions:

- `definedProjectInt`
- `projectIntTotal`
- the `#Ceil` characterization, guarded cast-orientation pair, static-`Int`
  collapse, and idempotence rule

Class: definitional total projection plus derived cast lemmas.

Semantic role and match domain: these are pure terms, not operational
configurations. `definedProjectInt(V)` is exactly `isInt(V)`. Orientation from
`Val` to `Int` is guarded by that predicate; the reverse orientation has the
same guard and `preserves-definedness`; the collapse rule applies only to an
already statically sorted `Int`.

Justification scope and containment: K's partial subsort cast is defined
exactly on values satisfying `isInt`. The `#Ceil` rule records that domain, and
the orientation rules identify the total twin with the partial cast only
inside it. Every target use is guarded by `allNonNegative`, which entails
`definedProjectInt` for each iterated head.

State footprint: none.

Value influence: the projected integer is assigned by the source statement
`value = value + 0`, then affects parity, comparison, accumulator locals, and
the result.

Value justification and validation: under the guard the projection is the
built-in cast, and on a statically known integer it collapses to that integer.
Frozen LLVM execution evaluates the same normalization on all concrete tests.
The body mutation and false-result mutation are both rejected.

### Guarded addition dispatch twin

Extension:

```k
rule applyBin("+", V:Val, I:Int)
  => projectIntTotal(V) +Int I
  requires definedProjectInt(V)
  [simplification]
```

Class: derived lemma.

Semantic role: it restates the frozen rule
`applyBin("+", I1:Int, I2:Int) => I1 +Int I2` over a dynamically sorted first
operand. It simplifies a pure operator term and does not skip lookup,
evaluation, control, or state changes.

Complete domain and context: exactly an `applyBin("+", Val, Int)` term under
`isInt(Val)`. There is no continuation or configuration-cell frame in its
match. The cast connection above makes this domain equal to the original
static-`Int` domain.

State footprint: none.

Value influence: it makes the source's integer identity normalization
statically visible; all later source operations execute using the frozen
integer rules.

Dependents: `SPEC.pluck-loop` and `SPEC.pluck-entry`.

Validation: LLVM smoke execution imports no proof extension and passes; the
Haskell target proof passes with the twin; changing the program's selecting
comparison to the opposite comparison produces `[4,0]` for `[4,2,3]` and is
rejected by `spec-body-mutation.k`.

### Domain and result summaries

Extensions:

- `allNonNegative`
- `shouldTake`
- `nextBest`
- `nextBestIndex`
- `scanBest`
- `scanBestIndex`
- `afterIndex`
- `resultList`

Class: definitional summaries.

Semantic role: they name the input domain and the mathematical values threaded
through the invariant; none replaces source execution.

Complete domains: the sequence functions have exhaustive empty/cons equations.
`nextBest` and `nextBestIndex` have complementary `shouldTake` and
`notBool shouldTake` guards. `resultList` has disjoint, exhaustive `B < 0` and
`B >= 0` guards. All recursion is on a structurally smaller `ValSeq`.

Matched context and state footprint: pure terms only; no cells are read,
written, preserved, or abstracted.

Value influence: these functions define the loop post-state and final output
expected by both target claims.

Justification: their equations are the source loop's base and step equations.
The loop circularity executes the body and establishes the connection between
those equations and the actual locals. The strict replacement rule supplies
the least-index tie behavior.

Dependents: both target claims.

Validation: the full proof, the rejected off-by-one postcondition, the rejected
body mutation, six frozen-semantics smoke cases, and 56,491 independent
differential cases.

### Reachability claims

`SPEC.pluck-loop` is a derived loop-invariant circularity. Its matched context
contains the exact loop body, arbitrary trailing `<k>` continuation, active
environment, and the exact local scope. The loop has no abrupt control,
allocation, exception, or external-state effect; omitted configuration cells
are preserved. It changes only `value`, `smallest`, `smallest_index`, and
`index`; `arr` is preserved. The focused proof printed `#Top`.

`SPEC.pluck-entry` is the target theorem. It pins the exact closure binding,
executes name lookup, argument evaluation, frame creation, parameter binding,
the body, both return branches, result allocation, and frame removal. No rule
summarizes or bypasses that execution.

## Commands and actual outputs

The complete reproducible command is:

```bash
./prove.sh
```

The captured run is `prove-run.out`. The script exited 0.

Important constituent commands and actual results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
# Exit: 0

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# Exit: 0

krun smoke.mpy --definition runtime-kompiled
# Exit: 0; final <k> .K </k>, <exc> NoExc </exc>, <exit-code> 0

python3 test_solution.py
# Exit: 0
# differential-tests: 56491 cases, 0 mismatches

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.pluck-loop
# Output: #Top
# Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# Output: #Top
# Exit: 0

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# Exit: 1 (expected)
# WarnStuckClaimState: demanded computed_index + 1 == computed_index

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# Exit: 1 (expected)
# Residual heap contained [4,0], not [2,1]
```

The compiler also printed pre-existing unused-variable warnings from
`reference-semantics/semantics/str.k`; they did not affect any exit status.

## Gate A — PASS

A1: the entry claim contains the exact `solution.mpy` closure body and executes
it. The binding is pinned in module scope. Concrete `smoke.mpy` also exercises
normal module definition loading. The selecting-comparison mutation is rejected
and exposes the changed `[4,0]` result.

A2: there is no operational bridge. Fixed semantics performs the call, loop,
assignments, branches, return, allocation, and frame lifecycle. The loop claim
frames only cells the loop does not modify.

A3: name lookup is pinned to the exact closure, argument evaluation is explicit,
the guarded dispatch domain equals the frozen integer-addition domain, and no
continuation or control effect is replaced.

A4: definitional equations are exhaustive on every target use; guarded cases
are complementary or disjoint; recursion structurally descends. The projection
rules are guarded by cast definedness.

A5: `[0]` is a satisfiable contract-domain witness and should return `[0,0]`.
The off-by-one-index mutation is rejected with exit 1. The body mutation on
`[4,2,3]` is also rejected with the concrete wrong result visible.

## Gate B — PASS

B1: `INPUT:ValSeq` is symbolic and unbounded. `allNonNegative` recursively
covers every finite list of non-negative integer values. The theorem is not a
finite collection of sizes or examples. It includes the prompt's empty-list
case and is stronger than the stated maximum length of 10,000.

B2: the fixed model uses mathematical integers and algebraic finite lists. The
prompt's nodes are explicitly non-negative integers, so non-integers and the
semantics' distinct `Bool` sort are outside the source contract. Within that
domain, `value + 0` is an integer identity and no modeled exceptional behavior
is suppressed.

B3: program execution is formally connected to the recursive scan by the loop
circularity. The scan-to-human-property bridge is the structural induction
given above and is independently supported by the differential oracle.

B4: the implementation returns the required smallest even value and preserves
the first index on ties.

## Gate C — PASS

Trust boundary:

- the supplied read-only MPY semantics and its K builtin theories;
- the installed K compiler/prover and Haskell/LLVM backends;
- standard reachability-logic partial-correctness interpretation;
- the guarded total-projection cast laws recorded explicitly in
  `verification.k`.

There is no target-dependent trusted primitive, opaque external function,
program-result oracle, or operational bridge.

Reproducible evidence:

- `smoke.py`/`smoke.mpy`: the four prompt examples plus an equal-value tie and
  a no-even case, evaluated by the frozen LLVM semantics;
- `test_solution.py`: an independently written `min((value,index), ...)`
  oracle; exhaustive values `0..5` for lengths `0..6`, 500 deterministic
  random lists, and four length-10,000 lists; 56,491 cases, zero mismatches;
- `spec-vacuity.k`: symbolic off-by-one postcondition, rejected;
- `spec-body-mutation.k`: concrete opposite-comparison implementation,
  rejected with `[4,0]`.

Excluded behavior:

- lists containing negative or non-integer nodes, as excluded by the prompt;
- behavior beyond the supplied MPY subset or its exception model;
- a separate proof of termination or complexity;
- arbitrary ambient heaps/aliases: the HumanEval entry is modeled with the
  semantics' documented unboxed read-only list input and an initially empty
  result heap.
