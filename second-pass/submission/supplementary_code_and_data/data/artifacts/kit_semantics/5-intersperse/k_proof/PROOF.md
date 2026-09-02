VALIDATED

# What is proven

Under the supplied `MPY` symbolic semantics, every terminating call to the
exact `intersperse` closure in `solution.py`, with a semantic list
`list(INPUT)` and an integer delimiter `D`, returns `ref(0)`.  Heap location
`0` contains `list(intersperseAcc(.ValSeq, INPUT, D))`; the call restores the
module environment and stack, leaves `NoExc`, and advances the fresh heap
location from `0` to `1`.

This is a partial-correctness theorem.  Termination and behavior outside the
supplied semantics are not claimed.

# Formal claims

`spec.k` contains two claims:

- `SPEC.loop-invariant` executes the fixed `#loop` semantics from an exact
  reachable plain function frame with a nonempty accumulated output.  It
  proves that the result-list heap entry becomes
  `intersperseAcc(vCons(A, AS), REST, D)`.
- `SPEC.intersperse-correct` starts from an exact invocation configuration:
  `Name("intersperse")` is bound to a closure containing the translated body,
  the input is `list(INPUT)`, and `D` is an `Int`.  It proves the returned
  reference and final heap sequence stated above.

The whole-program proof discharges the empty-input base case directly.  On a
nonempty input it executes the first iteration, reaches the invariant's exact
nonempty-accumulator configuration, and applies the circularity.

# Proof-extension inventory

## `INTERSPERSE-BODY`

- **Class:** definitional summary in the limited sense of a compile-time syntax
  abbreviation; it emits no runtime KORE rewrite.
- **Semantic role:** names, but does not replace, the exact `Stmts` tree in
  `solution.mpy`.
- **Domain and matched context:** occurrences of the literal token where a
  `Stmts` value is expected; macro expansion is complete before execution.
- **Justification scope and containment:** the expansion is the two statements
  in the translated `For` body, including the empty `else` branch.  Both the
  closure and invariant use the same expanded tree.
- **State footprint and value influence:** none as a macro.  The expanded fixed
  semantics reads `result`, `delimeter`, and `number`, and mutates only the list
  at the heap location bound to `result`.
- **Dependents:** both claims.
- **Validation:** `solution.mpy` is regenerated from the fixed translator.  The
  body-sensitivity probe materially changes the second append and is rejected.

## `intersperseAcc`

- **Class:** definitional summary.
- **Semantic role:** post-state mathematical characterization only.  It never
  appears at the head of program execution and replaces no fixed-semantics
  step.
- **Domain:** all `ACC:ValSeq`, `REST:ValSeq`, and `D:Val` values.
- **Matched context:** only applications of the summary function.  No control,
  stack, binding, or configuration cell is matched.
- **Equations:** empty `REST` returns `ACC`; an empty `ACC` with nonempty
  `REST` appends the first element without a delimiter; a nonempty `ACC` with
  nonempty `REST` appends `D` and then the next element.
- **Coverage, overlap, and descent:** the three constructor cases are exhaustive
  and pairwise disjoint.  Every recursive equation consumes one constructor
  from `REST`, so recursion terminates.
- **State footprint:** none.  Its value determines the postcondition's output
  sequence.
- **Value justification:** these equations are a direct recursive definition of
  inserting no delimiter before the first input and exactly one delimiter
  before every later input.  Their nested concatenation mirrors the supplied
  semantics' two successive `append` heap updates.
- **Dependents:** both claims.
- **Validation:** the invariant proof connects each equation to fixed execution;
  concrete and differential evidence is recorded below.

## `SPEC.loop-invariant`

- **Class:** derived lemma used coinductively as a loop circularity.
- **Semantic role:** executes the fixed `#loop`, lookup, binding, `if`, call,
  `append`, expression-discard, and loop-control rules.  It is not an
  operational bridge.
- **Domain:** every `REST:ValSeq`, integer `D`, nonempty accumulator
  `vCons(A, AS)`, exact local bindings for `numbers`, `delimeter`, `number`, and
  `result`, parent scope `0`, and the framed heap/scopes/continuation admitted
  by the claim.
- **Matched context and containment:** the complete loop term is fixed; the
  continuation is universally framed by the claim itself.  The body has no
  return, break, continue, or exception-producing rule on this well-formed
  domain, so fixed execution preserves the suffix until the loop finishes.
  The exact local map excludes impossible closure-cell branches.
- **State footprint:** reads the four local bindings and result heap entry;
  updates `number` and the list at `H`; preserves environment, parent binding,
  other scopes and heap entries, heap allocator, stack, return, exception, and
  exit cells.
- **Value influence:** the heap sequence is the target theorem's returned list.
  `intersperseAcc` fixes it through exhaustive equations.
- **Justification and dependents:** machine-checked fixed-semantics base and
  inductive cases; used by `SPEC.intersperse-correct`.
- **Control/value validation:** the unfiltered positive proof closes, the LLVM
  runs terminate normally, the wrong-body probe is rejected, and the false
  postcondition is rejected.

There are no task-local operational bridges, trusted primitives, opaque
result-bearing symbols, simplification lemmas, priority rules, or concrete-only
proof rules.

# Reproducible commands and actual results

The complete workflow is in `prove.sh`.  The material commands actually run
were:

```sh
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 differential_test.py
# cases=19530 mismatches=0; exit 0

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# exit 0 (the supplied definition emits non-exhaustiveness/unused-variable warnings)

krun concrete-tests.mpy --definition runtime-kompiled
# exit 0; .K, NoExc, exit-code 0
# empty_result    -> []
# singleton_result -> [1]
# example_result  -> [1, 4, 2, 4, 3]

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# exit 0 (unused-variable warnings originate in the supplied semantics)

kprove spec.k --definition verification-kompiled --spec-module SPEC
# #Top; exit 0

kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# WarnStuckClaimState; exit 1
# actual heap [4], required original result [1]

kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# WarnStuckClaimState; exit 1
# actual heap [1, 4, 2], deliberately required [1, 4, 2, 4]
```

# Gate results

## Gate A — PASS

- **A1:** the exact program closure, binding, body, arguments, frame lifecycle,
  and loop execute under fixed semantics.  The wrong-body ground mutation is
  rejected with the changed value visible in the residual heap.
- **A2/A3:** there is no operational bridge.  The claims constrain the returned
  reference, result heap, allocator, environment, stack, return state,
  exception state, and exit code.  The invariant uses the exact reachable
  local frame and actual continuation framing.
- **A4:** `intersperseAcc` is exhaustive, disjoint, truthful, and structurally
  decreasing.  No globally false lemma or opaque oracle is present.
- **A5:** `[1, 2]` with delimiter `4` is a realizable witness.  Requiring the
  false result `[1, 4, 2, 4]` is rejected and exposes the actual result
  `[1, 4, 2]`.

## Gate B — PASS

- **Input alignment:** the source `List[int]`/`int` domain is included.  The
  theorem is stronger for elements: `INPUT` may contain any supplied-semantics
  `Val`, while the delimiter remains an `Int`.
- **Language model:** the theorem uses the supplied MPY list, integer, scope,
  heap, function, and control model.  Python integers and MPY integers are
  unbounded for the exercised operations.  Input identity and mutation are not
  observable in this contract; the result value is fully constrained.
- **Summary/property:** from an empty accumulator the equations return `[]` for
  empty input, emit the first element without a delimiter, and emit exactly one
  delimiter before each subsequent element.  This is the prompt's requested
  insertion property and matches both examples.
- **Implementation alignment:** no implementation/contract discrepancy was
  found.

## Gate C — PASS

- **Trust ledger:** the trusted foundation is the supplied read-only MPY
  semantics, K's reachability prover/backend, and the fixed CPython-AST
  translator.  No task-local primitive or unproved value oracle is trusted.
- **Reproducible evidence:** all artifacts and commands above exist.  LLVM
  concretely executes the boundary and prompt cases.  The two negative K probes
  have the expected nonzero results and informative residuals.
- **Differential evidence:** `differential_test.py` compares `solution.py` with
  an independently written index-based oracle over every list of length 0
  through 5 drawn from `{-2,-1,0,1,2}` and every delimiter in that set: 19,530
  cases, zero mismatches.  This is finite validation evidence, not a universal
  proof.

# Trust boundary and exclusions

Formally established facts are conditional on the supplied MPY semantics and
K prover.  The fixed translator supplies the AST identity.  LLVM execution and
the differential oracle are empirical evidence only.  The proof does not
establish termination, CPython behaviors omitted by MPY, behavior for a
non-integer delimiter, allocation identity beyond the stated initial
configuration, or properties unrelated to the returned list.
