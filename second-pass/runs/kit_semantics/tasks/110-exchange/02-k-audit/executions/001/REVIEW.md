# Independent adversarial review: 110-exchange

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted MPY program over the material non-empty integer-list domain. The
proof is unbounded in both list lengths, executes the submitted function body,
and constrains the returned string. I do not accept the candidate's stronger
`VALIDATED` claim without qualification: its formal precondition also admits
arbitrary K `Float` values, while the submitted Python implementation and the
trusted canonical implementation disagree on fractional-float cases. The
proof-local Float promotion rules are also conditional on the supplied opaque
`floatMod`/`eqF` primitives. Those are non-fatal limitations because they
broaden rather than narrow the ordinary integer even/odd contract.

The complete command index is
[`evidence/COMMANDS.md`](evidence/COMMANDS.md). All builds and experiments used
the scratch copy below `/tmp/audit-work/scratch/proof`; no candidate-provided
compiled definition or cache was used.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `110-exchange`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- a mounted trusted semantics tree.

This agrees with the rendered task. `/reference/reference-semantics` is
present, so there is no mode/mount contradiction.

The campaign object in `/audit-campaign-lock.json` is exactly equal to
`audit_campaign` in `/audit-input.json`, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The mounted `/run.json`, `/task.json`, `/generation-result.json`, invocation,
metrics, runtime metrics, usage, prompt, last message, output log, trusted
prompt, translator, and canonical file all reproduce their recorded file
hashes.

Every required pipeline-v3 record is present, readable, and of the expected
regular-file or real-directory type. I read all small records, indexed all
53,479 lines of `/generation-evidence/codex-output.log`, and parsed every one
of the 615 structured-trace JSONL events. The trace contains one valid JSONL
file, no invalid JSON, and no symlink. Its file hash matches
`/generation-result.json`; its pipeline tree digest
`aa73c7f29f06e1bfcdd9e3c58a4a58c8549d5ac63dabad5003faf6b98cc2837b`
matches `/generation-evidence/usage.json`.

The independently recomputed pipeline tree digest of `/candidate` is
`94260d2db16cf846f8a36e8dc5504a95ccd82fed5d3c3d3a9c6485d022bc7659`,
matching both the generation result and invocation. The candidate prompt and
translator are byte-identical to `/reference/prompt.py` and
`/reference/py2mpy.py`.

The recursive supplied-semantics comparison found 25 entries in each tree
(one helper directory and 24 regular K files), zero missing/additional/type/
content differences, and zero symlinks. Both trees have pipeline digest
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching the task manifest and audit manifest hash. Thus the candidate did not
alter, add to, mistype, or replace the supplied semantics.

The candidate contains all required proof artifacts:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md`. Candidate-built `*-kompiled` directories, logs, prose, and traces
were treated only as untrusted claims.

Evidence:

- [`stage1/integrity.log`](evidence/stage1/integrity.log)
- [`stage1/records.log`](evidence/stage1/records.log)
- [`stage1/generation-output-index.log`](evidence/stage1/generation-output-index.log)
- [`stage1/trace-index.log`](evidence/stage1/trace-index.log)

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks about two non-empty lists of numbers. Elements may be
exchanged between the lists without a bound on the number of exchanges. The
result must be `"YES"` exactly when `lst1` can be made entirely even, and
`"NO"` otherwise.

The trusted canonical implementation counts:

- odd elements in `lst1`; and
- even elements in `lst2`;

then returns `"YES"` iff the latter count is at least the former.

The candidate instead counts every even element in the combined pool and
returns `"YES"` iff that count is at least `len(lst1)`. For integer elements,
these are equivalent because

`odd(lst1) = len(lst1) - even(lst1)`.

Therefore

`even(lst2) >= odd(lst1)`

is equivalent to

`even(lst1) + even(lst2) >= len(lst1)`.

The candidate preserves both input lists and has no other externally visible
effect.

### Translation identity

I regenerated MPY with the trusted translator:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

`cmp -s` exited 0. Both files have SHA-256
`0077aac3b5961f9ff24b495c0a1c710b6dcd4ec9d1c18c1d387a380c8dba331e`.
Thus the submitted `solution.mpy` is exactly the trusted translation of the
submitted `solution.py`.

### Independent differential evidence

The intended integer-domain differential imports the trusted canonical and
candidate entry points independently. It covers both documented examples,
empty robustness cases, below/equal/above branch thresholds, negative values,
arbitrarily large Python integers, all pairs of lists of length at most three
over `[-2,-1,0,1,2]`, and 10,000 seeded non-empty generated pairs. Result:

```text
cases=34349
mismatches=0
expectation_failures=0
```

The generated inputs and their digest are preserved.

A deliberately broader numeric exploration was also preserved. It found
1,384 canonical-versus-candidate mismatches. The smallest explicit witness is:

```text
lst1 = [2.5, -3.5]
lst2 = [4.25]
canonical = "YES"
candidate = "NO"
```

The canonical code counts only `% 2 == 1` values as obstructing `lst1`; the
candidate requires actual `% 2 == 0` values. This disagreement shows that the
candidate's statement that its Int/Bool/Float theorem is the unqualified full
canonical contract is too broad. It is not a material narrowing of the
ordinary integer even/odd domain: the candidate covers that domain
symbolically and the natural notion of odd/even together with the canonical
algorithm indicates that integers are the material domain. I nevertheless
retain this as a verdict-level concern because the trusted prompt says
"numbers" and contains no explicit type annotation.

Evidence:

- [`stage2/source-hashes.log`](evidence/stage2/source-hashes.log)
- [`stage2/mpy-byte-identity.log`](evidence/stage2/mpy-byte-identity.log)
- [`stage2/differential-intended.log`](evidence/stage2/differential-intended.log)
- [`stage2/differential-intended-inputs.txt`](evidence/stage2/differential-intended-inputs.txt)
- [`stage2/differential.log`](evidence/stage2/differential.log)
- [`stage2/differential-inputs.txt`](evidence/stage2/differential-inputs.txt)

## 3. Clean proof reconstruction

The scratch proof tree contains only copied source artifacts and the trusted
semantics. K version 7.1.293 was used.

I freshly built:

1. the trusted LLVM concrete definition (`MPY-KRUN`);
2. the bridge-free Haskell definition (`VERIFICATION-BASE`);
3. the connected Haskell definition (`VERIFICATION`); and
4. later, a fresh extended LLVM definition for numeric bridge testing.

All `kompile` commands exited 0. The compiler emitted warnings from the
supplied semantics and an LLVM exhaustiveness warning for guarded
`evenCount`; there was no build error. The `evenCount` guards are the exact
complements `numberEven(V)` and `notBool numberEven(V)`, so that warning is a
compiler coverage limitation rather than an uncovered mathematical case.

Independent concrete execution of eight documented/boundary integer cases
finished with `.K`, `NoExc`, and exit code 0.

All six claims in `connection-spec.k` were proved against
`VERIFICATION-BASE`, which excludes the final parity-composition bridge:

```text
kprove connection-spec.k \
  --definition verification-base-rebuilt \
  --spec-module CONNECTION-SPEC
#Top
exit 0
```

Each connection claim was also selected individually and closed with exit 0
and `#Top`. The three already-cooled pure-function claims report
`WarnTrivialClaim` because both sides normalize to the same base equations;
the three `*-exec` claims start from the actual `Compare(BinOp(...))`
constructor and exercise literal evaluation and operator routing.

`SPEC.count-loop` closes individually with `#Top`. The entry theorem depends
on this circularity. A diagnostic run selecting only `SPEC.exchange` was
interrupted after 23 minutes because the filter also removed `count-loop`,
forcing unbounded symbolic unrolling. This is not counted as a candidate
failure. With both target claims available, the clean required proof is:

```text
kprove spec.k \
  --definition verification-rebuilt \
  --spec-module SPEC
#Top
exit 0
```

This proves both the loop invariant and its dependent entry theorem.

Evidence:

- [`stage3/kompile-runtime.log`](evidence/stage3/kompile-runtime.log)
- [`stage3/krun-concrete.log`](evidence/stage3/krun-concrete.log)
- [`stage3/kompile-verification-base.log`](evidence/stage3/kompile-verification-base.log)
- [`stage3/kompile-verification.log`](evidence/stage3/kompile-verification.log)
- [`stage3/kprove-connection-all.log`](evidence/stage3/kprove-connection-all.log)
- [`stage3/kprove-positive-claims.log`](evidence/stage3/kprove-positive-claims.log)
- [`stage3/kprove-spec-all.log`](evidence/stage3/kprove-spec-all.log)

The clean reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.count-loop` says: in an ordinary function frame containing `lst1`,
`lst2`, integer `even_count = C`, and `value`, executing the actual submitted
loop over any finite numeric suffix `VS` consumes the loop and leaves
`even_count = C + evenCount(VS)`. It requires every suffix element to be a K
`Int`, `Bool`, or `Float`. It preserves the exact function-frame keys, parent
scope, empty heap, and arbitrary framed continuation.

`SPEC.exchange` says: from the supplied initial configuration, install the
submitted `exchange` binding, resolve and call it with arbitrary finite
non-empty numeric sequences `VS1` and `VS2`, execute its body, and return
`exchangeResult(VS1,VS2)`. `exchangeResult` is `"YES"` iff the combined
`evenCount` is at least `vsLen(VS1)`, otherwise `"NO"`. The claim also
requires restoration of environment, scope location, stack and return state,
an empty heap with unchanged allocation counter, `NoExc`, and exit code 0.
Only the final module-scope map is existential, which is appropriate because
installing the function binding is not part of the HumanEval observable
result.

### Mechanical program identity

The claim uses three macros: `countBody`, `exchangeBody`, and
`exchangeProgram`. I did not accept their comments as identity evidence.
Using the freshly compiled definition, I expanded:

- regenerated `solution.mpy`; and
- the claim term `exchangeProgram`;

to JSON KAST. `cmp -s` exited 0, and both expanded trees have SHA-256
`28e810f0d2d0dc3e6b9ab6148c9531aab915451620f33dbf11dcbe55178a54db`.
This constructor-level comparison pins the exact function name, parameters,
docstring expression, assignments, two `For` nodes, parity conditions,
`AugAssign`, `len` call, branches, and returns.

The `<k>` cell therefore executes the submitted program. It does not call an
answer oracle or replace either loop with `evenCount`.

### Satisfiable precondition and concrete substitution

`VS1 = vCons(1,.ValSeq)` and `VS2 = vCons(2,.ValSeq)` satisfy `allNumbers` and
both positive-length constraints. Substitution gives one even value and
`len(VS1)=1`, so the claimed result is `"YES"`. A ground K specialization
closed with `#Top`; both Python implementations also returned `"YES"`.

The entry represents read-only inputs as bare `list(VS)` values with an empty
heap. The supplied semantics expressly admits bare lists for read-only claim
inputs. Source list literals allocate references, but `For` and `len`
dereference those before the same material operations. Because this function
does not mutate its arguments or observe identity, the unboxed representation
does not change its result or control.

### Body sensitivity

A reviewer-authored mutation changed both actually loaded parity comparisons
from `== 0` to `== 1`, then required the original `"YES"` result on `[2],[2]`.
The spec built, executed the mutant to `"NO"`, and failed with exit 1 and
`WarnStuckClaimState`. This mutation changes the program term in `<k>`, not
merely an external source file.

Evidence:

- [`stage4/program-term-hashes.log`](evidence/stage4/program-term-hashes.log)
- [`stage4/program-term-identity.log`](evidence/stage4/program-term-identity.log)
- [`stage4/kprove-ground.log`](evidence/stage4/kprove-ground.log)
- [`stage4/ground-python.log`](evidence/stage4/ground-python.log)
- [`stage4/kprove-body-mutation.log`](evidence/stage4/kprove-body-mutation.log)

There is no substituted-program, free-result, tautology, or one-way-implication
gap.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The mechanical source inventory covers `reference-semantics/semantics.k`, all
23 helper files, `verification.k`, `connection-spec.k`, and `spec.k`. It
contains 1,162 declaration rows:

- 1,087 supplied-fixed rows, including 695 ordinary rules, 227 syntax
  declarations, five evaluation contexts, and the configuration;
- 59 proof-local rows, including all 15 syntax declarations and all 37 local
  rules;
- 10 connection-spec structural/claim rows; and
- six target-spec structural/claim rows.

Every row has an explicit decision and rationale in
[`stage5/rule-review.tsv`](evidence/stage5/rule-review.tsv). The supplied rows
are classified at the launcher-selected fixed-semantics level, with every
`[no-evaluators]` symbol separately marked as an opaque fixed trust boundary.
The program-construct routing is in
[`stage5/construct-map.md`](evidence/stage5/construct-map.md).

### Material fixed-semantics execution

Every submitted constructor has a declaration and execution path:

- module loading and statement sequencing;
- exact function binding, lookup, call-frame allocation and parameter binding;
- left-to-right argument and operator evaluation;
- assignment and integer augmentation;
- list iteration through `#iterNext/#iterYield/#iterDone`;
- condition evaluation and branch selection;
- `len(list(VS)) = vsLen(VS)`;
- return, abrupt removal of the remaining body, frame pop, environment
  restoration, and normal exception state; and
- string construction for `"YES"`/`"NO"`.

The loop claim is anchored on the real `#loop` control term created by
`For`. Its frame contains exactly the two parameters and two local variables
created by the submitted body. The final entry proof uses that circularity for
both syntactically identical loops.

### All proof-local rules

The 37 local rules divide exhaustively as follows.

1. **Three macro expansions.** They are exact, and mechanical expansion
   identity was established above. They have no post-expansion operational
   behavior.
2. **Three generated-sort predicates and fifteen guarded projection
   simplifications.** `definedProjectInt/Bool/Float` are exactly the generated
   sort predicates. Partial-cast definedness, forward/reverse orientation,
   collapse, and idempotence are guarded by the corresponding predicate.
   `project*Total` is opaque only off-sort; every off-sort occurrence in
   `numberEven` lies beneath a false Boolean conjunct, so it cannot choose a
   result or branch.
3. **Two `boolToInt` equations.** `false -> 0` and `true -> 1` are exhaustive
   and match Python Bool numeric coercion.
4. **Three primitive promotion rules.**
   `Bool % 2`, `Float % 2`, and `Float == 0` fill cases absent from the frozen
   subset. The Bool case is exact. The Float cases promote literals to
   `2.0`/`0.0` and delegate to supplied `floatMod`/`eqF`. The priority-40
   Float comparison specializes, consistently, the supplied mixed
   Float/Int route; it does not overlap a disagreeing Int or Bool case.
5. **Five domain rules.** `isNumberVal` is the sort-disjoint
   Int/Bool/Float union. `allNumbers` has an empty base and structurally
   descending cons case.
6. **One `numberEven` equation.** On each admitted sort exactly one
   definedness conjunct is true. It produces the same pure parity term as
   source evaluation; it is false for nonnumeric `Val` variants.
7. **Three `evenCount` equations.** The base is zero. The two cons equations
   descend on the tail and have complementary, non-overlapping guards.
8. **Two `exchangeResult` equations.** Integer `>=` and `<` guards are
   complementary and select different strings only on disjoint paths.
9. **Two final simplifications.** The composition bridge
   `applyCmp("==",applyBin("%",V,2),0) => numberEven(V)` is pure and applies
   only after operand/name/literal evaluation. The `#Ceil` lemma states
   definedness for numeric modulo by fixed nonzero 2. Neither touches a cell,
   continuation, stack, binding, heap, return, or exception.

The composition bridge's match domain is contained in its justification:
all six bridge-free claims quantify over arbitrary Int, Bool, or Float and
frame an arbitrary `<k>` suffix. The three execution forms start before
operator routing. Since this is a pure value computation, omitted state cells
are unaffected. The same source expression and summary use supplied
`floatMod`/`eqF`; this is interpretation-parametric rather than an
unconstrained value oracle.

I additionally ran the original program through the fresh extended LLVM
definition on eleven finite Float/Bool/mixed cases and ran the same assertions
in Python. Both completed. Opposite ground interpretations were rejected:

- even witness `2` reaches `true`, so a required `false` fails;
- odd witness `1` reaches `false`, so a required `true` fails.

### Static conclusion and limitation

No inventoried proof-local rule was found that can prove a false conclusion
about the submitted program on the material integer domain. Accordingly, I
make no unsupported "unsound rule" allegation requiring a false-conclusion
witness.

The Float primitive connection remains conditional: the bridge-free claims
prove equality inside the extended K theory, but do not independently prove
that the supplied opaque `floatMod` and `eqF` symbols implement all CPython
Float edge cases. Finite LLVM/Python tests support this boundary but do not
make it universal. This limitation affects only the candidate's extra
Int/Bool/Float scope, and is one reason for `CONCERNS` rather than `PASS`.

Evidence:

- [`stage5/rule-inventory.tsv`](evidence/stage5/rule-inventory.tsv)
- [`stage5/rule-review.tsv`](evidence/stage5/rule-review.tsv)
- [`stage5/construct-map.md`](evidence/stage5/construct-map.md)
- [`stage5/krun-numeric-bridge.log`](evidence/stage5/krun-numeric-bridge.log)
- [`stage5/kprove-opposite-even.log`](evidence/stage5/kprove-opposite-even.log)
- [`stage5/kprove-opposite-odd.log`](evidence/stage5/kprove-opposite-odd.log)

## 6. Fresh non-vacuity test

I did not rely on `/candidate/spec-vacuity.k`.

The reviewer-authored mutation uses the original submitted program and the
satisfying input `lst1=[2]`, `lst2=[1]`, but changes the required return from
the true `"YES"` to false `"NO"`.

Both Python implementations return `"YES"`. `kprove --dry-run` exits 0, so the
mutation parses and builds. The real proof then exits 1 with
`WarnStuckClaimState`. Its residual contains the reached ASCII string
`[89,69,83]` (`"YES"`) against the required `"NO"`, with normal final control
and state. The failure is therefore the intended unmet result obligation, not
a parser error, missing import, timeout, or unrelated crash.

Evidence:

- [`stage6/reviewer-vacuity.k`](evidence/stage6/reviewer-vacuity.k)
- [`stage6/witness.log`](evidence/stage6/witness.log)
- [`stage6/kprove-vacuity-dry-run.log`](evidence/stage6/kprove-vacuity-dry-run.log)
- [`stage6/kprove-vacuity.log`](evidence/stage6/kprove-vacuity.log)

The proof is result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### Machine-checked result

Conditional on the compiled theory, the successful reachability proof
establishes:

For arbitrary finite, non-empty K `ValSeq` inputs whose elements are all
`Int`, `Bool`, or `Float`, if the exact submitted translated `exchange`
program terminates normally from the specified initial state, its return is
`"YES"` exactly when

```text
evenCount(VS1) + evenCount(VS2) >= vsLen(VS1)
```

and otherwise is `"NO"`. Both actual loops execute, the local accumulator
equals the structural count, the call frame is popped, the environment and
allocation counters are restored, the heap is empty, the stack/return cells
are normal, no modeled exception is present, and exit code is zero.

The proof is symbolic and unbounded in both list lengths. It is not a finite
collection of examples or bounded unrolling.

### Trust and assumption ledger

1. **K prover/backend and builtin logic.** The K compiler, Haskell backend,
   reachability logic, integer/Boolean/string/map/list hooks, and their
   implementation are trusted. Every claim depends on this standard
   machine-checking boundary.
2. **Supplied semantics.** The 24 byte-identical trusted K files are the
   selected language model. The proof depends on their model of module load,
   values, frames, lists, loops, calls, returns, and operators. This is
   acceptable under `SUPPLIED_SEMANTICS`; it is not a claim of full CPython
   equivalence.
3. **Trusted translator bridge.** Trusted regeneration proves artifact
   identity between `solution.py` and `solution.mpy`, not universal semantic
   correctness of `py2mpy.py`. Constructor inspection and concrete
   differential execution support the bridge for this program.
4. **Proof-local macro transcription.** This is no longer merely assumed:
   expanded KAST identity mechanically pins it to `solution.mpy`.
5. **Bool promotion.** `boolToInt` and Bool modulo are ordinary, exhaustive
   Python numeric facts.
6. **Float primitives.** The candidate's Float modulo/equality route depends
   on supplied opaque `floatMod` and `eqF`, with concrete LLVM twins.
   Connection proofs are parametric in those meanings; finite tests support
   but do not universally validate CPython Float equivalence.
7. **Exchange combinatorics.** The bridge from the proved combined-even-count
   criterion to "some sequence of exchanges can make `lst1` all even" is an
   ordinary informal argument: exchanges preserve `len(lst1)` and permit any
   size-`len(lst1)` selection from the combined pool. Such a selection is
   all-even iff the pool contains at least that many even elements.
8. **Material source domain.** The proof fully covers non-empty integer lists,
   including arbitrary lengths and unbounded integers. Treating fractional
   floats as part of the canonical contract is ambiguous and exposes the
   recorded canonical/candidate mismatch; the candidate's broader
   `VALIDATED` wording is not accepted.
9. **Testing.** Differential, ground, mutation, and LLVM runs are finite
   evidence only. None substitutes for the K reachability proof.
10. **Partial correctness.** This review reports the Kit's partial-correctness
    result. It does not separately claim a CPython termination theorem or
    correctness for nonnumeric values, arbitrary Python numeric classes, list
    mutation/alias observations, or behaviors absent from the supplied model.

### Decision

Gate A passes: the proof is sound under its disclosed theory, pins and
executes the real submitted program, uses a justified loop circularity, and is
non-vacuous.

Gate B passes for the material HumanEval integer domain: the formal domain is
unbounded and includes it in full. There is no fixed-size restriction or
material precondition narrowing. The extra Float claim disagrees with the
trusted canonical on fractional cases, but does not make a false theorem about
the actually executed candidate program or exclude intended integer inputs.

The Float/canonical scope disagreement and opaque Float primitive bridge are
real, non-fatal audit limitations. They make the candidate's own
`PROOF.md` headline `VALIDATED` too strong and preclude an unqualified `PASS`,
but they do not invalidate the legitimate real-program proof on the material
source-contract domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
