VALIDATED

## What is proven

Under the supplied MPY semantics, the translated `median` function executes by
normal name lookup, argument evaluation, frame creation, assignments, calls to
`sorted` and `len`, parity branching, indexing, arithmetic, return, and frame
pop. No rule intercepts or summarizes the program-defined call.

Let `S = sortVS(VS)` and `L = vsLen(S)`.

- For every symbolic finite `VS:ValSeq` with `L > 0` and
  `pyMod(L, 2) == 1`, `median(list(VS))` returns
  `valSeqAt(S, (L - 1) / 2)`.
- For every symbolic finite `VS:ValSeq` with `L > 0` and
  `pyMod(L, 2) == 0`, the nine even claims cover every ordered pair of center
  types from `Int`, `Bool`, and `Float`. They return the supplied semantics'
  exact Python numeric average: Bool-to-Int promotion, addition, then true
  division.
- The proof is unbounded in list length. `VS`, the initial heap `HP`, and the
  fresh allocation location `HL` remain symbolic.
- The final configuration preserves the environment, module binding, scope
  allocator, stack, return state, exception state, and exit code. It adds
  exactly the newly allocated sorted list at `HL` and advances `heapLoc` once.

The odd claim is structural over every MPY `Val` class. The even claims cover
exactly the MPY value classes for which addition followed by division by the
integer `2` is defined. Empty lists, incomparable inputs, and even nonnumeric
lists do not return a median in Python and are not positive-result cases.

## Formal claims

`spec.k` contains ten target claims:

1. `median-odd`
2. `median-even-int-int`
3. `median-even-int-bool`
4. `median-even-bool-int`
5. `median-even-bool-bool`
6. `median-even-float-float`
7. `median-even-int-float`
8. `median-even-float-int`
9. `median-even-bool-float`
10. `median-even-float-bool`

Every claim starts with the exact global binding
`"median" |-> solutionMedianClosure`, an exact empty continuation, and explicit
initial operational cells. The unboxed `list(VS)` argument is the supplied
semantics' documented representation for read-only list inputs. The function
does not mutate `l`.

The preconditions are realizable. For example, `[3, 1, 2, 4, 5]` instantiates
the odd claim and returns `3`; `[-10, 4, 6, 1000, 10, 20]` instantiates the
Int/Int even claim and returns `8.0`.

## Proof-extension inventory

There are no operational bridges, simplification lemmas, loop circularities,
result oracles, or program-call interception rules in `verification.k`,
`program.k`, or `spec.k`.

The sole proof-local equation is:

```k
syntax Val ::= "solutionMedianClosure" [function, total]
rule solutionMedianClosure => closureVal("l", <exact translated body>, 0)
```

- Extension: `solutionMedianClosure` and its one equation in `program.k`.
- Class: definitional summary.
- Semantic role: names the exact closure value; it does not replace execution.
- Domain: the nullary symbol's single possible application.
- Matched context: any pure occurrence of that nullary value; it matches no
  `<k>`, continuation, control, binding, or state cell.
- Justification scope: `generate_program_k.py` invokes the supplied
  `py2mpy.py` emitter on the sole `median` function in `solution.py`, checks the
  function name and one-argument capture-free signature, and emits its exact
  parameter and statement body.
- Context containment: the definition is context-independent pure expansion,
  so every match has the same exact closure value.
- State footprint: reads, writes, preserves, and abstracts no state.
- Value influence: supplies the closure selected by normal lookup; thereafter
  the fixed semantics executes its body and determines control, allocation,
  return value, and final cells.
- Value justification: complete defining equation generated from the same AST
  emitter that creates `solution.mpy`.
- Justification: syntactic naming only; one exhaustive, terminating equation
  with no overlap.
- Dependents: all ten target claims.
- Control validation: `spec-body-mutation.k` executes a regenerated closure
  whose odd return is changed to `0`; it is rejected and its residual contains
  `<k> 0 ~> .K </k>`.
- Value validation: `spec-vacuity.k` changes the realizable odd witness's
  required result from `3` to `4`; it is rejected and its residual contains
  `<k> 3 ~> .K </k>`.
- Validation: Gate A checks A1 through A5 pass.

The ten declarations in `spec.k` are target reachability claims, not equations
or assumptions used to make other claims close.

## Exact commands and actual results

Tool versions:

```text
kompile: K version v7.1.293
kprove:  K version v7.1.293
```

The complete reproducible command sequence is in `prove.sh`. Its positive proof
commands are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 generate_program_k.py solution.py > program.k

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
krun differential-smoke.mpy \
  --definition runtime-kompiled \
  --output none

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual results:

- The aggregate target `kprove` command printed exactly `#Top` and exited `0`;
  this is preserved in `target-proof.log`.
- The resumed validation reran that aggregate command against the preserved
  Haskell definition; it again printed `#Top` and exited `0`, as preserved in
  `resume-target-proof.log`.
- `krun smoke.mpy` exited `0` with `<k> .K </k>`, `<exc> NoExc </exc>`, and
  `<exit-code> 0 </exit-code>`; the configuration is in `smoke-krun.log`.
- The 221-case differential MPY program exited `0`.
- The supplied compiler emitted warnings about unrelated partial helpers and
  unused variables; none was an error and none changed these results.

Negative audit commands:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kompile --backend haskell verification-mutant.k \
  --main-module VERIFICATION-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-mutant-kompiled
kprove spec-body-mutation.k \
  --definition verification-mutant-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Both negative probes exited `1` as expected. `vacuity.log` records the real
result `3` failing to unify with false postcondition `4`; `body-mutation.log`
records mutant result `0` failing to unify with correct postcondition `3`.
The resumed validation repeated both probes with the same exit codes and
residual values in `resume-vacuity.log` and `resume-body-mutation.log`.

## Gate A — PASS

- A1: `solutionMedianClosure` is generated from the actual source AST. Normal
  fixed-semantics invocation executes its exact binding and body. The
  body-sensitivity mutation is rejected.
- A2: there is no operational bridge. The claims explicitly track the one sort
  allocation and preserve every active state cell.
- A3: lookup, argument evaluation, builtin dispatch, indexing order, branch,
  return, and frame pop all execute under fixed semantics with an exact empty
  continuation.
- A4: the one proof-local function is nullary, total, terminating, exhaustive,
  and has no overlapping equations.
- A5: the concrete odd witness is satisfiable. The false result mutation is
  rejected with the actual result visible in the residual.

## Gate B — PASS

The theorem is structural and unbounded, not a fixed-size unrolling. Odd sizes
cover arbitrary MPY values. The nine even claims exhaust the Cartesian product
of MPY numeric classes `Int`, `Bool`, and `Float`, which are the represented
classes on which the source's center addition and division are defined.

The source contract says “median,” so the conventional definition controls.
The second worked example is internally inconsistent: sorting its input gives
`[-10, 4, 6, 10, 20, 1000]`, whose center average is `(6 + 10) / 2 = 8.0`, not
`15.0`. Following the Kit rule for a self-contradicted example, the definition
wins. The divergence is preserved in `smoke.py`, `domain_checks.py`, and the
differential suite; it does not narrow the theorem.

`domain-checks.log` records:

```text
odd_strings b
prompt_even 8.0
empty IndexError
even_strings TypeError
incomparable TypeError
```

Thus empty input and input combinations for which the specified Python
computation raises are contract-inherent undefined cases, not silently replaced
answers.

Model boundaries, rather than candidate restrictions:

- Python user-defined comparable/arithmetic objects and other value kinds not
  represented by MPY remain outside the fixed model.
- MPY's concrete sorter implements numeric and string cases; the universal odd
  structural claim is conditional on the supplied `sortVS` contract for any
  other comparable represented value.
- String construction in the supplied semantics is ASCII-oriented; broader
  Python Unicode behavior is a fixed-model boundary.
- Float value facts, including non-finite and rounding-edge behavior not covered
  by the finite tests, remain conditional on the supplied opaque float
  primitives.

No list length, example set, or bounded unrolling restricts the formal claims.

## Gate C — PASS

### Trust ledger

| Component | Boundary and influence | Dependents | Evidence |
|---|---|---|---|
| Supplied `sortVS` and `vsLen(sortVS(VS))` | Trusted fixed `sorted` primitive: ascending permutation, stability, and length preservation. It affects parity control, selected indexes, result, and the allocated sorted list. | All ten claims | Fixed semantics source; six-case LLVM smoke run; 221-case differential run. Universal correctness is conditional, not inferred from tests. |
| Supplied `valSeqAt(sortVS(VS), I)` | Trusted total indexing of the opaque sorted sequence at an in-bounds median index. It affects the returned value and even arithmetic operands. | All ten claims | Fixed semantics source and the same concrete/differential runs. |
| Supplied `divII`, `addF`, `intToF`, and `divFloatIntV` | Opaque fixed numeric primitives under `kprove`; claims thread their exact terms and make numeric meaning conditional on their contracts. They affect even results, not control. | The nine even claims as applicable | LLVM execution plus the 221-case CPython differential suite, including mixed Int/Bool/Float and large integer cases. |
| K implementation, SMT reasoning, and supplied MPY rules | Trusted verification platform and fixed semantics. | All claims | Successful clean recompilation, concrete execution, positive proof, and discriminating negative probes. |
| Supplied `py2mpy.py` | Trusted pure AST transliteration boundary. It determines the closure syntax but adds no semantics. | All claims | `solution.mpy` and `program.k` are regenerated on every `prove.sh` run; body mutation changes the generated closure and invalidates the claim. |

### Reproducible finite evidence

- `generate_differential.py` uses CPython's independently implemented
  `statistics.median` as oracle. It exhausts small integer tuples through
  length 3, small float and mixed numeric tuples through length 2, and adds the
  prompt examples and large-integer boundaries: 221 cases total, zero CPython
  mismatches. It then emits literal expected-result assertions for LLVM MPY
  execution, which exits `0`.
- `smoke.py` checks odd/even integers, Bool, mixed numeric, Float, and odd
  strings under LLVM.
- `spec-vacuity.k` and `spec-body-mutation.k` are persistent expected-failure
  artifacts with their full residual logs.

Finite evidence supports the named supplied primitives and adequacy bridge; it
is not presented as a universal proof. The universal structural facts are the
ten `#Top` reachability claims.

## Result-language separation

- Formally established: exact fixed-semantics execution and result structure
  for the ten unbounded claims, including final operational state.
- Conditional: interpreting opaque `sortVS`, opaque indexing over it, and
  opaque float terms as their stated Python operations.
- Empirically supported: those supplied primitives on the 221 differential
  cases and six smoke cases.
- Excluded as undefined: empty lists, incomparable inputs, and even
  nonnumeric inputs that raise under the source computation.
- Fixed-model boundaries: unrepresented Python objects, broader Unicode, and
  untested float edge behavior.
