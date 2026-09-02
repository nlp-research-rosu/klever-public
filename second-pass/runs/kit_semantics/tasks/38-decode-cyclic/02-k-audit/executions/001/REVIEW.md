# Adversarial audit: 38-decode-cyclic

## Audit result

The candidate contains a legitimate partial-correctness proof of the submitted
program. I reconstructed the supplied semantics and proof definition from
source, obtained `#Top` for all four positive claims, mechanically pinned the
entry term to the freshly translated program, reviewed every local K
declaration/rule, and rejected a fresh false-result mutation for the expected
semantic reason.

The proof is relative to the launcher-supplied reference semantics and the K
toolchain, as required by `SUPPLIED_SEMANTICS`. It neither narrows the HumanEval
string domain nor replaces any program-defined operation with a proof-local
bridge or oracle.

## 1. Input and provenance integrity

### Declared layout and mode

`/audit-input.json` declares:

- problem `38-decode-cyclic`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- the mounted paths used in this audit.

The mode and mounts agree: `/reference/reference-semantics` is present as a
real directory. No infrastructure contradiction was found.

I read the required launcher/generation records:

- `/audit-input.json`;
- `/audit-campaign-lock.json`;
- `/run.json`;
- `/task.json`;
- `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/runtime-metrics.json`;
- `/generation-evidence/usage.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`; and
- the 392-line JSONL trace below `/generation-evidence/codex-trace`.

All required records are readable regular files, the trace is valid JSONL, and
there are no symlinks under the candidate, trusted reference, or generation
mounts.

### Lock, hashes, and source integrity

The parsed campaign lock is exactly equal to the `audit_campaign` object in
`/audit-input.json`. Its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value.

The recorded byte hashes for the canonical program, prompt, translator, run
manifest, task manifest, generation result, invocation, metrics, runtime
metrics, usage record, generation prompt, last message, and output log all
match their mounted files. The independently reimplemented pipeline-v3 tree
hashes also match:

- candidate tree:
  `c8bbd396936ed49aeff26ea34563d23604ef39ee01b66cbb3fa40ccd695d45cf`;
- supplied-semantics manifest:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- structured trace:
  `8af86d2a71f4d6da1a3bcf908d3a1e8ebf45aadccf00f8a628d5aa78529366d4`.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. Recursive path, entry-type, and byte comparison found the candidate
`reference-semantics/` identical to the trusted tree: 24 regular files plus
one directory, with no missing, additional, mistyped, changed, or linked
entry. In particular, the candidate made no semantics change.

Candidate-provided compiled directories were observed but were never copied
into or used by the reconstruction.

Evidence:

- [integrity checker](evidence/stage1_integrity.py)
- [integrity command and output](evidence/stage1_integrity.log)

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt defines `encode_cyclic` as follows:

1. partition the string into consecutive groups of at most three characters;
2. rotate every complete triple left, `[a,b,c] -> [b,c,a]`; and
3. leave a final group of length zero, one, or two unchanged.

`decode_cyclic` must invert that operation. The trusted canonical implementation
returns `encode_cyclic(encode_cyclic(s))`. On a complete triple, two left
rotations produce `[c,a,b]`; shorter tails remain unchanged.

The candidate implementation accumulates characters into `group`. At length
three it appends `group[2] + group[:2]`, resets the group, and finally appends
the residual tail. Thus it implements the same `[a,b,c] -> [c,a,b]`
transformation for every complete triple and preserves the final short group.
Its public signature is the required `decode_cyclic(s: str)`.

### Trusted regeneration

In the scratch workspace I ran:

```bash
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -l solution.mpy solution.regenerated.mpy
```

Both commands exited 0; `cmp` printed nothing. Both files have SHA-256:

```text
82a7da13d81ad63d3ce25bac5c868eb315f860a840816a47fa9507f077215cb1
```

Evidence:

- [translation log](evidence/stage2_translate.log)
- [byte-comparison log](evidence/stage2_mpy_cmp.log)
- [translated hashes](evidence/stage2_mpy_sha256.log)

### Independent differential test

The reviewer-authored script imports `/reference/canonical.py` and
`/candidate/solution.py` by explicit path. It compares:

- direct canonical and candidate decoding;
- canonical encoding followed by candidate decoding;
- empty and lengths around every modulo-three branch boundary;
- NUL and other control characters;
- combining characters, non-ASCII BMP characters, and astral Unicode;
- all strings of lengths 0 through 8 over `"aB0!"`; and
- 10,000 deterministic strings of lengths 0 through 100 over a mixed Unicode
  alphabet.

Exact command:

```bash
python3 /audit-output/evidence/stage2_differential.py
```

Actual result:

```text
total_cases=97401
input_stream_sha256=e9607dab59930857de71feba80ee0d9ac58cf56a58a7c29fd522ab9b66f5c25a
canonical_candidate_mismatches=0
encode_decode_roundtrip_mismatches=0
```

The command exited 0. The deterministic generator and seed preserve the input
set.

Evidence:

- [differential script](evidence/stage2_differential.py)
- [differential log](evidence/stage2_differential.log)

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/audit-38-20260729`. The semantics copy came from the trusted
reference mount. The directories `runtime-audit-kompiled` and
`verification-audit-kompiled` were generated there from source; no
candidate-provided definition or cache was used.

The active tools report K version `v7.1.293`.

### Concrete definition and execution

Exact build:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

Exit: 0. The compiler emitted non-exhaustiveness warnings for unrelated
fixed-semantics helpers. None occurs in this program.

I translated and ran a reviewer-authored program containing the exact submitted
function body and assertions for lengths 0 through 9, both branch outcomes,
complete groups, residual tails, and encoded examples:

```bash
python3 py2mpy.py /audit-output/evidence/stage3_concrete.py \
  > stage3_concrete.mpy
krun stage3_concrete.mpy --definition runtime-audit-kompiled
```

Both commands exited 0. The final configuration has:

```text
<k> .K </k>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

Evidence:

- [concrete test source](evidence/stage3_concrete.py)
- [LLVM build log](evidence/stage3_kompile_llvm.log)
- [concrete translation log](evidence/stage3_translate_concrete.log)
- [concrete execution log](evidence/stage3_krun_concrete.log)

### Proof definition and positive claims

Exact proof build:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Exit: 0.

The complete positive proof:

```bash
kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC
```

exited 0 and printed `#Top`.

I additionally selected each loop claim:

```bash
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.loop-empty
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.loop-one
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.loop-two
```

Each exited 0 and printed `#Top`. The entry proof needs the loop circularities,
so I also ran the explicit complete selection:

```bash
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-empty,SPEC.loop-one,SPEC.loop-two,SPEC.decode-entry
```

It exited 0 and printed `#Top`.

Evidence:

- [Haskell build log](evidence/stage3_kompile_haskell.log)
- [complete proof log](evidence/stage3_kprove_all.log)
- [loop-empty log](evidence/stage3_kprove_loop_empty.log)
- [loop-one log](evidence/stage3_kprove_loop_one.log)
- [loop-two log](evidence/stage3_kprove_loop_two.log)
- [entry with invariants log](evidence/stage3_kprove_decode_entry_with_invariants.log)

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Claims in plain language

The three loop claims require:

- a current local environment location `L >= 1`;
- the exact builtins and module-parent chain;
- locals `s`, `result`, `group`, and `char`;
- no pending return or exception; and
- arbitrary but preserved heap, allocation counters, stack, exit code, and
  continuation.

Their postconditions are:

- `loop-empty`: starting with no buffered character, process every remaining
  code, append each completed triple as `[third,first,second]`, leave the
  final short tail in `group`, and set `char` to the last iterated character;
- `loop-one`: the same property when `group` initially contains one code `A`;
- `loop-two`: the same property when `group` initially contains two codes
  `A,B`.

The entry claim has no additional `requires` clause. It starts from the exact
initial module configuration, loads:

```k
Module(FuncDef("decode_cyclic", Params("s"), decodeFunctionBody))
```

resolves the resulting binding, calls it with arbitrary `str(INPUT:IntSeq)`,
and requires the returned value to be exactly:

```k
str(decodeCodes(INPUT))
```

It also requires normal return/frame cleanup: module environment restored,
empty stack and heap, `noRet`, `NoExc`, unchanged allocation counters, and
exit code 0. The result is not a free variable, an implication antecedent, or
a tautology.

### Satisfiable states

Concrete satisfiers exist for every precondition:

- `loop-empty`: `L=1`, `IS=.IntSeq`, empty accumulator/group, and any valid
  old `char`;
- `loop-one`: `L=1`, `group="a"`, `IS=.IntSeq`, and `char="a"`;
- `loop-two`: `L=1`, `group="ab"`, `IS=.IntSeq`, and `char="b"`;
- `decode-entry`: the exact initial cells shown in the claim and
  `INPUT=[98,99,97]` (`"bca"`).

For the entry witness, a fresh ground K claim proved to `"abc"` with `#Top`,
and both trusted canonical Python and candidate Python returned `"abc"`.

Evidence:

- [ground K witness](evidence/stage4_ground_witness.k)
- [ground proof log](evidence/stage4_ground_kprove.log)
- [ground Python comparison](evidence/stage4_ground_python.py)
- [ground Python log](evidence/stage4_ground_python.log)

### Mechanical program pinning

I parsed both:

1. the freshly regenerated `solution.mpy`; and
2. the entry claim's `Module(FuncDef(..., decodeFunctionBody))`

with `kast`, using module `VERIFICATION`, sort `Module`, and
`--expand-macros`. The expanded JSON KAST files are byte-identical and both
hash to:

```text
628c5fd0dc632b11251c126e74b348d1c6947487a0bed4873f5759de1d3578e3
```

This is constructor-level identity, including the function binding and body.
The only normalization is expansion of candidate macros into those exact
constructors.

Evidence:

- [claim program term](evidence/stage4_claim_program.mpy)
- [solution parse log](evidence/stage4_kast_solution.log)
- [claim parse log](evidence/stage4_kast_claim_program.log)
- [constructor comparison](evidence/stage4_constructor_cmp.log)
- [expanded hashes](evidence/stage4_constructor_sha256.log)

### Body sensitivity and source-contract domain

I independently ran the preserved body mutation against the fresh definition.
It changes the executed result-building expression itself, not an external
source file. The mutated body reached `"bca"` where the destination required
`"abc"`; `kprove` exited 1 with `WarnStuckClaimState`.

Evidence: [body-sensitivity log](evidence/stage4_body_sensitivity.log).

The formal input `str(INPUT:IntSeq)` is unbounded over every finite `IntSeq`.
It therefore covers every Python string represented as a finite sequence of
code points; it is not a finite-size or example-only theorem. Allowing
arbitrary integers is broader than valid Unicode but does not invalidate the
intended subset because every operation in this function is code-value
parametric.

The postcondition matches the canonical contract blockwise:

```text
prompt encode:   [a,b,c] -> [b,c,a]
encode twice:    [a,b,c] -> [c,a,b]
decodeCodes:     [a,b,c] -> [c,a,b]
tail length < 3: unchanged by both
```

This is a direct exhaustive argument over the four possible group shapes,
not reliance on testing alone.

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated inventory covers all 26 K source files used by the
proof: the supplied `semantics.k`, its 23 helper files, `verification.k`, and
`spec.k`. It contains 951 line-addressable records:

| Kind | Count |
|---|---:|
| configuration | 1 |
| contexts | 5 |
| syntax declarations | 83 |
| function declarations | 150 |
| equational rules | 425 |
| operational rules | 283 |
| reachability claims | 4 |

Every record has an explicit disposition in the companion matrix. Fixed
declarations/rules not reachable from this program are marked unused rather
than silently treated as proof evidence. The matrix identifies 127 used fixed
rules and 53 used fixed declarations/configuration records; every
proof-local record is separately classified.

Evidence:

- [inventory generator](evidence/stage5_inventory.py)
- [complete inventory](evidence/STAGE5_RULE_INVENTORY.md)
- [disposition generator](evidence/stage5_review_matrix.py)
- [complete disposition matrix](evidence/STAGE5_RULE_REVIEW_MATRIX.md)

### Proof-local extensions

`verification.k` contributes exactly:

| Extension | Class | Soundness finding |
|---|---|---|
| `decodeLoopBody` | syntax macro | Exact constructor fragment; no runtime match or state effect. |
| `decodeFunctionBody` | syntax macro | Expanded program is byte-identical at JSON KAST level to regenerated `solution.mpy`. |
| `decodedResult` | definitional summary | Four disjoint/exhaustive `IntSeq` cases; the recursive case consumes three constructors and appends `[C,A,B]`. |
| `decodedTail` | definitional summary | Four disjoint/exhaustive cases; the recursive case consumes three constructors and returns only the residual 0–2 codes. |
| `decodeCodes` | definitional summary | Concatenates the exact completed-group result and exact residual tail. |
| `finalLoopChar` | definitional summary | Empty case preserves the old target; cons case records the one-code string and strictly recurses. |

All four proof-local functions declared `[total]` are constructor-exhaustive
and structurally decreasing. Their guards/patterns do not overlap with
different right-hand sides. None rewrites a program term or cell. There are no
proof-local `[simplification]`, `[concrete]`, `[functional]`, `[priority]`, or
opaque-symbol declarations.

The three auxiliary claims are derived reachability circularities, not rules
in the proof definition. They execute the fixed `#loop` and exact body. The
entry claim executes fixed module loading, lookup, call, parameter binding,
statements, return, and frame popping.

### Used source constructs and fixed rules

The actual program's constructs map to fixed semantics as follows:

| Program construct | Fixed declarations/rules |
|---|---|
| `Module`, statement list | `syntax.k`; `core.k` `#loadAll` and statement sequencing |
| `FuncDef`, `Call`, `Return` | `functions.k` closure creation/binding/return/pop; `call.k` callee/argument dispatch and frame creation |
| `Name`, `len` | `core.k` scope-chain lookup and `builtinsScope`; `builtins.k` `applyBuiltin("len",...)`, `seqLen`, `isLen` |
| literals/docstring | fixed `Int` and `Str` rules; `strToCodes` is used only on ASCII source literals |
| assignments | strict RHS evaluation from `syntax.k`; `controls.k` current-scope update |
| `for char in s` | strict iterable evaluation, `str.k` iterator rules, and `controls.k` `#loop/#loopStep` |
| `if len(group) == 3` | call evaluation, integer equality, strict `If`, `truthy`, and `#branch` |
| string `+` | sequential operand evaluation and `str.k` `seqConcat` |
| `group[2]` | subscript contexts, `normIdx`, `applyIndex(str,...)`, and `intSeqAt` |
| `group[:2]` | ordered bound evaluation, default step 1, clamping, and `buildIS` |

The semantics preserves left-to-right expression/argument evaluation through
strictness or explicit contexts. The source performs no mutation, allocation,
I/O, exception handling, closure capture, or abrupt loop control. The only
state changes are the local bindings `result`, `group`, and `char`; the loop
claims constrain each and preserve every other active cell. The module lookup
chain contains no shadowing binding for `len`, so lookup reaches the fixed
builtin.

The index `2` is executed only after `len(group) == 3`, so the fixed semantics'
underspecification for out-of-bounds `intSeqAt` is unreachable. The slice uses
`NoBound, 2, NoBound`, hence step 1; unsupported step-zero behavior is
irrelevant. The fixed ASCII-only literal conversion processes only the
ASCII docstring and empty string literals; the arbitrary symbolic input enters
directly as `str(INPUT)` and is not passed through that literal conversion.

### Priorities, opaque symbols, and totality

Every priority rule is listed in the full inventory. No priority rule is
enabled on this program's proof path: the relevant high-priority rules concern
heap references, closure cells, special calls, list mutation, or other unused
constructs. Generic fixed execution handles the submitted body.

The supplied proof module contains opaque/no-evaluator facilities for:

- `sortVS`, `sortKeyVS`, and `md5hexCodes`;
- `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`;
- `floorFI`, `toF`, `ceilF`;
- `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`;
- `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
  and `sqrtF`.

None of these symbols occurs in the program, proof-local summaries, claims, or
residuals. They have no value, branch, control, state, or postcondition
influence here. The fixed compiler warnings for unrelated total functions
likewise do not affect this theorem.

No rule that can derive a false conclusion on the intended execution path was
found. Consequently, there is no unsound-rule witness to report. Unused
fixed-semantics approximations remain part of the launcher-designated
semantics trust boundary, not candidate proof extensions.

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

I did not reuse the candidate `spec-vacuity.k`. The fresh mutation uses
satisfying input `"abcd"` and changes only the result obligation:

```text
actual/canonical destination: "cabd"
mutated false destination:    "cabx"
```

The independent Python witness confirms both implementations return `"cabd"`
and that it differs from `"cabx"`.

First, the mutation was parsed and compiled without executing it:

```bash
kprove stage6_false_result.k \
  --definition verification-audit-kompiled \
  --spec-module STAGE6-FALSE-RESULT \
  --dry-run
```

Exit: 0.

Then:

```bash
kprove stage6_false_result.k \
  --definition verification-audit-kompiled \
  --spec-module STAGE6-FALSE-RESULT
```

exited 1 with `WarnStuckClaimState`. The residual is:

```k
str(iCons(99, iCons(97, iCons(98, iCons(100, .IntSeq)))))
```

which is the actual `"cabd"` result. The failure is therefore the expected
unmet result obligation, not a parse error, missing import, timeout, or
unreachable mutation.

Evidence:

- [fresh false claim](evidence/stage6_false_result.k)
- [Python witness](evidence/stage6_false_result_python.py)
- [Python witness log](evidence/stage6_false_result_python.log)
- [successful dry-run log](evidence/stage6_false_result_dry_run.log)
- [expected proof-failure log](evidence/stage6_false_result_kprove.log)

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the K proof establishes

For every finite `INPUT:IntSeq`, from the exact entry configuration in
`SPEC.decode-entry`, fixed semantics loads and binds the exact submitted
function body, calls it with `str(INPUT)`, and reaches normal return with:

```k
str(
  seqConcat(
    decodedResult(.IntSeq, INPUT),
    decodedTail(INPUT)))
```

where `decodedResult` maps every complete `[A,B,C]` block to `[C,A,B]` and
`decodedTail` preserves the remaining zero, one, or two codes. The proof also
establishes the claimed local-loop summaries and normal frame cleanup. Under
the Kit contract this is a partial-correctness result; no separate liveness
claim is asserted.

### Trust and evidence ledger

| Boundary | Influence | Classification and evidence |
|---|---|---|
| K v7.1.293 compiler, Haskell backend, rewriting engine, SMT integration | Proof parsing, execution, and reachability closure | Necessary low-level tool trust; fresh source builds and runs succeeded. |
| Launcher-supplied reference semantics | Defines Python-subset execution | Required fixed trust boundary for `SUPPLIED_SEMANTICS`; candidate copy is recursively identical. Every used rule was reviewed for this path. |
| Trusted `py2mpy.py` | Source-to-constructor translation | Required translator trust, strengthened by fresh byte-identical regeneration and constructor-level claim comparison. |
| Algebraic `IntSeq` string model | Represents Python character sequences | Adequate for this code-value-parametric program; intended Unicode cases are included. |
| Blockwise link from `decodeCodes` to canonical intent | Connects formal output to HumanEval wording/canonical code | Direct exhaustive mathematics over block lengths 0, 1, 2, and 3; not an opaque assumption. |
| CPython execution and trusted canonical implementation | Finite independent validation | Empirical support only, not a substitute for K proof. Direct program differential: 97,401 cases, zero mismatches. |
| Supplied opaque float/sort/MD5 symbols | None | Unused; no claim depends on them. |

As an additional finite check of the formal summary bridge, a reviewer-authored
model of the explicit `decodedResult`/`decodedTail` equations was compared
against the trusted canonical entry point:

```text
total_cases=97394
input_stream_sha256=ac21af401fd98955e57a97e903e26c8d02c5323e812d6db564df49967251dfbb
mismatches=0
```

Evidence:

- [summary differential script](evidence/stage7_summary_differential.py)
- [summary differential log](evidence/stage7_summary_differential.log)

Excluded behavior is limited to non-string calls and Python facilities absent
from the submitted body. The formal theorem is not bounded by input length and
does not omit any material behavior in the source contract.

### Gate and final decision

- Gate A, real-program soundness: **PASS**. Exact body execution, no bridge or
  oracle, sound summaries, satisfiable preconditions, body sensitivity, and
  fresh non-vacuity all hold.
- Gate B, intent adequacy: **PASS**. The theorem covers the full string domain
  and its explicit block transformation is the canonical inverse.
- Gate C, trust/evidence auditability: **PASS**. Assumptions and unused opaque
  facilities are named, and all dynamic evidence is reproducible.

The prior `#Top`, `PROOF.md`, compiled definitions, traces, and final generation
report were not relied upon. The independently reconstructed evidence supports
the candidate's legitimacy with no material adequacy or soundness gap.

VERDICT: PASS
LEGITIMACY: LEGIT
