# Independent adversarial audit — 51-remove-vowels

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied semantics. I reconstructed the source-only
definitions, obtained a fresh `#Top`, mechanically pinned the claim term to the
trusted translation of `solution.py`, validated the sole operational
specialization with a bridge-free exhaustive theorem, and observed the expected
failure under independent bridge, body, and postcondition mutations.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `51-remove-vowels`;
- condition `semantics`;
- mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The mode and trusted mounts agree: `/reference/reference-semantics` exists as a
real directory. There is therefore no infrastructure stop condition.

I independently checked every required record for this layout:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, the structured trace, and the present
`usage.json`. Historical `runtime-metrics.json` is absent but is not required
for `legacy-selected-stage1`. All required records are regular readable files,
and the required roots are real directories rather than symlinks.

The campaign object in `/audit-campaign-lock.json` exactly equals the campaign
block in `/audit-input.json`; its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The independently computed file hashes for the run manifest, task manifest,
stage-one result, invocation, metrics, prompt, usage, output log, final text,
canonical, prompt, and translator all match their launcher records.

The launcher-compatible tree digest of the mounted candidate is
`a6af721cd4f96f6fd53edcff3816bda999b9a54b6fb1d6bc3132b5ac88028226`,
matching both the invocation and stage-one result. The trusted and candidate
reference-semantics trees both have manifest digest
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
A separate recursive comparison checked types, relative names, and file bytes
for all 25 entries: there are no missing, additional, changed, mistyped, or
symlinked semantics entries. Candidate `prompt.py` and `py2mpy.py` are also
byte-identical to their trusted mounts.

The entire 369-line structured trace parsed as JSON: 84 tool calls have 84
outputs and the final usage agrees with `usage.json`. I also inspected the
generation output log. Its prior `#Top` and final report were treated only as
untrusted historical claims.

Evidence:

- [integrity script](evidence/integrity_check.py)
- [integrity log](evidence/stage1-integrity.log)
- [trace parser](evidence/trace_summary.py)
- [trace summary](evidence/stage1-trace-summary.log)

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for an input Python string, return the string
with vowels removed. Its examples establish case-insensitive removal of the ten
ASCII vowel characters `aeiouAEIOU`, preservation of order and all other
characters, and correct behavior for empty strings and newlines.

The trusted canonical returns the concatenation of characters whose
`s.lower()` is not one of `a`, `e`, `i`, `o`, `u`. The submitted implementation
uses an initially empty accumulator, iterates left to right, appends a character
exactly when it is not in `aeiouAEIOU`, and returns that accumulator. The extra
initial `char = ""` is semantically inert for nonempty inputs and makes the
empty-loop proof state explicit.

Running the trusted `/reference/py2mpy.py` on the scratch copy of `solution.py`
reproduced `solution.mpy` byte-for-byte. Both files have SHA-256
`b3cf89a61dce62002983fda7137a9b82d2a85a369ed4d4a56d14ae3d2cad2534`.

The independent differential test imported the trusted canonical and submitted
entry points separately. It checked:

- all 21 documented and selected boundary/branch cases;
- every Latin-1 character;
- every one of Python's 1,114,112 possible one-code-point strings, including
  surrogate code points;
- 2,800 deterministic generated multi-character strings (seed
  `0x51A0D17`);
- a long alternating vowel/consonant string.

There were zero mismatches across 1,117,191 inputs. This is finite/executable
evidence, not a replacement for the K proof. It also establishes that CPython's
per-character `lower()` behavior introduces no non-ASCII divergence from the
submitted exact-membership predicate.

Evidence:

- [translation fidelity](evidence/stage2-translation-fidelity.log)
- [differential script](evidence/differential_test.py)
- [differential result](evidence/stage2-differential.log)

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`. No candidate
definition, compiled directory, K cache, or Python cache was copied. The live
toolchain is K `v7.1.293` and Python `3.10.12`.

The concrete definition was freshly built from the trusted supplied semantics:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. Fresh `krun concrete-tests.mpy --definition runtime-kompiled`
also exited 0 with `.K`, `NoExc`, and exit code 0.

The proof definition was freshly built:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0. The positive target command was then run independently:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`. The source inventory confirms that `SPEC`
contains exactly four claims. They form one mutually circular proof group:
empty-loop, vowel-head loop, non-vowel-head loop, and entry. Proving the module
is the correct way to retain the mutually recursive loop circularities while
checking every claim.

The compiler warnings concern unused variables, or total functions in unused
parts of the fixed supplied semantics; there is no parse error, backend
uncertainty, timeout, or unexplored branch in the successful target run.

Evidence:

- [toolchain](evidence/stage3-toolchain.log)
- [LLVM build](evidence/stage3-llvm-build.log)
- [concrete run](evidence/stage3-concrete-tests.log)
- [Haskell build](evidence/stage3-haskell-build.log)
- [fresh positive proof](evidence/stage3-kprove-all.log)

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

The four claims mean:

1. **Empty loop.** With an empty remaining string, `#loop` is consumed and
   `text`, `result`, and `char` are unchanged.
2. **Vowel head.** If `C` is one of the ten vowel codes, looping over
   `C :: REST` leaves `C` out and finishes with
   `removeVowelCodesAcc(ACC, REST)`.
3. **Non-vowel head.** If `C` is not a vowel code, looping over `C :: REST`
   appends `C` to `ACC` and then filters `REST`.
4. **Entry.** Starting from the complete clean configuration, load the module,
   resolve and call `remove_vowels` on an arbitrary finite `CODES:IntSeq`, and
   return exactly `str(removeVowelCodes(CODES))`. The module-scope closure is
   preserved and every other configuration cell is pinned.

The loop claims match the real `For` control point. Their framed continuation
is sound: the fixed loop rules consume only the loop region and resume the
suffix. The material state footprint is precisely the local `result` and
`char`; `text` and the outer scopes are preserved. The final `char` on nonempty
loops is existential because it is irrelevant to the function return, while
the returned `result` remains fully constrained.

Program identity was checked mechanically, not textually. `kast
--expand-macros` produced KORE for both the freshly regenerated `solution.mpy`
module and the claim's `removeVowelsProgram`. Both outputs have SHA-256
`92327b81c64b18d1f1055857a4680190cb8d319195d10bcd629c51d6e1a01821`
and are byte-identical. Thus the claim executes the submitted function binding
and body; the macros do not substitute another algorithm.

Every precondition has a realizable ground witness. Examples include
`ACC=[120], REST=[]`; vowel head `C=97, REST=[98]`; non-vowel head
`C=98, REST=[97,99]`; and entry
`CODES=[97,66,233,69,10,117,122]`. Substitution yields respectively `"x"`,
`"xb"`, `"xbc"`, and `"Bé\nz"`, agreeing with both Python implementations.

The entry precondition does not bound length or enumerate examples. It accepts
every finite `IntSeq`, which includes every Python-string code-point sequence
and is broader than the source domain.

Evidence:

- [mechanical program pinning](evidence/stage4-program-pinning.log)
- [ground witness script](evidence/claim_witnesses.py)
- [ground witness results](evidence/stage4-claim-witnesses.log)
- [body mutation](evidence/verification-body-mutant.k)
- [body-mutation residual](evidence/stage5-body-sensitivity-kprove.log)

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers `semantics.k`, all 23 supplied helper K files,
`verification.k`, and `spec.k`. It records 949 declarations:

- 705 ordinary rules;
- 234 syntax declarations;
- 5 evaluation contexts;
- 1 configuration;
- 4 reachability claims.

It found 148 function-bearing syntax sentences, 110 `total` sentences, 7 macro
sentences, 46 priority-bearing rules, 35 concrete rules, 26 `owise` rules, 25
symbol declarations, no `functional` declaration, and no `simplification`
rule. The 25 supplied symbols comprise 22 explicit `no-evaluators` symbols and
three concrete-only float helpers (`floorFI`, `toF`, `ceilF`). All float, MD5,
and sorting symbols are unreachable here. The candidate adds no opaque symbol.

Each inventory entry has a corresponding explicit decision in
`stage5-rule-decisions.json`: 92 fixed declarations/rules are material, 814
fixed declarations/rules are unreachable, 22 fixed opaque declarations are
unreachable, and all 17 candidate declarations/rules plus all four claims are
classified individually. `stage5-used-construct-map.md` maps every constructor
in `solution.mpy` to its declaration, evaluation rule, control rule, and state
effect.

### Candidate proof extensions

| Extension | Class and decision |
|---|---|
| `vowelCodes` | Compile-time constant macro containing exactly the ten literal codes. Sound. |
| `isVowelCode` | Total mathematical predicate over `Int`; one unconditional equation enumerates exactly the same ten codes. Sound. |
| Priority-40 `strContains(iCons(C,.IntSeq), vowelCodes)` rule | Pure operational specialization. It reads/writes no cells and has no control effect. Sound over its complete match domain; see connection proof below. |
| `removeVowelCodesAcc` | Definitional result summary. Empty/constructor coverage is complete, vowel/non-vowel guards are complementary, and recursion strictly descends on `REST`. Sound. |
| `removeVowelCodes` | Sound wrapper initializing the accumulator to empty. |
| Loop/body/program macros | Compile-time constructors, with the complete program macro mechanically equal to the translated source. Sound. |

The sole operational bridge required special scrutiny. I rebuilt a separate
definition importing only the fixed `MPY` semantics plus reviewer predicates;
it does not import the candidate bridge. Twenty-one reachability claims
partition all K integers into the ten vowel points and the eleven intervening
or exterior intervals. In each partition, fixed `strContains` drives a
state-observable branch to the same Boolean outcome as `isVowelCode`. The
complete bridge-free proof exits 0 with `#Top`. This is an exhaustive
connection theorem over the bridge's complete `C:Int` domain, not finite
testing.

The bridge is context-contained because it is a pure function rewrite: its
only observable is the Boolean value, it has no continuation manipulation,
and the connection proof observes both possible values through an actual
branch and scope update. Flipping its result to
`notBool isVowelCode(C)` still builds but makes the original proof fail with a
stuck accumulator equality. This rejects the opposite interpretation.

A separate mutation removes the material `result += char` from the macro that
the claim actually executes. That definition also builds, but the proof fails
on the expected non-vowel accumulator equality. The theorem is therefore
sensitive to the executed body.

The fixed material rule families preserve left-to-right evaluation, lexical
lookup, argument binding, scope allocation/pop, string iteration, guard
evaluation, string concatenation, and return. No heap allocation, exception,
output, or hidden state effect occurs on this program path. The loop claims
frame all cells untouched by those rules.

I found no unsound candidate rule and therefore make no unsupported
unsoundness allegation or false-conclusion witness. Fixed-semantics rules for
unused language features remain the declared supplied-semantics trust boundary;
they cannot match a reachable head symbol in this submitted execution.

Evidence:

- [complete inventory](evidence/stage5-k-inventory.json)
- [inventory generator](evidence/k_inventory.py)
- [per-entry decisions](evidence/stage5-rule-decisions.json)
- [decision generator](evidence/rule_decisions.py)
- [used-construct map](evidence/stage5-used-construct-map.md)
- [bridge-free theorem sources](evidence/connection-spec.k)
- [bridge-free proof](evidence/stage5-bridgefree-kprove.log)
- [opposite bridge mutation](evidence/verification-bridge-mutant.k)
- [opposite bridge residual](evidence/stage5-opposite-bridge-kprove.log)
- [body-sensitivity residual](evidence/stage5-body-sensitivity-kprove.log)

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

I created a new `SPEC-VACUITY` module. It changes only the entry result from
`removeVowelCodes(CODES)` to that sequence with code 120 (`"x"`) appended.

The mutation is demonstrably false on a satisfying state:
`CODES=.IntSeq` represents input `""`; the real program returns `""`, while
the mutated obligation requires `"x"`.

`kprove --dry-run` exits 0, establishing that the mutation parses and builds.
The real mutation proof exits 1 with `WarnStuckClaimState`. Its residual is the
expected unmet equality

```text
removeVowelCodesAcc(.IntSeq, REST)
= seqConcat(removeVowelCodesAcc(.IntSeq, REST), iCons(120,.IntSeq))
```

This is a reached, result-bearing failure—not a parser error, missing import,
timeout, or unrelated backend crash.

Evidence:

- [false mutation](evidence/spec-vacuity.k)
- [satisfying witness](evidence/stage6-vacuity-witness.md)
- [successful dry run](evidence/stage6-vacuity-dry-run.log)
- [expected stuck proof](evidence/stage6-vacuity-kprove.log)

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied `MPY` semantics, for every finite `CODES:IntSeq`, execution
of the exact submitted `remove_vowels` body from the entry configuration
reaches the returned value obtained by deleting precisely codes
`65,69,73,79,85,97,101,105,111,117`, preserving order. This is a
result-constraining partial-correctness theorem, supported coinductively by the
three loop cases. The operational membership specialization is independently
connected to fixed execution over its complete domain.

### Trust and evidence ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `v7.1.293`, Haskell backend, SMT, and builtin integer/Boolean/map theories | All symbolic results | Standard low-level proof-engine trust boundary; version and fresh outputs recorded. |
| Immutable supplied `MPY` semantics | Meaning of translated execution | Required fixed semantics for this condition; recursively integrity-checked and exhaustively inventoried. All material operations were reviewed. |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Trusted input, reinforced by byte-identical regeneration and KORE identity of the executed term. |
| Human meaning of the ten vowel codes | Contract adequacy | The equations directly express case-insensitive ASCII vowels from the prompt/examples. Canonical-vs-generated testing covers every Python one-code-point string and broader sequences with zero mismatches. |
| Twenty-five supplied proof-domain symbols for float/MD5/sort | Other tasks/features | None is reachable or result-bearing here; no target claim depends on one. |
| Manual macro duplication in `verification.k` | Artifact maintenance | Not an immutable-proof defect: trusted regeneration plus macro-expanded KORE equality pins this candidate. A real body mutation invalidates the proof. |
| Python differential testing | Implementation/canonical evidence | Finite/exhaustive-on-singletons evidence only; it does not substitute for the K reachability proof. |

There is no empirical oracle, fresh opaque value, or assumed program-defined
helper feeding the returned result. The only initially suspicious bridge has a
fresh bridge-free universal validation and sensitivity checks.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust and
auditability) all pass. The formal domain is not materially narrowed: arbitrary
finite `IntSeq` inputs cover the unrestricted Python-string contract rather
than finitely many sizes or examples.

Stage 7 result: **PASS**.

VERDICT: PASS
LEGITIMACY: LEGIT
