# Independent adversarial review: 135-can-arrange

The candidate contains a sound, result-constraining partial-correctness proof
of the submitted translated program under the supplied MPY semantics. The
proof is unbounded over finite modeled lists, executes the exact translated
body, and its only execution bridge is universally connected to the fixed
comparison rules over its complete guard.

The proof is not a clean `PASS` because the supplied read-only model has
material, reproducibly documented boundaries: it has no `>=` behavior for
represented set/list/tuple values, and its concrete `>=` encoding for NaN does
not agree with CPython. The candidate did not introduce either limitation, its
precondition covers every adjacent comparison class that the fixed model
defines, and its Python implementation follows the docstring's literal
`not >=` predicate on the gap. Under campaign amendment v2 exception 1 and the
docstring-first v3 ground truth, these are `CONCERNS / LEGIT`, not candidate
invalidity.

## 1. Input and provenance integrity

The launcher declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and the expected problem and condition.
The trusted `/reference/reference-semantics` mount is present, so the rendered
mode and mounts are consistent.

I read all required pipeline-v3 records: `/audit-input.json`,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, all six required generation metadata/text records,
and the structured trace. I treated their content as claims only.

Independent checks in
[stage1_integrity.sh](/audit-output/evidence/stage1_integrity.sh) and
[stage1_integrity.log](/audit-output/evidence/stage1_integrity.log) established:

- The campaign block is structurally equal to
  `/audit-campaign-lock.json`, whose SHA-256 is the declared
  `053ed73c...dadd01`.
- The run, task, generation result, invocation, metrics, runtime metrics,
  usage, prompt, output, last-message, trusted prompt, translator, and
  canonical files all hash to their launcher-declared values.
- The single structured trace file hashes to
  `133f22b4...9d6ae`, exactly as recorded by both the invocation and generation
  result. All 553 lines parse as JSON: 159 `event_msg`, 391 `response_item`,
  and one each of `session_meta`, `turn_context`, and `world_state`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- A recursive, non-dereferencing comparison of candidate and trusted
  `reference-semantics/` trees exits 0. The tree has 24 regular source files,
  no missing/additional/different entry, and no symlink. Per-file trusted
  hashes are in the Stage 1 log.
- No symlink exists anywhere under the candidate, generation evidence, or
  trusted semantics tree.
- Every required candidate proof artifact is a readable regular file. Its
  independent hashes are recorded in
  [stage1_candidate_sources.log](/audit-output/evidence/stage1_candidate_sources.log).

The generation report's prior `#Top`, prose, compiled directories, and logs
were not reused as proof evidence. All executable source needed below was
copied to `/tmp/audit-work/135-can-arrange`; candidate-built `*-kompiled`
directories and caches were neither copied nor referenced.

Stage 1 result: integrity gate passes; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted docstring requires the largest index `i` whose element is *not
greater than or equal to* its immediate predecessor, or `-1` if no such index
exists. It says the given array has no duplicate values and gives:

- `[1, 2, 4, 3, 5] -> 3`
- `[1, 2, 3] -> -1`

The submitted `solution.py` scans left-to-right, updates the accumulator at
each literal `not value >= previous`, and therefore retains the largest such
index. Starting at index 0 and skipping the first comparison is equivalent to
starting at index 1. The implementation does not rely on duplicates, so it is
stronger than the stated premise in that dimension.

The trusted canonical scans with `<`. That is an equivalent helper witness on
ordinary total orders, but v3 makes the docstring—not canonical
implementation equality—the contract.

### Translation identity

In scratch, the command

```text
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0. `cmp` against submitted `solution.mpy` exited 0, and both files have
SHA-256 `9f1d4564...1329d`. Exact commands and statuses are in
[stage2_fidelity.log](/audit-output/evidence/stage2_fidelity.log).

### Independent differential

The reviewer-authored
[independent_differential.py](/audit-output/evidence/independent_differential.py)
loads the trusted canonical and generated entry points independently. It
exercises the examples, empty and singleton boundaries, the first and last
comparison branches, multiple descents, mixed Bool/Int/Float values, strings,
infinities, NaNs, nested containers, sets, exception cases, every distinct
permutation of seven small integers through length six, and deterministic
generated string and mixed-numeric cases.

The run covered 11,679 cases:

```text
candidate_contract_mismatches 0
candidate_vs_canonical_differences 3
```

The three helper differences were:

- `[1.0, NaN, 2.0]`: canonical `-1`, candidate `2`;
- `[NaN, 1.0]`: canonical `-1`, candidate `1`;
- two incomparable sets: canonical `-1`, candidate `1`.

All three candidate results follow the literal `not >=` contract. NaN,
non-finite behavior, and exotic element classes are also expressly
underdetermined edge classes under campaign v3. These differences are
documented observations, not docstring violations. Both documented examples
pass.

The candidate's own differential is weaker evidence because its oracle repeats
the same `not >=` predicate. This independent three-way differential corrects
that evidence limitation; neither finite test substitutes for the K proof.

Stage 2 result: program and translation fidelity pass.

## 3. Clean proof reconstruction

K v7.1.293 and Python 3.10.12 were available. The full clean command driver and
combined bounded output are
[stage3_reconstruct.sh](/audit-output/evidence/stage3_reconstruct.sh) and
[stage3_reconstruction.log](/audit-output/evidence/stage3_reconstruction.log).

### Concrete definition

I compiled the trusted semantics source, not the candidate's compiled output:

```text
kompile reference-semantics/semantics.k
  --backend llvm
  --main-module MPY-KRUN
  --syntax-module MPY-SYNTAX
  --output-definition runtime-audit-kompiled
```

It exited 0. A reviewer-authored translated smoke module covering both examples,
empty/singleton inputs, repeated descents, and strings ran with `krun`, exited
0, and ended in `.K`, `NoExc`, exit code 0. The compiler reported fixed-model
exhaustiveness warnings for unused operations such as `floorFI`, `toF`,
`mapStrVS`, and `valSeqAt`; none is used by this submitted program.

### Bridge-free comparison definition

I freshly compiled `verification.k` with main module `VERIFICATION-BASE`, which
excludes the candidate bridge. Each of the ten positive connection claims was
then selected and run independently:

```text
CONNECTION-SPEC.ge-int-int
CONNECTION-SPEC.ge-bool-bool
CONNECTION-SPEC.ge-bool-int
CONNECTION-SPEC.ge-int-bool
CONNECTION-SPEC.ge-float-float
CONNECTION-SPEC.ge-int-float
CONNECTION-SPEC.ge-float-int
CONNECTION-SPEC.ge-bool-float
CONNECTION-SPEC.ge-float-bool
CONNECTION-SPEC.ge-str-str
```

Every command exited 0 and printed `#Top`. Individual logs are named
`stage3_connection_<claim>.log` under
[evidence](/audit-output/evidence). The `WarnTrivialClaim` diagnostics mean
the fixed dispatch and `orderGe` simplified to the same term without a
reachability step; they do not indicate that the bridge was imported.

### Target definition and claims

I freshly compiled `verification.k` with main module `VERIFICATION`. The loop
claim alone exited 0 with `#Top`. The unfiltered target run, which includes
both the loop circularity and whole-program claim, also exited 0 with `#Top`.
See [stage3_target_loop.log](/audit-output/evidence/stage3_target_loop.log) and
[stage3_target_all.log](/audit-output/evidence/stage3_target_all.log).

Stage 3 result: every positive auxiliary and target proof reconstructs cleanly.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.can-arrange-loop` begins at the exact `#loop(list(VS), ...)` term reached
inside the submitted function. For a nonnegative absolute index `I`, previous
value `P`, and current result accumulator `A`, its precondition requires every
comparison in the remaining suffix to be defined by the fixed model. It
consumes that suffix and changes `index` to
`arrangeSeq(VS, I, P, A)`. The final internal `i`, `previous`, and `value`
bindings are existential because the exact following continuation only returns
`index` and then pops the call frame.

`SPEC.can-arrange` starts in the exact initial MPY configuration, loads the
translated module, resolves the resulting closure through the normal scope
chain, calls it with `list(VS)`, executes the body and loop, and returns
`arrangeSeq(VS, 0, 0, -1)`.

`scanDefined(VS, 0, 0)` permits an unrestricted first/singleton value, then
requires every adjacent pair actually compared to be numeric×numeric
(Int/Bool/Float combinations) or string×string. This exactly matches all `>=`
dispatch cases present in the fixed supplied semantics. It is unbounded in
list length and does not impose the docstring's duplicate restriction.

`arrangeSeq` consumes indices in increasing order and overwrites the
accumulator exactly when `orderGe` is false. Consequently, the final
accumulator is the largest qualifying index or the initial `-1`.

### Mechanical identity and witnesses

The reviewer-authored balanced-constructor/token check found 181 constructor
tokens in both regenerated `solution.mpy` and the `Module` argument to the
whole claim's `#loadAll`; they are identical after removing only explicit
empty `.Stmts` identities. Evidence:
[stage4_program_identity.py](/audit-output/evidence/stage4_program_identity.py)
and [stage4_adequacy.log](/audit-output/evidence/stage4_adequacy.log).

Thus the claim pins the same function name, parameter, statement order, loop
target/body, comparisons, assignments, and return. No typing import or material
program construct is omitted.

The empty list is a concrete satisfying entry-precondition state. Empty,
documented, and multiple-descent substitutions agree among `arrangeSeq`,
generated Python, and canonical Python. Ground K substitutions for the empty
and first documented input jointly proved `#Top`.

A separate body-sensitivity test changed the program term actually executed by
`#loadAll` to `return 0`, while retaining the original empty-input result
obligation. It built, then failed with `WarnStuckClaimState` and residual
`<k> 0 ~> .K </k>` instead of `-1`. See
[stage4-body-sensitivity.k](/audit-output/evidence/stage4-body-sensitivity.k)
and
[stage4_body_sensitivity.log](/audit-output/evidence/stage4_body_sensitivity.log).

The top-level formal container is a finite list. This is the material reading
supported by both examples and normal HumanEval “array” usage. Alternative
top-level tuples, strings, and arbitrary iterators are unspecified input
classes, so their exclusion is not a material contract narrowing.

Stage 4 result: claims are satisfiable, result-constraining, and pin the real
submitted program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule_inventory.txt](/audit-output/evidence/rule_inventory.txt), generated by
[rule_inventory.py](/audit-output/evidence/rule_inventory.py), enumerates every
source-level syntax declaration, configuration, context, rule, claim, and
relevant attribute from all 24 supplied K files plus `verification.k`,
`spec.k`, and `connection-spec.k`.

The inventory has 1,054 records:

- 249 syntax declarations;
- 787 rules;
- five contexts;
- one configuration;
- 12 claims.

Of these, 1,014 are entries in the integrity-verified supplied baseline, 28
are candidate-local declarations/rules, and 12 are proof obligations. Every
entry includes file, line, complete collapsed rule/declaration, attributes
(`function`, `total`, `no-evaluators`, `symbol`, `concrete`,
`simplification`, priority, `owise`, strictness, and macros where present),
and its review class. This is the exhaustive rule-level record; the grouped
analysis below applies one justification to entries with the same structure.

Because this is `SUPPLIED_SEMANTICS`, the unchanged 1,014 baseline entries are
the selected fixed foundation, not candidate proof extensions. I nevertheless
traced every construct used by `solution.mpy` through the relevant baseline
path:

| Used construct | Fixed declarations/rules and review |
|---|---|
| `Module`, `FuncDef`, `Params`, statement sequencing | `syntax.k`; `core.k` module/statement rules; `functions.k` closure binding. Exact order and binding are preserved. |
| `Call(Name("can_arrange"), list(VS))` | `core.k` lookup/evaluation; `call.k` callee/argument routing and frame creation; `functions.k` parameter binding and pop. The claim pins scopes, environment, stack, return, heap, and counters. |
| `Assign` and `Name` | `controls.k` ordinary scope update; `core.k` lexical lookup. No cell/heap priority leg can apply to this plain frame. |
| `For` over the input | `controls.k` evaluates the iterable once and uses `#loop/#loopStep`; `list.k` consumes one `vCons`; `tuple.k` binds the loop target. Each induction step removes one sequence constructor. |
| nested `If` | strict condition evaluation followed by `#branch`; integer truth of `i > 0` is exact. |
| unary `-` and binary `+` | `operators.k` dispatch plus exact `int.k` operations. |
| unary `not` | `operators.k` then `bool.k` `notBool truthy(V)`. The comparison result is Bool. |
| `>` and `>=` comparisons | `operators.k` evaluates left then right before pure `applyCmp`; Int/Bool/Float/String cases live in `int.k`, `bool.k`, `float.k`, and `str.k`. |
| `Return` | strict result evaluation, `retV`, exact saved frame pop, scope restoration, and continuation resumption in `functions.k`. |

No used construct is fabricated, skipped, or sent to an unconstrained fresh
result. Candidate-local rules do not access heap, scopes, stack, environment,
return, exception, or exit cells.

### Candidate-local declarations and rules

There are five local syntax declarations and 23 local rules:

1. `isNumericVal` and `orderablePair` each have one total equation. They are
   pure definitional classifiers using K sort predicates. There is no overlap
   or uncovered case.
2. `scanDefined` has four simplification equations. Empty/nonempty sequence and
   `I < 0`, `I == 0`, `I > 0` partition its full domain; recursive cases consume
   one `vCons`. Its value only restricts theorem applicability.
3. `orderGe` has ten static, sort-disjoint orderable cases and one guarded
   fallback. Each static case is exactly the corresponding fixed `>=` result;
   all ten bridge-free universal connection claims independently close. The
   fallback is an explicit totalization when `orderablePair` is false. It is
   never used by the operational bridge and target preconditions prevent it
   from influencing a program result.
4. `arrangeSeq` has five equations. Empty/nonempty and the integer-index
   trichotomy partition the domain; the two positive-index branches partition
   on the total Boolean `orderGe`; every recursive rule consumes one
   constructor. Its updates exactly implement “latest/largest qualifying
   index.”
5. The sole operational bridge is:

   ```text
   applyCmp(">=", V, W) => orderGe(V, W)
   requires orderablePair(V, W)
   ```

   It matches only the pure post-evaluation dispatch term, not `Compare`,
   operand/name evaluation, a continuation, or any state cell. Its state and
   control footprint is empty. Its complete guard is the disjoint union of
   the ten static connection claims proved in the bridge-free definition.
   The bridge and fixed rules may overlap, but their right-hand values are
   equal on every overlap.

The operational-context procedure was also tested independently. A fixed-only
claim and a bridge-enabled claim placed the comparison before an observable
assignment continuation; both selected `x = 7` and printed `#Top`.
[stage5_fixed_context.log](/audit-output/evidence/stage5_fixed_context.log) and
[stage5_extended_context.log](/audit-output/evidence/stage5_extended_context.log)
record those runs. The opposite fixed interpretation `2 >= 1 => false` was
rejected with residual `true`; see
[stage5_opposite_comparison.log](/audit-output/evidence/stage5_opposite_comparison.log).

The proof uses no candidate-local priority rule, concrete rule, fresh symbol,
external oracle, or unconnected program-body summary. I found no candidate
rule for which a false conclusion witness exists on the theorem domain.

### Supplied-model gaps, with concrete witnesses

These are fixed-model limitations, not candidate rule unsoundness:

- **NaN comparison encoding.** The supplied rule defines Float `>=` as
  `notBool floatLt`. Concrete IEEE comparison makes `floatLt` false when NaN
  participates, so the model makes `>=` true. The reviewer K program
  [reviewer_nan_model.mpy](/audit-output/evidence/reviewer_nan_model.mpy)
  executes the exact algorithm on `[NaN, 1.0]` and confirms model result `-1`
  (`.K`, `NoExc`). CPython has both `NaN >= 1.0` and `1.0 >= NaN` false, so
  submitted Python returns `1`, faithfully applying `not >=`. The paired
  outputs are
  [stage5_nan_model.log](/audit-output/evidence/stage5_nan_model.log) and
  [stage5_nan_python.log](/audit-output/evidence/stage5_nan_python.log).
- **Represented containers without `>=`.** The supplied model represents sets,
  lists, and tuples as values but only defines their limited equality/membership
  operations. Translating and running the exact algorithm on two distinct sets
  gets stuck at `applyCmp(">=", setV(...), setV(...))`, exit 113; see
  [stage5_set_model_gap.log](/audit-output/evidence/stage5_set_model_gap.log).
  CPython and the docstring-literal oracle return index `1` for incomparable
  sets, as independently shown in Stage 2.

The target precondition adds no comparison-domain narrowing beyond operations
the supplied model actually defines. The NaN behavior cannot be repaired by a
candidate proof rule without changing the fixed read-only model. The Python
program itself is faithful on both gaps. These findings satisfy all four
campaign-amendment conditions for a documented supplied-model representation
gap and therefore map to `CONCERNS / LEGIT`.

Stage 5 result: Gate A static soundness passes; fixed-model limitations remain
as non-fatal concerns.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`.
[stage6-false-result.k](/audit-output/evidence/stage6-false-result.k) is a
fresh claim containing the exact real `#loadAll` program and satisfiable empty
input, with only the result obligation changed from `-1` to `0`.

`kprove --dry-run` exited 0, proving that the mutation parsed and built against
the fresh definition. The actual proof exited 1 with
`WarnStuckClaimState` and the expected residual:

```text
<k> -1 ~> .K </k>
```

This is the relevant unmet result obligation, not a parser error, timeout, or
unrelated crash. Commands and outputs are in
[stage6_nonvacuity.log](/audit-output/evidence/stage6_nonvacuity.log).

Stage 6 result: non-vacuity passes.

## 7. Proven versus assumed accounting

### Precisely proven

Under the unchanged supplied MPY theory and for every finite `ValSeq`
satisfying `scanDefined(VS, 0, 0)`, execution of the exact regenerated
`can_arrange` module is partially correct with returned value
`arrangeSeq(VS, 0, 0, -1)`. The recursive equations make that value the
largest index whose fixed-model `>=` result is false, or `-1`. The theorem is
symbolic and unbounded in list length. It covers empty/singleton lists, every
modeled adjacent numeric combination, and modeled strings; it does not assume
distinct elements.

### Trust ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| Supplied MPY operational semantics | Defines syntax, evaluation, scope/call/loop state, comparison, and return for all claims. | Authorized fixed foundation; integrity is byte-for-byte verified. Concrete smoke supports used ordinary cases. |
| K v7.1.293 Haskell/LLVM backends, K builtins, SMT reasoning | Establish compilation, symbolic closure, and arithmetic/sort reasoning. | Standard proof-engine trust boundary; exact fresh commands and outputs are preserved. |
| `floatLt`, `ltIF`, `ltFI` | Opaque, total supplied symbols whose Boolean values affect comparison branches and final index. | Target proof is parametric in the supplied symbols and bridge-free connections use the same symbols. Concrete ordinary-float evidence exists, but NaN divergence is explicitly witnessed above. Concerning but permitted fixed-model gap. |
| `strLt` and IntSeq string representation | Determines string comparison branches. | Recursive supplied definition and universal string connection claim; finite ASCII/non-ASCII differential support only. No contrary witness found. |
| Ten-case guard partition | Establishes that every bridge match is covered by a bridge-free theorem. | Machine claims are universal within each static sort pair; exhaustive `orderablePair` partition is an ordinary finite sort argument. |
| `arrangeSeq` to natural-language “largest index” meaning | Converts the formal returned summary to user intent. | Direct structural induction on its five complete, descending equations; documented examples and independent reverse-style tests support, but do not replace, this mathematical reading. |
| Python-to-MPY source bridge | Connects the theorem term to submitted Python. | Trusted translator regenerates byte-identical MPY; independent constructor identity checks the exact term loaded by the claim; body mutation is rejected. |
| Differential and concrete tests | Support implementation intent and model boundaries. | Finite evidence only: 11,679 Python cases plus targeted K runs. They are not used as universal proof. |

### Gate summary and decision

- **Gate A — PASS.** Fresh `#Top`; exact body; satisfiable claim; complete local
  equations; bridge-free universal value connection; preserved state/control;
  body sensitivity; opposite-value rejection; fresh non-vacuity.
- **Gate B — PASS with documented fixed-model concerns.** The theorem is
  unbounded over the material list domain represented by the supplied model
  and the Python program satisfies every docstring-determined behavior tested.
  Unmodeled container orderings and divergent NaN behavior are supplied-model
  gaps with concrete witnesses and a faithful submitted program, so campaign
  amendment v2 exception 1 applies. Canonical edge differences do not show a
  docstring violation under v3.
- **Gate C — PASS.** Reviewer-authored scripts, mutations, exact commands,
  exit statuses, bounded outputs, and the exhaustive rule inventory are
  preserved under `/audit-output/evidence`. Formal results, conditional model
  conclusions, empirical support, and excluded behavior are separated.

The proof is legitimate. The fixed-model NaN/container boundaries and the
candidate's originally non-independent differential prevent an unqualified
`PASS`, but neither permits a false theorem about the modeled program nor
constitutes candidate-created domain narrowing.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
