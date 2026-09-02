VALIDATED

# What is proven

Under the supplied MPY semantics, `numerical_letter_grade` is partially
correct for every arbitrary finite list whose elements are MPY `Int` or
`Float` values. There is no bound on list length and no finite unrolling in
the target theorem.

For an input sequence `VS`, the function returns a fresh list containing one
letter-grade string per input, in the same order. Each output is selected by
the table encoded by `gradeValue`: equality with `4.0` gives `A+`; otherwise
the strict descending cutoffs give `A` through `D-`; otherwise the result is
`E`.

The proof executes the translated function body, including module loading,
name lookup, call-frame creation, parameter binding, list allocation, every
comparison and branch, `append`, return lookup, frame pop, and restoration of
the caller state. It does not replace the function or loop with an
operational summary.

This is a reachability/partial-correctness result. It is not a separate
machine-checked liveness theorem.

# Formal claim

`SPEC.entry` starts from the complete initial MPY state and the exact
`GRADE-PROGRAM` term. For symbolic `VS:ValSeq` satisfying
`allGradeNumbers(VS)`, it establishes:

```k
<k> ... => ref(0) </k>
<heap> .Map => 0 |-> list(gradeAcc(.ValSeq, VS)) </heap>
<heapLoc> 0 => 1 </heapLoc>
<env> 0 => 0 </env>
<scopeLoc> 1 => 1 </scopeLoc>
<stack> .List => .List </stack>
<ret> noRet => noRet </ret>
<exc> NoExc => NoExc </exc>
<exit-code> 0 => 0 </exit-code>
```

`SPEC.loop-invariant` is the unbounded circularity. At a real `#loop` head,
with accumulated output `ACC` and unprocessed suffix `VS`, it changes the
output heap value from `list(ACC)` to `list(gradeAcc(ACC, VS))`, preserves the
input and output bindings, and permits only the loop variable's final value
to be existential.

Its obligations are:

- Base: `gradeAcc(ACC, .ValSeq) = ACC`.
- Step: one fixed-semantics iteration binds the head, follows one of the
  thirteen actual branches, appends `gradeValue(head)`, and reapplies the
  circularity to the tail.
- Entry discharge: the function initializes `ACC` to `.ValSeq`; the
  circularity yields `gradeAcc(.ValSeq, VS)`, after which the actual return and
  frame-pop rules complete the entry claim.

# Proof-extension inventory

## `GRADE-STEP` and `GRADE-PROGRAM`

- Class: definitional summary (compile-time syntax macros).
- Semantic role: abbreviate the exact AST; no macro remains at runtime and no
  execution step is replaced.
- Domain/context: only the two closed macro terms, with no variables, frames,
  cells, or guards.
- State footprint/value influence: none directly; their expansion supplies
  the program executed by both claims.
- Justification and containment: `kast --expand-macros` produces byte-identical
  KORE for `solution.mpy` and `GRADE-PROGRAM` (`cmp` exit 0).
- Dependents: both target claims.
- Validation: `check_artifacts.py`, the KAST comparison, LLVM execution, and
  the body-mutation probe.

## `isGradeNumber` and `allGradeNumbers`

- Class: definitional summaries.
- Semantic role: constrain the dynamic MPY domain; they do not rewrite program
  terms.
- Domain: all `Val` values and all finite `ValSeq` constructor terms.
- Equations: `isGradeNumber(V)` is exactly `isInt(V) orBool isFloat(V)`;
  `allGradeNumbers` has disjoint empty/cons cases and structurally descends.
- State/context footprint: none.
- Value influence: preconditions for both claims and the guarded comparison
  restatements.
- Dependents: `gradeEq`, `gradeGt`, both dispatch rules, and both claims.
- Validation: integer/float mixed smoke tests, arbitrary symbolic `ValSeq`
  proof, and mutation rejection.

## `gradeEq` and `gradeGt`

- Class: definitional summaries.
- Semantic role: expose the supplied MPY Int/Float-vs-Float dispatch through a
  dynamic `Val` argument; they do not replace a `<k>` computation.
- Domain: total over `Val × Float`. The `Int`, `Float`, and nonnumeric cases
  are exhaustive and pairwise disjoint.
- Value equations:
  - `gradeEq(I,F) = eqF(intToF(I),F)` and
    `gradeEq(G,F) = G ==Float F`;
  - `gradeGt(I,F) = gtF(intToF(I),F)` and
    `gradeGt(G,F) = gtF(G,F)`;
  - the explicitly nonnumeric totalization is `false`, and is outside every
    comparison-dispatch use.
- State/context footprint: none.
- Value influence: all grading branches and the final result summary.
- Justification: constructor-by-constructor restatement of the corresponding
  fixed rules in `reference-semantics/semantics/float.k`.
- Dependents: `gradeValue`, the dispatch twins, and both claims.
- Validation: exhaustive equation/guard audit, LLVM boundary tests, the
  independently implemented table oracle, false-postcondition rejection, and
  body-mutation rejection.

## Guarded `applyCmp` simplification rules

- Class: derived lemmas (the Kit guarded dynamic-dispatch pattern).
- Semantic role: restate existing fixed `applyCmp("==", Int|Float, Float)` and
  `applyCmp(">", Int|Float, Float)` equations over symbolic `V:Val`.
- Complete match domain: any occurrence of the indicated `applyCmp` function
  under `isGradeNumber(V)`. There is no continuation, control-stack, binding,
  or cell wildcard because these are pure function equations.
- Justification scope/containment: `isGradeNumber` is exactly the disjoint
  `Int`/`Float` union, and `gradeEq`/`gradeGt` reproduce the fixed right-hand
  side for each constructor. Thus every match is in one fixed-rule domain.
- State footprint: no cells read, written, preserved, or abstracted.
- Value influence: branch choice and therefore appended strings.
- Dependents: the loop invariant and entry claim.
- Control/value validation: fixed LLVM execution covers every grade outcome;
  the `"Z"` body mutation is rejected; the false output is rejected. There is
  no operational bridge to compare.

## `gradeValue` and `gradeAcc`

- Class: definitional summaries.
- Semantic role: name the expected mathematical output without replacing
  execution.
- Domain: `gradeValue` is total on `Val`; target uses are numeric.
  `gradeAcc` has disjoint empty/cons equations and strictly descends through
  its second finite `ValSeq` argument.
- Context/state footprint: none.
- Value influence: they define the result constrained by the invariant and
  entry claim.
- Value justification: `gradeValue` uses the same comparison atoms and branch
  order as the real program; `gradeAcc` performs exactly one summarized append
  before recurring on the suffix.
- Dependents: both claims.
- Validation: the real loop proves the connection machine-checkably; no rule
  states the final postcondition as an axiom. The false-result and wrong-body
  probes both fail.

## `SPEC.loop-invariant`

- Class: derived lemma/circularity.
- Semantic role: machine-checked reachability through the real `#loop`; it is
  not an ordinary rewrite rule in the kompiled definition.
- Domain/context: arbitrary finite numeric `VS`, arbitrary `ACC`, exact local
  bindings, real heap output object, and an arbitrary framed continuation.
- State footprint: reads/binds `grade`, reads `letter_grades`, mutates only
  the list at heap location `H`, and preserves the input/output bindings and
  parent frame.
- Value influence: establishes `gradeAcc(ACC,VS)`.
- Justification: its base and inductive branches print `#Top` as part of the
  target proof.
- Dependents: `SPEC.entry`.
- Validation: isolated invariant proof printed `#Top`; the material body
  mutation is rejected with the residual showing `"Z"` versus `gradeValue`.

There are no proof-local operational bridges and no proof-local trusted
primitives.

# Exact commands and actual outputs

The complete reproducible command sequence is in `prove.sh`. The final
end-to-end invocation was:

```bash
./prove.sh
```

Actual overall exit: `0`.

The required positive target command was:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output: `#Top` in `target-proof.out`. Actual exit: `0`. This single
command proves both `SPEC.loop-invariant` and `SPEC.entry`.

The Haskell definition was built with:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Actual exit: `0`. Compiler warnings in `haskell-compile.out` are unused-variable
warnings originating in the supplied `str.k` and unused existential variables
in the spec; there are no proof errors.

The concrete definition and smoke test were:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual exits: `0`, `0`. `concrete.out` ends with `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`. The LLVM compilation
warnings are pre-existing exhaustiveness/unused-variable warnings in the
read-only reference semantics.

Program identity was checked with:

```bash
kast --definition verification-kompiled \
  --module VERIFICATION --sort Module --expand-macros \
  --output kore solution.mpy > solution-term.kore
kast --definition verification-kompiled \
  --module VERIFICATION --sort Module --expand-macros \
  --output kore --expression 'GRADE-PROGRAM' > proof-term.kore
cmp solution-term.kore proof-term.kore
```

Actual output: `KAST macro identity: PASS`. Actual `cmp` exit: `0`.

The A5 probe was:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Expected and actual exit: `1`. `vacuity.out` begins with
`WarnStuckClaimState`; the realized empty-input state contains
`list(.ValSeq)`, while the false destination demands `["E"]`.

The body-sensitivity probe was:

```bash
kompile mutation.k \
  --backend haskell \
  --main-module MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled
kprove spec-body-mutation.k \
  --definition mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual compile exit: `0`. Expected and actual proof exit: `1`.
`body-mutation.out` begins with `WarnStuckClaimState` and shows the mismatch
between the required `gradeValue(V)` and character code `90` (`"Z"`).

The independent differential command was:

```bash
python3 differential.py
```

Actual output in `differential.out`:

```text
cases=1003 mismatches=0
```

# Gate results

## Gate A — PASS

- A1: the exact translated program is executed. Expanded KORE identity passes,
  and replacing the real loop body with an append of `"Z"` invalidates the
  invariant.
- A2: no operational bridge exists. The fixed semantics performs list
  allocation and append mutation. The formal claims constrain the returned
  reference, heap contents/location, environment, scope location, stack,
  return state, exception state, and exit code.
- A3: fixed rules perform lookup, argument evaluation, call/frame management,
  branch control, return, and pop. The dispatch lemmas are pure,
  constructor-exhaustive restatements with no continuation or state footprint.
- A4: every proof-local total function has exhaustive disjoint cases; recursive
  equations descend; comparison dispatch guards are exactly the numeric union.
- A5: the empty input is a realizable witness. The deliberately false `["E"]`
  postcondition is rejected with exit 1. The wrong loop body is independently
  rejected with exit 1.

## Gate B — PASS

- B1: the theorem covers arbitrary finite list length and both numeric value
  classes on which the supplied comparison chain is defined (`Int` and
  `Float`). It imposes no GPA range bound. Nonnumeric MPY values are not GPAs
  and the supplied mixed comparison semantics is undefined for them.
- B2: MPY floats use K/IEEE floating-point values, matching the material Python
  GPA behavior. The output strings are ASCII, fully inside MPY's string model.
  Mixed Boolean/Float comparison is absent from the supplied semantics; Boolean
  values are outside the prompt's GPA domain.
- B3: `gradeValue` states the table in terms of the fixed comparison contracts,
  while the loop and entry claims separately prove that real execution
  constructs that summary.
- B4: the implementation uses the exact strict/equality boundaries from the
  prompt. The supplied example passes in Python and under LLVM MPY execution.

## Gate C — PASS

The trust boundary is explicit below. Every claimed check has an artifact,
exact command, recorded output, input scope, and oracle. Formal proof,
conditional primitive facts, and finite empirical evidence are kept separate.

# Trust boundary

| Component | Why outside this theorem | Influence and dependents | Evidence |
|---|---|---|---|
| Fixed MPY `intToF`, `eqF`, `gtF`, and `==Float` | The supplied semantics intentionally keeps symbolic float operations opaque or delegates them to K hooks. | They determine comparison atoms, branches, `gradeValue`, and both claims. The theorem is conditional on their documented numeric contracts. | LLVM MPY smoke execution over every grade outcome and mixed Int/Float example; independent Python differential test. |
| Supplied MPY operational semantics | It is the fixed model being verified against, not reproved here. | All control, lookup, heap, list, and frame behavior in both claims. | LLVM execution, successful symbolic proof, false-result rejection, and body-mutation rejection. |
| K toolchain/backend | Trusted proof checker and runtime implementation. | Compilation, symbolic reachability, and concrete hooks. | K version `v7.1.293`; reproducible logs and exit statuses. |
| `py2mpy.py` | Fixed supplied translator, not modified or verified here. | Determines `solution.mpy`. | Regeneration equality in `check_artifacts.py`; expanded KORE equality against `GRADE-PROGRAM`. |
| Termination | K reachability establishes partial correctness, not a separate liveness theorem. | The result is conditional on termination. | The loop structurally consumes a finite `ValSeq`; all concrete samples terminate. This is explanatory evidence, not a liveness proof. |

# Empirically supported facts

- `smoke.py` contains the exact same function AST as `solution.py`, checked by
  `check_artifacts.py`.
- The LLVM smoke scope covers the empty list, the prompt example, every exact
  cutoff, and a representative value immediately above every strict cutoff.
  All assertions pass under the supplied `MPY-KRUN` definition.
- `differential.py` uses an independently structured table-walk oracle. With
  seed `20260729`, it checks the prompt example, all listed boundaries, and
  1,000 random lists of length 0–24 containing integers 0–4 and float
  hundredths 0.00–4.00. Result: 1,003 cases, zero mismatches.
- These finite tests support the primitive/model boundary. They do not replace
  the unbounded K proof.

# Excluded behavior

- Nonnumeric values are excluded: the task asks for GPA values, and the fixed
  MPY Int/Float comparison chain is not defined on other `Val` constructors.
- Boolean-as-integer corner cases are outside the GPA domain and are not
  modeled by the supplied mixed Bool/Float comparison rules.
- Total correctness/termination is not claimed.
- No bound on finite input length is excluded; arbitrary finite length is the
  central symbolic theorem.
