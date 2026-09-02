# Independent audit: 81-numerical-letter-grade

## Scope and result

I audited Stage 3 lemma classification, deterministic Stage 4 generation, and the Stage 5 Lean proof for condition `kit-semantics` in `SUPPLIED_SEMANTICS` mode. The launcher and environment both report `CLASSIFICATION_AND_PROOF`.

The protected classification is complete and correct, the two generated Lean obligations are an exact bijection with the independently identified domain lemmas, and the submitted Lean definitions implement the frozen operational meaning on the complete obligation domain. The fresh proof build and axiom audit pass.

## Generator-source provenance gate

This gate passed before any Stage 4 judgment.

- `/reference/generation-tools/klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `/reference/generation-tools/klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`
- Producer bundle tree: `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`
- Immutable generator image: `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`

The two file hashes agree exactly among the mounted files, `source-manifest.json`, and `generator-manifest.json`. The image ID agrees between both manifests and the image-keyed producer path recorded in `/audit-input.json`; the producer bundle tree agrees with the launcher hash. Evidence: [producer manifests](/audit-output/evidence/01b-producer-manifests.txt), [hash recalculation](/audit-output/evidence/05-recorded-hash-recalculation.txt).

## Frozen-input and inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` implementation on the frozen `/reference/k-proof` workspace produced:

- verification module: `VERIFICATION`
- local verification-module closure: exactly `VERIFICATION`
- `verification.k` SHA-256: `b2323c2e29dd519f7c6457aac14996b82d5bd34e3eb9c6a939a6576d8b81f232`
- rule count: 16
- canonical inventory SHA-256: `00b871c4197f4e4b8c563bbbfd4e2d0186e6f8ce8b19b803de1e23228bec6727`

For every entry, the `source_rule_id` is `rule-` followed by the independently recomputed normalized-source SHA-256. The complete reconstruction is in [02-reconstructed-rule-inventory.txt](/audit-output/evidence/02-reconstructed-rule-inventory.txt).

The reconstruction and `/reference/lemma-discovery.json` have identical ordered identities and inventory hash. Both have 16 unique entries, with no omitted, extra, duplicated, or reordered identity. Every reconstructed source span, normalized hash, attribute list, and derived ID also agrees with the corresponding generated input record. Evidence: [06b-inventory-discovery-bijection.txt](/audit-output/evidence/06b-inventory-discovery-bijection.txt).

### Independent per-rule classification

| Frozen span | Source rule ID | Classification | Independent reason |
|---|---|---|---|
| 9–46 | `rule-913248f07e570f8e9cf4e10ccd2e45330ef636bc76303ff5ad67835ed0374797` | `DEFINITION` | `GRADE-STEP` is a named macro expanding to the exact nested grading AST. |
| 49–57 | `rule-ab056d115b33e511e623da01fcf497700ccb79847bda7824277b21bcbf6345af` | `DEFINITION` | `GRADE-PROGRAM` is the named whole-program AST macro. |
| 61 | `rule-9407ea7d6a4de9439363534f67694ee47e6ff907df9b35ff34b4a866b6602e7b` | `DEFINITION` | Defines the numeric-domain predicate as Int or Float. |
| 64 | `rule-c7226673454c9937bb81a182a982d47a41b4594d2a6ea2a53b050512a0f2120a` | `DEFINITION` | Empty-sequence base equation for `allGradeNumbers`. |
| 65–66 | `rule-43811671f02c87468177174e87d1e0fa17daa38184b24c78d16b3da6de2f02be` | `DEFINITION` | Structural recurrence for `allGradeNumbers`. |
| 72 | `rule-4aeb120c39e619e56b1bb2949769afb0de9f65a14815f8f8304abf8eabb853b0` | `DEFINITION` | Int case of the named `gradeEq` summary. |
| 73 | `rule-4b0057401ad369826c0c0f086d2de62b6bbdf480fcdb4ce5c3b9324e5f6b73cb` | `DEFINITION` | Float case of the named `gradeEq` summary. |
| 74–75 | `rule-1dcc8c06aaff13c93012f8657da7bc9eee86e8cd2b9481c7d964bc6d833b79f8` | `DEFINITION` | Guarded nonnumeric totalization of `gradeEq`. |
| 78 | `rule-8b8204b28122ab97e84e35c1504bdd05d5beed4934819f44dabcbedbc9f85f32` | `DEFINITION` | Int case of the named `gradeGt` summary. |
| 79 | `rule-5e4220b4a59610d50f112f372bc52b526f8251e55fcb996f2f236bbe7a0db863` | `DEFINITION` | Float case of the named `gradeGt` summary. |
| 80–81 | `rule-5924db7e5f35f3f96f7f05931067b1ad392bdb7dcfde5b27f1927e6c1875992c` | `DEFINITION` | Guarded nonnumeric totalization of `gradeGt`. |
| 84–87 | `rule-bb0819476c6343e9119c99a78b2ae8eb72ebad42dbc170a9eaa3c4af6f39f115` | `DOMAIN_LEMMA` | Guarded consolidation of the pre-existing Int/Float equality dispatch into `gradeEq`; marked `[simplification]`. |
| 88–91 | `rule-79c1c8d9ff74acff507b7b4a319ee7d9d034df3550afdf9196f29291297713c8` | `DOMAIN_LEMMA` | Guarded consolidation of the pre-existing Int/Float greater-than dispatch into `gradeGt`; marked `[simplification]`. |
| 96–133 | `rule-c5a38f6c6613309dfda5d4776797f7bf662da9f4d9a3f34f58ebec448836c677` | `DEFINITION` | Defines the named single-grade summary by the grading table. |
| 138 | `rule-f3847c739a1d22b36c279a649f98bc18c2073c8ec8582b54956c1f02f33dc66c` | `DEFINITION` | Base equation for the tail-recursive result summary. |
| 139–143 | `rule-954dcecb4ff810ef1b6ce869747c0457f931b774b64fd1f2197b5d3a0265ac57` | `DEFINITION` | Structural recurrence for the tail-recursive result summary. |

The two simplifications are not definitions because their left side is the pre-existing `applyCmp` operator rather than a newly defined summary. They are not ordinary operational rules because they rewrite no program configuration or observation state. They are not `PROVED_DERIVED_LEMMA`: Stage 1 compiles `verification.k` containing both rules before its only positive target `kprove` invocation, and there is no earlier rule-free proof of either exact statement. See [07-stage1-proof-order-and-uses.txt](/audit-output/evidence/07-stage1-proof-order-and-uses.txt).

Both domain lemmas are mathematically valid under the supplied semantics. For an Int left operand, the fixed rules reduce equality/greater-than to `eqF(intToF(I), F)`/`gtF(intToF(I), F)`; for a Float left operand they reduce to Float equality/`gtF`. Those are exactly the constructor equations of `gradeEq` and `gradeGt`. The guard excludes every other `Val` constructor. They are also directly relevant: every source grading branch compares a grade to a Float threshold using `==` or `>`, and `gradeValue`/`gradeAcc` in the postcondition use the corresponding summaries.

Thus all `[simplification]` rules are correctly classified as `DOMAIN_LEMMA`, and the independently determined domain set has exactly two entries.

## Stage 4 deterministic generation

The trusted preflight was rerun with `PYTHONPATH=/reference`, the specified frozen workspace, discovery manifest, generation directory, and pinned toolchain lock. It returned `PASS`, obligation count 2, designated sorry count 0, and successfully ran its isolated `lake clean` and `lake build`. Full returned evidence is [11-rerun-klean-preflight-success.txt](/audit-output/evidence/11-rerun-klean-preflight-success.txt).

The initial unshimmed preflight reached the build and exposed an audit-sandbox issue: Lean could not resolve `/proc/<current-pid>/exe`. A narrow preload shim redirected only that lookup to the available `/proc/self/exe`; Lean then reported the exact pinned version and commit. This did not modify any mounted input. The diagnosis and successful toolchain check are preserved in [09-toolchain-diagnostic.txt](/audit-output/evidence/09-toolchain-diagnostic.txt) and [10-lean-procself-workaround.txt](/audit-output/evidence/10-lean-procself-workaround.txt).

### Obligation bijection and mathematical judgment

The obligation map contains exactly these two conjuncts, in the same order as the independently identified domain set:

1. For all `F : SortFloat` and `V : SortVal`, if `isGradeNumber V = true`, then `applyCmp "==" V (injFloat F) = gradeEq V F`.
2. For all `F : SortFloat` and `V : SortVal`, if `isGradeNumber V = true`, then `applyCmp ">" V (injFloat F) = gradeGt V F`.

Each conjunct has the exact source rule ID, source span, normalized hash, inventory hash, operator string, sorts, Float-to-Val injection, guard, and right-hand summary. There are no extra or duplicated obligations, no omitted domain rule, no changed guard, and no weakened right side. The bound guard is not vacuous for the submitted operational definition: it is `true` for every injected Int and Float. Evidence: [obligation map and target](/audit-output/evidence/12-stage4-obligations-and-target.txt), [independent bijection](/audit-output/evidence/13-independent-obligation-target-bijection.txt).

### Fixed generated target

The unique generated declaration is `Klean81NumericalLetterGrade.Lemmas.targetStatement`. Its metadata is:

- definition SHA-256: `40098983cd633833d65c09f60c20fedcb1a20d9382b4e0e5b2a3dc8d8018e619`
- instantiated statement SHA-256: `f486a227f41afc456b054856aba86cf4116399675f7f861ef1387a23b4e3b17b`
- generated tree SHA-256: `6605b72d5f62c698fc9e460110023b0818ceeb0e036858d36de34c384ad0161e`

The declaration, definition, statement, parameter bindings, and hashes agree exactly across the generated project, generator manifest, launcher audit input, and rerun preflight. The target definition synthesized from `obligation-map.json` occurs exactly once in `Lemmas.lean`.

All 801 recorded Stage 1 file hashes match with no missing or extra file. The mounted Stage 1 tree/export, Stage 2 audit tree, discovery file, Stage 4 tree, producer tree, generated tree, and candidate tree all match their recorded hashes. The Stage 4 sidecar and obligation-map hashes also match. Evidence: [05-recorded-hash-recalculation.txt](/audit-output/evidence/05-recorded-hash-recalculation.txt), [24-all-accessible-recorded-hashes.txt](/audit-output/evidence/24-all-accessible-recorded-hashes.txt). The launcher also records a prior Stage 5 invocation-directory hash, but that host invocation directory is intentionally not among the mounted audit inputs; the mounted candidate itself matches `lean_workspace_sha256` and was rebuilt independently below.

## Stage 5 Lean proof

### Fresh rebuild and target identity

A fresh workspace was created at `/tmp/audit-work/stage5-fresh-001`. Only the candidate `Proof.lean`, `lakefile.lean`, and `lean-toolchain` were copied into it, and the immutable generated project was copied as `Base`. The Base tree hash before the build was the required `6605b72d...`; its source tree remained unchanged after the build.

Both mandated commands passed from this fresh workspace:

- `lake clean`: exit 0
- `lake build`: exit 0

Complete output is [16-fresh-lake-clean-build.txt](/audit-output/evidence/16-fresh-lake-clean-build.txt).

The candidate contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. It does not define or shadow `targetStatement`; the fixed target remains unique and hash-identical after the build. `Proof.final` contains the manifest’s exact instantiated target statement once. Static and post-build evidence: [14-candidate-static-inspection.txt](/audit-output/evidence/14-candidate-static-inspection.txt), [18-postbuild-target-and-forbidden-checks.txt](/audit-output/evidence/18-postbuild-target-and-forbidden-checks.txt).

Lean’s exact `#print Proof.final` confirms that the theorem proves the fixed generated declaration instantiated with the candidate’s four bound definitions, not a duplicate theorem or modified proposition. See [20-print-Proof-final.txt](/audit-output/evidence/20-print-Proof-final.txt).

### Axiom accounting

Exact `#print axioms Proof.final` output is in [17-print-axioms-Proof-final.txt](/audit-output/evidence/17-print-axioms-Proof-final.txt). The dependencies are:

- Generated and recorded in `trust-inventory.json`:
  - `«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int»`
  - `«_==Float_»`
  - `«_>Float__FLOAT_Bool_Float_Float»`
- Lean core logical foundations, not candidate declarations:
  - `propext`
  - `Classical.choice`
  - `Quot.sound`

There is no `sorryAx`, no candidate-added axiom/opaque declaration, and no unknown generated dependency. The generated three names, declaration kinds, exact types, source files, and source lines all match the trust allowlist. Reconciliation: [19b-axiom-reconciliation.txt](/audit-output/evidence/19b-axiom-reconciliation.txt).

### Operational-bridge audit

The four target parameters were located as exact `def`s in [Proof.lean](/candidate/Proof.lean:156):

| Bound parameter | Frozen meaning on its complete obligation domain | Candidate implementation and judgment |
|---|---|---|
| `LblapplyCmp...MPY-CORE...` | For `"=="`/`">"`, numeric `V`, and Float right operand, dispatch by the Int/Float constructor to the fixed Float rules. | Lines 156–228 pattern-match on both operands and operator. The four load-bearing Int/Float branches use the same promotion/equality/greater-than primitives as `float.k`. This is neither constant nor a call to the theorem’s right side. PASS. |
| `LblgradeEq...VERIFICATION...` | Int: `eqF(intToF(I), F)`; Float: Float equality; nonnumeric: false. | Lines 230–232 call `cmpGradeEqImpl`, whose three cases are exactly those equations. PASS. |
| `LblgradeGt...VERIFICATION...` | Int: `gtF(intToF(I), F)`; Float: `gtF(G, F)`; nonnumeric: false. | Lines 234–236 call `cmpGradeGtImpl`, whose cases use exact Int promotion and Float greater-than. PASS. |
| `LblisGradeNumber...VERIFICATION...` | `isInt(V) orBool isFloat(V)`. | Lines 238–239 return true exactly for the generated Int and Float injections and false for every other `SortVal` constructor. PASS. |

The helpers use exactly the bound primitive observations: Float equality, Float greater-than, and `Int2Float(I, 53, 11)`. The `.getD false` branches totalize Klean’s `Option` carrier only when a trusted primitive produces no modeled result; the corresponding frozen K symbols are total on the obligation sorts. On every modeled result, the candidate preserves that result exactly. The three primitive dependencies are visible in `#print axioms` and are recorded in the generator trust inventory.

Independent Lean bridge checks established symbolically, for arbitrary Ints/Floats and arbitrary trusted primitive results:

- `isGradeNumber(injInt i) = true`, `isGradeNumber(injFloat f) = true`, and a nonnumeric witness is false;
- both Int and Float cases of `gradeEq` and `gradeGt` reduce to the exact promotion/Float-hook expressions;
- both Int and Float cases of `applyCmp "=="` and `applyCmp ">"` equal the respective honest summaries; and
- the submitted `isGradeNumber` agrees with the deterministically generated definition on every `SortVal` constructor.

The check source is [BridgeChecks.lean](/audit-output/evidence/BridgeChecks.lean); it elaborated successfully in [21d-operational-bridge-final-checks.txt](/audit-output/evidence/21d-operational-bridge-final-checks.txt).

Adversarial and counterfactual tests were deliberately separated from the submitted workspace:

1. Negating the Int/Float equality dispatch caused `lake build` to fail with the load-bearing Int case reduced to an unsolved `False` goal. This shows the proof discriminates a wrong dispatch when the honest guard remains satisfiable.
2. Replacing `isGradeNumber` by constant false still built, demonstrating that the target could be made vacuous by a dishonest guard. The submitted definition is not that mutation; the all-constructor check above establishes the real guard.
3. Replacing Int promotion by hard-coded `0.0` also still built, demonstrating that theorem closure alone does not validate the shared implementation. The submitted definition instead calls the exact recorded `Int2Float(I, 53, 11)` primitive, as verified symbolically and by axiom accounting.

Exact mutation diffs are [27-counterfactual-mutation-diffs.txt](/audit-output/evidence/27-counterfactual-mutation-diffs.txt); results are [wrong-dispatch failure](/audit-output/evidence/22-counterfactual-bad-apply-mutation.txt), [vacuous-guard success](/audit-output/evidence/23-counterfactual-vacuous-guard-mutation.txt), and [hard-coded-promotion success](/audit-output/evidence/25-counterfactual-hardcoded-promotion-mutation.txt). These probes confirm that the independent operational comparison is necessary and that the actual submitted definitions pass it.

## Evidence index and conclusion

The exact major commands and their result files are indexed in [evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md). No prior PASS, classification rationale, candidate comment, or prior proof log was treated as authoritative; each decisive identity, classification, build, axiom dependency, and bridge equation was rechecked against frozen source or trusted tooling.

The Stage 3 classification is complete and mathematically correct; Stage 4 is provenance-bound, deterministic, bijective, and neither weakened nor vacuous under the honest bridge; and `Proof.final` is a clean proof of the exact fixed target with fully accounted trust and faithful operational parameter definitions.

VERDICT: PASS
LEGITIMACY: LEGIT
