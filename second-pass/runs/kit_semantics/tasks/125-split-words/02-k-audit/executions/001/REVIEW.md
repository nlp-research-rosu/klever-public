# Independent adversarial audit: 125-split-words

The candidate contains a sound, result-constraining partial-correctness proof
of the submitted program under the supplied K semantics. The proof was rebuilt
without candidate caches, all four positive claims independently closed, the
claim body is constructor-identical to trusted regeneration of the submitted
program, and fresh false-result and body mutations were rejected for the
expected reasons.

The qualification is a documented supplied-model behavior gap:
`isWSC` recognizes only tab, newline, carriage return, and space, whereas
CPython `str.split()` recognizes additional Unicode whitespace. The theorem
covers every input of the fixed model, the candidate explicitly records the
gap and a vertical-tab witness, and the submitted Python behaves correctly on
that witness. Campaign amendment v2 therefore maps this case to
`CONCERNS / LEGIT`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and the expected
`125-split-words`/`kit-semantics` task. The trusted
`/reference/reference-semantics` tree is present, so the rendered mode and
mounts do not conflict.

All required pipeline-v3 records are present, readable regular files:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured trace. Every declared individual file hash
recomputed from the mount matches `/audit-input.json`. The audit-campaign block
is exactly equal to `/audit-campaign-lock.json`, whose SHA-256 also matches the
recorded value.

The structured trace consists of one valid JSONL file with 218 records from
one session; the complete trace and 763,349-byte textual log were read and
summarized, without treating their reported `#Top` or `VALIDATED` claims as
proof evidence. See
[stage1_trace_summary.log](/audit-output/evidence/stage1_trace_summary.log).

The candidate and trusted prompt hashes match, as do the candidate and trusted
translator hashes. Recursive entry-type and content comparison of
`/candidate/reference-semantics` against
`/reference/reference-semantics` found 25 entries on each side, with no
missing, additional, changed, mistyped, or symlinked entry. There are no
symlinks or special file types in the candidate, reference, or generation
evidence trees. Independent source hashes and deterministic tree-manifest
digests are in
[stage1_independent_tree_hashes.log](/audit-output/evidence/stage1_independent_tree_hashes.log);
the full declared-hash and recursive-comparison results are in
[stage1_integrity.log](/audit-output/evidence/stage1_integrity.log).

No audit infrastructure breach was found. Candidate-built `*-kompiled`
directories and `__pycache__` entries were ignored.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted docstring requires:

1. if the input string contains whitespace, return words split on whitespace;
2. otherwise, if it contains a comma, return words split on commas;
3. otherwise, return the count of lowercase English letters at odd zero-based
   alphabet positions, namely `b,d,f,h,j,l,n,p,r,t,v,x,z`.

The submitted [solution.py](/candidate/solution.py) implements exactly that
precedence. `txt.split()` detects CPython whitespace; `txt and parts != [txt]`
detects whether that split changed a nonempty string; the second branch uses
`txt.split(",")`; and the final expression sums the thirteen singleton
counts. Empty input returns zero.

Trusted regeneration used:

```text
python3 /reference/py2mpy.py /tmp/audit-work/125-split-words/solution.py \
  > /tmp/audit-work/125-split-words/solution.regenerated.mpy
```

It exited 0. `cmp -s` against the submitted `solution.mpy` exited 0; both files
have SHA-256
`9ff948f61b7b9af0a06011f43d344b544d013e8f8c31fda72f15fc2e7727c944`.

The independent differential uses a separate docstring oracle and deterministic
inputs: all strings of lengths 0 through 4 over a 12-character alphabet plus
5,000 seeded strings of lengths 0 through 30 and explicit documented,
whitespace, comma, Unicode, empty, and repeated-delimiter boundaries. Results:

```text
total_unique_cases=27252
branch_counts={'whitespace': 22384, 'comma': 1911, 'count': 2957}
documented_failures=0
candidate_oracle_mismatches=0
candidate_canonical_mismatches=14895
```

The canonical mismatches are not candidate defects. The canonical checks only
literal space before its whitespace split, while the docstring says
“whitespace”; the candidate follows the docstring for tabs and Unicode
whitespace. On repeated, leading, or trailing commas, direct `str.split(",")`
keeps empty fields while canonical replacement-plus-whitespace-split drops
them. The docstring does not specify empty-field handling, and direct
separator splitting is a defensible reading. The script and complete bounded
output are
[stage2_differential.py](/audit-output/evidence/stage2_differential.py) and
[stage2_fidelity_and_differential.log](/audit-output/evidence/stage2_fidelity_and_differential.log).

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/125-split-words`; the semantics came from the trusted
`/reference` mount. K v7.1.293 was used.

The concrete definition was freshly built with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition auditor-runtime-kompiled
```

It exited 0. `krun solution.mpy --definition auditor-runtime-kompiled`
exited 0 and installed the exact function closure. An independently authored
smoke module exercised whitespace, comma, repeated-comma, count, empty, and
model-boundary paths; it exited 0 at `.K`, with `NoExc` and exit code 0.
Build and run records are
[stage3_concrete_build.log](/audit-output/evidence/stage3_concrete_build.log)
and
[stage3_concrete_runs.log](/audit-output/evidence/stage3_concrete_runs.log).

The proof definition was freshly built with:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition auditor-verification-kompiled
```

It exited 0. Each positive target was then selected and run separately:

| Claim | Exit | Result | Evidence |
|---|---:|---|---|
| `SPEC.split-words-empty` | 0 | `#Top` | [log](/audit-output/evidence/stage3_prove_empty.log) |
| `SPEC.split-words-whitespace` | 0 | `#Top` | [log](/audit-output/evidence/stage3_prove_whitespace.log) |
| `SPEC.split-words-comma` | 0 | `#Top` | [log](/audit-output/evidence/stage3_prove_comma.log) |
| `SPEC.split-words-count` | 0 | `#Top` | [log](/audit-output/evidence/stage3_prove_count.log) |

The clean Haskell build record is
[stage3_proof_build.log](/audit-output/evidence/stage3_proof_build.log).
No candidate-provided compiled definition, cache, proof log, or prior `#Top`
was reused.

## 4. Adequacy and real-program pinning

The four entry claims mean:

- Empty: input `str(.IntSeq)` returns integer `0`; the no-argument split
  allocates exactly one empty list.
- Whitespace: for nonempty `CS` where `splitWS(CS)` differs from `[str(CS)]`,
  return reference 0 and constrain it to exactly `list(splitWS(CS))`; reference
  1 is the temporary singleton list.
- Comma: for nonempty `CS` where `splitWS(CS) = [str(CS)]` and comma occurs,
  return reference 2 and constrain it to exactly `list(splitSep(CS,44))`;
  references 0 and 1 are the prior split and singleton lists.
- Count: for nonempty `CS` where `splitWS(CS) = [str(CS)]` and comma does not
  occur, return the sum of the thirteen required singleton counts; references
  0 and 1 are exactly constrained.

The empty/nonempty split, equality/disequality split, and comma/non-comma split
partition every finite `IntSeq`; no length bound or example-only condition is
present. Concrete satisfying witnesses are respectively `""`,
`"Hello world!"`, `"Hello,world!"`, and `"abcdef"`. Substitution yields
`0`, `["Hello","world!"]`, `["Hello","world!"]`, and `3`, agreeing with both
Python implementations. See
[stage4_ground_witnesses.py](/audit-output/evidence/stage4_ground_witnesses.py).

The claims start from the post-module-load closure rather than the whole
`Module` term. This is pinned mechanically:

- trusted regeneration proves the submitted `solution.mpy` is current;
- parsing the regenerated `FuncDef` body and the `splitWordsBody` rule RHS
  produced identical KAST hashes
  `8b6ac68c741f987d9cc2708d30bd13cc4351c409a9cc69ef4c7f132b956f8e2f`;
- the parameter is exactly `"txt"` and the module contains no other statement;
- fixed `FuncDef` execution at environment 0 installs exactly
  `closureVal(("txt",.ParamNames), BODY,0)`, the binding in every claim;
- fresh `krun` of the actual module independently produced that binding.

The successful comparison is in
[stage4_pinning_and_witnesses.log](/audit-output/evidence/stage4_pinning_and_witnesses.log).
Two earlier standalone-program-parser attempts rejected rule-only spellings of
`.Exprs`/`.Stmts`; those parser-format attempts are preserved as
`stage4_pinning_attempt1.log` and `stage4_pinning_attempt2.log`. The final
comparison used K's rule parser and succeeded; the preliminary parser errors
are not proof results.

The return values are not free: list claims constrain both the returned
reference and exact heap content; the count claims constrain the integer
directly. Heap allocation counters, scopes, environment, stack, return state,
and exception state are also constrained. A fresh body-sensitivity definition
replaced the executed closure body by `Return(Int(0))`; its dry run exited 0
and its proof exited 1 with `WarnStuckClaimState` and residual `<k> 0 ~> .K
</k>` against required `3`. See
[stage4_body_sensitivity.log](/audit-output/evidence/stage4_body_sensitivity.log).

## 5. Rule-by-rule static soundness review

The exhaustive inventory reads all 2,664 lines of the supplied semantics,
`verification.k`, and `spec.k`, and enumerates 1,022 sentences:
246 syntax declarations, 766 rules, five contexts, one configuration, and four
claims. It records 163 `function`, 115 `total`, 48 priority, 28 `owise`, 60
`concrete`, 24 `no-evaluators`, four macro, and one recursive-macro
attributes. There are no explicit `functional` or `simplification`
declarations. The complete sentence-by-sentence inventory is
[stage5_rule_inventory.md](/audit-output/evidence/stage5_rule_inventory.md).

The candidate contributes only:

1. `splitWordsBody`, a nullary `[function,total]` AST abbreviation with one
   unconditional equation;
2. `oddAlphabetCount(IntSeq)`, a `[function,total]` mathematical abbreviation
   with one unconditional equation.

There are no proof-local operational bridges, priorities, simplifications,
opaque symbols, concrete rules, or helper claims. `splitWordsBody` expands
before fixed execution and is constructor-identical to the regenerated body.
`oddAlphabetCount` occurs only in the postcondition; execution independently
reaches the same thirteen fixed-semantics `cntSub` terms. It therefore does not
smuggle the answer or replace a property-bearing computation.

The active fixed-semantics slice was checked for configuration shape,
left-to-right evaluation, call binding, frame creation and popping, short
circuiting, branch selection, allocation, heap dereference, list structural
comparison, string membership, both split modes, count recursion, addition,
return, and exception state. Recursive helper cases descend; paired guards are
disjoint; active priorities preempt only the appropriate generic dispatcher
and preserve the full modeled state transition. Every material operation in
the submitted body executes.

All supplied opaque float, sort, digest, concrete-only, and unrelated
collection/builtin rules have heads disjoint from the reachable terms and do
not occur in any claim or postcondition. No active false or overlapping
equation, fabricated result, unconstrained oracle, answer-specific execution
shortcut, or control mismatch was found. Accordingly, this review makes no
unsound-rule allegation requiring a false-conclusion witness. The detailed
constructor map and reasoning are in
[stage5_static_assessment.md](/audit-output/evidence/stage5_static_assessment.md).

One fixed rule is intentionally narrower than CPython:
`reference-semantics/semantics/methods.k:85-86` defines whitespace as codes
9, 10, 13, and 32. For vertical tab 11, the model returns integer `0`, while
the submitted Python correctly returns `[]`. This is the supplied-model gap
governing the qualified verdict, not a proof-local unsoundness or candidate
domain restriction.

## 6. Fresh non-vacuity test

The auditor-authored
[auditor-vacuity.k](/audit-output/evidence/auditor-vacuity.k) keeps the real
closure and all exact post-state cells but changes the ground result for
`"abcdef"` from `3` to `4`.

```text
kprove auditor-vacuity.k \
  --definition auditor-verification-kompiled \
  --spec-module AUDITOR-VACUITY --dry-run
```

exited 0, establishing that the mutation parsed and built. The same command
without `--dry-run` exited 1 and emitted `WarnStuckClaimState`; the residual
was `<k> 3 ~> .K </k>` while the destination required 4. This is the expected
unmet result obligation, not a parser error, timeout, or unrelated failure.
The corrected complete record is
[stage6_false_mutation.log](/audit-output/evidence/stage6_false_mutation.log).
The first proof run already had the same correct stuck residual, but its
reviewer-side single-line residual regex failed on multiline output; that
wrapper attempt is preserved in `stage6_false_mutation_attempt1.log`.

## 7. Proven versus assumed accounting

What the proof establishes is precise: for every finite `CS:IntSeq`, if
execution terminates under the supplied `MPY` semantics from the corresponding
claim precondition, the actual translated `split_words` closure returns the
branch result described in Stage 4 and reaches the constrained heap, allocator,
scope, stack, return, and exception state. This is unbounded partial
correctness, not finite unrolling and not a termination theorem.

| Boundary | Status and influence |
|---|---|
| Supplied `reference-semantics` | Trusted fixed operational model for value, control, allocation, state, and exceptions. Recursively integrity-checked and its active rules statically reviewed. Its narrower whitespace classification is the material documented concern. |
| K v7.1.293 backend/toolchain | Trusted checker and runtime. Fresh LLVM/Haskell builds, four positive proofs, and two discriminating negative probes provide reproducible checker evidence. |
| Trusted `py2mpy.py` | Trusted source-to-constructor bridge. Regeneration is byte-identical, and the exact function body is independently KAST-equal to the claim body. |
| Module-load normalization | Mechanically justified by the fixed `FuncDef` rule, exact parameter/body comparison, and concrete execution of the actual module. It introduces no assumed result. |
| `splitWordsBody` | Transparent proof-local syntax definition; no execution is skipped. |
| `oddAlphabetCount` | Transparent postcondition definition; the mathematical identification of codes 98,100,...,122 with odd-index lowercase ASCII letters is ordinary arithmetic. |
| Docstring oracle and differential | Independent finite evidence over 27,252 cases. It supports implementation intent only and is not used in claim closure. |
| CPython behavior | Used only to judge source-contract fidelity and expose the supplied-model gap. It is not a K axiom. |
| Termination | Not proved. Reachability establishes partial correctness, as requested. |

The documented supplied-model exception applies in full:

1. the whitespace divergence originates in the immutable supplied semantics;
2. the four claims cover every input that fixed model represents, with no
   candidate-added bound or restriction;
3. the candidate trust ledger explicitly records the boundary and vertical-tab
   divergence witness;
4. the submitted Python uses CPython `str.split()` and returns `[]` on that
   witness, so the divergence is model-versus-CPython, not
   program-versus-contract.

Gate A (real-program soundness and non-vacuity) passes. Intent adequacy covers
the complete fixed-model domain and the permitted supplied-model exception,
with no candidate narrowing. Gate C evidence is reproducible. The model gap
prevents an unqualified `PASS` under the campaign's explicit mapping but does
not invalidate the proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
