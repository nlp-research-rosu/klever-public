# Independent audit: HumanEval `69-search`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Result

The protected Stage 3 classification is complete and mathematically sound; Stage 4 deterministically generated exactly the five genuine domain-lemma obligations; and the Stage 5 candidate cleanly proves the fixed generated target using definitions that implement the relevant frozen K operations. I found no omitted rule, altered identity, weakened obligation, target substitution, or unrecorded trust escape.

## Producer provenance and frozen inputs

I hashed the two mounted generation-time producer files before judging Stage 4:

| Producer | Recomputed SHA-256 | Recorded SHA-256 | Result |
|---|---|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` | same in `source-manifest.json` and `generator-manifest.json` | match |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` | same in `source-manifest.json` and `generator-manifest.json` | match |

The immutable generator image is `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6` in both manifests. The producer path recorded in `/audit-input.json` contains that same image ID. The recomputed producer-source tree hash, using the launcher's tree-hash routine, is `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`, exactly the audit-input value. Producer provenance therefore satisfies the infrastructure prerequisite.

I also independently recomputed the recorded mounted-input hashes. The material values are:

| Input | Recomputed SHA-256 |
|---|---|
| Stage 1 K workspace | `372d5daa71162672c515447beff002f64d6314237e078d812ebfce398bd13ea6` |
| Stage 1 KLean export | `4943f93a498f152acb581e8dbaeed1dc6d55218f5b49f9e209af0f694eff17be` |
| Stage 2 K audit | `91f16559f165f73640adf9207ca8f000f680bcdba5b4263cd8d1359a03d9343f` |
| Stage 3 discovery manifest | `c472512716753a27b3984ba44a79df7f1f3c8cce4648982289a516e6c0c86966` |
| Stage 4 generation record | `bcdf7000833168306c16e079d7488f28fa7fc50d4ead90fb53545735716ce447` |
| Generated Lean tree | `5e9ca0c8083d76c100e9b600c6665227c690fd36fe690fc9e902d382e12cda75` |
| Stage 5 candidate | `441d75fbf9f2dfa62b620395180797056a2a484eaf01f9a3676488ee90d236fc` |

The exact Stage 1 export file map contains 777 files, with no missing, extra, or changed entry. Raw reconstruction and hash results are in `evidence/01_provenance_inventory.log` and `evidence/07_hash_target_bijection.log`.

## Independent rule-inventory reconstruction

I ran the trusted inventory implementation on the frozen `/reference/k-proof/verification.k`, rather than accepting the discovery manifest's list. It resolved the local verification-module closure to the single module `VERIFICATION`, reconstructed 23 rules, and recomputed for every rule its source span, normalized text hash, and `source_rule_id`.

The reconstructed facts are:

- frozen `verification.k` SHA-256: `626219d18cafb1fc6a9814a9f1e1afe6ec8af271b9d81ea1520a172e647991e7`;
- reconstructed inventory SHA-256: `1066209b71a607b520f502ba2fce41fc9fb386169ed80067c8bcb7576819bf34`;
- 23 reconstructed rules and 23 unique IDs;
- exact equality with the discovery manifest's spans, normalized hashes, texts, attributes, and ordered identities; and
- no omitted, extra, duplicated, or reordered rule.

Because each identity is `rule-<normalized-source-sha256>`, the full IDs below also state the independently recomputed normalized hashes.

## Independent Stage 3 classification

I re-read the frozen program, postcondition, `verification.k`, and the supplied operational semantics for values, operators, integer hooks, `applyBin`, and `applyCmp`. My classification of every inventory entry is:

| Frozen span | `source_rule_id` | Independent class | Reason |
|---|---|---|---|
| 11 | `rule-7b914623e87adc21e1f7f7260b77edc796f6180ade6a808ee402acef4564700d` | `DEFINITION` | Base case of the fresh `isIntVal` refinement predicate. |
| 12 | `rule-228c996e5270dd5c7b497c4cd214b34a58b8f6af7451d40d646feae80d465df7` | `DEFINITION` | `owise` case completing that predicate. |
| 15 | `rule-0f153294a059a4be56819068654eeea6e8629709074090b7ed4bc7c43018940e` | `DEFINITION` | Fresh named definedness predicate for the integer projection. |
| 20–22 | `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | `DOMAIN_LEMMA` | Characterizes definedness of the pre-existing partial `Val`-to-`Int` projection; it does not define a fresh left-hand symbol. |
| 24–26 | `rule-ced5adecb9e0d364813f64698375904533f4eeac50b93f2799465c7b5fead6d0` | `DEFINITION` | Guarded defining equation for the named totalized projection. |
| 28–30 | `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d` | `DEFINITION` | Guarded reverse normalization for that same named proof term. |
| 32 | `rule-7191d5f6c9756673cca00b440958222ca4d2d1d3d4e18cbc994313a0f4340442` | `DEFINITION` | Integer case of the totalized projection. |
| 33–34 | `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081` | `DEFINITION` | Idempotent normalization of the named totalized projection. |
| 39–42 | `rule-884f162b67149e88e7eecc28af46f50766a05e73cff70c9f7e167c33b1409e7d` | `DOMAIN_LEMMA` | Guarded integer instance of the pre-existing dynamic `==` dispatcher. |
| 44–47 | `rule-ffcf407de56764af73a323c60852665b87709ae760e0a275c8dacf75d96c5f02` | `DOMAIN_LEMMA` | Guarded integer instance of the pre-existing dynamic `>=` dispatcher. |
| 49–52 | `rule-3e1ce8e4b12d8d2bae33238dc22c1575ab618c72afa918828d490765e79c8c2c` | `DOMAIN_LEMMA` | Guarded integer instance of the pre-existing dynamic `>` dispatcher. |
| 54–57 | `rule-45c3bb147f4e28b3f60623a84ce2306b2a8b697607e4388f59b32c4585d29c66` | `DOMAIN_LEMMA` | Guarded integer instance of the pre-existing dynamic `+` dispatcher. |
| 61 | `rule-332de7605ea6aa1e510f40ded7182caba877f3081adf123c12192f6f51e58863` | `DEFINITION` | Base case of the input predicate `allPositive`. |
| 62–65 | `rule-d4697e4de1265f8357a8f3e6e099da645350fcf1ef2256f358deffb71a354ac0` | `DEFINITION` | Recursive case of `allPositive`. |
| 69 | `rule-395ea16548730c384c026e47fa3dec6cf06e488b4a8a34c66782f318805afab5` | `DEFINITION` | Base case of the frequency summary. |
| 70–73 | `rule-410bea703e13706f033c96ab0c848ade099dde8e98dee5ea6398fad33fff6b99` | `DEFINITION` | Integer recursive case of the frequency summary. |
| 74–76 | `rule-28291fde99a489e77fa659deeba905803f39ac1eabc6cfb5fc421ebda74c1858` | `DEFINITION` | Non-integer recursive case of the frequency summary. |
| 80–81 | `rule-e77a36e066e404542fa09b93ebe9987de9c23b5a4b093ad17b1c82af50bc634c` | `DEFINITION` | First guarded equation of the answer-update summary. |
| 82–83 | `rule-1fc0a2ec5c7608811a87f8397a63cabecde9e019e73082aa7cd99bbe2e38268a` | `DEFINITION` | Second guarded equation of the answer-update summary. |
| 84–85 | `rule-c9deb4d3603aea75cbc0d6dab13c35d28cfa9d10a58cc18270fc6a2e6869d0d2` | `DEFINITION` | Third guarded equation of the answer-update summary. |
| 89 | `rule-c122a567a37b33d7551a55edd058942613663f9ae9939508283ce965ef9237e7` | `DEFINITION` | Base case of the recursive search summary. |
| 90–101 | `rule-5158063d217eeb7d559392d234b56450f4e73c3774ecb1e8659bf96f89004c79` | `DEFINITION` | Integer recursive case of the search summary. |
| 102–107 | `rule-67ee2ef2c5f62b8c3c948d64947c4385c2340adc5c35f99d32d20f5a0e4a35fc` | `DEFINITION` | Non-integer recursive case of the search summary. |

This gives 18 `DEFINITION` and 5 `DOMAIN_LEMMA` entries, exactly as Stage 3 records. There is no `OPERATIONAL_RULE` in this verification-module closure: the ordinary operational rules are in the supplied semantics imported by it. There is also no `PROVED_DERIVED_LEMMA`: all five domain rules are already present in the verification module used to prove the later specification claims, and no earlier proof establishes any exact rule against a module from which that rule was removed.

All rules carrying a `simplification` attribute are in one of the two permitted classes: definitional normalization of `projectIntTotal`, or the five domain lemmas. The domain set is not empty. Each member is relevant: the source solution's loop uses `==`, `+`, `>=`, and `>`, while projection definedness connects symbolic `Val` inputs to those integer operations. The supplied K rules implement the same integer hooks underneath `applyBin` and `applyCmp`.

## Stage 4 generation and mathematical obligations

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and locked toolchain. It returned `status: PASS`, `obligation_count: 5`, zero designated sorries, and successful generated-project `lake clean`/`lake build` diagnostics. The returned evidence is preserved verbatim in `evidence/02_check_generation_retry.log`.

I then independently reconstructed the domain-rule/obligation map. The ordered source side and obligation side both contain exactly these five unique IDs:

1. `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` — projection definedness;
2. `rule-884f162b67149e88e7eecc28af46f50766a05e73cff70c9f7e167c33b1409e7d` — integer `==` dispatch;
3. `rule-ffcf407de56764af73a323c60852665b87709ae760e0a275c8dacf75d96c5f02` — integer `>=` dispatch;
4. `rule-3e1ce8e4b12d8d2bae33238dc22c1575ab618c72afa918828d490765e79c8c2c` — integer `>` dispatch; and
5. `rule-45c3bb147f4e28b3f60623a84ce2306b2a8b697607e4388f59b32c4585d29c66` — integer `+` dispatch.

For every pair, the frozen span, normalized source hash, classification entry, attributes, source text, generated Lean conjunct hash, and source-rule binding agree. The recomputed obligation-map hash is `478d3cf7d8543cd6a0e6bd833bbfe9b57d165fc70aec5eac04e8c7ae7ce8095d`.

Mathematically, the four dispatcher obligations retain the source guards that both operands are integer values and demand the exact hooked equality, order, or addition result. The projection obligation states that the singleton K-sequence integer projection succeeds exactly when the value is recognized as an integer. Its generated `∧ True` is the translation of `#Ceil(@V)` where `@V` is already a `SortVal`; it does not replace the substantive equivalence or create a separate vacuous obligation. I found no irrelevant, weakened, omitted, duplicated, or contradictory conjunct.

The independently regenerated target equals the mounted declaration byte-for-byte and has:

- declaration: `Klean69Search.Lemmas.targetStatement`;
- file: `Klean69Search/Lemmas.lean`;
- definition SHA-256: `41c68a20a7b72edbebde6180033852958ce073aa81dbd4849116efb1a190080b`;
- applied-statement SHA-256: `9e5acf6c4d631e565f38de8237e3cb6c11803e97f5bb387721b78a57fee5868c`; and
- exactly 11 parameter bindings.

Those values equal `generator-manifest.json`, `/audit-input.json`, the preflight result, and the independently extracted/generated text. `KLEAN_NO_OBLIGATIONS` is not the selected status and would not have been legitimate here because the true domain set contains five rules.

## Stage 5 clean build, target identity, and source audit

I created a fresh project at `/tmp/audit-work/69-search-proof-audit`, copied the candidate into it, and copied the fixed generated project into its `Base` directory. The copied Base tree retained the exact generated-tree hash. In that fresh directory:

- `lake clean` exited 0 (`evidence/03_lake_clean.log`);
- `lake build` exited 0 and ended with `Build completed successfully` (`evidence/04_lake_build.log`); and
- the trusted end-to-end final gate independently repeated the clean build and returned `status: PASS` (`evidence/11_klean_final_gate.log`).

The only build diagnostics were generated-file linter warnings for unused variables. The candidate neither edits nor shadows `Klean69Search.Lemmas.targetStatement`. The source gate found exactly one definition for each of the 11 required parameter bindings, found the exact required type on `Proof.final`, and found no `sorry`, `admit`, `unsafe`, new `axiom`, new `opaque`, or target-shadowing declaration. Thus `Proof.final` proves the fixed target rather than a duplicate or weakened variant.

## Operational bridge audit

I located and read every target parameter's exact candidate definition and compared it against its `kore_symbol`, bound source-rule IDs, frozen verification rules, source solution, and supplied operational semantics.

| Target parameter group | Independent judgment |
|---|---|
| `_andBool_` | Boolean conjunction, including its full truth table; exact K `andBool`. |
| `_>Int_`, `_>=Int_`, `_==Int_`, `_+Int_` | Lean integer comparison/equality/addition on the generated integer sort; exact K hooked integer operations, including negative and boundary values. |
| `isIntVal`, `definedProjectInt` | Return true exactly for the integer injection and false for all other `SortVal` constructors; exact frozen predicate meaning. |
| `projectIntTotal` | Returns the injected integer unchanged on the complete guarded domain used by all four dispatcher rules. Its value outside that guard is an unobserved totalization: frozen K supplies no evaluator/result there, and no obligation relies on it. |
| `project:Int?` | Succeeds exactly on a singleton K sequence containing an integer-injected value; rejects a Boolean and a sequence with an extra continuation. This matches the frozen sort projection used by the definedness lemma. |
| `applyBin` | On the complete relevant rule domain—operator `+` and two integer values—dispatches to exact integer addition and reinjects the integer result as `Val`. |
| `applyCmp` | On the complete relevant rule domains—operators `==`, `>=`, or `>` and two integer values—dispatches to the corresponding exact Boolean comparison. |

The candidate gives broader total definitions for dispatchers, but the proof does not use a convenient default in place of any frozen result: every source-rule guard/operator combination above is handled by an exact matching branch. The source program uses precisely those combinations.

The executable adversarial suite (`evidence/08_adversarial_parameters.lean` and its successful retry log) exercised all 11 bindings. It checked, among other cases, `14 + (-19) = -5`, true and false comparison boundaries, negative integer projection, rejection of Boolean projection, rejection of an extra K continuation, and both successful and failing dynamic comparison cases. The counterfactual suite (`evidence/09_counterfactual_mutations.lean`) constructed constant-false Boolean hooks, identity addition, left-returning binary dispatch, constant-false comparison/definedness predicates, zero projection, and an always-failing optional projection; each differs from the candidate on a satisfiable relevant witness. These checks corroborate the structural comparison: the bridge is not constant, identity-based, hard-coded to the theorem, or vacuous.

## Axiom and trust accounting

Running Lean directly with `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice]
```

The exact command output is in `evidence/05_print_axioms.log`. Both dependencies are permitted Lean core principles in the trusted inventory. `Proof.final` depends on none of the 42 generated allowlisted declarations, introduces no candidate axiom or opaque declaration, and does not depend on `sorryAx`. The independent reconciliation in `evidence/10_axiom_and_source_reconcile.log` reports no unexpected axiom.

The trusted final gate labels semantic classification `NOT_EVALUATED`; I treated that gate only as mechanical evidence. The classification, obligation relevance, and operational-bridge conclusions above are my independent semantic judgments.

## Evidence index and environment note

- `evidence/01_provenance_inventory.py` / `.log`: producer hashes, full reconstructed rule text/spans/hashes, inventory bijection.
- `evidence/02_check_generation.py` / `_retry.log`: trusted preflight invocation and returned evidence.
- `evidence/03_lake_clean.log`, `04_lake_build.log`: complete fresh-copy clean/build transcripts.
- `evidence/05_print_axioms.lean` / `.log`: direct `#print axioms Proof.final` run.
- `evidence/07_hash_target_bijection.py` / `.log`: all mounted hashes, exact rule/obligation bijection, target reconstruction and candidate target gate.
- `evidence/08_adversarial_parameters.lean` / `_retry.log`: operational examples for every binding.
- `evidence/09_counterfactual_mutations.lean` / `.log`: counterfactual bad-definition witnesses.
- `evidence/10_axiom_and_source_reconcile.py` / `.log`: forbidden-source and trust-inventory reconciliation.
- `evidence/11_klean_final_gate.log`: trusted end-to-end mechanical gate.

The first preflight attempt (`evidence/02_check_generation.log`) exposed an audit-sandbox PID-namespace issue: the pinned Lean runtime could not resolve `/proc/<inner-pid>/exe`. For reproducibility, I compiled the small audit-only `getpid` shim whose complete source is `evidence/outerpid.c`; it maps the process to the visible outer `/proc` PID and does not alter candidate, generated, source, or Lean files. With the unmodified pinned Lean executable, both required clean builds, direct axiom query, adversarial checks, preflight, and final gate then completed successfully.

VERDICT: PASS
LEGITIMACY: LEGIT
