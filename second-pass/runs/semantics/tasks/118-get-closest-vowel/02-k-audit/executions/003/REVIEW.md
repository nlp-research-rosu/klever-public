# Independent adversarial audit: 118-get-closest-vowel

The candidate's positive proof commands reconstruct successfully, and the entry
claims do pin the submitted function body. The proof is nevertheless not
legitimate. Its central recursion rule replaces every nested application of the
program-defined function with the desired `closestVowelSpec` result. That rule
is the theorem being sought, not a derived induction principle or a proved
execution summary. A body-sensitivity mutation demonstrates the defect
concretely: fixed execution returns `"X"` for `"bab"`, while the extended proof
still proves the false result `"a"` and prints `#Top`.

There is also an independent real-program adequacy failure. The source contract
does not bound word length, but the submitted recursive CPython implementation
raises `RecursionError` on sufficiently long English-letter strings while the
canonical implementation returns normally. The supplied K semantics and proof
idealize recursion as unbounded.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, `semantics_mode = SUPPLIED_SEMANTICS`, and the mounted
paths used in this audit. I inspected the launcher records through those
container paths, not the host provenance strings.

The following required records are present, regular/readable where applicable,
and valid JSON or JSONL:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the structured trace at
  `/generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T05-13-04-019f8e76-e4af-7df2-bb94-04a04b05b8cc.jsonl`;
- optional legacy `usage.json`, `legacy-metrics.json`, and
  `legacy-run-input.json`.

Runtime metrics are not required for this legacy-selected-stage1 layout.
`/audit-campaign-lock.json` exactly equals the `audit_campaign` object in
`/audit-input.json`, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All recorded regular-file hashes checked by the reviewer match. Every mounted
file was also independently SHA-256 hashed and every entry type/link target
inventoried. The trace contains 363 valid JSON events, its only file has the
recorded SHA-256, and no linked trace entry exists.

The supplied-semantics boundary is intact. `/reference/reference-semantics`
exists as required. Recursive comparison found the candidate's
`reference-semantics/` to have exactly the same paths, entry types, and file
bytes as the trusted tree: no missing, additional, changed, mistyped, or
symlinked entry. The candidate has no symlink anywhere. Candidate `prompt.py`
and `py2mpy.py` are byte-identical to their trusted mounts, and the canonical,
prompt, translator, record, generation-log, and usage hashes match the launcher
record.

The generation report's `KPROVE_PASSED` and its prose were treated only as
untrusted historical claims. There is no infrastructure breach. Reproducible
checks and exact results are in
[stage1_integrity.py](/audit-output/evidence/stage1_integrity.py) and
[stage1_integrity.log](/audit-output/evidence/stage1_integrity.log), with the
complete mounted-file manifest in
[mounted_file_hashes.log](/audit-output/evidence/mounted_file_hashes.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

For an English-letter string, return the rightmost vowel that is neither the
first nor last character and whose immediate neighbors are both consonants.
Matching is case-sensitive in the sense that the returned character preserves
case. Return `""` when no such vowel exists.

The trusted canonical function scans interior indices from right to left. The
candidate uses a recursive equivalent in the idealized model: solve `word[1:]`
first, propagate a nonempty answer, otherwise test the original indices
`0,1,2`.

Trusted regeneration with

`python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy`

exited 0. `cmp` against submitted `solution.mpy` exited 0; both files have
SHA-256
`6ffc5212ff003b36c8f23490a4fbc4ce1967a453b6ef4d40d261bf4fe138a6b6`.

### Independent differential result

The independent test imports the trusted canonical and generated entry points.
Its 8,919 preserved cases cover all prompt examples, lengths 0 through 3, all
strings over branch-sensitive alphabet `abEyZ` through length 5, 5,000
seeded ASCII-letter strings of length 0 through 128, and patterned strings
through length 2,003. The exact input sequence has SHA-256
`e0f54029a09e7b3d22ae3890bb48f500e55d52f0e99fd05ff2960809afa17d48`.

All cases on which both functions returned had zero value mismatches. There
were, however, 15 generated-side `RecursionError` exceptions across the
recursion-boundary cases; the canonical function returned normally. English
letter strings at those lengths satisfy the stated input contract. This is a
material source-contract and intended-execution mismatch, not a testing
failure. The corpus and exact run are
[differential_inputs.txt](/audit-output/evidence/differential_inputs.txt),
[differential_test.py](/audit-output/evidence/differential_test.py), and
[stage2_fidelity.log](/audit-output/evidence/stage2_fidelity.log). The earlier
bounded zero-mismatch run is retained separately as
[stage2_fidelity_bounded.log](/audit-output/evidence/stage2_fidelity_bounded.log).

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`; no
candidate-built definition or cache was copied or used. The toolchain reports K
v7.1.293.

Fresh reconstruction performed:

1. trusted translation of a reviewer-authored concrete assertion program;
2. LLVM compilation from trusted supplied semantics under `MPY-KRUN`;
3. concrete execution of empty, one-character, two-character, lower/upper
   qualifying, nonqualifying, and rightmost-choice inputs;
4. fresh Haskell compilation of `verification.k`;
5. the candidate's combined spec;
6. each of the four positive claims in a separate reviewer spec module.

LLVM execution exited 0 in a final configuration with `.K`, `NoExc`, empty
stack, and exit code 0. The Haskell definition compiled successfully. The
combined target and all four separate claim commands exited 0 and printed
`#Top`. Compiler non-exhaustiveness/unused-variable warnings are recorded but
did not prevent reconstruction.

The reviewer script records every exact command and exit status in
[stage3_rebuild.sh](/audit-output/evidence/stage3_rebuild.sh) and
[stage3_rebuild.log](/audit-output/evidence/stage3_rebuild.log).

This stage establishes closure under the candidate's extended theory. It does
not establish that the extension is a sound proof of the program.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

The four claims share a fully initialized module configuration: environment 0,
the exact `get_closest_vowel` closure in scope 0, trusted builtins at scope -1,
fresh scope/heap counters, empty heap and stack, `noRet`, `NoExc`, and exit code
0.

1. Empty `IntSeq` input returns the empty string.
2. Every one-code input returns the empty string.
3. Every two-code input returns the empty string.
4. Every input with at least three codes returns
   `closestVowelSpec` of exactly the input code sequence.

The domain is actually broader than the source contract: the code variables
range over all mathematical integers, not only English ASCII letters. On
nonletter integers the spec treats every code other than the ten vowel codes as
a consonant. This breadth does not narrow the HumanEval domain.

The return values are constrained constants or a deterministic recursively
defined function of the input; they are not free variables, tautologies, or
one-way implications. Every cell shown on the right remains constrained by the
claim's frame.

### Program identity

The entry state directly supplies the closure instead of executing the outer
`Module(FuncDef(...))`. That is acceptable only if its closure body is the
submitted body. I extracted the translated body and the verification macro,
normalized only the two surface spellings of the empty `Stmts` list, parsed
both independently with `kast`, and compared KORE. `cmp` exited 0; both KORE
terms have SHA-256
`2a23c032ae0d9e9549f8bf65d69f4a06ff681bbdb062c72efee103381b658e04`.
Together with trusted byte-identical regeneration, this mechanically pins the
same function name, parameter, and constructor body. See
[stage4_pinning.log](/audit-output/evidence/stage4_pinning.log).

The used constructor mapping is:

| Program constructor | Fixed-semantics declaration/behavior |
|---|---|
| `Module`, statement lists | `syntax.k:56,61`; `core.k:124-127` |
| `FuncDef`, closure, parameter binding | `syntax.k:53`; `functions.k:14-20,63-75` |
| `Call`, callee/argument order, closure frame | `syntax.k:28`; `core.k:185-191`; `call.k:18-32,69-75` |
| `Name` and builtins lookup | `syntax.k:12`; `core.k:129-181` |
| `len` on strings | `builtins.k:17-26` |
| `If` and truthiness | `syntax.k:49`; `core.k:198-205`; `controls.k:50-54` |
| `Assign` | `syntax.k:41`; `controls.k:8-18` |
| `Return` and frame restoration | `syntax.k:50`; `functions.k:77-90` |
| integer/string literals | `syntax.k:9,13`; `core.k:193-196`; `str.k:12-17` |
| compare and short-circuit `and` | `operators.k:14-20`; `int.k:22-27`; `bool.k:13-25` |
| string membership | `str.k:28-41` |
| string index and `[1:]` slice | `subscript.k:16-23,25-69,71-121` |

Concrete satisfying witnesses are `""`, `"a"`, `"ab"`, `"bab"`, and
`"yogurt"`. Reviewer entry claims for these inputs print `#Top`, and both
Python implementations respectively return `""`, `""`, `""`, `"a"`, and
`"u"`. Exact code sequences and results are in
[ground_compare.py](/audit-output/evidence/ground_compare.py) and
[stage4_pinning.log](/audit-output/evidence/stage4_pinning.log).

The program term is therefore pinned and the postcondition is result-bearing.
The defect is that a proof-local operational rule bypasses material execution
inside that pinned body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule_inventory.md](/audit-output/evidence/rule_inventory.md) inventories all
26 relevant K files line by line: the trusted `semantics.k` tree, candidate
`verification.k`, and candidate `spec.k`. It contains 955 entries: 232 syntax
declarations, 713 rules, 5 contexts, 1 configuration, and 4 claims. It also
indexes every `total`, macro, strictness, priority, simplification, `symbol`,
and `no-evaluators` occurrence. There is no local `functional` declaration.

The trusted supplied semantics contributes 928 entries. Its 25 opaque/external
symbol declarations concern float operations, sorting, and MD5. None is
reachable from this program or its postcondition. The fixed rules used here
implement ordinary left-to-right call evaluation, lexical lookup, frame
allocation/restoration, return control, string operations, and branching.
Review of their guards, priorities, cells, and overlaps found no task-specific
answer rule or used opaque oracle. Unused modules remain inside the declared
trusted supplied-semantics boundary and do not contribute to claim closure.

Candidate `verification.k` contributes exactly 5 syntax declarations and 18
rules:

| Inventory entries | Classification and finding |
|---|---|
| K0929-K0930 `getClosestBody` | Syntax macro/definitional alias. Its expanded constructor term is mechanically identical to the submitted body. Sound. |
| K0931-K0932 `isVowelCode` | Total definitional function. The ten integer equalities are exactly the upper/lower ASCII vowels. Guards and coverage are complete. Sound. |
| K0933-K0934 `qualifyingTriple` | Total definitional function: nonvowel, vowel, nonvowel. Sound. |
| K0935-K0942 `closestVowelSpec` | Total recursive definitional summary. Base overlaps all agree on `.IntSeq`; long-input guards split between a nonempty tail result and an empty tail result, then between qualifying and nonqualifying triples. Recursion descends one constructor. On algebraic ground `IntSeq` values it returns only empty or singleton and implements the rightmost choice. Sound as mathematics. |
| K0943 `[1:]` rule | Operational bridge. For a nonempty immutable string, fixed `subscript.k` does yield `str(R)` and has no observable state/control effect. The rule's arbitrary continuation is compatible with that pure slice. The candidate supplies no bridge-free universal connection theorem, so this is an evidence gap under the validation contract, but I found no false value witness and do not label this rule unsound. |
| K0944-K0945 `vowelCodes` | Macro expanding to the exact code sequence for `"AEIOUaeiou"`. Sound. |
| K0946 singleton `strContains` | Definitional acceleration. For a singleton pattern and the exact vowel code sequence, fixed prefix/substring recursion equals `isVowelCode(C)`. Sound. |
| K0947 nested `#applyK` | Illegitimate theorem-encoding operational bridge. Detailed below. |
| K0948-K0950 length simplifications | `IntSeq` structural length is nonnegative, so each inequality rewrite is ordinary integer mathematics. Sound. |
| K0951 fresh map update | Under `N not in_keys(BASE)`, K map update equals adjoining the fresh binding. Sound. |

The `closestVowelSpec` overlaps at lengths 0, 1, and 2 have identical right
sides. Its three long rules have disjoint conditions. The two priority-40
program rules preempt fixed slice/call execution. No candidate opaque symbol is
declared.

### Decisive failure: K0947

At `/candidate/verification.k:87-93`, K0947 matches

`#applyK(toCall(closureVal("word", getClosestBody, 0)),
(str(CS), .Vals))`

under any continuation, whenever the current `<env>` is any positive integer.
It rewrites directly to `str(closestVowelSpec(CS))`.

Fixed semantics would instead:

1. allocate a callee scope and increment `scopeLoc`;
2. push a continuation frame and change `env`;
3. bind `word`;
4. execute the complete program body, including further recursion;
5. set/reset `ret`, pop the stack, delete the callee scope, restore `env` and
   `scopeLoc`, and resume the continuation.

K0947 reads the closure, argument, and `env`, but omits and preserves
`scopes`, `scopeLoc`, `stack`, `ret`, heap, exception, and exit cells. Its guard
does not state that the call is the strictly smaller recursive call, does not
identify an active frame of this function, and does not establish any invariant
or decrease. More importantly, its result is exactly the same
`closestVowelSpec` used by the final postcondition. There is no bridge-free
universal connection theorem proving that execution of `getClosestBody`
returns this result. Thus the rule assumes the program-derived fact the entry
claim is supposed to prove.

The fresh operational-sensitivity witness changes the base case inside
`getClosestBody` from `Return(Str(""))` to `Return(Str("X"))`. This changes the
program term actually stored in the entry closure and matched by K0947; it does
not merely alter an unused external source file. On the intended-domain input
`"bab"`:

- CPython execution of the mutated function returns `"X"`;
- execution under the trusted, bridge-free LLVM semantics satisfies assertions
  that the result is `"X"` and not `"a"`;
- the freshly compiled extended proof nevertheless proves the concrete false
  claim that the result is `"a"` and prints `#Top`;
- it also proves the universal long-input claim and prints `#Top`.

This is the required false-conclusion witness. The bridge fabricates the empty
summary for the nested two-character call, so the outer execution selects
`"a"` without executing the mutated base case. Exact artifacts and output are
[operational_sensitivity_mutation.patch](/audit-output/evidence/operational_sensitivity_mutation.patch),
[spec-mutant-false.k](/audit-output/evidence/spec-mutant-false.k),
[operational_sensitivity.sh](/audit-output/evidence/operational_sensitivity.sh),
and
[operational_sensitivity.log](/audit-output/evidence/operational_sensitivity.log).

The witness does not assert that the original function happens to compute a
wrong value on `"bab"`; it demonstrates that the proof extension has imported
that correctness conclusion and is insensitive to the program-defined
computation it claims to summarize. Consequently the reconstructed `#Top` is
not a derivation of the result from the real program body.

## 6. Fresh non-vacuity test

I created a distinct reviewer mutation for the original body and original
definition: on the satisfiable input `"bab"`, change the correct postcondition
from `"a"` to `""`.

`kprove ... --dry-run` exited 0, demonstrating that the mutation and imports
build. The actual proof exited 1 with `WarnStuckClaimState`. Its residual
contains

`str ( iCons ( 97 , .IntSeq ) )`

which is `"a"`, and reports that this term does not unify with the false
destination and cannot be rewritten further. This is the expected unmet result
obligation, not a parser error, timeout, missing import, or unrelated crash.

The exact mutation, commands, exit statuses, and residual are in
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k),
[stage6_nonvacuity.sh](/audit-output/evidence/stage6_nonvacuity.sh), and
[stage6_nonvacuity.log](/audit-output/evidence/stage6_nonvacuity.log).
Non-vacuity passes, but result sensitivity cannot make the theorem-encoding
K0947 sound.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the supplied semantics plus all candidate rules, an entry call in the
four exact initialized configurations reaches the specified string. For
lengths at least three, this is a theorem of an *extended transition system in
which every nested call to the exact program closure in a positive-numbered
environment is already axiomatized to return `closestVowelSpec`*. Therefore
the machine result is conditional on essentially the desired correctness
theorem and is not a partial-correctness proof derived from real recursive
execution.

### Trust ledger

| Boundary or assumption | Influence | Assessment |
|---|---|---|
| Trusted supplied MPY semantics | All syntax, control, cells, builtins, strings, and calls | Required fixed boundary; candidate copy is exact. Relevant rules were reviewed. |
| Trusted `py2mpy.py` | Program constructor identity | Acceptable; byte-identical regeneration and KORE body comparison succeed. |
| K integer, Boolean, string, map, list, and equality hooks | Mathematical evaluation and state maps | Ordinary low-level K trust boundary. |
| Fixed opaque float/sort/MD5 symbols | None | Present in imported semantics but unused by program, summary, guards, and result. |
| `closestVowelSpec`, `isVowelCode`, `qualifyingTriple` | Final result | Truthful recursive mathematics with complete relevant equations; acceptable as a postcondition definition, not as a substitute for program execution. |
| K0943 slice bridge | Recursive argument value | Likely truthful for its exact pure slice, but lacks the validation contract's bridge-free universal theorem; nonfatal by itself. |
| K0947 nested-call bridge | Recursive result, outer branch, and final return | Illegitimate and decisive. It assumes the desired program-derived value; the false `"bab"` body-mutation witness proves operational insensitivity. |
| Finite differential and concrete testing | Python equivalence and semantic examples only | Reproducible empirical evidence, never a substitute for the K proof. It also exposes the recursion-limit counterexample. |
| Unbounded recursion in MPY versus CPython recursion limit | Termination/exception behavior on long contract inputs | Material language-model and real-program adequacy gap. The proof excludes CPython `RecursionError` without an input-length precondition. |

Gate A (real-program soundness) fails because of K0947, even though the A5
false-postcondition check passes. Gate B (intent adequacy) also fails for
unrestricted real CPython execution because of the recursion-limit
counterexamples. Gate C evidence is reproducible and clearly scoped, but it
cannot rescue failed soundness. Under the benchmark's decision boundary, the
candidate relies on an execution-bypassing, answer-encoding proof rule and does
not contain a legitimate proof of the requested real program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
