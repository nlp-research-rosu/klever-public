# Independent adversarial review: 52-below-threshold

This audit independently reconstructs a legitimate partial-correctness proof,
but with documented non-fatal limitations. The candidate pins the regenerated
program and proves the full unbounded domain of numeric lists representable by
the supplied MPY model. The `CONCERNS` rating is required because the supplied
model cannot represent otherwise defensible Python numeric classes such as
`Decimal`, and because one submitted empirical bridge comparison does not
actually exercise the exact bridge context. Neither limitation makes a false
conclusion provable.

## 1. Input and provenance integrity

### Launcher records and campaign lock

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `52-below-threshold`, and the
expected mounted paths. All mandatory launcher records are present, readable,
regular files (the trace root is a directory), and contain no symlinks:

- `/audit-input.json`
- `/audit-campaign-lock.json`
- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/runtime-metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- the structured JSONL trace beneath `/generation-evidence/codex-trace/`

The campaign object embedded in `/audit-input.json` is structurally identical
to `/audit-campaign-lock.json`. The lock's independently calculated SHA-256 is
`053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01`,
exactly the hash recorded in `/audit-input.json`.

Every directly launcher-declared file hash checked against its mounted file
matches, including the run/task/result manifests, invocation and metrics
records, prompt, canonical, translator, generation logs, runtime metrics, and
usage record. The sole trace file has SHA-256
`9b25e5750f3c8e3776dfa45f72b82aed4190340e3f907202720b04ea253bb0f8`,
matching `/generation-result.json`. All 1,021 trace lines parse as JSON; the
event counts are 1 `session_meta`, 307 `event_msg`, 708 `response_item`, 2
`world_state`, 2 `turn_context`, and 1 `compacted`.

The exact checks, hashes, record excerpts, generation-claim surfaces, and exit
statuses are in
[stage1_integrity.log](evidence/stage1_integrity.log). Independent full-tree
type and per-file SHA-256 manifests cover all 840 candidate files and all 8
generation-evidence files; their command record is
[stage1_tree_manifests.log](evidence/stage1_tree_manifests.log), with manifests
in [candidate-tree-sha256.txt](evidence/candidate-tree-sha256.txt),
[candidate-tree-types.txt](evidence/candidate-tree-types.txt),
[generation-tree-sha256.txt](evidence/generation-tree-sha256.txt), and
[generation-tree-types.txt](evidence/generation-tree-types.txt).

### Trusted-input and supplied-semantics integrity

`cmp` establishes byte identity for:

- `/candidate/prompt.py` and `/reference/prompt.py`;
- `/candidate/py2mpy.py` and `/reference/py2mpy.py`.

`diff -qr --no-dereference` reports no difference between
`/candidate/reference-semantics/` and
`/reference/reference-semantics/`. Independently generated type and per-file
hash manifests are byte-identical for the two trees:

- type-manifest SHA-256:
  `78189a305a2e25fa2ee501dabbe1df959b18747ccf96157534a603671c866329`;
- per-file-hash-manifest SHA-256:
  `fe7c5f2006be1642110fcb8ef3c666b1f86dc389c7d33fb2878394aeb633d5ac`.

No candidate, reference, or generation-evidence entry is a symlink. The trusted
reference-semantics mount is present as required by `SUPPLIED_SEMANTICS`.
Candidate-provided kompiled directories were inventoried but never used.

There is no infrastructure breach. Generation logs, `PROOF.md`, and historical
`#Top` reports were read only as untrusted claims.

## 2. Program fidelity and candidate-versus-canonical checks

### Docstring-first contract

`/reference/prompt.py` requires
`below_threshold(l: list, t: int)` to return true exactly when every number in
`l` is strictly below `t`. Consequently:

- the empty list returns true;
- equality with the threshold returns false;
- one below/equal/above element exercises all branch boundaries;
- a later failing element makes the result false;
- the two documented examples return `True` and `False`, respectively.

`/reference/canonical.py` is a witness using `e >= t`. The candidate in
`/candidate/solution.py:1` uses the extensionally equivalent ordinary-number
form “continue when `e < t`, otherwise return false,” then returns true after
exhaustion. It is a different implementation but follows the docstring
directly.

### Trusted regeneration

The command

```text
python3 /reference/py2mpy.py /candidate/solution.py
```

exits 0. Its saved output is byte-identical to
`/candidate/solution.mpy`; both SHA-256 values are
`fe8e905b51c529928f4eaa84d902f750bc8df20db7e7c57cb202d318017f86ca`.
See [stage2_program.log](evidence/stage2_program.log).

### Independent differential

The reviewer-authored
[differential_stage2.py](evidence/differential_stage2.py) imports the submitted
and trusted canonical entry points independently and uses direct strict
`all(value < threshold for value in values)` as its docstring oracle. It ran:

- both documented examples;
- empty, singleton below/equal/above, late equal/above, negative-threshold,
  Boolean, finite-float, infinity, and NaN cases;
- every list of lengths 0 through 4 over nine boundary representatives and
  thresholds -2 through 2 (36,905 cases);
- 5,000 independently seeded random integer lists of lengths 0 through 50,
  including arbitrary-precision magnitudes.

The exact result was:

```text
total_cases=41920
candidate_contract_mismatches=0
canonical_contract_mismatches=2
candidate_canonical_divergences=2
```

Both divergences are NaN cases: the candidate returns false because NaN is not
strictly below the threshold, whereas canonical's `NaN >= t` is also false and
therefore canonical returns true. Non-finite handling is expressly
underdetermined under campaign amendment v3. The candidate's strict-reading
choice is defensible and is not a defect.

## 3. Clean proof reconstruction

All required source files were copied to
`/tmp/audit-work/reconstruction/`; the trusted semantics came from
`/reference/reference-semantics`, not the candidate copy. No candidate cache or
kompiled definition was copied. Fresh definitions were built with K
v7.1.293.

### Concrete reconstruction

The fresh command

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
```

exited 0. A reviewer smoke program containing the exact submitted function and
documented, empty, equality, negative, Boolean, and finite-float cases ends
with `<k> .K </k>`, `<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`;
see [stage3_smoke_corrected.log](evidence/stage3_smoke_corrected.log).

For transparency, the first aggregate reconstruction script exited 1 because
the reviewer initially wrote the false expectation that `[-4, -3, -2]` is
entirely below `-2`. The fresh semantics correctly raised `AssertionError`.
The reviewer source was corrected to expect false and rerun successfully. This
auditor-authored test error is visible in
[stage3_reconstruction.log](evidence/stage3_reconstruction.log) and is not
attributed to the candidate.

### Proof-definition reconstruction and positive claims

All three Haskell definitions compiled from source with exit 0:

```text
kompile --backend haskell base-verification.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition fresh-connection-kompiled

kompile --backend haskell verification-loops.k \
  --main-module VERIFICATION-LOOPS --syntax-module MPY-SYNTAX \
  --output-definition fresh-loop-verification-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

Every positive claim was then selected and run independently. Each command
exited 0 and printed an exact `#Top` line:

| Proof group | Independently reconstructed claims |
|---|---|
| Comparison connection | `cmp-int`, `cmp-bool`, `cmp-float`, and the combined file |
| Loop connection | `loop-empty`, `loop-cons` |
| `For` connection | `for-empty`, `for-cons`, composed using only the already closed loop claims as `--trusted` |
| Entry theorem | `below-threshold-empty`, `below-threshold-int`, `below-threshold-bool`, `below-threshold-float`, and the combined file |

Per-command logs are
[stage3-prove-cmp-int.log](evidence/stage3-prove-cmp-int.log),
[stage3-prove-cmp-bool.log](evidence/stage3-prove-cmp-bool.log),
[stage3-prove-cmp-float.log](evidence/stage3-prove-cmp-float.log),
[stage3-prove-loop-empty.log](evidence/stage3-prove-loop-empty.log),
[stage3-prove-loop-cons.log](evidence/stage3-prove-loop-cons.log),
[stage3-prove-for-empty.log](evidence/stage3-prove-for-empty.log),
[stage3-prove-for-cons.log](evidence/stage3-prove-for-cons.log), and the five
`stage3-prove-entry-*.log` files. The complete exact command sequence is in
[stage3_reconstruction.sh](evidence/stage3_reconstruction.sh).

The comparison claims produce `WarnTrivialClaim` because each fixed dispatch
and its definition reduce to the same primitive expression. That warning is
not accepted as non-vacuity evidence; the separate Stage 6 mutation supplies
that gate.

## 4. Adequacy and real-program pinning

### Plain-language claims

The four entry claims in `/candidate/spec.k` say:

1. for every K `Int` threshold, the empty modeled list returns `true`;
2. for an `Int`-headed list whose symbolic tail is entirely numeric, return
   `allBelow` of the entire list;
3. the same for a `Bool`-headed list;
4. the same for a `Float`-headed list.

`numericSeq` permits an arbitrary finite tail mixing `Int`, `Bool`, and
`Float`; it does not bound length. `allBelow` is true on empty and otherwise is
the conjunction of strict modeled comparisons over every element. `Bool`
promotes to 0/1 as in Python. Threshold `T:Int` exactly matches the annotated
source threshold.

The empty/nonempty and three head sorts are disjoint and exhaustive over every
numeric `Val` represented by this supplied model. The postcondition is an
exact result, not an implication, existential value, or unconstrained
variable. `?FINALSCOPES` frames irrelevant final module-scope detail; it does
not weaken the `<k>` result or the unchanged heap, stack, return, exception,
and exit cells.

### Constructor-level body identity

[extract_claim_modules.py](evidence/extract_claim_modules.py) independently
extracts all four `#loadAll(Module(...))` arguments. The arguments are
textually identical. K's rule parser spells the empty `If` else-list as
`.Stmts`; the standalone program parser spells the same
`List{Stmt,""}` unit as an omitted list item. After only that documented
normalization, `kast --sort Module --output json` produces byte-identical KAST
for regenerated `solution.mpy` and all four claim modules. All five KAST files
have SHA-256
`4a93b89b15a7486742d8640df09cbb52a8566c4d3fceef262d1d5d4b10f4528e`.
The successful comparison is in
[stage4_pinning_corrected.log](evidence/stage4_pinning_corrected.log).

An earlier attempt fed rule-only `.Stmts` notation directly to the standalone
program parser and received a scanner error. That evidence-method error is
preserved in [stage4_pinning.log](evidence/stage4_pinning.log); the corrected
constructor comparison, not the failed attempt, supports pinning.

Thus `<k>` loads the exact binding, parameter order, docstring expression,
assignment, loop, comparison, `continue`, and return structure of the
submitted program. The function body, rather than an external file name or
oracle, is part of each theorem term.

### Satisfiable witnesses and ground results

Every entry precondition has a concrete witness:

| Partition | List and threshold | Claimed result | Submitted Python | Canonical |
|---|---|---:|---:|---:|
| Empty | `[], 0` | `True` | `True` | `True` |
| Int head | `[1, 3], 3` | `False` | `False` | `False` |
| Bool head | `[False, True], 1` | `False` | `False` | `False` |
| Float head | `[0.5, -2], 1` | `True` | `True` | `True` |

These exact results are recorded by
[stage4_witness.py](evidence/stage4_witness.py) and
[stage4_decimal_python.log](evidence/stage4_decimal_python.log). Stage 3's
fresh LLVM execution independently exercises all four modeled partitions.

### Domain adequacy and supplied-model gap

The theorem covers arbitrary finite lists of all numeric classes present in
the fixed `Val` model: `Int`, `Bool`, and `Float`, with no extra size,
magnitude, finiteness, or ordering precondition. The bare `list(ValSeq)`
representation is the supplied semantics' documented read-only claim
representation (`semantics/core.k:71-72`); the verified function performs no
identity test or mutation, so boxing the same contents behind `ref` adds no
observable source behavior here.

The fixed model has no `Decimal` or `Fraction` value class or corresponding
builtin/import binding. This is a supplied-model representation gap, not a
candidate restriction. The candidate already identifies unrepresented numeric
classes as a supplied-model boundary in `/candidate/PROOF.md:230-231`; the
following independent concrete witness completes that trust-ledger entry and
satisfies amendment v2's exception:

- CPython executes the submitted program on `[Decimal("1.5")], 2` as `True`
  and `[Decimal("2.0")], 2` as `False`; the direct strict oracle and canonical
  agree ([stage4_decimal_python.log](evidence/stage4_decimal_python.log)).
- Translating the same exact function plus those calls succeeds, but the
  trusted MPY execution stops at `#look("Decimal", -1)` rather than completing
  ([stage4_pinning_corrected.log](evidence/stage4_pinning_corrected.log)).
- `/reference/reference-semantics/semantics/core.k:25-38` enumerates the fixed
  `Val` classes, and `/reference/reference-semantics/semantics/controls.k:35-46`
  supports only selected `math` imports.

The divergence is model-versus-CPython. The submitted program itself is
faithful on the gap. Because the theorem covers every numeric input the fixed
model can represent and the gap is now concrete in this trust ledger, campaign
amendment v2 maps it to `CONCERNS / LEGIT`, not failure.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated
[rule-inventory.tsv](evidence/rule-inventory.tsv) is an exhaustive mechanical
inventory of all selected fixed and local K sources. Its corrected totals are:

- 24 fixed files;
- 764 supplied fixed semantic rules;
- 244 supplied fixed syntax declarations;
- 5 fixed evaluation contexts;
- 1 fixed configuration;
- all fixed modules, imports, requires, and endmodules;
- 5 candidate-local syntax declarations;
- 16 candidate-local rules;
- 11 claims across the connection, loop, and entry specifications.

The summary is
[rule-inventory-summary.txt](evidence/rule-inventory-summary.txt), and the
corrected generation log is
[stage5_inventory_corrected.log](evidence/stage5_inventory_corrected.log).
The first inventory log is retained because it incorrectly split guarded rules
at indented `requires` clauses and had a search-regex error; no conclusion
relies on that first pass.

There are no candidate-local `[functional]` or opaque declarations. The fixed
model contains 26 `[no-evaluators]` declarations; only `ltFI(Float, Int)`
contributes to this theorem. The four local operational rules all have
`priority(40)`. The sole local simplification is the guarded comparison
dispatch.

### Candidate-local rules

Every one of the 16 local rules has the following disposition:

| Rules | Classification and decision |
|---|---|
| `numericVal` (1) | Total sort recognizer. It is true exactly for K `Int`, `Bool`, or `Float`. Sound. |
| `numericSeq` (2) | Empty/cons equations are disjoint, exhaustive, and recurse on the strict tail. Sound. |
| `numericLt` (4) | Typed `Int`, `Bool`, and `Float` equations are disjoint; `[owise]` is their complement. `Bool` uses fixed 0/1 coercion and `Float` names fixed `ltFI`. Sound. |
| `allBelow` (2) | Empty/cons equations are disjoint and structurally descending. They define the exact universal strict-comparison result. Sound. |
| `lastVisited` (2) | Empty preserves the old loop variable; cons updates to the visited value and descends only when comparison succeeds. This exactly captures exhaustion versus first failure. Sound. |
| guarded `applyCmp` simplification (1) | The `numericVal` guard partitions into three fixed-dispatch cases. The bridge-free `cmp-int`, `cmp-bool`, and `cmp-float` claims each freshly close. Its overlaps with fixed rules have identical right-hand values. Sound derived lemma. |
| `#loop` empty/cons bridges (2) | Each is byte-for-byte the corresponding bridge-free reachability claim after removing only `rule`/claim-label/priority metadata. Sound operational bridges. |
| source `For` empty/cons bridges (2) | Each is likewise exactly the corresponding bridge-free `For` claim, proved from one fixed `For` step plus the already proved loop claims. Sound operational bridges. |

The mechanical four-pair comparison is
[compare_bridges.py](evidence/compare_bridges.py), with all four results `True`
in [stage5_static_checks.log](evidence/stage5_static_checks.log).

The bridge domains are mutually disjoint: `#loop` versus `For`, and empty
versus cons. The nonempty guards require the head and entire tail numeric.
They match the exact body, local binding names and values, parent scope,
continuation
`Return(Bool(true)) ~> #endcall`, caller frame `frame(.K,0,1)`, environment,
scope counter, return/exception/exit states, and preserve arbitrary heap and
heap counter. Their right sides reproduce return value, final `e`, frame
deletion, environment restoration, scope-counter restoration, and stack pop.
They do not admit an arbitrary continuation or extra frame.

The connection proofs do not import the operational bridges:

- `connection-spec.k` imports `VERIFICATION-BASE`, before the comparison
  simplification;
- `loop-spec.k` imports `VERIFICATION-LOOPS`, which has the comparison lemma
  but no operational bridge;
- the two loop claims freshly close before they are used as trusted
  composition lemmas for the two `For` claims.

### Used fixed-semantics path

All material constructors in `solution.mpy` map to fixed declarations and
rules:

| Program behavior | Fixed source and relevant behavior |
|---|---|
| `Module`, statement lists, `#loadAll` | `syntax.k`; `core.k:121-125` loads and sequences statements left to right. |
| `FuncDef` and binding | `functions.k:13-16` installs the exact closure body in current scope. |
| `Call`, callee and arguments | `call.k:16-21` plus `core.k:187-195` evaluate callee and arguments left to right. |
| User call/frame | `call.k:71-77` binds a fresh local scope and saves the exact caller continuation. |
| Parameter binding | `functions.k:56-67` binds parameters in order. |
| `Expr(Str(...))` docstring | strict evaluation plus `controls.k:48` discards its value with no effect. |
| `Assign(Name("e"), Int(0))` | `syntax.k` strict RHS, `core.k:199-202` literal, and `controls.k:9-18` current-scope update. |
| `Name` lookup | `core.k:128-153` performs scoped lookup. |
| `For` and list iteration | `controls.k:65-74`; `list.k:8-9` returns empty/done or head/yield/rest. |
| `Compare("<", ...)` | evaluation contexts and dispatch in `operators.k:11-18`; typed cases in `int.k:31`, `bool.k:12-18`, and `float.k:158-175`. |
| `If` | strict condition followed by `truthy(Bool)` and the disjoint branch rules at `controls.k:51-54`. |
| `Continue` | `controls.k:85-91` unwinds only to the loop label and resumes the saved next iteration. |
| `Return`/normal fallthrough | `functions.k:70-84` records the value, deletes the frame, restores environment and scope location, and returns to the exact continuation. |

Evaluation order, branch control, scope mutation, return control, and all
observable cells used by this function are therefore modeled. The input
elements are already values; no skipped element expression can have a side
effect.

Fresh body sensitivity was tested independently by changing `<` to `>` in the
program term while retaining the docstring-required result for `[1], 2`. The
operational bridges no longer match, fixed execution reaches `false`, and
`kprove` exits 1 with `WarnStuckClaimState`. See
[stage5-body-mutation-kprove.log](evidence/stage5-body-mutation-kprove.log).
This proves dependence on the body actually present in the theorem, not merely
on the external source file.

### Fixed opaque primitive and compiler observations

`ltFI(Float, Int)` is a supplied fixed primitive, declared total and opaque to
the Haskell prover, with concrete LLVM equations for finite and non-finite
floats at `/reference/reference-semantics/semantics/float.k:158-175`. It
affects the float branch and any mixed tail containing floats. The
bridge-free connection proves that fixed program execution produces exactly
this primitive; the theorem is interpretation-parametric in its fixed
contract. Fresh LLVM finite-float execution and Python differential evidence
support, but do not universally prove, the CPython bridge.

Fresh compilation reports fixed-model non-exhaustiveness warnings for several
unrelated total helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`,
and `valSeqAt`) on internal value shapes. None occurs on the verified
constructor/rule path. They remain supplied-model observations, not
candidate-local unsoundness.

No candidate-local false rule was found, so no unsoundness label or false-rule
witness is asserted.

### Limitation in submitted bridge-smoke evidence

The submitted `bridge-smoke.py` exists and its fixed-versus-extended full-state
diff is reproducible, but its calls occur inside `Compare`/`Assert`
continuations. A user-call frame there has a nonempty saved continuation,
whereas every bridge requires exactly `frame(.K, 0, 1)`. Consequently that
source-level smoke comparison does not demonstrate that the priority bridges
fired; both definitions can execute through fixed semantics. This weakens the
candidate's empirical Gate C claim.

It does not invalidate Gate A: the universal bridge-free loop/`For` claims
cover the complete bridge match domain, all four rules are mechanically
identical to those claims, and the fresh body-sensitivity failure independently
shows that altered execution is not accepted.

## 6. Fresh non-vacuity test

The reviewer-created
`/tmp/audit-work/reconstruction/stage6-false-postcondition.k` contains the
unmodified, constructor-identical submitted body and the satisfiable input
`[1], 2`, but deliberately demands `false`.

The dry run

```text
kprove stage6-false-postcondition.k \
  --definition fresh-verification-kompiled \
  --spec-module STAGE6-FALSE-POSTCONDITION --dry-run
```

exits 0, so the mutation parses and builds. The actual proof command exits 1,
prints `WarnStuckClaimState`, and exposes the expected unmet obligation:

```text
<k>
  true ~> .K
</k>
```

This is the actual result for the satisfying witness and directly contradicts
the mutated `false` destination. It is not a parser error, timeout, missing
import, unrelated crash, or unreachable mutation. The exact script and logs
are [stage6_nonvacuity.sh](evidence/stage6_nonvacuity.sh),
[stage6-false-postcondition-dry-run.log](evidence/stage6-false-postcondition-dry-run.log),
and
[stage6-false-postcondition-kprove.log](evidence/stage6-false-postcondition-kprove.log).

## 7. Proven versus assumed accounting

### Precisely proven

Subject to the fixed supplied semantics and K reachability logic, the
reconstructed partial-correctness proof establishes:

> For every K `Int` threshold and every arbitrary finite `ValSeq` whose
> elements are any mixture of modeled `Int`, `Bool`, and `Float`, loading the
> exact regenerated `below_threshold` binding and calling it from the stated
> initial configuration reaches normal return value
> `allBelow(sequence, threshold)`, with the stated restored environment,
> deleted callee frame, unchanged heap, empty stack, `NoExc`, and exit code 0.

`allBelow` is recursively true exactly when every element's fixed strict
comparison summary is true. The theorem is not bounded by examples, list
length, integer magnitude, or float finiteness. It proves the submitted
program term, not canonical and not an oracle-substituted implementation.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Trusted prompt and docstring | Defines the required behavior. | Authoritative by campaign rule. |
| Trusted translator | Connects inspected Python AST to MPY constructors; all entry terms depend on it. | Acceptable; byte regeneration plus KAST identity independently checked. |
| Supplied reference semantics | Defines loading, calls, cells, scopes, iteration, comparisons, and control. Every proof depends on it. | Required fixed trust boundary; tree integrity and used paths audited. |
| K toolchain v7.1.293 and K builtins | Compilation, rewriting, reachability, map/list/Int/Bool/Float hooks. | Standard unavoidable checker boundary; versions and fresh builds recorded. |
| Fixed `ltFI(Float,Int)` | Controls all float comparisons and thus float-bearing results. | Acceptable but notable; bridge-free exact connection plus finite LLVM/Python evidence, universal CPython meaning remains conditional on the supplied primitive. |
| Two loop claims passed via `--trusted` while proving two `For` claims | Allows proof composition. | Acceptable: the exact two claims were independently run immediately beforehand and returned `#Top`; no unproved property is trusted. |
| Bare `list(ValSeq)` claim representation | Represents read-only list contents without heap boxing. | Acceptable for this pure, non-identity-observing function; it is an explicit supplied-model convention. |
| Python differential | Supports implementation/docstring fidelity on 41,920 finite cases. | Finite empirical evidence only; not used as a universal proof. |
| `Decimal` and other unrepresented numeric classes | Outside the fixed model but within a defensible broad reading of “numbers.” | Documented supplied-model gap. The theorem covers every modeled numeric class and the submitted Python is faithful on the concrete gap witness. Amendment v2 requires `CONCERNS / LEGIT`. |
| NaN canonical divergence | Candidate returns false; canonical returns true. | Docstring-underdetermined non-finite handling under amendment v3; candidate's strict-reading behavior is defensible. |
| Submitted bridge-smoke context | Does not itself show the exact `.K`-frame bridges firing. | Non-fatal Gate C evidence limitation; universal bridge-free connections provide soundness. |

### Gate and verdict mapping

- Gate A, real-program soundness: **PASS**. Fresh proof closure, exact program
  pinning, exhaustive local-rule audit, bridge-free connections, body
  sensitivity, and fresh non-vacuity all pass.
- Gate B, intent adequacy: **PASS within the supplied representation**, with
  the campaign-amendment representation-gap qualification. The unrestricted
  modeled numeric-list domain is covered; no candidate-caused finite bound or
  extra narrowing exists.
- Gate C, trust/evidence auditability: **PASS with concerns**. Artifacts and
  exact commands exist, but the float primitive remains a supplied opaque
  boundary and the submitted bridge-smoke comparison is not bridge-sensitive.

The proof is therefore sound, result-constraining, unbounded, and pins the real
generated program. It is not `PASS / LEGIT` because the concrete supplied-model
representation gap falls under the amendment's mandatory
`CONCERNS / LEGIT` exception, reinforced by the empirical bridge-smoke
limitation. It is not `FAIL / NOT_LEGIT`: there is no failed reconstruction,
vacuity, substituted body, candidate-caused material domain restriction, or
unsound local rule.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
