# Independent adversarial audit: HumanEval/9 `rolling_max`

This audit reconstructed the proof from source and did not rely on the
candidate's compiled artifacts, logs, final report, or prior `#Top`. The
completed result is **PASS / LEGIT**. The theorem is an unrestricted
partial-correctness result for every finite list of mathematical integers, it
executes the submitted translated function body, and its returned heap object
is constrained to the rolling-prefix maxima.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `9-rolling-max`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`; and
- a mounted supplied-semantics baseline.

That mode agrees with the mounts: `/reference/reference-semantics` exists.
The selected legacy layout does not require a historical
`runtime-metrics.json`; its absence is not an infrastructure defect.

I independently checked all launcher-required paths and hashes. The campaign
lock is byte-hash identical to the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
and its parsed object exactly equals the `audit_campaign` block in
`/audit-input.json`. The run, task, stage result, invocation, metrics, usage,
prompt, Codex output, Codex last message, canonical source, trusted prompt, and
trusted translator all match their recorded SHA-256 values. See
[stage1_integrity.log](evidence/stage1_integrity.log) and the exact
[integrity command record](evidence/stage1_integrity.command.txt).

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. The candidate and trusted
supplied-semantics trees each contain the same 25 relative entries. Every
corresponding entry has the same type and bytes; neither tree contains a
symlink; and there are no missing or additional entries. Both independently
generated entry manifests hash to
`a41aed4aa0130a1ec22435b2c3e43a8ef2284802d55ce5b4f703e8483bef2446`.

I parsed the complete structured trace rather than accepting its final
message. It contains 361 valid JSONL records and 76 paired tool calls/results;
the trace file's hash matches the invocation record. All required selected
generation records were also parsed as JSON, and the text records were scanned
in full. This establishes provenance only; the trace's proof claims were not
used as proof evidence. The parser, bounded extracted record, and command
record are [stage1_generation_records.py](evidence/stage1_generation_records.py),
[stage1_generation_records.log](evidence/stage1_generation_records.log), and
[stage1_generation_records.command.txt](evidence/stage1_generation_records.command.txt).

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for `rolling_max(numbers: List[int]) -> List[int]`:
for each input position, return the greatest integer seen in the prefix ending
at that position. The documented example is
`[1,2,3,2,3,4,2] -> [1,2,3,3,3,4,4]`; the empty input naturally produces an
empty output.

The trusted canonical implementation keeps an optional running maximum. The
candidate uses an equivalent `first` Boolean: the first element initializes
`maximum`; every later element assigns `max(maximum, number)`; and each current
maximum is appended. This handles negative first elements correctly despite
the otherwise unused initial `maximum = 0`.

Using the trusted translator copied from `/reference/py2mpy.py`, I regenerated
the submitted `solution.mpy`. `cmp` reported byte identity and both files have
SHA-256
`1c682e0bf38512e253f987a9d81ae683cb33d65aac2f1b93b1e64a741dfdcdca`.
Commands and statuses are in [stage2_commands.txt](evidence/stage2_commands.txt).

The independent differential script imports the trusted canonical module and
the candidate generated Python module by distinct paths. It covers:

- the documented example;
- empty and singleton inputs;
- first-element initialization;
- later values below, equal to, and above the current maximum;
- negative, zero, very large positive, and very large negative Python
  integers;
- monotone lists of length 1,000;
- all 19,531 lists of lengths 0 through 6 over
  `{-2,-1,0,1,2}`; and
- 3,000 seeded generated lists of lengths 0 through 100.

Across 22,545 inputs there were zero candidate/canonical mismatches, zero
formal-summary/canonical mismatches, and zero input mutations. The serialized
test-input digest is
`62c01fe0fc12dad4ecc8ee6433b77d3935d7c82b6edbd466cd164a1ca99609ce`.
The complete reproducible scope is encoded in
[differential_test.py](evidence/differential_test.py), with results in
[differential_test.log](evidence/differential_test.log). These finite tests
support fidelity and the summary-to-contract bridge; they do not substitute
for the universal K proof.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/9-rolling-max`, using the
trusted supplied-semantics tree rather than a candidate-built definition. No
candidate compiled definition or cache was copied or referenced. The installed
`kompile` and `kprove` report K version `7.1.293`.

Fresh reconstruction produced these results:

| Target | Result |
|---|---|
| LLVM `MPY-KRUN` definition | exit 0 |
| Concrete `concrete-tests.mpy` execution | exit 0; final `.K`, `NoExc`, exit code 0 |
| Haskell `VERIFICATION` definition | exit 0 |
| Full `SPEC` containing both positive claims | exit 0; `#Top` |
| `SPEC.rolling-max-loop` alone | exit 0; `#Top` |
| End-to-end selection with the separately proved loop claim trusted | exit 0; `#Top` |

The exact commands, definitions, and status records are in
[stage3_commands.txt](evidence/stage3_commands.txt). Bounded native output is
preserved in
[stage3_krun_concrete_tests.log](evidence/stage3_krun_concrete_tests.log),
[stage3_kompile_haskell.log](evidence/stage3_kompile_haskell.log),
[stage3_kprove_all.log](evidence/stage3_kprove_all.log),
[stage3_kprove_loop.log](evidence/stage3_kprove_loop.log), and
[stage3_kprove_correct_using_proved_loop.log](evidence/stage3_kprove_correct_using_proved_loop.log).

The fixed semantics emits warnings about unused variables and total functions
on unrelated value constructors. Those warnings are part of the trusted
supplied tree, do not prevent either build, and concern operations unreachable
from this integer-list function.

## 4. Adequacy and real-program pinning

### Claims in plain language

`rolling-max-loop` starts at the real fixed-semantics `#loop` head for an
arbitrary finite `IntSeq`, with:

- the actual loop target `number` and actual `rollingMaxLoopBody`;
- an exact callee frame containing `result`, `first`, `maximum`, `number`, and
  `numbers`;
- the exact module/builtins parent chain; and
- an existing heap list `ACC`.

It says that after the loop, the original continuation resumes; `result`
contains the old accumulator followed by the recurrence's rolling maxima;
`first`, `maximum`, and `number` have their exact final values; and all omitted
cells are framed.

`rolling-max-correct` starts from the exact fresh MPY configuration and executes
`#loadAll(rollingMaxModule)` followed by a call of the loaded `rolling_max`
binding on `list(intsVS(INPUT))`. It says the call returns `ref(0)`, whose heap
object is exactly `list(rollingAcc(INPUT,true,0,.ValSeq))`; the module binding,
allocation counters, stack, return state, exception state, and exit code are
also fixed. The returned value is therefore not free, existential, a
tautology, or merely related by a one-way implication.

### Mechanical program identity

I parsed the regenerated `solution.mpy` and the claim's
`rollingMaxModule` expression using the fresh proof definition, with recursive
macro expansion enabled. Their JSON constructor ASTs are byte-identical and
share SHA-256
`4394dffbc12f4e0fe30a8c342080d767b2ce786a77fd5f76f9531550d372e53a`.
This mechanically validates list-sugar normalizations such as
`"List"` versus `("List",.ParamNames)` and proves that the claim executes the
same function binding and body submitted in `solution.mpy`. See
[stage4_commands.txt](evidence/stage4_commands.txt).

The omitted `Tuple` typing import from the canonical source is irrelevant:
candidate `solution.mpy` is regenerated from candidate `solution.py`, and
typing-only imports do not affect this function result. The program macro
actually includes the submitted `from typing import List` node and docstring.

### Satisfiability, concrete substitution, and sensitivity

[ground-instances.k](evidence/ground-instances.k) gives an exact state
satisfying the loop precondition for input `[4,2,7]`, as well as exact entry
states for `[]`, `[-8,-9,-3,-3,-10]`, and `[5,5,4,6,1]`. All four claims close
with `#Top`; their expected heap lists are respectively `[4,4,7]`, `[]`,
`[-8,-8,-3,-3,-3]`, and `[5,5,5,6,6]`. Both Python implementations produce
the same results. This exhibits satisfying states for both entry shapes and
concretely substitutes values into the claimed result.

An end-to-end-only diagnostic with the loop claim excluded and depth 100 stops
inside the second symbolic loop iteration, rather than jumping to the result.
That residual demonstrates that the helper claim is exercised.

For body sensitivity, I changed the call in the executed macro from `max` to
`min`, rebuilt a separate definition, and retained the original postcondition.
The build succeeds, but proof exits 1 with a meaningful residual requiring
`maximumAfter` and `rollingAcc` computed with `maxInt` to equal the mutated
execution computed with `minInt`. The preserved source and log are
[verification-body-mutation.k](evidence/verification-body-mutation.k) and
[stage4_body_mutation_kprove.log](evidence/stage4_body_mutation_kprove.log).
This mutation changes the actual claim term, not merely an external source
file.

The formal domain is all finite `IntSeq` values, hence all finite lists of K
mathematical integers. There is no length or magnitude bound and no material
narrowing of the annotated HumanEval `List[int]` domain.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I read all 2,345 source lines in the supplied semantics, verification, and
specification. The mechanical inventory covers 26 K files and 1,124
declaration/items, including:

- 236 syntax declarations;
- 713 rules: 240 operational and 473 equational;
- five evaluation contexts;
- 47 priority-bearing items;
- 150 function-bearing declarations;
- 112 total declarations;
- 35 concrete-bearing items; and
- 22 fixed-semantics opaque symbols.

There are no `functional`, `simplification`, or `anywhere` declarations in
these sources. The complete exact-text inventory is
[static_inventory.json](evidence/static_inventory.json), generated by
[static_inventory.py](evidence/static_inventory.py); a line-oriented cross-check
is [rule_inventory_raw.txt](evidence/rule_inventory_raw.txt).

Every inventory item has an explicit disposition and rationale in
[rule_assessments.json](evidence/rule_assessments.json): 103 materially used
fixed entries, 21 concrete-only entries, 22 unused fixed opaque boundaries,
29 individually sound candidate proof/spec entries, and the remaining
structural or unreachable fixed-subset entries. No inventoried candidate rule
was left unclassified.

### Used-language coverage

The constructor map and active rule path are:

| Submitted construct | Declaration and material rules |
|---|---|
| `Module`, `ImportFrom`, statement sequence | `syntax.k`; `core.k` load/sequence; `controls.k` typing-import no-op |
| `FuncDef`, `Params`, call, return | `functions.k` definition/bind/return/pop; `call.k` callee/argument/frame rules |
| `ListExpr` and returned heap object | `list.k` construction; `core.k` left-to-right argument evaluation and `#alloc` |
| `For` and target `Name("number")` | `controls.k` `#loop`; `tuple.k` name target binding |
| `If(Name("first"),...)` | strictness plus `controls.k` branch rules and `core.k` Boolean truth |
| `max(maximum,number)` | builtins lookup, generic call dispatch, `builtins.k` `maxVals`, K `maxInt` |
| `result.append(maximum)` | attribute/bound-method dispatch and `list.k` in-place append |
| docstring expression | `str.k` ASCII literal conversion and `controls.k` value discard |

This path preserves left-to-right argument evaluation, lexical lookup,
allocation, mutation of the result list, callee stack/frame lifecycle, abrupt
return, and every observable cell modeled by the fixed semantics. The input
list is represented as the fixed semantics' permitted bare read-only list;
the program never mutates or aliases it.

`MPY-CONCRETE` is imported only by the LLVM definition, not by
`VERIFICATION`. The 22 opaque digest, float, and sort symbols belong to the
fixed supplied semantics and are all unreachable here. No target claim
depends on their interpretation.

### Candidate proof extensions

| Extension | Class and audit result |
|---|---|
| `rollingMaxLoopBody`, `rollingMaxBody`, `rollingMaxModule` | Definitional macros. Macro expansion is mechanically identical to submitted `solution.mpy`; they replace no execution. |
| `intsVS` and its two equations | Definitional embedding. Empty/cons guards are exhaustive and disjoint; recursion descends on the `IntSeq` tail. |
| Two priority `#iterNext(list(intsVS(...)))` rules | Operational bridges. They produce exactly the fixed list iterator's done/yield value and remainder, preserve arbitrary `CONT`, and omit no changed cell. |
| `nextRolling` | Total definitional summary. Boolean cases are disjoint and exhaustive; `maxInt` is ordinary integer maximum. |
| `rollingAcc` | Total structural fold. Constructor cases are disjoint, recursion descends, and it appends exactly each new running maximum. |
| `firstAfter` | Total summary. Its `FIRST=false` rule overlaps the empty and cons rules only where both right-hand sides are `false`; all overlaps agree. |
| `maximumAfter`, `numberAfter` | Total structural summaries with disjoint constructor cases and strict tail descent. |

There are no proof-local opaque symbols or unconstrained result values. The
only proof-local priority rules are the two iterator bridges.

For those bridges, simply deleting them while retaining `intsVS` as an
ordinary non-function rule leaves `#iterNext(list(intsVS(...)))` stuck: K does
not contextually reduce that symbol under the iterator. I preserved this
diagnostic in
[stage5_bridge_connection_kprove.log](evidence/stage5_bridge_connection_kprove.log).
It explains the acceleration but does not justify its value.

I then constructed a bridge-free connection definition using the candidate's
exact two exhaustive `intsVS` equations, declared as a total function so they
can evaluate under consumers, without importing either proposed bridge. The
empty and cons connection claims quantify over arbitrary `CONT` and
automatically frame every other cell. Both close with `#Top`; see
[verification-iter-definitional.k](evidence/verification-iter-definitional.k),
[iter-bridge-connection-definitional.k](evidence/iter-bridge-connection-definitional.k),
and [stage5_bridge_definitional_kprove.log](evidence/stage5_bridge_definitional_kprove.log).
Because `IntSeq` has exactly empty/cons constructors, the `function,total`
presentation adds no oracle or value assumption. This supplies the universal
fixed-iterator connection and complete-context containment required for the
bridges.

The loop claim itself matches the exact real loop head and body. It accounts
for all locals written by target binding, branching, `max`, and append; its
arbitrary continuation is preserved; and the fixed execution changes none of
the omitted cells. No rule encodes a task answer while bypassing program
execution, and no rule admits a false conclusion on the intended domain.

## 6. Fresh non-vacuity test

The candidate supplied no artifact that I relied on for non-vacuity. I created
a fresh specification that changes only the end-to-end result heap from:

`list(rollingAcc(INPUT,true,0,.ValSeq))`

to:

`list(vCons(0,rollingAcc(INPUT,true,0,.ValSeq)))`.

The mutated specification is [spec-vacuity.k](evidence/spec-vacuity.k). A
`kprove --dry-run` exits 0, so the mutation parses and builds. The proof then
exits 1 with `WarnStuckClaimState` after real execution reaches `ref(0)`. Its
residual is exactly the unmet equality:

`rollingAcc(INPUT,...) = vCons(0,rollingAcc(INPUT,...))`.

For the satisfying witness `INPUT=.IntSeq` from `entry-empty`, this is
`.ValSeq = vCons(0,.ValSeq)`, which is false. This is not a parser error,
timeout, missing import, unreachable mutation, or unrelated crash. Exact
commands and statuses are in [stage6_commands.txt](evidence/stage6_commands.txt);
native output is [stage6_vacuity_kprove.log](evidence/stage6_vacuity_kprove.log).

## 7. Proven versus assumed accounting

### What the proof establishes

Under the supplied MPY semantics, for every finite sequence of K integers, the
freshly loaded submitted `rolling_max` function is partially correct: if its
execution terminates from the claim's initial state, it returns the fresh
reference `0`, that reference contains exactly the recurrence obtained by
taking the maximum of every nonempty input prefix, no exception is present,
and the stack/return/allocation/module state has the claimed final form.

The loop theorem additionally establishes the exact final values of all
loop-carried locals and the exact mutation of an arbitrary existing result
accumulator. The theorem is universal over list length and integer magnitude;
it is not finite unrolling or example-only verification.

### Trust and assumptions

1. **K toolchain and supplied semantics.** K `7.1.293`, its Haskell reachability
   backend, and the launcher-authenticated supplied MPY tree are trusted. The
   active subset used here was reviewed rule by rule. This is the normal
   low-level execution trust boundary, not a proof-local correctness oracle.

2. **K mathematical primitives.** K integers, Booleans, maps, lists, string
   hooks for the ASCII docstring, and `maxInt` are trusted according to their
   ordinary mathematical meanings. `maxInt` is the only result-bearing
   primitive in the rolling recurrence.

3. **Translation bridge.** `/reference/py2mpy.py` is a trusted benchmark input.
   The submitted `.mpy` was regenerated byte-identically, and its expanded
   constructor term was mechanically matched to the claim. No informal
   source-to-claim body transcription remains.

4. **Intent bridge.** The statement that the simple
   `nextRolling`/`rollingAcc` recurrence is “the maximum of every prefix” is
   ordinary induction on the finite input sequence. It is also independently
   supported, but not universally proved, by zero mismatches against the
   canonical implementation on 22,545 documented, exhaustive-small, boundary,
   long, and generated inputs.

5. **Input representation.** A finite `IntSeq` embedded into a bare MPY
   `list(ValSeq)` stands for a Python `List[int]`. This excludes non-integers
   exactly as the source annotation does. The candidate neither mutates nor
   observes the identity of the input, so the bare read-only representation
   loses no material behavior.

6. **Unused fixed primitives.** The supplied semantics contains 22 explicit
   opaque float, digest, and sort symbols. None can be reached by this program,
   influence a branch or state, appear in a summary, or affect either target
   claim. They add no assumption to this theorem.

The proof does not claim behavior for non-list or non-integer inputs, arbitrary
unsupported Python programs, liveness/complexity, or behavior outside the
fixed semantics' represented subset. Those exclusions do not narrow the
HumanEval source-contract domain.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust
and reproducible evidence) all pass. There is no material adequacy gap,
unconstrained oracle, substituted program, bounded domain, vacuity, or
unsound rule supporting the result.

VERDICT: PASS
LEGITIMACY: LEGIT
