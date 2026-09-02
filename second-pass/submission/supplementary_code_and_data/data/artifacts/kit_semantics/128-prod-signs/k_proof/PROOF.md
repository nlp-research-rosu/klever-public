VALIDATED

# What is proven

Under the supplied MPY reference semantics and the audited proof extensions,
`spec.k` proves partial correctness of the exact constructor tree generated for
`solution.py`.

For every finite `INPUT:IntSeq`, `SPEC.prod-signs` loads the translated
`prod_signs` definition, calls it with the read-only integer list
`list(intVals(INPUT))`, and reaches `prodSignsResult(INPUT)` with `NoExc` and
exit code 0. `SPEC.loop-invariant` separately proves the exact loop transition
to `foldResult(REST, TOTAL, SIGN)`.

The result functions state:

- `prodSignsResult(.IntSeq) = noneV`.
- A nonempty input starts `foldResult` with total 0 and sign 1.
- Each fold step adds `absInt(value)` to the total; it negates the sign for a
  negative value, preserves it for a positive value, and sets it to zero for
  zero.
- The final result is `total *Int sign`.

By structural induction on the finite input sequence, this is `None` for the
empty list and otherwise the sum of all magnitudes multiplied by the product
of the element signs, which is the prompt's contract.

# Formal claim

The formal input domain is every finite sequence of mathematical K integers.
There is no bound on integer magnitude. The claim uses the reference
semantics' supported unboxed representation for read-only list inputs.

The postcondition is:

```text
INPUT = []      implies result = None
INPUT nonempty  implies result =
  (sum of abs(value) for value in INPUT)
  * (product of sign(value) for value in INPUT)
```

The whole-program claim also fixes the loaded function body, argument binding,
builtins parent scope, module scope, initial heap and stack, normal return,
absence of exceptions, and exit code.

# Proof-extension inventory

| Extension | Class and domain | Matched context and state footprint | Value/control justification | Dependents and validation |
|---|---|---|---|---|
| `intVals(IntSeq)` and the two materialization rules in `connection.k` | Definitional representation; exhaustive empty/`iCons` cases | Only `#iterNext(list(intVals(...)))` followed by `#loopStep(TARGET,BODY)` and arbitrary `CONT`; all completed configuration cells are preserved | Empty maps to `.ValSeq`; a head integer maps to `vCons(VALUE, intVals(REST))`. This fixes list order and element values structurally | Justifies the typed-iterator connection. `CONNECTION-SPEC` proves empty and symbolic-step cases. Ground values 4 and −2 succeed; interpreting 4 as 5 is rejected |
| The `verification-base.k` iterator rule together with both `#typedNext` rules | Operational bridge over every `IntSeq`, narrowed to a for-loop `#loopStep` continuation | Replaces only the iterator redex in the `<k>` cell, preserves arbitrary `CONT`, and does not mention or modify any other cell | `CONNECTION-SPEC` is a bridge-free universal connection theorem. It imports `CONNECTION`, not `VERIFICATION-BASE`; its structural materialization exposes the represented list to the fixed MPY list iterator | Used by the loop connection and target proof. Both connection claims produce `#Top`; the wrong-value mutation exits 1 |
| `foldResult` equations | Definitional summary for finite `IntSeq`, arbitrary integer `TOTAL` and `SIGN` | Mathematical term only; it does not replace a program redex | Negative, zero, and positive guards are pairwise disjoint and exhaustive for integers. Every equation recurses on `REST`, so it descends structurally. `absInt` comes from the fixed semantics | Used by both target claims and the loop connection. The loop connection universally proves that exact execution reaches this value |
| `prodSignsResult` equations | Definitional summary for every finite `IntSeq` | Mathematical result term only | Empty/nonempty equations are disjoint and exhaustive; the nonempty equation invokes the justified `foldResult` with the program's initial accumulators | Postcondition of `SPEC.prod-signs`; the combined target proof produces `#Top` |
| Exact loop rule in `verification.k` | Operational bridge for the exact translated body and exact post-loop continuation | Matches the precise normal call frame: `env=1`; exact builtin, module, and local scopes; `scopeLoc=2`; arbitrary preserved heap and heap location; one exact call frame; `noRet`; `NoExc`; exit 0. It removes the local scope and frame exactly as a normal return does. The continuation is the combined `If`/`Return` `Stmts` followed by `#endcall`, not an arbitrary suffix | `LOOP-CONNECTION-SPEC` proves the complete same transition without importing `verification.k`; it uses fixed MPY execution plus the independently connected typed iterator. It proves returned value, frame pop, scopes, control, heap preservation, exception state, and exit state | Used by both target claims. The connection produces `#Top`. Changing the body from `seen = 1` to `seen = 0` makes the connection fail with a `noneV` residual |
| `CONNECTION-SPEC` and `LOOP-CONNECTION-SPEC` | Derived auxiliary reachability claims | Their domains are the complete match domains described above | Both are proved in definitions that omit the operational bridge they justify; the dependency order is acyclic: represented iterator connection, then loop connection, then target proof | Both positive commands print `#Top` and exit 0 |

No new trusted primitive or unconstrained result-bearing oracle is introduced.
The exact builtins scope pins `abs` to `builtinV("abs")`; its integer result is
defined by the supplied semantics.

# Exact commands and actual outputs

`prove.sh` contains the executable record. The positive build and proof
commands actually run were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled

kompile --backend haskell connection.k \
  --main-module CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

kompile --backend haskell loop-connection.k \
  --main-module LOOP-CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-connection-kompiled
kprove loop-connection-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-CONNECTION-SPEC
kprove iterator-witness-spec.k \
  --definition loop-connection-kompiled \
  --spec-module ITERATOR-WITNESS-SPEC

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual positive results:

| Command | Actual result |
|---|---|
| Both translation commands | exit 0; `solution.mpy` and `smoke.mpy` generated |
| LLVM `kompile` | exit 0 |
| `krun smoke.mpy` | final `<k> .K </k>`, `<exc> NoExc </exc>`, `<exit-code> 0 </exit-code>`; process exit 0 |
| `kprove connection-spec.k` | `#Top`; exit 0 |
| `kprove loop-connection-spec.k` | `#Top`; exit 0 |
| `kprove iterator-witness-spec.k` | `#Top`; exit 0 |
| `kprove spec.k` | `#Top`; exit 0 |

The compilers also emitted non-fatal warnings about unused variables, the
deprecated spelling of the `functional` attribute, and non-exhaustive total
functions in unrelated parts of the supplied LLVM semantics. None of the
positive commands exited non-zero.

The exact negative validation commands were:

```bash
kprove connection-mutation-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-MUTATION-SPEC
kprove loop-body-mutation-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-BODY-MUTATION-SPEC
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
python3 differential_test.py
```

Actual negative and differential results:

| Check | Actual result |
|---|---|
| Iterator value 4 mutated to 5 | stuck at `#bindTgt(TARGET, 4)`; exit 1 |
| Body mutated from `seen = 1` to `seen = 0` | stuck with returned `noneV` for a realizable nonempty branch; exit 1 |
| Result mutated to `foldResult(...) +Int 1` | implication failure showing `foldResult +Int 1` is not equal to `foldResult`; exit 1 |
| Independent differential test | `DIFFERENTIAL_CASES=19616 MISMATCHES=0`; exit 0 |

The expected-failure wrapper in `prove.sh` records each non-zero result and
makes the complete runner exit 0 only when all positive and negative outcomes
have the required polarity.

# Gate results

## Gate A — PASS

- A1: `solution.mpy` and the `FuncDef` in `SPEC.prod-signs` have the same
  translated constructor body. The whole-program claim executes loading,
  lookup, argument binding, initialization, the first loop step, and return.
  `LOOP-CONNECTION-SPEC` executes the exact loop body for every remaining
  sequence. The material body mutation is rejected.
- A2: Both operational bridges have complete state-footprint records. The
  iterator bridge changes only iterator control. The loop bridge's connection
  theorem covers value, scopes, frame removal, stack, heap, return state,
  exception state, and exit code.
- A3: Iterator binding and continuation are universal in the iterator
  connection. The loop rule pins the exact `abs` binding, body, combined
  post-loop continuation, call frame, and normal control state. It cannot match
  exceptional or alternate-continuation configurations.
- A4: All recursive equations have exhaustive, non-overlapping structural or
  sign cases and strict structural descent. There are no overlapping
  contradictory proof-local equations.
- A5: The initial empty and nonempty configurations are realizable; concrete K
  executions witness them. For example, `REST=.IntSeq`, `TOTAL=2`, `SIGN=1`
  makes the original loop result 2 and the mutation demand 3. The mutation
  exits 1 with the expected failed equality.

## Gate B — PASS

- The formal domain, all finite lists of integers, matches the prompt's stated
  domain. K integers and CPython integers are both unbounded for this purpose.
- The reference semantics explicitly permits unboxed read-only lists in
  claims. This function only reads the input; concrete heap-allocated list
  literals also execute successfully in `smoke.mpy`.
- The accumulator recurrence has the prompt's meaning by induction: `total`
  is the sum of magnitudes and `sign` is the product of signs after every
  processed prefix. `seen` distinguishes exactly the empty input.
- The three prompt examples agree with the implementation, concrete K run,
  and independent oracle.

## Gate C — PASS

- Every proof-local symbol and operational bridge is inventoried above with its
  dependents and evidence.
- All positive, mutation, concrete, and differential artifacts exist in the
  workspace and their exact commands and observed results are recorded.
- Formal claims, conditional trust, finite evidence, and excluded behavior are
  separated below.

# Trust boundary

| Assumption | Influence and dependents | Evidence |
|---|---|---|
| The supplied, read-only MPY semantics correctly models the exercised Python subset | Defines all program execution, binding, integer arithmetic, `abs`, lists, calls, and control used by every K claim | Concrete LLVM execution of five assertions; bridge-free symbolic connection proofs; supplied semantics was not modified |
| `py2mpy.py` faithfully translates the relevant CPython AST nodes | Connects `solution.py` to `solution.mpy` and to the matching constructor tree in `spec.k` | The fixed translator is run directly; generated constructor tree was checked against the formal `FuncDef`; both Python and K concrete tests use the same source body |
| K's compiler, LLVM/Haskell backends, and prover implement their stated logic | Underlies all `krun` and `kprove` results | Successful independent concrete and symbolic runs, including deliberately rejected claims |

No conclusion depends on an unproved external value oracle. The reference
semantics and toolchain are trusted foundations, not theorems proved here.

# Empirically supported facts

`smoke.py` checks the three prompt examples plus two additional negative-sign
parity cases under concrete LLVM execution.

`differential_test.py` compares the actual `solution.prod_signs` against an
independently written oracle that counts negatives and detects zero rather than
reusing the proof recurrence. Its 19,616 cases comprise:

- all three stated examples;
- all arrays of lengths 0 through 5 over integers −3 through 3; and
- representative positive, negative, cancelling, and zero-containing
  100-digit integer cases.

The recorded run has zero mismatches. This is finite validation evidence, not
a replacement for the universal K claims.

# Excluded behavior

- Inputs containing non-integers, non-list iterables, or infinite iterables are
  outside the formal domain.
- Rebinding or shadowing `abs`, exceptional entry states, and alternate call
  frames are outside the exact whole-program precondition.
- The theorem does not establish correctness of the supplied semantics,
  translator, K implementation, or hardware.
- This is a partial-correctness reachability proof, not a separately stated
  total-correctness or resource-bound theorem.

The `VALIDATED` headline is the proof-quality outcome after Gates A, B, and C.
The runner marker `KPROVE_PASSED` separately reports only that every required
positive target-proof command printed `#Top` and exited 0.
