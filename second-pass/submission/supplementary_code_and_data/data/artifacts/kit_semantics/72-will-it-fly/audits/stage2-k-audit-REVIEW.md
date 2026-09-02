# Independent adversarial audit: 72-will-it-fly

## Outcome

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated program over the material HumanEval domain evidenced by
the trusted prompt: finite integer lists and an integer capacity (with the
supplied model also admitting homogeneous Boolean values). I rebuilt every
positive definition and claim from source in a new scratch directory, obtained
`#Top` with exit status 0 for every target claim, mechanically matched the
executed closure body to the trusted regeneration of `solution.mpy`, and made a
fresh false result obligation fail with the expected reachable residual.

I assign `CONCERNS / LEGIT`, rather than `PASS`, because the untyped Python
contract-to-K domain boundary is informal. The supplied model uses
constructor equality for list elements, so cross-sort Python numeric equality
is not modeled (for example, Python regards `[1, True]` as palindromic, whereas
the K `Int`/`Bool` constructors differ). The extra float claim is structural in
opaque fixed-semantics primitives and does not cover every mixed choice of
element and capacity sort. These are real but non-fatal limitations: they do not
narrow the material integer domain exhibited by every trusted example, and
they do not make a false integer-domain conclusion provable.

I followed the required Kit order: `using-kit`, then `validating-proof` and its
proof-extension soundness procedure. I did not use `writing-semantics`, because
the rendered mode is `SUPPLIED_SEMANTICS`.

All candidate and generation materials were treated as untrusted evidence.
All build products used below were freshly created under
`/tmp/audit-work/72-will-it-fly`; no candidate `*-kompiled` directory, cache,
binary, trace assertion, `#Top`, or `PROOF.md` conclusion was reused.

## 1. Input and provenance integrity

### Gate result

The infrastructure gate passed. `/audit-input.json` declares:

- problem `72-will-it-fly`;
- condition `kit-semantics`;
- `record_layout: pipeline-v3`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- a mounted trusted semantics tree.

`/reference/reference-semantics` is present, as this mode requires. There is no
rendered-mode contradiction and therefore no infrastructure breach.

The complete independent check and its reproducible script are
[01-infrastructure.log](/audit-output/evidence/01-infrastructure.log) and
[infra_check.py](/audit-output/evidence/infra_check.py). It established:

- `/audit-campaign-lock.json` is a direct regular file, its JSON object exactly
  equals the `audit_campaign` block in `/audit-input.json`, and its independently
  computed SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every launcher-declared mount is present with the required direct file or
  directory type.
- All required pipeline-v3 records are present and readable:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace tree.
- Independent SHA-256 values match all recorded regular-file hashes for the
  canonical program, trusted and candidate prompt, trusted and candidate
  translator, run/task/result/invocation records, all three metrics/usage
  records, and the generation prompt, last message, and output log.
- The 4,166,659-byte generation output was read in full. The trace contains one
  direct regular JSONL file; its SHA-256
  `1c611d4051713db8166b66f3d2d05ded5ee43c0ee824ef7a85502869e1d7889e`
  matches `/generation-result.json`, and all 1,105 lines parse as JSON.
- Fresh extracted-tree identifiers were also calculated for the complete
  candidate and trace namespaces. Bundle-level hashes in the launcher record
  were not confused with extracted-tree serialization hashes.

The supplied-semantics comparison was recursive and type-sensitive. The
candidate tree and `/reference/reference-semantics` have exactly the same 24
regular files and one directory, with no missing, additional, changed,
mistyped, special, or symlinked entry. Both independently reproduce the
pipeline manifest-tree digest
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
The candidate prompt and translator are byte-identical to their trusted mounts.

The required proof artifacts `solution.py`, `solution.mpy`, `verification.k`,
`spec.k`, `prove.sh`, and `PROOF.md` are direct regular files. Their presence is
not taken as proof of correctness.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt says that the object flies exactly when its list is
palindromic and its element sum is no greater than `w`
([prompt.py](/reference/prompt.py:2)). It gives four integer examples covering
unbalanced, overweight, exact-capacity, and singleton behavior.

The canonical function first rejects `sum(q) > w`, then compares symmetric
elements and returns true only if no mismatch is found
([canonical.py](/reference/canonical.py:24)). The candidate is the equivalent
short-circuit expression:

```python
return q == q[::-1] and sum(q) <= w
```

([solution.py](/candidate/solution.py:1)).

Using the trusted `/reference/py2mpy.py`, I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited 0. The regenerated and submitted files are byte-identical,
with SHA-256
`7c0e0763451ba64ad5a942a7e0cf477e9755446d733bd21ae8221636efd7efa0`.
The exact command record is
[02-program-fidelity.log](/audit-output/evidence/02-program-fidelity.log).

### Independent differential test

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted and candidate entry points independently and checks:

- the four documented examples;
- empty lists, singleton and two-element boundaries;
- sum exactly equal to, just above, and just below capacity;
- negative values, very large integers, Boolean and float representatives;
- all lists of length 0 through 5 over `[-3,3]`, crossed with 19 capacities;
- all lists of length 0 through 4 over representative mixed Python numerics,
  crossed with six capacities;
- 10,000 deterministic longer generated cases, with both palindromic and
  arbitrary shapes.

It checked 399,376 cases and found zero result or result-type mismatches, exit
status 0. This is strong implementation-equivalence evidence, not a substitute
for the K proof or a proof over untested Python values.

## 3. Clean proof reconstruction

### Fresh toolchain and builds

The installed independently invoked K toolchain is v7.1.293
([03-toolchain.log](/audit-output/evidence/03-toolchain.log)). Source artifacts
were copied to scratch; all candidate-built definitions and caches were ignored.

The principal fresh commands and outcomes were:

| Purpose | Exact command | Result |
|---|---|---|
| Concrete definition | `kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition reviewer-runtime-kompiled` | exit 0 |
| Bridge-free integer/slice definition | `kompile --backend haskell verification.k --main-module SUMMARY-DEFINITION --syntax-module MPY-SYNTAX --output-definition reviewer-connection-kompiled` | exit 0 |
| Float-rest connection definition | `kompile --backend haskell verification.k --main-module FLOAT-REST-VERIFICATION --syntax-module MPY-SYNTAX --output-definition reviewer-float-connection-kompiled` | exit 0 |
| Target definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition reviewer-verification-kompiled` | exit 0 |

The bounded build logs are
[04-llvm-build.log](/audit-output/evidence/04-llvm-build.log),
[06-connection-build.log](/audit-output/evidence/06-connection-build.log),
[08-float-connection-build.log](/audit-output/evidence/08-float-connection-build.log),
and [10-target-build.log](/audit-output/evidence/10-target-build.log).
Only pre-existing unused-variable warnings from the trusted `str.k` appeared.

The reviewer translated and executed an independent assertion program through
the fresh LLVM definition. Prompt examples, empty and threshold cases,
palindrome boundaries, negatives, a homogeneous float case, and an unbalanced
float short-circuit case all ended in `.K`, `NoExc`, exit code 0. See
[k_concrete_tests.py](/audit-output/evidence/k_concrete_tests.py) and
[05-concrete-execution.log](/audit-output/evidence/05-concrete-execution.log).

### Independent positive proofs

The bridge-free connection proof:

```text
kprove connection-spec.k --definition reviewer-connection-kompiled --spec-module SUM-CONNECTION
```

exited 0 and printed `#Top`. The separate ground connection witnesses did the
same. This definition imports `SUMMARY-DEFINITION`, not the target operational
bridges. Evidence:
[07-connection-proofs.log](/audit-output/evidence/07-connection-proofs.log).

The composed float connection:

```text
kprove float-connection-spec.k --definition reviewer-float-connection-kompiled --spec-module FLOAT-SUM-CONNECTION
```

exited 0 and printed `#Top`; its only proof-local operational bridge is the
already independently connected float-rest fold. Evidence:
[09-float-connection-proof.log](/audit-output/evidence/09-float-connection-proof.log).

The complete target:

```text
kprove spec.k --definition reviewer-verification-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`
([11-target-proof.log](/audit-output/evidence/11-target-proof.log)). I then
invoked each of the four claims separately with `--claims`:

- `SPEC.will-it-fly-balanced`;
- `SPEC.will-it-fly-unbalanced`;
- `SPEC.will-it-fly-float-balanced`;
- `SPEC.will-it-fly-any-unbalanced`.

Every command exited 0 and printed `#Top`
([12-target-claims-individual.log](/audit-output/evidence/12-target-claims-individual.log)).
Thus aggregate success did not conceal an unproved target.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

The claims in [spec.k](/candidate/spec.k:8) have the following meanings:

| Claim | Preconditions | Result constraint | Satisfying witness |
|---|---|---|---|
| `balanced` | Every element is modeled as `Int` or `Bool`, no float is present, and the sequence equals its reverse; `w` is `Int` | Returns exactly `sumInts(0,VS) <=Int W` | `q=[3], w=5`, result `true` |
| `unbalanced` | Same integral domain, but sequence differs from its reverse; `w` is `Int` | Returns exactly `false` | `q=[1,2], w=5`, result `false` |
| `float-balanced` | Every element is numeric, at least one is `Float`, the sequence is not all-integral, it equals its reverse, and `w` is `Float` | Returns exactly `notBool gtF(sumToFloat(0,VS),W)` | `q=[1.5], w=2.0`, result `true` |
| `any-unbalanced` | Any modeled sequence that differs from its reverse; `w` may be any `Val` | Returns exactly `false`, before evaluating `sum` | `q=[1.0,2.0], w=5`, result `false` |

All four preconditions are satisfiable. Substitution gives the stated result in
both Python implementations. The integer and unbalanced witnesses also close as
ground K claims. The Haskell backend cannot concretely evaluate its missing
`Int2Float` hook, so the balanced-float ground check was instead executed
through the fresh LLVM definition and both Python functions. The transparent
record, including the expected Haskell hook limitation, is
[14-ground-witnesses.log](/audit-output/evidence/14-ground-witnesses.log).

Each entry claim binds `"will_it_fly"` to `willItFlyClosure()`, then executes a
real `Call(Name("will_it_fly"), ...)`. It fixes the initial environment,
scopes, heap, stack, return, exception, and exit-code cells. Its destination
also fixes the Boolean result and the material slice allocation. No result is a
free variable, tautology, or one-way implication.

### Constructor-level pinning

The submitted MPY program is a `Module` containing a `FuncDef` with parameters
`q,w` and the translated body shown in
[solution.mpy](/candidate/solution.mpy:1). The proof helper expands
`willItFlyClosure()` to a normal `closureVal` containing that body
([verification.k](/candidate/verification.k:165)); it does not return an oracle
or bypass calls and returns.

The reviewer-authored
[pinning_check.py](/audit-output/evidence/pinning_check.py) parsed
`solution.mpy` with `kast`, read the freshly compiled source rule from
`parsed.txt`, constructed the expected closure KAST from the parsed function
parameters and body, and required exact term equality. It found:

```text
constructor_params_equal=true
constructor_body_equal=true
closure_defining_scope=0
entry_claim_binding_count=4
entry_claim_call_count=4
REAL_PROGRAM_PINNING=PASS
```

The first attempt used an unsuitable `kast --input kast` reparsing route and
failed; the corrected constructor comparison then exited 0. Both attempts are
preserved rather than hidden in
[13-pinning.log](/audit-output/evidence/13-pinning.log).

Omitting the outer module-load/definition step is a demonstrated inert
normalization here: the claim supplies the exact function binding and body that
module loading would create, while still exercising normal lookup, argument
evaluation, frame binding, body execution, return, and pop rules.

A separate body-sensitivity mutation bound the called name to the changed body
`return False` while retaining the true obligation for `[3],5`. It built in dry
run, then exited 1 with `WarnStuckClaimState` and the concrete `false` residual
([reviewer-body-sensitivity.k](/audit-output/evidence/reviewer-body-sensitivity.k),
[21-body-sensitivity.log](/audit-output/evidence/21-body-sensitivity.log)).
The theorem therefore depends on the body actually bound and executed.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I inventoried every K source declaration in all 24 supplied-semantics files and
every candidate top-level K file, including candidate negative tests so that
they could not be mistaken for positive imports. The inventory contains 33
files and 1,057 declarations:

- 208 syntax declarations, including 34 opaque symbols;
- 242 operational rules;
- 472 function/equational rules;
- 40 simplification rules;
- 5 contexts;
- 1 configuration;
- 17 reachability claims;
- 38 module declarations.

The source location, attributes, normalized declaration, and category for every
row are in
[rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv); counts by file
are in
[rule-inventory-summary.md](/audit-output/evidence/rule-inventory-summary.md).
The generating command and hashes are in
[15-rule-inventory.log](/audit-output/evidence/15-rule-inventory.log).

I attached an audit decision and rationale to all 1,057 rows in
[rule-review.tsv](/audit-output/evidence/rule-review.tsv). The outcome counts are
in
[rule-review-summary.md](/audit-output/evidence/rule-review-summary.md), with
the reproducible annotation record in
[16-rule-review.log](/audit-output/evidence/16-rule-review.log). The 811
`ACCEPTED_FIXED_INERT` rows are unchanged supplied-semantics declarations
unreachable from this program and these entry configurations, not an assertion
that they implement all of CPython. The 142 `ACCEPTED_FIXED_USED` rows were
reviewed along the concrete control path.

### Used-construct map and fixed execution

The submitted term uses `Module`, `FuncDef`, `Params`, `Return`, `BoolOp`,
`Compare`, `Name`, `CmpOp`, `Subscript`, `Slice`, `NoBound`, `UnaryOp`, `Int`,
and `Call`. Their syntax is declared in the unchanged
`semantics/syntax.k` ([lines 9–61](/candidate/reference-semantics/semantics/syntax.k:9)).
The material operations map as follows:

| Operation/control | Fixed declarations and rules |
|---|---|
| Module/function value, names, argument evaluation | configuration/load, scope lookup, builtins scope, and left-to-right argument loop in [core.k](/candidate/reference-semantics/semantics/core.k:49); call routing and closure frame creation in [call.k](/candidate/reference-semantics/semantics/call.k:19) |
| Parameter binding and return | [functions.k](/candidate/reference-semantics/semantics/functions.k:63) and [functions.k](/candidate/reference-semantics/semantics/functions.k:77) |
| `and` evaluation | strict head-only short-circuit rules in [bool.k](/candidate/reference-semantics/semantics/bool.k:13) |
| Comparison evaluation | left-to-right contexts and dispatch in [operators.k](/candidate/reference-semantics/semantics/operators.k:14) |
| `q[::-1]` | bound evaluation, negative-step normalization, sequence construction, and fresh allocation in [subscript.k](/candidate/reference-semantics/semantics/subscript.k:43) |
| List equality | structural sequence equality in [list.k](/candidate/reference-semantics/semantics/list.k:17) |
| `sum(q)` | builtin dispatch, list iteration, integer/Boolean conversion, and float transition in [call.k](/candidate/reference-semantics/semantics/call.k:26), [builtins.k](/candidate/reference-semantics/semantics/builtins.k:46), and [float.k](/candidate/reference-semantics/semantics/float.k:257) |
| `<=` | integer comparison in [int.k](/candidate/reference-semantics/semantics/int.k:22) and homogeneous float comparison in [float.k](/candidate/reference-semantics/semantics/float.k:123) |

This path executes the slice and its allocation before list comparison, then
executes `sum` only on the true branch of `and`. State and allocation in the
claims agree with those effects. Priorities 40/39 only ensure that already
justified summary bridges preempt their low-level folds; priority is not used as
a correctness argument.

### Proof-local functions, simplifications, and bridges

The local review reached these conclusions:

- `integralV` and `floatV` are exact, mutually exclusive generated-sort tests.
  `allIntegral`, `allNumeric`, and `hasFloat` have disjoint empty/cons equations,
  structurally descend, and are exhaustive for finite `ValSeq`.
- `projectIntTotal`, `projectBoolTotal`, and `projectFloatTotal` return the
  original value under exact sort guards. Their cast and `#Ceil` simplifications
  agree on overlaps. Arbitrary total interpretations off those guards never
  affect a result-bearing target use.
- `intLikeTotal` implements Python's sum interpretation of `Int` and `Bool`.
  The rule `intOf(V) => intLikeTotal(V)` is guarded by the exact disjunction of
  those two cases. Removing it makes the universal integer connection fail on a
  residual comparison of `intOf(V)` and `intLikeTotal(V)`
  ([18-intof-derivation-sensitivity.log](/audit-output/evidence/18-intof-derivation-sensitivity.log)).
  In the definition without that rule, independent typed claims for arbitrary
  `I:Int` and `B:Bool` both close with `#Top`
  ([intof-typed-connection.k](/audit-output/evidence/intof-typed-connection.k),
  [19-intof-typed-connection.log](/audit-output/evidence/19-intof-typed-connection.log)).
  Thus it is a derived dispatch, not an oracle.
- `sumInts`, `sumFloatRest`, `sumToFloat`, and `reverseSlice` are
  constructor-descending definitions on their guarded domains. `noFloatSum` is
  opaque, but every result-bearing float use requires `hasFloat(VS)`, so a finite
  satisfying sequence necessarily encounters a float before the empty case and
  cannot reach it.
- `willItFlyClosure()` expands to the exact program term established in Stage 4
  and then relies on ordinary fixed call/return semantics.
- The slice bridge at `verification.k:254`, integer-sum bridge at line 260,
  initial-float bridge at line 267, and float-rest bridge at line 279 all
  summarize the exact low-level continuation rather than an arbitrary
  computation. Integer and slice connections are proved in a definition
  containing none of the four bridges; float-rest is proved with only its own
  target bridge excluded; the initial float transition composes only with that
  independently established float-rest lemma. Exact compiled-source isolation
  checks are preserved in
  [17-definition-isolation.log](/audit-output/evidence/17-definition-isolation.log).

Fresh deliberately wrong interpretations provide further sensitivity evidence:
`sumInts = ACC+42`, identity reversal, and a float summary dropping the
accumulated prefix all compiled in an isolated negative definition, but their
connection obligations each produced the expected `WarnStuckClaimState` and
nonzero exit. An initial concrete-float probe encountered the known Haskell
`Int2Float` hook limitation; the corrected symbolic-accumulator probe then
failed on the intended `addF(intToF(ACC),F) != F` obligation. Both the correction
and raw outcomes are in
[20-opposite-interpretations.log](/audit-output/evidence/20-opposite-interpretations.log).

Candidate mutation modules and mutation claims are imported only by separate
negative modules. They are absent from all positive definitions and are
classified `EXCLUDED_NEGATIVE_ONLY` in the exhaustive table.

I found no proof-local rule that can enable a false conclusion on the material
integer domain, no task-answer axiom, no unconstrained result oracle, no
fabricated abrupt return, and no skipped material state effect. Consequently
there is no positive-rule unsoundness claim requiring a false-conclusion
witness.

There is a narrower fixed-model boundary outside that domain. The supplied list
rule compares element constructors with `==K`; CPython numeric equality equates
some cross-sort values. A concrete bridge-divergence witness is `q=[1,True],
w=2`: both Python implementations return true, while the K sequence differs
from its constructor-reversed sequence and enters the false short-circuit
claim. Likewise, the formal float claim is phrased in opaque `intToF`, `addF`,
and `gtF` terms. I treat this as a documented domain/trust limitation, not as an
unsound candidate rule on the intended integer input domain.

## 6. Fresh non-vacuity test

I ignored the candidate's `spec-vacuity.k` as proof and authored a new mutation:
[reviewer-spec-vacuity.k](/audit-output/evidence/reviewer-spec-vacuity.k). It
executes the original pinned body on the satisfying input `q=[3], w=5`, retains
the true integral/palindrome/sum facts, but demands the demonstrably false
result `false`.

First:

```text
kprove reviewer-spec-vacuity.k --definition reviewer-verification-kompiled --spec-module REVIEWER-SPEC-VACUITY --dry-run --output none
```

exited 0, establishing that the mutation parses and builds. The actual proof
command then exited 1 with `WarnStuckClaimState`; the residual contains
`<k> true ~> .K </k>` against the demanded false destination. This is the
expected reachable unmet result obligation, not a parser failure, timeout,
missing import, unrelated crash, or unreachable precondition. Full evidence is
[22-fresh-nonvacuity.log](/audit-output/evidence/22-fresh-nonvacuity.log).

## 7. Proven versus assumed accounting

### What is proved

Under the supplied MPY semantics and the fixed initial/final cells in the entry
claims, the reconstructed reachability proof establishes:

1. For every finite `ValSeq` whose elements satisfy the model's integral
   classifier and every `W:Int`, the exact generated function returns
   `sumInts(0,VS) <=Int W` when `VS` equals its reversal, and returns false when
   it does not.
2. Therefore, on the unrestricted material integer-list/integer-capacity
   domain—including empty lists, negative and unbounded mathematical integers,
   arbitrary length, and every sum/weight boundary—the result is true exactly
   when the list is palindromic and its sum is at most the capacity.
3. For the supplied model's float-containing numeric sequences that are
   constructor-palindromic with a float capacity, the exact generated function
   returns the structurally exact opaque float comparison term.
4. For every modeled constructor-unbalanced sequence, evaluation returns false
   through the real `and` short-circuit without requiring the `sum` branch.
5. The reversal allocation, ordinary environment lookup, parameter binding,
   call frame, return, and final state constraints are part of the reachability
   claims; the result is not inferred from differential tests.

This is a proof of the generated rewrite, not a direct proof of the canonical
loop implementation. Trusted regeneration plus exact constructor pinning
connects the theorem to the submitted `solution.mpy`; the large differential
test supports, but does not formally prove, equivalence to the canonical Python
implementation.

### Assumptions and trust boundaries

| Boundary | Status and reason |
|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, matching/unification, and builtin mathematical theories | Necessary toolchain trust. Both independent reconstruction and negative sensitivity were observed; no candidate-produced executable was trusted. |
| The 24-file supplied semantics | Trusted input for this rendered condition and byte-identical in candidate/reference trees. Every declaration was inventoried, and every used rule path was statically reviewed and concretely exercised. |
| Trusted `py2mpy.py` | Acceptable translation bridge: candidate copy is byte-identical, regeneration is byte-identical, and the parsed function term is mechanically matched to the closure. Translator correctness itself remains trusted. |
| Integer/Boolean K primitives, finite sequence constructors, maps, lists, and ordinary arithmetic | Acceptable low-level semantic/mathematical boundary for the material domain; no task answer is embedded in them. |
| `reverseSlice`, `sumInts`, `sumFloatRest`, `sumToFloat` | Proven summaries, not assumptions: their operational connections close in isolated definitions, and wrong interpretations are rejected. |
| Guarded `intOf`/`intLikeTotal` dispatch | Derived from the two supplied typed rules; independently checked for arbitrary typed Int and Bool branches. |
| Opaque float primitives `intToF`, `addF`, `gtF` and unavailable Haskell `Int2Float` hook | Concerning but non-fatal. The float theorem proves structural correspondence, while concrete LLVM tests check only selected values. No claim of a complete symbolic IEEE-754 proof is warranted. |
| Material source-domain interpretation | Concerning informal bridge. The trusted prompt is untyped but all examples use integer lists and integer capacity. That integer domain is covered universally; cross-sort numerics and exotic Python values are not claimed as materially specified. |
| Differential tests | Empirical support only for canonical/generated Python equivalence and selected model behavior. They are not counted as K proof steps. |
| Candidate `PROOF.md`, traces, prior `#Top`, logs, and compiled definitions | No trust assigned; used only to locate claims and then independently reconstructed or checked. |

### Verdict rationale

This is not `FAIL`: all required proof artifacts exist; fresh builds and every
positive target close; the postconditions constrain the actual Boolean result;
the exact regenerated body is what the claims bind and call; satisfying inputs
exist; the fresh false mutation is rejected; the proof is unbounded in list
length and integer value; and no unsound proof-local rule or task-answer oracle
survived static review.

It is `LEGIT` because those facts establish the requested partial-correctness
property for the real generated program over the material source-contract
domain. The verdict remains `CONCERNS`, rather than `PASS`, because the
Python-to-K type boundary and opaque float extension leave explicitly
documented, non-material coverage and trust limitations.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
