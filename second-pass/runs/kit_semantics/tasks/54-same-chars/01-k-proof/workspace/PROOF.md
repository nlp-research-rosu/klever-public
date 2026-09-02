VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every pair of symbolic string-code
sequences `S0` and `S1`, loading the translated `same_chars` definition and
calling it with `str(S0)` and `str(S1)` finishes with:

```k
"result" |-> sameSet(dedupCodes(S0), dedupCodes(S1))
```

The proof executes the actual translated function body. It also fixes the
observable final control and state: `.K`, environment `0`, scope location `1`,
an empty heap, heap location `0`, an empty stack, `noRet`, `NoExc`, and exit
code `0`. This is a partial-correctness reachability theorem in the sense of the
Kit workflow.

The supplied definitions give the result its intended meaning:
`dedupCodes` retains one occurrence of each character code, `sameSet` is mutual
`subsetCodes`, and `subsetCodes` checks membership using `codeIn`. Thus the
result is true exactly when each input contains every distinct character of the
other input.

## Formal claim and scope

- Program boundary: the exact `FuncDef` emitted in `solution.mpy`, followed by
  a module-level harness assignment that calls `Name("same_chars")`.
- Input domain: every `str(S0)` and `str(S1)` where `S0` and `S1` have sort
  `IntSeq`; there is no strengthened `requires` condition.
- Observable final state: the result binding and every cell listed above.
- Intended property: return true iff the two input strings contain the same
  distinct characters, ignoring multiplicity and order.
- Formal artifact: claim `SPEC.same-chars` in `spec.k`.

The claim begins at `#loadAll`, so module binding, lookup of `same_chars`,
parameter binding, lookup of the built-in `set`, argument evaluation, both set
constructions, comparison, return, frame restoration, and assignment of the
result all run under the fixed semantics.

## Proof-extension inventory

The reconstructed inventory is empty.

`verification.k` only imports the supplied `MPY` module. It declares no syntax,
function, totality assertion, equation, simplification rule, ordinary rewrite,
priority rule, operational bridge, trusted primitive, opaque term, or auxiliary
claim. `spec.k` contains only the positive target claim. Therefore there is no
proof extension for which the contract's extension-record fields apply.

The functions `dedupCodes`, `sameSet`, `subsetCodes`, and `codeIn` are part of
the supplied fixed semantics, not proof-local additions. The two mutation
claims are validation probes and are not imported by the positive proof.

## Commands and actual outputs

Tool versions used:

```text
K version: v7.1.293
Python 3.10.12
```

The complete reproducible workflow is `./prove.sh`; its final run exited `0`.
It records these exact positive build and proof commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py krun-smoke.py > krun-smoke.mpy
python3 -m py_compile solution.py test_solution.py
python3 test_solution.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun solution.mpy --definition runtime-kompiled
krun krun-smoke.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual differential-test output, exit `0`:

```text
prompt_examples=6 exhaustive_pairs=14641 mismatches=0
```

Direct execution of `solution.mpy` exited `0`, consumed the module to `.K`, and
bound `same_chars` to the closure containing the translated body. The LLVM
smoke execution also exited `0` and included these module bindings:

```text
"example_1" |-> true
"example_2" |-> true
"example_3" |-> true
"example_4" |-> false
"example_5" |-> false
"example_6" |-> false
```

The LLVM configuration also ended with `.K`, `NoExc`, and exit code `0`.

Actual positive target-proof output:

```text
#Top
```

The positive `kprove` command exited `0`. The Haskell compile and proof also
printed four supplied-semantics warnings about unused `As`/`Bs` variables in
the two decided branches of `strLt`; no warning concerns the target claim or
the set-equality dependency slice. The LLVM build exited `0` with additional
non-exhaustiveness warnings in unrelated float, mapping, join, and subscript
operations.

The exact negative commands are also in `prove.sh`:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Both exited `1` with `WarnStuckClaimState`, as required:

- `spec-vacuity.k` demanded `false` for inputs `"a"` and `"aa"`; its residual
  contained `"result" |-> true`.
- `spec-body-mutation.k` replaced the body with `return False` while demanding
  `true` for the same inputs; its residual contained `"result" |-> false` and
  the mutated closure body.

`prove.sh` checks that each negative command is nonzero and printed:

```text
EXPECTED_FAILURE: spec-vacuity.k exited 1
EXPECTED_FAILURE: spec-body-mutation.k exited 1
```

## Gate A — PASS

- A1, program identity and body sensitivity: the exact translated body occurs
  in the entry computation and executes through the fixed call/return rules.
  The changed-body probe failed with the changed result, demonstrating body
  sensitivity.
- A2, operational-state preservation: no operational bridge exists. The claim
  observes the result, environment, scopes, allocation counters, heap, stack,
  return state, exception state, and exit code after fixed execution.
- A3, binding/evaluation/control fidelity: `same_chars` is loaded into module
  scope and looked up by name; `set` is reached through the supplied scope chain
  and built-ins frame. Fixed rules perform left-to-right argument evaluation,
  parameter binding, return, frame pop, and the final assignment.
- A4, consistency and rule validity: no proof-local equations or rewrites were
  added. Consequently there are no extension guards, overlaps, coverage claims,
  or totalization claims to audit.
- A5, non-vacuity: `S0 = iCons(97, .IntSeq)` and
  `S1 = iCons(97, iCons(97, .IntSeq))` is a realizable witness. The deliberately
  false result mutation was rejected and exposed the actual `true` result.

## Gate B — PASS

- B1: the prompt annotates both inputs as strings. The formal inputs are exactly
  two `str(IntSeq)` values and add no content, length, alphabet, or nonempty
  restriction.
- B2: the supplied model represents a string as a sequence of integer character
  codes. Although concrete source literals in this semantics are ASCII-only,
  the symbolic theorem ranges over arbitrary `IntSeq` values. The property uses
  only occurrence and integer equality, so it does not depend on hashing, set
  iteration order, or a numeric encoding-specific operation.
- B3: the postcondition is the supplied semantics' own set construction and set
  equality. Inspection of its exhaustive list equations connects the summary
  directly to mutual distinct-character membership. The independent tests
  support, but do not replace, this definitional adequacy argument.
- B4: `return set(s0) == set(s1)` directly implements the natural-language
  contract and agrees with all supplied examples.

## Gate C — PASS

### Trust ledger

| Unproved component | Role and influence | Dependents | Evidence |
|---|---|---|---|
| Supplied `MPY` semantics, especially call/binding rules and `applyBuiltin("set", ...)`, `dedupCodes`, `sameSet`, `subsetCodes`, `codeIn` | Fixed execution model; affects value, control, state, exceptions, and termination behavior | `SPEC.same-chars` | Source inspection, LLVM execution of all prompt examples, both discriminating mutations, and the differential test |
| K v7.1.293 compiler, LLVM runtime, Haskell backend, and prover | Trusted implementation of parsing, execution, and reachability proof | All K evidence | Reproducible positive `#Top`, concrete executions, and two expected-failure residuals |
| `py2mpy.py` translation from CPython AST to constructors | Connects `solution.py` to `solution.mpy`; affects program identity | Deliverable/source correspondence | `prove.sh` regenerates `solution.mpy`; the emitted constructor body is reproduced exactly in `spec.k`; Python byte-compilation succeeds |

No result-bearing opaque primitive or external trusted operation is reached by
this program. Unused opaque facilities elsewhere in the supplied semantics,
such as sorting or hashing support, are outside the dependency slice.

### Reproducible finite evidence

`test_solution.py` uses an independently written two-direction membership
oracle rather than set equality. It checks:

- all six prompt examples; and
- all 14,641 ordered pairs drawn from the 121 strings over alphabet `abc` with
  lengths zero through four.

The recorded result is zero mismatches. `krun-smoke.mpy` independently exercises
the six prompt examples under the required LLVM build of the supplied
semantics. These are finite evidence only; the universal result is supplied by
the symbolic `kprove` claim.

## Trust boundary and excluded behavior

Formally established: the reachability claim over all two-string `IntSeq`
inputs under the supplied `MPY` theory, with the complete observed final state.

Conditionally trusted: correctness of the supplied reference semantics,
`py2mpy.py`, and the K toolchain implementations.

Empirically supported: agreement with all prompt examples and with the
independent oracle on the documented finite domain.

Excluded: calls with non-string arguments; behavior outside the supplied
semantics; CPython implementation details such as hashing, allocation, and
performance; and a separate proof of the K toolchain or translator. The theorem
is reported as partial correctness and does not independently assert a general
liveness result beyond the executions closed by the reachability proof.
