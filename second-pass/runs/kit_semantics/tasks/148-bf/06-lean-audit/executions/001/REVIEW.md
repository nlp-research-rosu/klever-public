# Independent audit: HumanEval `148-bf`

## Scope and result

This audit covers condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, and the protected Stage 3 classification plus deterministic Stage 4 generation. Both `AUDIT_MODE` and the signed `/audit-input.json` resolution record `CLASSIFICATION_ONLY`. The resolution has no Lean workspace or invocation, `stage5_result` is null, `/candidate` is absent, and the generated target is null. Stage 5 proof and operational-bridge checks are therefore inapplicable rather than omitted.

The Stage 3 classification is correct: all 17 rules in the local verification-module closure are definitions, and the true domain-lemma set is empty. Stage 4 consequently has zero obligations and correctly selected `KLEAN_NO_OBLIGATIONS` without generating a target or permitting a Stage 5 candidate.

## Input and producer integrity

I independently verified the signed resolution digest `c3790a7c5378993c14585ed21a137eff2869f0685ca36397009f7192924b91fc`. Every resolution hash recomputed exactly, including the Stage 1 workspace and export digests, protected discovery manifest, selected Stage 2 audit tree, selected Stage 4 tree, generated-project tree, and producer-source tree. The exact set of 789 Stage 1 regular files matched the 789 recorded `stage1_source_hashes`; there were zero path or digest mismatches. The full per-file comparison is in `evidence/02-resolution-and-hashes.log`.

Before evaluating Stage 4, I authenticated the producer sources:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Those values match both `source-manifest.json` and `generator-manifest.json`. The producer bundle contains exactly those two files and the source manifest. Its tree digest is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, matching `/audit-input.json`. The immutable image ID `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` agrees between the source manifest, generator provenance, and the image-key component of the producer path recorded in `/audit-input.json`. There is no producer-provenance infrastructure error.

## Inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification`, I reconstructed the local closure selected by the final `kompile verification.k --main-module VERIFICATION` command. The closure is exactly `[VERIFICATION]`; imported `MPY` is supplied semantics outside the local `verification.k` module set. The frozen `verification.k` digest is `c72e7edc950e084dce76d0776a3a7492d6a9c42f8d4f37cf14c0d71aec2094d1`.

For every reconstructed rule, I separately sliced the frozen source by the returned line span, normalized whitespace, recomputed SHA-256, checked that `source_rule_id` was exactly `rule-<normalized-sha256>`, and recomputed the canonical whole-inventory hash. All checks passed. The inventory hash is `16428e5ee7ce644b84ef8ad08e4e7f58213de2531a5bd36080bafebea24f7093`.

The complete ordered inventory is below. In each row, the exact `source_rule_id` is `rule-` followed by the displayed SHA-256.

| Lines | LHS/role | Normalized SHA-256 | Independent class |
|---:|---|---|---|
| 10–51 | `bfBody`, exact statement-term macro | `0629da93c5130935249ecfa4991c65d2afaaca2b33ec20afc6a779f158c11014` | `DEFINITION` |
| 54–55 | `bfModule`, exact module-term macro | `6bd0b985697081bba61414fe0cb7e6c71e74e938dc9839ce970e8282328ed6df` | `DEFINITION` |
| 58–59 | `bfCall`, call-term macro | `88469b06cedfdd9bc9231dd866cbabd952ef4e833651c4773ab66caa83e829fd` | `DEFINITION` |
| 63–71 | `planetValues`, ordered summary constant | `253ec3e1f18c2bc078c0f545ec4ee0507f3f8493dc5d2c771d4a7096479972a1` | `DEFINITION` |
| 75 | `planetIndex`, Mercury case | `d4d0231b5462732c3739470808deffd92ea65132f2d1e22a1deb0340bdeeda2a` | `DEFINITION` |
| 76 | `planetIndex`, Venus case | `f80de9aa06decd6bf81bb377f5d9813000f9934c5041e937854b54379878f17a` | `DEFINITION` |
| 77 | `planetIndex`, Earth case | `7d64656d0e9a2d8638d8ddeee422525493b0df124fa33af6675cdc1589e86d16` | `DEFINITION` |
| 78 | `planetIndex`, Mars case | `20063a48d0ce7c4fca27c55ce3bd0de9313e08a91d5a83a73bd7e52b3fc9e34f` | `DEFINITION` |
| 79 | `planetIndex`, Jupiter case | `9e6e1b44998e2655a8d678d46a5ac15f05d33edf216d6417b34cf22d392cae11` | `DEFINITION` |
| 80 | `planetIndex`, Saturn case | `fd00b5adacd219da87aa3198c0f0895954e5c2229e61df8955be7075a3546793` | `DEFINITION` |
| 81 | `planetIndex`, Uranus case | `a279c5182ae22abd95fe6899c923efd8ad22ed1067732ea4012676d0c38468dc` | `DEFINITION` |
| 82 | `planetIndex`, Neptune case | `e77a5a10c75b003145436d2cb697a7e7e287641d64a7179db37ee9777952f116` | `DEFINITION` |
| 83–91 | `planetIndex`, complementary invalid case | `290d758deb5a5561de5e1f4148346bf51bd3c2111c41c76d51b16bb9663544cc` | `DEFINITION` |
| 94–95 | `betweenPlanets`, compositional summary | `1a835c691e935312edfe3366c97d6d9795ef6ff7fe1dcaef8cd29d19aa671055` | `DEFINITION` |
| 98–99 | `betweenIndices`, invalid-index case | `fe571a7c3d64be70ffb927f16913ddad122595eb7855000f80017f252084e278` | `DEFINITION` |
| 100–101 | `betweenIndices`, ascending case | `9ae27cb61f454e0908af4cc42b45951e6c3db3484cc719d90cb03a6060954a89` | `DEFINITION` |
| 102–103 | `betweenIndices`, reverse/equal case | `5ab9c9b4681879c29b57a9fd17bce1e4d1f0a6cc0bc6eedce445b2755fee843c` | `DEFINITION` |

The 17 protected manifest identities are unique and occur in exactly this order. There are no omissions, duplicates, extras, reordered identities, or changed hashes. The trusted Stage 3 contract validation also succeeds. Raw spans, text, hashes, IDs, attributes, classifications, and order comparisons are preserved in `evidence/03-rule-inventory-reconstruction.log`.

## Independent classification judgment

The first three rules are structural macros over fresh symbols. `bfBody` is the exact MPY statement term represented by the frozen source: it constructs the eight-planet tuple, rejects either invalid name, computes both tuple indices, and slices strictly between them. `bfModule` only packages that body in the `bf` function definition; `bfCall` only names the ordinary call term. They do not bypass the fixed call, binding, body, return, heap, or control rules.

The remaining 14 rules define the mathematical result summary used on the claim's right-hand side:

- `planetValues` names the same ordered eight-string sequence as the program literal.
- The nine `planetIndex` equations form a disjoint and exhaustive definition over `IntSeq`: eight distinct ASCII name encodings map to indices 0–7, and the conjunction of their negations maps every other sequence to `-1`.
- `betweenPlanets` composes the two named summaries.
- The three `betweenIndices` guards are disjoint and exhaustive: a negative input produces the empty sequence; otherwise `I < J` selects `I+1 .. J-1`, and `I >= J` selects `J+1 .. I-1`.

This matches the supplied operational semantics. Tuple literals evaluate elements into `tuple(ValSeq)`; tuple membership folds over equality; `tuple.index` returns the first matching zero-based index; and tuple slicing lowers to `buildVS` with positive unit step. Equal or adjacent indices make the `buildVS` start no smaller than its stop and therefore return `.ValSeq`. Reversed inputs still use the smaller endpoint first, so output remains ordered by proximity to the sun. Invalid strings return before `index` is invoked and correspond to the `-1` summary branch.

Every LHS is a fresh verification symbol rather than an existing mathematical or operational symbol, and none of these rules rewrites an executing `<k>` configuration. They define macros, constants, or total summary functions; they do not assert a fact about the source result. Consequently none is an `OPERATIONAL_RULE` or a `DOMAIN_LEMMA`. No rule is claimed as `PROVED_DERIVED_LEMMA`, and there is no earlier proof-without-the-rule/later-use pattern to assess. The inventory reports no rule-level `simplification` attribute; in any event every equation with a definitional simplification role is classified `DEFINITION`, satisfying the simplification restriction.

As an independent adequacy check, I parsed—without executing—the frozen `solution.py` AST and verified the exact tuple, invalid guard, index calls, comparison, and both slice bounds. An independent direct operational oracle and a separately implemented summary model agreed on all 121 pairs drawn from the eight valid names plus `"Pluto"`, the empty string, and a non-ASCII near-name. Endpoint-inclusion, reverse-order, and invalid-nonempty counterfactual mutations each produced a concrete mismatch. This finite check supports, but does not replace, the structural semantics argument. Full cases and mutation witnesses are in `evidence/07-classification-semantics.log`.

The independent classification counts are therefore:

| Class | Count |
|---|---:|
| `DEFINITION` | 17 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

## Deterministic Stage 4 audit

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required Stage 1 workspace, protected discovery manifest, selected Stage 4 generation, and trusted toolchain lock.

The first invocation reached its clean-build step but the installed Lean/Lake binaries could not discover their installation because this audit sandbox exposes `/proc/self/exe` while hiding `/proc/<sandbox-pid>/exe`. The exact failure is preserved in `evidence/04-check-generation.log`, and the namespace observation is in `evidence/04c-proc-namespace-diagnostic.log`. I used the narrow source-preserved shim in `evidence/proc_exe_readlink_shim.c`; it changes only numeric `/proc/<pid>/exe` `readlink` calls to `/proc/self/exe`. It does not alter Lean input, declarations, elaboration, or build outputs. With that environment correction, `lean --version` reported Lean 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock.

The exact `check_generation` rerun succeeded with:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean` exit 0 and empty-output SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build` exit 0 and output SHA-256 `a1cb16f66317e96b07ff2c9a71563f37763f546d029ffb8a07100ddba29ceb07`;
- Stage 1 export digest `479973a3da247f87af7baa384498f51e8f463d0c1956c4b5a91bcf870865405a`;
- protected discovery digest `82c19ac4ce5ba0aaa4fa0b389dcf5b8da1f605e9463b2ec4f349401a57dafa71`;
- generated tree digest `8bf24d530fcae1f2c487a94b200ce654a040ab062413dc58f512cce164eb54b3`;
- obligation count 0 and target null.

The successful returned evidence is in `evidence/05-check-generation-rerun.log`. Its diagnostics and hashes exactly reproduce the immutable recorded preflight.

I also checked the Stage 4 mapping independently of that aggregate result. The independently classified domain IDs, `input-manifest.json` source rules, `obligation-map.json` source rules, generated obligation IDs, and trust parameters are all exactly the empty list. All recorded obligation counts are zero. The obligation-map SHA-256 is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, matching the generator manifest. The trusted target constructor returns no expected definition, the generated-project target parser finds no target declaration, and the generator manifest, preflight, and `/audit-input.json` all record target null. Thus there is no omission, duplicate, weakened or irrelevant obligation, target change, or vacuous conjunct. `KLEAN_NO_OBLIGATIONS` is justified by a genuinely empty independently classified domain set.

The generated library contains generic executable trust declarations recorded by its trust inventory, but there is no generated proposition or proof that can depend on them in this mode. The generated `Lemmas` namespace is empty. No Stage 5 candidate exists, so no `Proof.final`, axiom printout, target-parameter definition, or operational bridge is present to audit.

## Evidence index

- `evidence/01-producer-authentication.log`: raw producer and manifest hashes.
- `evidence/02-resolution-and-hashes.log`: signed-input validation, every resolution tree/file hash, and all 789 Stage 1 file comparisons.
- `evidence/03-rule-inventory-reconstruction.log`: canonical inventory, full rules, recomputed spans/hashes/IDs, whole hash, and exact Stage 3 order/bijection.
- `evidence/04-check-generation.log`: preserved initial host-environment failure.
- `evidence/04a-toolchain-shim-build.log`, `evidence/04b-lean-version-with-shim.log`, and `evidence/04c-proc-namespace-diagnostic.log`: environment correction and pinned-toolchain evidence.
- `evidence/05-check-generation-rerun.log`: successful mandated checker result and build diagnostics.
- `evidence/06-stage4-independent-checks.log`: independent source-rule/obligation bijection and target-absence checks.
- `evidence/07-classification-semantics.log`: source AST, semantic cases, and counterfactual mutations.
- `evidence/08-verification-source.log`, `evidence/09-source-program.log`, and `evidence/10-operational-semantics-rules.log`: frozen source and relevant supplied-semantics excerpts.

VERDICT: PASS
LEGITIMACY: LEGIT
