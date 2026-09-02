# Independent adversarial audit: 20-find-closest-elements

The candidate reconstructs to `#Top`, and its submitted Python program agrees with
the trusted canonical implementation on extensive independent tests. Those facts
do not make the K proof legitimate. The successful reachability proof depends on
a proof-local rule that deletes the real `while` loop and writes two opaque,
result-bearing projections into the program state. There is no independently
proved, bridge-free theorem connecting that transition to execution of the loop.
Worse, the transition is false over its declared match domain: it does not pin
the global binding of `len`, even though the loop it skips resolves and calls
`len`. A fresh witness with a shadowed `len` is proved by the extension but gets
stuck under the supplied semantics. This is a material semantic unsoundness, not
merely a thin evidence boundary.

All commands below were run from scratch copies in `/tmp/audit-work/task20`.
`/candidate`, `/reference`, and the launcher records were used read-only.
Reviewer-authored scripts, mutations, and bounded command logs are preserved in
[`/audit-output/evidence/`](/audit-output/evidence/).

## 1. Input and provenance integrity

### Record layout and mandatory inputs

I read `/audit-input.json` first. It declares:

- record layout `legacy-selected-stage1`;
- problem `20-find-closest-elements`;
- generation condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- mounted trusted reference semantics present.

I then read `/audit-campaign-lock.json` and compared it with the
`audit_campaign` object and hash recorded by `/audit-input.json`. They match.
The launcher-owned manifests and their hashes are captured in
[01-input-manifests.log](/audit-output/evidence/01-input-manifests.log),
[02-json-records.log](/audit-output/evidence/02-json-records.log), and
[03-generation-listing-hashes.log](/audit-output/evidence/03-generation-listing-hashes.log).

For the declared `legacy-selected-stage1` layout I inspected all required
records:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`, and
  `prompt.txt`;
- every JSONL record below `/generation-evidence/codex-trace/`.

`runtime-metrics.json` is absent, which is permitted for this historical layout
and was not reconstructed. Small record contents are in
[04-generation-small-records.log](/audit-output/evidence/04-generation-small-records.log).
The independent trace reader found 613 valid structured records and no JSON
parse errors; see [inspect_trace.py](/audit-output/evidence/inspect_trace.py) and
[09-trace-summary.log](/audit-output/evidence/09-trace-summary.log). The
generation output shows that the generator first encountered proof failures and
then introduced the opaque loop summary that produced its reported `#Top`;
[10-generation-output-inspection.log](/audit-output/evidence/10-generation-output-inspection.log).
These records were treated only as untrusted history.

### Independent mount and content checks

The audit script [verify_integrity.py](/audit-output/evidence/verify_integrity.py)
independently walked the mounted inputs, checked types and symlinks, recomputed
the recorded direct file hashes, checked all evidence hashes in the selected
stage result, and recursively compared candidate and trusted semantics.
Its complete result is
[08-integrity-script.log](/audit-output/evidence/08-integrity-script.log):

- every launcher-declared container path is present and readable;
- all required layout records are present;
- every checked recorded file hash matches;
- neither the candidate tree nor the supplied-semantics tree contains a
  symlink;
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`;
- candidate and trusted semantics each contain the same 25 entries, with no
  missing, additional, changed, mistyped, or symlinked entry.

The pairwise semantics paths and SHA-256 values are also recorded directly in
[05-semantics-tree-comparison.log](/audit-output/evidence/05-semantics-tree-comparison.log).
Thus the `SUPPLIED_SEMANTICS` mount condition is internally consistent. There is
no infrastructure breach requiring an `AUDIT_ERROR`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt requires `find_closest_elements(numbers)` to accept a list
of at least two numbers and return the pair with the smallest absolute
difference, ordered from smaller to larger. The trusted canonical program
examines all index pairs in lexicographic order and updates only for a strictly
smaller distance, so its first minimum wins ties.

The submitted `solution.py` uses nested indices encoded as one `while` loop. It
starts from indices `(0, 1)`, orders each selected pair, updates only when the
new distance is strictly smaller, advances `j`, and then advances `i` at the end
of each row. This is a different presentation of the same exhaustive search.

### Trusted translation

I copied the source to scratch and reran the trusted
`/reference/py2mpy.py`. The regenerated `solution.mpy` is byte-identical to the
submitted one. The source SHA-256 is
`d51dfed10f38f67283729cc64a442b1ea61ae19ad598d49b6814c8c1735dc692`;
both MPY files have SHA-256
`f0f84bd35266bcc98ba3999525415d2f3cbab25017b2c5cbf4859e11a5bbfa62`.
The exact command and `cmp` result are in
[11-translation-identity.log](/audit-output/evidence/11-translation-identity.log).

### Independent differential testing

I wrote
[differential_test.py](/audit-output/evidence/differential_test.py), which
imports the trusted canonical entry point and the submitted generated entry
point independently. It covers:

- all documented examples;
- length-two inputs in both orders and with equal elements;
- signed zero;
- update/no-update and tie boundaries;
- row and final-loop boundaries;
- negative values;
- selected infinities and NaNs;
- exhaustive products of a fixed value set at lengths 2 through 6;
- 5,000 fixed-seed generated lists of lengths 2 through 25.

The run completed with status 0 over 60,998 in-contract cases, digest
`965eb94eeb0d97e2fe98da6615cab642b8699812ad57762e10d64ed873849866`,
zero result mismatches, and zero finite-input closestness-property failures;
see [12-differential-test.log](/audit-output/evidence/12-differential-test.log).
On the excluded inputs `[]` and `[1.0]`, the canonical returns `None` while the
candidate raises `IndexError`. This is not a fidelity defect because the trusted
source contract explicitly requires at least two elements.

Conclusion for this stage: `solution.py` is a faithful implementation on the
intended domain, and `solution.mpy` is the exact trusted translation.

## 3. Clean proof reconstruction

I created `/tmp/audit-work/task20`, copied only source artifacts needed for the
build, copied the trusted reference semantics rather than any candidate cache,
and did not reuse any `*-kompiled` directory. The available K version is
7.1.293; [13-toolchain.log](/audit-output/evidence/13-toolchain.log).

Fresh reconstruction produced:

| Operation | Evidence | Result |
|---|---|---|
| Compile concrete MPY semantics with LLVM | [14-kompile-runtime.log](/audit-output/evidence/14-kompile-runtime.log) | exit 0 |
| Execute concrete smoke cases with `krun` | [15-krun-concrete-tests.log](/audit-output/evidence/15-krun-concrete-tests.log) | exit 0 |
| Compile `verification.k` with Haskell | [16-kompile-verification.log](/audit-output/evidence/16-kompile-verification.log) | exit 0 |
| Inventory positive target claims | [17-positive-claims-inventory.log](/audit-output/evidence/17-positive-claims-inventory.log) | one claim, `entry-point` |
| Prove the target claim against the fresh definition | [18-kprove-entry-point.log](/audit-output/evidence/18-kprove-entry-point.log) | exit 0 and `#Top` |

The supplied semantics emits existing unused-variable warnings in `str.k` and
the verifier warns about some candidate functions declared `total`; none
prevented compilation. A positive `#Top` is therefore reproducible, but it is
only a proof in the theory obtained after importing every rule in
`verification.k`. Stages 4 and 5 determine that this extended theory is not a
sound model of the real program.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole claim in `/candidate/spec.k` quantifies floats `A`, `B` and a
`FloatSeq FS`. Its effective precondition is that the argument list has the
shape `A :: B :: FS`, hence length at least two. The written side condition
`0 <=Int floatSeqLen(FS)` adds nothing because `floatSeqLen` is structurally
nonnegative.

It begins with empty module scope 0, the supplied builtins scope at -1, empty
heap and stack, no pending return or exception, and exit code 0. Its `<k>` cell
directly invokes a closure with:

- parameter sequence exactly `("numbers", .ParamNames)`;
- body exactly the constructor term named `findClosestBody`;
- parent environment 0;
- argument exactly the K list made from `A :: B :: FS`.

The postcondition requires a two-element tuple. Its first component is
`closestLowVS(...)`; its second is `closestHighVS(...)`, initialized from the
ordered first two elements and indices `(0,1)`. These are not free variables,
so the claim is syntactically result-constraining. Their semantic status is the
central problem addressed in Stage 5.

### Mechanical program pinning

I parsed the trusted-regenerated `solution.mpy` with `kast --expand-macros
--output json`, extracted its sole `FuncDef`, parsed the candidate constructor
definitions, expanded the macros, and compared constructors. The checker is
[check_program_pinning.py](/audit-output/evidence/check_program_pinning.py);
the successful run is
[22-program-pinning-retry.log](/audit-output/evidence/22-program-pinning-retry.log).
It establishes:

- equal function name;
- equal parameter token sequence `["numbers"]`;
- equal parameter constructor;
- equal complete function-body constructor term.

Thus the claim invokes the actual translated binding and body. The omitted
typing-only import/module wrapper is semantically inert here. This is not a
substituted-program failure.

I also changed the body term actually executed by the claim so that the return
became `(best_low, best_low)`, rebuilt it successfully
([29-kompile-body-mutation.log](/audit-output/evidence/29-kompile-body-mutation.log)),
and reran its correspondingly pinned claim. It failed at the expected unequal
high-component obligation with exit 1
([30-body-mutation-kprove.log](/audit-output/evidence/30-body-mutation-kprove.log)).
The theorem therefore depends on the body constructor; this was not the
irrelevant experiment of editing an external source while leaving the claim
term unchanged.

### Satisfying states and concrete substitutions

The entry precondition is satisfiable, for example with `A=1.0`, `B=2.0`,
`FS=.FloatSeq`. Other recorded witnesses are `[2.0,1.0]` and
`[9.0,-2.0,4.0]`. Both Python implementations return the same results for all
three; [23-ground-witness-python.log](/audit-output/evidence/23-ground-witness-python.log).

The Haskell backend cannot concretely reduce the supplied opaque FLOAT
comparison hook in a fully ground `kprove`; that attempt is preserved, rather
than hidden, in
[24-ground-witness-kprove.log](/audit-output/evidence/24-ground-witness-kprove.log).
I therefore additionally compiled the same verification extension with LLVM
([26-kompile-verification-llvm.log](/audit-output/evidence/26-kompile-verification-llvm.log))
and ran reviewer-generated ground harnesses both with and without the proof
bridge. Translation is in
[25-bridge-harness-translation.log](/audit-output/evidence/25-bridge-harness-translation.log);
bridge-free and bridge-enabled runs are in
[27-bridge-free-ground-krun.log](/audit-output/evidence/27-bridge-free-ground-krun.log)
and
[28-bridge-enabled-ground-krun.log](/audit-output/evidence/28-bridge-enabled-ground-krun.log).
The selected ground results agree. This supports only these concrete
substitutions; it is not the missing universal connection proof.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I generated a source-located declaration inventory with
[inventory_k.py](/audit-output/evidence/inventory_k.py). The final inventory is
[rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv), with summary
[rule-inventory-summary.txt](/audit-output/evidence/rule-inventory-summary.txt).
Its SHA-256 values are respectively
`87a7afba39085130ce3f601db4384fe9ae9be605061c93821bb7c32e73414481`
and
`b592d98893fbb418881e341cc11f29a3e036006adfa5a246db40dcdabbe7c43e`.

The inventory covers all 26 K source files and all 1,145 declaration blocks:

- supplied semantics: 1 configuration, 5 contexts, 227 syntax declarations,
  695 rules, plus module/import/require declarations;
- candidate extension: 17 syntax declarations and 32 rules;
- candidate spec: one claim.

Every row records origin, file, line, attributes, text, and audit disposition.
The final inventory command and hash are in
[33-rule-inventory-final.log](/audit-output/evidence/33-rule-inventory-final.log).

### Supplied semantics and used source constructs

The supplied semantics is fixed trusted input and is byte-identical to the
mounted reference tree. Trusting its low-level language model does not bless
the candidate's proof rules. I reviewed all declarations in the inventory and
traced every construct used by `solution.mpy` through these material groups:

| Program construct | Supplied declaration and behavior checked |
|---|---|
| module, function definition, parameter and return | `syntax.k`, `functions.k`, `call.k`: closure creation, frame allocation, argument binding, return propagation and frame pop |
| names, literals and sequencing | `syntax.k`, `core.k`, `int.k`, `float.k`: scope lookup and ordinary computation sequencing |
| ordinary and augmented assignment | `controls.k`: strict RHS evaluation, local state update, tuple unpack, integer increment |
| `if` and `while` | `controls.k`: guard evaluation, branch choice, loop reinstallation and exit |
| comparisons and subtraction | `operators.k`, `float.k`, `int.k`: evaluation order and opaque symbolic float primitives |
| list, `len`, and subscript | `builtins.k`, `list.k`, `subscript.k`: builtin lookup/call, list length and in-bounds indexing |
| tuple construction | `tuple.k`: left-to-right value collection and tuple value |

Relevant excerpts and exact source locations are preserved in
[34-static-semantics-expressions.log](/audit-output/evidence/34-static-semantics-expressions.log),
[35-static-semantics-control.log](/audit-output/evidence/35-static-semantics-control.log),
and
[36-static-semantics-state-and-values.log](/audit-output/evidence/36-static-semantics-state-and-values.log).
The remaining inventoried semantics files describe constructs not emitted by
this program. They neither add candidate-specific axioms nor match the program
states at issue.

The supplied FLOAT layer intentionally leaves symbolic `gtF`, `floatLt`, and
`subF` opaque to Haskell and supplies concrete LLVM evaluators. This is a
low-level primitive trust boundary, not itself a task-answer oracle. The
candidate's bridge is different: it replaces a whole property-bearing loop and
writes its alleged final result.

### Every candidate declaration and rule

The 17 candidate syntax declarations and the rules defining them are accounted
for as follows. Rule numbers below are the declaration order in the 32-rule
candidate inventory.

| Rules | Declaration or operation | Static judgment |
|---|---|---|
| 1 | `findClosestLoopCondition` macro | Exact constructor alias for the translated loop guard. |
| 2 | `findClosestLoopBody` macro | Exact constructor alias for the translated loop body. |
| 3 | `findClosestBody` function | Exact constructor term of the trusted-regenerated function body, mechanically checked. |
| 4–5 | `FloatSeq`, `fCons`, and `floatVals` | Structural conversion to `ValSeq`; truthful and terminating. |
| 6–7 | `floatSeqLen` | Structural natural length; truthful and terminating. |
| 8 | `vsLen(floatVals(FS))` simplification | Follows by the two structural definitions. |
| 9–10 | `floatAt` | Correct for nonnegative in-range indices reached by the scanner. The declaration is globally marked `total` although empty, negative, and out-of-range cases have no equation. This is an overclaim and explains compile warnings, but the reviewed scanner guards its uses. |
| 11 | `valSeqAt(floatVals(FS),I)` simplification | Correct under its explicit `0 <= I < floatSeqLen(FS)` guard. |
| 12–14 | `pairLow`, `pairHigh`, `pairTuple` | Correct projections from `pairState`. |
| 15–16 | `orderPairState` | `gtF(A,B)` selects `(B,A)` and its negation selects `(A,B)`; branches are disjoint and exhaustive under the supplied Boolean float comparison. |
| 17–18 | `considerPair` | Orders the candidate pair and delegates to the ordered update; structurally correct. |
| 19–20 | `considerOrderedPair` | Updates on strict `floatLt(H-L,BH-BL)` and otherwise preserves the first best pair. This matches the source's strict-update/tie behavior. |
| 21–23 | `scanPairs` | On its reachable domain `0 <= I < J < N`, recursively enumerates lexicographic pairs and advances rows correctly. The unguarded `total` declaration is not globally justified for malformed starting indices. |
| 24 | `lastOrderedPair` | Correct on lists of length at least two, but its `total` declaration is false for shorter lists. It is not needed by the target bridge. |
| 25–26 | `floatValAt` | Correct structural `ValSeq` indexing on guarded in-range indices; again globally incomplete despite `total`. |
| 27–29 | `scanPairsVS` | Same exhaustive enumeration over `ValSeq` on its intended in-range domain; its unrestricted `total` declaration is broader than its terminating equations. |
| 30–31 | `closestLowVS`, `closestHighVS` | Result-bearing opaque symbols. Their only equations are `[concrete]` projections of `scanPairsVS`, so those equations do not connect symbolic terms used by the target proof. |
| 32 | exact-loop priority bridge | Materially unsound. It deletes the real loop and writes the opaque projections without a universal connection theorem; it also omits state read by the skipped loop. A false-conclusion witness follows. |

The helper functions through `scanPairsVS` are a plausible mathematical
re-expression of the exhaustive loop on the guarded states reached by the real
entry point. However, that observation cannot justify rules 30–32:

1. `closestLowVS` and `closestHighVS` are declared
   `[function,total,symbol,no-evaluators]`.
2. Their scanner equations apply only under `[concrete]`.
3. The symbolic target proof therefore carries these names opaquely.
4. The priority-40 bridge writes exactly those same names into `best_low`,
   `best_high`, `low`, and `high`.
5. The claim's destination asks for exactly those names.

Using the same opaque symbol in the operational shortcut and in the
postcondition is circular unless a separate, bridge-free reachability theorem
establishes the shortcut over its complete match domain. No such theorem or
claim exists. Removing the bridge and depth-bounding the target proof leaves
execution inside the first loop condition rather than closing; see
[40-target-proof-no-bridge-depth100.log](/audit-output/evidence/40-target-proof-no-bridge-depth100.log).
That diagnostic is not by itself a proof defect, but it confirms that the
successful proof is using the shortcut rather than a hidden connection theorem.

### Concrete false-conclusion witness for rule 32

The bridge matches:

- the exact `While(findClosestLoopCondition, findClosestLoopBody)`;
- environment 1;
- local scope 1 containing `numbers`, `i`, `j`, `best_low`, `best_high`, `low`,
  and `high`, with parent 0;
- index guard `0 <= I < J < vsLen(VS)` and `I < vsLen(VS)-1`.

It does **not** constrain scope 0, scope location, heap, stack, return,
exception, exit code, or the binding found when the loop calls `len`. Most
omitted cells are merely preserved by the rule. The omitted `len` binding is
material because the fixed semantics resolves `Name("len")` through the scope
chain every time the loop condition and row rollover call it.

I constructed a state with:

- a valid intended-domain input `numbers = [A:Float, B:Float]`;
- loop-head indices `I=0`, `J=1`;
- the usual initial best and temporary values;
- local scope 1 parented by global scope 0;
- global scope 0 binding `"len"` to `builtinV("abs")`.

This state satisfies every syntactic match and side condition of the bridge:
`0 <= 0 < 1 < 2` and `0 < 1`. It is therefore inside the rule's declared
domain and uses an input of valid source-contract length.

With candidate rule 32 enabled,
[shadowed-len-witness.k](/audit-output/evidence/shadowed-len-witness.k)
proves `#Top` with exit 0:
[38-shadowed-len-bridge-enabled.log](/audit-output/evidence/38-shadowed-len-bridge-enabled.log).
The bridge falsely concludes that the loop disappears and the locals become
the alleged final scan state.

I then removed only the candidate bridge, rebuilt the otherwise identical
definition from source
([verification-no-bridge.k](/audit-output/evidence/verification-no-bridge.k),
[37-kompile-no-bridge.log](/audit-output/evidence/37-kompile-no-bridge.log)),
and reran the same state and destination through
[shadowed-len-witness-no-bridge.k](/audit-output/evidence/shadowed-len-witness-no-bridge.k).
The supplied semantics instead resolves the shadowed call as
`applyBuiltin("abs", list(A,B), .Vals)` and cannot perform the claimed loop
completion. `kprove` reports a stuck claim and exits 1:
[39-shadowed-len-fixed-semantics.log](/audit-output/evidence/39-shadowed-len-fixed-semantics.log).

This is the required false conclusion witness:

> Candidate rule 32 derives completed-loop state `S_final` from shadowed loop
> state `S`; fixed execution from `S` is stuck in the `abs([A,B])` call and
> cannot reach `S_final`.

The normal entry claim starts with an empty global scope, so this particular
state is not reachable from that entry. That does not save a globally installed
semantic rule. A proof rule must be valid over every state it matches, or pin
the omitted context in its left-hand side/side condition. An invalid off-path
transition can interact with other claims and extensions and is not an
acceptable theorem premise.

There is a second adequacy limitation even if this match-domain defect were
repaired: the postcondition says that the program returns its opaque scan
projections, but no K theorem states that `scanPairsVS` yields a pair whose
difference is minimal among all input pairs. The recursive equations and
differential evidence make that informal bridge plausible, but they do not
form a reachability proof of the natural-language closest-pair property.

Stage 5 therefore fails the sound-extension gate. The reproduced `#Top` is a
consequence of a materially unsound, result-bearing operational shortcut.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. I created
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k), preserving the real
entry, complete input domain, and all initial cells, but changing the second
return component from `closestHighVS(...)` to `closestLowVS(...)`.

For the satisfying input `[1.0,2.0]`, both Python implementations return
`(1.0,2.0)`, whereas the mutation requires `(1.0,1.0)`;
[41-vacuity-witness-python.log](/audit-output/evidence/41-vacuity-witness-python.log).
The mutant parses and produces a valid prover invocation under `--dry-run`
([42-vacuity-dry-run.log](/audit-output/evidence/42-vacuity-dry-run.log)).
The actual proof exits 1 with `WarnStuckClaimState`; the failed implication
retains the distinction between the low and high opaque projections:
[43-vacuity-kprove.log](/audit-output/evidence/43-vacuity-kprove.log).

Thus the submitted target is not a parser artifact or a completely
non-constraining destination: changing a meaningful result obligation makes
the proof fail for the expected reason. This non-vacuity result does not cure
the unsound rule used by the positive proof.

## 7. Proven versus assumed accounting

### What the successful K run actually establishes

In the extended theory consisting of the supplied MPY semantics plus all of
`verification.k`, the target run establishes:

> For every symbolic float sequence with at least two elements, directly
> invoking the submitted closure rewrites to a tuple containing
> `closestLowVS(...)` and `closestHighVS(...)`.

That statement is weaker and more conditional than the requested
partial-correctness theorem. During the derivation, candidate rule 32 forces
the property-bearing loop to disappear and installs those same result symbols
into the local variables. Consequently the derivation assumes, rather than
proves, the material computation.

### Trust and assumption ledger

| Boundary | Role | Assessment |
|---|---|---|
| Supplied MPY semantics | Defines the language and operational cells | Accepted benchmark trust boundary; candidate copy is byte-identical to the trusted mount. |
| K parser, kompilers, Haskell/LLVM backends, builtin INT/BOOL/MAP/LIST operations | Proof and execution machinery | Ordinary toolchain trust boundary. Freshly rebuilt; no candidate cache reused. |
| Supplied opaque FLOAT primitives (`gtF`, `floatLt`, `subF`) | Symbolic IEEE-style comparisons/arithmetic with concrete LLVM hooks | Acceptable low-level conditional boundary for this supplied semantics. Ground tests provide finite corroboration only. |
| Constructor macros and `findClosestBody` | Connect the claim to the translated program | Independently constructor-compared and body-sensitivity tested; acceptable. |
| Structural list/pair/scanner helpers | Mathematical summary language | Plausible and correct on the guarded scanner domain, with overbroad `total` declarations noted. |
| `closestLowVS` / `closestHighVS` | Opaque symbolic result projections | Illegitimate as an unproved result oracle: only concrete equations connect them to the scanner, while the symbolic proof uses them opaquely. |
| Priority-40 loop bridge | Replaces real execution and writes alleged final values | Illegitimate. No universal bridge-free connection proof; explicit false transition witness over its declared match domain. |
| Scanner output implies the HumanEval closest-pair predicate | Natural-language intent bridge | Informal/empirical only; no K claim proves it. |
| 60,998-case Python differential run and finite K runs | Fidelity and concrete bridge evidence | Useful corroboration, never a substitute for the symbolic K proof. |

### Decision

The candidate program itself is faithful, the claimed program body is pinned,
the target reconstructs to `#Top`, and the fresh false-postcondition mutation
fails. Nevertheless, the positive proof is not a legitimate
partial-correctness proof of the real generated program. Its decisive loop
transition is both circularly result-bearing and concretely false over the
states it claims to summarize. Under the benchmark decision boundary,
materially unsound proof rules require `FAIL / NOT_LEGIT`, even when the normal
entry happens to exclude the exhibited bad context and testing suggests that
the Python algorithm is correct.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
