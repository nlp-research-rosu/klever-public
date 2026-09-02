VALIDATED

## What is proven

Under the supplied MPY semantics, both claims execute the exact `sort_array`
closure body through the name binding in the module scope.

- For the empty input list at heap address 0, the call returns a fresh empty
  list at address 1.
- For every nonempty finite list of non-negative integers, the call returns a
  fresh list at address 1 whose contents are
  `condRev(sortVS(input), even(first + last))`.
- The original list at address 0 is unchanged. The final environment, scopes,
  call stack, return state, exception state, and exit code are also constrained.

This is a partial-correctness result. The value-level statement that `sortVS`
is an ascending sort is conditional on the named trusted primitive contract in
the supplied reference semantics. `condRev` is defined there: an odd endpoint
sum leaves the ascending sequence unchanged, while an even sum reverses it.

## Formal claims

`SPEC.empty` covers `[]`.

`SPEC.nonempty` represents an integer list as
`intVals(iCons(F, IS))`. Its precondition is:

```k
F >=Int 0
andBool nonNegative(IS)
andBool valSeqAt(
  vCons(F, intVals(IS)),
  vsLen(intVals(IS))) ==K L:Int
```

Thus `F` is the first element, `L` is the actual final element obtained by the
fixed subscript functions, and every element is non-negative. The destination
heap contains:

```k
0 |-> list(intVals(iCons(F, IS)))
1 |-> list(
  condRev(
    sortVS(intVals(iCons(F, IS))),
    pyMod(F +Int L, 2) ==Int 0))
```

The empty and nonempty claims exhaust the prompt's list domain.

## Proof-extension inventory

### `intVals`

| Field | Record |
|---|---|
| Extension | `intVals(.IntSeq) => .ValSeq`; `intVals(iCons(I, IS)) => vCons(I, intVals(IS))` |
| Class | Definitional summary |
| Semantic role | Encodes an `IntSeq` as the corresponding `ValSeq`; it does not replace program execution |
| Domain | Every `IntSeq` |
| Matched context | Pure function terms only; no continuation, binding, control, or configuration cells |
| Justification scope | Exactly the two constructors of `IntSeq` |
| Context containment | The equations match only their constructor cases, which are the complete justification domain |
| State footprint | None |
| Value influence | Determines the symbolic input sequence, the sequence supplied to `sortVS`, and the preserved input heap value |
| Value justification | Exhaustive constructor-preserving equations |
| Justification | Structural definition of embedding integer sequences into value sequences |
| Dependents | `SPEC.nonempty` and `nonNegative`'s domain interpretation |
| Control validation | Not applicable: no execution or control is replaced |
| Value validation | Cases generated from the exact `solution.py` source pass both CPython and MPY/LLVM |
| Validation | Equations are disjoint, exhaustive, and recursively descend on `IS` |

### `nonNegative`

| Field | Record |
|---|---|
| Extension | `nonNegative(.IntSeq) => true`; recursive `iCons` equation |
| Class | Definitional summary |
| Semantic role | States the input-domain predicate; it does not rewrite program execution |
| Domain | Every `IntSeq` |
| Matched context | Pure predicate terms only; no continuation or cells |
| Justification scope | Exactly the two constructors of `IntSeq` |
| Context containment | Match and justification domains coincide |
| State footprint | None |
| Value influence | Restricts the theorem to the prompt's non-negative inputs |
| Value justification | Empty conjunction is true; the recursive case checks the head and tail |
| Justification | Structural definition of elementwise non-negativity |
| Dependents | The precondition of `SPEC.nonempty` |
| Control validation | Not applicable |
| Value validation | All 344 differential cases satisfy the intended generated domain |
| Validation | Equations are disjoint, exhaustive, and recursively descend on `IS` |

There are no proof-local operational rewrites, simplification lemmas,
auxiliary claims, opaque result oracles, or rules that bypass the function
body. `SPEC.empty` and `SPEC.nonempty` are the target theorems, not imported
execution rules.

### Imported trusted primitive: `sortVS`

| Field | Record |
|---|---|
| Extension | Supplied `MPY-SORT.sortVS(ValSeq)` and the fixed `sorted` call rule |
| Class | Trusted primitive in the supplied semantics |
| Semantic role | Gives the value of Python's ascending `sorted`; the fixed call rule still performs argument evaluation and fresh allocation |
| Domain | Integer lists for this theorem |
| Matched context | The supplied `#applyK(toCall(builtinV("sorted")), ...)` rules, with the active continuation framed by the fixed semantics |
| Justification scope | Named reference-semantics contract: `sortVS` is the ascending sort of its input |
| Context containment | No task-local rule broadens the supplied rule's match context |
| State footprint | `sortVS` is pure; the supplied call rule updates `<k>`, `<heap>`, and `<heapLoc>` to allocate the result |
| Value influence | Determines the order and permutation of the returned list |
| Value justification | Explicit external contract in `reference-semantics/semantics/sort.k`; symbolic evaluation is intentionally opaque |
| Justification | Trusted semantics boundary, independently exercised by the LLVM concrete insertion-sort implementation |
| Dependents | Both target claims; value opacity is material in `SPEC.nonempty` |
| Control validation | Fixed execution is used; the theorem constrains normal return, allocation, preserved input, stack, exception, and exit state |
| Value validation | 344 LLVM-vs-CPython cases, zero mismatches or K assertion failures |
| Validation | Trust is explicit and conditional; finite evidence does not claim universal sort correctness |

## Commands and actual outputs

The complete reproducible command sequence is in `prove.sh`. The recorded run
is `prove-run.out`; `./prove.sh` exited 0.

```bash
python3 py2mpy.py solution.py > solution.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun solution.mpy --definition runtime-kompiled
python3 differential_test.py
```

Actual differential output:

```text
differential: 344 cases, CPython mismatches=0, MPY assertion failures=0
```

The 344 cases comprise every list of length 0 through 4 over values 0 through
3, plus the unique additional prompt examples. Each K batch is generated from
the exact current `solution.py` source.

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.empty
# Output: #Top
# Exit: 0

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.nonempty
# Output: #Top
# Exit: 0

kprove spec.k --definition verification-kompiled --spec-module SPEC
# Output: #Top
# Exit: 0
```

The builds exited 0. They emitted only warnings originating in the supplied
reference semantics (non-exhaustive concrete helper matches and unused
variables in `str.k`), not task-definition errors.

### Negative validation probes

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# Output includes: WarnStuckClaimState
# Exit: 1 (expected)
```

For the satisfiable witness `[0, 1]`, the actual result in the residual is
`[0, 1]`, while the deliberately false destination demands `[1, 0]`.

```bash
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# Output includes: WarnStuckClaimState
# Exit: 1 (expected)
```

The mutation changes the nonempty body to `reverse=True`. Its residual returns
`[1, 0]` for witness `[0, 1]`, so the original ascending postcondition is
rejected. Full residuals are preserved in `vacuity.out` and
`body-mutation.out`.

## Gate results

### Gate A — PASS

- A1: The target claims execute the exact translated body under a scope that
  pins `sort_array` to that closure and retains the normal builtin lookup
  chain. The material body mutation fails.
- A2: There is no task-local operational bridge. The claims constrain the
  original and result heap objects, fresh heap location, environment, scopes,
  stack, return state, exception state, and exit code.
- A3: Name lookup, left-to-right arguments, endpoint subscripts, modulo,
  comparison, keyword tagging, call/return control, and allocation all execute
  under the fixed semantics.
- A4: Both proof-local functions have disjoint, exhaustive constructor cases
  and strict recursive descent. No overlapping or off-domain equations exist.
- A5: Empty and `[0, 1]` are realizable witnesses. The false-result mutation is
  rejected with a concrete result mismatch.

### Gate B — PASS

- B1: The theorem domain is exactly finite lists of non-negative integers,
  split into empty and nonempty cases.
- B2: MPY integers are unbounded like Python integers for the operations used.
  The reference semantics intentionally abstracts symbolic sorting through
  `sortVS`; exceptions and unsupported Python values are outside the domain.
- B3: The theorem formally proves the wrapper, parity choice, fresh copy, and
  non-mutation. Ascending-sort meaning is conditional on the named `sortVS`
  contract and is empirically supported, not re-described as a K theorem.
- B4: The implementation matches the prompt and all supplied examples.

### Gate C — PASS

- C1: The trust ledger above names `sortVS`, its value influence, dependents,
  and evidence. The supplied MPY semantics, K backends, and translator are also
  part of the ordinary verification-tool trust base.
- C2: All positive proofs, concrete tests, the false-result probe, and the body
  mutation have existing artifacts, exact commands, actual outcomes, and
  preserved output.
- C3: Formal facts, the conditional sort contract, finite evidence, and
  excluded behavior are separated throughout this report.

## Trust boundary

The proof trusts the supplied reference semantics and K toolchain. In
particular, it trusts the symbolic contract that `sortVS` denotes ascending
sorting. The task-local proof does not add a rule for ordering or permutation.
The LLVM implementation and CPython oracle provide finite independent evidence
for that contract over the recorded sample.

The supplied `prompt.py`, `py2mpy.py`, and `reference-semantics/` files were not
modified.

## Empirically supported facts

- All four prompt examples pass in CPython.
- Across 344 documented inputs, `solution.py` matches the independent CPython
  oracle, preserves its input list, and returns a distinct Python list.
- The exact same source, translated to MPY in batches, produces zero assertion
  failures under LLVM.
- The two negative K probes fail for their intended semantic mismatch.

These finite results support the semantics and intent bridge; they do not
replace the universal K reachability claims or universally prove `sortVS`.

## Excluded behavior

- Negative elements, non-integer elements, non-list inputs, and exceptional
  calls are outside the prompt-aligned formal domain.
- The theorem is partial correctness and does not separately prove
  termination, resource bounds, or CPython implementation details.
- Universal ordering/permutation correctness of `sortVS` is a named trusted
  primitive contract, not a theorem proved in `spec.k`.
