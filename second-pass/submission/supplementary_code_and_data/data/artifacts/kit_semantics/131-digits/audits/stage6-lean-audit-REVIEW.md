# Independent audit: HumanEval 131-digits

## Scope and outcome

I audited condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, in launcher mode `CLASSIFICATION_AND_PROOF`. I treated
the Stage 1 workspace, Stage 2 review, protected Stage 3 manifest, Stage 4
artifacts, and Stage 5 candidate as evidence only. I did not adopt the prior
review's verdict or classification.

The result is PASS. The canonical Stage 1 inventory and protected Stage 3
manifest are bijective, the six definitions and four domain lemmas are
correctly classified, Stage 4 deterministically emits exactly the four
relevant algebraic obligations, and the Stage 5 candidate proves the fixed
target using operationally faithful integer definitions.

Material commands and their output locations are indexed in
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

## Producer provenance and immutable input hashes

I hashed the producer sources before judging Stage 4:

| Artifact | Recomputed SHA-256 |
|---|---|
| `generation-tools/klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `generation-tools/klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |
| producer-source tree | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` |

The individual hashes match `generator-manifest.json` and
`source-manifest.json`. The immutable generator image is
`sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`
in both manifests and in the basename of the producer-source path recorded by
`/audit-input.json`. Evidence:
[`01_producer_hashes_and_manifests.txt`](evidence/01_producer_hashes_and_manifests.txt)
and
[`05_independent_recorded_hash_checks.txt`](evidence/05_independent_recorded_hash_checks.txt).

Independent digest checks also matched:

| Bound input | Recomputed and expected digest |
|---|---|
| full Stage 1 workspace | `9be6e10de85757799aad54bc9b53dc8255c3443ebfd058b94ed5ce76e51e85e2` |
| Stage 1 export digest | `03f6eda51ddc047159f1482a543a41b2a5fd6773634e97938525882cd01f50f5` |
| Stage 2 audit tree | `e4024fa77e1b37f7d39d44ac796fb307d5750b4a448aa795f22ae587278552a1` |
| Stage 3 manifest | `2255dd105c0ddd37ccd59aa62155d6d20d4c03e29e040454fb72e98896dcae02` |
| Stage 4 generation tree | `12af2343b3648d734fc6b0101dae061f3434a3b4563fc0a5133c2c679483d4d2` |
| generated Lean tree | `53b47905ad531bdfd672d59469a8c401412f78b1d99f0ac24f59d0b16da41ef2` |
| Stage 5 candidate tree | `08b31b956562bc6c580ab6cc0a027c160c90b5fa540af5a8d3e1e6bffda324cc` |

All 773 Stage 1 per-file source hashes recorded in the launcher input match;
there are no missing, mismatched, or unrecorded files.

## Canonical rule inventory and Stage 3 bijection

Using the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`, I reconstructed the local closure of the selected
`VERIFICATION` main module:

- verification source hash:
  `ce8bebe32fe76c976b365b4d864c3ddd2a30aab82136055b0901a8e1b30b7272`;
- local closure, in source order:
  `VERIFICATION-SYNTAX`, `VERIFICATION`;
- rule count: 10;
- canonical inventory hash:
  `0a1d759c28623d9c6b243594fed4806c09dcfb862b9aac752f052cfe8f180f0d`.

The full reconstructed records, including source text, lines, normalized
hashes, attributes, and IDs, are in
[`06_reconstructed_inventory.json`](evidence/06_reconstructed_inventory.json).
Every `source_rule_id` is exactly `rule-` plus its independently recomputed
normalized source hash.

The protected manifest has exactly the same ten unique IDs in exactly the same
order. Its inventory hash matches, and it has no omission, duplicate, extra
entry, reordered identity, or unknown hash. The trusted Stage 3 contract also
accepts it. Evidence:
[`08_discovery_bijection_pass.txt`](evidence/08_discovery_bijection_pass.txt).

## Independent classification

My classification of every inventory entry agrees with Stage 3:

| Lines | Source rule | Judgment |
|---|---|---|
| 19–20 | `oddDigitsProduct(N) => 1` for `N <=Int 0` | `DEFINITION`: empty-product base equation |
| 21–25 | odd-positive `oddDigitsProduct` recurrence | `DEFINITION`: multiply the decimal last digit and recurse on the prefix |
| 26–29 | even-positive `oddDigitsProduct` recurrence | `DEFINITION`: discard the even last digit and recurse |
| 31–32 | `oddDigitSeen(N) => 0` for `N <=Int 0` | `DEFINITION`: no-odd-digit base equation |
| 33–35 | odd-positive `oddDigitSeen(N) => 1` | `DEFINITION`: current odd digit establishes presence |
| 36–39 | even-positive `oddDigitSeen` recurrence | `DEFINITION`: recurse on the decimal prefix |
| 43 | `1 *Int X => X` | `DOMAIN_LEMMA`: integer left identity |
| 44 | `X *Int 1 => X` | `DOMAIN_LEMMA`: integer right identity |
| 45 | `X +Int 1 -Int X => 1` | `DOMAIN_LEMMA`: integer cancellation |
| 46 | `(X *Int Y) *Int Z => X *Int (Y *Int Z)` | `DOMAIN_LEMMA`: integer multiplication associativity |

The summary equations are genuine named recurrences. For positive `N`, the
supplied `pyMod` and `//` rules remove one decimal digit; parity of a positive
integer equals parity of its last decimal digit, so the guarded odd/even cases
match the source loop. The recurrences cover the positive cases and decrease
to the nonpositive base.

All four simplification rules are universally true over K `Int` and are
material to the proof:

- left and right identity normalize the initial/terminal product;
- associativity aligns the accumulated product with the remaining-digit
  summary;
- cancellation normalizes the `found` bit expression
  `F + 1 - (F * 1)`.

None is an operational execution rule. None was proved as an exact earlier
claim in a rule-free module: Stage 1 compiles `verification.k` containing all
four before its only positive `kprove` run. Therefore none qualifies as
`PROVED_DERIVED_LEMMA`. There are no `OPERATIONAL_RULE` or
`PROVED_DERIVED_LEMMA` entries, and every `[simplification]` entry is correctly
a `DOMAIN_LEMMA`. The frozen program, spec, integer semantics, and Stage 1
proof order are recorded in
[`09_frozen_program_spec_rules_semantics.txt`](evidence/09_frozen_program_spec_rules_semantics.txt)
and
[`59_stage1_proof_order_and_claims.txt`](evidence/59_stage1_proof_order_and_claims.txt).

## Stage 4 generation and fixed target

The selected export status is `OK`, not `KLEAN_NO_OBLIGATIONS`. This is
correct because the independently classified domain set contains four rules.

I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three specified mounted inputs. The audit sandbox initially blocked Lean
4.22's numeric `/proc/<pid>/exe` lookup, causing Lake configuration discovery
to fail. I diagnosed this exact syscall path and used a local preload shim that
only maps `/proc/<digits>/exe` to the equivalent `/proc/self/exe`. Its source,
hash, compilation, and successful pinned Lean version check are in
[`35_lean_sandbox_shim_build_and_test.txt`](evidence/35_lean_sandbox_shim_build_and_test.txt).
It does not alter Lean source, elaboration, kernel checking, or arithmetic.

With that sandbox compatibility shim, the same trusted function returned
`PASS`, clean-built the generated project, reported four obligations, zero
sorries, 46 inventoried trust declarations, and the expected hashes. The
returned object is
[`36_check_generation_returned.json`](evidence/36_check_generation_returned.json).

The ordered obligation bijection is:

1. `1 *Int X => X` ↔
   `∀ X : SortInt, «_*Int_» 1 X = X`;
2. `X *Int 1 => X` ↔
   `∀ X : SortInt, «_*Int_» X 1 = X`;
3. `X +Int 1 -Int X => 1` ↔
   `∀ X : SortInt, «_-Int_» («_+Int_» X 1) X = 1`;
4. multiplication associativity ↔ the same universally quantified
   associativity equation over `SortInt`.

For every entry, the source ID, source span, normalized hash, inventory hash,
discovery hash, and recomputed Lean-conjunct hash match. The input-manifest
source records, obligation-map source records, and independently enriched
domain records are identical in order. There are four unique source IDs and
four unique conjunct hashes, with no omitted, duplicate, irrelevant, weakened,
or extra obligation. `SortInt` is definitionally `Int`, so its quantified
domain is inhabited; none of the equations is a vacuous conjunct.

Evidence is in
[`42_independent_stage4_bijection_and_target.txt`](evidence/42_independent_stage4_bijection_and_target.txt)
and
[`43_corrected_stage4_source_record_comparison.txt`](evidence/43_corrected_stage4_source_record_comparison.txt).
The former's diagnostic `input_source_rules_exact False` compares enriched
Stage 4 records to bare Stage 3 records; the corrected comparison adds the two
required provenance fields and is entirely true.

The obligation-map file hash is
`c7c3d31f76d5ab91f7c24d7fb6f021e7cbfaea236dc6d4213136622301c1fbd8`;
the trust-inventory file hash is
`5bc54fb48fffbcfa5b9a8a34effde7ae57ddf9536057f8c6adc5968b354f54fa`.
Both match their recording manifests.

The only generated target is
`Klean131Digits.Lemmas.targetStatement`, in
`Klean131Digits/Lemmas.lean`. Its recomputed hashes are:

- definition:
  `2a07d0fac7f668610bacd4dbff0abbf3d131040204b17bd05e72bb352b1d65a8`;
- instantiated statement:
  `0233ab7714d3db69a8f0b44a527d6ce7999812e397827e915f00fbb427969ecf`.

The declaration, file, exact statement, parameter bindings, and both hashes
match the generator manifest, returned preflight, and `/audit-input.json`.

## Stage 5 clean build, target identity, and trust

I made a fresh project at `/tmp/audit-work/stage5-project`, copied the
candidate into it, and copied the immutable generated project into `Base`.
I then ran both required commands:

```text
lake clean    exit 0
lake build    exit 0, Build completed successfully.
```

Complete outputs are
[`45_stage5_lake_clean.txt`](evidence/45_stage5_lake_clean.txt) and
[`46_stage5_lake_build.txt`](evidence/46_stage5_lake_build.txt).
After the build, the `Base` tree digest remains exactly
`53b47905ad531bdfd672d59469a8c401412f78b1d99f0ac24f59d0b16da41ef2`.
The copied candidate source files are byte-identical to `/candidate`.

There is exactly one `targetStatement` declaration in the fresh tree, and it
is the immutable declaration under `Base`. The candidate neither changes nor
shadows it. `Proof.lean` has exactly one theorem named `final`; its normalized
type is exactly the manifest statement, and Lean accepts an explicit
type-ascription of `Proof.final` to that target. There is no weakened,
duplicated, or alternate theorem.

After removing comments for token scanning, the candidate source has no
`sorry`, `admit`, `unsafe`, `axiom`, or `opaque` code token. Trusted declaration
extraction finds no candidate axiom or opaque declaration. The word “opaque”
appears only in an explanatory comment, not as Lean code. Evidence:
[`47_stage5_identity_and_static_trust_scan.txt`](evidence/47_stage5_identity_and_static_trust_scan.txt)
and
[`57_proof_statement_and_axiom_reconciliation.txt`](evidence/57_proof_statement_and_axiom_reconciliation.txt).

The exact requested Lean output is:

```text
'Proof.final' depends on axioms: [propext]
```

It is preserved without log framing in
[`58_print_axioms_exact_output.txt`](evidence/58_print_axioms_exact_output.txt).
`propext` is one of the trusted mechanical gate's three foundational Lean
allowances (`Classical.choice`, `propext`, `Quot.sound`). `Proof.final` uses
none of the 46 generated allowlisted declarations. There is no `sorryAx` and
the set of unrecorded dependencies is empty.

## Operational-bridge audit

The frozen compiled K definition identifies the three target KORE symbols as
total integer hooks:

| Target parameter | Frozen KORE hook | Candidate definition |
|---|---|---|
| `«_-Int_»` | `Lbl'Unds'-Int'Unds'`, `INT.sub` | `fun x y => x - y` |
| `«_+Int_»` | `Lbl'UndsPlus'Int'Unds'`, `INT.add` | `fun x y => x + y` |
| `«_*Int_»` | `Lbl'UndsStar'Int'Unds'`, `INT.mul` | `fun x y => x * y` |

The supplied MPY operational rules map Python `+`, `-`, and `*` on integers
directly to those K hooks. The generated Prelude defines `SortInt := Int` and
defines the corresponding generated operations as `some (x + y)`,
`some (x - y)`, and `some (x * y)`. Thus the total parameters are exactly the
payload meanings of the frozen total hooks.

The bindings to source rules are exact:

- subtraction and addition are bound to
  `rule-b09bdfe5e2bc74b215bed27c498fc03e78a4929071d23d07a626110c519fed02`;
- multiplication is bound to
  `rule-082958cd68b6ff48e923703bfbdc398fbdc293247656d1a01d3339fbcf725de4`,
  `rule-2ab4c7bc73ad01bbe3db34c2b3cc0d6c95c87c850e1e3f40e6891b9a061c05a7`,
  and
  `rule-6c033d38e2e8c948160d245d94624fb6c578d69ea99fc1c15c896b557eaa1ee3`.

Lean checked universal definitional connections between every candidate
function and both the corresponding Lean integer operation and generated
`Option` wrapper. All six checks close by `rfl`; see
[`56_universal_operational_bridge_checks.txt`](evidence/56_universal_operational_bridge_checks.txt).
The exact K hook declarations, MPY dispatch rules, generated definitions, and
candidate definitions are juxtaposed in
[`60_operational_symbol_bridge_sources.txt`](evidence/60_operational_symbol_bridge_sources.txt).

Adversarial values include negative results, mixed signs, zero, and large
unbounded integers. Representative outputs were:

```text
5 - 8 = -3
-7 - 4 = -11
-7 + 4 = -3
-7 * 4 = -28
0 * 99999999999999999999 = 0
-123456789 * -987654321 = 121932631112635269
```

They are recorded with the printed candidate definitions and exact proof type
in
[`51_proof_identity_and_adversarial_values.txt`](evidence/51_proof_identity_and_adversarial_values.txt).

As a counterfactual sensitivity test, I defined:

- constant subtraction `fakeSub _ _ := 1`;
- projection addition `fakeAdd x _ := x`;
- shifted-addition “multiplication” `fakeMul x y := x + y - 1`.

Lean proves that these convenient but operationally false functions also
satisfy the four generated equations, while concrete examples distinguish
them from the candidate (`1` versus `-3`, `-7` versus `-3`, and `-4` versus
`-28`). This demonstrates that clean theorem closure alone does not establish
the operational bridge. The successful counterfactual, with no `sorryAx`, is
in
[`55_counterfactual_convenient_bridge_pass.txt`](evidence/55_counterfactual_convenient_bridge_pass.txt).
Earlier evidence files 52–54 are retained failed draft attempts and are not
used as positive evidence.

The actual candidate is not one of these convenient models: its three exact
definitions are universally identical to the frozen `INT.sub`, `INT.add`, and
`INT.mul` meanings. Therefore the operational bridge passes despite the
target's intentional underdetermination.

## Final judgment

Stage 3 correctly separates definitional summaries from the four genuine,
relevant domain lemmas. Stage 4 preserves a complete ordered bijection and a
fixed non-vacuous target under verified producer provenance. Stage 5 cleanly
proves exactly that target, introduces no trust escape, and supplies faithful
total meanings for every KORE-bound parameter.

VERDICT: PASS
LEGITIMACY: LEGIT
