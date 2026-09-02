# Independent adversarial review: 158-find-max

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted translated program over arbitrary finite modeled lists
of strings. I rebuilt every definition from source, obtained fresh `#Top`
results for the loop and whole-entry claims, mechanically matched the program
term in the entry claim to trusted translator output, and made a fresh false
tie-result claim fail at the expected return value.

The proof is not awarded an unqualified `PASS`. Its two proof-local symbolic
dispatch rules are true guarded restatements of the fixed string-constructor
rules, but the candidate's connection claims cover only the explicit
`str(CS)` constructor. My fresh attempt to prove the connection over the
rules' complete symbolic `V:Val` plus `isStr(V)` match domain compiled but
stuck. The compiled definition establishes that `isStr` is exactly true for
an injected `Str` and false otherwise, and `str(IntSeq)` is the only `Str`
constructor, so there is no false-conclusion witness and I do not classify
the rules as unsound. The missing complete machine-checked connection theorem
is nevertheless a real auditability/trust-boundary limitation.

## 1. Input and provenance integrity

`/audit-input.json` is readable and declares:

- problem `158-find-max`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- the launcher container paths used in this review.

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` exists. The required pipeline-v3 records are
all readable: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured trace. The one trace file contains 639 valid
JSONL records. The generation output, last message, trace, and candidate
reports were treated only as untrusted historical claims.

The audit campaign block in `/audit-input.json` is structurally equal to
`/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the recorded value. All launcher-recorded singleton hashes checked
in `evidence/stage1_integrity.log` match, including the canonical,
prompt, translator, run/task/result records, generation records, and trace
file.

Using the pipeline's published tree-hash algorithm against the mounted
inputs produced:

- candidate:
  `8493aee4dabd466c4cad8c7a27b666162f1228a05e3f0ae6bd6f163973569fc4`,
  equal to `/generation-result.json`'s workspace hash;
- candidate supplied semantics:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- trusted supplied semantics: the same
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  equal to `/task.json`'s input hash; and
- generation trace:
  `c6315539ae233af1a533cc655d22fafba952a382c44cdb5b333f8955aaf12cec`,
  equal to `/generation-evidence/usage.json`'s source-trace hash.

See `evidence/launcher_tree_hashes.log`.

Independent byte/type checks found:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`;
- recursive `diff -qr --no-dereference` between the candidate and trusted
  semantics trees exits 0;
- independent per-entry semantics manifests are byte-identical, with digest
  `e29e166cd3d4c8cfef2c70156872dd9b4ab5a855c6ce17c8a65e0d58e5129d6c`;
  and
- the candidate tree and both semantics trees contain no symlinks.

The complete reviewer candidate manifest is
`evidence/candidate_tree.manifest.tsv`; the semantics manifests and commands
are in `evidence/semantics_tree_manifest.*`. Required candidate proof
artifacts are regular files. There is no infrastructure breach.

## 2. Program fidelity and canonical comparison

### Source contract

`/reference/prompt.py:2` requires `find_max(words)` to accept a list of
different strings and return the string having the largest number of distinct
characters, breaking score ties by lexicographically smallest string. The
trusted canonical at `/reference/canonical.py:16` implements the ordered key
`(-len(set(x)), x)` and takes element zero. That indexing makes a nonempty list
an effective precondition of the canonical implementation, even though the
prose does not state it explicitly.

`/candidate/solution.py` keeps a current result and distinct-character score,
scans every word, and replaces the current result precisely for a larger score
or for an equal score with a lexicographically smaller word. Initial score
`-1` guarantees that the first word wins. This is a different but equivalent
algorithm on nonempty lists of strings.

### Trusted translation

In a clean scratch copy I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

using the trusted translator. It exited 0, and `cmp` against the submitted
`solution.mpy` exited 0. Both files have SHA-256
`238028ce6473ad33a825cfc4e1330d7fd8df42af559496d7f0a0e1f6761ceb9f`.
Commands and output are in `evidence/stage2_program_fidelity.log`.

### Independent differential test

`evidence/differential_test.py` imports the trusted canonical and scratch
candidate as separate modules. It covers all documented examples, the empty
boundary, one empty word, score increase/decrease, both lexicographic tie
directions, Unicode/code-point cases, a 500-character boundary, all
permutations of a small word pool up to length four, and 750 deterministic
generated distinct-word lists.

The run exited 0:

```text
total_cases=1863
nonempty_cases=1862
nonempty_mismatches=0
empty_divergences=1
```

The sole divergence is explicit: on `[]`, the canonical raises `IndexError`
while the candidate returns `""`. Because the canonical itself makes the
maximum problem undefined on that boundary, this is extra candidate behavior
outside the effective nonempty source domain, not domain narrowing. The
formal theorem includes this extra case. Complete inputs/results are preserved
in `evidence/differential_cases.json`.

## 3. Clean proof reconstruction

`evidence/prepare_scratch.sh` created
`/tmp/audit-work/reconstruct-001` and copied only candidate source proof
artifacts, the trusted prompt/canonical/translator, and the trusted semantics
tree. The pre-build check found no `*-kompiled` directory. No
candidate-provided definition or cache was used. The live toolchain reports K
7.1.293.

The exact clean commands and exit statuses are in
`evidence/stage3_status.log`.

1. LLVM compilation of trusted `reference-semantics/semantics.k` with
   `MPY-KRUN`/`MPY-SYNTAX` exited 0.
2. A reviewer-authored translated concrete test program executed through that
   definition and exited 0 with `.K`, `NoExc`, and exit code 0. It covers all
   essential branch directions plus empty-list/empty-string behavior. See
   `evidence/concrete_reconstruction.py` and
   `evidence/stage3_krun_concrete.log`.
3. Fresh Haskell compilation of `verification.k` exited 0.
4. The isolated `SPEC.loop-inv` proof exited 0 and printed `#Top`
   (`evidence/stage3_kprove_loop.log`).
5. The full `SPEC` proof, containing both the loop and entry claims, exited 0
   and printed `#Top` (`evidence/stage3_kprove_all.log`).
6. A separate Haskell definition importing only fixed semantics for the
   candidate's connection claims compiled successfully. Both constructor
   connection claims exited 0 and printed `#Top`, with
   `WarnTrivialClaim` because they simplify directly by the fixed equations
   (`evidence/stage3_kprove_connection.log`).

The positive proof reconstruction therefore passes. Compiler warnings concern
unused variables or total functions in unused supplied-semantics modules; none
changes a positive exit or the reachable program slice.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-inv` at `/candidate/spec.k:6` starts at the exact fixed-semantics
`#loop` head for an arbitrary remaining `ValSeq`. Its precondition says every
remaining value is a direct modeled string and says the accumulated `BEST` is
also a non-reference string. It threads:

- the best word through `bestWord`;
- its score through `bestScore`;
- the final loop-target value through `lastWord`; and
- the final score temporary through `lastScore`.

It removes the completed loop and preserves the pinned function/module scope,
original `words` binding, empty heap, arbitrary continuation and stack, return
state, exception state, and exit code.

`SPEC.find-max` at `/candidate/spec.k:85` loads the submitted module, registers
the exact `find_max` closure, resolves and calls it with an arbitrary unboxed
modeled list `list(WORDS)`, executes its body, returns, and pops the frame. Its
only precondition is `allStrings(WORDS)`. The destination is not a free
variable: the returned `<k>` value must equal
`bestWord(WORDS, str(.IntSeq), -1)`, and all explicitly present observable
cells must reach the normal caller state.

The domain is unbounded in list length and modeled string length. Requiring
neither distinctness nor nonemptiness proves a superset of the effective
source domain; it does not exclude a material source case.

### Mechanical program identity

`evidence/extract_claim_program.py` reads the actual `SPEC.find-max`
`#loadAll(Module(...))` term from scratch `spec.k`, balances its parentheses,
and removes only explicit `.Exprs`/`.Stmts` unit spellings. `kast` parsed both
that extracted term and trusted-regenerated `solution.mpy` to KORE under the
fresh LLVM definition. `cmp` exited 0; both KORE files have SHA-256
`59cde9d6459be00c9ad738b7609466369e3d9494fe3697f224e9bc40d96f4f0b`.
See `evidence/stage4_program_pinning.log`. The loop claim repeats the same loop
body and closure body visible in the entry term.

### Satisfiable witnesses and result substitution

For `WORDS = ["ba", "ab"]`, `BEST = ""`, and initial score `-1`, both entry
and loop preconditions are satisfiable. Reviewer claims machine-check that the
formal predicates reduce to true and that the formal result fold reduces to
`"ab"`; `kprove` exits 0 with `#Top`
(`evidence/stage4-witness-spec.k`,
`evidence/stage4_witness_kprove.log`). Both trusted canonical Python and
candidate Python return `"ab"` on the same input
(`evidence/stage4_witness_python.log`).

The body-sensitivity test changes `max_unique` from `-1` to `100` inside the
actual `Module` term loaded by the K claim and inside its registered closure;
it does not merely edit an external source file. Keeping the original expected
result for `["a"]` makes the proof exit 1 with `WarnStuckClaimState` and a
residual empty-string return. See `evidence/audit-body-sensitivity.k` and
`evidence/stage4_body_sensitivity_*`. The theorem is sensitive to its executed
body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` scanned 28 K source files total: all 24 files in the
trusted semantics tree plus `verification.k`, `spec.k`, and the two connection
sources.
`evidence/k_inventory.tsv` enumerates every source-level syntax declaration,
configuration, context, rule, and claim with location, full normalized text,
and attributes. `evidence/static_rule_review.tsv` gives an assessment for
every rule and claim.

The inventory contains:

- 237 syntax declarations;
- 716 rules (695 fixed-semantics and 21 proof-local);
- 4 claims;
- 5 contexts; and
- 1 configuration.

It separately identifies 117 `[total]` declarations/statements, zero explicit
source `[functional]` declarations, 23 `no-evaluators` declarations, 45
priority rules, and 7 simplification rules. K generates functional axioms for
function symbols in compiled KORE; the zero count refers only to explicit
source attributes. Per-file counts and every opaque declaration appear in
`evidence/k_inventory_summary.md`.

No fixed-semantics source contains `find_max`, `bestWord`, `uniqueCount`, or
another task-specific answer. Because the candidate semantics tree is
byte/type-identical to the trusted supplied tree, all fixed rules belong to
the selected immutable model. The exact reachable slice is mapped in
`evidence/used_construct_map.md`: module load/sequencing, scope lookup,
unannotated closure call/return, assignment, list iteration and `for`, integer
operations, short-circuit `and`/`or`, string-set deduplication and length, and
lexicographic code-sequence comparison.

Reachable priority rules either implement normal call/control behavior or are
provably inapplicable to the unboxed read-only list, direct strings, empty
heap, and unannotated closure pinned by the claim. Fixed opaque float, sort,
MD5, keyed-sort, dictionary, and method symbols are unreachable. The fixed
string literal converter is ASCII-limited, but the only source literal in
this program is `""`; symbolic external inputs enter directly as arbitrary
`str(IntSeq)` values.

### Proof-local declarations and rules

All 21 rules in `/candidate/verification.k` were checked:

1. `definedProjectStr`, the `#Ceil` rule, and the guarded
   `projectStrTotal` orientations express the generated `Val :> Str`
   projection. The compiled definition has a total/functional `isStr`,
   a true rule exactly for injected `Str`, and an `owise` false rule
   (`evidence/stage5_isstr_kore.log`). `projectStrTotal` is intentionally
   unconstrained off this guard, but every result-bearing target use is under
   `allStrings` or an explicit best-string guard.
2. `codesOf(str(CS)) = CS` is exhaustive because `str(IntSeq)` is the only
   `Str` constructor. `allStrings` has disjoint empty/cons cases and
   structurally descends.
3. `uniqueCount` composes fixed `dedupCodes` and `isLen`.
   `candidateWins` exactly mirrors the translated score and tie condition.
4. `bestWord`, `bestScore`, `lastWord`, and `lastScore` have disjoint
   empty/cons cases and structurally descend on the tail. Their equations
   agree with the assignments and branch in the real loop.
5. No proof-local rule rewrites a `<k>` control context, returns from the
   function, discards a continuation, changes a scope/heap/stack cell, or
   bypasses the program-defined body.

The two guarded simplification rules at `/candidate/verification.k:36` and
`:41` broaden fixed constructor equations to a symbolic `Val` satisfying
`isStr`. Their state footprint is empty; their result affects the score and
tie branch. On the overlap `V = str(CS)`, projection and `codesOf` reduce to
`CS`, so each right-hand side is identical to the fixed rule. Pairwise
overlaps with projection-collapse/idempotence rules also agree.

The candidate's `connection-spec.k` proves only:

- `applyBuiltin("set", str(CS), .Vals)` gives the fixed deduplicated set; and
- `applyCmp("<", str(A), str(B))` gives fixed `strLt(A,B)`.

Those claims are true but trivial constructor equations. To test the complete
bridge domain, I created `evidence/audit-dynamic-connection.k`, which imports
fixed semantics and independently justified projection helpers but omits both
candidate dispatch rules. Compilation succeeds. The universal claims over
`V:Val` guarded by `isStr(V)` fail with a genuine
`WarnStuckClaimState`; fixed semantics cannot constructor-split the symbolic
value from that predicate
(`evidence/stage5_kprove_dynamic_connection.log`).

This failure is an evidence gap, not an unsoundness witness. There is no
ground or symbolic false conclusion admitted by either rule: the compiled
`isStr` equations and the sole `Str` constructor exhaust the guard, and the
constructor equations agree. Per the audit requirement, I do not label a rule
unsound without a false-conclusion witness. The limitation prevents a clean
validation `PASS` because the complete machine-checked connection theorem
required by the Kit contract is absent.

## 6. Fresh non-vacuity test

I did not rely on `/candidate/spec-vacuity.k`. The fresh mutation
`evidence/audit-false-mutation.k` executes the exact submitted program on the
satisfying, distinct-string input `["ba", "ab"]` but changes the required
return to the false tie winner `"ba"`.

The exact command is recorded in
`evidence/stage6_false_mutation_status.log`. It parses and runs against the
fresh verification definition, exits 1, and reports
`WarnStuckClaimState`. The residual `<k>` value is
`str(iCons(97, iCons(98, .IntSeq)))`, namely the correct `"ab"`, while the
destination requires `"ba"`. The failure is therefore the expected unmet
result obligation, not a parser error, timeout, import failure, or unrelated
crash. The proof is non-vacuous and discriminates the lexicographic tie case.

## 7. Proven versus assumed accounting

### What the proof establishes

Under the supplied K model and proof-local equations reviewed above, for every
finite modeled `ValSeq` whose elements are direct `str(IntSeq)` values: if the
translated `find_max` call terminates normally from the pinned initial
configuration, its returned value is the structural fold that selects the
word with maximum deduplicated-code count and, on equal count, the
lexicographically least code sequence. Normal scope/call cleanup, empty heap,
empty stack, `noRet`, `NoExc`, and exit code 0 are also constrained by the
entry claim. This includes every nonempty list of distinct modeled strings
required by the source contract and additionally covers duplicates and the
candidate's empty-list return.

It is a partial-correctness result. A separate liveness theorem is not proved.

### Trust and evidence ledger

| Boundary | Influence | Assessment/evidence |
|---|---|---|
| Supplied `reference-semantics` | Defines values, evaluation order, lookup, call/return, iteration, `set`, length, and lexical comparison. | Authorized fixed model and byte/type-identical to the trusted mount. Reachable rules are mapped statically and exercised concretely. |
| K 7.1.293 parser, compiler, Haskell/LLVM backends, and solver | All parses, execution, and proof closure. | Metatheoretic trusted implementation. Versions and complete fresh command logs are preserved. |
| Trusted `py2mpy.py` | Connects candidate Python AST to `solution.mpy`. | Byte-verified trusted input; fresh output is byte-identical to the submission. |
| Generated `isStr` and partial subsort-cast law; proof-local total projector | Refines symbolic `Val` inputs so fixed string operations can be summarized. | Constructor-exact and no false witness; compiled KORE confirms its cases. Complete bridge-free dynamic connection did not prove, so this is the principal concern. |
| Modeled `IntSeq` string versus CPython `str` | Connects code deduplication and integer-code lexical order to the HumanEval wording. | Straightforward code-point interpretation and 1,862 nonempty canonical differential cases, including Unicode; finite testing is supporting evidence, not a universal theorem. |
| Unboxed read-only `list(WORDS)` at the external call boundary | Represents a Python input list without heap allocation/aliasing. | Explicitly admitted by the fixed semantics for claim inputs. This program never mutates the argument, so no observable alias behavior is omitted. |
| Termination | Conditions the partial-correctness conclusion. | Structurally evident for finite source lists/strings and observed concretely, but not a separate proved liveness property. |

The Python differential test is not substituted for the K proof. It supports
only candidate-versus-canonical fidelity and the model-to-CPython bridge. The
K proof itself supplies the unbounded list/string theorem.

### Gate and decision summary

- Real-program soundness/result constraint: passes by source review,
  constructor-exhaustive reasoning, clean `#Top`, satisfying witnesses, body
  sensitivity, and the fresh false-result rejection. The complete automated
  dynamic connection sub-obligation remains an evidence limitation.
- Intent adequacy: passes. There is no fixed-size bound or material
  source-domain restriction.
- Trust/evidence auditability: limited by the unclosed full-guard connection
  theorem and the informal modeled-string/CPython bridge.

These limitations are non-fatal because they do not permit a demonstrated
false conclusion, do not narrow the HumanEval domain, and do not replace or
bypass execution of the submitted body. They justify `CONCERNS / LEGIT`
rather than `PASS / LEGIT`; none meets the benchmark's `FAIL / NOT_LEGIT`
conditions.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
