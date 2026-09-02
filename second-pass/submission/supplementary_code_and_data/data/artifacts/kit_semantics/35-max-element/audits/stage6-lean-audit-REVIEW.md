# Independent audit: HumanEval 35-max-element / kit-semantics

## Outcome

I independently audited Stage 3 classification, deterministic Stage 4 generation, and the Stage 5 Lean proof in launcher mode `CLASSIFICATION_AND_PROOF` with semantics mode `SUPPLIED_SEMANTICS`. I did not rely on any prior PASS, classification rationale, proof comment, or review. The frozen program is:

```python
def max_element(l: list):
    return max(l)
```

The protected classifications are correct, the 15 generated obligations are the exact nonempty domain-lemma set, and `Proof.final` proves the unchanged generated target with operationally honest bindings. The result is PASS / LEGIT.

## Producer and input identity

Before judging Stage 4, I hashed the exact generation-time producer sources:

| Producer | SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |

Both hashes match `source-manifest.json` and `generator-manifest.json`. The producer-source tree hash is `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`, matching `/audit-input.json`. The immutable generator image ID is consistently `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6` in the source manifest, generator manifest, and launcher-bound immutable source-bundle path.

The other launcher-bound identities also match: Stage 1 pipeline tree `8a6526d1111d0694a97ab24715d01e8d70fff9884c83d5113598ebf9f7f749d2`, Stage 1 export tree `a650785d8c11e43b411856b653cbad0f465f6d09df27702a206b6f8768cad759`, Stage 2 audit tree `cffec7207d928a2099e3dbf9b409c623a4f686395f873784efa6740de56e3775`, Stage 3 manifest `0432716be2a252959dd9cf6bd24aa11488b76d03589a04434c400944d2589331`, Stage 4 pipeline tree `f4acd24b47ada5b26fc127912acf59ca967edea99d2a17a33cc5369c34ae54dc`, generated export tree `6eedeca43fb0e6ce143a75bfc6ce3f08755dae826ef9b99b0a1fdaaf9bfe38f2`, and Stage 5 candidate pipeline tree `bde1a31039b473d712889672862b142f673f68faba741c7fc91d18ded7b4eac4`. Every regular Stage 1 file hash also matches the launcher-recorded map.

The full producer and input comparisons are in `evidence/02_mechanical_reconstruction_corrected.log`.

## Inventory reconstruction and Stage 3 classification

Using the trusted local rule-inventory implementation, I reconstructed the local verification-module closure of the final frozen `verification.k`. The selected module is `VERIFICATION`; its local closure is exactly `['VERIFICATION']`. The source hash is `cad7035d9ebd863f4d75692b08d03413204df13a74ebcb52e4cda1bfb35e6c10`.

The reconstruction contains 55 rules and has inventory hash `a2523def47030dccad31ef8683dd617cfc620e1f05b3fe7f963639ba8eee7c2f`. For every rule I recomputed the source span, comment-insensitive normalized source, normalized SHA-256, and `source_rule_id = "rule-" + normalized_sha256`. The protected Stage 3 manifest is a bijective match in the same order: no omitted, duplicated, extra, reordered, or altered identity exists.

My independent classification is:

| Class | Count | Judgment |
|---|---:|---|
| `DEFINITION` | 40 | Correct |
| `DOMAIN_LEMMA` | 15 | Correct |
| `OPERATIONAL_RULE` | 0 | Correct |
| `PROVED_DERIVED_LEMMA` | 0 | Correct |

The 40 definitions introduce and define named summaries or proof terms: total projections; `isNumericV`, `allNumericVS`, and `allStrVS`; the opaque concrete float-max twin; `codesOf`; the four-way `numericView`; the exhaustive numeric comparison table; and the numeric/string maximum folds and specialized accumulators. Each has a new defined head or is a recurrence/case of such a head. None is an ordinary imported-language execution rule.

The 15 domain lemmas are exactly:

| Frozen lines | Count | Domain fact |
|---|---:|---|
| 9–11, 46–48, 68–70, 81–83 | 4 | Definedness of the partial Val projections is characterized by the corresponding sort predicate. |
| 15–17, 52–54, 74–76, 87–89 | 4 | A guarded symbolic partial projection equals its named total projection. |
| 22–25 | 1 | The imported `applyCmp` Int case agrees with guarded Int projection and `>Int`. |
| 63–64 | 1 | Symbolic `maxFloat` agrees with the concrete opaque twin. |
| 132–135, 136–139 | 2 | Imported dynamic `applyCmp` agrees with the numeric and string comparison summaries on their respective domains. |
| 143–151 | 3 | Int, Float, and Bool value-sort predicates are mutually exclusive. |

These are facts about existing imported casts, comparison dispatch, the `FLOAT.max` hook, and sort disjointness—not definitions of their left-hand operations and not ordinary execution rules. Stage 1 does not first prove any exact one in a module omitting the rule and then use it later, so none qualifies as `PROVED_DERIVED_LEMMA`. They are all relevant: `max` compares Int/Bool/Float mixtures or strings, the postcondition identifies the maximum element, and the Stage 1 summaries require exactly these projection, comparison, float, and guard-disjointness bridges. There is no unrelated domain fact.

Every rule carrying `simplification` is in one of the two permitted classes. Full rule text, spans, hashes, IDs, attributes, and classifications appear in `evidence/02_mechanical_reconstruction_corrected.log`.

## Stage 4 generation and mathematical obligation audit

I directly reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, `/reference/k-proof`, `/reference/lemma-discovery.json`, and `/reference/klean-generation`. It returned `PASS` with 15 obligations, zero designated sorries, the expected generated-tree hash, and successful generated-project clean/build commands. The complete returned evidence is `evidence/07_klean_preflight_pass.log`.

Independently of that structural result, I compared the ordered set of independently classified domain IDs with the Stage 4 source-rule set and obligation map. All three are the same 15-element ordered set. Each obligation has the exact reconstructed source span, normalized source hash, inventory hash, discovery-manifest hash, and recomputed Lean-conjunct hash. There are no omissions, duplicates, added obligations, changed rules, or reordered identities.

The obligations preserve the mathematics of the frozen rules:

- Four definedness equivalences expose the exact optional projection and exact sort predicate.
- Four guarded equalities relate the partial projection to the corresponding total projection.
- Three comparison equations preserve the Int, mixed-numeric, and string `>` behavior.
- One universal equality preserves concrete and opaque float maximum.
- Three universally guarded equations preserve sort disjointness.

The four definedness translations contain `∧ True` because the frozen right-hand side literally contains `#Ceil(@V)` and `@V : Val` is already a total generated Lean value. This is the exact translation of that source subterm, not an added free-standing conjunct or a weakening of the nontrivial equivalence. The sort-predicate side remains load-bearing, and adversarial Int/Bool/Float/Str witnesses confirm the guards and equivalences are satisfiable. No generated obligation is irrelevant or vacuously true as a whole.

The fixed target is:

- declaration: `Klean35MaxElement.Lemmas.targetStatement`
- file: `Klean35MaxElement/Lemmas.lean`
- definition SHA-256: `d278bfd415e4e5e8119d008f41e83c5fcbecad9d91a029c7d37edb0574ab8418`
- statement SHA-256: `ac69b69a6eb9f68af8cead6d01b6704e4547ab28f72e9c18b14394004aeba7f1`

Those values and all 27 ordered parameter bindings match the generator manifest, generated source, fresh `Base` copy, and `/audit-input.json`. Because the true domain set is nonempty, this correctly has a generated target and proof candidate; it is not a `KLEAN_NO_OBLIGATIONS` case.

## Stage 5 clean build, target identity, and trust accounting

I copied the candidate into `/tmp/audit-work/proof-audit-base`, verified its pre-`Base` export digest as `f670251ed12214561dd2cb800ac2bc7b4bae37991fc9bdfcfcf8ee6d9814c92c`, and copied the selected generated project into it as `Base`. I then ran literal `lake clean` followed by `lake build`. Both exited 0; the complete output ends with `Build completed successfully` in `evidence/08_fresh_lake_clean_build.log`. The trusted final gate independently repeated clean, build, and axiom audit and returned `PASS` in `evidence/13_final_gate.json`.

The candidate contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. It does not define or shadow `targetStatement`; its only two references are the exact theorem type and the proof's `unfold`. `Proof.final` has the exact fixed manifest statement with the same 27 parameters in the same order, not a duplicate or weakened proposition.

The exact Lean output is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`sorryAx` is absent. The three dependencies are Lean's trusted core axioms recognized by the trusted final gate. I reconciled them against the 57-entry generated/project `trust-inventory.json`: none of those 57 declarations is used by `Proof.final`, and there is no axiom outside the union of the recorded project inventory and the gate's three standard core axioms. The exact output is in `evidence/09_print_axioms.log`; the reconciliation is in `evidence/15_identity_and_trust.log`.

## Operational bridge audit

I located every exact candidate `def` for the 27 target parameters and compared it with its bound KORE symbol, all recorded `source_rule_ids`, the corresponding reconstructed `verification.k` rules, the source solution, and the supplied MPY operational semantics. The complete binding-by-binding matrix is `evidence/14_operational_bridge.log`.

The implementations are operationally faithful:

| Parameter group | Count | Independent judgment |
|---|---:|---|
| Boolean conjunction/disjunction and `>Int` | 3 | Lean Bool operations and mathematical strict Int order match K hooks. |
| `applyCmp` and `codesOf` | 2 | Constructor dispatch matches the represented MPY comparison table; strings unwrap their exact code sequence. |
| Four sort tests | 4 | They recognize only a singleton `K` sequence containing the exact corresponding injected sort. |
| `isNumericV`, `numericView`, `numericGt` | 3 | Exact Int/Bool/Float union, disjoint tagged view, and exhaustive frozen mixed-order table. Mixed Int/Float comparisons use exact binary64 dyadics rather than lossy Int-to-Float conversion. |
| `maxFOpaque` and `maxFloat` | 2 | Both implement K `FLOAT.max`: max-number NaN behavior, positive zero on signed-zero ties, and the numerically greater ordinary operand. |
| Direct, total, and optional projections | 12 | Exact constructor payloads on the source guards; optional projections reject other sorts. Defaults outside a partial operation's guard are not used to fake an obligation. |
| `strLt` | 1 | Strict lexicographic ordering of integer code-point sequences, including prefix cases. |

I compiled an independent Lean adversarial suite covering asymmetric booleans and integers, same/different sort projections, all numeric tags, numeric/non-numeric separation, exact ordering at `9007199254740993` versus binary64 `9007199254740992`, lexicographic prefix and differing-code cases, dynamic numeric and string dispatch, ordinary float maximum, one-sided NaNs, and both signed-zero orders. It also proves concrete separating witnesses against counterfactual constant comparison/predicate definitions, hard-coded projection and numeric-view definitions, a constant string comparator, and an identity float maximum. The passing compiler transcript is `evidence/12_adversarial_lean_pass.log`.

For the subtle float bridge, I did not trust the candidate comment. I compiled a new minimal K definition importing `FLOAT` and ground-ran `maxFloat` on NaN in each operand position, both signed-zero orders, both ordinary operand orders, and infinities. K returned the non-NaN operand, positive zero, and the numerical maximum, exactly matching the candidate. Raw K outputs are in `evidence/10_k_float_oracle.log`.

No target parameter is constant, identity, hard-coded, vacuous, or otherwise chosen merely to make the equations easy. The clean proof and axiom list therefore have a valid operational bridge to the frozen semantics.

## Evidence and environment note

`evidence/INDEX.md` identifies the definitive raw logs and helper sources. The container's PID namespace omitted `/proc/<pid>/exe`, which prevents the pinned Lean launcher from locating itself. I preserved the failed environmental retries and used a narrow `readlink` shim that only supplies the already pinned Lean 4.22 executable path for `/proc/*/exe`; it cannot alter candidate or provenance file reads. The trusted final gate was then run as its normal CLI under that environment and independently passed.

VERDICT: PASS
LEGITIMACY: LEGIT
