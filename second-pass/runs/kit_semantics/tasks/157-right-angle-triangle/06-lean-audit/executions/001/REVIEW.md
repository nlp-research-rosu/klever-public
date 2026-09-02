# Independent Stage 3/4 audit: 157-right-angle-triangle

## Scope and result

The launcher environment and `/audit-input.json` both select `CLASSIFICATION_ONLY` for condition `kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`. The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; `/candidate`, a Lean workspace, a Lean invocation, and a Stage 5 result are all absent.

I independently reconstructed the local rule inventory, reclassified every rule from the frozen K source and supplied operational semantics, verified producer provenance and all recorded input/tree hashes, reran `tools.klean_preflight.check_generation`, and independently checked the empty source-rule/obligation mapping and absent target. The protected Stage 3 classification and deterministic Stage 4 output are legitimate.

## Producer provenance gate

I hashed the mounted generation-time sources before judging Stage 4:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both values exactly match `source-manifest.json` and `generator-manifest.json`. The immutable generator image ID is consistently `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` in the source manifest, generator manifest, and the image-addressed producer-source path recorded by `/audit-input.json`. The independently recomputed producer-source tree hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, also matching the launcher record. Thus the infrastructure producer-source gate passes; no `AUDIT_ERROR` applies.

Raw evidence: [producer hashes and manifests](/audit-output/evidence/01-producer-provenance.txt), [independent hash summary](/audit-output/evidence/41-independent-hash-summary.txt).

## Inventory reconstruction and bijection

Using the trusted canonical inventory implementation directly on `/reference/k-proof`, I reconstructed:

- verification file SHA-256: `be2594dcc8e487fab6f75f1c592dfe3c30240ec2cc8cd050dba70375cfb8cf75`;
- selected module: `VERIFICATION`;
- local verification-module closure: exactly `[VERIFICATION]`;
- ordered rule count: 14; and
- canonical inventory SHA-256: `f18755c8299c46ecc0c49530526a2460c852955ad805fe23a7788caeb6175604`.

The reconstruction recomputed every source span, comment-normalized rule hash, and `source_rule_id`. Trusted manifest validation then compared the ordered canonical records bijectively with `/reference/lemma-discovery.json` and exited 0. There are no omitted, duplicate, extra, reordered, or hash-changed rules. The discovery file itself hashes to `87e2cfb5ce97be8697808912b2750b8cfa2a3460a8209c07a92a35dbc915defc`, matching every recorded binding.

Raw evidence: [full reconstructed inventory and bijection](/audit-output/evidence/06-inventory-reconstruction-and-bijection.txt).

## Independent classification judgment

I did not accept the protected rationales as authoritative. I compared the rules to `solution.py`, its exact `solution.mpy` translation, `spec.k`, and the supplied operator, Float, Boolean, and syntax semantics.

| Span | Source rule | Classification | Independent basis |
|---|---|---|---|
| 9–51 | `rule-65ee359690c078f314b8315c3c94f6b34835bd20c0477637da6af76778cb6311` | `DEFINITION` | Nullary macro naming the exact closure/return AST of the source body. |
| 58–60 | `rule-a1eb58804a065f00833d0cbff55cae05f7761567a754ebd590c73ddaa855646c` | `DEFINITION` | Concrete equation for the named `trustedFloatEq` proof term, reducing to the supplied Float equality hook. |
| 64–70 | `rule-c6539c39ccea106c35e916b768648493791aeac70bc31344ebb53f72dbce4b71` | `OPERATIONAL_RULE` | K-cell observation step after both Float operands have evaluated; it preserves the continuation and routes Float equality to the named proof term. |
| 79 | `rule-b1545a06cd0d3ee4ecafe211cfda36d9751f52e9da5c1c1de2cbe40bac4f6a0d` | `DEFINITION` | Integer branch of `ratSquare`. |
| 80 | `rule-31b9c981ad4580f01b7319d650db78633cceddfae0847e5882e90719f8f93a15` | `DEFINITION` | Float branch of `ratSquare` using supplied `mulF`. |
| 82 | `rule-aa80bc4e205f53786d399a0371853b4f4eae4815b58b747ea925bc44702ee37e` | `DEFINITION` | Int/Int branch of `ratAdd`. |
| 83 | `rule-9fb7033cdbeb63a2d02cc452e8e120a0703114f66571646d17900b17d023ccda` | `DEFINITION` | Float/Float branch of `ratAdd` using supplied `addF`. |
| 84 | `rule-df4850e1b3b778356ac4b1e4fb8f71d6b6e16b0e00f292bd3c53d92dc38fff98` | `DEFINITION` | Int/Float branch of `ratAdd` using supplied conversion and addition. |
| 85 | `rule-26fd9a98998e60f90ca8da1882e9dd903042f49046e2e06c353ae351866725aa` | `DEFINITION` | Float/Int branch of `ratAdd` using supplied conversion and addition. |
| 87 | `rule-010bd337cb206f908725187e688369f657100fa2471779046a1410fbc1698f55` | `DEFINITION` | Int/Int branch of `ratEq`. |
| 88 | `rule-1afabb2501ba90f7b6b2f4a191175e8345881ad804004a8236b0d9f6c1f2938b` | `DEFINITION` | Float/Float branch of `ratEq` in terms of the named proof term. |
| 89 | `rule-f057392d9a01c96d24175b0d4f7208b353fa74cbca6db6a0fe229d27cbb63742` | `DEFINITION` | Int/Float branch of `ratEq` using supplied `eqIF`. |
| 90 | `rule-b0af0664109d2a9418b589eebb1c7d92db991a458e003b53c3df708fa93f9f96` | `DEFINITION` | Float/Int branch of `ratEq` using the supplied canonical argument order. |
| 92–95 | `rule-d8d41e07eca28f709366e4001ff4bb2533907409c202365ff87267e3f7c2a3c5` | `DEFINITION` | Composition defining the three Pythagorean alternatives in `ratExpected`. |

The operational classification at lines 64–70 follows behavior, not its comment: fixed semantics first dispatches an evaluated `Compare` to `applyCmp`, whose Float-equality case returns the Float equality hook. The local rule is instead a K-cell observation step for that same evaluated operation and continuation. It is not an equation asserting a mathematical property. The line 58–60 rule is likewise definitional: it names the proof-domain primitive and supplies its concrete evaluator; it does not assert a proposition about program results.

The `ratSquare`, `ratAdd`, `ratEq`, and `ratExpected` equations define the postcondition vocabulary. Even though `ratExpected` denotes the requested expression, it merely expands that expression and does not assert that the program satisfies it. None is a hidden domain fact. All definitions are relevant to the exact source body or its postcondition.

Independent totals are 13 `DEFINITION`, one `OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and zero `DOMAIN_LEMMA`, exactly matching Stage 3. No inventory rule has the `simplification` attribute, so the simplification-category restriction is satisfied. No derived-lemma provenance claim is made.

Raw evidence: [frozen source and semantic index](/audit-output/evidence/07-frozen-source-and-semantic-rule-index.txt), [relevant supplied semantics](/audit-output/evidence/08-relevant-supplied-semantics.txt), [rule-by-rule reassessment](/audit-output/evidence/40-independent-classification.tsv).

## Stage 4 integrity, bijection, and target identity

I independently implemented both recorded tree-hash framings and recomputed all launcher bindings. The resolution hash, Stage 1 workspace tree, Stage 1 export tree, all 1,513 Stage 1 regular-file hashes and exact file set, selected K-audit tree, Stage 3 discovery file, producer-source tree, selected generation tree, generated-project tree, verification file, obligation map, trust inventory, and both selected-artifact hashes all match `/audit-input.json` and the generation manifests.

The trusted `tools.klean_preflight.check_generation` initially could not run `lake clean` because the sandbox blocks Lean 4.22's numeric `/proc/<pid>/exe` lookup. I preserved that failure. A narrow temporary preload shim under `/tmp/audit-work` supplied the pinned Lean-family executable path only; it did not modify any mounted artifact. Lean then reported version 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock. The exact trusted check was rerun with `PYTHONPATH=/reference` and returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty-output SHA-256 `e3b0c442…b855`;
- `lake build`: exit 0, output SHA-256 `836e946d…6c48`;
- obligation count 0;
- target `null`;
- designated sorry count 0; and
- unchanged Stage 1, Stage 3, and generated-tree hashes.

Raw evidence: [initial environmental failure](/audit-output/evidence/10-check-generation.txt), [shim diagnosis and pinned Lean version](/audit-output/evidence/26-lean-app-path-shim.txt), [successful trusted rerun](/audit-output/evidence/27-check-generation-rerun.txt).

The mathematical domain set is genuinely empty after independent classification. Correspondingly, `obligation-map.json` contains exactly empty `source_rules`, `obligations`, and `trust_parameters` arrays; `generator-manifest.json` records obligation count 0 and target `null`; the generated `Lemmas.lean` contains only imports, comments, and an empty namespace; and no generated Lean file declares `targetStatement`. Thus the source-rule/obligation map is an exact empty bijection. There is no conjunct to omit, duplicate, weaken, make vacuous, or render irrelevant, and no fixed target that could have changed.

The generated project hash is `c971aec604ac4594065cbca2bbc8b3860df3b11deaa6af78f2151412cbcd3331`; the obligation-map file hash is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`. Both match the generator manifest and audit input.

Raw evidence: [generated target files](/audit-output/evidence/39-generated-target-files.txt), [target and Stage 5 absence](/audit-output/evidence/38-target-and-stage5-absence.txt), [full independent hash audit](/audit-output/evidence/37-independent-hash-and-zero-obligation-check.txt).

## Stage 5

Stage 5 is correctly absent in `CLASSIFICATION_ONLY` mode. There is no generated target and no `/candidate`; the audit input records null Lean workspace, null Lean invocation, and null Stage 5 result. Therefore clean candidate build, `#print axioms Proof.final`, target shadowing, proof identity, and operational-bridge parameter checks do not apply.

## Final judgment

The Stage 3 classification is complete and semantically correct, its true domain-lemma set is empty, and Stage 4 deterministically and faithfully represents that empty set with no target. Producer provenance, manifests, tree hashes, source-rule mapping, and the trusted clean-build preflight all pass. The selected `KLEAN_NO_OBLIGATIONS` status is legitimate.

VERDICT: PASS
LEGITIMACY: LEGIT
