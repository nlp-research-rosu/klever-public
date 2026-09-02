# Independent adversarial review: 17-parse-music

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I reconstructed the proof from source,
checked that its program term is the regenerated submitted function, reviewed
the complete imported K rule inventory, and rejected a fresh reachable false
postcondition. Candidate-provided compiled definitions, logs, `PROOF.md`, and
generation claims were not used as proof authority.

## 1. Input and provenance integrity

The declared layout is `pipeline-v3`, the condition is `kit-semantics`, and the
rendered semantics mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, as required.

The independent checker and its complete command log are
[provenance_check.py](/audit-output/evidence/provenance_check.py) and
[provenance_check.log](/audit-output/evidence/provenance_check.log). It checked
the following:

- `/audit-input.json` and `/audit-campaign-lock.json` are real regular files.
  The `audit_campaign` object equals the mounted lock object, and the lock's
  SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every record required for `pipeline-v3` is present and is not a symlink:
  `/run.json`, `/task.json`, `/generation-result.json`, invocation, metrics,
  runtime metrics, usage, last message, output log, prompt, and the structured
  trace.
- All recorded per-file hashes checked by the script match. The single JSONL
  trace has its recorded hash
  `759b5f3e2b3effdef95273f7eff9459f58457de597f2e24a505f324ea9128581`;
  all 449 JSONL records parse, with the expected terminal task-complete record.
  Generation success messages were treated only as untrusted historical
  claims.
- The pipeline tree digest independently recomputed for the mounted candidate
  is
  `b894ae2f2d27466ee2c63bf82eb833ca09fc2d04c43e1fe9993968246adad88d`,
  equal to the recorded stage output. The independently recomputed trace-tree
  digest is
  `388098a9767a111be0d8e4d625c59125d17aa8cbd437b9d824b9062e67ffbd68`,
  equal to `usage.json`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- Recursive type-and-content comparison of candidate and trusted supplied
  semantics found exactly the same 24 regular files, no missing or additional
  entries, no symlinks or unsupported types, and no byte differences. Both
  trees independently hash to
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the task manifest.

The run, task, result, invocation, metrics, runtime-metrics, and usage objects
are mutually consistent. There is no semantics-mode contradiction and no audit
infrastructure breach.

## 2. Program fidelity and canonical comparison

### Contract

The trusted [prompt.py](/reference/prompt.py:4) asks `parse_music` to translate
a valid space-delimited sequence of note tokens to durations, preserving
order:

- `o` means 4 beats;
- `o|` means 2 beats;
- `.|` means 1 beat.

The trusted [canonical.py](/reference/canonical.py:19) splits on the ASCII
space, drops empty fields, and looks up those three tokens. Thus empty strings
and runs of spaces yield an empty list, and leading, trailing, or repeated
spaces are harmless on the intended token language.

The submitted [solution.py](/candidate/solution.py:4) is a character scanner.
It stores a pending 4 after `o` and a pending 1 after `.`, turns pending 4 into
2 and appends on `|`, flushes pending 4 on any other character, and flushes a
final pending 4 at end-of-input. This is a different algorithm but has the same
result on the contract domain. Its behavior on invalid strings is more
permissive than the canonical implementation; that does not narrow or alter the
valid source-contract domain.

### Trusted regeneration

In a fresh scratch copy, the exact command

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy &&
cmp solution.mpy solution.regenerated.mpy &&
sha256sum solution.mpy solution.regenerated.mpy
```

exited 0. Both files hash to
`01547d6182a76e76989e55e1f983f2fa053036300de4551bfcad5e407d8a3484`;
see [translation_identity.log](/audit-output/evidence/translation_identity.log).

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and submitted Python entry points by absolute path. Its
deterministic input corpus is preserved in
[differential_inputs.jsonl](/audit-output/evidence/differential_inputs.jsonl)
with SHA-256
`257a95329c3837307f103443a47ea8babb18e9ed598604d280539c7776b8205e`.
It includes:

- the documented example;
- empty and all source-branch boundary cases;
- every note sequence of length 0 through 6 under one-, two-, and three-space
  separators and leading/trailing layouts;
- 5,000 deterministic generated valid strings of up to 100 notes;
- homogeneous and mixed valid strings of 4,096 notes.

The command `python3 /audit-output/evidence/differential_test.py` exited 0 with
18,040 unique cases and zero mismatches. The exact output and status are in
[differential_test.log](/audit-output/evidence/differential_test.log).

## 3. Clean proof reconstruction

I copied only source inputs to `/tmp/audit-work/candidate-src`, taking
`reference-semantics/`, `prompt.py`, `canonical.py`, and `py2mpy.py` from the
trusted reference mount. Candidate `runtime-kompiled/`,
`verification-kompiled/`, Python caches, and prior logs were neither copied nor
used. Fresh output directories were named `runtime-audit-kompiled` and
`verification-audit-kompiled`.

Tool versions were K 7.1.293 and Python 3.10.12; see
[tool_versions.log](/audit-output/evidence/tool_versions.log).

| Purpose | Exact command | Exit/result |
|---|---|---|
| LLVM definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled` | 0; [log](/audit-output/evidence/kompile_llvm.log) |
| Concrete execution | `krun concrete_cases.mpy --definition runtime-audit-kompiled` | 0; final `<k> .K </k>`, `<exit-code> 0`; [log](/audit-output/evidence/krun_concrete.log) |
| Haskell proof definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled` | 0; [log](/audit-output/evidence/kompile_haskell.log) |
| Loop claim | `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.scan-loop` | 0, `#Top`; [log](/audit-output/evidence/kprove_scan_loop.log) |
| Complete two-claim spec | `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC` | 0, `#Top`; [log](/audit-output/evidence/kprove_all.log) |

The compiler warnings concern unused variables and incomplete functions in
unrelated portions of the supplied general-purpose semantics. No warning is a
proof failure or is on a target-used total function. The concrete source
[concrete_cases.py](/audit-output/evidence/concrete_cases.py) contains assertions
for empty input, spaces, each note form, repeated spaces, and the prompt example.

Both positive target claims therefore close under a clean definition with the
required zero exit status and `#Top`.

## 4. Adequacy and real-program pinning

### Claims in plain language

The auxiliary [scan-loop claim](/candidate/spec.k:6) says: starting at the real
`#loop` over an arbitrary finite suffix `CS`, with pending integer `CUR` and
result list `ACC`, fixed execution consumes that suffix and leaves
`current = scanCurrent(CS,CUR)` and
`result = scanResult(CS,CUR,ACC)`. It preserves the input and result reference,
the parent scope, framed scopes/heap entries, and the continuation. The final
`char` is intentionally existential because it is irrelevant after the loop.

The [entry claim](/candidate/spec.k:23) says: for every finite `CS:IntSeq`, in a
fully specified module/builtins state with an empty heap and `parse_music`
bound to the submitted body, calling it on `str(CS)` returns `ref(0)`. The sole
heap object is then `0 |-> list(musicResult(CS))`; the frame is popped, the
caller environment and scopes are restored, the heap counter is 1, the stack
is empty, return state is `noRet`, exception state is `NoExc`, and exit code is
0. This is a strong result-bearing postcondition, not a free value,
tautology, or one-way implication.

### Mechanical constructor identity

[constructor_compare.py](/audit-output/evidence/constructor_compare.py)
mechanically:

1. reads the freshly regenerated `solution.mpy`;
2. extracts the `parseMusicBody` and `parseMusicCharBody` equations from
   `verification.k`;
3. expands the one nested body alias;
4. normalizes only the outer-parser spellings of empty `.Exprs` and `.Stmts`;
5. parses both complete `FuncDef` terms with `kast`; and
6. compares their KAST objects for exact equality.

The check also verifies the entry call name and closure binding in `spec.k`.
It exited 0 with
`funcdef_kast_sha256=0b7fbc378d37b264286fcba2dc0e081843416f77adbf8638439caa8c51e51634`
and `constructor_equal=true`; see
[constructor_compare.log](/audit-output/evidence/constructor_compare.log).
The extracted normalized and raw terms are
[claim_function.mpy](/audit-output/evidence/claim_function.mpy) and
[claim_function_raw.txt](/audit-output/evidence/claim_function_raw.txt).

The claim starts after module loading rather than at the complete module. This
normalization is semantically inert and demonstrated by the supplied rules:
`ImportFrom("typing", ...)` takes the non-math no-op rule in
`controls.k`, while the unannotated `FuncDef` rule in `functions.k` creates
exactly `closureVal("music_string", .ParamNames, BODY, 0)`. The claim pins that
same binding, body, defining environment, module state, and allocation state.

### Satisfiable states and substitutions

[ground-spec.k](/audit-output/evidence/ground-spec.k) supplies three explicit
satisfying states:

- the entry configuration with `CS = .IntSeq`, expecting `[]`;
- the entry configuration with `CS` equal to the codes of `"o o| .|"`,
  expecting `[4,2,1]`;
- a fully ground empty-suffix loop head with concrete environment, scope,
  result heap location, accumulator, current value, and parent.

`kprove ground-spec.k --definition verification-audit-kompiled
--spec-module AUDIT-GROUND-SPEC` exited 0 with `#Top`; see
[kprove_ground.log](/audit-output/evidence/kprove_ground.log).
[ground_compare.py](/audit-output/evidence/ground_compare.py) independently
shows that both trusted canonical and submitted Python implementations return
`[]` and `[4,2,1]` for those two entry inputs; see
[ground_compare.log](/audit-output/evidence/ground_compare.log).

As supplementary body-sensitivity evidence, I independently ran the
candidate's changed-body claim after inspecting it. Its closure actually uses
the mutated body in which `o` assigns 5. The proof exited 1 with a reachable
actual empty list instead of the demanded `[4]`; see
[kprove_candidate_body_mutation.log](/audit-output/evidence/kprove_candidate_body_mutation.log).
This changes the term executed by the claim, not merely an external source
file.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[inventory_k.py](/audit-output/evidence/inventory_k.py) inventories the supplied
entry file, all 23 supplied helper K files, `verification.k`, and `spec.k`.
The exact source blocks, file hashes, line numbers, attributes, and stable IDs
are in [rule_inventory.txt](/audit-output/evidence/rule_inventory.txt), with
machine-readable counts in
[rule_inventory_summary.json](/audit-output/evidence/rule_inventory_summary.json).
The inventory contains 712 rules, 232 syntax declaration blocks, 5 contexts, 1
configuration, and 2 claims. There are no `[simplification]` or `[functional]`
declarations. The inventory itself hashes to
`b673e1f8215bffa2a0dec96d5be682cf802d67d98720edf0fbcaffa3c5379aff`.

The following range disposition applies to every rule ID in each range. Rules
marked unused have no constructor/operator/call shape reachable from this
program, so they cannot contribute to target closure. They remain part of the
trusted supplied semantics rather than candidate proof extensions.

| File | Rule IDs | Target-path review |
|---|---:|---|
| `semantics.k`, `syntax.k`, `iter.k` | no rules | Import graph, AST grammar, and iterator protocol declaration are well-sorted; all submitted constructors are declared. |
| `assert.k` | 0001–0003 | Unused (`Assert` absent). |
| `bool.k` | 0004–0016 | Boolean operator/short-circuit rules are disjoint; target only consumes comparison booleans through `truthy`. |
| `builtins.k` | 0017–0153 | No builtin call occurs in the claimed body; these rules cannot match the target path. |
| `call.k` | 0154–0174 | Relevant callee-first/argument-left-to-right routing, bound method dispatch, closure frame creation, and parameter binding are faithful. The exact list-append rule preempts generic method dispatch. |
| `comprehension.k` | 0175–0181 | Unused; the submitted implementation has no comprehension. |
| `concrete.k` | 0182–0197 | Not imported by the Haskell `VERIFICATION` module; used only by the separate LLVM concrete definition. |
| `controls.k` | 0198–0231 | Relevant `Assign`, effect-only `Expr`, `If`, `For`, loop iteration, and loop-label rules preserve evaluation order and the intended cells. Break/continue/while/import branches not reached by the claim do not affect it. |
| `core.k` | 0232–0277 | Relevant configuration, allocation, statement sequencing, lexical lookup, literal evaluation, argument evaluation, truthiness, and sequence helpers are faithful and preserve the framed cells. |
| `dict.k` | 0278–0305 | Unused; no dict constructor, subscript, or dict method appears. |
| `float.k` | 0306–0426 | Unused and sort-disjoint; no Float term or float operation appears in the program or claims. |
| `functions.k` | 0427–0441 | The unannotated closure rule, ordinary parameter binding, abrupt `Return`, `#pop`, environment restoration, frame deletion, and heap preservation match the actual call. Annotated-closure branches are disjoint and unused. |
| `int.k` | 0442–0457 | The used integer `==` rule is ordinary integer equality. Other operators are unused. |
| `list.k` | 0458–0484 | Relevant empty-list allocation, `valSeqConcat`, and in-place `append` are exact. The append priority selects the heap-mutating receiver case and returns `noneV`; `Expr` then discards it. |
| `methods.k` | 0485–0559 | No `applyMethod` rule is reached; append is handled by `list.k`. |
| `operators.k` | 0560–0569 | Contexts evaluate comparison operands in order and dispatch exact string or integer equality. Heap-reference branches are not used for these comparisons. |
| `range.k` | 0570–0575 | Unused. |
| `set.k` | 0576–0587 | Unused. |
| `sort.k` | 0588–0606 | Unused; neither `sorted` nor `.sort()` appears. |
| `str.k` | 0607–0634 | Relevant string iteration yields exactly one-character strings in order; ASCII literal conversion and string equality distinguish `o`, `.`, and `|` at codes 111, 46, and 124. |
| `subscript.k` | 0635–0674 | Unused. |
| `tuple.k` | 0675–0695 | The relevant `#bindTgt(Name(...),V)` rule updates `char` in the current loop frame. Tuple construction/unpacking branches are unused. |
| `verification.k` | 0696–0712 | Reviewed individually below; all are truthful and no rule bypasses a `<k>` computation. |

### Used-construct coverage and state/control effects

Every material submitted constructor has a fixed execution route:

| Submitted construct | Declaration and operational route |
|---|---|
| function call and name | `syntax.k`; `core.k` lookup; `call.k` callee/args and closure frame |
| `result = []` | assignment strictness; `list.k` evaluation and `core.k` fresh allocation |
| integer/string/name literals | `core.k` and `str.k` |
| `for char in music_string` | `controls.k`; `str.k` iterator; `tuple.k` name-target binding |
| nested `if` and comparisons | strictness/contexts in `syntax.k` and `operators.k`; equality in `str.k`/`int.k`; branching in `controls.k` |
| `result.append(current)` | `call.k` bound method and argument order; priority-selected heap update in `list.k`; effect discard in `controls.k` |
| `return result` | strict lookup, abrupt return, and frame pop in `functions.k` |

The call reads and restores `<env>`, allocates/deletes a scope, pushes/pops
`<stack>`, allocates and mutates `<heap>`, advances `<heapLoc>`, and uses
`<ret>`. The entry postcondition observes all of those cells plus `<exc>` and
`<exit-code>`. The loop body allocates no new objects, performs no return or
exceptional control, and changes only `char`, `current`, and the referenced
list; the loop claim frames all other state and its arbitrary continuation.

### Proof-local declarations and rules

The proof-local theory has no priority rule, simplification, opaque symbol,
oracle, or operational bridge.

- `parseMusicBody` and `parseMusicCharBody` each have one exact unfolding
  equation. The KAST comparison proves these equations name the submitted AST;
  fixed semantics then performs every lookup, comparison, branch, call,
  mutation, loop step, return, and pop.
- `mutatedParseMusicBody` and `mutatedParseMusicCharBody` are disjoint nullary
  symbols used only by a negative probe. They do not occur in either positive
  claim.
- `nextCurrent` has the exhaustive, disjoint partition
  `C=111`, `C=46`, and neither.
- `nextResult` partitions pipe/current-4, pipe/current-not-4,
  other-delimiter/current-4, and the complementary no-append cases. Any
  syntactic overlap inside the final disjunction has the same right-hand side;
  there is no conflicting equation.
- `scanCurrent` and `scanResult` have disjoint empty/cons equations and recurse
  on the strict `IntSeq` tail.
- `musicResult` has disjoint, exhaustive final-current-equals-4 and
  final-current-not-equals-4 equations.

[step_partition_check.py](/audit-output/evidence/step_partition_check.py)
independently compares the source one-character transition with these
equations over every code predicate class and both current-value classes. It
exited 0 with 20 representative partition cases and zero mismatches; see
[step_partition_check.log](/audit-output/evidence/step_partition_check.log).
The universal connection is not inferred from that finite check: it is the
focused, machine-checked `SPEC.scan-loop` reachability claim.

The supplied definition contains 25 explicitly symbolic primitives:
`sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, and `md5hexCodes`. None appears in the submitted program, proof-local
definitions, claims, or final residuals; their sorts/call patterns are
unreachable here. Underdefined out-of-bounds subscript helpers and the supplied
sort/float/MD5 trust boundaries are likewise irrelevant to this theorem.

I found no unsound candidate rule. Consequently there is no unsoundness claim
for which a false-conclusion witness is required.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`.
[audit-false-post.k](/audit-output/evidence/audit-false-post.k) is a fresh
reviewer-authored mutation using the reachable input `"o o| .|"`. It changes
only the result-constraining heap obligation from the true `[4,2,1]` to the
false `[4,2,2]`, while executing the original `parseMusicBody`.

First,

```text
kprove audit-false-post.k --definition verification-audit-kompiled
  --spec-module AUDIT-FALSE-POST --dry-run
```

exited 0, proving that the mutation parses and builds; see
[false_post_dry_run.log](/audit-output/evidence/false_post_dry_run.log).
Then the same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its reachable residual contains

```text
0 |-> list(vCons(4, vCons(2, vCons(1, .ValSeq))))
```

instead of the demanded final 2; see
[false_post_proof.log](/audit-output/evidence/false_post_proof.log). The
positive ground K claim and both Python implementations independently establish
the same satisfying witness. This is a meaningful unmet result obligation, not
a parse error, missing import, timeout, unrelated crash, or unreachable
mutation.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

For every finite `CS:IntSeq`, under the supplied `MPY` definition, the exact
submitted `parse_music` closure called from the entry configuration reaches a
normal final configuration returning `ref(0)` whose heap object is exactly
`list(musicResult(CS))`, with the stated frame, allocation, stack, return,
exception, and exit-code effects. The independently closed loop claim proves
that `scanCurrent` and `scanResult` are exact summaries of all iterations of the
real body. This is a universal K reachability proof, not a bounded collection of
examples.

On the valid music grammar, the summary has the requested meaning by an
exhaustive token induction:

- `o` sets pending 4; a following space flushes 4, and end-of-input performs
  the same final flush;
- `o|` sets pending 4, then `|` changes it to 2, appends 2, and resets;
- `.|` sets pending 1, then `|` appends 1 and resets;
- any separating space with pending 0 emits nothing.

Concatenating these cases preserves order, and repeated/leading/trailing spaces
are no-op separator cases. Thus `musicResult` equals the canonical token map on
the complete intended domain. The 18,040-case differential test is supporting
evidence for this bridge, not a substitute for the universal K execution proof.

### Trust ledger

| Boundary | Effect on theorem | Assessment/evidence |
|---|---|---|
| Supplied MPY semantics | Defines Python-subset values, evaluation order, calls, state, and control. | Required trusted input; recursively identical candidate/trusted trees. Every target-used rule was statically reviewed and concretely exercised. |
| K 7.1.293 compiler, Haskell backend, SMT/rewrite engine | Establishes `#Top` and the stuck mutation residual. | Standard unavoidable checker boundary; clean positive and discriminating negative runs recorded. |
| K built-in Int, Bool, String, Map, List, equality, and collection framing primitives | Implement the low-level mathematics and configuration matching used by fixed semantics. | Ordinary low-level trust boundary; no task answer is encoded in it. |
| `strToCodes` use of K string hooks for the three ASCII literals | Produces codes 111, 46, and 124 used by the real comparisons. | Ground fixed-semantics reduction closes the symbolic proof and concrete cases; literals are within the declared ASCII subset. |
| Trusted `py2mpy.py` and CPython AST parsing | Determines the submitted MPY constructor artifact from `solution.py`. | Regeneration is byte-identical and constructor comparison pins the exact function. Translator-to-Python fidelity is additionally supported by concrete and differential execution. |
| The 25 supplied symbolic primitives listed in Stage 5 | Could abstract sorting, float, or MD5 behavior in other tasks. | They have no dependent target rule, claim, value, branch, state, or postcondition in this proof and therefore add no assumption to the result. |
| Canonical-vs-generated differential corpus | Supports implementation/intent and Python-to-MPY model adequacy on finite cases. | 18,040 cases, zero mismatches; explicitly not used as universal proof. |
| Token-induction interpretation of `musicResult` | Connects the exact execution summary to the natural-language legend. | Exhaustive over all three token forms and separator/end cases; no domain restriction or result-bearing oracle is introduced. |

Gate A passes: the real body executes under fixed semantics, there is no
operational bridge or result oracle, the preconditions are satisfiable, the
result is constrained, and the fresh false postcondition is rejected. Gate B
passes: the formal `IntSeq` domain includes the full source-contract string
domain, and the summary has the required note meaning without a finite bound.
Gate C passes: all commands, inputs, scripts, inventories, outputs, and trust
boundaries needed for this decision are preserved under
`/audit-output/evidence/`.

VERDICT: PASS
LEGITIMACY: LEGIT
