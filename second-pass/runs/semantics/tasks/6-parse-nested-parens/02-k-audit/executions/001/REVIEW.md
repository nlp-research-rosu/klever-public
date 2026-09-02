# Independent adversarial review: 6-parse-nested-parens

Decision: **FAIL / NOT_LEGIT**.

The submitted K claims reconstruct successfully and are non-vacuous, but they do not execute or load the submitted `solution.mpy`. The entry claim calls a proof-local synthetic closure whose body is copied into `verification.k`. A direct body-sensitivity test replaced `solution.py`/`solution.mpy` with a function that always returns `[999]`; after a fresh Haskell rebuild, the unchanged claims still exited 0 with `#Top`. Thus the successful proof is about the copied closure, not the real generated program. This is exactly the substituted-program failure in the decision boundary.

There is also a source-contract discrepancy: the submitted Python emits zero-valued groups for an empty string and for leading, trailing, or repeated spaces, while the trusted canonical implementation ignores empty split fields. This discrepancy occurs on inputs admitted by the K claim's `parenInput` precondition.

All reviewer work was done under `/tmp/audit-work`; `/candidate` was only read. Reviewer-authored artifacts and bounded logs are under `/audit-output/evidence`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. `/reference/reference-semantics` is present, so the trusted mounts are consistent with that mode; this is not an infrastructure breach.

The recursive candidate-versus-reference semantics comparison exited 0. Both trees contain one top-level `semantics.k`, the `semantics/` directory, and the same 23 regular helper files. No entry in the candidate semantics tree is a symlink or a non-file/non-directory object. There are no missing, additional, or changed entries. Candidate `prompt.py` and `py2mpy.py` are also byte-identical to the trusted mounted versions. Hashes, types, and exact comparison commands are in `evidence/01-integrity.log`.

Required provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace or candidate `PROOF.md` is present. The candidate does contain untrusted auxiliaries `prove.sh`, `concrete_tests.py`, `concrete_tests.mpy`, and a `__pycache__`; none was treated as proof evidence or reused as a build cache.

The scratch source copy and complete copied-file listing are in `evidence/00-scratch-copy.log`. No candidate-compiled definition was present or copied. The reconstruction uses a fresh copy of the trusted reference semantics, not a candidate cache.

Stage result: semantics/prompt/translator integrity passes; provenance completeness fails because the four named records are absent. This incompleteness is not the basis of the legitimacy verdict.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt describes a string containing space-separated groups of parentheses and requires one output integer per group: the greatest parenthesis nesting depth. The trusted canonical function implements this by splitting on ASCII space, discarding empty fields, scanning every nonempty group, and returning each maximum depth. The documented example maps:

`"(()()) ((())) () ((())()())"` to `[2, 3, 1, 3]`.

The submitted implementation instead scans the whole character stream. It appends the current maximum at every space, resets its state, then unconditionally appends once more after the loop. It agrees on nonempty groups separated by exactly one space, but it materializes empty fields as zeros.

The trusted translator regenerated `solution.mpy` byte-for-byte: both submitted and regenerated files are 970 bytes with SHA-256 `afa6188c96fbcb733382af9864858d7c1c591c354d8f577c2acaa1aa148b246f`. See `evidence/02-translation-identity.log`.

### Independent differential execution

`evidence/differential_test.py` independently imports `/reference/canonical.py` and the submitted `solution.py`; it does not reuse proof equations. Its deterministic 98-input set includes:

- the documented example;
- empty, space-only, leading/trailing/doubled-separator cases;
- every submitted branch boundary, including maximum update/no-update;
- unbalanced boundary strings and an out-of-alphabet diagnostic;
- every balanced group with one through four pairs;
- every ordered pair of balanced groups with one through three pairs, joined by one space.

The complete inputs and per-input outputs are in `evidence/differential-inputs.json` and `evidence/differential-results.tsv`. The exact command is in `evidence/03-differential.log`. It exited 1 because it deliberately returns nonzero on a mismatch. There were 93 matches and five mismatches:

| Input | Trusted canonical | Submission |
|---|---:|---:|
| `""` | `[]` | `[0]` |
| `" "` | `[]` | `[0, 0]` |
| `" ()"` | `[1]` | `[0, 1]` |
| `"() "` | `[1]` | `[1, 0]` |
| `"()  ()"` | `[1, 1]` | `[1, 0, 1]` |

All generated nonempty balanced inputs with single separators matched. The boundary discrepancies are nevertheless material to the formal theorem because `parenInput` admits all five.

Stage result: translation fidelity passes; implementation-to-canonical fidelity fails on admitted empty/spacing boundaries.

## 3. Clean proof reconstruction

The audit used K version `v7.1.337` and Python 3.10.12 (`evidence/20-environment.log`).

The clean source tree is recorded in `evidence/04-rebuild-source-setup.log`. It contains the candidate's source `spec.k` and `verification.k`, the regenerated/checked submitted sources, and a fresh trusted semantics tree. It initially contains no `*-kompiled` or `__pycache__` directory.

Fresh builds:

- LLVM concrete definition: exit 0, `evidence/05-kompile-llvm.log`.
- Haskell proof definition: exit 0, `evidence/06-kompile-haskell.log`.

The compiler reported fixed-semantics warnings about several non-exhaustive total functions and unused variables. None of the warned functions (`mapStrVS`, float conversions, `joinCodes`, or `valSeqAt`) occurs in this program or its proof-local equations.

Positive proof runs:

- `SPEC.parse-loop` alone: exit 0 and `#Top`, `evidence/07-kprove-parse-loop.log`.
- Complete `SPEC` containing the loop claim and entry claim: exit 0 and `#Top`, `evidence/09-kprove-all-claims.log`.

The entry claim relies on the loop claim as its circularity. As an extra diagnostic, selecting only `SPEC.parse-nested-parens` removed that auxiliary claim and produced no prover output for about three minutes; the auditor interrupted it with status 130 (`evidence/08-kprove-entry-alone.log`). That timeout is not treated as a candidate failure or as infrastructure evidence; the complete intended proof run closes both positive claims.

The fresh LLVM definition also executed reviewer-authored assertions over a function AST identical to submitted `solution.py`. Normal, empty, leading/trailing/double-space, and maximum-no-update cases all passed under K; see `evidence/k_concrete_tests.py`, its generated `.mpy`, and `evidence/10-k-concrete-tests.log`.

Stage result: the candidate's stated theory reconstructs successfully. Reconstruction success alone does not establish real-program pinning.

## 4. Adequacy and real-program pinning

### Claims in plain language

`parse-loop` assumes:

- the front of `<k>` is the supplied semantics' real `#loop` over a semantic string suffix `S`, targeting `char` and using proof-local `parseLoopBody`;
- frame 1 contains a result reference at heap location 0 plus current `depth`, `maximum`, and `char`;
- `S` contains only character codes 40 (`(`), 41 (`)`), and 32 (space);
- return/exception/exit cells are normal.

It concludes that the loop is consumed, `depth` and `maximum` equal the corresponding mathematical scan projections, heap list 0 contains all completed group maxima, and `char` is the last consumed character (or its old value for an empty suffix). The arbitrary continuation and stack are framed.

`parse-nested-parens` assumes a clean module-level configuration and any finite semantic string `S` satisfying the same three-character alphabet predicate. It calls `parseNestedParensClosure` directly and concludes that execution returns `ref(0)`, allocates exactly one list at heap location 0, stores `parsedParens(S)` in that list, restores the caller frame, and raises no exception.

Both preconditions are satisfiable. An entry witness is `S = .IntSeq`. A loop witness is `S = .IntSeq`, `D = 0`, `M = 0`, `VS = .ValSeq`, `OLD = str(.IntSeq)`, `INPUT = str(.IntSeq)`, and `ST = .List`. For the entry witness, `parenInput(.IntSeq) = true` and `parsedParens(.IntSeq) = vCons(0, .ValSeq)`.

The destination is result-constraining: the returned reference is fixed to 0, the heap sequence is fixed to `parsedParens(S)`, the heap counter is fixed to 1, and the control/state cells are fixed. There is no free result variable, tautological implication, or unconstrained oracle in the postcondition.

Closed substitutions are in `evidence/15-ground-witnesses.log`. The formal scan and submitted Python agree on every recorded satisfying input. For the documented input all three results are `[2,3,1,3]`. For `S = ""`, the formal result and submission are `[0]` while canonical Python returns `[]`; leading and doubled spaces have analogous discrepancies.

### Pinning failure

The entry `<k>` cell is:

`Call(parseNestedParensClosure, str(S))`

It is not `#loadAll(Module(...))`, does not contain submitted `solution.mpy`, does not execute its `ImportFrom` or `FuncDef`, and does not look up the `"parse_nested_parens"` binding. `verification.k` defines:

- `parseLoopBody` as a copied AST fragment;
- `parseFunctionBody` as a copied function body;
- `parseNestedParensClosure` as `closureVal("paren_string", parseFunctionBody, 0)`.

The copied body is textually equal to the original submitted translation, but that equality is outside the reachability theorem. There is no bridge-free auxiliary claim that loads the submitted module and connects its actual binding/body to the synthetic closure.

The direct sensitivity witness is conclusive:

1. `evidence/solution-body-mutant.py` returns `[999]` for every input; its trusted translation is `evidence/solution-body-mutant.mpy`.
2. On the documented satisfying input, Python confirms the mutant result is `[999]` (`evidence/11-body-mutation-setup.log`).
3. The original and mutant MPY hashes differ, while the proof sources are byte-identical.
4. A fresh Haskell build exits 0 (`evidence/12-body-mutation-kompile.log`).
5. The unchanged complete proof still exits 0 with `#Top` (`evidence/13-body-mutation-kprove.log`).

This is not an allegation that the transparent equation defining a newly named constant is mathematically false. It is the narrower, witnessed defect that the proof substitutes that constant for the real artifact and therefore cannot establish a conclusion about changes to the submitted program.

Stage result: **fail**. The proof does not pin the real generated program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` produced the source-located exhaustive inventory `evidence/k-rule-inventory.tsv` and counts in `evidence/k-rule-inventory-summary.json`. Across the assembled supplied semantics, helpers, `verification.k`, and `spec.k`, it records:

- 237 syntax declarations;
- 713 rules;
- 5 contexts;
- 1 configuration;
- 2 claims.

Of the rules, 695 belong to the trusted supplied-semantics tree selected by the rendered condition, and 18 are candidate-local rules in `verification.k`. The inventory includes every function/total/concrete/owise/priority/symbol/no-evaluators attribute and every declaration block. Searches found no `functional` declaration and no simplification rule. The candidate adds no local priority, concrete, simplification, functional, symbol, or no-evaluators attribute.

The supplied 695 rules are fixed by the problem's trusted semantics boundary, not candidate proof extensions. Each is marked accordingly in the inventory. I checked the configuration, import graph, and the complete operational slice used by this program; unused modules cannot be reached by any submitted construct. No candidate-versus-reference change exists from which to derive a semantics-integrity defect.

The 25 supplied symbolic/opaque declarations are enumerated in `evidence/19-opaque-symbol-inventory.log`: float operations/conversions, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None occurs in `solution.mpy`, `verification.k`, or `spec.k`, so none affects control, state, or result here.

Every candidate-local declaration and every one of its 18 rules has an individual domain, overlap/coverage, classification, assessment, and dependent in:

- `evidence/verification-declaration-review.tsv`
- `evidence/verification-rule-review.tsv`

The local mathematical rules pass equation-level review:

- `parenMax` has disjoint exhaustive guards `A > B` and `A <= B`.
- `scanParens` has disjoint empty, `(`, `)`, space, and `owise` cases and structurally decreases the `IntSeq`.
- `scanDepth`, `scanMaximum`, and `scanValues` are truthful projections after `scanParens` normalizes to `scanDone`.
- `finalChar` has disjoint empty/cons cases and structurally decreases.
- `parsedParens` exactly describes the copied algorithm, including its unconditional final append.
- `parenInput` is an exhaustive structurally decreasing alphabet predicate.

There are no overlapping contradictory local equations, non-descending recursions, proof-local opaque values, or task-answer rules that bypass the copied body's execution. The illegitimate element is the copied program substitution described in Stage 4, not a false scan equation.

### Used construct and state/control audit

`evidence/solution-construct-map.tsv` maps every submitted MPY construct to its syntax and operational rules. The relevant fixed-semantics path covers:

- `Module` loading and statement sequencing;
- generic no-op `ImportFrom("typing", "List")`;
- `FuncDef`, closure creation, parameter binding, call frame allocation, `Return`, and frame pop;
- RHS strictness, `Name` lookup, assignments, integer/string/list literals;
- single-evaluation `For`, string iteration, target binding, and the `#loop` continuation;
- left-to-right comparison/call argument evaluation;
- integer `+`, `-`, and `>`;
- list allocation and in-place `append`;
- branch selection, expression-result discard, heap allocation, and escaping returned references.

The synthetic closure itself executes these fixed rules faithfully: it allocates frame 1, allocates result list 0, iterates the string, mutates that list, returns `ref(0)`, removes the callee frame, restores `env = 0` and `scopeLoc = 1`, and preserves the returned heap object. The loop claim matches the real synthetic control head `#loop(str(S), Name("char"), parseLoopBody)` and its actual heap/scope layout. Its arbitrary `INPUT` and `ST` values are harmless because the loop body reads neither the original parameter nor stack.

The full submitted module path, however, includes module loading, the typing import, real `FuncDef`, and name lookup. Those constructs are absent from the entry theorem. The manual closure constant has no complete-context connection theorem proving equivalence to that path. The body mutation supplies the required concrete false-connection witness.

Stage result: local mathematics and the used fixed-semantics slice are sound for the synthetic closure; real-program substitution is a material adequacy failure.

## 6. Fresh non-vacuity test

The reviewer-created mutation is `evidence/spec-vacuity.k`. It keeps the loop invariant unchanged but changes the entry destination from:

`list(parsedParens(S))`

to:

`list(vCons(999, parsedParens(S)))`.

This is demonstrably false at the satisfying input `S = .IntSeq`: the copied body returns `[0]`, while the mutated destination requires `[999, 0]`.

- Setup/hash log: `evidence/16-vacuity-setup.log`.
- Parse/build dry run: exit 0, `evidence/17-vacuity-dry-run.log`.
- Actual proof: exit 1, `evidence/18-vacuity-kprove.log`.

The failure is the expected `WarnStuckClaimState`, not a parser/import/backend error. Its residual shows the actual heap sequence and the unmet equality between that sequence and the same sequence prefixed by `999`.

Stage result: pass. The reconstructed synthetic-closure theorem is non-vacuous and discriminates a false result.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Conditional on the trusted supplied MPY semantics and the transparent proof-local equations, the complete reachability run establishes partial correctness of the synthetic closure:

For every finite `IntSeq S` containing only codes 40, 41, and 32, if `closureVal("paren_string", parseFunctionBody, 0)` is called from the claim's clean configuration and terminates, it returns `ref(0)` with heap object 0 equal to the proof-local scan `parsedParens(S)`, with the stated restored control cells and no exception. The auxiliary theorem establishes the corresponding suffix-processing invariant for the synthetic `#loop`.

It does **not** establish that:

- `solution.mpy` was loaded or its function binding was called;
- the current contents of `solution.py`/`solution.mpy` agree with `parseFunctionBody`;
- `parsedParens` equals the trusted canonical function over the whole formal precondition;
- the natural-language contract holds for empty or repeated/edge-space inputs;
- any candidate generation report or prior trace is accurate.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted `py2mpy.py` | Source-to-MPY identity | Acceptable trusted input; byte identity was independently checked. |
| Supplied reference semantics | All operational behavior | Acceptable condition-selected trust boundary; candidate tree is exactly identical. |
| K built-in Int/Bool/String/Map/List theories and K v7.1.337 prover/backend | Arithmetic, equality, collections, reachability closure | Ordinary machine-checking trust boundary. |
| Proof-local `parenMax`, scans, projections, and predicates | Entire stated result | Transparent, terminating equations; exhaustively reviewed. No opaque local symbol. |
| Manual equality of `parseFunctionBody`/`parseLoopBody` to the submitted MPY | Claimed bridge from synthetic closure to real program | **Illegitimate as a proof bridge.** It is not expressed or proved in K; the body-mutation witness shows the reachability proof is insensitive to the artifact. |
| Canonical-versus-submission differential evidence | Intent/implementation bridge on 98 inputs | Finite evidence only. It finds five admitted boundary divergences and cannot establish universal equivalence. |
| Supplied opaque float/sort/MD5 symbols | None in this theorem | Inactive and therefore harmless here; complete names are in `evidence/19-opaque-symbol-inventory.log`. |
| Termination | Whether partial correctness yields an observed result | Not a theorem conclusion in this review; the claims are reported as partial correctness. |
| Missing generation logs/metrics/trace | Provenance auditability | Concerning process gap, but not used as evidence and not needed for the decisive pinning witness. |

The false-result mutation shows that the synthetic theorem is genuinely result-constraining. It cannot cure the independent body-sensitivity failure: non-vacuity of a theorem about a substituted body is not a proof of the real program.

The decisive verdict therefore does not rely on a timeout, compiler warning, missing log, or infrastructure uncertainty. It relies on a successful, freshly rebuilt proof that remains successful after a concrete material change to the submitted program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
