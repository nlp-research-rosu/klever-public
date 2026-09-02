# Independent audit: 158-find-max / kit-semantics

## Result

I independently audited Stage 3 classification, deterministic Stage 4 generation, and the Stage 5 Lean proof in launcher mode `CLASSIFICATION_AND_PROOF`, with semantics mode `SUPPLIED_SEMANTICS`. The classification is complete and mathematically appropriate, Stage 4 generated exactly the four genuine domain obligations, and `Proof.final` proves the fixed target using operationally faithful bindings and no unrecorded trust escape.

## Input and producer authentication

The signed audit-input envelope verified with resolved-input SHA-256 `4f48b813163a72b3668d460bc3187fee623aebcf784304933e5f2582481a5f12`. I recomputed every mounted pipeline tree hash; the Stage 1 workspace, selected Stage 2 audit, Stage 4 generation, generator-source tree, and Stage 5 workspace all equal their launcher-recorded values. All 790 recorded Stage 1 per-file hashes match. The separately recorded `lean_invocation_sha256` names a launcher directory that was not mounted; it is not an input used by this audit, while the mounted Lean workspace itself was fully checked and matches `lean_workspace_sha256`.

Before judging Stage 4, I hashed the two producer files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |

Both values match the generator manifest and source manifest. Their immutable image ID also agrees with the generator manifest, source manifest, and the generator-source path recorded in the audit input: `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`. The source-tree hash is `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`. There is no producer-source infrastructure error.

Evidence: [launcher and mounts](/audit-output/evidence/00_launcher_and_files.txt), [manifests and producer hashes](/audit-output/evidence/01_stage4_manifests_and_producer_hashes.txt), and [independent mounted-hash audit](/audit-output/evidence/15_all_mounted_hashes_and_target_identity.txt).

## Stage 3 inventory reconstruction

I ran the trusted local rule-inventory implementation against frozen `/reference/k-proof/verification.k`. Its local verification-module closure is exactly module `VERIFICATION`; imported supplied semantics are not incorrectly counted as locally introduced verification rules. Reconstruction found 21 rules. The frozen `verification.k` source hash is `e55b3452293a195c30fb330a9c73d713d05052c61b6a2c2d1272791458f64f05`, and the recomputed whole inventory hash is:

`b74ac0a769f9ce93027f625ba4030e585fe307aa7c7ec1941c933938c4cea026`

For every entry, the reconstructed source span, normalized text hash, and `source_rule_id = "rule-" + normalized_sha256` match the protected discovery manifest. The two ordered lists contain 21 unique identities and are equal. Thus there are no missing, extra, duplicate, or reordered rules and no altered hashes.

My independent classification is:

| Ordinal / lines | Classification | Frozen semantic role |
|---|---|---|
| 1 / 8 | `DEFINITION` | `definedProjectStr` names the string-domain predicate. |
| 2 / 13–15 | `DOMAIN_LEMMA` | Characterizes definedness of the pre-existing partial `Val`-to-`Str` cast. |
| 3 / 17–19 | `DEFINITION` | Guarded defining equation for total string projection. |
| 4 / 20–22 | `DEFINITION` | Reverse cast normalization defining the same summary. |
| 5 / 23 | `DEFINITION` | Projection is the identity on `Str`. |
| 6 / 24 | `DOMAIN_LEMMA` | Additional idempotence law for the total projection. |
| 7 / 27 | `DEFINITION` | `codesOf` is the `str` payload destructor. |
| 8–9 / 31–33 | `DEFINITION` | Base and recurrence for the `allStrings` input-domain summary. |
| 10 / 36–39 | `DOMAIN_LEMMA` | Guarded dynamic `set(str)` observation equation. |
| 11 / 41–44 | `DOMAIN_LEMMA` | Guarded dynamic string-less-than observation equation. |
| 12 / 48–49 | `DEFINITION` | Defines the unique-character score. |
| 13 / 53–58 | `DEFINITION` | Defines score-first, lexicographic-tie candidate selection. |
| 14–15 / 62–67 | `DEFINITION` | Base and recurrence for `bestWord`. |
| 16–17 / 70–75 | `DEFINITION` | Base and recurrence for `bestScore`. |
| 18–19 / 79–80 | `DEFINITION` | Base and recurrence for the loop's last word. |
| 20–21 / 83–84 | `DEFINITION` | Base and recurrence for the loop's last score. |

Totals are 17 `DEFINITION`, four `DOMAIN_LEMMA`, zero `OPERATIONAL_RULE`, and zero `PROVED_DERIVED_LEMMA`. Every rule carrying `simplification` or `simplification(10)` is in one of the two permitted classes.

The two Stage 1 connection claims prove only the static constructor equations `applyBuiltin("set", str(CS), .Vals)` and `applyCmp("<", str(A), str(B))`. Stage 1 does not first prove any of the four exact dynamic/domain rules in a module omitting the rule and then use it later. Therefore none qualifies as `PROVED_DERIVED_LEMMA`. Conversely, the guarded dispatch equations are observations of already-defined supplied-semantics operations, not definitions merely because they are useful during proof.

All four domain lemmas are relevant. The source computes `len(set(word))`, uses string `<` for score ties, and carries dynamically typed `Val` strings through the loop invariant and final `bestWord` postcondition. Cast definedness and projection idempotence provide the bridge from that dynamic domain to the supplied `str(IntSeq)` operations; set dispatch supplies the unique-character score; and `<` dispatch supplies the tie-breaker.

Evidence: [raw reconstructed inventory](/audit-output/evidence/02_reconstructed_inventory.json.log), [bijective comparison and all 21 entries](/audit-output/evidence/03a_inventory_bijection_and_manifest_classes.txt), [frozen program/spec/claims](/audit-output/evidence/04_frozen_program_verification_and_claims.txt), and [relevant supplied semantics](/audit-output/evidence/05_relevant_supplied_semantics_rules.txt).

## Stage 4 generation and mathematical judgment

With `PYTHONPATH=/reference`, I freshly invoked `tools.klean_preflight.check_generation` on the three required mounted paths. It returned `PASS`, rebuilt the generated project from clean state, found zero designated sorries, reported four obligations, and reproduced these hashes:

- Stage 1 export: `160981b3958478ffb7e0dbb87d5ef3d354f79b785845a1002b7dfbecefce0543`
- Discovery manifest: `2a54a24703df954d49d9f08e737518bab76bc0d1315c0dccde0deac377d7b9e4`
- Generated tree: `9728c45ff54bdfe307d6dad5e27fcf4bece8161a8f935c96146283ed9cf5acb6`

The obligation map is an exact ordered bijection with the independently identified domain set:

| Source rule | Generated obligation |
|---|---|
| `rule-0dda33275c7cbd177…f5bf83` | Exact string-cast definedness equivalence. |
| `rule-f85e27b93f985712…55f5e0` | Exact total-projection idempotence equation. |
| `rule-ec057976d8c8f7e9…17c3` | Exact guarded dynamic `set(str)` equation. |
| `rule-1684a1226f0f5683…1f20b` | Exact guarded dynamic string `<` equation. |

Each obligation preserves the source variables, guards, operations, result, source span, normalized hash, inventory hash, and discovery hash. There are no omitted or duplicate domain rules and no generated obligation for any of the 17 definitions. The selected status is a normal four-obligation generation, not `KLEAN_NO_OBLIGATIONS`.

The first Lean formula contains the normalization of source `#Ceil(@V)` to `True`, because `@V` is already bound at sort `Val`. This does not create a vacuous top-level obligation or weaken the rule: the formula still universally proves that the partial string projection is present exactly when `definedProjectStr V = true`. The other three obligations likewise have satisfiable guards (concrete string values witness them) and nonconstant conclusions. Thus no top-level conjunct is irrelevant, `True`, or otherwise vacuous.

The fixed generated target is uniquely `Klean158FindMax.Lemmas.targetStatement` in `Klean158FindMax/Lemmas.lean`, with definition SHA-256 `f089c29c95ea14538c4f40a8146210dca386c479161fa458c0a9d6ad5d6e0298` and statement SHA-256 `c5478f273aaf85e78137c527503fc6fb7b719f6b888fe97a7ff01c19b46c6e0d`. The observed declaration and its nine parameter bindings equal the generator manifest, preflight record, obligation map, and audit input.

Evidence: [successful fresh generation preflight](/audit-output/evidence/10_fresh_klean_preflight_success.txt), [generated sources and obligation map](/audit-output/evidence/11a_generated_and_candidate_sources.txt), and [target/hash identity](/audit-output/evidence/15_all_mounted_hashes_and_target_identity.txt).

## Stage 5 clean build, proof identity, and trust accounting

I created `/tmp/audit-work/158-find-max-proof-audit`, copied the deterministic generated project into it as `Base`, and copied only the candidate source/project files. A scan of all candidate Lean sources found no `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. The candidate has exactly one definition for each target parameter, does not declare or shadow `targetStatement`, and contains exactly one `theorem final` with the generator-recorded statement.

Both requested commands ran from this fresh project:

- `lake clean`: exit 0.
- `lake build`: exit 0, `Build completed successfully.`

The trusted final gate independently repeated candidate copying, Base replacement, clean, build, exact-statement checking, and the axiom audit; it returned `PASS`. The generated `Base/Klean158FindMax/Lemmas.lean` is byte-identical to the selected generated source (file SHA-256 `53d154a3569f4fd1ea3ec719c348fb9d183853901f5631595b426e5380e3f9f6`).

This container exposes host PIDs in procfs while system calls return namespaced PIDs, which initially prevented Lean from locating `/proc/<pid>/exe`. I used an audit-local `LD_PRELOAD` shim whose complete source is preserved in evidence; it only makes `getpid()` agree with procfs. It modifies neither candidate nor generated files and does not affect Lean definitions or proofs.

An audit file explicitly checked `Proof.final` against the full nine-argument fixed target and ran the exact command `#print axioms Proof.final`. Lean reported:

`'Proof.final' depends on axioms: [propext, Classical.choice]`

There is no `sorryAx` and no generated Klean trust axiom in the transitive dependency set. `propext` and `Classical.choice` are the two core Lean dependencies explicitly admitted by the trusted final gate's inventory policy; every one of the 42 generated trust declarations is therefore irrelevant to this proof. No dependency is unrecorded.

Evidence: [fresh-copy and forbidden-token scan](/audit-output/evidence/12_fresh_proof_project_copy_and_static_scan.txt), [clean](/audit-output/evidence/13_candidate_lake_clean.txt), [complete build output](/audit-output/evidence/14_candidate_lake_build.txt), [exact target and axiom output](/audit-output/evidence/16_exact_print_axioms_and_target_check.txt), and [trusted final-gate result](/audit-output/evidence/17_trusted_klean_final_gate.txt).

## Operational bridge and non-vacuity

I inspected each exact target binding rather than treating the clean build as sufficient:

| Target parameter | Candidate definition and comparison with frozen meaning |
|---|---|
| `_andBool_` | Boolean conjunction, matching the guard connective. |
| `applyBuiltin` | Calls an executable dispatch table whose `"set"`, singleton-string branch returns `setV(deduplicateCharacterCodes codes)`, exactly matching `builtins.k` and the dynamic source rule. |
| `applyCmp` | Its two-string branch calls `compareStrings`; operator `"<"` calls the exact lexicographic recurrence. |
| `codesOf` | Pattern-matches `str(codes)` and returns `codes`, exactly the frozen destructor rule. |
| `dedupCodes` | First-seen-order insert-if-absent recursion, matching `set.k`; this preserves the supplied semantics' set cardinality observation. |
| `definedProjectStr` | Returns true exactly for the `SortVal.inj_SortStr` constructor and false for every other `Val`. |
| `projectStrTotal` | Returns the exact string for string values. Its empty-string value outside the guarded string domain is a totalization only; no operational rule observes that fallback, and it remains a retraction satisfying the separately generated idempotence obligation. |
| `strLt` | Empty, proper-prefix, head-less, head-greater, and equal-head recursive cases exactly match `str.k` lines 49–54. |
| `project:Str?` | Returns `some` only for an exact one-item K sequence containing an injected string and ending in `.K`, matching generated injection and partial-cast definedness. |

I compiled a separate adversarial Lean audit covering all nine bindings. It checks `aba → ab` deduplication, already-distinct input, proper-prefix and reverse lexicographic order, equality, string and non-string `Val` cases, exact versus trailing K sequences, valid and invalid `set` dispatch, and multiple string `<` cases. It also defines and refutes constant-false definedness, constant-empty projection, identity deduplication, constant-false ordering/comparison, constant-none projection, and constant-none builtin dispatch. The audit exits 0. These witnesses show the load-bearing definitions are not constant, identity, hard-coded to the theorem, or vacuous and implement the operational branches used by the frozen program.

`Proof.final` is the one theorem over the one immutable generated declaration; it proves all four exact conjuncts after instantiating the nine audited operational definitions. It does not prove a duplicate, a weakened restatement, or a theorem disconnected from the generated target.

Evidence: [adversarial bridge source](/audit-output/evidence/18a_operational_bridge_audit_source.txt) and [successful Lean result](/audit-output/evidence/18_operational_bridge_adversarial_lean.txt). A hash index for the raw evidence is at [evidence index](/audit-output/evidence/19_evidence_sha256_index.txt).

VERDICT: PASS
LEGITIMACY: LEGIT
