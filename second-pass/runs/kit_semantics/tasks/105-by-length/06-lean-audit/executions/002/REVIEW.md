# Independent Stage 3–5 audit: HumanEval 105-by-length

## Decision

The protected Stage 3 classification is complete and mathematically correct, the selected Stage 4 output is the deterministic one-obligation translation of the only true domain lemma, and the Stage 5 candidate proves the immutable generated theorem with honest operational bindings. I found no omitted rule, weakened obligation, target substitution, candidate trust escape, or operational-bridge shortcut.

The launcher binding verifies as `CLASSIFICATION_AND_PROOF`, condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, with resolved-input SHA-256 `0db7b785133ca98993273adb4d1b2d08f97224695c461de7a099f0c2b04a32dc`. I treated all mounted prose and prior results as evidence only and reconstructed the result from the frozen sources and trusted tooling.

## Input and producer provenance

The launcher-bound hashes all matched: K workspace `14e1f68e49e379a8cc0b7d20c097a2d26bd08ae55fa7d35bc7f0ec3ef7991aea`, Stage 1 export `5cab8bdf04771b50412d561b8edcfaa3ebf1f7550a6acf8f386fb274dcf92db4`, Stage 2 audit `9067024337babc3410b97a0a958dd849d026ea75a4bcc7802ec24d3709c28ef8`, discovery manifest `ea297e7947d65f3f8dfbf31581af286687b0c08ef32a7e225f271c65124ec7bb`, complete generation `a4b7d6b297bbb66acfedfce2f7e9880a6eb32e7e5efe6fbacf7381832f1e1fb9`, generated tree `bcbd88215a42455adad5d49c22a5ebe24958d2fdad0016e2c718c96379e89da8`, producer-source tree `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, and candidate `2e933c9d143aa378c97c9693dc5b16976b9ba579bc05f3f795cc0558b8e2dd44`. All 780 Stage 1 source-map entries were present and unchanged.

Before evaluating generation, I independently hashed the two mounted producer files:

- `klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Both match the source manifest, generator manifest, and audit input. The source manifest and audit path also agree on immutable generator image `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`. Thus the producer-source infrastructure prerequisite passes. Full comparisons are in [03_hash_and_inventory_reconstruction.txt](evidence/03_hash_and_inventory_reconstruction.txt).

## Independent rule inventory and classification

Using the trusted `k_rule_inventory.inventory_verification` implementation on frozen `verification.k`, I obtained local verification-module closure `VERIFICATION` only, source SHA-256 `9696cfcae2e2436114cda643ad130cf607767bf60afd368c0a63ddbe9a1c863b`, ten rules, and inventory SHA-256 `aae99af3f9847ce2ab92c4c7c79358ecfcde2abeaa10a418c3fd084758889f0e`. For every rule I recomputed the source span, normalized source, normalized hash, and `source_rule_id`. The ordered identities and records compare bijectively with `lemma-discovery.json`: no omission, extra entry, duplicate, reordering, span change, or hash change exists.

My independent classifications are:

| Frozen lines | Rule or named term | Classification | Reason |
|---:|---|---|---|
| 8–14 | `collectLoopBody` | `DEFINITION` | Exact syntax macro for the loop body. |
| 17–22 | `collectDigitBody` | `DEFINITION` | Exact syntax macro for the helper body. |
| 25–53 | `byLengthBody` | `DEFINITION` | Exact syntax macro for the source function body. |
| 56–66 | `solutionModule` | `DEFINITION` | Named macro assembling the two source functions. |
| 70 | `allInts` base | `DEFINITION` | Base equation of a named input-domain predicate. |
| 71–72 | `allInts` step | `DEFINITION` | Recursive equation of that predicate. |
| 75–78 | guarded `applyCmp("==", V, I)` simplification | `DOMAIN_LEMMA` | Sort-refinement equation not itself a definition or ordinary execution rule. |
| 84 | `collectAcc` base | `DEFINITION` | Base equation of the named execution summary. |
| 85–97 | `collectAcc` step | `DEFINITION` | Recursive equation of the named execution summary. |
| 101–118 | `byLengthVS` | `DEFINITION` | Named result summary built from `collectAcc`. |

The sole simplification rule has full identity `rule-4a33e8fabf1037b714c839a6db0b745a25e879f3ee38553ad06d7cffc831f430`; classifying it as `DOMAIN_LEMMA` satisfies the simplification policy. It is not a `PROVED_DERIVED_LEMMA`: Stage 1 does not first prove this exact rule against a module omitting it and then import it later. It is not an `OPERATIONAL_RULE`: ordinary integer comparison already lives in the supplied `MPY-INT` semantics as `applyCmp("==", I1:Int, I2:Int) => I1 ==Int I2`.

The domain lemma is true and relevant. Under `isInt(V)`, the K predicate/refinement rules force `V` to be an injected integer `J`; the frozen operational comparison becomes `J ==Int I`, exactly the projected right-hand side. The source helper compares each `value == digit`, `allInts` guards the proof domain, and `collectAcc` uses the same projected integer equality. This is therefore not an irrelevant mathematical fact smuggled into the proof. The exact reconstructed inventory and all source slices are in [03_hash_and_inventory_reconstruction.txt](evidence/03_hash_and_inventory_reconstruction.txt); the source program and semantic rules are preserved in [14_operational_bridge_sources_and_tests.txt](evidence/14_operational_bridge_sources_and_tests.txt).

## Deterministic Stage 4 generation

I ran the required `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the exact frozen workspace, protected discovery manifest, selected generation, and trusted lock file. It returned `status: PASS`, `obligation_count: 1`, zero designated sorries, 47 inventoried generated trust declarations, and successful `lake clean`/`lake build`. The returned evidence is [08_required_stage4_preflight_success.txt](evidence/08_required_stage4_preflight_success.txt).

The first invocation, retained in [04_required_stage4_preflight.txt](evidence/04_required_stage4_preflight.txt), reached `lake clean` but Lake could not locate its installation because the sandbox exposes a PID namespace without the corresponding `/proc/<pid>/exe`. I diagnosed this independently and reran with the exact locked Lean toolchain plus a narrow compatibility shim which redirects only `readlink("/proc/<digits>/exe")` to `/proc/self/exe`. Its source and binary hashes and successful control build are recorded in [07_lean_proc_compatibility_and_test.txt](evidence/07_lean_proc_compatibility_and_test.txt). The shim affects application-location discovery only; it does not alter Lean sources, elaboration, the generated project, or proof declarations. The required rerun and the later trusted final gate both passed.

The Stage 3 partition exported into Stage 4 contains exactly nine definitions, zero operational rules, zero proved-derived lemmas, and the one domain source rule above. Every inventory identity occurs exactly once. The obligation map has exactly one obligation, with the same rule identity, span, normalized hash, inventory hash, and discovery-manifest hash. Its Lean conjunct retains both quantified K variables, the satisfiable `isInt` guard, the right integer injection, and the entire comparison equality; it is neither literal nor reducible to `True`/`False`. For example, injected integer `V = 17` satisfies the guard, so the conjunct is not vacuous.

The exact generated declaration is `Klean105ByLength.Lemmas.targetStatement`. Its definition hash is `9fd05dd81aa754ff39920cd21046a722ee57d943d1719895762e09924adde7dc`; its application statement hash is `22910f52851033b1a5112d6ff0b674228069a23696a80017135079b1a6daafc5`. The target is exactly the mapped single conjunct—there is no omitted, duplicated, irrelevant, or weakened obligation and no alternate target. All binding hashes, obligation-map hash `83ff1167c29937f5f33017115ad0315c6d610eea5172e92b52dee551a115a827`, and target recomputations are in [09_stage4_bijection_and_target_hashes.txt](evidence/09_stage4_bijection_and_target_hashes.txt).

This is not a `KLEAN_NO_OBLIGATIONS` case: the independently classified domain set genuinely contains one rule and Stage 4 correctly generated one target.

## Stage 5 clean proof and target identity

I created `/tmp/audit-work/lean-proof-audit`, copied the candidate root into it, replaced `Base` with a fresh copy of `/reference/klean-generation/generated`, then ran `lake clean` and `lake build`. Both exited zero; the complete build transcript is [10_fresh_candidate_clean_build.txt](evidence/10_fresh_candidate_clean_build.txt). The candidate `Proof.lean` SHA-256 remained `32229e395dc219b3378aa5e6a690a5dee5cc6d3644662e86ef5e8080dcf28d9c`, and the fresh `Base/Klean105ByLength/Lemmas.lean` matched the reference at `c436d3951236a33f54676721c01a63bf6cf3a56e50b15859cd68b3cb6b547817`.

Candidate-authored Lean contains no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. It does not declare or shadow `targetStatement`. Each of the four required parameter definitions occurs exactly once, and `Proof.final` occurs exactly once with the generator-manifest statement—not a copied theorem, weakened proposition, or vacuous variant. Static evidence is [11_candidate_static_gate.txt](evidence/11_candidate_static_gate.txt).

I also ran the trusted complete final gate over the immutable inputs. It reran generation preflight, performed another clean candidate build, checked the exact final statement, ran the axiom audit, rechecked input stability, and returned `PASS` for `CLASSIFICATION_AND_PROOF`; see [15_trusted_final_gate.json](evidence/15_trusted_final_gate.json) and [15_trusted_final_gate_command.txt](evidence/15_trusted_final_gate_command.txt). As specified by that tool, its `semantic_classification` field is only `NOT_EVALUATED`; the independent semantic judgment is supplied by this review.

## Proof identity, axioms, and operational bridge

Running Lean on an audit module containing exact `#check`, `#print Proof.final`, and `#print axioms Proof.final` confirmed that the theorem type is precisely:

`Klean105ByLength.Lemmas.targetStatement Proof.«_==Int_» Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val» Proof.isInt Proof.«project:Int»`.

The exact output says `Proof.final` depends on `[propext, Classical.choice]`; see [12_axiom_audit_exact.txt](evidence/12_axiom_audit_exact.txt). Both are in the trusted final gate's fixed Lean-core allowlist (`propext`, `Classical.choice`, `Quot.sound`) that is combined with `trust-inventory.json`. No one of the 47 generated inventory axioms is used, `sorryAx` is absent, and the set of unrecorded dependencies is empty. The mechanical reconciliation is [16_axiom_reconciliation.txt](evidence/16_axiom_reconciliation.txt).

For each target parameter I located and checked the exact candidate definition against its `kore_symbol`, binding hash, common source-rule ID, frozen rule, source solution, and supplied semantics:

- `«_==Int_»` is Lean integer equality, exactly K's `==Int` on `SortInt`.
- `«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»` maps the relevant `"=="`, integer/integer branch to the same integer equality. Its other defined branches mirror the supplied dispatch rules (bool, float/mixed float, strings, lists, tuples, sets, dictionaries, and `None`); its final `false` branch only totalizes combinations for which the frozen partial K function has no rule. The generated theorem's guard and right injection cannot reach that totalization branch.
- `isInt` returns true exactly on a singleton K sequence containing an injected integer and false otherwise, matching the compiled K predicate and its `owise` rule.
- `«project:Int»` returns that injected integer, matching the K projection. Returning zero outside the projection's partial domain is irrelevant because `isInt = true` excludes every such input.

These definitions also match the source program's only relevant observation: integer loop-element equality with the selected digit. The complete candidate definition and source comparison are in [14_operational_bridge_sources_and_tests.txt](evidence/14_operational_bridge_sources_and_tests.txt), with the wider frozen `applyCmp` rule inventory in [18_applycmp_semantics_inventory.txt](evidence/18_applycmp_semantics_inventory.txt).

I compiled adversarial Lean examples for equal and unequal positive/negative integers, a non-integer rejection, projection, and both sides of `applyCmp`. Results were respectively true/false as required; see [19_operational_bridge_evaluations_success.txt](evidence/19_operational_bridge_evaluations_success.txt). The audit artifact also defines coordinated constant-false equality and comparison bridges and proves that those dishonest definitions could satisfy the bare equation. Crucially, mutating only comparison or only equality is refuted at the satisfiable `17 == 17` witness. This demonstrates why clean proof alone is insufficient, while confirming that the candidate's actual four definitions implement the frozen operational match rather than exploiting coordinated constants, identity functions, hard-coded values, or an impossible guard. The artifact first re-ran once while the complete gate had temporarily cleaned the shared generated build directory; [17_operational_bridge_evaluations.txt](evidence/17_operational_bridge_evaluations.txt) records that missing-object-file concurrency artifact, and the post-gate rerun in evidence 19 is the valid completed run.

## Evidence summary

Raw environment, sources, manifests, hashes, diagnostics, complete clean-build output, exact axiom output, counterfactual test sources, and trusted-gate results are under `evidence/`. The evidence establishes structural integrity mechanically; the classification truth, domain relevance, non-vacuity, and operational-bridge conclusions above are my independent mathematical judgment.

VERDICT: PASS
LEGITIMACY: LEGIT
