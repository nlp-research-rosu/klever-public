# Independent audit: HumanEval 115-max-fill

## Result

The protected Stage 3 classification is correct, the selected Stage 4
generation is authentic and bijective with the independently identified domain
lemma, and the Stage 5 candidate clean-builds and proves the exact fixed target
without axioms. Both target parameters implement their frozen K/KORE meanings;
the proof does not rely on coordinated but operationally false definitions.

Audit mode was `CLASSIFICATION_AND_PROOF`; condition was `kit-semantics`; the
semantics mode was `SUPPLIED_SEMANTICS`.

## Input and producer authentication

I treated all mounted prose, logs, comments, and prior verdicts as evidence
only. The trusted hashing code independently produced these matches:

- Stage 1 pipeline tree:
  `2dbdc057ac8a02489661eed53c54533d2bae263adce1fec0c40f9437c3c04365`.
- Stage 1 deterministic-export tree:
  `65f72949be70a5265ec83fcc3a10827f55dc9d312ee161a8b6d8b49f6cbabd1d`.
- Selected Stage 2 audit tree:
  `865895e981975765ffabeea928318532b87c72bcedfaa8737c3f9cb85d2622a3`.
- Stage 3 manifest:
  `72fd07596c391ded3f7fd11366397cbdb2eeef5a2059f112cf01fd7f96dc0a82`.
- Stage 4 generation tree:
  `0b2474e45c2698853c14df953c65a647735d34b7462357cafe47ff70f4639869`.
- Generated-project deterministic tree:
  `15ff8c29ed6d97fcabad6a92a502d46bc9ac0f30b30552742622e0c860edf9d4`.
- Stage 5 candidate pipeline tree:
  `778be8804f83a113eff27fc237397803fbea00707d0ede84405828363e6de47a`.
- All 789 Stage 1 per-file paths and SHA-256 values matched
  `stage1_source_hashes`, with no missing, extra, or changed file.

Before judging Stage 4, I hashed the two mounted producer sources:

- `klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`.
- `klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`.

Each value agrees with `source-manifest.json` and
`generator-manifest.json`. The source bundle contains exactly those two
producers and the source manifest. Its launcher tree hash is
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`.
The immutable generator image ID agrees across the source manifest, generator
manifest, and the launcher-recorded source-bundle path:
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`.
There is therefore no producer-provenance `AUDIT_ERROR`.

The complete hash comparison is in
[17_recorded_hash_verification.log](/audit-output/evidence/17_recorded_hash_verification.log);
the direct producer hashes are in
[06_producer_hash_authentication.log](/audit-output/evidence/06_producer_hash_authentication.log).

## Inventory reconstruction and Stage 3 classification

I invoked `tools.k_rule_inventory.inventory_verification` from
`PYTHONPATH=/reference` on the frozen Stage 1 workspace. Under the trusted
selection rule, the last `kompile verification.k --main-module ...` in
`prove.sh` selects `MAX-FILL-SUMMARY`; its local verification-file closure
contains only `MAX-FILL-SUMMARY`. The two later dispatch rules in
`MAX-FILL-VERIFICATION` are consequently outside this inventory, not omitted
inventory entries.

The reconstruction found:

- `verification.k` SHA-256:
  `517ec006a4b3d8452813b99de96046f88e30fc50fd4388e4bd5eecd5bfbf5979`.
- 19 rules, all with distinct normalized hashes and `source_rule_id` values.
- Canonical ordered inventory SHA-256:
  `c38d770ae0a9652b812217694490b3b0706fee0fe43a7d38653391e673572a78`.

I independently normalized and rehashed every extracted source span. All 19
hashes matched. The Stage 3 manifest has exactly the same 19 IDs in the same
order, with no omission, duplicate, extra ID, or reordering. The manifest
inventory hash also matches. See
[03_reconstructed_rule_inventory.json.log](/audit-output/evidence/03_reconstructed_rule_inventory.json.log)
and
[18_stage3_inventory_bijection.log](/audit-output/evidence/18_stage3_inventory_bijection.log).

My rule-by-rule classification is:

| Inventory entries | Frozen lines | Independent judgment |
|---|---:|---|
| `definedProjectInt` equation | 9 | `DEFINITION`: defines the named domain predicate as `isInt`. |
| `#Ceil` of the Val-to-Int projection | 14-16 | `DOMAIN_LEMMA`: characterizes the domain of a built-in partial projection; it does not define a new summary-headed term. |
| three `projectInt` equations | 17-23 | `DEFINITION`, `DEFINITION`, `DEFINITION`: guarded and constructor equations for the named projection proof term. |
| `rowVals(list(VS))` | 27 | `DEFINITION`: constructor equation for a named structural projection. |
| `isListVal` | 30 | `DEFINITION`: named predicate definition. |
| two `allBinary` equations | 37-42 | `DEFINITION`, `DEFINITION`: base and structurally recursive domain-predicate equations. |
| two `allRows` equations | 44-46 | `DEFINITION`, `DEFINITION`: base and structurally recursive grid-domain equations. |
| two `rowSum` equations | 54-55 | `DEFINITION`, `DEFINITION`: base and recurrence for a named execution summary. |
| two `bucketCost` equations | 59-64 | `DEFINITION`, `DEFINITION`: disjoint positive-capacity and totalization branches of the named summary. |
| two `gridCost` equations | 66-67 | `DEFINITION`, `DEFINITION`: base and recurrence for the named grid summary. |
| two `finalRow` equations | 72-73 | `DEFINITION`, `DEFINITION`: base and recurrence for the named loop-target summary. |

Thus the independent partition is 18 `DEFINITION`, zero
`OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and one `DOMAIN_LEMMA`,
exactly matching Stage 3. Every simplification-form rule is a definition or
the domain lemma.

The domain rule has not first been proved as the same claim against a module
that omits it: the Stage 1 claims are `sum-loop`, `grid-loop`, `max-fill`, and
the two dispatch-connection claims, none of which is this `#Ceil` equation.
Accordingly it cannot be upgraded to `PROVED_DERIVED_LEMMA`. It is materially
relevant: the source contract restricts grid elements to integer `0` or `1`;
the source program evaluates `sum(row)`; and `allBinary`, `rowSum`, the sum
loop, and the final program claim all depend on safely recognizing or
projecting those integer values. Evidence is in
[34_no_prior_exact_domain_lemma_proof.log](/audit-output/evidence/34_no_prior_exact_domain_lemma_proof.log)
and
[31_source_contract_and_projection_relevance.log](/audit-output/evidence/31_source_contract_and_projection_relevance.log).
The full independent record for all IDs and rationales is
[independent_classification.md](/audit-output/evidence/independent_classification.md).

## Stage 4 preflight, bijection, and target

I reran the required function:

```text
PYTHONPATH=/reference python3 -c '... tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json) ...'
```

The sandbox PID namespace initially made Lean's runtime look for a nonexistent
`/proc/<namespace-pid>/exe`. A captured readlink trace established that exact
cause. I compiled a narrow `LD_PRELOAD` shim that redirects only such executable
lookups to `/proc/self/exe`; it then reported Lean 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, the pinned version. With that
environment repair, the unmodified trusted preflight returned `PASS`, and both
its isolated `lake clean` and `lake build` exited 0. The successful returned
evidence is
[16_fresh_klean_preflight_pass.log](/audit-output/evidence/16_fresh_klean_preflight_pass.log);
the diagnosis and shim validation are
[14_lean_toolchain_diagnosis.log](/audit-output/evidence/14_lean_toolchain_diagnosis.log)
and
[15_lean_proc_workaround_validation.log](/audit-output/evidence/15_lean_proc_workaround_validation.log).

My independent Stage 4 comparison starts from the independently classified
domain set, which contains exactly:

`rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`.

The obligation map's ordered `source_rules` and ordered `obligations` lists each
contain exactly that ID once. Its source text, lines 14-16, normalized hash,
inventory hash, and discovery hash all agree with the frozen reconstruction.
The obligation-map SHA-256 is
`f5ac18f262e55d4fc4a9073609a0273300fbf4682958dd6c39ac07ee87f7417b`,
and its one conjunct hash is
`b662f964bf7f384e66f364e46321b25e9db710fa6bf297b174ac7dece76dd4ba`.
There is no omission, duplicate, irrelevant extra obligation, or source-rule
reordering. See
[33_independent_stage4_bijection.log](/audit-output/evidence/33_independent_stage4_bijection.log).

The generated proposition states, for every generated `SortVal` value `V`,
that the Option-valued KORE projection `project:Int?` is defined on the exact
K injection of `V` iff `definedProjectInt V = true`. This is the mathematical
content of the frozen matching-logic rule:

```text
#Ceil({@V:Val}:>Int)
  <-> (definedProjectInt(@V) = true and #Ceil(@V))
```

The Lean text contains an internal `∧ True`. It is not an invented filler or a
separate vacuous mapped obligation: it is the direct translation of the
source rule's explicit `#Ceil(@V)` conjunct, and a bound element variable of
sort `Val` is defined. The sole top-level mapped conjunct remains the
nontrivial projection-domain equivalence. Thus the target is neither weakened
nor made vacuous relative to the frozen rule.

The fixed target is:

- declaration: `Klean115MaxFill.Lemmas.targetStatement`;
- definition hash:
  `73ebd4f36a82337ccff0414e1db640c698262f1dad83f69603ea469b1f9eedb3`;
- applied statement:
  `Klean115MaxFill.Lemmas.targetStatement «definedProjectInt(_)_MAX-FILL-SUMMARY_Bool_Val» «project:Int?»`;
- statement hash:
  `51e731789decebfd1c5258f35f26465cc3ec52da6e7c328c6fd80bb9b2a70b0c`.

The declaration, definition, parameter records, binding hashes, applied
statement, and statement hash agree exactly among the generated file, generator
manifest, preflight result, and `/audit-input.json`.

## Stage 5 clean build, proof identity, and trust

I copied the candidate to
`/tmp/audit-work/115-max-fill-proof-audit-fresh`, copied the immutable generated
project's contents into its existing empty `Base`, then ran:

```text
LD_PRELOAD=/tmp/readlink_fix.so lake clean
LD_PRELOAD=/tmp/readlink_fix.so lake build
```

Both exited 0, and the build ended `Build completed successfully.` The complete
transcript is
[22_isolated_candidate_clean_build.log](/audit-output/evidence/22_isolated_candidate_clean_build.log).
An earlier staging attempt copied the generated directory one level too deep
and stopped at configuration discovery before any proof build; that discarded
attempt is retained as raw evidence in `21_isolated_candidate_clean_build.log`.

Outside `Base`, the candidate has exactly two parameter `def`s and one
`theorem final`. It contains no `sorry`, `admit`, `unsafe`, `axiom`, or
`opaque`, and no `targetStatement` declaration that could shadow or replace the
generated target. The copied `Base/Klean115MaxFill/Lemmas.lean` is byte-for-byte
equal to the mounted generated file. See
[26_candidate_only_source_gate.log](/audit-output/evidence/26_candidate_only_source_gate.log).

The trusted Stage 5 mechanical check independently copied the candidate,
replaced its empty `Base` with the generated project, clean-built it, checked
the exact theorem type, and returned `PASS`. `Proof.final` states the exact
fixed generated target rather than a duplicate or weakened proposition. Its
evidence is
[23_trusted_stage5_mechanical_check.log](/audit-output/evidence/23_trusted_stage5_mechanical_check.log).

I also ran Lean explicitly with `#print axioms Proof.final`. Its exact result
was:

```text
Proof.final : Klean115MaxFill.Lemmas.targetStatement Proof.«definedProjectInt(_)_MAX-FILL-SUMMARY_Bool_Val»
  Proof.«project:Int?»
'Proof.final' does not depend on any axioms
```

This is saved in
[24_exact_print_axioms_proof_final.log](/audit-output/evidence/24_exact_print_axioms_proof_final.log).
The used-axiom set is empty, so it contains neither `sorryAx` nor any unrecorded
trust dependency. The 43 generated declarations listed by
`trust-inventory.json` are not dependencies of `Proof.final`; an empty
dependency set is fully reconciled with that allowlist.

## Operational-bridge audit

Both target parameters are bound to the sole domain-rule ID, but their bodies
must additionally implement the symbols referenced by that rule.

1. `«definedProjectInt(_)_MAX-FILL-SUMMARY_Bool_Val»`

   The candidate returns `true` exactly for `SortVal.inj_SortInt` and `false`
   for every other `SortVal` constructor. The bound KORE symbol is the total
   `definedProjectInt : SortVal -> SortBool`; frozen line 9 defines it as
   supplied `isInt`. The supplied value algebra makes `Int` a distinct
   subsort/constructor of `Val`, and the generated operational `isInt` recognizes
   exactly a one-item K term injected from `SortInt`. The candidate therefore
   matches both the frozen definition and supplied operational semantics. It is
   not constant or identity-like.

2. `«project:Int?»`

   The bound KORE symbol `Lblproject'Coln'Int` is the partial projection
   `SortK -> SortInt`. Under `#Ceil`, deterministic generation correctly exposes
   it as `SortK -> Option SortInt`. The candidate returns `some i` only on the
   exact representation `kseq (inj_SortInt i) dotk`, returns the same `i`, and
   returns `none` on non-Int or multi-item K terms. This is the operational
   meaning of K's sort projection and not merely a definedness oracle.

I checked witnesses for integer `7`, Bool `false`, `noneV`, and a malformed
two-item K sequence. Candidate results were respectively `true`, `false`,
`false` for the predicate and `some 7`, `none`, `none` for the projection.
Constant-true and constant-false predicate mutations were refuted by concrete
Bool and Int witnesses.

The strongest counterfactual was a `badProjectZero` definition that recognizes
the correct Int-shaped domain but returns `some 0` for every integer. It still
proves the generated domain equation, demonstrating why a clean theorem alone
is insufficient. The submitted candidate differs on the adversarial witness
`7`: `badProjectZero` returns `some 0`, while the candidate returns `some 7`.
Lean checked the bad mutation's theorem and the candidate/value inequivalence,
so the separate operational-bridge judgment is exercised rather than assumed.
The final test source and successful output are
[30_operational_bridge_adversarial_test_source.log](/audit-output/evidence/30_operational_bridge_adversarial_test_source.log)
and
[29_operational_bridge_adversarial_lean_checks_pass.log](/audit-output/evidence/29_operational_bridge_adversarial_lean_checks_pass.log).

The KORE declarations and exact compiled source rule are captured in
[32_kore_parameter_bindings.log](/audit-output/evidence/32_kore_parameter_bindings.log).
Both submitted parameter definitions pass the operational bridge requirement.

## Final judgment

Stage 3 accounts for and correctly classifies the complete trusted inventory.
The true domain-lemma set is nonempty and contains exactly one relevant rule,
so `KLEAN_NO_OBLIGATIONS` would have been illegitimate; the selected Stage 4
correctly generated one fixed target instead. Stage 4 provenance, bijection,
and target identity all hold. Stage 5 proves exactly that target in a clean
build, uses no axioms, and supplies operationally faithful definitions for both
target parameters.

VERDICT: PASS
LEGITIMACY: LEGIT
