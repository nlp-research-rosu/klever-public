# Independent adversarial review: 111-histogram

Conclusion: the candidate contains a legitimate partial-correctness proof of
the submitted program under the supplied MPY semantics. The proof is
result-constraining, uses the actual regenerated program term, and covers the
material prompt domain. I retain non-fatal concerns because the formal
precondition is broader than the token grammar while the recursive
`histogramResult`-to-English-contract bridge is established by inspection and
finite differential evidence rather than a separate K theorem.

All execution was performed from
`/tmp/audit-work/111-histogram-audit`. Candidate-built `runtime-kompiled/`,
`verification-kompiled/`, caches, logs, `PROOF.md`, and traces were not used as
proof authorities.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `111-histogram`, and condition
`kit-semantics`. This agrees with the rendered audit request. The trusted
`/reference/reference-semantics` mount is present, as required for this mode.

All required pipeline-v3 records were present, regular/readable files (or the
required trace directory), and parsed successfully:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`;
- `codex-last.txt`, `codex-output.log`, `prompt.txt`; and
- the one 645-line JSONL file below `codex-trace/`.

The complete required-path/type check is recorded in
[stage1-integrity-corrected.log](evidence/stage1-integrity-corrected.log).
The first `stage1-integrity.log` is retained but is not evidence: that initial
reviewer script used unsupported `find -printf=...` syntax and expected `jq`,
which is not installed. The corrected script has neither problem.

The campaign block in `/audit-input.json` exactly equals
`/audit-campaign-lock.json`, and the lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value. Sixteen launcher-declared individual-file hashes
were recomputed and matched, including the canonical, trusted/candidate prompt,
trusted/candidate translator, run/task/result records, invocation records, and
generation text/log records. See
[stage1_json_check.py](evidence/stage1_json_check.py) and the corrected
integrity log.

Independent tree/file provenance checks also agree with the records that
created those trees:

- the mounted candidate's pipeline tree hash is
  `6efc5bbf9dba1984bce4ba4acfd3dd2e56cddedf4189d59c6b9971881b4f4dad`,
  exactly the output workspace hash in `/generation-result.json`;
- each supplied-semantics tree has pipeline hash
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  exactly the task-manifest semantics hash;
- the mounted structured-trace tree has pipeline hash
  `aba3bdf6a2a06cd115ccda6e5f2da8e15b15f1efe2df795ede38153acfccf9e8`,
  exactly `usage.json`'s source-trace hash; and
- the JSONL file hash is
  `8841569369d2bea835ddebaff5ff16fbdd9114f529c507afa2bc172f038da28f`,
  exactly the hash in `generation-result.json` and `invocation.json`.

`audit-input.json` additionally records launcher-specific content-tree digests
(`candidate_tree_sha256`, the non-manifest semantics digest, and
`generation_codex_trace_sha256`). The public pipeline hash algorithm is
different from those content digests; the diagnostic comparison is retained in
[stage1-tree-hashes-all.log](evidence/stage1-tree-hashes-all.log). The exact
pipeline/result matches above, individual-file matches, and recursive semantic
comparison independently establish the mounted provenance.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounts. The candidate and trusted `reference-semantics/` trees have identical
entry types, modes, sizes, and bytes under recursive `diff --no-dereference`.
Neither tree contains a symlink; there are no missing, additional, mistyped, or
changed entries. Thus the supplied semantics passes the condition-aware
integrity boundary. `verification.k` remains proof-local and receives no
blessing from that comparison.

The generation records were read only as historical claims. The structured
trace was parsed in full: 645 JSON records, 136 tool/custom calls, and the final
generation claim were summarized by
[summarize_generation_trace.py](evidence/summarize_generation_trace.py) in
[stage1-trace-summary.log](evidence/stage1-trace-summary.log). The generation
reported a successful five-claim proof, but that report was not relied upon.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for `histogram(test)`: for a string representing
space-separated lowercase letters, return a dictionary containing every letter
with the greatest repetition count, mapped to that count; ties are retained and
the empty string returns `{}`.

The trusted canonical splits at ASCII spaces, finds the greatest count among
non-empty tokens, then inserts every token whose count equals that maximum.
The submitted rewrite performs two direct character scans: the first computes
the maximum non-space character frequency; the second inserts all non-space
characters attaining it. For the documented grammar—single lowercase-letter
tokens separated by one space—the algorithms are extensionally equal.

Using the trusted translator copied into scratch:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.mpy solution.regenerated.mpy
```

exited 0. Both MPY files have SHA-256
`cf0986eb563ba48ecf1b5c449262f89f3c676249112360f9e5d9161d6d217f38`.
The exact command is in
[stage2-translation.log](evidence/stage2-translation.log).

The independent differential test
[differential_audit.py](evidence/differential_audit.py) imports the trusted
canonical and submitted function separately. It covers:

- all five documented examples;
- empty, all-space, alphabet-endpoint, strict/false comparison branches,
  unique-maximum, tied-maximum, repeated-update, and spacing cases;
- all raw strings of lengths 0 through 7 over `"abc "`; and
- 1,000 deterministic generated strict-domain strings of up to 80 tokens over
  `a` through `z`.

Across 22,835 unique cases, 1,109 had the strict documented shape and produced
zero canonical/candidate mismatches. Both implementations return `{"a": 1}`
for the satisfiable witness `"a"` and `{"a": 2, "b": 2}` for
`"a b b a"`. Full output is in
[stage2-differential.log](evidence/stage2-differential.log).

The test also deliberately characterized the broader raw-string domain. There
were 21,109 canonical/candidate mismatches outside the strict shape, including:

```text
"ab"   : canonical {"ab": 1}; candidate {"a": 1, "b": 1}
"a  b" : canonical {"a": 1, "": 1, "b": 1}; candidate {"a": 1, "b": 1}
```

These are not counterexamples on the material “space-separated letters”
domain, but they matter because the K precondition admits them. The theorem
soundly describes the submitted program on those extra inputs; it should not be
read as canonical token behavior there. The additional interpretation of
“lowercase” as ASCII `a`–`z` is consistent with the examples and normal
HumanEval domain, but remains an explicit intent assumption.

## 3. Clean proof reconstruction

K v7.1.293, `kompile`, `krun`, and `kprove` were found independently; see
[toolchain.log](evidence/toolchain.log). Scratch received only candidate source
files, the trusted translator/canonical/prompt, and a fresh copy of the trusted
supplied semantics.

### Fresh concrete definition

The LLVM definition was rebuilt from
`reference-semantics/semantics.k` using `MPY-KRUN`/`MPY-SYNTAX`. The build
exited 0; its warnings concern unused or non-exhaustive supplied-semantics
functions outside this program's path. See
[stage3-kompile-llvm.log](evidence/stage3-kompile-llvm.log).

The reviewer concrete program
[concrete_semantics_audit.py](evidence/concrete_semantics_audit.py) embeds the
submitted function AST exactly, as mechanically checked by
[check_concrete_body.py](evidence/check_concrete_body.py). It asserts normal,
boundary, tie, maximum, spacing, and broad-domain cases. Trusted translation,
CPython execution, and fresh `krun` all exited 0. `krun` ended with `.K`,
`NoExc`, exit code 0, empty heap/stack, and the loaded exact closure. Evidence:
[stage3-concrete-body.log](evidence/stage3-concrete-body.log),
[stage3-concrete-translate.log](evidence/stage3-concrete-translate.log), and
[stage3-krun-concrete.log](evidence/stage3-krun-concrete.log).

### Fresh proof definition and positive claims

The Haskell proof definition was rebuilt from `verification.k`; it exited 0.
See [stage3-kompile-haskell.log](evidence/stage3-kompile-haskell.log).

The five claims have an explicit acyclic lemma dependency:

```text
first-count-loop  -> first-loop  \
                                  -> histogram
second-count-loop -> second-loop /
```

The following fresh runs all exited 0 and printed `#Top`:

| Proof obligation(s) | Evidence |
|---|---|
| `SPEC.first-count-loop` alone | [stage3-kprove-first-count.log](evidence/stage3-kprove-first-count.log) |
| `SPEC.second-count-loop` alone | [stage3-kprove-second-count.log](evidence/stage3-kprove-second-count.log) |
| `first-count-loop,first-loop` | [stage3-kprove-first-dependency-set.log](evidence/stage3-kprove-first-dependency-set.log) |
| `second-count-loop,second-loop` | [stage3-kprove-second-dependency-set.log](evidence/stage3-kprove-second-dependency-set.log) |
| all five claims, including `SPEC.histogram` | [stage3-kprove-all.log](evidence/stage3-kprove-all.log) |

Selecting either outer claim alone exits 1 because `--claims` removes its
inner-loop lemma; the residual is precisely the unmet count-to-fold
relationship. Those diagnostic failures are preserved in
[stage3-kprove-first-loop.log](evidence/stage3-kprove-first-loop.log) and
[stage3-kprove-second-loop-isolated.log](evidence/stage3-kprove-second-loop-isolated.log).
They do not refute the dependency-closed claims. The generation's own script
likewise proved the inner claims separately and then all claims together.

An exploratory selection of `SPEC.histogram` alone was manually stopped after
60 seconds without a result and is not used as evidence. No timeout is
converted into a candidate verdict. The dependency-closed all-claim run is the
successful target-proof run.

The clean reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Plain-language claims

- `first-count-loop`: with `letter` a singleton target string and `count = N`,
  executing the exact inner loop over suffix `REM` leaves
  `count = countHistogramCode(REM, TARGET, N)`. It preserves the first-phase
  result, maximum, control cells, heap, scope allocation, return/exception, and
  exit state.
- `second-count-loop`: the same exact count result in phase 2 while preserving
  the current dictionary and maximum.
- `first-loop`: executing the exact first outer loop over `REM`, where every
  inner loop scans the original `test = ORIG`, leaves
  `max_count = maxHistogramCount(REM, ORIG, M)`.
- `second-loop`: executing the exact second outer loop leaves `result` equal to
  `buildHistogram(REM, ORIG, M, KS, VS)`.
- `histogram`: for any `CS` satisfying `validHistogramInput`, start from the
  complete fresh module configuration, load the literal function, resolve its
  binding, call it on `str(CS)`, execute every source statement, return, and
  frame pop, and reach `histogramResult(CS)` with the loaded closure and all
  other initial machine state restored.

The helper preconditions are satisfiable, for example with `L = 1`, framed
outer scope `S = .Map`, no heap/stack/exception, and empty `REM`; their exact
scope maps then satisfy `notBool L in_keys(S)`. The entry precondition is
satisfied by `CS = iCons(97, .IntSeq)` (`"a"`). Ground K claims for that
predicate, the empty summary, and the `"a"` summary each printed `#Top` and
exited 0:
[stage4-ground-valid.log](evidence/stage4-ground-valid.log),
[stage4-ground-result-empty.log](evidence/stage4-ground-result-empty.log), and
[stage4-ground-result-a.log](evidence/stage4-ground-result-a.log).
The `"a"` summary is exactly the dictionary key `"a"` with value 1, agreeing
with both Python implementations.

### Mechanical program identity

[extract_claim_program.py](evidence/extract_claim_program.py) extracts the
balanced `Module(...)` term inside `SPEC.histogram`. It performs only surface
normalization of one explicit `.Entries` unit and eleven explicit `.Stmts`
units. `kast` then parsed both regenerated `solution.mpy` and the extracted
claim program with the fresh definition. Their JSON KAST files were byte
identical and shared SHA-256
`90c2be895d4c6d55f055f208b75ea0fe659ed486a7785781bfd7b84080b8bd85`.
See
[stage4-program-pinning-corrected.log](evidence/stage4-program-pinning-corrected.log).
This establishes constructor-level identity; the claim does not execute a
substituted function.

The postcondition is equality to `histogramResult(CS)`, not a free result, an
implication, or a tautology. The scope postcondition also fixes the loaded
closure to the same body.

### Body sensitivity

The fresh mutation
[audit-body-sensitivity.k](evidence/audit-body-sensitivity.k) changes the
second-pass comparison from `==` to `!=` in both occurrences of the function
body actually embedded in the main claim (load term and post-state closure),
grounds the call at `"a"`, and retains the correct `histogramResult("a")`
obligation. Its dry run builds successfully. The proof then exits 1 with
`WarnStuckClaimState`; fixed execution returns the empty dictionary while the
required summary is `{"a": 1}`. See
[stage4-body-mutation-dry-run.log](evidence/stage4-body-mutation-dry-run.log)
and
[stage4-body-mutation-proof.log](evidence/stage4-body-mutation-proof.log).
This changes the term actually executed by the theorem, not merely an external
source file.

The theorem therefore pins and is sensitive to the real submitted body.

## 5. Rule-by-rule static soundness review

[k_rule_inventory.py](evidence/k_rule_inventory.py) inventories every local K
sentence in the assembled supplied semantics, all helper K files,
`verification.k`, and `spec.k`. The exact 1,301-line inventory is in
[stage5-rule-inventory-with-counts.log](evidence/stage5-rule-inventory-with-counts.log):

- 26 K files;
- 232 syntax declarations;
- one configuration;
- 704 ordinary/functional/operational rules;
- five contexts;
- five claims; and
- 291 lines carrying `function`, `functional`, `total`, `no-evaluators`,
  `simplification`, `priority`, `owise`, `concrete`, macro, or strictness
  attributes.

There are no additional generated proof-helper K files. The complete
constructor-to-rule mapping and proof-local classification is preserved in
[USED-CONSTRUCT-MAP.md](evidence/USED-CONSTRUCT-MAP.md).

### Proof-local rules

`verification.k` contains five syntax/function declarations and nine equations:

| Function | Static decision |
|---|---|
| `countHistogramCode` | Sound total definition. Empty/cons guards are disjoint and exhaustive; the cons rule adds exactly one iff the head equals the target and strictly consumes the sequence. |
| `validHistogramInput` | Sound total domain predicate. Empty/cons coverage is disjoint/exhaustive and recursion consumes one code. |
| `maxHistogramCount` | Sound total fold. It skips code 32 and otherwise performs the source's exact strict-greater update with the exact inner-count summary. Every branch consumes one remaining code. |
| `buildHistogram` | Sound total fold. It skips code 32 and otherwise invokes the same supplied `dPutK`/`dPutV` helpers as fixed dictionary assignment iff the exact count equals `M`. Empty/cons coverage is complete and descending. |
| `histogramResult` | Sound unconditional composition starting the first fold at 0 and the dictionary at parallel empty sequences. |

There are no proof-local `functional`/simplification/priority/`owise`/concrete
rules, opaque symbols, fresh oracles, operational bridges, call interceptions,
or rules rewriting any source construct. No equation overlaps inconsistently,
and every `[total]` annotation has constructor coverage and strict descent.

### Fixed semantics on the theorem path

The used declarations/rules were checked in full in
[stage5-used-semantics.log](evidence/stage5-used-semantics.log) and
[stage5-used-semantics-detail.log](evidence/stage5-used-semantics-detail.log):

- configuration/module loading and sequencing:
  `core.k:49-60,124-127`;
- closure binding, lookup, left-to-right argument evaluation, frame
  allocation/binding, return and pop:
  `core.k:130-191`, `functions.k:14-16,63-90`,
  `call.k:18-21,69-75`;
- assignment and `If`: `controls.k:8-18,50-54`;
- `For` control and iteration: `controls.k:62-75`, `iter.k:8`,
  `str.k:8-10`, and name target binding at `tuple.k:30-41`;
- operator evaluation and used string/integer cases:
  `operators.k:10-17`, `str.k:24-26`, `int.k:9,22-27`;
- empty dictionary, subscript assignment, ordered insert/update, and sequence
  append:
  `dict.k:19-54,68-85` and `list.k:18-20`; and
- literal/truth evaluation: `core.k:193-205`, `str.k:12-17`.

These rules preserve the relevant binding, strict/left-to-right evaluation,
state updates, allocation (none on this path), control, return, exception, and
stack behavior. The priority alternatives for cells, heap references, methods,
and dictionary reads have guards or term shapes that do not match the plain
local strings/integers/dictionary used here. The source contains no exceptional
operation on the formal domain.

The four loop claims are derived reachability lemmas, not semantic rewrites.
They match the exact `#loop`, target, body, phase-specific local map, and every
machine cell. Their arbitrary continuation framing is sound here: none of the
loop bodies contains return, break, continue, exception, allocation, or output.
Every result-bearing local subsequently observed by a caller is constrained.
Existential final values are only temporary `letter`/`candidate`/`count`
values that are overwritten or not observed before the result/return.

### Remaining supplied rules and opaque symbols

Every remaining inventoried supplied rule has a left-hand-side construct absent
from the submitted body, summary functions, helper conditions, and entry
postcondition. Thus those rules cannot contribute a task answer or bypass this
execution. This includes assertions/builtins/comprehensions/floats/methods/range/
set/sort/slicing and unused list/tuple cases. The LLVM reviewer's assertions
exercise `assert.k` only as concrete tests, not in the proof theorem.

The supplied semantics' explicit opaque/no-evaluator symbols are:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`.
None occurs in any target claim or reachable execution term. Likewise,
known total-but-underspecified supplied operations such as out-of-bounds
`valSeqAt` are theorem-inert.

No candidate or used fixed-semantics rule was found unsound, so there is no
unsoundness allegation requiring a false-conclusion witness. The broad formal
input behavior is a specification/intent issue, not a false K conclusion.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not used. The reviewer-generated
[audit-spec-vacuity.k](evidence/audit-spec-vacuity.k), created by
[make_fresh_vacuity_mutation.py](evidence/make_fresh_vacuity_mutation.py),
retains the four auxiliary loop claims and the exact whole-program load/call/
return claim, grounds the satisfying input at `"a"`, and changes only the final
result obligation from the correct `{"a": 1}` to the false `{"a": 2}`.

`kprove --dry-run` exited 0, demonstrating that the mutated artifact parses and
builds; see
[stage6-mutation-dry-run.log](evidence/stage6-mutation-dry-run.log).
The actual proof exited 1 with `WarnStuckClaimState`. Its terminal `<k>` cell
contains:

```text
dictV(vCons(str(iCons(97, .IntSeq)), .ValSeq),
      vCons(1, .ValSeq))
```

which cannot unify with the required value 2. The stack is empty, return/
exception are reset, exit code is 0, and the exact loaded closure remains,
showing that failure occurs at the intended final result obligation after real
execution—not at parsing, import, timeout, or an unrelated crash. See
[stage6-mutation-proof.log](evidence/stage6-mutation-proof.log).

The proof is non-vacuous and discriminating.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY theory, for every finite `IntSeq` containing only code 32
or codes 97 through 122, if execution of the submitted `histogram` function
terminates from the claim's fresh module state, its returned K value is exactly:

1. the ordered dictionary produced by scanning all non-space codes;
2. retaining precisely those codes whose whole-input frequency equals the
   maximum frequency found by the first scan; and
3. mapping each retained singleton string to that frequency.

The empty/all-space modeled input returns the empty dictionary. This is partial
correctness; termination and resource complexity are not themselves the stated
reachability theorem.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Byte-identical supplied MPY semantics | All claims: syntax, values, control, state, calls, dictionaries | Acceptable fixed semantics for `SUPPLIED_SEMANTICS`. It is intentionally not full CPython. Used rules were statically reviewed and concretely exercised. |
| Trusted `py2mpy.py` | Source-to-MPY and constructor pinning | Acceptable trusted input. Regeneration is byte-identical and independent KAST comparison pins the claim body. |
| K v7.1.293, Haskell backend, SMT, LLVM backend | Machine checking and concrete runs | Standard unavoidable toolchain trust. LLVM evidence is testing only; Haskell `#Top` is the formal proof gate. |
| K unbounded `Int` and `IntSeq` string model | Counts, comparisons, character iteration | Acceptable for the specified lowercase-letter task; it differs from full CPython Unicode/resource behavior. |
| ASCII `a`–`z` interpretation of “lowercase letters” | Entry-domain adequacy | Non-fatal intent assumption. It matches examples and standard HumanEval use, but the prompt does not spell out Unicode. |
| Strict single-letter token grammar | Canonical/rewrite equivalence | Material prompt domain is covered with zero mismatches. The K precondition is broader and the rewrite intentionally differs from canonical token behavior outside that grammar. |
| Recursive summary means “all maximum-frequency letters” | Natural-language interpretation of `histogramResult` | Equations make the bridge transparent and structural; independent testing supports it, but there is no separate K theorem phrased as a set/max characterization. This is the principal non-fatal concern. |
| Finite differential/concrete evidence | Program/intent and implementation/model bridges only | 22,835 Python cases plus fresh MPY concrete cases; not treated as universal proof. |
| Supplied opaque primitives | None | They are imported but absent from every proof dependency and result. |

Gate A (real-program soundness) passes: the actual body executes, summaries are
truthful total definitions, the program term is pinned and body-sensitive, and
the fresh false postcondition is rejected. Gate B (material intent adequacy)
passes for space-separated single ASCII lowercase-letter tokens, including the
unrestricted finite length domain; there is no finite-size restriction. Gate C
(auditability) passes: source, commands, statuses, mutations, inventories, and
logs are preserved.

This is not `FAIL / NOT_LEGIT`: there is no missing/failed dependency-closed
proof, substituted program, vacuity, result oracle, unsound used rule, or
material finite/bounded restriction. I select `CONCERNS / LEGIT` rather than
`PASS / LEGIT` because the theorem admits malformed token strings on which the
rewrite and trusted canonical differ, and because the summary-to-English
property bridge remains an inspected definition plus finite evidence rather
than a separately stated mathematical K theorem. Neither concern permits a
false conclusion about the submitted program under the stated K precondition.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
