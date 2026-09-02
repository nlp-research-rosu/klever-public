VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact translated body of
`sort_third` has been proved partially correct for a symbolic `VS:ValSeq`.
`ValSeq` is the semantics' inductive representation of an arbitrary finite
list; no length bound, fixed size, example enumeration, or loop-unrolling
bound is in the target claim.

Starting from the initial module configuration, the `SPEC.sort-third` claim:

1. loads the exact `sort_third` closure;
2. resolves and calls that closure with `list(VS)`;
3. executes slicing, `sorted`, all allocations, the loop, indexing,
   `append`, return, and frame cleanup using the fixed reference semantics;
4. returns `ref(2)`, whose heap value is `list(sortThirdResult(VS))`.

`sortThirdResult(VS)` is definitionally the sequence formed by:

- taking `buildVS(VS, 0, vsLen(VS), 3)`;
- applying the supplied `sortVS` primitive to that sequence;
- traversing every index `I` from `0` through `vsLen(VS) - 1`;
- taking item `I / 3` from that sorted sequence when `I % 3 == 0`, and
  taking item `I` from `VS` otherwise.

Thus every non-third position is unchanged, while the positions divisible by
three receive, in order, the sorted values originally at those positions.
The ordering/permutation meaning of `sortVS` is the named trust boundary
provided by the reference semantics and audited below.

The proof is a partial-correctness proof. It does not separately prove a
liveness theorem.

## Formal claims

`SPEC.loop-invariant` is an unbounded circularity. At a loop head with
`0 <= I <= N`, `N == vsLen(VS)`, an arbitrary already-produced prefix `A`,
and the actual `l`, `thirds`, `result`, and `i` bindings, it proves:

```text
i becomes N
result becomes A ++ mergeThirdFrom(VS, SV, I, N)
```

The invariant pins the function-to-module-to-builtins scope chain and requires
that the module scope does not shadow `len`. It frames the active continuation
without discarding it.

`SPEC.sort-third` is the target entry claim. It is quantified over
`VS:ValSeq` with no domain-strengthening `requires` clause. Its initial heap is
empty. Its final heap records all three exact allocations:

```text
0 |-> list(buildVS(VS, 0, vsLen(VS), 3))
1 |-> list(sortVS(buildVS(VS, 0, vsLen(VS), 3)))
2 |-> list(sortThirdResult(VS))
```

The initial and final environment, scope location, stack, return state,
exception state, and exit code are also constrained.

The claims must be proved together so that `SPEC.sort-third` can consume
`SPEC.loop-invariant` as its circularity. Filtering the target claim alone
would remove that proof dependency.

## Proof-extension inventory

### `mergeThirdFrom`

| Field | Record |
|---|---|
| Extension | Three exhaustive equations for `mergeThirdFrom(VS, SV, I, N)` |
| Class | Definitional summary |
| Semantic role | Names the mathematical suffix produced by remaining loop iterations; it does not rewrite an MPY program term |
| Domain | All `ValSeq` values and all integers. `I >= N` is the base case; `I < N` is split disjointly by `pyMod(I, 3) == 0` and `=/= 0` |
| Matched context | A pure summary term only; no continuation, binding, control, or configuration cell is matched |
| Justification scope | Exactly the complete term domain above |
| Context containment | Equality of the match and justification domains; there are no frames or omitted cells |
| State footprint | None |
| Value influence | Determines the final list suffix in both claims |
| Value justification | Base/step recursion mirrors the program's branch and advances `I` by one; `N - I` strictly decreases on recursive cases |
| Justification | Direct structural definition of the intended merge |
| Dependents | `SPEC.loop-invariant`, `sortThirdResult`, and `SPEC.sort-third` |
| Control validation | Not applicable: no execution is replaced |
| Value validation | The two prompt examples, concrete K cases, and the 895-case independent differential test agree |
| Validation | Coverage and disjointness audited; recursive descent holds whenever a recursive rule applies |

### `sortThirdResult`

| Field | Record |
|---|---|
| Extension | Opaque total symbol, the folding equation from the complete `mergeThirdFrom` term, and the guarded zero-length equation |
| Class | Definitional summary |
| Semantic role | Solver-friendly name for the complete result; it does not rewrite source execution |
| Domain | All `VS:ValSeq`; the zero rule is guarded by `vsLen(VS) <= 0` |
| Matched context | Summary terms only |
| Justification scope | The folding equation fixes the value to the exact complete merge for every `VS` |
| Context containment | Exact pure-term match; no operational context exists |
| State footprint | None |
| Value influence | Names the final returned heap sequence |
| Value justification | Universal folding equation; `vsLen(VS) <= 0` implies `VS == .ValSeq` because `vsLen` is zero at `.ValSeq` and adds one at every constructor |
| Justification | Definitional abbreviation. The folding orientation prevents eager unbounded unfolding but does not weaken the equation |
| Dependents | `SPEC.sort-third` |
| Control validation | Not applicable |
| Value validation | The false empty-result claim for input `[1]` is rejected with the actual result `[1]` |
| Validation | The zero case agrees with the universal complete-result definition |

### `valSeqConcat` lemmas

| Field | Record |
|---|---|
| Extension | Associativity and right identity simplification rules |
| Class | Derived lemmas |
| Semantic role | Normalize accumulator expressions after fixed `append` execution |
| Domain | All `A`, `B`, and `C` of sort `ValSeq` |
| Matched context | Pure `valSeqConcat` terms only |
| Justification scope | Complete stated domain |
| Context containment | Exact pure-term matches |
| State footprint | None |
| Value influence | Permits the loop accumulator to match the invariant result |
| Value justification | Structural induction on `A` using MPY-LIST's two exhaustive `valSeqConcat` equations |
| Justification | Standard associativity and `A ++ [] = A` derivations |
| Dependents | `SPEC.loop-invariant` and transitively `SPEC.sort-third` |
| Control validation | Not applicable |
| Value validation | Concrete empty, singleton, and multi-element K executions |
| Validation | No guards or overlapping competing right-hand sides |

### `SPEC.loop-invariant`

| Field | Record |
|---|---|
| Extension | Reachability circularity at the exact `#while` loop head |
| Class | Derived lemma |
| Semantic role | Summarizes repeated fixed-semantics execution after proving the base and inductive branches |
| Domain | `0 <= I <= N`, `N == vsLen(VS)`, exact local bindings and heap objects, fixed parent chain, and no module-level `len` shadow |
| Matched context | Exact loop condition and body, arbitrary preserved continuation, current environment, module/builtin scopes, result and sorted-list heap entries |
| Justification scope | The same framed loop-head configurations quantified by the claim |
| Context containment | The continuation is preserved as the same K frame; the claim introduces no return, pop, exception, break, or continuation discard |
| State footprint | Reads `l`, `thirds`, `result`, `i`, the module/builtin scopes, and two heap entries; writes only `i` and the result list; all other cells are framed unchanged |
| Value influence | Determines every appended element and the final result |
| Value justification | Fixed semantics executes lookup, arithmetic, branch selection, indexing, append, and increment before circularity reuse |
| Justification | `kprove` closes both base and inductive paths with `#Top` |
| Dependents | `SPEC.sort-third` |
| Control validation | The `% 3` to `% 2` body mutation produces `<exit-code> 1` on a realizable witness |
| Value validation | The false-postcondition mutation is rejected |
| Validation | Focused invariant proof prints `#Top`, exit 0 |

### Supplied `sortVS`

| Field | Record |
|---|---|
| Extension | `sortVS` and the supplied `sorted(list)` allocation rule in `reference-semantics/semantics/sort.k` |
| Class | Trusted primitive from the fixed reference semantics |
| Semantic role | Represents the ascending sort performed by Python's `sorted`; concrete LLVM rules insertion-sort integer and string sequences |
| Domain | Symbolic `ValSeq` in the formal theorem; concrete homogeneous integer and string sequences in the supplied LLVM rules |
| Matched context | The supplied `#applyK(toCall(builtinV("sorted")), ...)` continuation and heap allocation context |
| Justification scope | Named external contract: `sortVS(VS)` is the ascending permutation returned by `sorted(list(VS))` for normally sortable inputs |
| Context containment | This is part of the fixed supplied semantics, not a proof-local bridge; the theorem is conditional on that declared primitive contract |
| State footprint | Reads the argument sequence; allocates one fresh list and increments `heapLoc`; no other state is changed |
| Value influence | Supplies all result values at indices divisible by three |
| Value justification | Named reference-semantics trust boundary plus concrete insertion-sort rules for integer/string witnesses |
| Justification | Explicit trust declared in the supplied semantics; it is intentionally outside this task's theorem |
| Dependents | Both formal claims and the human-facing ordering conclusion |
| Control validation | Concrete K execution reaches normal completion and the expected allocation/result state |
| Value validation | Seven K assertions include integer and string sorting; the two prompt examples pass; Python differential testing reports 895 cases and zero mismatches |
| Validation | Recorded as conditional trust, not misreported as a K proof of sorting |

No proof-local operational bridge, priority rule, source-call interception, or
fresh result oracle is present.

## Exact commands and actual outputs

The complete executable record is `./prove.sh`. Its final run exited 0.
Important commands and their actual outcomes were:

```bash
python3 py2mpy.py solution.py > solution.mpy
# Exit: 0

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# Exit: 0 (supplied-semantics warnings only)

krun concrete_test.mpy --definition runtime-kompiled
# <exit-code> 0; process exit 0

python3 differential_test.py
# differential: 895 cases, 0 mismatches
# Exit: 0

krun body_mutation_test.mpy --definition runtime-kompiled
# <exit-code> 1; process exit 1 (expected)

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# Exit: 0 (supplied-semantics unused-variable warnings only)

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
# #Top
# Exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# #Top
# Exit: 0

kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# WarnStuckClaimState
# Actual result heap: 2 |-> list(vCons(1, .ValSeq))
# Mutated target heap: 2 |-> list(.ValSeq)
# Exit: 1 (expected)
```

K tool versions used:

```text
K version: v7.1.293
Build date: Fri Oct 03 13:32:35 CDT 2025
```

The LLVM compiler emitted pre-existing non-exhaustiveness warnings in unrelated
supplied helpers and the documented total `valSeqAt` catch case. The Haskell
compiler emitted only pre-existing unused-variable warnings in the supplied
string semantics. Neither build failed.

## Gate results

### Gate A — PASS

- **A1:** The target claim begins at module loading and an exact named call.
  The exact body from `solution.mpy` executes; it is not replaced by a summary
  rule. Regeneration is the first command in `prove.sh`. The `% 3` to `% 2`
  source-body mutation is rejected by concrete K execution.
- **A2:** The claim records the slice, sorted-list, and result allocations,
  `heapLoc`, scope cleanup, stack, return state, exception state, and exit code.
  The loop claim writes only `i` and the result heap object.
- **A3:** Lookup, argument evaluation, builtin resolution, indexing, append,
  branch control, return, and frame pop are all executed by fixed semantics.
  The loop claim pins the parent chain and excludes a shadowing module `len`.
  Its arbitrary continuation is preserved rather than discarded.
- **A4:** `mergeThirdFrom` has complete disjoint guards and a decreasing
  recursion measure. `sortThirdResult` is fixed by its universal folding
  equation. The concatenation lemmas are valid structural inductions. There
  are no inconsistent overlapping equations.
- **A5:** `VS = vCons(1, .ValSeq)` is a realizable witness. The deliberate
  empty-result mutation exits 1 with a residual showing the actual `[1]`
  result.

### Gate B — PASS

- **B1:** The entry theorem covers a symbolic arbitrary finite `ValSeq`; it has
  no size bound or finite unrolling restriction. For the normal-return contract,
  the selected values must be mutually sortable, which is already implicit in
  the prompt's use of “sorted”.
- **B2:** The supplied model uses mathematical integers and an opaque symbolic
  sort. Concrete LLVM evidence covers homogeneous integer and string lists.
  Python values with comparison side effects or exceptional heterogeneous
  comparisons are outside the material HumanEval normal-return domain.
- **B3:** The execution-to-merge characterization is formally proved. The
  statement that `sortVS` is Python's ascending sorted permutation is explicitly
  conditional on the supplied primitive contract and supported empirically; it
  is not claimed as a theorem derived in this K proof.
- **B4:** The implementation agrees with the prompt examples and the
  independent slice-assignment oracle.

### Gate C — PASS

- Every proof-local function, equation, simplification lemma, and circularity is
  inventoried above.
- The fixed-semantics and `sortVS` trust boundaries and all dependent claims are
  named.
- `concrete_test.py`, `differential_test.py`,
  `body_mutation_test.py`, `spec-vacuity.k`, and their recorded output files
  exist. `prove.sh` regenerates and reruns all evidence.
- Formal facts, conditional trust, empirical evidence, and exclusions are
  separated in this report.

## Trust boundary

The proof is conditional on:

1. K v7.1.293, its Haskell backend, and the SMT reasoning it invokes;
2. the supplied, read-only `reference-semantics/` definition as the intended
   Python subset;
3. `py2mpy.py` as the AST-to-constructor transliterator;
4. the supplied `sortVS` contract for normally sortable values.

Only item 4 directly determines the ordering of result values. The remaining
program control and list-position logic is proved by fixed-semantics execution.

## Empirically supported facts

- `concrete_test.py`: seven K assertions, including both prompt examples,
  empty/singleton/boundary lengths, negative integers, and strings; zero
  assertion failures.
- `differential_test.py`: 895 deterministic cases. The independent oracle uses
  Python slice assignment (`expected[::3] = sorted(source[::3])`), not the K
  summary equations; zero mismatches.
- `body_mutation_test.py`: changing divisibility from three to two changes the
  behavior and is rejected (`<exit-code> 1`).
- `spec-vacuity.k`: changing the singleton result to empty is rejected by
  `kprove` (exit 1).

These finite results support the trust and adequacy audit; they are not used as
a substitute for the symbolic unbounded proof.

## Excluded behavior

- A separate termination/liveness theorem is not claimed.
- Exceptional calls to `sorted` on values that Python cannot mutually compare
  are outside the prompt's normal-return contract.
- User-defined comparison methods, comparison side effects, concurrency, and
  external state are not represented by the supplied Python subset.
- The claim observes the returned sequence and all task-relevant allocation and
  control cells; it does not claim CPython object identity or performance.
