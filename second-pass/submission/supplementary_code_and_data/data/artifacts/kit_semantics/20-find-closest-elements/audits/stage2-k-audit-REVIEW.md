# Independent adversarial review: 20-find-closest-elements

The candidate contains a genuine, freshly reconstructable K reachability proof
of the submitted program on its formal `Float` domain. The proof is
result-constraining, constructor-pins the translated program, and its only
operational bridge has a bridge-free universal connection proof. It is not a
fully self-contained formal proof of the natural-language phrase “closest
elements”: the final K result is an exact recursive scan summary whose
global-minimum meaning, and whose connection to Python's special-float behavior,
remain an informal/empirical adequacy bridge. That is a non-fatal limitation,
not an unsound rule or a substituted-program proof.

I treated every candidate report, cache, trace, and prior `#Top` as untrusted.
All dynamic work used trusted source copies under
`/tmp/audit-work/20-find-closest-elements`; no candidate-built definition was
copied or invoked. Reviewer scripts, patches, and bounded logs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

The launcher record declares `record_layout: pipeline-v3` and
`semantics_mode: SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the mount layout agrees
with the rendered semantics mode.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required pipeline-v3 generation
record, the generation prompt, the 5.2 MB textual log, and the structured
trace. The trace has one file and 1,029 valid JSONL records. The generation
records claim a successful run, three positive `#Top` results, and a
`SOUND-BUT-LIMITED` report; none of those claims was used as proof evidence.

Independent integrity results:

- The campaign-lock JSON equals the `audit_campaign` block in
  `/audit-input.json`, and its SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every required pipeline-v3 record is a regular, non-symlinked file, and every
  launcher-recorded file hash matches. Every output hash in
  `/generation-result.json`, including the structured trace, also matches.
- Every launcher-declared `container_paths` target exists and is not a
  symlink.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- The candidate and trusted supplied-semantics trees have exactly the same 25
  entries, entry types, relative paths, and file hashes. Neither tree contains
  a symlink. There is no missing, additional, mistyped, or changed semantics
  entry.
- An independent manifest of the entire candidate mount covers 811 entries
  and finds zero symlinks and zero special entries. Its reviewer-algorithm hash
  is
  `eaeed4da09768ad7d9b7be6522d0b1d16843259d8890ad7e12320be0f22de7a3`.

The complete checks, exact hashes, trace event counts, commands, and exit
statuses are in
[01_provenance_integrity.log](/audit-output/evidence/01_provenance_integrity.log)
and
[02_provenance_structured_check.log](/audit-output/evidence/02_provenance_structured_check.log).
There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt requires `find_closest_elements(numbers: List[float])` for a
list of length at least two. It must return two elements at minimum pairwise
distance, ordered as the smaller value followed by the larger value. Duplicate
positions may produce an equal pair. The two documented results are `(2.0,
2.2)` and `(2.0, 2.0)`.

The trusted canonical implementation enumerates all ordered pairs of distinct
positions, initializes from the first such pair, and replaces the accumulator
only for a strictly smaller distance.

### Submitted implementation

`solution.py` initializes from positions 0 and 1, materializes
`list(enumerate(numbers))`, and scans every pair with indices `i < j`. A
strictly closer pair replaces the accumulator, with its two values put in
ascending order. For ordinary finite values, this is extensionally equivalent
to the canonical scan; avoiding the symmetric `j < i` cases does not change
the minimum.

Using the trusted translator, I regenerated `solution.mpy` and required byte
identity with the submission. Both files have SHA-256
`35dc7dd07d8b54b2e62111cfec11461f4d94f6e30c86864fab6201a5b3c97d24`;
the command exited 0. See
[03_translator_regeneration.log](/audit-output/evidence/03_translator_regeneration.log).

### Independent differential testing

The reviewer-authored
[differential_audit.py](/audit-output/evidence/differential_audit.py) imports
the trusted canonical module and submitted generated module by separate file
paths. It covers:

- both prompt examples;
- empty and singleton diagnostic calls;
- ascending, descending, equal, negative, duplicate, strict-tie, update, and
  no-update branch boundaries;
- all-`int` and mixed `int`/`float` numeric inputs;
- signed zero, NaN, and infinities;
- 2,000 seeded finite-float lists of lengths 2 through 9; and
- 500 seeded numeric-tower lists of lengths 2 through 9.

The ordinary finite-float sample had zero canonical mismatches and zero
contract-property failures. The 500 mixed numeric cases also had zero
mismatches and zero property failures. Full scope and results are in
[04_differential_audit.log](/audit-output/evidence/04_differential_audit.log).

Four fixed diagnostic cases differed exactly:

1. On empty and singleton lists, outside the stated length precondition, the
   canonical returns `None` while the submitted implementation raises
   `IndexError`.
2. On `[-0.0, 0.0]`, the canonical preserves `(-0.0, 0.0)` while the
   submission returns `(0.0, -0.0)`. The values are numerically equal and
   either position has minimum distance zero, but their IEEE sign-bit order
   differs.
3. With NaN in the first position, the two programs place NaN in different
   tuple positions. The prompt supplies no meaningful smaller/larger or
   distance contract for NaN.

The last two are special-float fidelity limitations worth recording, but they
do not falsify the ordinary finite-number contract exercised by the prompt.
The formal K claim ranges over K `Float` terms but states its result
parametrically through the supplied float primitives; it does not assert a
Python/K NaN ordering theorem.

The K theorem excludes runtime `Int` values even though both Python programs
and the supplied semantics execute all-`Int` and mixed numeric examples. The
trusted signature is specifically `List[float]`, so I do not treat that
boundary as a material narrowing of the declared HumanEval domain. If “list of
numbers” were instead interpreted as an untyped numeric-tower contract, this
would become a material scope failure; the exclusion is made explicit here
rather than hidden.

## 3. Clean proof reconstruction

The installed tools are K `v7.1.293` and Python `3.10.12`; see
[05_tool_versions.log](/audit-output/evidence/05_tool_versions.log).
Fresh trusted sources were copied into scratch without any `*-kompiled`
directory or cache from `/candidate`.

The following independent positive reconstruction succeeded:

| Purpose | Fresh command result | Evidence |
|---|---|---|
| Fixed Haskell semantics | `kompile ... --main-module MPY ... --output-definition fixed-fresh-kompiled`, exit 0 | [06_build_fixed_haskell.log](/audit-output/evidence/06_build_fixed_haskell.log) |
| Fixed projection lemmas | `kprove projection-spec.k ...`, exit 0, `#Top` | [07_prove_projection.log](/audit-output/evidence/07_prove_projection.log) |
| Bridge-free definition | `kompile verification.k --main-module VERIFICATION-BASE ...`, exit 0 | [08_build_connection_haskell.log](/audit-output/evidence/08_build_connection_haskell.log) |
| Inner-loop connection | `kprove connection-spec.k ...`, exit 0, `#Top` | [09_prove_connection.log](/audit-output/evidence/09_prove_connection.log) |
| Target definition | `kompile verification.k --main-module VERIFICATION ...`, exit 0 | [10_build_verification_haskell.log](/audit-output/evidence/10_build_verification_haskell.log) |
| All three target claims | `kprove spec.k ... --spec-module SPEC`, exit 0, `#Top` | [11_prove_all_target_claims.log](/audit-output/evidence/11_prove_all_target_claims.log) |
| Inner-loop selected claim | exit 0, `#Top` | [12_prove_target_inner_loop.log](/audit-output/evidence/12_prove_target_inner_loop.log) |
| Outer-loop selected claim | exit 0, `#Top` | [13_prove_target_outer_loop.log](/audit-output/evidence/13_prove_target_outer_loop.log) |

The ordinary `kprove spec.k` command proves every claim in `SPEC`, including
the entry claim, in one run. As a diagnostic, I also selected only
`SPEC.find-closest`; that removes the outer-loop circularity on which the entry
proof is intentionally based, so symbolic unrolling did not converge and I
interrupted it after about 136 seconds. This is not a failed required positive
target: the complete spec, with its declared auxiliary claim, closed in nine
seconds. The diagnostic is recorded transparently in
[14_prove_target_find_closest.log](/audit-output/evidence/14_prove_target_find_closest.log).

I also freshly built the LLVM concrete definition and ran a regenerated smoke
module containing the submitted body and four assertions. Compilation and
execution exited 0; final `<k>` is `.K`, `<stack>` is empty, `<exc>` is
`NoExc`, and `<exit-code>` is 0. See
[15_build_concrete_llvm.log](/audit-output/evidence/15_build_concrete_llvm.log)
and
[16_concrete_smoke.log](/audit-output/evidence/16_concrete_smoke.log).

Thus every positive proof artifact required by the candidate exists, every
positive target command closes afresh, and no prior compiled definition is
needed.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.inner-loop` starts at the real fixed-semantics `#loop` for the submitted
inner `for item2 in items` body. Its precondition says `item1` is exactly a
two-component `(Int index, Float value)` tuple and every remaining inner item
has the same shape. It preserves the arbitrary continuation and all framed
cells, sets `item2` to the last iterated item (or preserves its old value for
an empty remainder), and sets `closest` to the recursive `innerFirst` /
`innerSecond` scan result.

`SPEC.outer-loop` starts at the real `#loop` for `for item1 in items`. Its
precondition says both the remaining outer sequence and the complete item list
contain canonical `(Int, Float)` tuples, with the complete list stored in the
heap. It preserves the arbitrary continuation and heap, permits the final
loop-variable bindings to be existential, and constrains `closest` to the
recursive `outerFirst` / `outerSecond` scan.

`SPEC.find-closest` starts from:

```text
#loadAll(solutionModule)
~> Call(Name("find_closest_elements"),
        list(vCons(F0, vCons(F1, REST))))
```

where `F0` and `F1` have K sort `Float` and `allFloatVS(REST)` holds. Therefore
the formal domain is every finite K-Float list of unbounded length at least
two. The postcondition is an exact two-element tuple:

```text
(outerFirst(enumVS(VS,0), enumVS(VS,0), orderedFirst(F0,F1), orderedSecond(F0,F1)),
 outerSecond(enumVS(VS,0), enumVS(VS,0), orderedFirst(F0,F1), orderedSecond(F0,F1)))
```

It also constrains the loaded closure body, module binding, two allocated
enumeration/list objects, heap counter, restored scope, empty stack, return
cell, exception cell, and exit code. The returned values are not free variables
and the claim is not a one-way implication or shape-only postcondition.

### Mechanical program identity

The translator identity from stage 2 connects `solution.py` to
`solution.mpy`. I then parsed both regenerated `solution.mpy` and the
`solutionModule` term with the freshly built definition and expanded all
macros in module `VERIFICATION`. The resulting constructor JSON files are
byte-identical with SHA-256
`edb7be528389908324833ec7e13a7135f08e351ca78c3113d27d4318cb12ebd1`.
This is the required constructor-level comparison; see
[18_constructor_pinning_corrected.log](/audit-output/evidence/18_constructor_pinning_corrected.log).
The earlier
[17_constructor_pinning.log](/audit-output/evidence/17_constructor_pinning.log)
is a retained diagnostic that used the syntax-only module and therefore did
not expand proof-module macros; it is superseded by the corrected comparison.

### Satisfiable states and ground substitution

Concrete satisfying examples exist for every claim:

- Entry: `REST = .ValSeq`, `F0 = 1.0`, `F1 = 2.0`.
- Inner loop: `REST = .ValSeq`, `ITEM1 = tuple(0, 1.0)`, and any Float
  accumulator pair.
- Outer loop: `REST = .ValSeq`, `ALL = .ValSeq`, with the stated heap binding.

For the nontrivial entry witness `[1.0, 9.0, 3.0, 4.0]`, direct substitution
into the formal fold yields `(3.0, 4.0)`, and both Python implementations
return `(3.0, 4.0)`. Three more ground substitutions agree as well; see the
reviewer-authored
[claimed_summary_witness.py](/audit-output/evidence/claimed_summary_witness.py)
and
[27_claimed_summary_witness.log](/audit-output/evidence/27_claimed_summary_witness.log).
The same Float witness executes under fresh LLVM semantics. The separate K
witness also demonstrates that all-`Int` and mixed inputs execute even though
the theorem excludes them; see
[satisfying_and_excluded_witness.py](/audit-output/evidence/satisfying_and_excluded_witness.py)
and
[20_satisfying_and_excluded_k_witness.log](/audit-output/evidence/20_satisfying_and_excluded_k_witness.log).

### Body sensitivity

I made a fresh mutation to the macro-expanded function body actually loaded by
the entry claim: its final `Return(Name("closest"))` became
`Return(TupleExpr(Float(0.0), Float(0.0)))`. The modified proof definition
built successfully. The unchanged target result then failed with exit 1 and
`WarnStuckClaimState`; the residual explicitly contains the executed mutated
closure and the actual `(0.0, 0.0)` return against the expected folds. See
[body-sensitivity.patch](/audit-output/evidence/body-sensitivity.patch),
[22_build_body_mutation.log](/audit-output/evidence/22_build_body_mutation.log),
and
[23_body_sensitivity_expected_failure.log](/audit-output/evidence/23_body_sensitivity_expected_failure.log).
This demonstrates dependence on the executed body, not merely on an external
source filename.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory enumerates every module, configuration,
context, syntax declaration, rule, claim, attribute, priority, and source line
in all supplied K sources and all candidate-local K sources. It contains 1,073
records: 233 syntax records, 731 rules, one configuration, five contexts, and
eight claims. Of these, 1,001 records are in the byte-identical supplied
semantics and 72 are proof-local. The full line-addressable inventory is
[rule_inventory.md](/audit-output/evidence/rule_inventory.md), generated by
[inventory_k_rules.py](/audit-output/evidence/inventory_k_rules.py); generation
details are in
[19_rule_inventory_generation.log](/audit-output/evidence/19_rule_inventory_generation.log).

There is no candidate `semantic.k`: in this supplied-semantics condition the
25-file `reference-semantics` tree is the fixed baseline. I did not treat that
baseline as blessing `verification.k`. I checked every one of the 36
proof-local rules separately and inspected the complete fixed-semantics slice
used by the translated program. The inventory retains all 695 supplied rules,
including unused ones, so no opaque, total, priority, or concrete declaration
is silently omitted.

### Construct-to-semantics map

| Submitted construct | Fixed declaration/execution |
|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:124-127` |
| typing-only `ImportFrom` | `syntax.k:43`; non-math no-op `controls.k:35-36` |
| `FuncDef`, closure binding | `syntax.k:53`; `functions.k:14-16` |
| `Call`, callee and left-to-right arguments | `syntax.k:29`; `call.k:20-21`; `core.k:183-191` |
| user-function frame/parameter/return | `call.k:69-74`; `functions.k:63-66,78-90` |
| `Name` lookup and builtin binding | `core.k:131-181` |
| `Assign` | strict RHS in `syntax.k:41`; scope update in `controls.k:9-18` |
| `If` | strict condition in `syntax.k:49`; branch rules `controls.k:50-54` |
| `For`, iterator step, loop continuation | `syntax.k:45`; `controls.k:65-74`; list iteration `list.k:9-10` |
| `list(enumerate(numbers))` | builtin dispatch `call.k:31`; enumerate allocation/fold `builtins.k:123-129`; list copy/allocation `builtins.k:28-38`; allocator `core.k:118-121` |
| `Subscript` and tuple indices | evaluation contexts and dispatch `subscript.k:27-40`; positional recursion `subscript.k:7-23`; proof-local guarded projection lemmas |
| `TupleExpr` | left-to-right argument evaluation and construction `tuple.k:13-18` |
| `Compare` | contexts/dispatch `operators.k:14-17`; Int `<` `int.k:22`; Float `<` `float.k:50-52` |
| Float subtraction and `abs` | `float.k:103-105` and `float.k:54-56` |
| `Return` and frame pop | `functions.k:78-90` |

The fixed configuration models control, scope, heap allocation, call stack,
return state, exception state, and exit code. The entry claim constrains all of
those observable cells. Evaluation order is left-to-right for calls and tuple
construction; assignment/if/for strictness and the explicit comparison and
subscript contexts match the source evaluation order.

### Every proof-local declaration and rule

The four macro symbols `innerBody`, `outerBody`, `findBody`, and
`solutionModule` have four expansion rules. The corrected constructor
comparison proves their complete expansion is the submitted translated module;
they introduce no semantic step or task answer.

There are 15 proof-local total functions:

- Domain/projection functions: `allFloatVS`, `allFloatItems`,
  `floatProjection`, `itemIndex`, and `itemFloat`.
- Ordering/step functions: `orderedFirst`, `orderedSecond`, `candidateWins`,
  `stepFirst`, and `stepSecond`.
- Structural summaries: `innerFirst`, `innerSecond`, `outerFirst`,
  `outerSecond`, and `lastItem`.

`floatProjection`, `itemIndex`, and `itemFloat` are opaque only off their typed
constructor equations. Every result-bearing use is protected by equality to
the corresponding canonical Float or `(Int, Float)` constructor. The
recognizers recurse strictly over `ValSeq`; their empty/cons equations are
disjoint and exhaustive.

The three simplifications are:

1. `applyIndex(V, 0) => itemIndex(V)` under equality of `V` to the exact
   two-component canonical tuple;
2. the corresponding index-1 projection; and
3. `allFloatItems(enumVS(VS,I)) => true` when `allFloatVS(VS)`.

The first two follow directly from fixed tuple indexing; the fixed-only
projection claims freshly prove both. The third follows by structural
induction from the supplied `enumVS` equations, which construct exactly
`tuple(Int, Float)` items. Its guard prevents an off-domain conclusion.

`orderedFirst`/`orderedSecond` have complementary `floatLt` and
`notBool floatLt` guards. `stepFirst`/`stepSecond` have a non-winner case and
two complementary winner cases. Their overlaps are empty and together they
cover every Bool outcome. `candidateWins` is exactly the source conjunction:
increasing indices and strictly smaller absolute distance.

Each `inner*`, `outer*`, and `lastItem` function has disjoint empty/cons
equations and structurally descends its sequence. In each step, both output
components are computed from the same old accumulator before recursion, just
as the source assignment does. No fold is an unconstrained oracle.

The remaining proof-local rule is the priority-40 inner-loop bridge at
`verification.k:255`. Its complete match fixes:

- the exact `#loop(list(REST), Name("item2"), innerBody)` redex;
- arbitrary but preserved continuation;
- environment 1;
- the entire builtin, module, and local scope maps;
- the actual closure binding and `findBody`;
- canonical `item1`, all canonical remaining items, old `item2`, and old
  Float accumulator; and
- the exact updates to only `item2` and `closest`.

All omitted cells are framed and the continuation is preserved; the bridge
does not return, pop a frame, allocate, throw, or discard control. The
bridge-free connection theorem has the identical match domain and arbitrary
continuation and uses `VERIFICATION-BASE`, not `VERIFICATION`. A direct diff
of the fresh rule lists shows that the target definition contains exactly one
additional rule—the bridge at `verification.k:255`—over the connection
definition. See
[26_bridge_definition_delta.log](/audit-output/evidence/26_bridge_definition_delta.log).
The connection proof's fresh `#Top` and the body-sensitivity failure provide
the universal and operational-sensitivity evidence required by the Kit
contract.

I found no false proof-local equation, priority overlap, totality assertion, or
operational bridge. Accordingly, I make no “unsound rule” allegation requiring
a false-conclusion witness. The narrower gaps are instead stated explicitly:
the postcondition-to-global-minimum argument is informal, the proof uses the
supplied opaque float boundary, and runtime `Int` inputs are outside the formal
precondition.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation changes
the entry result's second component from `outerSecond(...)` to
`outerFirst(...)`, leaving the actual executed program and first component
unchanged. This is demonstrably false for the satisfying length-two witness
`[1.0, 2.0]`, where the required result is `(1.0, 2.0)`, and for the nontrivial
witness `[1.0, 9.0, 3.0, 4.0]`, where it would demand `(3.0, 3.0)` instead of
`(3.0, 4.0)`.

The exact mutation is
[fresh-vacuity.patch](/audit-output/evidence/fresh-vacuity.patch). It parsed
and compiled through `kprove --dry-run` with exit 0, as recorded in
[24_fresh_vacuity_dry_run.log](/audit-output/evidence/24_fresh_vacuity_dry_run.log).
The actual proof exited 1 with `WarnStuckClaimState`. Its residual explicitly
requires equality of the real `outerSecond` value and mutated `outerFirst`
value, so the failure is the expected reachable result obligation rather than
a parser error, missing import, timeout, or unrelated crash. See
[25_fresh_vacuity_expected_failure.log](/audit-output/evidence/25_fresh_vacuity_expected_failure.log).

The proof is therefore non-vacuous and discriminates a meaningful false
result.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the supplied MPY semantics, for every finite K `Float` list of arbitrary
length at least two, if execution terminates, loading the exact translated
submitted module and invoking its actual `find_closest_elements` binding
reaches the exact two-component recursive scan summary in `SPEC.find-closest`.
The scan considers every enumerated `i < j` pair, updates only on the supplied
strict distance comparison, and orders each selected pair through the same
supplied Float comparison used by the program. The theorem also establishes
the stated heap allocations, restored control state, empty stack, no exception,
and zero exit code. The two loop claims and the bridge-free connection theorem
establish the corresponding inner and outer summaries for unbounded finite
sequences.

The theorem does not merely establish examples or a bounded unrolling. It is
not shape-only, does not contain a free result oracle, and is sensitive to both
the program body and the second returned component.

### Trust and limitation ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Supplied MPY semantics and K/Haskell backend | All execution and proof steps | Foundational trusted input/tool boundary. Candidate copy is byte/type-identical to the trusted mount. |
| Trusted `py2mpy.py` | Python-to-constructor bridge | Byte-identical candidate copy; regenerated output is exact; macro-expanded constructor pin is exact. This is still a trusted frontend rather than a theorem about CPython AST semantics. |
| Supplied `subF`, `absF`, `floatLt` | Branching, distances, ordered result, all scan summaries | Fixed external primitives, `[no-evaluators]` for symbolic proof and `[concrete]` for execution. The K theorem is parametric because execution and postcondition use the same symbols; finite LLVM/Python tests support, but do not universally prove, Python float adequacy. |
| Mathematical scan invariant | Human phrase “the closest two” | Informal: initialization is one valid pair; after each enumerated `i < j` pair, strict replacement retains a minimum-distance pair among the processed prefix; all distinct position pairs are eventually processed; ordering is preserved. Straightforward and supported by differential tests, but not a separate K predicate/theorem. |
| Runtime `Int` and mixed numeric lists | Potential broad reading of “numbers” | Excluded by `allFloatVS`, although implementations handle them. Non-material under the explicit `List[float]` signature; disclosed as a scope boundary. |
| NaN and signed-zero exact behavior | Python/canonical special-float fidelity | NaN has no meaningful smaller/larger contract; signed zero is numerically equal but bitwise ordering differs. These cases prevent claiming universal bit-level canonical equivalence. |
| Termination | Total-correctness interpretation | Not separately claimed; the report is a Kit partial-correctness result. Structural folds and concrete executions provide evidence, not a separate total-correctness theorem. |

Differential tests, concrete K runs, and the informal scan invariant support
only the bridges named above. They are not substitutes for the reconstructed
reachability proof.

### Decision

Gate A (real-program soundness and non-vacuity) passes. The bridge is
independently connected to fixed execution, all proof-local equations are
truthful on their complete guards, the exact body is executed, and false/body
mutations are rejected.

The material declared source domain is unbounded `List[float]` of length at
least two, and the formal domain covers it at the supplied K-semantics level.
This is not a finite-size, examples-only, or bounded-unrolling theorem, so the
benchmark's mandatory `FAIL` mapping for material domain narrowing does not
apply.

There are nevertheless legitimate non-fatal limitations: the global-minimum
meaning is an informal bridge from a precise recursive scan specification, the
float primitives are an explicit external trust boundary, and special-float
bit-level behavior is not canonically equivalent. Those limitations rule out a
clean `PASS`, but none permits a false K conclusion or substitutes another
program. The candidate is therefore legitimate with concerns.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
