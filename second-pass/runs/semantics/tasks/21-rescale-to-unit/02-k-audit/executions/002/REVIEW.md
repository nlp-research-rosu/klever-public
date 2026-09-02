# Independent adversarial audit: 21-rescale-to-unit

The submitted Python implementation is faithful to the canonical program, and
the submitted K claim does reconstruct to `#Top`. The proof is nevertheless
not legitimate: two priority rules replace the program's `min` and `max`
computations with unconstrained, result-bearing symbols, and the postcondition
uses those same symbols. No fixed-semantics connection theorem determines that
they are the actual extrema. The proof therefore establishes a circular
structural statement under a modified theory, not partial correctness of the
real generated program against the source contract.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `21-rescale-to-unit`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- campaign `bare-semantics-audit-20260726`.

I used the `container_paths` mounts rather than the host provenance paths.
The campaign block is structurally identical to
`/audit-campaign-lock.json`, whose independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

All records required for `legacy-selected-stage1` are real regular files or
real directories of the expected type: `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
`usage.json` is present and was inspected. The historical
`legacy-metrics.json` and `legacy-run-input.json` are also present and their
hashes match both generation manifests. No historical runtime-metrics record
is required for this layout. The trace contains one regular JSONL file, parses
as 245 records, and has the recorded file SHA-256. The generation records were
treated only as untrusted claims.

Independent hash/type results are in
[`stage1_integrity_rerun`](evidence/stage1_integrity_rerun/output.log) and
[`stage1_types_hashes`](evidence/stage1_types_hashes/output.log). Every
recorded single-file hash checked there matches. An independent implementation
of the launcher's typed tree digest produced:

- `4e06397a...` for trusted reference semantics, matching
  `trusted_reference_semantics_manifest_sha256`;
- `cfa39515...` for the candidate tree, matching the retained
  `workspace_sha256` in both stage-1 manifests;
- `97a37edb...` for the trace tree, matching `usage.json`'s
  `source_trace_sha256`.

See [`stage1_tree_hash_exact`](evidence/stage1_tree_hash_exact/output.log).
The candidate and trusted prompt are byte-identical, as are the candidate and
trusted translator. The candidate and reference mounts contain no symlinks.

The trusted `/reference/reference-semantics` tree is present as required.
Recursive entry/type comparison found exactly 25 entries in each tree
(one subdirectory and 24 files), no missing or additional entry, and no byte
difference. The complete relative per-file hash list is preserved in
[`stage1_tree_digest_probes`](evidence/stage1_tree_digest_probes/output.log);
that exploratory command's final exit 2 is only a reviewer `printf` formatting
mistake after all comparisons had passed. The authoritative integrity rerun
exits 0. The first `stage1_integrity` run also contained an intentionally
over-strict reviewer check equating the embedded audit manifest with
`task.json`; the embedded object legitimately adds `config`. The corrected
shared-field and recorded-hash check is the exit-0 rerun cited above.

There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires a list of at least two floats to be transformed
linearly so its minimum becomes 0 and its maximum becomes 1. The trusted
canonical implementation computes `min(numbers)`, computes `max(numbers)`,
and returns the order-preserving list
`(x - min) / (max - min)` for every input element. Equal-valued lists make the
Python implementation raise `ZeroDivisionError`; non-finite floats also expose
the usual IEEE/Python edge behavior, so the endpoint prose is meaningful
without qualification only on normally returning inputs with distinct finite
extrema.

`solution.py` uses the same algorithm, with only a comprehension variable
rename and formatting differences. Running the trusted translator in clean
scratch:

```text
cd /tmp/audit-work/21-rescale-to-unit-audit
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -l solution.mpy regenerated-solution.mpy
```

exited 0, and both files have SHA-256
`bdb65c4c8c0e79045c2cfb52c9643f3803e3e3f6ff93ee83716c423f19b0da88`.
See [`stage2_translation_identity`](evidence/stage2_translation_identity/output.log).

The independent differential test imports the trusted canonical and generated
entry points separately. It covers the documented example; empty, singleton,
equal-extrema, ascending, descending, negative, duplicate-extrema, large
finite, infinity, and NaN cases; plus 2,000 seeded lists of lengths 2 through
25. It found zero mismatches. The script, complete deterministic input corpus,
command, result, and exit status are:

- [`differential_test.py`](evidence/differential_test.py)
- [`differential_inputs.json`](evidence/differential_inputs.json)
- [`stage2_differential_with_inputs`](evidence/stage2_differential_with_inputs/output.log)

This finite evidence supports implementation equivalence. It is not a
universal proof and does not validate any K proof-local abstraction.

## 3. Clean proof reconstruction

I copied source artifacts to
`/tmp/audit-work/21-rescale-to-unit-audit`, taking the supplied semantics from
the trusted reference mount. I copied no candidate `__pycache__`, compiled
definition, or cache. The toolchain is K `v7.1.293`, matching the campaign.

The concrete definition was rebuilt with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. The trusted translator regenerated `smoke.mpy` byte-identically,
and:

```text
krun regenerated-smoke.mpy --definition runtime-kompiled
```

exited 0 with an empty `<k>` cell, `NoExc`, and exit code 0 after the three
candidate smoke assertions. Evidence:
[`stage3_kompile_llvm`](evidence/stage3_kompile_llvm/output.log) and
[`stage3_krun_smoke`](evidence/stage3_krun_smoke/output.log).

The proof definition was rebuilt with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

It exited 0. A source inventory found exactly one positive target claim.
Independently running:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`. Evidence:
[`stage3_kompile_haskell`](evidence/stage3_kompile_haskell/output.log),
[`stage3_positive_claim_inventory`](evidence/stage3_positive_claim_inventory/output.log),
and [`stage3_kprove_positive`](evidence/stage3_kprove_positive/output.log).
Compiler warnings concern fixed-semantics unused variables and existential
final cells; they do not negate this reconstruction.

Thus the candidate passes the mechanical closure check under its submitted
theory. That check does not establish soundness of the theory.

## 4. Adequacy and real-program pinning

### Plain-language claim

The entry precondition starts from the semantics' standard module state and
supplies a `ValSeq` with two explicit `Float` heads and an arbitrary tail
satisfying `allFloats`. It therefore covers arbitrary lengths of at least two;
it is not a finite unrolling.

The postcondition requires normal restored control state and an observed
returned list whose elements are described by `scaleAcc` over the original
sequence, using `minVF(original)` as the low value and `maxVF(original)` as the
high value. Final scope, heap, and allocator contents are existential.

### Program identity

`#runRescale` expands to a complete `Module` containing the submitted binding
and function body, followed by a call to `rescale_to_unit` and `#observe`.
A reviewer script extracted the embedded `Module`. The only textual
normalization was `FreeVars(.ParamNames)` to the external program parser's
equivalent empty-list spelling `FreeVars()`. Parsing both terms with macro
expansion to KORE yielded identical bytes and SHA-256
`90fa8d2ef6f00ea1c5a535ab4d86b0728eb21254ff1514e56457b87e40aaacc3`.
See [`extract_claim_program.py`](evidence/extract_claim_program.py) and
[`stage4_constructor_identity_rerun`](evidence/stage4_constructor_identity_rerun/output.log).

A body-sensitivity mutation changed the denominator operator in the embedded
executed body from subtraction to addition while leaving the proof summary for
the original body unchanged. The mutated definition compiled, but proof exited
1 with `WarnStuckClaimState` and the expected `addF(...)` versus `subF(...)`
result mismatch. This mutation changes the program term actually executed by
the claim. Evidence:
[`verification-body-mut.k`](evidence/mutations/verification-body-mut.k),
[`stage4_body_mutation_build`](evidence/stage4_body_mutation_build/output.log),
and [`stage4_body_mutation_proof`](evidence/stage4_body_mutation_proof/output.log).
The claim therefore pins the submitted body and is body-sensitive.

### Satisfiability and concrete substitution

`FIRST = 1.0`, `SECOND = 2.0`, and `REST = .ValSeq` satisfy the entry
precondition because `allFloats(.ValSeq) => true`. Both trusted canonical
Python and candidate Python return `[0.0, 1.0]`. The instantiated K
postcondition, however, remains:

```text
list(scaleAcc(.ValSeq, [1.0,2.0],
              minVF([1.0,2.0]), maxVF([1.0,2.0])))
```

No equation or claim reduces those extrema symbols to `1.0` and `2.0`.
See [`ground_witness.py`](evidence/ground_witness.py) and
[`stage4_ground_witness`](evidence/stage4_ground_witness/output.log).

The result is not a free RHS variable or an implication-only tautology: it is
structurally constrained. But it is constrained only relative to the same
opaque extrema inserted into execution by the proof rules. No K theorem shows
that the result uses actual extrema or that the minimum and maximum outputs
are 0 and 1. Real-program pinning passes; result-to-contract adequacy fails.

## 5. Rule-by-rule static soundness review

The exhaustive lexical inventory covers the clean trusted supplied semantics,
`verification.k`, and `spec.k`: 26 files, 951 records, comprising 236 syntax
declarations, 708 rules, five contexts, one configuration, and one claim.
Every full source block, including functions, `total`, opaque `symbol` /
`no-evaluators`, `concrete`, priority, `owise`, strictness, and macro
attributes, is in [`rule_inventory.md`](evidence/rule_inventory.md).
[`rule_assessment.tsv`](evidence/rule_assessment.tsv) assigns a disposition and
rationale to every one of the 951 records, with no unclassified record.

The 928 declarations from `reference-semantics` are launcher-trusted fixed
semantics and byte-identical to the mounted baseline. Of these, 565 are in
modules participating in the submitted program's execution path and 363 are
unreachable from this program. The fixed trust does not extend to
proof-specific rules. The constructor-to-rule mapping in
[`program_construct_map.md`](evidence/program_construct_map.md) checks the
configuration, cells, module/statement sequencing, typing-only import,
closure-cell binding, name lookup, call and return frames, left-to-right
argument/operator evaluation, list iteration/allocation, and comprehension
control flow.

The proof-local inventory is:

| Extension | Classification and decision |
|---|---|
| `minVF`, `maxVF` (`verification.k:9-10`) | Program-derived, result-bearing opaque functions. Rejected: no defining equations and no bridge-free connection theorem. |
| priority `min` / `max` rules (`verification.k:12-17`) | Operational bridges. Binding and argument evaluation have already selected `builtinV("min"/"max")`, and the fixed fold is state-pure, but the returned value is replaced by the unconstrained symbols. Rejected. Their unguarded domain is also broader than the nonempty all-float target domain. |
| `asFloat` (`verification.k:21-22`) | Identity is true on `Float`. The `total` declaration is not exhaustive over all `Val`; this is a limited global declaration, but the target precondition restricts every use to `Float`, so it is not the decisive defect. |
| `scaleF`, `scaleAcc` (`verification.k:24-35`) | Truthful structural definitions. Base/cons guards are disjoint, recursion descends on `REST`, and `valSeqConcat` preserves order. |
| `allFloats` (`verification.k:37-40`) | Truthful, exhaustive structural predicate over `ValSeq`. |
| `FloatSeq` / `injectFloats` (`verification.k:44-48`) | Exhaustive and descending, but unused by the target claim. |
| exact `ListComp` summary (`verification.k:54-81`) | Operational bridge. It reads the current binding/cell values and allocates the described output, but skips the fixed comprehension call/frame/loop and accepts an arbitrary continuation. No bridge-free universal connection theorem covers its complete context or state footprint. I record this as an unjustified evidence gap rather than independently label it false, because no separate false-result witness for this rule alone was established. |
| `#observe` (`verification.k:85-87`) | Sound for its exact heap match: it reads the value stored at the returned reference. |
| `#runRescale` (`verification.k:91-119`) | Sound program wrapper. Constructor identity and body sensitivity were checked mechanically. |

There are no proof-local simplification rules, lemmas, or auxiliary claims.
The only claim is `spec.k:6`.

### False-conclusion witness for the rejected extrema bridges

The original theory imposes no equation on `minVF` or `maxVF`, so it admits an
interpretation in which both are constant fresh Float values `wrongLo()` and
`wrongHi()`. I made that interpretation explicit while leaving the original
claim shape unchanged. The definition compiled, and:

```text
kprove spec-wrong-extrema-original-shape.k \
  --definition verification-wrong-opaque-extrema-kompiled \
  --spec-module SPEC-WRONG-EXTREMA-ORIGINAL-SHAPE
```

again exited 0 with `#Top`. Sources and logs:
[`verification-wrong-extrema.k`](evidence/mutations/verification-wrong-extrema.k),
[`spec-wrong-extrema-original-shape.k`](evidence/mutations/spec-wrong-extrema-original-shape.k),
[`stage5_wrong_opaque_extrema_build`](evidence/stage5_wrong_opaque_extrema_build/output.log),
and
[`stage5_wrong_opaque_extrema_original_shape`](evidence/stage5_wrong_opaque_extrema_original_shape/output.log).

Assign the permitted fresh interpretation `wrongLo() = 9.0`,
`wrongHi() = 10.0`. For the satisfying input `[1.0, 2.0]`, the proved
structural transform then denotes `[(1-9)/(10-9), (2-9)/(10-9)] =
[-8.0, -7.0]`, while both real Python implementations return `[0.0, 1.0]`.
This is a concrete false-conclusion witness over the intended domain for both
result-bearing extrema bridges and the circular postcondition.

Two earlier exploratory attempts grounded the K Float terms directly and hit
the documented missing Haskell `FLOAT.sub` hook. Those nonzero logs are not
used as verdict evidence; the successful opaque-interpretation probe above
avoids that backend limitation and supplies the symbolic countermodel.

## 6. Fresh non-vacuity test

I created a distinct `SPEC-VACUITY-AUDIT` claim that keeps the original
satisfiable precondition and complete execution but changes the required
returned value to `list(.ValSeq)`. This is false for the satisfying witness
`[1.0, 2.0]`, whose real result has two elements.

The mutation is preserved as
[`spec-vacuity-audit.k`](evidence/mutations/spec-vacuity-audit.k). It first
passed parsing/build with:

```text
kprove --dry-run spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
```

exit 0. The actual proof command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its residual explicitly requires the false equality
`.ValSeq == scaleAcc(...)`; this is the expected unmet result obligation, not
a parser error, missing import, timeout, or unrelated crash. Evidence:
[`stage6_false_mutation_dry_run`](evidence/stage6_false_mutation_dry_run/output.log)
and [`stage6_false_mutation_proof`](evidence/stage6_false_mutation_proof/output.log).

The proof is therefore discriminating with respect to its structural result.
This non-vacuity success does not repair the circular meaning of the extrema
symbols.

## 7. Proven versus assumed accounting

What `#Top` precisely establishes is conditional on the submitted extended K
theory:

> For every K float sequence of length at least two satisfying `allFloats`,
> the exact submitted module and function call reach a normal observed list
> whose structure is `scaleAcc` applied to the input and to the proof-local
> terms `minVF(input)` and `maxVF(input)`.

It does **not** establish that those terms are the sequence's real minimum and
maximum, that the returned endpoints are 0 and 1, or that the proof-local
comprehension summary is universally equivalent to fixed execution.

Trust and assumption ledger:

| Boundary | Effect on theorem | Assessment |
|---|---|---|
| K toolchain/backend and launcher-trusted supplied semantics | Defines all parsing, cells, control, allocation, and fixed operations. | Accepted audit trust boundary; rebuilt from byte-verified source. |
| Trusted translator | Connects `solution.py` to `solution.mpy`. | Accepted here through byte regeneration and constructor-level comparison. |
| Fixed opaque `subF` / `divF` with concrete LLVM twins | Carries every result element structurally; symbolic Haskell does not prove IEEE arithmetic. | Acceptable only for a structural theorem conditional on their documented concrete meaning; finite smoke evidence supports ground behavior. It cannot justify extrema. |
| Proof-local `minVF` / `maxVF` | Determines every output element and the final postcondition. | Illegitimate. They summarize program-defined computation without a connection theorem and admit the wrong-extrema witness above. |
| Proof-local exact-comprehension bridge | Replaces material iteration/control/allocation. | Unvalidated operational bridge; no complete-context connection theorem. |
| `scaleF`, `scaleAcc`, `allFloats`, `#observe` | Defines structural list mapping/domain/observation. | Locally truthful over the target's Float domain. |
| Canonical-versus-candidate differential tests | Supports Python implementation equivalence for 2,013 recorded cases. | Finite empirical evidence only, not part of the K proof. |
| Ordinary mathematical argument that `(x-min)/(max-min)` rescales endpoints | Connects a correct formula to the prose contract on normally returning distinct finite inputs. | Informal and, more importantly, inapplicable until actual extrema are connected; no such K theorem exists. |
| All other fixed-semantics opaque symbols | None are reachable from this target claim. | Enumerated in the inventory and excluded from the theorem dependency set. |

Gate A (real-program proof-extension soundness) fails because of the
result-bearing extrema oracles. Gate B also lacks a formal
summary-to-contract bridge. Gate C's finite differential evidence is
reproducible but cannot substitute for either missing theorem. The successful
clean `#Top`, source pinning, and false-postcondition rejection do not overcome
the false-conclusion counter-interpretation. Under the benchmark decision
boundary, this is a non-legitimate proof, not a merely limited legitimate one.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
