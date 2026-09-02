VALIDATED

## What is proven

Under the supplied MPY semantics, for every finite `ValSeq` whose elements are
semantic string values, loading the exact translated `solution.py` module and
calling `concatenate(list(VS))` terminates with:

```k
str(concatFrom(.IntSeq, VS))
```

`concatFrom` is the left fold that appends each element's `IntSeq` to the
accumulator. Thus the returned semantic string contains every input string, in
order, with no separator. The theorem also constrains frame restoration, heap,
stack, return, exception, and exit-code cells. As specified by the Kit
workflow, this is a partial-correctness result; it does not separately claim a
liveness theorem.

## Formal claim and scope

- Program boundary: the exact `ImportFrom`, `FuncDef`, call binding, function
  body, loop, return, and frame-pop term generated from `solution.py`.
- Input domain: `list(VS)` with `isStringSeq(VS)`, exactly the modeled
  `List[str]` domain.
- Observable final state: the returned `str(concatFrom(.IntSeq, VS))`; the
  entry claim also restores `env`, `scopeLoc`, `heap`, `heapLoc`, `stack`,
  `ret`, `exc`, and `exit-code`. The retained module binding is intentionally
  unobserved.
- Intended property: concatenate all input strings in list order.
- Claims: `SPEC.concat-loop-empty`, `SPEC.concat-loop-step`, and
  `SPEC.concatenate`.

## Proof-extension inventory

No proof-local rule intercepts `Call`, `For`, `#loop`, binding, lookup,
`AugAssign`, return, or frame-pop. Those operations execute with the fixed MPY
rules.

| Extension | Class and role | Domain, context, and footprint | Value justification and dependents | Validation |
|---|---|---|---|---|
| `stringCodes(str(S)) => S`; owise fallback to `.IntSeq` | Definitional summary; total string recognizer projection | Pure `Val -> IntSeq`; no cells or control. The cases are disjoint and cover `Val`. | Exact on strings. The fallback cannot make a non-string equal `str(...)` because the constructors differ. Used by `isStringSeq`, `concatFrom`, `lastFrom`, and the guarded `applyBin` lemma. | Ground and symbolic cases simplify in the successful proof; non-string inputs are excluded by `isStringSeq`. |
| `isStringSeq` base/cons equations | Definitional summary; input-domain predicate | Pure `ValSeq -> Bool`; `.ValSeq` and `vCons` are disjoint and exhaustive. | The cons equation requires `V ==K str(stringCodes(V))`, true exactly for strings, and recurses on the strict tail. All three target claims depend on it. | Empty and inductive branches both close; concrete witnesses include empty and nonempty lists. |
| `concatFrom` equations | Definitional summary of the returned value | Pure function on an accumulator and a finite string `ValSeq`; every proof use is guarded by the string-domain predicate. Recursion descends on `REST`. | The base returns the accumulator; the step uses MPY's `seqConcat` with the exact head codes. The entry result and both loop claims depend on it. | `#Top`, LLVM examples, and 255 independent CPython differential cases. |
| `lastFrom` equations | Definitional summary of the final loop-target local | Pure function on the prior target and a finite string `ValSeq`; recursion descends on `REST`. | Empty iteration preserves the old target; a step makes the head current and continues. It preserves the exact local scope state in the loop claims, although that local is later popped. | Both loop claims close after replacing the earlier existential local with this exact summary. |
| Guarded `[simplification]` rule for `applyBin("+", str(A), V)` | Derived lemma; symbolic normalization only | Pure `applyBin` term in any simplifier context; no state/control cells. Guard: `V ==K str(stringCodes(V))`. | Under the guard, `V` is a string. The RHS is exactly MPY-STR's fixed rule `applyBin("+", str(A), str(B)) => str(seqConcat(A,B))`. On overlap with that rule, `stringCodes(str(B)) => B`, so RHSs agree. Used by the inductive loop claim. | The positive proof closes; the changed-body probe fails. No opaque or fresh value is introduced. |
| `concat-loop-empty` and `concat-loop-step` | Derived reachability lemmas (the loop-invariant family), used coinductively | Exact `#loop` body, `env = 1`, builtins/global frames, and exact local keys `result`, `string`, `strings`; arbitrary continuation and omitted cells are equally universally quantified by the claims. They write exact `result` and `string` summaries and preserve `strings`, globals, continuation, and every framed cell. | Fixed MPY semantics executes iterator dispatch, target binding, lookup, `AugAssign`, and control. The step claim executes one iteration and recurs on `REST`; the base executes `#iterDone`. `SPEC.concatenate` depends on them. | Each invariant member printed `#Top` in focused construction runs, and the required combined run printed `#Top`. A material body mutation was rejected with exit 1. |

There are no operational bridge rules and no trusted or opaque primitive added
by this proof. The loop claims are machine-checked auxiliary execution
theorems, not axioms that bypass the body.

## Reproducible commands and actual results

The complete runner is `./prove.sh`. Its essential commands are:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC

python3 differential_tests.py
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual results:

- K version: `v7.1.293`.
- LLVM compile: exit 0. `krun`: exit 0, final `<k> .K </k>`, with
  `empty = ""`, `example = "abc"`, and `mixed = "xyz"`.
- Haskell compile: exit 0.
- Required all-claims `kprove`: output `#Top`, exit 0.
- False-result mutation (`concatenate([]) == "x"`): `WarnStuckClaimState`,
  residual result `str(.IntSeq)`, exit 1.
- Body mutation (append `""` instead of the loop element on `["a"]`):
  `WarnStuckClaimState`, residual result `str(.IntSeq)`, exit 1.
- CPython differential oracle: `cases=255 mismatches=0`, exit 0. The oracle is
  Python's independent `"".join(strings)`, not a reuse of the K equations.

## Gate results

### Gate A — PASS

A1: `solution.mpy` is regenerated before proof, and the entry claim contains
the same exact translated body. Fixed semantics executes the program-defined
function. The material changed-body probe is rejected.

A2/A3: the exact loop summaries preserve both modified locals, the original
input binding, all framed cells, the continuation, binding, evaluation order,
and return/frame control. There is no call or control bridge.

A4: total equations are exhaustive and disjoint; partial folds are used only
on their guarded string domain and descend structurally. The guarded
`applyBin` lemma agrees with the fixed rule on its complete domain.

A5: `[]` is a realizable precondition witness and `["a","b","c"]` gives a
distinct result. The false `"x"` postcondition is rejected with exit 1.

### Gate B — PASS

The formal domain matches the prompt's `List[str]` annotation, and the formal
postcondition is exactly ordered string concatenation, including the empty-list
case. Inputs outside `List[str]` are excluded. MPY literals are concrete
ASCII-only, but the symbolic theorem ranges over arbitrary `IntSeq` string
contents; concatenation is sequence append, so this representation difference
does not weaken the stated property.

### Gate C — PASS

All commands, probe artifacts, input scopes, oracles, exit codes, and residuals
are recorded and reproducible. Finite tests are reported only as evidence; the
universal result comes from `kprove`.

## Trust boundary

- The supplied read-only MPY semantics is treated as the fixed Python model.
- The installed K parser, compiler, Haskell backend, and reachability prover
  are trusted to implement K correctly.
- `py2mpy.py` is the supplied fixed translator; `prove.sh` regenerates
  `solution.mpy` immediately before compilation and proof.
- CPython and `str.join` are used only as an independent finite-test oracle.
- No external primitive, opaque program result, or unproved proof-local rule is
  trusted.

## Empirical support

`concrete_tests.py` checks the prompt boundaries and a mixed empty/nonempty
case in the LLVM semantics. `differential_tests.py` checks five fixed boundary
cases plus 250 deterministic generated lists, including empty strings,
whitespace, non-ASCII characters, and emoji, against CPython `str.join`, with
zero mismatches.

## Excluded behavior

The theorem excludes non-list inputs, list elements that are not strings,
Python exceptions outside that typed domain, mutation/concurrency during
iteration, and behaviors absent from the supplied MPY model. It is a theorem
about the supplied semantics; the finite CPython tests do not prove semantic
equivalence for all Python executions.
