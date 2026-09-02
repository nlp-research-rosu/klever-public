VALIDATED

## What is proven

Under the supplied MPY semantics, the exact `filter_integers` closure in
`solution.mpy` has the following partial-correctness property: for every finite
symbolic `INPUT:ValSeq`, calling it returns a fresh list containing, in original
order, exactly the values for which the fixed semantic function
`isIntV` is true. The fixed semantics defines that class as `Int` plus `Bool`,
matching Python's `bool`-is-an-`int` behavior.

The theorem executes name lookup, function-call setup, parameter binding, list
allocation, iteration, `isinstance`, branching, `append`, return, and frame
cleanup. It is not a bounded-size proof.

## Formal claim

`SPEC.filter-entry` starts with:

```k
Call(Name("filter_integers"), (list(INPUT:ValSeq), .Exprs))
```

in a module scope that binds the name to the exact one-argument closure body.
It ends with `ref(0)`, an otherwise-restored caller configuration, and:

```k
<heap> .Map => 0 |-> list(filterAcc(INPUT, .ValSeq)) </heap>
```

`filterAcc` is a structurally recursive filter over the semantics' own
`.ValSeq` and `vCons` constructors. `SPEC.filter-loop` is the unbounded loop
circularity. It handles an arbitrary remaining `ValSeq` and arbitrary running
accumulator, and its constructor step is discharged by fixed-semantics
execution before the circularity is reapplied.

The formal input has no length bound and no element-type precondition.

## Proof-extension inventory

| Extension | Class and semantic role | Complete domain and matched context | State footprint and value influence | Justification, dependents, and validation |
|---|---|---|---|---|
| `filterBody`, `filterLoopBody` macro equations | Definitional syntax aliases; they do not replace runtime execution | Compile-time occurrences of the two nullary macro symbols; no continuation, binding, or cell is matched | No runtime cells are read or written; expansion fixes the closure and loop syntax used by both claims | Exact transcription of `solution.mpy`; depended on by both claims. LLVM prints the same closure, the Python/K harness function AST is identical, and the removed-loop body mutation fails |
| `isIntV(V) => isInt(V) orBool isBool(V) [simplification]` | Derived lemma; dynamic-to-static dispatch twin for a fixed pure function | Every `V:Val`; context-independent term simplification only | No state or control effect. Its Boolean value affects the program branch and `filterAcc` | Constructor exhaustion of the supplied equations: `Int -> true`, `Bool -> true`, all other `Val` constructors -> false. It agrees on all overlaps. Integer-discarded and string-retained opposite-result probes both fail |
| `filterAcc` base and constructor equations | Definitional summary; names the mathematical result without replacing execution | All pairs `(ValSeq, ValSeq)`. Empty and `vCons` cases are exhaustive; the recursive call strictly descends through `REST` | No operational cells. Its value constrains the returned heap list | The empty case returns the accumulator. The constructor case uses the fixed `isIntV` and either appends the unchanged head or skips it. `SPEC.filter-loop` machine-connects this definition to execution; false-result mutation fails |
| `SPEC.filter-loop` | Derived auxiliary reachability claim and loop circularity | Exact loop head, exact return/`#endcall` suffix, plain function frame, module and builtin bindings, result heap cell, allocator location, stack frame, return/exception/exit cells | Reads the iterated sequence, local bindings, builtin scopes, and result list; writes `value` and the result list, then restores environment, scopes, stack, and return state exactly | Proved by fixed semantic steps plus the definitions above. The entry claim depends on it. Full `kprove` prints `#Top`; the body mutation fails |

There are no operational bridges, priority rules, fresh result oracles,
opaque proof-local values, or trusted proof-local primitives. The fixed
`valSeqConcat` and `isIntV` operations come from the supplied semantics.

## Exact commands and actual outputs

The complete reproducible runner is `./prove.sh`. Its substantive commands are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 differential-test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC

kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
kprove spec-classifier-mutation.k --definition verification-kompiled \
  --spec-module SPEC-CLASSIFIER-MUTATION
kprove spec-noninteger-mutation.k --definition verification-kompiled \
  --spec-module SPEC-NONINTEGER-MUTATION
```

Actual final-run results:

| Command/result | Exit | Actual output |
|---|---:|---|
| `python3 differential-test.py` | 0 | `python differential: 22621 lists, 0 mismatches`; harness and solution ASTs identical |
| LLVM `kompile` | 0 | Completed; warnings identify unrelated non-exhaustive helpers and unused variables in the supplied semantics |
| `krun concrete-tests.mpy` | 0 | Final configuration has `<k> .K </k>`, `<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>` |
| Haskell `kompile` | 0 | Completed; only supplied-semantics unused-variable warnings |
| target `kprove spec.k` | 0 | `#Top` |
| `SPEC-VACUITY` | 1 | `WarnStuckClaimState`; actual empty result conflicts with deliberately expected `[0]` |
| `SPEC-BODY-MUTATION` | 1 | `WarnStuckClaimState`; removed-loop body returns `[]`, not `[1]` |
| `SPEC-CLASSIFIER-MUTATION` | 1 | `WarnStuckClaimState`; actual result is `[1]`, rejecting the opposite integer classification |
| `SPEC-NONINTEGER-MUTATION` | 1 | `WarnStuckClaimState`; actual result is `[]`, rejecting retention of `"x"` |
| complete `./prove.sh` | 0 | All positive checks and all expected-failure checks completed |

The full outputs are preserved in `concrete-tests.krun.out`,
`target.kprove.out`, and the four `*.kprove.out` mutation logs.

## Gate results

### Gate A — PASS

- A1: The scope pins the exact closure body, parameter, defining environment,
  and binding. Program-defined code executes. Removing the loop invalidates the
  proof.
- A2/A3: No execution is bridged. The claims preserve or explicitly constrain
  all active cells, and fixed semantics performs lookup, argument evaluation,
  call/return control, mutation, and cleanup.
- A4: `filterAcc` is total by exhaustive sequence cases and structurally
  descending recursion. The classifier lemma is exactly consistent with all
  supplied `isIntV` equations.
- A5: `[]` is a realizable witness. The deliberately false `[0]` postcondition,
  both opposite classifications, and the changed body are rejected.

### Gate B — PASS

- B1: `INPUT:ValSeq` is arbitrary and unbounded. Every element constructor
  represented by the fixed `Val` sort is admitted; there is no example-only,
  homogeneous, or fixed-length restriction.
- B2: The theorem covers the full value universe represented by the supplied
  semantics. CPython value kinds absent from that semantics, such as
  user-defined classes and arbitrary subclasses, are a fixed-model boundary,
  not a theorem-side narrowing.
- B3: `filterAcc` directly states stable filtering by the supplied
  `isinstance(_, int)` classifier; the loop claim formally connects it to
  execution.
- B4: The implementation agrees with the prompt examples and the independent
  differential oracle.

### Gate C — PASS

Every proof-local extension is inventoried above. Commands, inputs, oracles,
outputs, exit statuses, and mutation residuals are preserved as artifacts.
Formal results, model boundaries, and finite evidence are separated.

## Trust boundary

The proof trusts the supplied read-only reference semantics, `py2mpy.py`, the K
toolchain/backend/solver, and their runtime dependencies. None is re-axiomatized
locally. The classifier simplification is a derived constructor-exhaustive
restatement of fixed equations, not an external assumption.

The theorem is conditional on the MPY model. Python object kinds not represented
by `Val` are outside the formal universe. The differential test includes one
CPython `int` subclass as empirical evidence only.

## Empirically supported facts

- LLVM executed both prompt examples, the empty list, and a mixed
  bool/int/None/float case with no exception.
- The independent Python oracle classifies through each concrete type's MRO,
  not through `isinstance`; it checked all 22,621 lists of lengths 0–4 over a
  12-value pool with zero mismatches.
- The translated concrete harness and `solution.py` contain identical
  `filter_integers` ASTs.
- Finite tests support implementation/model alignment; they are not used as a
  substitute for the unbounded K proof.

## Excluded behavior

- This is a partial-correctness reachability proof, not a separate liveness or
  resource-bound theorem.
- Non-list arguments are outside the annotated HumanEval input contract.
- CPython-only value classes missing from the supplied MPY semantics are outside
  the formal model, as recorded in the trust boundary.
- The entry claim uses the reference semantics' documented bare, read-only list
  input representation and its exact initial caller state; arbitrary preexisting
  external heap or I/O state is not part of this pure function contract.
