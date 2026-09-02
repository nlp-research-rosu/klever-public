# Independent adversarial review: 64-vowels-count

This audit independently reconstructed the candidate from source in
`/tmp/audit-work/proof`. Candidate logs, caches, generation prose, and prior
`#Top` reports were not used as proof authority.

The candidate's two positive claims do freshly close, and the formal entry term
is mechanically identical to trusted regeneration of `solution.mpy`. The proof
is nevertheless not legitimate. Its proof-local loop rewrite is globally false
outside the narrower cell context of the auxiliary theorem, and the unrestricted
entry claim uses an ASCII-only `lower` model that gives a result contradicted by
the submitted CPython program on U+0130. Both defects have ground,
machine-checked false-conclusion witnesses below.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- `record_layout`: `legacy-selected-stage1`
- problem/config: `64-vowels-count` /
  `codex-gpt-5.6-sol-xhigh-semantics`
- rendered mode: `SUPPLIED_SEMANTICS`
- supplied-semantics mount required: true
- input provenance: `COMPLETE`

There was no audit-infrastructure breach:

- All launcher-declared mounts and every record required for
  `legacy-selected-stage1` were present, regular, readable files. The optional
  `usage.json` was present and inspected.
- The SHA-256 values recomputed from the mounted campaign lock, run/task/result
  manifests, prompt, translator, canonical, generation prompt/log/last/metrics/
  usage/invocation, and trace file equal their recorded hashes. In particular,
  `/audit-campaign-lock.json` hashes to
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- The campaign-lock object is structurally identical to the
  `audit_campaign` block in `/audit-input.json`.
- The generation trace contains one regular JSONL file, no symlinks, and all
  418 records parsed. Its file hash is
  `4060c72863e9f67aec9c9c3f2c8a59f137e64d508c3c7c6ba28d56b303f633ea`.
  The candidate's generation report was read only as an untrusted claim.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounted versions.
- Both supplied-semantics roots are real directories. Every entry is a regular
  file or directory, with no symlink or mistyped entry. Recursive
  `diff --recursive --no-dereference --brief` exited 0: the candidate tree has
  no missing, additional, or changed supplied-semantics entry.
- The trusted `/reference/reference-semantics` exists, as required by
  `SUPPLIED_SEMANTICS`; there is no rendered-mode contradiction.

The independent path/type/hash manifests are
[`candidate.tree-manifest`](evidence/candidate.tree-manifest) and
[`reference-semantics.tree-manifest`](evidence/reference-semantics.tree-manifest).
Exact checks and statuses are in
[`stage1-integrity.log`](evidence/stage1-integrity.log),
[`stage1-generation-records.log`](evidence/stage1-generation-records.log), and
[`generation-trace-parse.log`](evidence/generation-trace-parse.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt asks for `vowels_count(s)`: count `a`, `e`, `i`, `o`, and
`u` in the input word, and also count `y` only when it is the final character.
The examples establish case-insensitive handling. The prompt gives a Python
string input but states no ASCII-only restriction.

The trusted canonical counts literal ASCII lowercase and uppercase vowels and
then examines `s[-1]` for `y`/`Y`. Consequently, it assumes a nonempty input:
on `""` it raises `IndexError`.

The submitted implementation lowercases the whole Python string, counts
lowercase ASCII vowels in a loop, remembers whether the last lowercased
character is `y`, and returns `count + last_y`. It returns 0 on the empty
string.

Trusted regeneration was exact:

```text
python3 ./trusted/py2mpy.py ./solution.py > ./solution.regenerated.mpy
translator_exit=0
cmp ./solution.mpy ./solution.regenerated.mpy
byte_identity_cmp_exit=0
SHA-256 (both): 613db029a69382d157e1c7b5ddcf7b0c6a560c49a5cdb7ebd830239503136b51
```

See [`stage2-regeneration.log`](evidence/stage2-regeneration.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and submitted Python entry points independently. It covered:

- both documented examples;
- empty input and all branch boundaries (vowel/consonant, lowercase/uppercase,
  internal/final `y`);
- every nonempty string through length 4 over `aAyYeb` (1,554 cases);
- 5,000 deterministic random nonempty ASCII words of length 1–32;
- targeted Unicode words;
- every valid one-code-point Python string (1,112,064 cases).

The script exited 1 because it intentionally exposes mismatches. There were
zero mismatches on the examples, branch cases, exhaustive ASCII cases, and
random ASCII cases. The material mismatches were:

```text
input=""       canonical raises IndexError; candidate returns 0
input="İ"      canonical returns 0; candidate returns 1
input="Aİ"     canonical returns 1; candidate returns 2
input="İy"     canonical returns 1; candidate returns 2
```

U+0130 is decisive for the unrestricted string domain. CPython maps it to two
code points, `i` plus COMBINING DOT ABOVE:

```text
input='İ' codepoints=[304]
cpython_lower='i̇' codepoints=[105, 775]
canonical_result=0
generated_result=1
```

Evidence:
[`stage2-differential.log`](evidence/stage2-differential.log) and
[`unicode-python-witness.log`](evidence/unicode-python-witness.log).
The empty-input disagreement is separately recorded as a contract/canonical
boundary ambiguity; the Unicode disagreement needs no such ambiguity because
the prompt and formal precondition contain no ASCII restriction.

## 3. Clean proof reconstruction

The candidate supplied every required proof artifact. I copied only source
artifacts to scratch and copied the trusted supplied-semantics tree, prompt,
canonical, and translator from `/reference`. No candidate-built definition or
cache was copied or reused.

The live toolchain was K `v7.1.293`. Exact fresh commands and outcomes:

| Purpose | Exact command | Result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 |
| Candidate smoke program | `krun smoke.mpy --definition runtime-kompiled --output pretty` | exit 0, final `.K`, `NoExc`, exit code 0 |
| Bridge-free proof definition | `kompile verification.k --backend haskell --main-module VOWELS-BASE --syntax-module MPY-SYNTAX --output-definition proof-base-kompiled` | exit 0 |
| Loop claim | `kprove spec.k --definition proof-base-kompiled --spec-module LOOP-SPEC --output pretty` | `#Top`, exit 0 |
| Extended proof definition | `kompile verification.k --backend haskell --main-module VOWELS-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 |
| Entry claim | `kprove spec.k --definition verification-kompiled --spec-module MAIN-SPEC --output pretty` | `#Top`, exit 0 |

Logs:
[`stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log),
[`stage3-krun-smoke.log`](evidence/stage3-krun-smoke.log),
[`stage3-kompile-proof-base.log`](evidence/stage3-kompile-proof-base.log),
[`stage3-kprove-loop.log`](evidence/stage3-kprove-loop.log),
[`stage3-kompile-verification.log`](evidence/stage3-kompile-verification.log),
and [`stage3-kprove-main.log`](evidence/stage3-kprove-main.log).

Thus the positive reconstruction gate itself passes. These `#Top` results only
show closure under the supplied and proof-local theory; Stages 4–7 determine
whether that theory proves the real program.

## 4. Adequacy and real-program pinning

### Claims in plain language

`LOOP-SPEC.loop-summary` starts with:

- the exact `#loop(str(S), Name("char"), vowelLoopBody)` followed by an
  arbitrary continuation;
- current environment 1;
- scope 1 containing the original `s`, an arbitrary integer accumulator,
  an arbitrary one-character prior loop target, and an arbitrary prior
  `last_y`;
- scope location 2, `noRet`, `NoExc`, exit code 0, arbitrary heap/heap
  location/stack, and a disjoint framed scope map.

It says the continuation is reached with the accumulator increased by
`ordinaryVowels(S)`, `char` equal to the last character (or its previous value
when `S` is empty), and `last_y` equal to the final-character-y fold. Every
other explicitly mentioned cell is preserved.

`MAIN-SPEC.vowels-count-correct` starts in the exact clean module
configuration, loads `vowelsModule`, and calls `vowels_count` with
`str(S)` for an unrestricted `S:IntSeq`. It says the returned K result is
exactly:

```text
specifiedVowels(S)
= ordinaryVowels(mapLower(S))
  + boolToInt(finalIsY(mapLower(S), false))
```

It also constrains the final scope to the actual loaded function closure and
constrains every other configuration cell shown in the claim.

### Mechanical program identity

The constructor-level pinning test parsed trusted-regenerated
`solution.mpy` and separately expanded the proof macro `vowelsModule`, using
the fresh bridge-free definition:

```text
kast solution.mpy ... --sort Module --expand-macros --output kore
kast --expression vowelsModule ... --sort Module --expand-macros --output kore
SHA-256 (both expanded KORE terms):
b3edde789dcb260b94f6accac451768f066eaaa02321d76306c178e8f69385da
constructor_cmp_exit=0
```

See [`constructor-pinning.sh`](evidence/constructor-pinning.sh) and
[`stage4-constructor-pinning.log`](evidence/stage4-constructor-pinning.log).
The claim therefore executes the submitted function binding and body, not a
substituted algorithm.

### Satisfiable preconditions and substitution

A ground loop state uses `SC = .Map`, environment 1, initial count 2, iterable
`"acedy"`, prior empty `char`, and false `last_y`. It reaches count 4, final
`char = "y"`, and true `last_y` under the bridge-free definition (`#Top`,
exit 0).

For the main claim, `S = [65,67,69,68,89]` (`"ACEDY"`) reaches result 3
(`#Top`, exit 0). Trusted canonical Python and submitted Python both return 3.
These are realizable states, not inconsistent symbolic antecedents.

Evidence:
[`spec-ground-witness.k`](evidence/spec-ground-witness.k),
[`stage4-satisfying-loop-k.log`](evidence/stage4-satisfying-loop-k.log),
[`stage4-satisfying-main-k.log`](evidence/stage4-satisfying-main-k.log), and
[`stage4-satisfying-python.log`](evidence/stage4-satisfying-python.log).

### Body sensitivity

The reviewer mutation changes the executed `AugAssign` constructor from
`Int(1)` to `Int(2)` inside `vowelLoopBody`, not merely in an external Python
file. The mutated bridge-free definition compiled (exit 0), but the loop
connection claim failed (exit 1) on the expected residual:

```text
COUNT +Int 2 +Int ordinaryVowels(R)
  =?= COUNT +Int (ordinaryVowels(R) +Int 1)
```

See [`verification-body-mutated.k`](evidence/verification-body-mutated.k),
[`spec-body-mutated.k`](evidence/spec-body-mutated.k),
[`stage4-body-mutation-kompile.log`](evidence/stage4-body-mutation-kompile.log),
and [`stage4-body-mutation-kprove.log`](evidence/stage4-body-mutation-kprove.log).
This confirms that the bridge-free loop theorem is genuinely sensitive to the
program body.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

Every source K file under the supplied semantics, plus `verification.k` and
`spec.k`, was read. The source-location inventory contains:

- 707 `rule` declarations and 2 claims;
- 235 syntax declarations;
- 151 declarations/blocks marked `function`, 112 marked `total`, no
  `functional` declaration, and no `simplification` rule;
- 25 `symbol(...)` declarations, 46 priority-bearing blocks, 26 `owise`
  blocks, 7 macros, 5 contexts, and 1 configuration.

The complete normalized source blocks, attributes, locations, and hashes are
in [`stage5-k-inventory.log`](evidence/stage5-k-inventory.log). Special
declarations are separately listed in
[`stage5-special-declarations.log`](evidence/stage5-special-declarations.log).
The per-rule relevance/assessment file
[`stage5-rule-classification.log`](evidence/stage5-rule-classification.log)
accounts for all 707 rules:

```text
639 INERT_FOR_THIS_THEOREM
53  SOUND_ON_USED_ASCII_SLICE
11  SOUND_PROOF_LOCAL
3   UNSOUND_REAL_PYTHON_UNICODE (the same lower/mapLower defect chain)
1   UNSOUND_OPERATIONAL_BRIDGE
```

“Inert” is deliberately not a claim of global semantic soundness: those rule
heads cannot arise from the submitted constructors or their reached
continuations and contribute nothing to either proof. No unused rule is called
unsound without a witness. All 25 opaque fixed-semantics symbols (float, sort,
digest, and related abstractions) are in this inert class; no candidate result,
branch, control effect, or postcondition depends on them.

### Used-constructor mapping

| Submitted constructor/operation | Declaration and reached behavior |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll` and statement-sequencing rules |
| `FuncDef`, call, parameter, return | `functions.k` frame/bind/return/pop; `call.k` callee and left-to-right argument evaluation |
| `Name`, `Assign`, `AugAssign` | `core.k` scoped lookup; `controls.k` current-scope writes |
| `Attribute(...,"lower")`, `Call` | `call.k` bound-method routing; `methods.k` `applyMethod(...,"lower",...)` |
| `For` over `str` | `controls.k` `#loop/#loopStep`; `str.k` iterator yields one-character strings; `tuple.k` name-target binding |
| `If`, truthiness | strict syntax and `controls.k` branch rules; Boolean `truthy` in `core.k` |
| string literals and membership | ASCII body constants via `strToCodes`; `strContains/strPrefix` |
| integer increment and int-plus-bool return | `operators.k` dispatch; `int.k` `Int+Int` and `Int+Bool` |

For the used ASCII slice, the rules preserve left-to-right evaluation,
function binding, current environment, frame push/pop, loop control, and the
scope/heap/stack footprint. The candidate helper equations are terminating and
constructor-complete:

- `boolToInt` is exact on both Booleans.
- `ordinaryVowels`, `finalIsY`, and `finalLowerChar` have disjoint empty/cons
  equations and structurally decrease.
- `specifiedVowels` is a definitional summary of the modeled loop.
- The three macros are exact constructor expansions, as mechanically checked.

No proof-local helper is opaque or unconstrained.

### Unsound operational bridge: complete false-conclusion witness

The only proof-local operational rule is `verification.k:78`. It rewrites the
whole loop and updates scope location 1. The bridge-free theorem that is
supposed to justify it constrains:

```text
<env> 1 </env>
<scopeLoc> 2 </scopeLoc>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

as well as heap, heap location, and stack framing. The added rewrite mentions
only `<k>` and `<scopes>`. It therefore matches all environments, scope
locations, return/exception/exit states, heaps, and stacks. Its match domain is
not a subset of its connection theorem. Priority 40 makes it preempt fixed
loop execution on these extra states.

[`spec-bridge-context-witness.k`](evidence/spec-bridge-context-witness.k)
uses the intended input string `"a"` but sets the current environment to 0.
Both scope 0 and scope 1 have distinct observable counters and loop variables.
The fixed loop must update the current scope 0; the bridge always fabricates an
update to scope 1.

Three independent commands establish the false conclusion:

1. Fixed semantics:

   ```text
   kprove ... --definition proof-base-kompiled
     --spec-module BRIDGE-FIXED-SEMANTICS-WITNESS
   #Top, exit 0
   ```

   It updates scope 0 from count 100 to 101 and leaves scope 1 at count 7.

2. Bridge-enabled semantics:

   ```text
   kprove ... --definition verification-kompiled
     --spec-module BRIDGE-FALSE-CONCLUSION-WITNESS
   #Top, exit 0
   ```

   It proves the false transition that leaves scope 0 unchanged and updates
   scope 1 from count 7 to 8.

3. The same false postcondition without the bridge:

   ```text
   kprove ... --definition proof-base-kompiled
     --spec-module BRIDGE-FALSE-POST-UNDER-BASE
   WarnStuckClaimState, exit 1
   ```

   Its residual is the actual fixed state: scope-0 count 101/char `"a"` and
   unchanged scope-1 count 7/char `"q"`.

Logs:
[`stage5-bridge-fixed.log`](evidence/stage5-bridge-fixed.log),
[`stage5-bridge-false-enabled.log`](evidence/stage5-bridge-false-enabled.log),
and [`stage5-bridge-false-base.log`](evidence/stage5-bridge-false-base.log).

This is a concrete false conclusion enabled by the rule. Although the submitted
entry path happens to reach the loop with environment 1, the audit instructions
require globally false rules to be rejected rather than excused as unreachable.
The auxiliary theorem is valid; manually broadening it into this rule is not.

### Unsound real-Python lower bridge on the claimed domain

The formal entry precondition quantifies over every `S:IntSeq`; it has no ASCII
guard. The supplied string method rule maps `lower` through `mapLower`, whose
`lowerC` changes only ASCII `A`–`Z` and otherwise returns the code unchanged.

For `S = iCons(304,.IntSeq)`:

- the K entry claim with postcondition 0 closes (`#Top`, exit 0);
- the K entry claim with the real submitted-Python result 1 gets stuck at a
  final K result of 0 (exit 1);
- CPython executes `"\u0130".lower()` as code points `[105,775]`, so the actual
  submitted program counts the ASCII `i` and returns 1;
- the trusted canonical returns 0.

Evidence:
[`spec-unicode-zero.k`](evidence/spec-unicode-zero.k),
[`spec-unicode-one.k`](evidence/spec-unicode-one.k),
[`unicode-kprove-zero.log`](evidence/unicode-kprove-zero.log),
[`unicode-kprove-one.log`](evidence/unicode-kprove-one.log), and
[`unicode-python-witness.log`](evidence/unicode-python-witness.log).

The direct LLVM parser cannot construct a non-ASCII `Str` literal because the
supplied `strToCodes` rule is explicitly ASCII-only; that attempted `krun`
exited 113 and is recorded in [`unicode-k-zero.log`](evidence/unicode-k-zero.log).
It is not treated as proof evidence or as an infrastructure failure. The ground
reachability claims avoid that parser boundary by supplying the exact
`str(iCons(304,.IntSeq))` value and give the decisive model result.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. The fresh
[`spec-vacuity.k`](evidence/spec-vacuity.k) changes the unrestricted main
postcondition from:

```text
specifiedVowels(S)
```

to the false:

```text
specifiedVowels(S) +Int 1
```

The original precondition is satisfiable; for example, `S = .IntSeq` returns 0
but the mutation demands 1.

The mutated artifact built successfully:

```text
kprove spec-vacuity.k --definition verification-kompiled
  --spec-module SPEC-VACUITY --dry-run
exit 0
```

The actual proof failed for the expected unmet result obligation:

```text
kprove spec-vacuity.k --definition verification-kompiled
  --spec-module SPEC-VACUITY --output pretty
WarnStuckClaimState
... summary +Int 1 #Equals summary ...
exit 1
```

See [`stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log) and
[`stage6-vacuity-kprove.log`](evidence/stage6-vacuity-kprove.log). This is a
meaningful non-vacuity pass: the positive entry claim constrains the return
value. It does not cure the unsound theory used to obtain that value.

## 7. Proven versus assumed accounting

### What the successful K runs establish

Under the supplied K theory plus all rules in `verification.k`, the exact
constructor term regenerated from the submitted program reaches
`specifiedVowels(S)` from the exact main configuration for every formal
`S:IntSeq`. Separately, under `VOWELS-BASE` without the operational bridge, the
loop-summary claim closes by symbolic execution/circularity for environment 1
and the other cells fixed by that claim.

That is a theorem about this K theory. It is not a legitimate theorem that the
real generated Python program satisfies the source contract over the full
Python-string domain.

### Trust ledger

| Boundary | Influence and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell prover, K `Int`/`Bool`/`Map`/`List` theories | All builds and claims | Ordinary low-level trusted computing base; fresh runs and exact versions recorded |
| Trusted `py2mpy.py` | Python-AST-to-constructor identity | Acceptable mounted trust boundary; byte identity plus expanded-KORE identity checked |
| Supplied semantics | All execution behavior | Integrity is exact, but integrity does not imply adequacy to CPython; Unicode `lower` is materially false on the claim's unrestricted domain |
| Candidate structural summaries | Loop and final result | Fully defined, terminating, and sound for the internal ASCII lowering model |
| Bridge-free loop claim | Intended connection theorem for the loop summary | Valid and body-sensitive over its stated complete configuration |
| Proof-local priority-40 loop rewrite | Main-claim closure | Illegitimate: strictly broader than the connection theorem and machine-checked to prove a false state transition |
| 25 supplied opaque `symbol(...)` primitives | None for this program | Inert; no result/control/state/postcondition dependence |
| Differential testing | Python implementation/canonical bridge on finite cases | Strong finite evidence only; exposes rather than repairs Unicode and empty-input divergences |
| Empty-input interpretation | Candidate returns 0; canonical raises | Documented boundary ambiguity around “word”; not needed for the verdict |

### Gate results and decision

- Real-program soundness / Kit Gate A: **FAIL**. The operational bridge has a
  larger match domain than its bridge-free justification and demonstrably
  proves a false scope transition.
- Intent adequacy / Kit Gate B: **FAIL** for the unrestricted contract and
  formal precondition. The submitted program, canonical, and K lower model
  disagree on a valid Python string, and the formal theorem contains no ASCII
  restriction.
- Evidence auditability / Kit Gate C: the reconstruction, differential,
  pinning, body-sensitivity, bridge witness, Unicode witness, and non-vacuity
  evidence are reproducible. This later evidence gate cannot rescue Gates A
  or B.

The proof is non-vacuous and pins the submitted constructor term, but it relies
on a materially unsound proof rule and proves the wrong real result on part of
its stated domain. Under the benchmark decision boundary, that is
`FAIL / NOT_LEGIT`, not a non-fatal concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
