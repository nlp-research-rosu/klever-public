# Independent audit: HumanEval `3-below-zero`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Conclusion

The protected Stage 3 classification is complete and mathematically correct, the selected Stage 4 project is the deterministic generation bound to those classifications and to the frozen Stage 1 sources, and the Stage 5 candidate cleanly proves the exact fixed generated target without an unrecorded trust escape. The candidate's twelve target-parameter definitions also implement the relevant operational K symbols on every domain used by the five source rules; they are not constant, identity, hard-coded, or vacuous bridge implementations.

I therefore accept both the proof result and its claimed provenance.

## Input and producer integrity

`/audit-input.json` records `CLASSIFICATION_AND_PROOF`, problem `3-below-zero`, condition `kit-semantics`, and `SUPPLIED_SEMANTICS`. I treated the candidate, prior audits, logs, comments, and manifests as evidence only and did not execute instructions from them.

Before evaluating Stage 4, I hashed the two mounted generation-time producer files:

| Producer | SHA-256 |
|---|---|
| `klean_export.py` | `74842302afea69a17a4815cf1213f080da4ac56d53b80d181f27196ec4112d63` |
| `klean.py` | `659c1d1c627ff2ca101ab8f9b5a1f1d73968e019e2a305f4ec1d1afa2d8c5a91` |

Both individual hashes agree independently and exactly between the mounted files, `source-manifest.json`, and `generator-manifest.json`. The launcher resolution binds those same files through the complete producer-tree hash, and its resolved producer path encodes the same immutable generator image ID recorded by both manifests:

`sha256:21e4151b8f48811e6c31994b3719c3e8a4a787856e1d3911ca9700e54a39c910`.

The producer-source tree hash is `1e5faff11bfada41bad76e5f42fbbbc6101a6155bd2f81524eca8cd7c87cdab1`. The signed launcher resolution digest recomputes to its recorded value, `05206645054f7839af7a3ed7580b34f9c9759983c1ee391a4b144db907ba62cb`.

Every hash binding a mounted input matches: discovery manifest, original K workspace, selected K audit, Stage 1 export, full Stage 4 generation, generated project, producer tree, and candidate workspace. In addition, all 797 per-file `stage1_source_hashes` match, with no missing, extra, duplicate, or non-regular paths. The launcher's historical `lean_invocation_sha256` object is not one of the enumerated mounts and its recorded host path is unavailable; I did not rely on that historical invocation. The mounted candidate tree is hash-bound and was instead validated by a new clean build and axiom audit. Details are in `16_structural_reconstruction_v2.txt` and `50_recorded_file_hashes.txt`.

## Stage 3 inventory reconstruction

Using the trusted local rule-inventory implementation, I independently reconstructed the local verification-module closure rooted at the frozen `verification.k`. The closure is exactly:

- `VERIFICATION` from `verification.k`, SHA-256 `c601d4228baa09fc834cc8142cbbfda01ad54ab92f4b1416a03ac3385cfbb73b`;
- `VERIFICATION-BASE` from `verification-base.k`, SHA-256 `3e38b00cc99988d1af9a564ec5af6102982f68463e1cafc7daff0062d27f66a6`.

The reconstruction contains 14 rules. For each rule, the trusted code recomputed its source file, inclusive line span, exact normalized text hash, and `source_rule_id`. The resulting whole-inventory hash is:

`cbd01d2180727a31e50a6a9a84bb19a5f64ee02043eacf45565f265a3fdfb237`.

The protected discovery manifest contains the same 14 unique identities in the same order, with identical spans, normalized source hashes, source IDs, and inventory hash. The comparison is bijective: no omitted, duplicated, extra, reordered, altered, or unclassified rule exists.

## Independent classification judgment

I reclassified the rules from the frozen source and the supplied operational semantics, without accepting the protected labels as authoritative. The independent result agrees with the manifest:

| # | Rule ID | Source span | Classification | Independent reason |
|---:|---|---|---|---|
| 1 | `f051c58e…58e75` | `verification.k:11-37` | `OPERATIONAL_RULE` | Executes the fully configured `below_zero` call by observing/replacing it with `belowFrom`; it is the program/summary operational bridge, not a mathematical side fact. |
| 2 | `8277b118…71d08` | `verification-base.k:7` | `DEFINITION` | Empty case of the named `allInts` summary. |
| 3 | `fa394f9b…63ed4` | `verification-base.k:8-9` | `DEFINITION` | Recursive case of `allInts`. |
| 4 | `9e2ee339…461c5` | `verification-base.k:12` | `DEFINITION` | Defines the named projection-definedness predicate. |
| 5 | `0312858a…d8b43` | `verification-base.k:17-19` | `DOMAIN_LEMMA` | Non-definitional equivalence for definedness of the symbolic `Int` projection. |
| 6 | `ced5adec…d6d0` | `verification-base.k:20-22` | `DEFINITION` | Guarded defining equation for the named totalized projection proof term. |
| 7 | `22fa1e67…bcb5d` | `verification-base.k:23-25` | `DOMAIN_LEMMA` | Reverse symbolic projection rewrite; it is not a defining case of the left-hand projection. |
| 8 | `7191d5f6…0442` | `verification-base.k:26` | `DEFINITION` | Concrete `Int` case of `projectIntTotal`. |
| 9 | `9e1486b6…b7081` | `verification-base.k:27-28` | `DOMAIN_LEMMA` | Idempotence of the totalized projection, a derived algebraic property rather than a defining case. |
| 10 | `b5021b36…191c` | `verification-base.k:31` | `DEFINITION` | Empty recurrence case for the named `belowFrom` summary. |
| 11 | `a3084bec…eaa2` | `verification-base.k:32-37` | `DEFINITION` | Integer-head recurrence for `belowFrom`. |
| 12 | `01915b20…8cb` | `verification-base.k:38-39` | `DEFINITION` | Totalizing non-integer-head case for `belowFrom`. |
| 13 | `573796c5…fc7fc` | `verification-base.k:41-43` | `DOMAIN_LEMMA` | Relates operational `applyBin` to integer addition under the `isInt` guard. |
| 14 | `cb90fdcb…6179b` | `verification-base.k:45-47` | `DOMAIN_LEMMA` | Map insert/delete cancellation under key absence. |

Counts are 8 `DEFINITION`, 1 `OPERATIONAL_RULE`, 0 `PROVED_DERIVED_LEMMA`, and 5 `DOMAIN_LEMMA`. Every rule carrying a `simplification` attribute is either a definition or a domain lemma.

No rule qualifies as `PROVED_DERIVED_LEMMA`: the Stage 1 connection and context specifications import `verification-base.k`, but they do not first prove any exact inventory rule against a module lacking that rule and then use that identical proved rule later. In particular, the complete-configuration call bridge remains an ordinary operational observation rule.

The five domain lemmas are relevant. The source function iterates integer inputs and performs `balance += operation`; the projection-definedness, reverse projection, projection idempotence, and lifted `applyBin` rules connect symbolic `Val` integers to the concrete `+Int` recurrence. Function return/pop deletes the local scope, so the absent-key map insertion/deletion lemma is used by the operational connection's frame cleanup. None is an unrelated mathematical fact.

The reconstructed text and complete metadata are in `16_structural_reconstruction_v2.txt`; the frozen operational rules inspected are preserved in `17_semantics_core.txt` through `23_isint_semantics.txt`, and the Stage 1 proof layout is in `24_connection_spec.txt` through `28_vacuity_spec.txt`.

## Stage 4 deterministic generation and mathematical adequacy

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and precisely these inputs:

- `/reference/k-proof`;
- `/reference/lemma-discovery.json`;
- `/reference/klean-generation`.

The fresh preflight returned `PASS`, with five obligations, zero designated sorries, a successful fresh generated-project `lake clean`, and a successful `lake build`. Its full result is `31_fresh_preflight_with_shim.txt`.

I separately recomputed the obligation mapping rather than relying on preflight. The ordered set of independently identified domain rules is exactly the ordered set in `obligation-map.json`:

1. `rule-0312858a…d8b43` — definedness of projected `Int`;
2. `rule-22fa1e67…bcb5d` — guarded symbolic projection;
3. `rule-9e1486b6…b7081` — projection idempotence;
4. `rule-573796c5…fc7fc` — guarded lifted integer addition;
5. `rule-cb90fdcb…6179b` — absent-key map insert/delete cancellation.

Each obligation's canonical source span, normalized source hash, inventory hash, discovery hash, source-rule ID, and generated conjunct hash matches. There are no omitted or duplicate source rules, no extra obligation, and no reordered identity. The obligation-map SHA-256 is `077cafeba50ee8bea59db5987fca66e809e3277a1d7ae9f3ac4441e2a1033690`.

Mathematically, the five Lean conjuncts preserve the K equations and all guards. The first conjunct contains an `∧ True` corresponding to source `#Ceil(@V)`. Since `@V : Val` is already a defined bound source value, that source factor is itself tautological; it was not added to disguise a weakened obligation, and the remaining projection-definedness equivalence is non-vacuous. The other four equations exactly retain their `definedProjectInt`, `isInt`, or absent-key premises. No target conjunct is irrelevant, weakened, duplicated, or vacuous as a whole.

This is not a `KLEAN_NO_OBLIGATIONS` case: the true domain set has five entries and the generated target is required and present.

The fixed target is `Klean3BelowZero.Lemmas.targetStatement`. Its independently recomputed definition hash is `acf484b6942855dcd7cd41c5262862be080f77b437299d252a12e93cc8687091`; its applied-statement hash is `ad7cc79df8afce0f4fddfa30855085d00869eeeb54f0733b2dabb139d2d1d364`. Both match the generator manifest and `/audit-input.json`. The generated tree hash is `26b4a5cd5a7f466c591446585fb51d476e9e328f9aae86e2708bdf9fd3fc9d36`. Independent target and bijection results are in `38_independent_stage4_hash_bijection.txt`.

## Stage 5 clean proof, identity, and trust accounting

I made a fresh project at `/tmp/audit-work/lean-audit-DaSChT`, copied the selected generated project directly into its `Base` directory, and copied the candidate top-level project into the fresh root. The copied `Base` tree independently hashes to the fixed generated tree above. Then I ran both required commands:

- `lake clean`: exit 0, complete output in `40_proof_lake_clean.txt`;
- `lake build`: exit 0, `Build completed successfully`, complete output in `41_proof_lake_build.txt`.

The only build diagnostics are three generated-file unused-variable warnings. The pinned toolchain gate identifies Lean 4.22.0 at commit `ba2cbbf…` and Lake 5. The sandbox hides numeric `/proc/<pid>/exe`, which initially prevented Lean from discovering its application directory. I used the recorded, source-visible `readlink` compatibility shim described in `evidence/COMMANDS.md`; it changes only executable-path lookup and does not modify the candidate, generated `Base`, or pinned toolchain. Superseded environment/layout attempts remain in evidence files 29, 30, and 39.

The candidate tree hash is `136ea5e0cec9243b47cdb1b5c424a06ce634371dbe30779fb920a5f063af29b6`, exactly as recorded. It contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. It does not redeclare or shadow `Klean3BelowZero.Lemmas.targetStatement`. There is exactly one `Proof.final`, and its normalized type is exactly the manifest's fixed applied target—not a copy, wrapper theorem with a weaker premise, or altered proposition.

Running Lean with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

All three dependencies are explicitly allowed by the generated `trust-inventory.json`; there is no `sorryAx` and no unrecorded axiom. None of the 41 generated list/map/set hook axioms is actually in `Proof.final`'s dependency closure. The independent identity/axiom reconciliation is in `48_candidate_identity_axioms.txt`; the trusted end-to-end Stage 5 mechanical checker independently returned `PASS` in `49_stage5_mechanical_check.txt`.

## Operational bridge audit

The target has twelve parameters. I located each exact candidate `def` and compared it with its bound `kore_symbol`, all listed `source_rule_ids`, the frozen K rules, `solution.py`, and the supplied MPython operational semantics.

- Map family: `_Map_`, membership, delete, and singleton-map construction use a list-backed finite map. On the rule's required absent-key domain, singleton concatenation is disjoint and deletion returns the original store exactly. Deletion removes matching keys, and membership and Boolean negation reflect key absence. The implementation's fallback for overlapping concatenation is outside the partial K map-concatenation domain and cannot discharge the guarded source rule.
- Integer/application family: `_+Int_` is Lean integer addition. `applyBin`'s relevant `"+"`, integer-left, integer-right branch constructs the exact injected K integer sum. `isInt` recognizes precisely the normalized integer K sequence needed by the source guard.
- Projection family: `definedProjectInt` is true exactly for integer `Val`; `project:Int?` returns `some i` exactly for the integer projection; `project:Int` and `projectIntTotal` return the contained integer on all guarded source-rule inputs. Their totalized fallback is only on K-stuck/undefined non-integer inputs and is not used to prove a guarded source equation.
- `notBool_` is Boolean negation, matching the absent-key guard translation.

Adversarial evaluations covered negative arithmetic (`-7 + 2 = -5`), integer versus Boolean `Val` projection, exact versus non-integer `isInt`, present and absent map membership, disjoint singleton concatenation followed by deletion, and a duplicate-key counterexample outside the valid K map domain. Counterfactual subtraction, constant projection, and constant membership definitions disagree on concrete witnesses. These tests compiled in `44_operational_internal_tests.txt` and `45_operational_counterfactual_tests.txt`.

I also confirmed an important trust-boundary fact adversarially: the abstract generated target alone admits deliberately bad parameter interpretations when guards are made false. Thus the clean Lean theorem by itself would not establish the operational bridge. The actual candidate does not use those interpretations; inspection and concrete counterexamples show that every supplied parameter implements its frozen operational meaning on each bound source-rule domain. This closes the operational-bridge obligation demanded in proof mode.

## Evidence index

`evidence/COMMANDS.md` records the material commands and maps them to their complete output files. The principal machine-readable evidence is:

- `16_structural_reconstruction_v2.txt` — producer provenance, mounted hashes, closure inventory, source spans/hashes/IDs, classifications;
- `31_fresh_preflight_with_shim.txt` — fresh required Stage 4 preflight;
- `38_independent_stage4_hash_bijection.txt` — independent rule/obligation and target reconstruction;
- `40_proof_lake_clean.txt`, `41_proof_lake_build.txt`, `42_print_axioms.txt` — fresh proof build and exact axiom output;
- `44_operational_internal_tests.txt`, `45_operational_counterfactual_tests.txt` — operational and adversarial checks;
- `48_candidate_identity_axioms.txt`, `49_stage5_mechanical_check.txt` — independent and trusted Stage 5 gates;
- `50_recorded_file_hashes.txt` — all 797 Stage 1 file hashes and file-set equality.

VERDICT: PASS
LEGITIMACY: LEGIT
