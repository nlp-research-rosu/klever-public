# Independent audit: HumanEval `15-string-sequence`

## Scope and result

I audited condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, in launcher mode `CLASSIFICATION_AND_PROOF`. I treated
the Stage 1 workspace, prior Stage 2 review, Stage 3 classification, Stage 4
generation, Stage 5 candidate, logs, and comments as untrusted evidence. The
trusted code under `/reference/tools` was used for inventory reconstruction,
hashing, preflight, and the final mechanical gate; classification and
operational adequacy were judged independently from the frozen source and
semantics.

The audit passes. There are six rules in the local verification-module
closure: five genuine definitions and one genuine, relevant domain lemma.
Stage 4 maps that domain lemma bijectively to one exact Lean obligation. The
Stage 5 candidate clean-builds, proves exactly the immutable generated target,
uses no candidate-added trust escape, and supplies operationally faithful
definitions on the complete domain exercised by the obligation.

## Input and producer integrity

`AUDIT_MODE` and `/audit-input.json` both record
`CLASSIFICATION_AND_PROOF`. The launcher-selected Stage 4 status is `PASS`,
not `KLEAN_NO_OBLIGATIONS`, so a generated target and Stage 5 proof are
required.

All mounted launcher hashes recomputed exactly:

| Input | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 pipeline tree | `9efe5dd77f40e3e3de6ba6a478fc84970a622a7a0b88846317a3d6a2c6e25316` |
| Stage 1 Klean export tree | `cf214e76b153246b2c03dbd7d08b93de5be4c5e2de95ec588952791e146dca07` |
| Stage 3 discovery manifest | `9ca004938b0eb0cc46c64461dab10cbc33e54848d6eff8031093461206211681` |
| Selected Stage 2 audit tree | `de53031b4c5af427938107c223feb85b8bf4e31304af2ee6301e5f190c43c87f` |
| Selected Stage 4 generation tree | `2b9673b9911eeb5da0ea3024046cae185863930af307966a424a944a67630453` |
| Producer-source bundle tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |
| Generated project tree | `03184370be88a4be25b7705af84c8dc4b2badc459cece616bb0eb2be7b87b16e` |
| Stage 5 candidate workspace tree | `bf5738366cc2bd2b9bef537cc49c3ab9e4e2f14b9cfc151fd58ac45b866f0f56` |

The entire launcher map of 775 Stage 1 regular-file hashes also matched with
no missing, extra, or changed file. The launcher records a Stage 5 invocation
tree hash, but that invocation directory is not one of the mounted audit
inputs; it was not treated as proof evidence. The mounted candidate workspace
hash and the signed audit-input binding were both independently accepted by
the trusted final gate.

Before judging Stage 4, I hashed the exact mounted producer sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

These match `generator-manifest.json` and
`generation-tools/source-manifest.json`. Both manifests and the launcher path
bind the same generator image:
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
The producer bundle contains exactly those two sources and its source
manifest. There is therefore no producer-provenance `AUDIT_ERROR`.

Evidence:
`evidence/08_inventory_reconstruction.txt`,
`evidence/11_producer_provenance_launcher_hash.txt`, and
`evidence/21_recorded_hashes.txt`.

## Rule-inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`. `prove.sh` selects `VERIFICATION`; its local closure
inside `verification.k` is just `VERIFICATION` (the imported `MPY` module is
in the frozen supplied-semantics files, not another local module in
`verification.k`).

The reconstructed `verification.k` hash is
`ee81e70e2574494a39476eaf9c16e78fd279a5ca657a62a56978a63a23e8aa1b`.
The canonical six-rule inventory hash is
`88adbf942eb1c766f28585672f908061a5c3385bad356f21790fe5db810b2d20`.

The protected Stage 3 manifest has exactly six unique IDs, in exactly the
reconstructed order. Its inventory hash matches. There are no omissions,
extras, duplicate identities, changed normalized hashes, reordered
identities, or unclassified rules. Stage 4's enriched source records also
match the reconstructed text, source spans, normalized hashes, and IDs.

## Independent classification

| Lines | Source rule ID | Classification | Independent judgment |
|---|---|---|---|
| 10–12 | `rule-fef3abb92ec888abf14e3bf9a2fd8f282df0e342c4122d6cd092d876bcb85646` | `DEFINITION` | Guarded base equation for the named `sequenceAcc` summary: once `I > N`, the accumulator is the result. |
| 14–22 | `rule-43f49722bb57ff9eafcc5227f4b4353cd12742df4bb56c784efe6e413736cdbf` | `DEFINITION` | Guarded recurrence for `sequenceAcc`: append space plus the decimal rendering of `I`, increment `I`, and recur. `[concrete]` controls symbolic unfolding but does not change its definitional role. |
| 26–28 | `rule-d55499ddc47bd6adf4d30b16fdbd3314a5db1919e0074fd704e4bfe2e4543f7c` | `DEFINITION` | Symbolic form of the same base equation, provided for simplification. It defines the base behavior of the named summary. |
| 30–38 | `rule-5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc` | `DOMAIN_LEMMA` | Reverse-oriented fold of the recurrence under `I <= N`. It is mathematically true but is proof-closing rather than a definition. |
| 44–45 | `rule-02288b5620299a0a1ac5b02b112560d2ffdd21df6457ef2054ea9f3746dbef3b` | `DEFINITION` | Negative-input equation for the named result summary `stringSequenceCodes`. |
| 47–49 | `rule-975c7f6f0a3b75ffe8b642274c4103c08f2594d0bccd1678e974201218b3ab16` | `DEFINITION` | Nonnegative-input equation for `stringSequenceCodes`, seeding `"0"` and invoking `sequenceAcc` at counter one. |

The line 30–38 rule states, under `I <= N`,

`sequenceAcc(append(ACC, " " ++ Int2String(I)), I + 1, N)
 = sequenceAcc(ACC, I, N)`.

It is the symmetric use of the line 14–22 recurrence. Stage 1 does not first
prove this exact rule against a module from which it is absent: `prove.sh`
compiles `verification.k` with the rule already installed and then runs the
two claims together. It therefore cannot be labeled
`PROVED_DERIVED_LEMMA`; `DOMAIN_LEMMA` is the correct classification.

The lemma is directly relevant. The loop invariant in `spec.k` changes
`result` from `ACC` to the same appended accumulator and increments `i`;
folding that updated summary back to `sequenceAcc(ACC,I,N)` is precisely the
inductive preservation step. The source program likewise performs
`result = result + " " + str(i)` followed by `i = i + 1`. This is not an
irrelevant mathematical fact and does not assert the final postcondition by
fiat.

Every rule with `[simplification]` is either one of the three `DEFINITION`
entries above or this `DOMAIN_LEMMA`. There are no local
`OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries.

Evidence:
`evidence/04_frozen_source_and_manifests.txt`,
`evidence/08_inventory_reconstruction.txt`, and
`evidence/09_stage1_derivation_and_relevance.txt`.

## Deterministic Stage 4 generation

I reran:

`PYTHONPATH=/reference python3 evidence/run_generation_preflight.py`

which calls `tools.klean_preflight.check_generation` with the required Stage
1 workspace, Stage 3 manifest, Stage 4 generation, and pinned toolchain lock.
The successful rerun returned:

- status `PASS`;
- one obligation;
- zero designated sorries;
- generated tree
  `03184370be88a4be25b7705af84c8dc4b2badc459cece616bb0eb2be7b87b16e`;
- clean generated-project `lake clean` and `lake build` exit codes 0.

The first invocation exposed a runner-specific procfs problem: Lean 4.22
looked up `/proc/<pid>/exe`, while this audit runner exposes the equivalent
`/proc/self/exe`. I preserved that failure, confirmed the pinned Lean
`ba2cbbf...` toolchain, and used the narrow compatibility shim in
`evidence/proc_compat.c`. The shim only retries a failed
`/proc/<pid>/exe` `readlink` as `/proc/self/exe`; it does not alter Lean
sources, proof terms, project files, or command results. With it, both the
mandated preflight and all independent clean builds succeeded.

The independently classified domain set has exactly one ID:
`rule-5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc`.
The Stage 4 input manifest, obligation map's source list, and obligation list
contain that ID exactly once and in the same order. Its source span is 30–38,
its normalized hash is
`5cd1e3b5568df299d3f434281eb340a991725f175ade15ddce1a4febdab6d0fc`,
and its generated conjunct hash is
`f25dae2bbb43062ed4b07b8428310a07338768f018a7b2bd34d0da4f020ccdda`.

The generated conjunct retains all three variables `N`, `I`, and `ACC`, the
guard `I <=Int N = true`, both nested `seqConcat` applications, the space code
32, `strToCodes(Int2String(I))`, `I +Int 1`, and both `sequenceAcc` calls.
It is the exact domain rule, not a weakened or unrelated statement.

The target is the exact one-conjunct proposition:

- declaration:
  `Klean15StringSequence.Lemmas.targetStatement`;
- definition hash:
  `5db5c5d4b927ead79bff158c90c901b775cdd37d4733cb49a27baf51dc429ea8`;
- applied statement hash:
  `f4089e414b7890c60d296ccb171c89777d1d4ca8f150af29d96a4016fb8ca342`.

The generated file, generator manifest, and `/audit-input.json` agree
exactly. There is no omitted or duplicate obligation and no target change.
The guard is satisfiable under the honest comparison definition; for example,
`I = 1`, `N = 3`, and `ACC = [88]` produce `true` and both sides evaluate to
`[88,32,49,32,50,32,51]`. Thus the sole conjunct is not vacuous.

Evidence:
`evidence/20_generation_preflight_rerun.txt` and
`evidence/22_stage4_identity.txt`.

## Stage 5 clean build, proof identity, and trust

I created `/tmp/audit-work/stage5-fresh`, copied the candidate into it, and
copied the immutable generated project into `Base`. I then ran, separately:

- `LD_PRELOAD=/tmp/audit-work/proc_compat.so lake clean`
- `LD_PRELOAD=/tmp/audit-work/proc_compat.so lake build`

Both exited 0; the clean command produced no output and the build ended
`Build completed successfully.` Every original generated entry in `Base`
remained byte-identical after the build, and its target still matched the
generator manifest.

The only non-`Base` Lean sources are `Proof.lean` and `lakefile.lean`.
Static checking found no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`
token in them. Each of the six required parameter definitions occurs exactly
once. The candidate does not declare, redefine, or shadow
`Klean15StringSequence.Lemmas.targetStatement`. It contains exactly one
`theorem final`, whose normalized type is exactly the generator's fixed
applied statement.

Running Lean on an independent audit source with both an exact type check and
`#print axioms Proof.final` produced:

`'Proof.final' depends on axioms: [propext]`

There is no `sorryAx`. `propext` is in the trusted final gate's Lean-core
allowance (`propext`, `Classical.choice`, and `Quot.sound`), not a
candidate-added declaration. None of the 42 generated declarations recorded
by `trust-inventory.json` is a dependency of `Proof.final`, and there is no
unrecorded axiom dependency. The trusted end-to-end final mechanical gate
also returned `PASS`, the exact target, and `used_axioms: ["propext"]`.

Evidence:
`evidence/24_stage5_lake_clean.txt`,
`evidence/25_stage5_lake_build.txt`,
`evidence/26_print_axioms.txt`,
`evidence/27_candidate_static.txt`,
`evidence/28_axiom_accounting.txt`, and
`evidence/33_trusted_final_mechanical_gate.txt`.

## Operational-bridge audit

All six target parameters are bound to the sole source rule and are materially
used by its translation.

| Candidate definition | Frozen meaning and judgment |
|---|---|
| `«_<=Int_» x y := decide (x ≤ y)` | Exact K unbounded-integer `<=Int` result, including negative and equality cases. |
| `«_+Int_» x y := x + y` | Exact K unbounded-integer addition; no overflow or truncation. |
| `«Int2String(_)_STRING-COMMON_String_Int» x := toString x` | Exact decimal integer rendering used by K `Int2String`, including a leading minus sign for negative integers. Its output is ASCII. |
| `«seqConcat(_,_)_MPY-STR_IntSeq_IntSeq_IntSeq» := seqConcatModel` | Exact structural equations from `str.k`: empty-left returns the right sequence; a head constructor is preserved and recursion continues on the left tail. |
| `«sequenceAcc(_,_,_)_VERIFICATION_IntSeq_IntSeq_Int_Int» acc i n := sequenceAccGo (n-i+1).toNat acc i` | Exact base and recurrence of `verification.k`. If `i > n`, fuel is zero and the result is `acc`; if `i <= n`, fuel is exactly the inclusive count `n-i+1`, and each step appends space plus the rendering of the current counter before incrementing. |
| `«strToCodes(_)_MPY-STR_IntSeq_String» s := intSeqOfChars s.toList` | Exact codepoint sequence on the complete matched domain. The frozen `strToCodes` rule is ASCII-only, and the generated obligation calls it only on `Int2String(I)`, whose range is ASCII; the source solution does the same. The candidate totalizes non-ASCII strings, but no target term or proof conclusion reaches that extra domain. |

The operational test evaluated true/false comparison boundaries, negative
addition and rendering, empty and nonempty concatenation, a loop base case,
positive and negative counters, and a concrete recurrence witness. Results
included:

- `-3 <= -2 = true`, `7 <= 7 = true`, `2 <= -1 = false`;
- `-9 + 4 = -5`;
- `Int2String(-120) = "-120"`;
- concatenating `[1,2]` and `[3,4]` yields `[1,2,3,4]`;
- `sequenceAcc([88],1,3)` yields
  `[88,32,49,32,50,32,51]`;
- `sequenceAcc([88],3,2)` yields `[88]`;
- `sequenceAcc([], -2, 0)` yields the codes for `" -2 -1 0"`;
- the concrete left and right sides of the generated rule are equal.

Counterfactual mutations confirmed why this semantic bridge check is
load-bearing:

1. Replacing `<=Int` with constant `false` still lets the theorem build by
   making its guard impossible. This mutant is mechanically convenient and
   operationally invalid. The actual candidate is not that mutant: it
   implements real integer comparison and has satisfiable true and false
   witnesses.
2. Replacing `sequenceAcc` with the constant accumulator causes the proof
   build to fail on the nonempty append equation.
3. Replacing `Int2String` with the constant empty string causes the proof
   build to fail because the recurrence step no longer matches the summary.

The actual definitions vary with their inputs, agree with the frozen rules on
the complete obligation domain, preserve sequence order and values, and
implement the source loop's inclusive counter behavior. They are not
constant, identity, hard-coded, or vacuous proof conveniences. The Unicode
totalization of `strToCodes` is outside the frozen rule's and theorem's match
domain and has no load-bearing effect.

Evidence:
`evidence/06_parameter_semantics_search.txt`,
`evidence/29_operational_adversarial_examples.txt`,
`evidence/30_mutation_guard_false.txt`,
`evidence/31_mutation_sequence_constant.txt`, and
`evidence/32_mutation_renderer_constant.txt`.

## Conclusion

The Stage 3 classification is complete and correct; the true domain set is
nonempty and contains exactly the reverse recurrence. Stage 4 has authentic
producer provenance and deterministically generates exactly one faithful
obligation and its fixed target. Stage 5 proves that target in a fresh clean
build without candidate trust escapes, and its six interpretations implement
the frozen operational meanings on the entire domain used by the theorem.

VERDICT: PASS
LEGITIMACY: LEGIT
