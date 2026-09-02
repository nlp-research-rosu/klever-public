# Independent audit: HumanEval `85-add`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Result

The Stage 3 classification is complete and mathematically appropriate, the
Stage 4 generation is authenticated and bijective with the three genuine
domain lemmas, and the Stage 5 candidate proves the exact fixed target using
operationally faithful definitions. I found no legitimacy failure.

This conclusion does not rely on the prior Stage 2 PASS or any candidate
comment. All classifications and operational-bridge judgments below were
reconstructed from the frozen K source and supplied semantics.

## Input and producer authentication

The launcher mode in both `AUDIT_MODE` and `/audit-input.json` is
`CLASSIFICATION_AND_PROOF`. The trusted full binding gate reproduced all
launcher-recorded input hashes, including:

- Stage 1 export tree:
  `3e9e0258904ab465be2ac65f2e44f01adea14b4544ab5fde7eeb4ef76c03804b`
- Stage 3 manifest:
  `ac864263543109dab05b2a7af63cb86c3697512cb991a6626db778fcb5d48b7f`
- Stage 4 generated tree:
  `031534484043e45353edac0c462a99674971daa500591fe52ecace6c331db1b3`
- Stage 5 workspace:
  `225dced726df68bfbab55507bb2d9bc0303e150804c09631f9ca7a752dfa2dbe`
- Producer-source tree:
  `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`

Before judging Stage 4, I independently hashed both mounted producer files:

- `klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`

Those values agree exactly with `source-manifest.json` and
`generator-manifest.json`. The generator image ID is
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`
in both manifests, and the same ID is embedded in the producer-source path
recorded by `/audit-input.json`. The complete producer tree also matches the
launcher hash. Producer provenance is therefore authenticated; there is no
producer-source `AUDIT_ERROR`.

## Stage 1 inventory reconstruction and Stage 3 bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`. The selected main module is `VERIFICATION`, and its
local closure is ordered as `VERIFICATION-SYNTAX`, `VERIFICATION`. The
reconstruction found exactly 13 rules. It recomputed:

- `verification.k` SHA-256:
  `df8b02d899f4f7b350cc88539744b65e7823d6929ea160eb08ad559d95103e56`
- inventory SHA-256:
  `36b7269f531b8499a3ecc5033b85b9cbd19024d07da31b455cd99ab6ca61e21c`

The reconstructed and protected inventories have identical ordered
`source_rule_id` lists, both lists contain 13 unique IDs, and their set
differences are empty. Thus there are no omissions, extras, duplicate
identities, reordered identities, changed spans, or changed normalized hashes.
The trusted Stage 3 contract validation independently returned the same
result.

## Independent classification judgment

The 13 rules classify as follows:

| Lines | Rule | Classification | Independent judgment |
|---:|---|---|---|
| 23 | `allInts(.ValSeq)` | `DEFINITION` | Base equation of the named structural domain predicate. |
| 24–25 | `allInts(vCons(...))` | `DEFINITION` | Constructor recurrence of that predicate. |
| 27 | `definedProjectInt(V)` | `DEFINITION` | Defines a named guard as the supplied Int-sort predicate. |
| 30–32 | `#Ceil({V}:>Int)` | `DOMAIN_LEMMA` | A load-bearing, unproved characterization of the pre-existing partial projection; it does not define a new symbol. |
| 33–35 | `projectIntTotal(V) => {V}:>Int` | `DEFINITION` | Guarded defining equation for the new named proof term. |
| 36–38 | `{V}:>Int => projectIntTotal(V)` | `DEFINITION` | Guarded macro/canonical orientation into that named proof term. |
| 39 | `projectIntTotal(I) => I` | `DEFINITION` | Constructor case of the named proof term. |
| 40–41 | nested `projectIntTotal` collapse | `DEFINITION` | Canonicalization equation for the same named proof term; it is also redundant with the Int case, but is not a new mathematical assumption. |
| 45–48 | guarded `%` dispatch | `DOMAIN_LEMMA` | Extends the supplied Int dispatch to a symbolic `Val` under `isInt`; it is neither a new-symbol definition nor separately proved before use. |
| 49–52 | guarded `+` dispatch | `DOMAIN_LEMMA` | The analogous unproved symbolic-sort dispatch fact for addition. |
| 56 | empty `addSummary` | `DEFINITION` | Base equation of the postcondition summary. |
| 57–58 | even-index `addSummary` | `DEFINITION` | Structural recurrence that skips the even-indexed head. |
| 59–64 | odd-index `addSummary` | `DEFINITION` | Structural recurrence that conditionally adds an even head. |

There are no `OPERATIONAL_RULE` entries: the supplied operational rules remain
in the frozen semantics, while the two `applyBin` twins above are proof-local,
unproved symbolic-sort facts. There are no `PROVED_DERIVED_LEMMA` entries:
Stage 1 contains no earlier claim that proves any of these exact rules against
a module omitting it. All three domain rules are already installed when the
Stage 1 claims are proved.

The domain lemmas are relevant rather than decorative:

- the projection-definedness lemma supports the guarded symbolic Int cast;
- the `%` lemma corresponds directly to `value % 2` in the source condition;
- the `+` lemma corresponds directly to `result += value` in the source body.

Seven inventory rules carry `simplification` or `simplification(...)`. All
seven are classified as either `DEFINITION` or `DOMAIN_LEMMA`, as required.
The independently reconstructed true domain set is therefore exactly the
three protected Stage 3 entries.

## Stage 4 structural and mathematical audit

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against the frozen Stage 1 workspace, protected Stage 3 manifest, selected
Stage 4 generation, and pinned toolchain lock. After the launcher workaround
described below, it returned:

- status `PASS`;
- obligation count 3;
- generated tree hash
  `031534484043e45353edac0c462a99674971daa500591fe52ecace6c331db1b3`;
- zero designated sorries;
- a successful clean build of the generated project.

The obligation-map file hash is
`d4a593ca997a536daf0cf778e0e0c41105c522ea80c145dbe5411cf17d8b7471`.
Its three ordered obligations are in an exact one-to-one correspondence with
the three domain-rule IDs, including their source spans, normalized hashes,
inventory hash, and discovery-manifest hash. There are no duplicates or
omissions.

The mathematical translations are faithful:

1. The projection obligation states that the generated `project:Int?`
   succeeds exactly when `definedProjectInt V = true`. The source-side
   `#Ceil(V)` becomes `True` because `V` is already an inhabitant of the total
   generated `SortVal`; the remaining equivalence still distinguishes Int
   from every non-Int constructor and is not a vacuous theorem.
2. The `%` obligation is the exact guarded equality between `applyBin "%"`
   on an Int-valued `Val` and injected `pyMod (projectIntTotal V) I`.
3. The `+` obligation is the exact guarded equality between `applyBin "+"`
   on an Int accumulator and an Int-valued `Val`, and injected K integer
   addition after projection.

Under the audited operational meaning of `isInt`, both guarded obligations
have abundant satisfiable witnesses (for example any injected negative or
positive Int), so their guards are not vacuous. The equations are exactly the
ones needed by the frozen program and are neither weakened nor irrelevant.

The generated target is
`Klean85Add.Lemmas.targetStatement`. Recomputing it from
`obligation-map.json` gives:

- definition hash:
  `6dbed9467b37f676d6b7a214b6153271ca28a6ef81691549969e2e52de0c1b9e`
- applied-statement hash:
  `709b20d64b8a3eed81f08097b289ec0b8a92208cdc7ce1a3d1ce168d22119374`

The complete target object is identical in the generated source,
`generator-manifest.json`, and `/audit-input.json`.

## Stage 5 proof, identity, and trust

I copied the candidate into a fresh
`/tmp/audit-work/85-add-proof-audit` workspace and copied the immutable
generated project into it as `Base`. The copied `Base` tree has the exact
generated digest
`031534484043e45353edac0c462a99674971daa500591fe52ecace6c331db1b3`.

I then ran both required commands:

- `lake clean`: exit 0;
- `lake build`: exit 0, with only the generated target's unused-hypothesis
  linter warnings.

The candidate contains exactly one definition for each of the seven target
parameters and exactly one `theorem final`. It does not define or shadow
`Klean85Add.Lemmas.targetStatement`. Its theorem type is the exact fixed
manifest statement, not a copied or weakened variant. Independent scanning
and the trusted candidate gate found no `sorry`, `admit`, `unsafe`, new
`axiom`, or new `opaque` declaration outside immutable `Base`.

The exact Lean output requested by the audit is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice]
```

Both are Lean core axioms explicitly accepted by the trusted final-gate
policy. `sorryAx` is absent. None of the 42 allowlisted generated
collection/projection trust declarations is a dependency of `Proof.final`,
and there is no unrecorded proof escape. The trusted full mechanical gate,
including audit-input hash binding, returned `PASS`.

## Operational-bridge audit

Each generated parameter was checked against its KORE symbol, bound source
rule IDs, frozen `verification.k`, supplied semantics, and the actual source
program:

| Parameter | Candidate meaning | Judgment |
|---|---|---|
| `_+Int_` | Lean integer addition | Exact model of K `_+Int_`; negative and mixed-sign witnesses reduce correctly. |
| `applyBin` | Constructor dispatch with exact Int `%` and Int `+` branches | The two source-relevant branches match `semantics/int.k` and the guarded Stage 1 rules. It is not constant or hard-coded to the target result. |
| `definedProjectInt` | True exactly on `SortVal.inj_SortInt` | Exact model of `definedProjectInt(V) => isInt(V)` for the supplied `Val` constructors. |
| `isInt` | True exactly on a singleton K sequence containing an injected Int | Matches the generated/supplied Int sort predicate, including false results for Bool, non-Int values, and a nonempty trailing continuation. |
| `projectIntTotal` | Extracts an injected Int; returns 0 off-domain | Exact on the guarded domain used by both source rules. The off-domain totalization is not observed under `isInt` and does not replace a fixed off-domain K value. |
| `pyMod` | `((x tmod y) + y) tmod y`, with 0 at `y = 0` | Exact frozen `pyMod` recurrence whenever `%Int` is defined. The source divisor is the constant 2; the zero case merely totalizes the supplied partial hook consistently on both sides. |
| `project:Int?` | `some i` exactly for a singleton injected Int, otherwise `none` | Exact partial projection/definedness model. |

The independently compiled `BridgeAudit.lean` exercised all seven definitions,
including `-5 % 2 = 1`, `5 % -2 = -1`, mixed-sign addition, Int versus Bool,
and a K term with a trailing continuation. It also supplied witnesses that
constant mutations of addition, dispatch, definedness, projection,
`projectIntTotal`, and `pyMod` violate the target equations.

A deliberately false constant `isInt` can make the two guarded conjuncts
vacuous; I confirmed this counterfactual in Lean. That demonstrates why the
requested operational-bridge audit is necessary and why clean compilation
alone would be insufficient. It does not apply to this candidate: the actual
definition is the exact sort predicate, and injected Int witnesses make each
guard satisfiable.

## Reproducibility and launcher note

Raw outputs are under `/audit-output/evidence/`, and the exact command record
is in `evidence/COMMANDS.md`. The most important artifacts are:

- `03_reconstructed_rule_inventory.log`
- `04_stage3_bijection_validation.log`
- `11_rerun_klean_preflight_pass.log`
- `16_fresh_candidate_lake_build.log`
- `17_print_axioms_proof_final.log`
- `20_full_mechanical_input_binding_gate.log`
- `21_operational_bridge_adversarial_examples.log`
- `26_target_identity_and_exact_definition.log`

The first preflight invocation failed before elaboration because this audit
sandbox gives child processes an inner PID for which `/proc/<pid>/exe` does
not exist. Lean 4.22 uses that path to locate its installation. I reproduced
the mismatch and preserved the failure. A 28-line `LD_PRELOAD` shim redirects
only `/proc/<pid>/exe` reads to `/proc/self/exe`; its source and hash are in
the evidence directory. With that launcher-only workaround, the pinned Lean
version/commit matched the lock and all generated and candidate checks
completed. The shim changes executable path discovery only, not Lean
elaboration, kernel checking, imports, declarations, or proof terms.

VERDICT: PASS
LEGITIMACY: LEGIT
