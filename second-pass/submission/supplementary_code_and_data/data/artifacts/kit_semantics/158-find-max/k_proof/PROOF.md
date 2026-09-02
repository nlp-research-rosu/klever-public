VALIDATED

## What is proven

Under the supplied `MPY` semantics, the exact translated body of
`find_max(words)` is partially correct for every finite modeled list whose
elements are strings.  If the call terminates, it returns the fold

```k
bestWord(WORDS, str(.IntSeq), 0 -Int 1)
```

where each candidate's score is
`isLen(dedupCodes(character-codes))`; a candidate replaces the current best
when its score is larger, or when the score is equal and `strLt` says the
candidate is lexicographically smaller.

The theorem is unbounded in both list length and string length.  It does not
assume that the words are distinct, so it covers a superset of the prompt's
stated input domain.  On the empty list the implementation returns `""`; this
is an explicit extension at the otherwise maximum-free boundary.

This is a partial-correctness result.  Termination is not a conclusion of the
Kit reachability proof.

## Formal claim and observable state

`SPEC.find-max` starts with the exact `Module(FuncDef(...))` emitted for
`solution.py`, loads it, looks up and calls `find_max`, binds the unboxed
symbolic `list(WORDS)`, executes the function body, returns, and pops its call
frame.  Its only precondition is `allStrings(WORDS)`.

The destination constrains the returned `<k>` value to the fold above and also
constrains the final environment, module binding, scope allocator, heap, call
stack, return cell, exception cell, and exit code.  In particular, it ends at
environment 0 with an empty heap and stack, `noRet`, `NoExc`, and exit code 0.

`SPEC.loop-inv` is the circularity for the arbitrary remaining `ValSeq`.  It
threads the best word and score plus the final values of the loop target
`word` and temporary `unique`.  Its exact loop body is the body embedded in
`solution.mpy`.

## Rebuilt proof-extension inventory

The inventory below was reconstructed from the final `verification.k` and
`spec.k`, not copied from the construction notes.

| Extension | Class and semantic role | Complete domain/context and state footprint | Value/control justification, dependents, and validation |
|---|---|---|---|
| `definedProjectStr`, `projectStrTotal`, its `#Ceil` rule, guarded cast orientations, collapse, idempotence, and `codesOf` | Definitional summary plus derived sort-projection lemmas. They refine a dynamic `Val` to the existing `Str` subsort; they do not rewrite a program control term. | Term context only; no continuation or configuration cells. Cast orientation fires only under `definedProjectStr(V) = isStr(V)`. Collapse applies to an already-static `Str`. Off the guard, the total projector has no evaluator or value-producing rule. | The guarded orientation equates the projector with K's built-in partial subsort cast; `codesOf(str(CS)) = CS`. Values affect scoring and comparison, but only on the guarded string domain. No control/state effect. All target claims depend on this refinement. Constructor-domain fixed equations are checked in `connection-spec.k`; concrete and differential witnesses exercise distinct score and tie outcomes. |
| `allStrings` | Definitional domain predicate. | Total over `.ValSeq` and `vCons(V, REST)`; it requires every head to satisfy the generated `Str` sort predicate and also rules out heap references. No cells or control. | Exactly describes the modeled list-of-strings domain and supplies the guard for every projection use. `SPEC.find-max` and `SPEC.loop-inv` depend on it. |
| Guarded `applyBuiltin("set", V, .Vals)` twin | Derived dispatch lemma; it restates fixed `set(str(CS))` at the dynamic supersort. | Any term context, guard `definedProjectStr(V)`. No continuation is discarded, and no cell is read or written. Its match domain is exactly the existing static string case after guarded projection. | RHS is the fixed equation `setV(dedupCodes(CS))` with `CS = codesOf(projectStrTotal(V))`. It affects `unique` and the result branch. `CONNECTION-SPEC.set-str-connection`, compiled without `VERIFICATION`, proves the universal fixed constructor equation. The overlap with the original static rule has the same RHS. |
| Guarded `applyCmp("<", A, B)` twin | Derived dispatch lemma; it restates fixed string `<` at the dynamic supersort. | Any term context, guard that both operands satisfy `definedProjectStr`. No state or control effect. The match domain is exactly two projected static strings. | RHS is the fixed `strLt` equation over the two code sequences. It affects only the tie branch. `CONNECTION-SPEC.str-lt-connection`, without `VERIFICATION`, proves the universal fixed constructor equation. The overlap with the original rule agrees. |
| `uniqueCount`, `candidateWins` | Total definitional summaries. | All declared arguments; the target uses them only where `allStrings` and the best-string invariant supply projection guards. No cells/control. | Exact composition of supplied `dedupCodes`, `isLen`, integer comparison, and `strLt`. They determine score and replacement. Equations are unconditional and terminating. |
| `bestWord`, `bestScore`, `lastWord`, `lastScore` | Total definitional fold summaries; they name mathematical state and do not replace program execution. | Exhaustive `.ValSeq`/`vCons` cases, with structural descent on the tail and a total Boolean `#if`. No configuration match or state effect. | `bestWord`/`bestScore` use exactly `candidateWins`; the `last*` functions describe the two other loop-written locals. Both claims depend on them. Base/step execution is established by the machine-checked circularity, not assumed as a postcondition rule. |
| `SPEC.loop-inv` | Derived auxiliary reachability claim/circularity. | Exact `#loop(list(WORDS), Name("word"), BODY)` with an arbitrary trailing continuation; environment 1; exact module, builtins, and local scopes; empty heap; arbitrary preserved stack; `noRet`, `NoExc`, exit 0. | Fixed semantics executes lookup, `set`, `len`, comparisons, assignments, iteration, and loop control. It writes only `result`, `max_unique`, `word`, and `unique`; it preserves `words`, module/builtins, heap, stack, exception, and suffix. There is no abrupt control in the body, so the arbitrary suffix is contained. The isolated claim prints `#Top`. `SPEC.find-max` depends on it. |
| `SPEC.find-max` | Positive target reachability claim. | Exact module load, exact closure body/binding, one symbolic list argument, exact initial and final configuration. | Fixed semantics executes call evaluation, binding, body, return, and frame cleanup. It depends on the loop circularity and summaries. The complete all-claims command prints `#Top`. |

There are no opaque program-result oracles and no rule that returns from,
skips, or replaces the program-defined function body.

## Commands and actual results

The complete reproducible runner is `prove.sh`.  The final recorded run was:

```bash
./prove.sh > prove.out 2>&1
```

Actual result: exit 0.

The required positive target proof command was:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output: `#Top`; exit 0.  This command proves all claims together, so the
entry claim can use the unbounded loop circularity.

The supporting isolated invariant command was:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-inv
```

Actual output: `#Top`; exit 0.

The bridge-free fixed-equation command was:

```bash
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
```

Actual output: two `WarnTrivialClaim` notices (the fixed function equations
simplify immediately), then `#Top`; exit 0.

LLVM execution used:

```bash
krun concrete_tests.mpy --definition runtime-kompiled
```

Actual final cells include `.K`, `NoExc`, and exit code 0; process exit 0.

The false-result mutation used:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`; the residual return is
`str(iCons(97, .IntSeq))` (`"a"`) while the mutated destination requires `""`.

The material body mutation used:

```bash
krun body_mutation.mpy --definition runtime-kompiled
```

Actual result: exit 1, `AssertionError`, and exit-code cell 1.  Changing
`max_unique = -1` to `max_unique = 100` changes the `["a"]` result and is
detected.

The independent differential command was:

```bash
python3 differential_test.py
```

Actual output:

```text
cases=6104 mismatches=0
```

## Gate results

### Gate A — PASS

- A1: the target claim embeds the exact translated function body and executes
  it through module load, lookup, call, return, and pop.  The material body
  mutant changes observable behavior and fails.
- A2/A3: no proof rule skips control or mutates state.  The two dynamic
  dispatch lemmas are value-only, exactly guarded restatements of existing
  static equations.  Name binding remains the supplied semantics' lookup
  through the exact callee/module/builtins scopes.
- A4: definitional functions have exhaustive disjoint constructor cases or
  unconditional equations with structural descent.  Projection use is guarded;
  overlaps with fixed static dispatch agree.
- A5: `["a"]` is a realizable witness.  The false-result K mutation is rejected
  with the correct `"a"` residual.

The Haskell backend cannot use `isStr(V)` alone to refine a symbolic `V:Val`
to the `str(CS)` constructor; a fixed-only constructor-split invariant was
therefore explored and produced the genuine stuck dynamic `set(V)` residual.
The final guarded-total-projection construction is the Kit's sort-refinement
idiom: it preserves the fixed value through the partial cast and restates only
the already checked static equations.

### Gate B — PASS

- The input is an arbitrary finite `ValSeq` satisfying `allStrings`; there is
  no bound on list or string length.
- Distinctness is not required by the theorem, so the prompt's distinct-word
  lists are included.
- The result summary directly encodes maximum unique-character count and
  lexicographically smallest tie-breaking, and the invariant threads that
  summary through every loop iteration.
- The empty-list return `""` is an explicit additional behavior, not a domain
  exclusion.
- The fixed model represents a string as an `IntSeq` and orders its integer
  codes.  The proof covers every string value represented by that model.
  CPython's full Unicode/runtime representation remains a model boundary, not
  a theorem-side length or alphabet restriction.

### Gate C — PASS

Every named assumption and validation artifact is recorded below, all commands
exist in `prove.sh`, all positive commands have current `#Top`/exit-0 results,
and both negative probes have the expected nonzero results.

## Trust boundary

| Component | Why outside this theorem | Influence and dependents | Evidence |
|---|---|---|---|
| Supplied read-only `reference-semantics/` | The task grants this as the Python model. | Defines all program values, binding, control, `set`, `len`, distinct-code folding, and lexicographic comparison; all claims depend on it. | LLVM examples, bridge-free fixed-equation claims, false-result residual, and differential tests. |
| K v7.1.293 Haskell/LLVM backends and solver | Proof-checking implementation and backend correctness are metatheoretic trust. | All `kompile`, `krun`, and `kprove` conclusions. | Exact versions and replayable `prove.sh`; final runner exit 0. |
| K generated subsort predicate/cast law | The guarded projection relies on `isStr` and the built-in `Val :> Str` cast preserving a value in the declared subsort. | Only dynamic-to-static value refinement; no control/state effect. | Explicit `#Ceil`, guarded orientation, collapse, and idempotence rules; universal fixed constructor equations; ground and differential witnesses. |
| Partial-correctness termination boundary | Kit reachability result does not establish termination as a separate liveness theorem. | The postcondition is conditional on termination. | Finite concrete execution and the structurally decreasing source loop support, but do not formally prove, termination. |

`projectStrTotal` has no evaluator off `definedProjectStr`; no target-dependent
use occurs off that guard.  The supplied opaque sort primitives are not used by
this implementation or proof.

## Empirically supported facts and excluded behavior

- `concrete_tests.py` covers all prompt examples, score preference, pure
  lexicographic ties, and the chosen empty-list behavior under the supplied
  LLVM semantics.
- `differential_test.py` uses Python's independent
  `sorted(words, key=(-len(set(word)), word))` oracle over prompt cases,
  exhaustive permutations of a representative pool, deterministic random
  distinct lists, empty strings/lists, and Unicode witnesses: 6,104 cases,
  zero mismatches.
- Finite tests support the semantics-to-CPython adequacy boundary; they are not
  used as a universal proof.
- Inputs containing non-strings are excluded because the prompt requires a
  list of strings and the fixed `set` operation is undefined for them here.
- Python exceptions, mutation/aliasing of input lists, concurrency, I/O, and
  other behavior outside the pure entry call are not claimed.
