# Independent audit: HumanEval `161-solve`

## Scope and result

I independently audited the protected Stage 3 classification, deterministic Stage 4 generation, and Stage 5 Lean proof for condition `kit-semantics` under `SUPPLIED_SEMANTICS`. The launcher-selected mode was `CLASSIFICATION_AND_PROOF`.

All mounted candidate and provenance material was treated as untrusted evidence. Trusted inventory, preflight, and mechanical-gate code came from `/reference/tools`. The authenticated Stage 4 producer sources came from `/reference/generation-tools`.

The reconstructed Stage 3 inventory and classifications are correct. The one true domain lemma is relevant to the frozen program, Stage 4 generated exactly its unweakened obligation, and the Stage 5 bridge implements K equality rather than merely exploiting the narrow theorem. The clean Lean proof has only the expected Lean logical-foundation axioms.

## Producer authentication

Before judging generated output, I hashed both generation-time producers and compared them with `source-manifest.json`, `generator-manifest.json`, and `/audit-input.json`.

| Producer | Recomputed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | exact match |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | exact match |

The producer bundle contains only those two sources and its source manifest. Its recomputed tree hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, matching `/audit-input.json`. Both manifests record generator image:

`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`

The immutable producer-source path in `/audit-input.json` is bound to that same image digest. Producer authentication therefore passed; no infrastructure `AUDIT_ERROR` applies.

## Stage 3 inventory reconstruction

Using the trusted rule-inventory implementation, I rebuilt the local verification-module closure of the frozen Stage 1 `verification.k`. The selected closure is exactly module `VERIFICATION`.

- Frozen `verification.k` SHA-256: `6ce1fc2291909e6514239c96aeaa95f9c44183d6e7edc4d9fff24cce53d284cf`
- Reconstructed inventory hash: `8e830da1fd92fcf9ad97885fd223cc1c66ee296544b87724dddfa010b5d7117e`
- Inventory size: 14 rules
- Ordered comparison with `/reference/lemma-discovery.json`: exact bijection
- Duplicated, omitted, extra, reordered, or unaccounted rules: none

For every entry, I recomputed the source span, normalized source text hash, and `source_rule_id = "rule-" + normalized_hash`. Every value matches the protected classification. The independent semantic classification is:

| Lines | Source rule ID | Classification | Independent rationale |
|---:|---|---|---|
| 8–9 | `rule-387d11f8474864387ce45c90f1ba7bc44da2dcb0e552a8b7845434062e527a49` | `DOMAIN_LEMMA` | Constructor disjointness: a nonempty `IntSeq` is not `.IntSeq`. It neither defines a named term nor performs ordinary execution. |
| 13–27 | `rule-a22bf74536ca2c9ab90997fa2778e59bb863fe55a97cb2d4ef4e0938017132fe` | `DEFINITION` | Defines the `loopBody` macro. |
| 30–43 | `rule-63de44a807e654f91177cf67175935a5d211c45c4dea2cce51f96809ae8edb68` | `DEFINITION` | Defines the `solveBody` macro. |
| 47–49 | `rule-13260ace346b9d3312c1c69885119f82365f8cd95478602565cbbd51523885bf` | `DEFINITION` | Defines `charAlpha`. |
| 52 | `rule-3e7420736a514e9735f2d54b143358800536f98bdef17bbbae3f53fab0417311` | `DEFINITION` | Base equation for `alphaAcc`. |
| 53–56 | `rule-7cea80b383444c0a24af307676d999b06567e3c19806f9704bb30082eaef567b` | `DEFINITION` | Letter recurrence for `alphaAcc`. |
| 57–60 | `rule-cf8204f153dc4880703edac662156a67163ad1f72b5d25e0cde7624a58eab5ab` | `DEFINITION` | Nonletter recurrence for `alphaAcc`. |
| 64 | `rule-6e22fa23d2b431489c1813a0e42c9379a6ddd997d1489360173a48d2a56dd71a` | `DEFINITION` | Base equation for `toggleAcc`. |
| 65–70 | `rule-c187a2ccd2c14dc676381be01081faa10437dcc5a5b4dd239f034830c42c9e2d` | `DEFINITION` | Letter recurrence for `toggleAcc`. |
| 71–76 | `rule-3b0125b6f25e2e0b93548d4e208f4684cf4f8c102113d3b20c4530fa13c34743` | `DEFINITION` | Nonletter recurrence for `toggleAcc`. |
| 80 | `rule-6ef920be7b128d7d43ac335f88c4df1507ecc50eacc0533f0bc398785c7c1273` | `DEFINITION` | Base equation for `lastChar`. |
| 81–82 | `rule-102913393a20fe11e1b5622563cb515de6283834d18cd6148c4982b55e138c6d` | `DEFINITION` | Recurrence for `lastChar`. |
| 86–87 | `rule-6250cd4b638d1bc7e9f40e84712e922075d6c68a96be3e77a3129478c69ec390` | `DEFINITION` | Letter-present branch of `solveResult`. |
| 88–89 | `rule-5d2df1091b88eaad6d77a78c0d8aae5544297a549790e441458d8125d5817724` | `DEFINITION` | No-letter branch of `solveResult`. |

Thus there are 13 definitions, one domain lemma, no operational rules, and no proved-derived lemmas. Every rule marked `simplification` is either a definition or the domain lemma.

The domain lemma is mathematically and operationally relevant. Supplied string iteration produces a one-character sequence `str(iCons(C, .IntSeq))`. `isalpha` tests whether the sequence is nonempty through `notBool (CS ==K .IntSeq)` before the ASCII alphabetic test. That result controls whether the solution follows the swap-case branch or the reverse branch. Constructor disjointness is therefore directly connected to the source program and postcondition.

Although Stage 1 also has a separate claim for this rule against a module that omits it, it is not a `PROVED_DERIVED_LEMMA`: `prove.sh` compiles and proves the main `verification.k`/`spec.k` task first and only afterward runs the lemma-only proof. It does not satisfy the required prove-first-then-use ordering.

## Stage 4 deterministic generation

I reran the exact requested trusted entry point, `tools.klean_preflight.check_generation`, with `PYTHONPATH=/reference` and the specified K workspace, protected discovery file, and generated project. Its final result was `PASS` with one obligation, 42 trust-inventory declarations, no sorries, and successful generated-project `lake clean` and `lake build`.

The independent source-domain set is exactly:

`rule-387d11f8474864387ce45c90f1ba7bc44da2dcb0e552a8b7845434062e527a49`

That singleton set agrees exactly and in order with the input manifest, obligation map, generated obligation list, and target provenance. There are no duplicate, omitted, irrelevant, or extra obligations. Because the true domain set is nonempty, `OK` with one obligation is the proper generation status; `KLEAN_NO_OBLIGATIONS` would have been invalid.

The generated conjunct preserves the complete source rule without a guard:

`∀ C : SortInt, _==K_ (kseq (inj (iCons C .IntSeq)) .K) (kseq (inj .IntSeq) .K) = false`

It quantifies the arbitrary head character and asserts exactly the nonempty-versus-empty constructor inequality. No antecedent, subcase, duplicated conjunct, target substitution, or weakening was introduced. The theorem is narrow enough that a constant-false bridge could satisfy it, but that does not make the conjunct vacuous; it makes the independent Stage 5 bridge audit essential.

The fixed generated target matches all authenticated records:

- Declaration: `Klean161Solve.Lemmas.targetStatement`
- Definition hash: `062a2d100055593c76b564e1807c3a59cd723214f4bbc212ceb0ddc0835d5353`
- Applied statement: `Klean161Solve.Lemmas.targetStatement «_==K_»`
- Statement hash: `e0b47abab3ca67a13fd4ba44fd52256e53e5a9154d3ea7bc242e4dd25e05e23e`
- Parameter binding hash: `b5e0704f0db14aafe3dc3639e37230dc0a2db173a975a62f1bc0d57827d242c7`
- Bound KORE symbol: `Lbl'UndsEqlsEqls'K'Unds'`

The trusted exporter independently reproduced the same target object and hashes. All recorded discovery, source, rule-inventory, obligation, generated-project, selected-tree, and producer-tree hashes checked successfully. The generated source tree was unchanged by the proof candidate.

## Stage 5 clean proof and target identity

I made a fresh project under `/tmp/audit-work/161-solve-proof-audit-2`, copied the candidate there, and overlaid the immutable generated project contents as `Base`. In that fresh copy, both required commands succeeded:

- `lake clean`: exit 0
- `lake build`: exit 0

The proof defines the sole bridge parameter exactly once:

```lean
noncomputable def «_==K_» (lhs rhs : SortK) : SortBool := by
  classical
  exact if lhs = rhs then true else false
```

`Proof.final` has exactly the fixed generated type:

`Klean161Solve.Lemmas.targetStatement Proof.«_==K_»`

The candidate neither modifies nor shadows `targetStatement`. Outside `Base`, the only Lean project sources are `Proof.lean` and `lakefile.lean`. Static and trusted mechanical checks found no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`.

The exact Lean output from the independent axiom query was:

```text
Proof.final : Klean161Solve.Lemmas.targetStatement Proof.«_==K_»
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. `propext`, `Classical.choice`, and `Quot.sound` are the standard Lean logical foundations explicitly permitted by the trusted Stage 5 gate. The 42 generated trust-inventory declarations were reconciled separately; `Proof.final` depends on none of them. There is no unrecorded candidate or generated proof escape.

The trusted Stage 5 mechanical gate independently returned `PASS`, with the same exact target identity, successful clean build, and the same three used axioms.

## Operational-bridge judgment

The bridge was checked against its KORE binding, source rule, supplied K semantics, and source solution—not merely against build success.

The K prelude gives `_==K_` the total `KEQUAL.eq` hook. On the generated inductive representation of K terms, the candidate returns K true exactly when its two `SortK` arguments are propositionally equal and K false exactly when they are unequal. This is the intended structural equality behavior for the relevant represented terms.

Independent Lean tests established:

- for all `lhs rhs`, the bridge is true iff `lhs = rhs`;
- for all `lhs rhs`, the bridge is false iff `lhs ≠ rhs`;
- `.K ==K .K` evaluates true;
- an arbitrary singleton `iCons C .IntSeq` term compared with `.IntSeq` evaluates false;
- a singleton term compared with itself evaluates true.

I also tested counterfactual mutations. A constant-false bridge can prove the narrow generated constructor-disjointness target but fails reflexivity, confirming why theorem success alone would be insufficient. A constant-true bridge fails the target. The submitted bridge passes both the fixed obligation and the broader equality checks. It is not constant, hard-coded to the target, an identity passthrough, or otherwise operationally convenient but false.

## Execution-environment note

The first preflight attempt exposed a sandbox PID-namespace issue in Lean/Lake executable discovery: the process PID did not index the corresponding executable under the mounted `/proc`. I preserved those failures as evidence. For the successful rerun, I used an audit-only `LD_PRELOAD` shim that reports the host `NSpid` value for `getpid`, allowing the locked Lean 4.22.0 toolchain to locate itself. The shim changes no generated or candidate source and does not alter Lean elaboration or proof logic. Toolchain version/commit checks, preflight, clean builds, axiom inspection, adversarial tests, and the trusted Stage 5 gate then all completed successfully.

## Evidence

Raw commands and complete outputs are under `/audit-output/evidence/`. Principal records include:

- `structural_checks.py` and `structural_checks.log`: producer authentication, source and tree hashes, inventory reconstruction, manifest validation, source-rule/obligation bijection, and fixed target reproduction.
- `derived_lemma_order_check.log`: Stage 1 ordering that excludes `PROVED_DERIVED_LEMMA`.
- `operational_bridge_sources.log`: frozen program, relevant verification rules, and supplied operational semantics.
- `preflight_rerun.log` and `preflight_rerun_configured.log`: preserved environment-discovery failures.
- `lean_environment_workaround.log` and `preflight_rerun_success.log`: contained PID correction, locked toolchain identity, and successful trusted preflight.
- `fresh_clean_build.log`: preserved first copy-layout failure.
- `fresh_clean_build_success.log`: successful fresh `lake clean` and `lake build`.
- `proof_static_checks.log`: candidate-source, tree, forbidden-token, target-shadowing, parameter, and theorem-type checks.
- `axioms_and_bridge_tests.log`: exact axiom output plus adversarial and counterfactual bridge tests.
- `trusted_stage5_mechanical_gate.log`: independent trusted Stage 5 gate result.

VERDICT: PASS
LEGITIMACY: LEGIT
