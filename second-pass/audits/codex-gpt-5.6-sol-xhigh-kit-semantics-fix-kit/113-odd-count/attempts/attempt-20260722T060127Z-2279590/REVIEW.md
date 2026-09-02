# Independent adversarial audit: 113-odd-count

## Outcome

The candidate contains a legitimate, non-vacuous partial-correctness proof of the submitted translated program over its stated K domain: finite lists of finite ASCII digit strings. I rebuilt the supplied concrete semantics and four proof definitions from source in an isolated scratch tree; every positive claim exited 0 with `#Top`. The final claim loads the byte-verified translation of `solution.py`, returns a constrained reference, and constrains that reference's heap value to the calculated output list. Separately proved lower-layer claims justify all three execution-summary bridges.

The verdict is `CONCERNS / LEGIT`, not `PASS`, for two non-fatal adequacy/reporting limitations. First, the prompt says “digits” without an ASCII qualifier, while `digitStrings` admits only code points 48–57; both trusted canonical Python and submitted Python accept tested Arabic-Indic, full-width, and Devanagari decimal digits that the theorem excludes. Second, the final postcondition uses the proof-local opaque constructor `sentenceVal(N)` rather than a concrete `str(...)`; its exact-string meaning is supported by a separate successfully reconstructed sentence-expression claim and a guarded terminal abstraction, so it is sound, but the last interpretation step is modular/meta-level rather than a direct concrete-string postcondition.

All evidence cited below was reviewer-authored or freshly recorded. Candidate prose, compiled definitions, logs, traces, and caches were not trusted.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount `/reference/reference-semantics` is present. There is no mode/mount contradiction, so this is a candidate audit rather than an infrastructure error.

The required candidate sources and provenance files are regular, non-symlink files. No symlink exists anywhere under `/candidate`. Byte comparisons gave:

- `/candidate/prompt.py` = `/reference/prompt.py` (`cmp` exit 0).
- `/candidate/py2mpy.py` = `/reference/py2mpy.py` (`cmp` exit 0).
- `/candidate/reference-semantics/` = `/reference/reference-semantics/` recursively (`diff --no-dereference -qr` exit 0), with exactly 26 entries in each tree.
- There are no missing, additional, changed, mistyped, or symlinked entries in the candidate semantics tree.

The complete type, hash, size, and comparison record is in [stage1_integrity.log](/audit-output/evidence/stage1_integrity.log). Candidate-built `*-kompiled` trees and caches were deliberately not copied or used.

I read the untrusted provenance claims in `run-input.json`, `metrics.json`, `codex-last.txt`, and the 4,177,420-byte `codex-output.log`. They claim problem `113-odd-count`, generation condition `kit-semantics`, an exit-0 generation run, four `#Top` proofs, and two expected failures. These were treated only as claims. The structured trace is a valid 1,155-record JSONL stream spanning 2026-07-22T03:07:08.176Z through 04:02:24.193Z; [trace_summary.py](/audit-output/evidence/trace_summary.py) parsed every record, with results in [trace_summary.log](/audit-output/evidence/trace_summary.log).

The candidate's [PROOF.md](/candidate/PROOF.md:1) has several reporting inaccuracies that do not survive as audit evidence: it names a nonexistent `ODD-COUNT-CORRECT` label (the actual label is `odd-count`), shows command flags different from [prove.sh](/candidate/prove.sh:20), and calls the direction `sentenceVal(N) -> str(sentenceCodes(N))` a concretization even though the actual rule is the guarded forward abstraction `str(CS) => sentenceVal(N)` at [verification.k](/candidate/verification.k:132). The independent reconstruction below resolves the underlying facts.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt requires `odd_count(lst)` for a list of digit-only strings. For each string, it counts its odd digits and replaces every lowercase `i` in `the number of odd elements in the string i of the input.` by that count. The returned list preserves input order and length. The trusted canonical implementation computes `sum(int(d) % 2 == 1 for d in arr)` and constructs that sentence ([canonical.py](/reference/canonical.py:18)).

The submitted [solution.py](/candidate/solution.py:1) uses two explicit loops. It resets `count` for each string, adds `int(digit) % 2` for each character, appends the exact required sentence, resets three temporary locals, and returns `result`. On ASCII decimal characters, `int(digit) % 2` equals the canonical Boolean count. Empty lists and empty strings take the expected zero-iteration branches.

### Translation and K program identity

Using only the trusted translator copied from `/reference`, I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
```

Both commands together exited 0; the submitted and regenerated MPY files are byte-identical ([translation_identity.log](/audit-output/evidence/translation_identity.log)). I independently wrapped the regenerated MPY term as `solutionProgram`; it is byte-identical to the submitted [solution-program.k](/candidate/solution-program.k:1), including the one grammar-required normalization from `ListExpr()` to `ListExpr(.Exprs)` ([generate_program_wrapper.py](/audit-output/evidence/generate_program_wrapper.py), [program_wrapper_identity.log](/audit-output/evidence/program_wrapper_identity.log)). Thus the final K entry claim does not load a substituted program.

### Independent differential testing

[differential_audit.py](/audit-output/evidence/differential_audit.py) separately imports `/reference/canonical.py` and the scratch copy of the candidate entry point. It also uses an independently written oracle based on membership in `13579` and `template.replace("i", count)`. Its 13,942 cases comprise:

- both documented examples;
- empty list and empty string;
- all single digits, even-only, odd-only, leading-zero, repeated, multi-element, multi-digit-count, and long-string boundaries;
- every one-element input string of lengths 0 through 4 over `0`–`9` (11,111 strings);
- 820 Cartesian list cases of widths 0 through 3 over nine boundary strings;
- 2,000 deterministic generated lists with strings of lengths 0 through 30.

The run exited 0 with zero mismatches against both the canonical implementation and the independent oracle ([differential.log](/audit-output/evidence/differential.log)). This is finite bridge evidence, not a replacement for the K proof.

### Domain limitation

The formal guard `digitCodes` accepts only integer codes 48 through 57 ([verification.k](/candidate/verification.k:94)). In contrast, both Python implementations accept several unambiguously decimal, non-ASCII strings. The reviewer probe records equal Python results for `١٢٣`, `１２３４`, and `१२३४५`, while the formal guard is false in every case ([unicode_domain_probe.py](/audit-output/evidence/unicode_domain_probe.py), [unicode_domain_probe.log](/audit-output/evidence/unicode_domain_probe.log)). This does not make any proved conclusion false—the excluded inputs do not satisfy the K precondition—but it limits the bridge from the unqualified prompt wording to the theorem.

## 3. Clean proof reconstruction

I created `/tmp/audit-work/113-odd-count`, copied only candidate source artifacts needed for proof, copied the semantics from the trusted `/reference` tree, and generated all definitions anew. Source hashes are recorded in [scratch_source_hashes.log](/audit-output/evidence/scratch_source_hashes.log). The installed live toolchain is K v7.1.293 and Python 3.10.12 ([toolchain.log](/audit-output/evidence/toolchain.log)).

### Concrete reconstruction

The command below exited 0 and created `runtime-audit-kompiled` only in scratch:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

See [kompile_runtime.log](/audit-output/evidence/kompile_runtime.log). A reviewer-authored witness embeds the candidate function body byte-for-byte and asserts results for `[]`, `[""]`, `["2"]`, and `["1", "20", "13579"]`; body identity is recorded in [concrete_witness_body_identity.log](/audit-output/evidence/concrete_witness_body_identity.log). Trusted translation succeeded, and `krun concrete_witness.mpy --definition runtime-audit-kompiled --output none` exited 0 ([witness_translation.log](/audit-output/evidence/witness_translation.log), [krun_witness.log](/audit-output/evidence/krun_witness.log)).

### Positive symbolic proofs

Every positive module contains exactly one claim, so each command below independently exercised its entire target module. All definitions were compiled from scratch with the Haskell backend.

| Layer | Fresh definition command | Proof command | Result |
| --- | --- | --- | --- |
| Inner loop | `kompile --backend haskell verification.k --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX --output-definition inner-audit-kompiled` | `kprove spec.k --definition inner-audit-kompiled --spec-module INNER-SPEC` | exit 0, `#Top` |
| Sentence | `kompile ... --main-module VERIFICATION-SENTENCE-DEFINITION ... --output-definition sentence-audit-kompiled` | `kprove spec.k --definition sentence-audit-kompiled --spec-module SENTENCE-SPEC` | exit 0, `#Top` |
| Outer loop | `kompile ... --main-module VERIFICATION-OUTER-BASE ... --output-definition outer-audit-kompiled` | `kprove spec.k --definition outer-audit-kompiled --spec-module OUTER-SPEC` | exit 0, `#Top` |
| Final entry | `kompile ... --main-module VERIFICATION ... --output-definition verification-audit-kompiled` | `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC` | exit 0, `#Top` |

Exact commands, statuses, and outputs are in [kompile_inner.log](/audit-output/evidence/kompile_inner.log), [kprove_inner.log](/audit-output/evidence/kprove_inner.log), [kompile_sentence.log](/audit-output/evidence/kompile_sentence.log), [kprove_sentence.log](/audit-output/evidence/kprove_sentence.log), [kompile_outer.log](/audit-output/evidence/kompile_outer.log), [kprove_outer.log](/audit-output/evidence/kprove_outer.log), [kompile_final.log](/audit-output/evidence/kompile_final.log), and [kprove_final.log](/audit-output/evidence/kprove_final.log).

The only material compiler totality warning is in the fixed supplied semantics: `valSeqAt(_, _)` is declared total but has no empty-sequence equation. `Subscript`/`valSeqAt` is not syntactically used by this program or any proof extension, so it cannot contribute to these closures. Other displayed warnings are unused variables.

## 4. Adequacy and real-program pinning

### Plain-language meaning of each claim

1. `INNER-SPEC.inner-loop` ([spec.k](/candidate/spec.k:6)): if the remaining string code sequence `CS` consists of ASCII digits, executing the exact inner `for digit in digits` loop adds the number of odd codes in `CS` to the existing count and leaves `digit` as the final one-character string, or unchanged when `CS` is empty.
2. `SENTENCE-SPEC.sentence-expression` ([spec.k](/candidate/spec.k:37)): with local `count = N`, evaluating the exact nested concatenation expression reaches the abstract value `sentenceVal(N)`. The lower definition permits that abstract terminal only when the concrete result codes equal `sentenceCodes(N)`.
3. `OUTER-SPEC.outer-loop` ([spec.k](/candidate/spec.k:57)): from the real outer-loop iterator state, for a remaining sequence of ASCII digit strings, execution appends one appropriate `sentenceVal` per string to the existing result list, consumes the exact cleanup statements, resets the three temporaries, and resumes the framed continuation.
4. `SPEC.odd-count` ([spec.k](/candidate/spec.k:101)): from the supplied initial configuration, load `solutionProgram`, call its `odd_count` closure on any `INPUT` satisfying `digitStrings`, and return `ref(0)` with heap location 0 equal to `list(oddCountAppend(.ValSeq, INPUT))`, no exception, an empty call stack, and the expected post-call scope/allocation state.

### Satisfiable preconditions

Every claim has an explicit realizable witness. For the inner claim, take `CS = iCons(49, .IntSeq)`, `C = 0`, `PREV = .IntSeq`, an allocated empty result list, and the displayed standard scope; `digitCodes(CS)` reduces to true. For the sentence claim, take the same standard scope with `N = 1`. For the outer claim, take `VS = vCons(str(iCons(49, .IntSeq)), .ValSeq)`, `ACC = .ValSeq`, and the displayed cleanup continuation; `digitStrings(VS)` reduces to true. For the entry claim, the supplied initial configuration with `INPUT` encoding `["1"]` satisfies its guard. Empty-list and empty-string inputs are also admitted.

The stronger concrete entry witness [concrete-entry-witness.k](/audit-output/evidence/concrete-entry-witness.k) substitutes `["1", "20", "13579"]` and demands exactly `sentenceVal(1)`, `sentenceVal(0)`, and `sentenceVal(5)`. It built and proved with exit 0 and `#Top` ([concrete_entry_witness_build.log](/audit-output/evidence/concrete_entry_witness_build.log), [concrete_entry_witness_proof.log](/audit-output/evidence/concrete_entry_witness_proof.log)). Both Python implementations return the corresponding concrete sentences ([python_witness.log](/audit-output/evidence/python_witness.log)).

### Pinning and result constraint

The `<k>` cell executes `#loadAll(solutionProgram) ~> Call(Name("odd_count"), list(INPUT))`. `solutionProgram` was independently shown byte-identical to the trusted translation. `oddCountBody`, `outerBody`, `innerBody`, and `sentenceExpr` are exact aliases of the translated whole body and nested real fragments; the cleanup in the outer claim is exactly translated lines 42–44 of `solution.mpy`. The return is not free: `<k>` is fixed to `ref(0)`, heap location 0 is fixed to the calculated list, `heapLoc` advances exactly once, and `<exc>` remains `NoExc`.

Reviewer body sensitivity provides a second pinning check. [body-mutant.py](/audit-output/evidence/body-mutant.py) changes only the update to `count += 0`; its independently translated proof definition built successfully, but the claim demanding the correct result for `["1"]` exited 1 with `WarnStuckClaimState`, exposing `sentenceVal(0)` instead of `sentenceVal(1)` ([body_mutant_build.log](/audit-output/evidence/body_mutant_build.log), [body_mutant_proof.log](/audit-output/evidence/body_mutant_proof.log)).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and semantics boundary

[rule_inventory.md](/audit-output/evidence/rule_inventory.md), generated by [inventory_k.py](/audit-output/evidence/inventory_k.py), source-locates and reproduces every top-level declaration in the selected semantics, `solution-program.k`, `verification.k`, and `spec.k`: 236 syntax declarations, 718 rules, 5 contexts, 1 configuration, and 4 claims. Of these, the fixed supplied semantics contributes 227 syntax declarations, 695 rules, all 5 contexts, and the configuration; proof-local files contribute 9 syntax declarations, 23 rules (22 in `verification.k` and one exact program-wrapper equation), and 4 claims.

The supplied modules inventory is:

| Module/file | Syntax declarations | Rules | Relevance decision |
| --- | ---: | ---: | --- |
| `syntax.k` | 16 | 0 | Declares every AST construct used by `solution.mpy`. |
| `core.k` | 37 | 46 | Configuration, values, allocation, loading, sequencing, lookup, literals, and shared evaluators are used. |
| `iter.k`, `range.k` | 3 | 6 | Iterator declaration is used; range behavior is unreachable. |
| `operators.k`, `int.k`, `bool.k` | 1 | 39 | `+`, `%`, dispatch, truth/guards are used; unused cases cannot introduce a task answer. |
| `float.k` | 34 | 121 | Unreachable from all program/proof syntax on the guarded domain. |
| `str.k` | 5 | 28 | String iteration, ASCII literal codes, concatenation, and exact code sequences are used. |
| `set.k`, `tuple.k`, `dict.k` | 22 | 61 | Unreachable collection domains. |
| `list.k` | 5 | 27 | List allocation/iteration/append are used. |
| `subscript.k`, `comprehension.k` | 18 | 47 | Unreachable; includes the noted unused `valSeqAt` totality warning. |
| `methods.k` | 27 | 75 | Generic method layer is imported; only call routing to list `append` is reachable, whose rule is in `list.k`. |
| `controls.k` | 3 | 34 | Assignment, augmented assignment, `for`, cleanup sequencing, and iteration control are used. |
| `functions.k`, `call.k` | 7 | 36 | Function definition, binding, frame lifecycle, return, lookup, call order, builtin/type dispatch, and bound methods are used. |
| `builtins.k` | 38 | 137 | Used cases are `int(one ASCII digit)` and `str(Int)`; other builtin cases are unreachable. |
| `sort.k`, `assert.k`, `concrete.k` | 11 | 38 | Assert rules are imported but unreachable in positive proofs and are exercised only by the concrete witness; `concrete.k` is imported only by `MPY-KRUN`. Sorting is unreachable. |

Because this is `SUPPLIED_SEMANTICS`, the 695 byte-verified fixed rules define the selected language model rather than being candidate proof extensions. I nevertheless checked the complete inventory for answer encoding and imports: no trusted-semantics source contains `odd_count`, the requested sentence, `sentenceVal`, `oddDigits`, or `oddCountAppend` ([static_boundary_checks.log](/audit-output/evidence/static_boundary_checks.log)). Unused fixed rules have no syntactic path from this program. Relevant fixed rules preserve left-to-right strict evaluation, ordinary scope lookup, type-object binding of `int`/`str`, frame creation/removal, heap allocation, list mutation, loop control, and `NoExc` on the guarded path.

### Construct-to-rule map

| Submitted construct | Declaration/evaluation | State/control effect checked |
| --- | --- | --- |
| `Module`, `FuncDef`, `Params` | `syntax.k`; `#loadAll` in `core.k`; closure rule in `functions.k` | Binds the exact body as `odd_count` in module scope 0. |
| `Call(Name("odd_count"), ...)` | lookup in `core.k`; left-to-right `#evalArgs`; closure dispatch in `call.k` | Allocates frame 1, binds `lst`, preserves caller continuation, later pops frame. |
| `ListExpr()` | `list.k` | Allocates only result list at heap 0 and advances `heapLoc` to 1. |
| `Assign`, `Name`, `Int`, `Str` | strict syntax; `core.k`; `controls.k`; `str.k` | Locals are updated in current frame; literals are exact integers/ASCII code sequences. |
| Outer and inner `For` | strict iterable evaluation; `controls.k`; list/str `#iterNext` | Target binding precedes body, bodies run in order, and empty iterables take `#iterDone`. |
| `AugAssign(... "+", int(digit) % 2)` | strict RHS; lookup/call; `builtins.k`; `int.k`; `controls.k` | One-character guarded digit converts to `C-48`, Python modulo by 2 is added to existing count. |
| Nested output `BinOp("+", ...)` and `str(count)` | `seqstrict(2,3)`; call routing; `str.k`; `builtins.k` | Exact left-to-right string concatenation; no heap or exception effect on the guarded path. |
| `result.append(...)` | cooled `Attribute`; call dispatch; priority-40 list append | Mutates exactly the list at result reference `H`, appending one value. |
| Cleanup and `Return` | sequencing/assign rules; `functions.k` pop | Resets temporaries, returns the result reference, removes frame 1, restores scope location. |

### Every proof-local rule

The 23 proof-local rules are exhaustively decided as follows.

- Exact definitional aliases (5 rules): `solutionProgram`, `sentenceExpr`, `innerBody`, `outerBody`, and `oddCountBody`. Each is nullary, total, and its sole equation exactly reproduces the regenerated program or real subterm. They do not replace a different body.
- Mathematical/structural definitions (14 rules): `oddBit` (1), `oddDigits` (2 constructor cases), `oddCountAppend` (2), `lastDigit` (2), `digitCodes` (2), `digitStrings` (2), `codesOfVal` (string plus disjoint `owise`), and `sentenceCodes` (1). Constructor cases cover their declared domains, guards are disjoint or `owise`, and every recursive call descends on a finite `IntSeq` or `ValSeq`. `oddBit(C) = pyMod(C-48,2)` agrees with `int` and parity for guarded codes 48–57. `codesOfVal` maps nonstrings to empty only as a total default; every result-bearing use is under `digitStrings`/`isStr`. These are definitions, not oracles.
- Opaque value declaration: `sentenceVal(Int)` has no function/total attribute and no independent equations. It affects the final result, so it is not silently trusted: its only intended meaning is established through the next terminal bridge and the sentence auxiliary claim.
- Guarded terminal abstraction (1 rule): [verification.k](/candidate/verification.k:132) rewrites a terminal `str(CS)` to `sentenceVal(N)` only when `CS ==K sentenceCodes(N)` and the exact function scope is present. It changes only `<k>`, reads but does not change scopes, has no continuation in that module, and cannot fabricate a mismatching count/string pair.
- Inner operational bridge (1 rule, priority 40): [verification.k](/candidate/verification.k:152) pins the exact inner loop AST, current environment, local frame, lack of a module `int` shadow, and a builtin binding exactly equal to `typeV("int")`. It writes only `count` and `digit`; heap, control continuation, exceptions, allocation, return, and stack cells are framed. `INNER-SPEC` proves the same transition without importing this bridge.
- Sentence operational bridge (1 rule, priority 30): [verification.k](/candidate/verification.k:193) pins `E ==K sentenceExpr`, `count = N`, the local frame, lack of a module `str` shadow, and the exact builtin type. The expression is pure on this domain, and only its computation value is abstracted; other cells and the continuation are framed. `SENTENCE-SPEC` proves the bridge result using the lower terminal abstraction and real expression evaluation.
- Outer operational bridge (1 rule, priority 40): [verification.k](/candidate/verification.k:222) pins the real `#iterNext`/`#loopStep`, entire translated outer body, exact append argument, exact cleanup statements, local/result binding, heap entry, and both builtin bindings. It consumes precisely that control segment, appends `oddCountAppend(ACC, VS)`, and performs the cleanup's three resets. `OUTER-SPEC` proves this transition using only the already checked inner and sentence bridge layers.

There are no proof-local simplification rules, `functional` declarations, `concrete` rules, unguarded catch-all execution rules, or conflicting overlaps among proof-local priority rules. The only `owise` proof rule is the disjoint non-string branch of `codesOfVal`. Priorities merely make the three exact guarded bridges preempt the lower operational step at their pinned redexes; they do not broaden guards or assert equations.

I found no unsound candidate rule and therefore make no unsoundness allegation requiring a false-conclusion witness. The narrower evidence gaps are the ASCII domain restriction and the manually audited modular interpretation of `sentenceVal`; neither enables a false conclusion for a state satisfying the entry precondition.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. [fresh-vacuity.k](/audit-output/evidence/fresh-vacuity.k) calls the actual `solutionProgram` on `["2"]`, which satisfies `digitStrings`, but changes the result-constraining heap obligation from the true `sentenceVal(0)` to false `sentenceVal(1)`.

The mutation first built successfully:

```text
kprove fresh-vacuity.k --definition verification-audit-kompiled \
  --spec-module AUDIT-FRESH-VACUITY --dry-run
```

Exit was 0 ([fresh_vacuity_build.log](/audit-output/evidence/fresh_vacuity_build.log)). The real proof command then exited 1 with `WarnStuckClaimState`; its fully evaluated residual heap contains `list(vCons(sentenceVal(0), .ValSeq))`, which does not unify with the demanded `sentenceVal(1)` ([fresh_vacuity_proof.log](/audit-output/evidence/fresh_vacuity_proof.log)). This is the expected unmet obligation, not a parse error, missing import, timeout, or unrelated crash.

This mutation, the successful explicit positive witness, and the independent body mutation jointly show that the precondition is satisfiable, the heap/result obligation is reachable, the result is discriminating, and the real body matters.

## 7. Proven versus assumed accounting

### What the reconstructed proof establishes

Under the supplied K semantics and proof-local definitions, for every finite `ValSeq INPUT` whose members are `str` values containing only codes 48–57, execution of the exact trusted translation of submitted `odd_count` from the supplied initial configuration reaches normal return `ref(0)`. Heap 0 contains one `sentenceVal(N)` for each input string in order, where `N` is the structural sum of each code's ASCII numeric value modulo 2. The separately reconstructed sentence claim establishes that `sentenceVal(N)` represents exactly the concrete ASCII string obtained by inserting `Int2String(N)` into all four required positions. This is a partial-correctness result; malformed/out-of-domain behavior and a separate termination theorem are not claimed.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
| --- | --- | --- |
| Trusted prompt, canonical source, and translator mounts | Intent statement, differential oracle, Python-to-MPY identity | Explicitly authorized trusted inputs; prompt/translator candidate copies were byte-checked. |
| Byte-identical supplied semantics | All concrete and symbolic execution | The governing `SUPPLIED_SEMANTICS` boundary. It is intentionally a Python subset and ASCII string model; acceptable for the formal theorem, but the Unicode discrepancy causes the `CONCERNS` verdict. |
| K v7.1.293 frontend, LLVM/Haskell backends, SMT/rewrite engine, K builtin mathematics | Every compile, execution, and `#Top` | Ordinary unavoidable machine-checking trust boundary. Fresh builds and negative controls reduce process/evidence risk but do not verify K itself. |
| `Int2String`, `strToCodes`, integer and string builtins in supplied semantics | Exact sentence codes and digit conversion | Fixed semantics primitives, concretely exercised on boundary counts. No candidate rule redefines them. |
| `sentenceVal` representation and manual layer composition | Human-readable interpretation of final opaque values; outer/final bridge justification | Acceptable but visible proof abstraction. Exact guarded lower claim closes; there is no unconstrained oracle. K does not itself import the auxiliary claims as rewrite theorems, so identity of each proved transition and bridge was checked statically. |
| Ordinary arithmetic fact that `(code-48) mod 2` counts odd ASCII digits | Natural-language “odd digit” interpretation | True for the complete guarded domain 48–57; also supported, but not universally proved by, the independent differential run. |
| Trusted canonical function and reviewer oracle | Program/intent bridge on tested inputs | Finite empirical evidence only (13,942 ASCII cases); not used in place of `kprove`. |
| Host filesystem/process isolation | Provenance and clean-build claims | Sources were copied to `/tmp/audit-work`; all candidate compiled artifacts were excluded, and exact commands/statuses are preserved below `/audit-output/evidence`. |

### Gate assessment and verdict rationale

- Real-program soundness: pass. Exact body translation and wrapper identity hold; all bridge footprints and guards are sound; all lower claims and the final claim close; positive, false-result, and changed-body witnesses discriminate as expected.
- Intent adequacy: pass with limitation. The theorem computes the requested result on the conventional ASCII HumanEval domain, but the prompt's unqualified word “digits” and the broader actual Python behavior leave a concrete Unicode domain gap.
- Trust/evidence auditability: pass with limitation. Evidence is fresh and reproducible. The opaque result representation is justified by an exact lower claim, but its use in the final theorem requires the audited modular bridge rather than a direct concrete-string heap postcondition.

These limitations do not permit a false conclusion on any state satisfying `digitStrings(INPUT)`, do not bypass the submitted body, and do not make the proof vacuous. They warrant `CONCERNS`, not `FAIL`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
