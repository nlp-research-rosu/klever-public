VALIDATED

# What is proven

Under the supplied `MPY` semantics, for every finite `ValSeq` `VS` satisfying
`allStrVS(VS)` and every substring code sequence `P`, executing the exact
translated `filter_by_substring` module from the initial MPY configuration and
calling it with `list(VS)` and `str(P)` returns `ref(0)`.  The heap at location
`0` contains:

```k
list(filterAcc(.ValSeq, P, VS))
```

`filterAcc` preserves input order and duplicates and includes exactly an input
string whose code sequence satisfies the supplied semantics' `strContains`.
The module binding, scope cleanup, heap allocation count, empty stack,
`noRet`, `NoExc`, and zero exit code are also fixed by the entry claim.

This is a K reachability proof of partial correctness.  It does not separately
claim a liveness theorem.

# Formal claim and validation scope

- Program boundary: the complete `solution.mpy` module load, the exact
  `filter_by_substring` function binding and body, argument evaluation,
  function-frame creation, the actual `for` loop and `append` call, return,
  and frame pop.
- Input domain: `substring` is any semantic `str(P)` and `strings` is any
  finite `list(VS)` for which `allStrVS(VS)` is true.  This is the prompt's
  `List[str]` and `str` domain.
- Observable final state: returned reference, referenced result list, module
  binding, allocation counter, stack, return state, exception state, and exit
  code.  The input is represented by the semantics' documented unboxed,
  read-only `list(VS)` claim value; the implementation never mutates it.
- Intended property: return the input strings, in their original order and
  with duplicates preserved, exactly when `substring` occurs contiguously in
  the string.

The two claims in `spec.k` are:

1. `SPEC.filter-loop`, the loop-head circularity.
2. `SPEC.filter-by-substring`, the complete module-and-call theorem.

The loop proof discharges:

- Base: an empty remaining sequence leaves the accumulator unchanged.
- Step, contained: the fixed semantics evaluates membership to true, dispatches
  `result.append(string)`, mutates the accumulator heap object, and applies the
  invariant to the tail.
- Step, excluded: the fixed semantics evaluates membership to false, leaves
  the accumulator unchanged, and applies the invariant to the tail.
- Whole-program use: the allocated empty accumulator instantiates
  `filterAcc(.ValSeq, P, VS)`; the function then returns that same reference.

# Proof-extension inventory

There are no proof-local trusted primitives and no operational bridge that
replaces a source call, function body, loop body, return, or state transition.

## `strCodes`

- Class: definitional summary.
- Semantic role: exposes the code sequence of a semantic string; it does not
  replace program execution.
- Domain: every `Val`.  `str(S)` maps to `S`; every non-string constructor maps
  to `.IntSeq` through `[owise]`.
- Matched context and justification scope: pure `strCodes(V)` terms in any
  expression context; both are the complete `Val` domain.
- State footprint: none.
- Value influence: used to state string-ness, normalize an equal operand, and
  select `filterAcc` cases.
- Value justification: exhaustive, disjoint constructor equations.  For a
  string the result is its constructor field; for a non-string the chosen
  default cannot make that value equal to `str(strCodes(V))`.
- Dependents: `allStrVS`, the normalization lemma, `filterAcc`, both target
  claims.
- Validation: `SPEC-VALUE-CHECK.codes-a` closed with `#Top`; the opposite value
  in `SPEC-VALUE-OPPOSITE.wrong-codes-a` exited 1 and became stuck at
  `iCons(97, .IntSeq)`.

## `allStrVS`

- Class: definitional summary.
- Semantic role: formalizes the prompt's `List[str]` domain.
- Domain: every `ValSeq`.
- Matched context and justification scope: pure `allStrVS(VS)` terms; the
  `.ValSeq` and `vCons` equations exhaust the sort.
- State footprint: none.
- Value influence: restricts the entry and loop claims to string elements.
- Value justification: on a head `V`,
  `V ==K str(strCodes(V))` is true exactly for the `str` constructor; recursion
  checks the strictly shorter tail.
- Dependents: both target claims.
- Validation: the positive proof covers symbolic `VS`; ground empty and
  non-empty witnesses are exercised by the mutation and concrete artifacts.

## guarded `applyCmp` operand normalization

- Class: derived lemma.
- Semantic role: from the guard
  `V ==K str(strCodes(V))`, replace only the right operand with that equal
  constructor-shaped value.  The resulting `applyCmp` remains present and the
  fixed `MPY-STR` rule evaluates membership.
- Domain: `applyCmp("in", str(P), V)` under exactly that equality guard.
- Matched context and justification scope: any simplifier context containing
  that function term; equality congruence applies in the same complete domain.
- Context containment: the guard itself proves that the old and new operands
  are equal.  No continuation, binding, control, or state cell is matched or
  discarded.
- State footprint: none.
- Value influence: enables the fixed membership result to control the loop
  branch; it does not choose that result.
- Value justification: substitutivity of equality.  On overlap with the fixed
  `applyCmp("in", str(P), str(S))` equation, `strCodes(str(S)) = S`, so the
  normalized term is the same fixed operation on the same value.
- Dependents: `SPEC.filter-loop` and therefore the entry claim.
- Control validation: fixed LLVM executions exercise both contained and
  excluded elements.  The extended ground claims for true and false membership
  both close.
- Value validation: `contains-yes` and `contains-no` close under the extended
  definition; the source-level body mutation is rejected.

## `filterAcc`

- Class: definitional summary.
- Semantic role: names the mathematical result of filtering the remaining
  sequence into an accumulator; it does not rewrite a program term.
- Domain: every accumulator and pattern, with an empty remaining sequence or a
  string-characterized head.  This covers every use under `allStrVS`.
- Matched context and justification scope: pure `filterAcc(A,P,VS)` terms on
  that domain.
- State footprint: none.
- Value influence: fixes the result list in the loop and entry postconditions.
- Value justification: the base returns `A`; the two step guards are disjoint
  complements of `strContains(P, strCodes(V))`; the contained case appends
  exactly `V`, and the excluded case does not.  Both recurse on the strictly
  shorter tail.
- Dependents: the loop and entry claims.
- Validation: the actual loop establishes the summary universally.  The false
  result mutation and the changed-condition mutation are both rejected.

## `SPEC.filter-loop`

- Class: derived lemma (auxiliary reachability claim/circularity).
- Semantic role: executes and summarizes the real fixed-semantics `#loop`; it
  is not an ordinary rewrite rule.
- Domain: all `VS` satisfying `allStrVS(VS)`, any accumulator `ACC`, pattern
  `P`, result heap location `H`, exact plain local function frame, arbitrary
  outer scopes, heap remainder, parent, and trailing `<k>` continuation.
- Matched context: the exact `#loop(list(VS), Name("string"), If(...append...))`
  body from `solution.mpy`; exact `result`, `string`, `strings`, and
  `substring` bindings; `H |-> list(ACC)`; arbitrary framed continuation and
  outer maps.  Omitted configuration cells are framed unchanged by K's
  completed configuration.
- Justification scope and containment: the reachability claim itself is
  quantified over every continuation and framed state that it matches, so its
  justification and match domains coincide.
- State footprint: reads `<env>`, the four local bindings, and heap location
  `H`; updates the local `string` binding and the list at `H`; consumes only the
  loop computation.  It preserves the outer scopes, result/string-list
  bindings other than the final loop variable, parent, heap remainder,
  allocation counter, stack, return state, exception state, and exit code.
- Value influence: fixes the result heap list through `filterAcc`.
- Justification: machine-checked base and inductive fixed-semantics execution.
- Dependents: `SPEC.filter-by-substring`.
- Validation: focused and complete proof runs printed `#Top`.  Replacing the
  source condition `in` with `not in` made the ground connection fail.

# Commands and actual results

The reproducible runner is `./prove.sh`; it completed with exit 0.

Translation:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
```

Both regenerated files matched the checked artifacts.

Concrete LLVM build and execution:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-smoke.mpy --definition runtime-kompiled
```

Actual result: both commands exited 0.  `krun` ended with `.K`, `NoExc`, and
exit code `0`; the heap contained the empty-list result and the prompt example
result `["abc", "bacd", "array"]`.  `kompile` emitted existing
reference-semantics exhaustiveness/unused-variable warnings.

Symbolic Haskell build and complete target proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual result:

```text
#Top
```

Both commands exited 0.  A focused final loop run also printed `#Top` and
exited 0:

```bash
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.filter-loop
```

Value-sensitivity checks:

```bash
kprove spec-value-check.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-CHECK
```

Actual result: `#Top`, exit 0.  K also printed `WarnTrivialClaim` because the
three ground function claims simplify before a transition is needed.

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`.  For the satisfiable witness
`strings=[]`, `substring="a"`, execution returned `ref(0)` with
`0 |-> list(.ValSeq)`, contradicting the mutated one-empty-string result.

Body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`.  With the body changed from
`in` to `not in`, the witness `["a"], "a"` returned an empty list rather than
the required `["a"]`.

Opposite-value probe:

```bash
kprove spec-value-opposite.k \
  --definition verification-kompiled \
  --spec-module SPEC-VALUE-OPPOSITE
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual was
`iCons(97, .IntSeq)`, not the deliberately claimed `.IntSeq`.

Independent CPython differential evidence:

```bash
python3 differential_test.py
```

Actual result, exit 0:

```text
cases=3200 mismatches=0
```

The oracle uses Python's `filter` plus native substring membership, independently
of the implementation's explicit loop and independently of the K summary
equations.  Inputs exhaust strings over `{a,b}` of lengths 0–2, lists of
lengths 0–3, and eight patterns including empty and absent patterns.

During construction, a focused entry-only invocation was interrupted after it
kept unrolling.  Bounded `--depth 20` and `--depth 40` diagnostics showed that
`--claims SPEC.filter-by-substring` had filtered the loop circularity out of
the proof theory.  This was diagnostic, not a required positive proof command.
The correct complete command above retains both claims and closes with `#Top`.

# Gate results

## Gate A — PASS

- A1: `solution.mpy` is freshly generated from `solution.py`; the entry claim
  embeds that exact module and function body.  The body executes under fixed
  semantics.  The `in` to `not in` mutation is rejected.
- A2: no operational bridge skips state.  The loop claim accounts for the
  local target update, result-list heap mutation, continuation, and preserved
  cells.
- A3: module/function binding, lookup, argument order, call frame, local
  bindings, method dispatch, return, and frame pop execute under the supplied
  rules.  The normalization lemma changes an operand only under an exact
  equality and leaves fixed `applyCmp` execution in place.
- A4: all total definitions have exhaustive, disjoint constructor equations.
  The two recursive `filterAcc` cases have complementary guards and strict
  descent; the function is deliberately not marked total outside its stated
  domain.  Overlaps with fixed equations agree.
- A5: the empty-list witness satisfies the precondition.  The false result
  postcondition exits 1.  Ground true/false membership values and the opposite
  projection probe have the expected polarity.

## Gate B — PASS

- The formal input restriction matches `List[str]` and `str`; no silent
  strengthening beyond the prompt's annotations is used.
- The supplied semantics models a string as an `IntSeq` and membership as
  contiguous occurrence.  This matches the property used by the prompt.  Its
  concrete literal loader is ASCII-only, while the symbolic theorem ranges
  over arbitrary code sequences; concrete evidence is therefore ASCII, not a
  claim of exhaustive CPython Unicode testing.
- `filterAcc` is both connected to actual execution by the loop claim and
  definitionally expresses the requested order-preserving filter.
- The implementation and prompt examples agree.

## Gate C — PASS

- Trust ledger: the supplied read-only `MPY` semantics, K frontend/backend,
  solver, and fixed `py2mpy.py` translator are the proof infrastructure.
  There are no proof-local trusted primitives or opaque result oracles.
- Every cited concrete, differential, mutation, and value-sensitivity artifact
  exists in this directory and is invoked by `prove.sh`.
- Universal correctness is attributed only to the `#Top` reachability proof.
  The 3,200-case differential run and two LLVM examples are reported only as
  finite evidence.

# Trust boundary and excluded behavior

Trusted infrastructure is the supplied `reference-semantics/`, K v7.1.293 and
its Haskell/LLVM backends and solver stack, CPython's parser as used by the
fixed translator, and the fixed `py2mpy.py`.  The proof does not validate those
components themselves.

Excluded behavior:

- values outside the annotated `List[str]`, `str` domain;
- Python subclasses, custom containers, mutation/aliasing behavior outside the
  supplied MPY subset, concurrency, I/O, or exceptions not modeled here;
- a separate termination/liveness theorem;
- exhaustive Unicode differential testing (the symbolic property is over
  arbitrary `IntSeq`, while concrete MPY literals in this semantics are
  ASCII-only).

The proof-quality headline `VALIDATED` is independent of the runner marker
`KPROVE_PASSED`: the former records Gates A–C, while the latter records only
successful positive target-proof execution.
