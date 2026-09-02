# Independent adversarial audit: 28-concatenate

The candidate contains a legitimate partial-correctness proof of the generated
program over the full source-contract domain `List[str]`. This conclusion is
based on a fresh source reconstruction, not on the candidate's compiled
definitions, `PROOF.md`, generation report, or prior `#Top`.

## 1. Input and provenance integrity

The launcher record declares `record_layout = pipeline-v3`,
`condition = kit-semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mounts agree with
the rendered mode. There is no infrastructure contradiction.

I read `/audit-input.json` first and checked its `record_layout`,
`container_paths`, hashes, integrity fields, and campaign block. I then checked
the mounted paths, not the host provenance paths. The independent checker and
full results are
[`evidence/check_provenance.py`](evidence/check_provenance.py) and
[`evidence/stage1-provenance.log`](evidence/stage1-provenance.log).
In particular:

- `/audit-campaign-lock.json` is a regular file, its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed JSON is exactly the `audit_campaign` block in
  `/audit-input.json`.
- Every required `pipeline-v3` record is a regular file:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`. Every direct recorded
  file hash matches.
- The structured trace is one regular JSONL file. All 340 events parse; the
  checker read the full trace and the full 858,139-byte output log. A bounded
  event-by-event command/patch/final-claim summary is in
  [`evidence/stage1-generation-trace-summary.log`](evidence/stage1-generation-trace-summary.log).
  The generation records claim a successful proof, but no later audit result
  relies on that claim.
- The pipeline-v3 length-delimited tree hashes independently recompute to
  `898ef000…579f29` for `/candidate`,
  `4e06397a…3789f` for each semantics tree, and
  `49a4dd59…326de6` for the trace. These match the mounted pipeline records.
- The candidate and trusted prompts are byte-identical; the candidate and
  trusted translators are byte-identical.
- Recursive, no-dereference comparison of
  `/candidate/reference-semantics` and
  `/reference/reference-semantics` finds exactly one real directory and 24
  regular files on each side, with identical relative names and bytes. There
  are no missing, additional, mistyped, or symlinked semantics entries.
- All six required candidate proof artifacts (`solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`) are regular,
  non-symlink files. Candidate-built `runtime-kompiled` and
  `verification-kompiled` were not used.

Stage 1 result: PASS. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for every list of strings, return one string
formed by concatenating all members in list order, with no separator. The
documented boundaries are `concatenate([]) == ""` and
`concatenate(["a","b","c"]) == "abc"`. The trusted canonical body is
`return ''.join(strings)`.

The submitted program initializes `result = ""`, initializes the loop target
`string = ""`, appends each list member to `result` in a `for` loop, and
returns `result`. The extra loop-target initialization is result-inert and also
defines the local on the zero-iteration path. This is a different but faithful
algorithm for the entire typed domain; it is not a fixed-size implementation.

In the scratch tree I ran the trusted `/reference/py2mpy.py` on the copied
`solution.py`. `cmp` succeeds and both submitted and regenerated constructor
files have SHA-256
`76f72a295e084927590a18af5a031a11a16dad65c5673d5fd10d1d29ce127456`.
Commands and statuses are in
[`evidence/stage2-regeneration.log`](evidence/stage2-regeneration.log) and
[`evidence/stage2-regeneration-hashes.log`](evidence/stage2-regeneration-hashes.log).

The reviewer-authored differential test imports both trusted canonical and
submitted entry points. It checks ten fixed cases covering the prompt examples,
zero/one/many iterations, empty elements, whitespace, NUL, combining
characters, non-ASCII and astral Unicode, and long strings. It then checks
1,000 deterministic generated lists (lengths 0 through 12; member lengths 0
through 20). All 1,010 return values and types match. The exact input list,
seed, input digest, and results are preserved in
[`evidence/stage2-differential-inputs-results.json`](evidence/stage2-differential-inputs-results.json);
the script and bounded log are
[`evidence/differential_test.py`](evidence/differential_test.py) and
[`evidence/stage2-differential.log`](evidence/stage2-differential.log).

Stage 2 result: PASS.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/reconstruction`. The
candidate's compiled definitions, Python cache, and proof logs were absent from
that build tree.

The installed tools independently report K `v7.1.293`. Fresh reconstruction
produced:

| Check | Exact operation | Result |
|---|---|---|
| Concrete definition | `kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled` | Exit 0; [`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log) |
| Concrete execution | `krun concrete_execution.mpy --definition runtime-audit-kompiled` | Exit 0, `.K`; `""`, `""`, `"q"`, `"abc"`, `"xyz"` exactly present; [`stage3-krun.log`](evidence/stage3-krun.log) |
| Proof definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-audit-kompiled` | Exit 0; [`stage3-kompile-proof.log`](evidence/stage3-kompile-proof.log) |
| All positive claims | `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC` | `#Top`, exit 0; [`stage3-kprove-all.log`](evidence/stage3-kprove-all.log) |
| Empty-loop lemma | same proof with `--claims SPEC.concat-loop-empty` | `#Top`, exit 0; [`stage3-kprove-loop-empty.log`](evidence/stage3-kprove-loop-empty.log) |
| Step lemma | same proof with `--claims SPEC.concat-loop-step` | `#Top`, exit 0; [`stage3-kprove-loop-step.log`](evidence/stage3-kprove-loop-step.log) |
| Entry after independently proved helpers | same proof with `--trusted SPEC.concat-loop-empty,SPEC.concat-loop-step` | `#Top`, exit 0; [`stage3-kprove-concatenate-with-proved-helpers.log`](evidence/stage3-kprove-concatenate-with-proved-helpers.log) |

The final command is a compositional check: the two loop claims were first
proved independently, then used as lemmas while only the entry remained to
prove. The aggregate command independently proves the complete claim set.

For transparency, filtering to `SPEC.concatenate` alone removes both helper
claims from the spec and causes ordinary unbounded loop unrolling. I interrupted
that diagnostic after about 90 seconds; it is recorded as exit 130 in
[`stage3-kprove-concatenate.log`](evidence/stage3-kprove-concatenate.log).
It is not the candidate's target proof command and is not treated as proof
failure or infrastructure uncertainty.

The LLVM compiler reports non-exhaustiveness warnings for several
launcher-supplied total functions (`mapStrVS`, float helpers, `joinCodes`, and
`valSeqAt`). None is reachable from this program or its proof. The proof build
has only unused-variable warnings in supplied `strLt`; no warning affects a
positive claim.

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Claims in plain language

`concat-loop-empty` says: in the exact local frame, an empty remaining list
performs no iteration; `result`, `string`, `strings`, globals, the continuation,
and every omitted cell remain unchanged.

`concat-loop-step` says: for a nonempty remaining list whose head and tail are
strings, fixed semantics executes the exact target binding and
`result += string` body until the loop finishes. It leaves `result` equal to
the old accumulator followed by every remaining string, leaves the loop target
equal to the last visited string, and preserves the original `strings` binding,
globals, continuation, and framed cells.

`concatenate` says: from the exact initial MPY configuration, load the submitted
module, bind and call its `concatenate` closure on any finite semantic list of
strings, and return
`str(concatFrom(.IntSeq, VS))`. It additionally restores `env`, `scopeLoc`,
empty heap and heap counter, stack, return state, exception state, and exit
code. Only the final module-scope map is existential, appropriately allowing
the loaded function binding. The returned value is not free, tautological, or
guarded by a one-way implication.

### Mechanical program identity

The reviewer script extracts the balanced argument of the entry claim's
`#loadAll`, removes only whitespace outside string tokens, and compares it with
the trusted regenerated `solution.mpy`. Both constructor streams have SHA-256
`3455b021…67c8bc` and are identical. The check is in
[`evidence/check_program_pinning.py`](evidence/check_program_pinning.py) with
result in
[`evidence/stage4-program-pinning.log`](evidence/stage4-program-pinning.log).
It includes every material `ImportFrom`, binding, assignment, `For`,
`AugAssign`, lookup, call, and return constructor. No external source file is
being mistaken for the term executed by the theorem.

### Satisfiable states and substitutions

The reviewer ground spec gives concrete states for both loop preconditions:

- empty loop: accumulator `"ab"`, prior target `"z"`, empty remaining list;
- step loop: accumulator `"ab"`, prior target `"z"`, remaining `["c"]`.

It also executes the exact full module/call on `[]`, `["q"]`, and
`["", "ab", "c"]`. All five ground claims print `#Top` and exit 0 in
[`evidence/stage4-ground-kprove.log`](evidence/stage4-ground-kprove.log).
The corresponding instantiated K code sequences are `[]`, `[113]`, and
`[97,98,99]`; both trusted and submitted Python return `""`, `"q"`, and
`"abc"`. See
[`evidence/stage4-python-witness-comparison.log`](evidence/stage4-python-witness-comparison.log).

The formal precondition `isStringSeq(VS)` covers both ValSeq constructors
recursively and imposes no length or character bound. It is exactly the
`List[str]` source domain. The proof is not a finite unrolling. Symbolic input
strings may contain arbitrary `IntSeq` contents; that is over-broad relative
to valid Unicode scalar sequences, not a narrowing of Python strings, and
concatenation is sequence append on the intended subset.

A fresh body-sensitivity spec changes the program term itself to append literal
`"x"` on input `["a"]` while retaining the old expected `"a"`. Fixed execution
reaches `str(iCons(120,.IntSeq))` and the proof fails with
`WarnStuckClaimState`, exit 1. See
[`evidence/spec-fresh-body-sensitivity.k`](evidence/spec-fresh-body-sensitivity.k)
and [`evidence/stage5-body-sensitivity.log`](evidence/stage5-body-sensitivity.log).
This is sensitivity to the executed theorem body, not merely to an external
source file.

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers the assembled supplied `semantics.k`, all 23
helper K files, `verification.k`, and `spec.k`. It contains 1,111 records:
231 syntax declarations, 704 rules, 5 contexts, 1 configuration, 3 claims,
and all module/import/require structure. Attribute coverage includes all 109
`total` declarations, 149 `function` declarations, 22 `no-evaluators` opaque
symbols, 45 priority rules, 36 concrete rules, 27 owise rules, 4 macros, and
the sole simplification rule. There are no local `functional` declarations.

The complete inventory is
[`evidence/stage5-rule-inventory.tsv`](evidence/stage5-rule-inventory.tsv).
Every one of its 1,111 rows has a disposition and rationale in
[`evidence/stage5-rule-assessment.tsv`](evidence/stage5-rule-assessment.tsv);
there are zero unassessed rows. The material constructor/rule map and full
proof-extension record are
[`evidence/stage5-used-rule-map.md`](evidence/stage5-used-rule-map.md).

The supplied semantics is byte-identical to the trusted launcher baseline.
Static reachability review identifies 74 fixed declarations/rules on this
program path: module sequencing; typing-only import removal; closure binding;
lexical lookup; left-to-right callee/argument evaluation; frame allocation and
parameter binding; local assignment; list iterator dispatch; loop-target
binding; loop continuation; string literal and append; return; and frame pop.
Their binding, evaluation order, continuation, and cell footprints agree with
the submitted Python body. The remaining 660 fixed rules have LHS
constructs/sorts unreachable from this term; in particular all 22 opaque
symbols, all fixed concrete-only rules, and all fixed priority bridges are
inert. No unused fixed rule can supply this claim's result.

The candidate adds four function declarations and nine rules:

1. `stringCodes(str(S)) = S` plus an owise `.IntSeq` value for non-strings is a
   total, disjoint projection. On ground non-string `V`, the constructor
   equality `V ==K str(stringCodes(V))` is false.
2. `isStringSeq` is a total, structurally descending recognizer over exactly
   `.ValSeq` and `vCons`.
3. `concatFrom` is the exact guarded left fold of supplied `seqConcat`; every
   use lies under the string-sequence precondition.
4. `lastFrom` exactly describes Python's final loop-target local and descends
   on the tail.
5. The only `[simplification]` rule has domain
   `applyBin("+",str(A),V)` with guard
   `V ==K str(stringCodes(V))`. The guard is true exactly when `V=str(B)`;
   both it and supplied `str.k` then produce
   `str(seqConcat(A,B))`. It is pure and changes no state, binding,
   continuation, allocation, exception, or control cell.

Ground positive and negative recognizer cases, both folds, and the
simplification overlap all close in
[`evidence/stage5-proof-local-function-tests.log`](evidence/stage5-proof-local-function-tests.log).
The loop claims are derived reachability lemmas, not ordinary rewrite axioms.
They match the exact body and frame, are quantified over the continuation and
framed cells they accept, execute fixed semantics, and were independently
proved before compositional use.

There is no candidate operational bridge, unconstrained oracle, fresh result,
answer-encoding rule, abrupt-control shortcut, inconsistent overlap, false
totalization, or priority preemption. No rule is labeled unsound, so the
false-conclusion-witness obligation for an unsoundness finding does not arise.

Stage 5 result: PASS.

## 6. Fresh non-vacuity test

I did not use the candidate's `spec-vacuity.k`. The fresh reviewer mutation
keeps the exact submitted program term and uses the satisfying typed input
`["a","b"]`, but changes the result obligation from true `"ab"` to false
`"ac"`. The source is
[`evidence/spec-fresh-false-result.k`](evidence/spec-fresh-false-result.k).

`kprove spec-fresh-false-result.k --definition
verification-audit-kompiled --spec-module SPEC-FRESH-FALSE-RESULT` parses and
executes successfully to the terminal actual value
`str(iCons(97,iCons(98,.IntSeq)))`. That state cannot unify with expected
`str(iCons(97,iCons(99,.IntSeq)))`; K reports `WarnStuckClaimState` and exits
1. The bounded command, residual, and exact status are in
[`evidence/stage6-fresh-false-result.log`](evidence/stage6-fresh-false-result.log).
This is the expected unmet result obligation, not a parser error, missing
import, timeout, crash, or unreachable mutation.

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### Formally established

Conditional on the supplied MPY semantics and K implementation, the successful
reachability proof establishes:

> For every finite semantic `ValSeq` all of whose elements have form
> `str(IntSeq)`, executing the exact trusted translation of submitted
> `solution.py` from the stated initial configuration and calling
> `concatenate(list(VS))` reaches
> `str(concatFrom(.IntSeq,VS))`, where `concatFrom` appends every member's code
> sequence in order. The specified heap, counters, stack, return, exception,
> and exit cells are restored as claimed.

This is a universal, unrestricted typed-domain partial-correctness result. The
differential tests and ground executions are supporting evidence, not a
substitute for this K proof.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Launcher-supplied MPY semantics | Defines all executed binding, call, loop, string, return, and state behavior | Acceptable and mandated. The candidate copy is byte-identical; every used rule was statically mapped and concrete boundaries were executed. |
| K parser, kompilers, LLVM/Haskell backends, and `kprove` | Parses, executes, and proves the reachability claims | Standard machine-checking trust boundary; fresh reconstruction avoids candidate binaries/caches. |
| K built-in integers, algebraic constructors, maps/lists, Boolean operations, equality, and sequence recursion | Supports fixed semantics and proof-local mathematics | Ordinary K mathematical/runtime primitives; no candidate opaque interpretation is involved. |
| Trusted `py2mpy.py` | Connects `solution.py` to the constructor program | Mandated trusted translator; fresh output is byte-identical and the entry claim is mechanically identical to that output. |
| `str(IntSeq)` as the semantic string representation | Bridges semantic sequence append to ordered Python string concatenation | Acceptable for this operation: no character inspection or normalization occurs. Symbolic coverage is arbitrary sequence content; 1,010 CPython comparisons support, but do not prove, the general intent bridge. |
| Python type annotation `List[str]` | Excludes non-list and non-string inputs | Matches the prompt exactly. There is no added size, alphabet, encoding, or example-only restriction. |
| Termination and external behavior outside the model | Concurrency, mutation during iteration, invalid input exceptions, and full CPython internals | Outside the typed HumanEval contract and partial-correctness theorem; none is used to prove a value-level conclusion on the intended domain. |

No supplied opaque primitive and no candidate opaque symbol affects the branch,
return value, state, exception, or postcondition of this theorem. There is no
empirical oracle inside the proof.

Stages 1 through 7 all pass. The proof is sound under the selected supplied
semantics, constrains the requested result, mechanically executes the real
generated program, and covers the material HumanEval source-contract domain.
The ordinary explicit tool/semantics trust boundary is not a material adequacy
gap.

VERDICT: PASS
LEGITIMACY: LEGIT
