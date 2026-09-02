# Independent Stage 3–5 audit: HumanEval 130-tri

## Scope and result

This audit covers problem `130-tri`, condition `kit-semantics`, and semantics mode `SUPPLIED_SEMANTICS`. The launcher and `AUDIT_MODE` both say `CLASSIFICATION_ONLY`. The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; `/candidate` is absent. Consequently, Stage 5 proof construction, `Proof.final`, `#print axioms`, and operational-bridge parameter review are not applicable.

I did not rely on the selected Stage 2 verdict, the protected Stage 3 labels, or prior logs as judgments. I reconstructed the Stage 3 inventory with the trusted rule-inventory implementation, classified every reconstructed rule from the frozen K source and operational semantics, authenticated the exact Stage 4 producer sources, reran the trusted Stage 4 preflight, and independently checked the hashes, obligation bijection, and target identity.

The result is PASS/LEGIT. The independently reconstructed domain-lemma set is genuinely empty, so an empty obligation set, no generated target, and no Stage 5 candidate are the correct outputs.

## Frozen-input and producer authentication

The launcher-style tree digests and exporter-style tree digests were recomputed with the trusted implementations. Every recorded value matched:

| Input | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace, launcher tree algorithm | `ba471467f35010670b043f6e2b97cb67df27f6be72efcd93b623d1e16402c605` |
| Stage 1 export, exporter tree algorithm | `ae2e99dfc54c52aa5010961ba83e0bdf2af548bfd28a6b6d430bcd51204d0c5b` |
| Stage 2 selected audit tree | `0d62fa4c1281577c69e4f2823249b6082b386a090e2cc6530e84a0d3b5cb9f65` |
| Protected Stage 3 manifest file | `9e98c4a7aa5b5078482a664de560fc3866df4f2d5e6e16bdaf4d87ca6525c880` |
| Selected Stage 4 generation tree | `19b03fc808b786eb59aeacf641b7e1c24d0ad5c70402b486a91feb55443c278b` |
| Generated Lean project, exporter tree algorithm | `65a048af62b12b27abd9d94d80909edda5329d32b1613c44210fba43217d6515` |
| Generation producer-source tree | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` |

All 779 individual `stage1_source_hashes` in `/audit-input.json` were also recomputed: there were no missing, extra, or changed entries.

Before judging Stage 4, I hashed both mounted generation-time producer files:

| Producer | Observed hash | Result |
|---|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` | Matches `source-manifest.json` and `generator-manifest.json` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` | Matches `source-manifest.json` and `generator-manifest.json` |

The immutable generator image is consistently identified as `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc` by the source manifest, generator manifest, and the image-key component of the launcher-recorded producer-source path. The obligation-map file hash, frozen `verification.k` hash, and toolchain lock also matched their manifests. Evidence: `01-producer-and-manifest-hashes.log`, `02-manifests-and-launcher.log`, `18-launcher-style-tree-digests.log`, and `19-all-recorded-hash-verification.log`.

## Inventory reconstruction and bijection

The trusted `tools.k_rule_inventory.inventory_verification` selected `VERIFICATION` as the main module and reconstructed its local closure as `VERIFICATION-SYNTAX`, then `VERIFICATION`. It found exactly ten rules. It recomputed the frozen file hash as `f9ca701f8c9962b093e604f97fa130ef0d14cb1478bed0c96313e5aa7da85893` and the canonical whole-inventory hash as `d86e2617188d6ba4a76b8b0d18613904c9a2b3607d2af2956cac4ffc88f494f9`.

For every rule, the reported `source_rule_id` was exactly `rule-` followed by its recomputed normalized source hash. The reconstructed spans were `(13–14)`, `(17–31)`, `(34–38)`, `(41–42)`, `(51–52)`, `(53–56)`, `(57–59)`, `(64–65)`, `(66–71)`, and `(73–73)`. Rehashing the ordered canonical rule documents reproduced the whole-inventory hash.

The protected manifest contains exactly the same ten identities in the same order. Both identity lists are unique; there are no omissions, duplicates, extras, or reordered entries. The trusted `lemma_discovery_contract.validate_trust_boundary` also accepted all source spans, normalized hashes, identities, and classifications structurally. Evidence: `06-reconstructed-rule-inventory.log`, `07-stage3-bijection-validation.log`, `27-explicit-inventory-order-bijection.log`, and `28-source-id-and-inventory-hash-check.log`.

## Independent Stage 3 classification

I independently classify all ten rules as `DEFINITION`, agreeing with the protected manifest:

| Span and source-rule identity | Independent classification | Judgment |
|---|---|---|
| 13–14, `rule-3016862ec9f61c9f8e250b0f2b7bfb49c3be042189fa800969cb468d8436433e` | `DEFINITION` | `triLoopCondition` is a `[macro]` name for the exact `i <= n` AST. |
| 17–31, `rule-9f9771176866dbd5612151eba842e91827d249160c68380a843c6aef1508988c` | `DEFINITION` | `triLoopBody` is a `[macro]` name for the exact nested branch, append, and increment AST. |
| 34–38, `rule-f6885500f92955d6c73100a99413425dd4bb229d455cecb55bc5b5957d6a5009` | `DEFINITION` | `triFunctionBody` composes the exact initialization, loop, and return AST. |
| 41–42, `rule-9a61ae4856ca86244da25be7fff91c03fa54438494390be30ea850d2307ae715` | `DEFINITION` | `triDefinition` names the exact `tri(n)` function-definition AST. |
| 51–52, `rule-c4c4c3e5c9e80b377717622978dc67aff4c417b51927335af87970b773fd0588` | `DEFINITION` | This is the negative-index totalization equation for the named `triValue` summary; negative indices are outside the proved `N >= 0`, `I >= 0` execution domain. |
| 53–56, `rule-5a5bbd9741b0fac3ee8556335743164019d885260d97be6e705886321e30353f` | `DEFINITION` | This defines `triValue` on nonnegative odd indices by exactly the product computed by the source branch. |
| 57–59, `rule-ffc8510abe57a4241fd78ba80136c4f8f98f5f04c940923109fa48e78b15dd90` | `DEFINITION` | This defines `triValue` on nonnegative even indices by exactly `1 + i // 2`, including `i = 0`. |
| 64–65, `rule-c64282d33978054e893889af080d36475bf71e7dd522f6044c6888ceae6f0de2` | `DEFINITION` | This is the terminating base equation of the named `triComplete` sequence summary. |
| 66–71, `rule-503acfd8fb63e70b1dd9d242cfc57fab3e83dfb81eb352be0fec1c511cd7a37f` | `DEFINITION` | This is the recursive equation of `triComplete`: append the current `triValue`, increment `I`, and recur. |
| 73, `rule-a3d3f0cc205af87ab1b9b8415eeda1875352c75017b437d1ffa13cc85b1def54` | `DEFINITION` | `triResult` is a wrapper starting `triComplete` from the empty prefix and index zero. |

The four macro rules only define named syntax and do not execute or observe a program state. Their expansions match the frozen translated solution AST. The six remaining rules define three fresh proof-local summary functions; none rewrites an operational configuration or preempts fixed-semantics execution.

The operational K rules confirm the correspondence. Integer `%` reduces to `pyMod`; integer `//` reduces to `(i - pyMod(i,2)) / 2`; `append` updates the list in the heap; `While` evaluates its condition and iterates through `#while`; `If` selects on truthiness; and `AugAssign` updates `i` using the bound value. For nonnegative `i`, `pyMod(i,2)` is 0 or 1. Thus the `triValue` guards are disjoint and exhaustive. At 0 the even equation gives 1; at 1 the odd equation gives 3; at every later even or odd index its right-hand side is the source branch expression. The `triComplete` guards `I > N` and `I <= N` are disjoint and exhaustive, and the recursive branch strictly increases `I`.

An independent finite witness, which did not import or execute the frozen solution, compared the separately encoded operational branches against the summary equations for indices 0 through 1000 and found zero mismatches. It also compared complete results at bounds `-1, 0, 1, 2, 3, 4, 5, 20, 100`, again with zero mismatches. Counterfactual odd and even formula mutations were detected immediately. This is finite corroboration; the classification judgment rests on the exact equations and operational rules. Evidence: `05-frozen-source-and-spec.log`, `10-operational-semantics-trace.log`, `22-classification-witness.log`, and `classification_witness.py`.

No rule is an `OPERATIONAL_RULE`: none is an ordinary execution/observation rule over semantic state. No rule is a `PROVED_DERIVED_LEMMA`: Stage 1 does not first prove any of these exact rules in a module omitting it and later install it as a rule. No rule is a `DOMAIN_LEMMA`: each rule introduces or unfolds a named macro/summary rather than asserting a separate mathematical fact. The prompt-facing base, even, and odd-recurrence facts occur as claims in `spec.k`; they are not hidden simplification rules in the verification-module closure. The rule-level inventory contains no `simplification` attribute, and every function/macro evaluation equation is in the allowed `DEFINITION` category.

Therefore the independently classified true domain-lemma set is empty.

## Deterministic Stage 4 generation and target identity

Inspection of the authenticated generation-time producer shows that it exports only `validated["domain_lemmas"]` as source rules. It checks the ordered source-rule/obligation identity list, emits `targetStatement` only when the proposition list is nonempty, and rejects any target declaration when obligations are empty.

The selected output is exactly consistent with the independently empty domain set:

- `input-manifest.json` has `source_rules: []`.
- `obligation-map.json` has `source_rules: []`, `obligations: []`, and `trust_parameters: []`.
- `generator-manifest.json` records `obligation_count: 0` and `target: null`.
- The trusted `target_statement` parser returned `None`.
- `Klean130Tri/Lemmas.lean` contains only imports, a namespace, and its closing `end`; it has no `targetStatement` declaration.
- There are no omitted, duplicated, irrelevant, weakened, or vacuous conjuncts: there are no domain lemmas to translate and no generated target at all.

The obligation-map hash recomputed as `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, matching the generator manifest. Evidence: `17-obligations-target-and-trust.log`, `20-empty-bijection-and-target-check.log`, `25-producer-domain-target-path.log`, and `26-producer-obligation-emission-path.log`.

## Fresh trusted preflight

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage 4 generation, and pinned toolchain lock.

The first native attempt reached its isolated `lake clean` step but failed because the audit sandbox prevented Lean's runtime from resolving `/proc/<pid>/exe`; even native `lean --version` returned `error: failed to locate application`. I preserved that failure in `11-fresh-check-generation.log` and the toolchain diagnostic in `12-toolchain-diagnostic.log`.

To complete the mandated check without changing the checker, inputs, generated project, or toolchain, I used the recorded compatibility shim in `app_path_compat.c`. It only supplies the running executable name from the ELF `AT_EXECFN` auxiliary value when libc `readlink` is called on `/proc/self/exe` or `/proc/<pid>/exe`; all other `readlink` calls pass through unchanged. Native Lean failed before the shim and the pinned Lean then reported version 4.22.0, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, with it. The shim source and binary hashes and this before/after test are in `23-app-path-compatibility.log`.

Under that narrow environment compatibility, the trusted checker returned:

- status `KLEAN_NO_OBLIGATIONS`;
- frozen input and Stage 1 hash `ae2e99dfc54c52aa5010961ba83e0bdf2af548bfd28a6b6d430bcd51204d0c5b`;
- protected Stage 3 hash `9e98c4a7aa5b5078482a664de560fc3866df4f2d5e6e16bdaf4d87ca6525c880`;
- generated tree hash `65a048af62b12b27abd9d94d80909edda5329d32b1613c44210fba43217d6515`;
- obligation count 0 and target `null`;
- designated sorry count 0;
- `lake clean` exit 0;
- `lake build` exit 0 with `Build completed successfully.`

The fresh clean/build output hashes exactly reproduce the recorded Stage 4 preflight hashes. The checker also found the 43 generated non-propositional executable trust declarations exactly equal to `trust-inventory.json` and rejected proposition trust, proof holes, forbidden imports, and malformed target state. Because there is no theorem target, these generated executable declarations do not serve as a proof of any obligation. Full returned evidence is in `15-fresh-check-generation-with-app-path-compat.log`.

## Stage 5 disposition

`AUDIT_MODE` and `/audit-input.json` agree on `CLASSIFICATION_ONLY`; `/candidate` does not exist. Since the independently classified domain set is empty, Stage 4 correctly generated no target and Stage 5 must not exist. There is no `Proof.final` whose statement, axioms, forbidden constructs, or operational parameter definitions could be audited. This absence is the required state, not missing proof evidence.

## Evidence index

Raw command transcripts and results are under `/audit-output/evidence/`. The principal records are:

- `COMMANDS.md`: exact command index for the raw transcripts.
- `01-producer-and-manifest-hashes.log` and `19-all-recorded-hash-verification.log`: producer, source, artifact, and manifest hashes.
- `05-frozen-source-and-spec.log`, `06-reconstructed-rule-inventory.log`, and `28-source-id-and-inventory-hash-check.log`: frozen source, spans, normalized identities, and inventory hash.
- `07-stage3-bijection-validation.log` and `27-explicit-inventory-order-bijection.log`: structural and ordered Stage 3 bijection checks.
- `10-operational-semantics-trace.log` and `22-classification-witness.log`: operational correspondence and counterfactual witnesses.
- `15-fresh-check-generation-with-app-path-compat.log`: fresh trusted preflight return value.
- `20-empty-bijection-and-target-check.log`: exact empty source-rule/obligation bijection, null target, audit mode, and absent candidate.
- `25-producer-domain-target-path.log` and `26-producer-obligation-emission-path.log`: authenticated producer control paths relevant to domain selection and target emission.

VERDICT: PASS
LEGITIMACY: LEGIT
