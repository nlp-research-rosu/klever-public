# Independent adversarial review: 153-Strongest-Extension

## Overall determination

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program under the supplied K model. The proof is unbounded over
all finite strings and all finite lists of strings representable as the model's
`IntSeq`/`ValSeq` values, pins the exact translated function body, and constrains
the returned string to the first extension with maximal score.

The result is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
read-only supplied semantics defines upper- and lower-case characters as ASCII
code-point ranges. CPython's predicates are Unicode-aware. The candidate did
not introduce this restriction, proves every string/list value admitted by the
fixed model, explicitly records the boundary and the `Ω` witness in
`/candidate/PROOF.md:174`, and its Python source behaves correctly under
CPython on that witness. This is the documented supplied-model behavior gap
covered by campaign amendment v2.

All execution and mutation work used the clean scratch tree
`/tmp/audit-work/153-strongest-extension`. Candidate caches and compiled
definitions were not copied or used. Reviewer-authored sources and command
logs are in [`evidence/`](/audit-output/evidence).

## 1. Input and provenance integrity

`/audit-input.json` declares `pipeline-v3`, problem
`153-Strongest-Extension`, condition `kit-semantics`,
`SUPPLIED_SEMANTICS`, and a required reference-semantics mount. The mount
`/reference/reference-semantics` is present, so the rendered mode and trusted
mount agree.

I read all launcher-required records for this layout: `/run.json`,
`/task.json`, `/generation-result.json`, the invocation, generation/runtime
metrics, usage, last message, output log, generation prompt, and the complete
structured trace. The single JSONL trace contains 1,039 valid records:
1 session record, 317 event messages, 715 response items, 2 world states,
3 turn contexts, and 1 compaction record. These records were treated only as
untrusted history.

The independent provenance checker in
[`provenance_check.py`](/audit-output/evidence/provenance_check.py) establishes:

- the campaign-lock JSON equals the campaign block and its SHA-256 is
  `053ed73c...dadd01`, exactly the recorded value;
- every required pipeline-v3 record is readable, and every individually
  recorded SHA-256 for the run, task, result, invocation, metrics, runtime
  metrics, usage, last message, output log, generation prompt, canonical,
  trusted prompt, and translator matches the mounted bytes;
- the direct trace-file hash matches the hash in `generation-result.json`;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts;
- a recursive entry-type and per-file-content comparison of the candidate and
  trusted `reference-semantics/` trees is identical across all 26 entries;
- there are no symlinks below the candidate, reference, or generation-evidence
  mounts; and
- all required source proof artifacts are regular files.

The checker also records independent reviewer tree manifests and the
launcher-recorded aggregate hashes without treating either hashing convention
as a substitute for the direct recursive comparison. Full command, hashes,
trace counts, and exit status 0 are in
[`01_provenance.log`](/audit-output/evidence/01_provenance.log). There is no
provenance or audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted docstring says to score each extension name as the number of
uppercase letters minus the number of lowercase letters, select the strongest,
choose the first on a tie, and return
`ClassName.StrongestExtensionName`. Both documented examples determine those
behaviors. It does not specify what to do with an empty extension list.

The candidate source at `/candidate/solution.py:1`:

- initializes no winner with `best_strength = None`, which correctly permits
  a first extension with a negative score;
- counts each one-character iteration using `isupper()` and, otherwise,
  `islower()`;
- updates only on strict `>`, preserving the first extension on ties; and
- returns the required dotted concatenation.

For a single Python character, the canonical test
`isalpha() and isupper()/islower()` and the candidate's direct case predicates
produce the same contribution. The different algorithm is therefore faithful.
On an empty list, the candidate returns `class_name + "."` while canonical
raises `IndexError`; this input is underdetermined by the docstring, and the
candidate's total extension is defensible.

Running the trusted `/reference/py2mpy.py` on the candidate Python source
produced a byte-for-byte identical `solution.mpy`; see
[`02_translation_identity.log`](/audit-output/evidence/02_translation_identity.log).

The independent differential program
[`independent_differential.py`](/audit-output/evidence/independent_differential.py)
loaded the trusted canonical and candidate entry points. It exercised both
documented examples, empty strings, an empty list, negative scores, all three
case categories, greater/equal/less update boundaries, Unicode, and 10,000
deterministically generated nonempty cases. There were zero candidate/canonical
or candidate/doc-oracle mismatches on the 10,015 nonempty cases. The empty-list
difference was observed and classified as underdetermined.

The same test provides the concrete model-gap witness:
`("Gap", ["", "Ω"])`. CPython candidate and canonical both return
`"Gap.Ω"`; the supplied model's ASCII score makes the two extensions tie and
selects `"Gap."`. Inputs, outputs, and exit status 0 are preserved in
[`02_independent_differential.log`](/audit-output/evidence/02_independent_differential.log).

## 3. Clean proof reconstruction

The scratch tree contains fresh copies only of source artifacts. I built new
LLVM and Haskell definitions with K 7.1.293 and did not use the candidate's
`*-kompiled` directories, archive, log, or caches. Tool versions are recorded
in [`03_tool_versions.log`](/audit-output/evidence/03_tool_versions.log).

For concrete reconstruction, I translated the independent directed program
[`concrete_reconstruction.py`](/audit-output/evidence/concrete_reconstruction.py),
built the trusted supplied semantics with the LLVM backend, and ran it. The
execution ended with `.K`, `NoExc`, and exit code 0. Evidence:

- [`03_concrete_translate.log`](/audit-output/evidence/03_concrete_translate.log)
- [`03_llvm_build.log`](/audit-output/evidence/03_llvm_build.log)
- [`03_concrete_krun.log`](/audit-output/evidence/03_concrete_krun.log)

I then built three clean Haskell definitions in dependency order: the base
connection definition, the definition containing the already-checked inner
bridges for the outer connection, and the final target definition. All builds
exited 0:

- [`03_build_connection.log`](/audit-output/evidence/03_build_connection.log)
- [`03_build_outer_connection.log`](/audit-output/evidence/03_build_outer_connection.log)
- [`03_build_target.log`](/audit-output/evidence/03_build_target.log)

Every positive claim was run individually. Each command exited 0 and printed
`#Top`:

| Definition level | Claim | Evidence |
|---|---|---|
| fixed semantics plus pure definitions | projection identity | [`03_prove_connection_projection.log`](/audit-output/evidence/03_prove_connection_projection.log) |
| fixed semantics plus pure definitions | yield connection | [`03_prove_connection_yield.log`](/audit-output/evidence/03_prove_connection_yield.log) |
| fixed semantics plus pure definitions | inner-loop connection | [`03_prove_connection_inner.log`](/audit-output/evidence/03_prove_connection_inner.log) |
| after importing checked inner/yield bridges | outer-loop connection | [`03_prove_outer_connection.log`](/audit-output/evidence/03_prove_outer_connection.log) |
| final target | inner loop | [`03_prove_target_inner.log`](/audit-output/evidence/03_prove_target_inner.log) |
| final target | outer loop | [`03_prove_target_outer.log`](/audit-output/evidence/03_prove_target_outer.log) |
| final target | empty entry | [`03_prove_target_entry_empty.log`](/audit-output/evidence/03_prove_target_entry_empty.log) |
| final target | nonempty entry | [`03_prove_target_entry_nonempty.log`](/audit-output/evidence/03_prove_target_entry_nonempty.log) |

The projection proof emits a trivial-claim warning because the same
proof-local datatype simplifier normalizes it. It is not accepted on that
warning alone; its rule-level justification and an opposite probe are covered
in stage 5.

## 4. Adequacy and real-program pinning

The four target claims mean:

- `inner-loop`: in the exact seven-local function frame, scanning any finite
  model string adds its character score to `strength`, and leaves `character`
  as the final visited one-character string (or unchanged for an empty
  string).
- `outer-loop`: once `best_strength` is an integer, scanning any finite
  all-string tail updates the winner, score, last extension, last character,
  and last strength according to the explicit structural folds.
- `entry-empty`: for any model string `class_name`, loading and calling the
  submitted function with an empty list returns `class_name + "."`.
- `entry-nonempty`: for any model string `class_name`, any first model string,
  and any finite all-string tail, loading and calling the submitted function
  returns `class_name + "." + first_maximum_extension`.

The entry claims start with `#loadAll(Module(FuncDef(...)))`, create the
function binding through the fixed loader, resolve it, and make a real call.
They also fix the initial environment, scopes, allocator state, heap, stack,
return, exception, and exit-code cells. The right-hand `<k>` value is the
computed `expectedResult`, not a free variable, implication, or unconstrained
oracle.

For mechanical pinning, I independently formed
[`claimed_program.mpy`](/audit-output/evidence/claimed_program.mpy) from the
claim's `FuncDef` and `STRONGEST-BODY`. `kast --expand-macros --output kore`
gave it and regenerated `solution.mpy` the same 8,206-byte KORE term and SHA-256
`c1c6f7...`; `cmp` exited 0. This is constructor-level identity after macro
expansion, not a textual resemblance. See
[`04_program_pinning_kast.log`](/audit-output/evidence/04_program_pinning_kast.log).

The entry preconditions are satisfiable. Independent witnesses include the
empty input with class `.IntSeq`, and class `"C"` with first extension `"a"`
and tail `["B"]`; the latter's claimed and Python result is `"C.B"`.
[`claim_witnesses.py`](/audit-output/evidence/claim_witnesses.py) and
[`04_claim_witnesses.log`](/audit-output/evidence/04_claim_witnesses.log)
preserve these substitutions.

A body-sensitivity mutation replaced the function body actually loaded by the
claim with `Return(Str("wrong"))`. The changed definition built successfully,
but the original result obligation reached a stuck state and `kprove` exited 1.
This changes the executed claim term itself, not an unused external file:

- [`04_build_body_mutation.log`](/audit-output/evidence/04_build_body_mutation.log)
- [`04_body_mutation_proof.log`](/audit-output/evidence/04_body_mutation_proof.log)

Thus the proof pins the real regenerated program and is result-constraining.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I read every line of the supplied `semantics.k` and its helper K files, and
every candidate K source. The complete line-addressed inventory is
[`05_rule_inventory.log`](/audit-output/evidence/05_rule_inventory.log);
the generating reviewer script is
[`inventory_k.py`](/audit-output/evidence/inventory_k.py). It records file
hashes and full blocks for every `requires`, module/import, syntax declaration,
configuration, context, rule, and claim, including attributes.

Across the supplied tree and all candidate K artifacts, including candidate
mutation files that are not imported by the positive target, the inventory
contains 35 modules, 263 syntax declarations, 1 configuration, 5 contexts,
807 rules, and 12 claims. Attribute counts include 175 `function`, 122
`total`, 26 `no-evaluators`, 28 `symbol`, 51 `priority`, 29 `owise`, 12
`simplification`, 62 `concrete`, 3 `preserves-definedness`, 7 `macro`, and
1 `macro-rec`. The unimported mutation/spec-vacuity artifacts have no path
into the successful theorem.

### Used-construct coverage

Every constructor in the submitted `solution.mpy` has both a syntax
declaration and a material execution path:

| Program construct | Supplied declaration/execution rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `semantics/syntax.k`; `core.k` `#loadAll`; `functions.k` closure creation |
| `Call`, arguments, return | `call.k` callee and left-to-right argument machinery, closure frame rules; `functions.k` return/pop |
| `Name`, `Int`, `Str`, `NoneVal` | `core.k` lookup and literal rules |
| `Assign`, `AugAssign` | `controls.k` local writes and rewrite through `BinOp` |
| `For`, list iteration, string iteration | `controls.k` `#loop/#loopStep`; `list.k` and `str.k` `#iterNext`; target binding rules |
| `If` | `controls.k` truth evaluation and branch selection |
| short-circuit `or` | `bool.k` contexts and truthy/falsey continuation rules |
| `is`, integer `>`, integer `+/-` | `operators.k` and `int.k` |
| attribute method calls | `call.k`/attribute dispatch; `methods.k` `isupper` and `islower` |
| string `+` | `operators.k` dispatch and `str.k` `seqConcat` |

The fixed configuration accounts for `<k>`, environment/scopes, allocation
and heap, call stack, return, exception, and exit status. Call frames and local
writes preserve evaluation order and state. The program performs no mutable
container update; list/string inputs are iterated, and string concatenation
constructs the returned value.

### Supplied rules

The candidate's entire `reference-semantics/` is byte- and type-identical to
the trusted read-only tree. Its many rule families unrelated to this program
(floats, dicts, sets, sorting, comprehensions, slicing, and other builtins) are
inert here. The used fixed rules have ordinary deterministic roles described
above. Their overlaps are resolved by their fixed sorts, guards, `owise`, and
priorities.

The one material model limitation is in `semantics/methods.k`: `isUpperC`
recognizes 65--90 and `isLowerC` recognizes 97--122. This is internally
consistent with the theorem's `charStrength`; it is not CPython's Unicode
classification. A bridge-free exact-program claim under the trusted semantics
for `("Gap", ["", "Ω"])` proves the fixed result `"Gap."`, independently
confirming the divergence:

- [`reviewer-pinning.k`](/audit-output/evidence/reviewer-pinning.k)
- [`model_gap_spec.k`](/audit-output/evidence/model_gap_spec.k)
- [`05_build_reviewer_pinning.log`](/audit-output/evidence/05_build_reviewer_pinning.log)
- [`05_prove_model_gap.log`](/audit-output/evidence/05_prove_model_gap.log)

### Candidate definitions and rules

The three `INNER-BODY`, `OUTER-BODY`, and `STRONGEST-BODY` rules are macros:
they expand to the exact translated syntax and add no alternate execution
semantics.

The mathematical helpers are structural computations, not answer axioms:

- `charStrength` has three disjoint and exhaustive guarded ASCII cases;
  `extensionStrength` and `lastCharacter` recurse on a strictly smaller
  `IntSeq`.
- `isStringVal` and `allStrings` are exact constructor predicates.
- `bestCodes` and `bestScore` split on strict `>` versus its Boolean negation,
  descend the `ValSeq`, and retain the earlier winner on equality.
- `lastExtension`, `lastStrength`, and `lastCharacterAcross` exactly summarize
  the source locals and descend the tail.
- `expectedResult` adds the dot and, for nonempty input, uses the first
  extension as the initial winner and score.

The guarded projection layer deserves special scrutiny. `Str` has the sole
constructor `str(IntSeq)` in the fixed model. `projectStrTotal` and
`codesProject` expose that constructor only when `isStringVal` is true;
`codesProject` remains opaque outside that domain. Every result-bearing use is
guarded by `isStringVal` or `allStrings`. The forward/reverse projection
simplifiers therefore express the fixed datatype identity rather than
fabricating a string. As an independent negative check, the false claim that
projecting concrete `"A"` yields `""` built, reached a stuck state, and exited
1 in [`05_projection_opposite.log`](/audit-output/evidence/05_projection_opposite.log).
The projection connection's own `#Top` is consequently supported by static
datatype analysis and this negative probe, not accepted solely because its
simplifier makes the positive claim trivial.

There are three operational bridge rules:

1. The priority-40 yield rule is the fixed `#iterYield/#loopStep` transition
   with a statically typed string projection. Its universal connection claim
   is proved in `VERIFICATION-BASE`, before this rule is imported.
2. The priority-30 inner-loop rule summarizes exactly the submitted inner body
   in the exact closed seven-binding frame. Its universal connection claim is
   also proved before import.
3. The priority-20 outer-loop rule summarizes exactly the submitted outer
   body and five changed locals under `allStrings`. Its connection claim is
   proved after importing only the already-connected yield/inner rules and
   before importing the outer bridge itself.

This dependency order avoids a bridge proving its own connection. The bridge
left sides fix the real loop target and body; arbitrary following computation
is framed by `...`. Fresh continuation-sensitive claims put an observable
assignment after an inner loop and obtain the same final state with the fixed
rules and with the bridge:

- [`fixed_continuation_spec.k`](/audit-output/evidence/fixed_continuation_spec.k)
- [`bridge_continuation_spec.k`](/audit-output/evidence/bridge_continuation_spec.k)
- [`05_fixed_continuation.log`](/audit-output/evidence/05_fixed_continuation.log)
- [`05_bridge_continuation.log`](/audit-output/evidence/05_bridge_continuation.log)

The outer bridge requires an integer best score, but this does not narrow the
nonempty entry domain: the first iteration executes through the fixed
semantics while `best_strength` is `None`, installs the first integer score,
and only then can the bridge summarize an arbitrary tail. The empty entry has
its own theorem. `allStrings` is exactly the docstring's extension-name input
class, not a finite-size bound or a candidate-created restriction. Class
strings, first strings, tails, and character sequences all remain symbolic and
unbounded in finite length.

No inventoried candidate rule bypasses the function call, asserts the task
answer, substitutes a different program, or introduces an unconstrained
result oracle. I found no rule capable of enabling a false conclusion on the
claimed fixed-model domain. Accordingly, there is no unsoundness accusation
for which a false-conclusion witness is being withheld.

## 6. Fresh non-vacuity test

I ignored the candidate's `spec-vacuity.k` as proof of this gate and wrote the
fresh claim
[`reviewer-vacuity.k`](/audit-output/evidence/reviewer-vacuity.k). It loads the
exact submitted function on the satisfying concrete input
`Strongest_Extension("C", ["a", "B"])`, but deliberately requires the wrong
winner `"C.a"` instead of the actual `"C.B"`.

The dry run generated the proof command and exited 0, establishing that the
mutation parsed and built:
[`06_vacuity_dry_run.log`](/audit-output/evidence/06_vacuity_dry_run.log).
The real proof executed the program, reported `WarnStuckClaimState`, and exited
1:
[`06_vacuity_proof.log`](/audit-output/evidence/06_vacuity_proof.log). This is
the expected unmet result obligation, not a parser error, timeout, missing
import, or unreachable mutation. The theorem is non-vacuous.

## 7. Proven-versus-assumed accounting

### What the reachability proof establishes

Under the supplied semantics, for every finite model string `class_name` and
every finite list of finite model strings `extensions`, the exact regenerated
submitted function terminates normally and returns:

- `class_name + "."` when the list is empty; or
- `class_name + "." + extensions[i]` for nonempty input, where `i` is the
  least index whose extension has maximal fixed-model score, and that score is
  the sum of `+1` for ASCII uppercase, `-1` for ASCII lowercase, and `0`
  otherwise.

This is a symbolic, unbounded finite-data theorem, not a finite enumeration or
bounded unrolling. The empty-list behavior is the candidate's defensible policy
for a case the docstring leaves open.

### Trust ledger

| Boundary | Accounting |
|---|---|
| Read-only supplied K semantics | Trusted benchmark model; candidate copy was recursively verified identical. |
| K parser/compiler, Haskell proof backend, SMT/KORE machinery, LLVM concrete backend, and host arithmetic/sequence builtins | Standard toolchain trust boundary; versions and fresh builds are recorded. |
| K constructor disjointness, subsort injection/projection, maps, sequences, and integer arithmetic | Ordinary fixed-model primitives used by both execution and proofs. |
| Proof-local projection simplifiers | Derived from the sole `Str ::= str(IntSeq)` constructor and confined by exact string guards. The positive connection is mechanically checked, but its trivial normalization makes the static derivation and rejected opposite probe part of the justification. This is a minor proof-local trust/evidence limitation, not an oracle. |
| Loop bridges | Not assumptions: each is preceded by a universal reachability connection proof against the lower-level definition. K's circular reachability reasoning is part of the trusted prover. |
| First-maximum interpretation of `bestCodes` | Formally computed by exhaustive strict-update/negated-update structural equations; its identification as “first maximum” additionally uses ordinary induction over a finite sequence. |
| CPython/source bridge | Supported by direct source inspection, trusted translation identity, directed tests, and 10,000 generated cases. Differential testing supports this bridge only; it does not replace the K theorem. |
| Unicode case behavior | Documented supplied-model gap. The fixed rules are ASCII-only; CPython and the submitted source are Unicode-aware. Witness: `("Gap", ["", "Ω"])` gives `"Gap."` in the fixed model and `"Gap.Ω"` in CPython. The candidate documents `Ω` and the model boundary in its trust ledger and introduces no further narrowing. |
| Empty extensions | Docstring-underdetermined. Candidate returns `class_name + "."`; canonical raises. The proof covers, rather than excludes, the candidate policy. |
| Unused opaque supplied symbols | Float, sort, hash, and other unused semantic families cannot occur in the exact submitted term and do not affect the target result. |

The Unicode discrepancy is model-versus-CPython, not
program-versus-docstring: the Python program uses the intended Python case
predicates and passes the concrete Unicode witness. Under campaign amendment
v2, that documented supplied-model gap requires the non-fatal
`CONCERNS / LEGIT` mapping.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
