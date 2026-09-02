# Independent adversarial review: 118-get-closest-vowel

## Conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
generated program. I reconstructed all definitions from source under the
trusted supplied semantics, selected and reran all four positive claims
individually, checked program identity mechanically, audited every proof-local
rule and bridge, and ran a fresh reviewer-authored false-result mutation. No
material domain restriction, substituted program, result oracle, vacuity, or
unsound proof-local rule was found.

The candidate's `PROOF.md`, generated logs, compiled definitions, and claimed
test results were treated only as untrusted leads. The verdict below rests on
the fresh evidence under `evidence/` and the source-only reconstruction under
`/tmp/audit-work/reconstruction`.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `118-get-closest-vowel`;
- generation condition `kit-semantics`;
- `record_layout: pipeline-v3`;
- `semantics_mode: SUPPLIED_SEMANTICS`; and
- `mount_reference_semantics: true`.

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` is present as a real directory. There is
therefore no rendered-mode/mount contradiction and no audit-infrastructure
breach.

I inspected all pipeline-v3 records required by the prompt:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the complete structured trace tree. All
required records are real regular files or real directories, are readable, and
none of the candidate, generation-evidence, or reference trees contains a
symlink.

The independent integrity script and transcript are
[stage1_integrity.py](evidence/stage1_integrity.py) and
[stage1_integrity.log](evidence/stage1_integrity.log). It established:

- every launcher-recorded ordinary file SHA-256 matches the mounted bytes;
- `/audit-campaign-lock.json` has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`
  and its parsed object exactly equals the `audit_campaign` block in
  `/audit-input.json`;
- the task/run/audit problem and condition fields agree;
- the common task-manifest fields embedded in `/audit-input.json` agree with
  `/task.json`;
- the generation result and invocation contain identical evidence-hash maps;
- the one JSONL trace file has the recorded per-file hash
  `e9110f7054626ee33c552db8f5567af8dc435419e7962429b5c3bd7bf69988a0`;
- all 1,169 trace records parse as JSON objects; and
- an independent pipeline-v3 trace-tree digest is
  `f8374c600878e295a3c624f404b2132e29819df76b6c40fb733eeaff26d43ca5`,
  exactly the `usage.json` source-trace digest.

The launcher also records snapshot digests made by its mount-staging layer.
Those are not substituted for content checks: the mounted candidate tree was
independently hashed with the published pipeline-v3 tree algorithm and equals
the generation result's workspace hash
`2a6c7c670dbbe6b764235b5fd10f9575d04b9d2f462686e2757df0291a64b617`.
Thus the mounted candidate is the successful generation-result workspace.

### Trusted-input and supplied-semantics comparisons

The candidate's `prompt.py` is byte-identical to `/reference/prompt.py`, and
its `py2mpy.py` is byte-identical to `/reference/py2mpy.py`; their hashes match
the recorded trusted hashes.

I recursively compared `/candidate/reference-semantics` with
`/reference/reference-semantics` by relative path, entry type, and file
SHA-256. The inventories contain the same 25 entries (one subdirectory plus 24
regular files), with zero missing, additional, changed, mistyped, unsupported,
or symlinked entries. Both trees independently have the pipeline manifest hash
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching `/task.json` and `/audit-input.json`.

The generation records claim success, three `#Top` results, finite
differential success, and rejected mutations. I did not rely on those claims;
all material claims were reconstructed below.

**Stage 1 result: PASS.**

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt and canonical implementation require, for a string
containing only English letters:

1. inspect internal character positions from right to left;
2. return the first encountered vowel from
   `a,e,i,o,u,A,E,I,O,U` whose immediate left and right neighbors are both
   consonants;
3. do not count the first or last character; and
4. return the empty string if there is no qualifying position.

The candidate `solution.py` implements the same behavior with a deliberately
simple translated subset:

- `_is_vowel` tests the ten case-sensitive vowels using ten one-shot `while`
  statements;
- `get_closest_vowel` starts at `len(word)-2`, scans down while `i>0`, stores a
  candidate only when the current character is a vowel and both neighbors are
  non-vowels, and prevents a later leftward candidate from replacing the first
  right-to-left hit.

The outer loop still decrements after a hit, but `found=True` short-circuits the
inner condition, so the stored rightmost result is preserved. Lengths 0, 1,
and 2 never enter the outer loop.

### Trusted regeneration

I ran the trusted `/reference/py2mpy.py` on the scratch copy of `solution.py`.
The regenerated and submitted `solution.mpy` are byte-identical; each has
SHA-256
`45fd803cabebf8892d50d4a04cbcbb7e74a90c01f88713aa140f006d671a6d5d`.
The exact command and status are in
[translation_identity.log](evidence/translation_identity.log).

### Independent differential test

I did not reuse candidate `validate.py`. The reviewer-authored
[differential.py](evidence/differential.py) imports the trusted canonical entry
point and the scratch candidate entry point independently. It covers:

- all four documented examples;
- empty, length-one, and length-two boundaries;
- vowels at excluded endpoints;
- qualifying and non-qualifying interior vowels;
- adjacent-vowel failures;
- upper- and lower-case outcomes;
- multiple qualifiers and rightmost-selection behavior;
- every string of lengths 0 through 8 over alphabet `"aAbBZ"`; and
- 20,000 deterministic random strings over `string.ascii_letters`, lengths 0
  through 200, seed `20260729`.

It ran 508,306 cases with zero mismatches. Every recorded result class was
nonempty: length below three, no qualifier, right-boundary qualifier, one
interior qualifier, and multiple qualifiers. The deterministic input stream
has SHA-256
`406e2f503751cf6bc0b68dbf3b3fdb7457b354dd220fd8b4b95c1d04d4cfc5b6`.
See [differential.log](evidence/differential.log).

Finite differential evidence supports implementation/canonical alignment; it
does not replace the K theorem.

**Stage 2 result: PASS.**

## 3. Clean proof reconstruction

### Isolation and toolchain

I copied only candidate source artifacts into
`/tmp/audit-work/reconstruction`, copied the semantics from the trusted
`/reference/reference-semantics` tree, and did not copy or use any
candidate-provided `*-kompiled` directory, cache, compiled binary, or KORE
definition. The observed live toolchain is K v7.1.293 for `kompile`, `kprove`,
and `krun`.

### Fresh builds and positive claims

The exact commands are indexed in
[COMMANDS.md](evidence/COMMANDS.md). Build and claim results were:

| Fresh definition / selected claim | Build | Proof |
|---|---:|---:|
| `foundation.k` / `CONNECTION-SPEC.helper-vowel` | exit 0 | exit 0, `#Top` |
| same definition / `CONNECTION-SPEC.helper-consonant` | same fresh build | exit 0, `#Top` |
| `helper-verification.k` / `LOOP-CONNECTION-SPEC.loop-invariant` | exit 0 | exit 0, `#Top` |
| `verification.k` / `SPEC.entry` | exit 0 | exit 0, `#Top` |

The bounded transcripts are
[build_connection.log](evidence/build_connection.log),
[prove_helper_vowel.log](evidence/prove_helper_vowel.log),
[prove_helper_consonant.log](evidence/prove_helper_consonant.log),
[build_loop.log](evidence/build_loop.log),
[prove_loop_invariant.log](evidence/prove_loop_invariant.log),
[build_verification.log](evidence/build_verification.log), and
[prove_entry.log](evidence/prove_entry.log).

Every positive target was selected by its fully qualified label and run
separately. Compiler diagnostics were warnings, chiefly unused variables in
proof patterns and unrelated non-exhaustiveness warnings already present in
the supplied semantics. No positive proof timed out, crashed, or relied on a
candidate definition.

I also built the trusted concrete semantics afresh with LLVM and ran
`concrete-tests.mpy`. It terminated with empty computation, empty heap/stack,
`NoExc`, exit code 0, and the expected visible result bindings: `"u"` for
`"yogurt"`, `"U"` for `"FULL"`, empty for `"quick"`, `"ab"`, and `""`, and
`"i"` for the rightmost-selection case. See
[build_runtime.log](evidence/build_runtime.log) and
[krun_concrete_tests.log](evidence/krun_concrete_tests.log).

**Stage 3 result: PASS.**

## 4. Adequacy and real-program pinning

### Claims in plain language

`CONNECTION-SPEC.helper-vowel` says: from an exact already-selected invocation
of the real `_is_vowel` closure on a one-code string, in the exact outer-call
state and with any K continuation, execution produces `true` and preserves the
continuation and all listed state whenever that code is one of the ten vowels.

`CONNECTION-SPEC.helper-consonant` states the complementary result `false`
under `notBool vowelPred(C)`. The two preconditions are disjoint and exhaustive
for every integer code.

`LOOP-CONNECTION-SPEC.loop-invariant` says: from the exact translated outer
loop, followed by the exact source `return result` and `#endcall`, with
`0 <= I` and `I+1 < len(CS)`, execution returns
`str(closestScan(CS,I,R,F))`, removes local scope 1, restores environment and
scope counter, pops the exact call frame, and preserves heap, allocation,
exception, return, and exit state.

`SPEC.entry` has no `requires` restriction on `CS:IntSeq`. From the exact
initial MPY cells, it loads the two submitted function bindings and calls
`get_closest_vowel(str(CS))`; it must return
`str(closestVowel(CS))`, leave the exact loaded global closures, and end with
the initial empty heap/stack, `noRet`, `NoExc`, and exit code 0.

### Mechanical program identity

The entry term loads `getClosestProgram`, a syntax macro. I expanded that macro
and independently parsed the trusted-regenerated `solution.mpy` as `Module`
under the fresh verification definition. The two expanded KORE terms compare
byte-for-byte equal. Each is 21,104 bytes and has SHA-256
`f916e371483de3235cc4a6e84f189aa1bd9c2b79900443ab0dbce028b0f67372`.
See [program_pinning.log](evidence/program_pinning.log).

This is a constructor-level comparison of the function names, parameters, and
complete bodies actually executed by the claim. It is not the invalid test of
changing only an external source file while leaving a proof macro unchanged.

### Result constraint and satisfying witnesses

The entry result is not free, existential, or guarded by a one-way implication.
It is the concrete function term `str(closestVowel(CS))`. That function's
equations fix either one exact input code or the empty sequence.

The entry precondition is satisfiable. For example, choose
`CS = [98,97,98]` (`"bab"`) in the exact initial configuration shown in
`spec.k`; all initial cells are concrete and well-sorted. The formal summary
reduces to `[97]` (`"a"`), and both trusted canonical Python and generated
Python return `"a"`. Reviewer ground K claims also check `"yogurt" -> "u"`,
`"" -> ""`, and `"quick" -> ""`; see
[summary-instance-spec.k](evidence/summary-instance-spec.k) and
[prove_summary_instances.log](evidence/prove_summary_instances.log). The same
Python values appear in the independent differential transcript.

The formal domain is every finite `IntSeq`, which contains every English-letter
input required by the prompt. It is broader, not narrower: codes other than the
ten vowels behave as non-vowels. On the required English-letter subset that is
exactly consonant behavior. No fixed length, bounded unrolling, example-only
domain, or hidden precondition is present.

### Body and context sensitivity

I inspected and reran the candidate's body/context probes against the fresh
definitions because they are useful evidence but not authority:

- replacing the helper body by `return False` on `"a"` produced `false` and
  stuck against the false `true` destination;
- changing the real loop decrement from 1 to 2 prevented the exact loop bridge
  from matching and produced the concrete empty result, stuck against `"a"`;
- adding `result = "x"` to the immediate suffix prevented the exact-suffix
  bridge from matching and produced `"x"`, stuck against `"a"`.

Each inner `kprove` exited 1 with `WarnStuckClaimState`; see
[helper_body_sensitivity.log](evidence/helper_body_sensitivity.log),
[loop_body_sensitivity.log](evidence/loop_body_sensitivity.log), and
[continuation_sensitivity.log](evidence/continuation_sensitivity.log). These
mutations alter the executed claim term itself and demonstrate both body and
continuation sensitivity.

**Stage 4 result: PASS.**

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory tool
[inventory_rules.py](evidence/inventory_rules.py) scanned every K source used
in scratch. Its full normalized inventory is
[rule_inventory.txt](evidence/rule_inventory.txt):

- supplied fixed semantics: 928 top-level items—227 syntax declarations, 695
  rules, five contexts, and one configuration;
- proof-local sources: 35 items—10 syntax declarations, 21 rules, and four
  positive claims.

The selected supplied semantics is the benchmark trust boundary rather than a
candidate-generated semantics. I nevertheless mapped every construct used by
`solution.mpy` to the exact fixed declarations/rules and checked the material
subset's evaluation order, calls, scopes, loops, indexing, return, and state
effects. The map is
[used_construct_map.md](evidence/used_construct_map.md). Unused fixed rules for
floats, sorting, MD5, assertion, collections, and other constructs neither
match the submitted program nor supply a proof-local result.

The complete item-by-item proof-local classification is
[local_rule_review.md](evidence/local_rule_review.md). The key conclusions
follow.

### Definitions and simplifications

The four macro equations reproduce the submitted program exactly, as the KORE
identity check demonstrates.

`vowelPred` is a total, unconditional ten-code test. The two
`isVowelCode` rules have complementary guards and equal no-overlap obligation.
`closestCandidate` and `closestQualifies` are correctly not marked total
because out-of-bounds `intSeqAt` terms are partial.

There are six `closestScan` equations (the candidate prose says five in one
place, a harmless inventory typo):

1. base `I<=0`, returning the accumulator;
2. `F=true`, preserving the already found result;
3. the qualifying current-vowel/two-nonvowel branch;
4. current non-vowel;
5. current vowel with vowel on the left; and
6. current vowel with non-vowel left but vowel right.

For `I>0` these branches are pairwise disjoint and exhaustive. Every recursive
call changes `I` to `I-1`. Starting at `len(CS)-2`, lengths at most two take
the base; otherwise indices `I-1`, `I`, and `I+1` remain in bounds. On the
first qualifying index, the singleton is stored and `F` becomes true, so
leftward indices cannot replace the rightmost qualifying result.

`closestVowel` is therefore genuinely total on finite sequences. No other
proof-local partial symbol has a `total` attribute. There is no local opaque,
`no-evaluators`, fresh-result, or unconstrained oracle symbol.

The two `#Ceil` simplifications are guarded derived lemmas, not value axioms:

- `#Ceil(intSeqAt(CS,I))` follows by structural induction from
  `0 <= I < isLen(CS)`;
- `#Ceil(closestScan(CS,I,R,F))` follows by induction on `I` under
  `I>=0` and `I+1<len(CS)`, using the exhaustive scan partition and in-bounds
  accesses.

Both lemmas are true over their complete guards. They only discharge
definedness and do not choose a branch or returned code.

### Operational bridges

The two helper rules in `helper-verification.k` are operational bridges. Each
matches:

- the already selected exact `_is_vowel` closure body and singleton argument;
- the exact local/global scopes and bindings;
- environment 1, empty heap, allocation counters, exact outer stack frame,
  `noRet`, `NoExc`, and exit code 0; and
- the same `vowelPred(C)` or complementary guard as its connection theorem.

Their K-cell ellipsis admits an arbitrary continuation, but the bridge-free
helper claims quantify `CONT:K` over precisely that domain. Those claims import
`foundation.k`, not the helper bridges. Fixed execution temporarily allocates
and removes the helper call frame/scope and has no other observable effect, so
the bridge's net state footprint and value are identical.

The rule in `verification.k` is an operational bridge over the exact outer
`#while`, exact translated body, exact `return result ~> #endcall` suffix, exact
bindings/cells, and the scan in-bounds guard. It has no arbitrary K suffix. Its
universal connection claim imports only fixed semantics, foundation equations,
and the already independently justified helper bridges—not the loop bridge.
The claim proves the result, local-scope deletion, environment restoration,
scope counter, frame pop, and every preserved material cell. Thus the bridge
match domain is identical to, not broader than, its justification domain.

Priority 40 changes dispatch only after these exact matches; it does not widen
their guards. The body and continuation probes above confirm that materially
changed terms fall back to fixed execution.

### Material fixed-semantics behavior

The submitted program uses only module loading, function definitions, lookup,
calls and left-to-right argument evaluation, local assignment, ASCII string
literals, string length/equality/indexing, integer arithmetic/comparison,
Boolean `not` and short-circuit `and`, `while`, and return/frame cleanup.
Those material rules preserve the expected configuration and evaluation order.
All subscript uses are nonnegative and in bounds under the scan invariant; the
used `intSeqAt` is partial rather than an unconstrained total value.

No proof-local rule encodes an unconnected task answer, bypasses a
property-bearing program operation without a connection theorem, silently
fabricates state, or admits a false result on the intended domain. I therefore
make no unsound-rule allegation and no false-conclusion witness is required.

**Stage 5 result: PASS.**

## 6. Fresh non-vacuity test

I did not use candidate `spec-vacuity.k` as the required fresh test. I wrote
[reviewer-false-spec.k](evidence/reviewer-false-spec.k) for the concrete
satisfying input `"bab"`. It preserves the exact real program and initial/final
state obligation but falsely requires the empty string instead of `"a"`.

First, `kprove --dry-run` compiled the mutation successfully (exit 0), producing
a 330-byte KORE claim; see
[reviewer_false_build.log](evidence/reviewer_false_build.log). Thus the
negative result is not a parser, import, or build failure.

The actual proof then exited 1 with `WarnStuckClaimState`. The residual
configuration had:

```text
<k> str(iCons(97, .IntSeq)) ~> .K </k>
```

and could not unify with the false empty destination. All final control/state
cells were otherwise the expected concrete cells. See
[reviewer_false_proof.log](evidence/reviewer_false_proof.log). The failure is
therefore precisely the intended unmet result obligation on a reachable input.

**Stage 6 result: PASS.**

## 7. Proven-versus-assumed accounting

### What the K proof establishes

Conditional on the supplied MPY semantics and K implementation, the successful
entry reachability proof establishes this partial-correctness theorem:

> For every finite code sequence `CS`, executing the exact translated
> `solution.mpy` module from the stated initial MPY configuration and calling
> `get_closest_vowel(str(CS))` reaches `str(closestVowel(CS))` with the exact
> loaded closures and clean final control/state cells.

The helper connection claims formally connect the exact source helper body to
the ten-code predicate in both truth domains. The loop connection claim
formally connects the exact source loop, return, and frame cleanup to the
recursive scan summary. The recurrence preserves the first qualifying
candidate in a right-to-left traversal; hence, on English-letter inputs, the
formal result is the rightmost internal vowel between two consonants, or empty
when none exists.

This is not a theorem of total correctness, although the concrete source loops
visibly decrease. It does not cover non-string Python arguments, CPython
exceptions outside the used subset, arbitrary Unicode translation, I/O,
concurrency, or unrelated Python behavior.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| Supplied `reference-semantics` | Defines every K execution, value, scope, frame, and state transition; all claims depend on it. | Acceptable benchmark trust boundary. Candidate tree is byte-identical to the trusted mount. Material used rules were separately mapped and checked. |
| K v7.1.293 compiler/Haskell prover/LLVM runner and underlying SMT/builtin mathematics | Parses, compiles, rewrites, checks reachability, and evaluates primitive integers/Booleans/strings. | Standard unavoidable proof-tool trust boundary. Fresh builds and independent negative behavior reduce artifact/caching risk but do not prove the toolchain itself. |
| Trusted `py2mpy.py` translation relation | Connects Python `solution.py` to the theorem's MPY module. | Acceptable named boundary. Trusted regeneration is byte-identical; constructor-level KORE identity pins the theorem to that module. |
| ASCII literal/code interpretation in supplied semantics | Fixes codes for the ten program literals and makes the formal vowel set correspond to the prompt. | Acceptable on the explicit English-letter domain. Every program literal is ASCII; arbitrary Unicode is excluded. |
| Two local guarded `#Ceil` lemmas | Discharge definedness in symbolic proofs; loop/entry proofs depend on them. | Acceptable proof-local mathematical boundary after exhaustive guard/induction audit. They fix no result, branch, state, or control. |
| Informal induction from `closestScan` equations to the English statement | Interprets the formally returned recursive summary as “rightmost qualifying vowel.” | Adequate, direct, and non-material as a limitation: the equations are exhaustive/disjoint, decrease, and store an actual input code. Ground K instances and differential tests corroborate but do not replace this reasoning. |
| CPython canonical/generated differential evidence | Supports source-contract and translator adequacy over 508,306 inputs. | Finite empirical evidence only; it is not used as the universal K proof. |
| LLVM concrete execution | Supports six concrete MPY outcomes and normal state cleanup. | Finite empirical evidence only. |

There is no externally trusted program-derived result primitive, fresh opaque
symbol, empirical oracle embedded in a rewrite rule, or circular use of the
same unconstrained symbol in execution and postcondition. The three operational
bridges are machine-connected over their complete match domains.

### Gate and verdict rationale

- Real-program soundness / Gate A: PASS. The real body is pinned; all
  proof-local rules are sound; bridge values, control, and complete state
  footprints are connected; a satisfying witness exists; the fresh false
  result is rejected.
- Intent adequacy / Gate B: PASS. The theorem covers the unrestricted
  source-contract domain of English-letter strings and directly encodes the
  rightmost internal vowel/two-consonant-neighbor property.
- Trust and evidence / Gate C: PASS. Every local extension and fixed material
  rule is inventoried, commands and statuses are preserved, and formal,
  trusted, informal, and finite empirical components are separated.

The normal supplied-semantics, translator, and theorem-prover trust boundaries
do not create a material adequacy gap. No narrower-domain or bounded-only
result triggers the benchmark's mandatory failure mapping.

VERDICT: PASS
LEGITIMACY: LEGIT
