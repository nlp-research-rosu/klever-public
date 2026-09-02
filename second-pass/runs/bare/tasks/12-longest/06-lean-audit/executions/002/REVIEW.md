# Independent Stage 3/4 Audit — HumanEval `12-longest`

## Scope and result

The launcher selected `CLASSIFICATION_ONLY` for condition `bare` and semantics
mode `GENERATED_SEMANTICS`. There is therefore no Stage 5 candidate to audit.
`/candidate` is absent, the signed resolution has `stage5_result: null`, and
all target fields are null.

I independently reconstructed and classified the rules in the local
verification-module closure, checked the Stage 3 manifest bijectively, reran
the trusted Stage 4 preflight, and independently checked the empty obligation
map and absent target. The Stage 3 classification is correct: 13 definitions,
5 operational rules, no proved derived lemma, and no domain lemma. Consequently
`KLEAN_NO_OBLIGATIONS` is the correct Stage 4 result.

## Frozen inputs and provenance

The signed audit-input envelope validates with resolved-input digest
`4d8b8e7343299eb8443869f5424522ba4be9f3c63b9a7623eefdf30c91bd918d`.
The launcher mode agrees with `AUDIT_MODE=CLASSIFICATION_ONLY`.

All material hashes that bind mounted inputs recomputed exactly:

| Object | Recomputed SHA-256 | Result |
|---|---|---|
| Mechanical-checker lock | `9cd22493bf7a2445bebb5c81b74bbe427a73a98d5c2a547db8b5c69b697ad56a` | matches audit input |
| Stage 1 workspace, pipeline tree hash | `f1616457f244f34f7285e6eecb970faf76c4cf75771844c2ae5ea814be098477` | matches audit input |
| Stage 1 deterministic-export tree | `5d3faa1a08c461fb4cca52e79b1ad7f41fe97e52b47b168058c034b075e9aef1` | matches audit input and Stage 4 manifests |
| `verification.k` | `ff40adf397cc707c4b5426c16572837e23a14834b93aafbbc134c51c45402bd5` | matches audit input and input manifest |
| Stage 3 discovery manifest | `d4be6d49dbe337b1abcdbf53e0d00d2494a7372008351466566552b3772b223d` | matches audit input and Stage 4 manifests |
| Selected Stage 2 artifact | `1023b7f35d11be83de048f36909bdf2dc65f4d0fddf663d9e9e9e4e722cf728b` | matches audit input |
| Selected Stage 4 artifact | `054b86725325d035f3dc39a1ec388880efb474d8651e20b275747afc179ebbdf` | matches audit input |
| Generated project tree | `a85c18ade04d80d50c836c27c215b6c58199dd2b4f14fae76d127c279b8cdb20` | matches audit input, generator manifest, export result, and preflight |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` | matches generator manifest |
| Trust inventory | `030e2e8e9b34e98d92afabf766db253bf5b67546e58de1baaffe7f4afe73e4fb` | matches export result |

Every entry in `stage1_source_hashes`, including `semantic.k`, `spec.k`,
`solution.py`, `solution.mpy`, `prove.sh`, and `verification.k`, also matches.
Every file named by the mechanical-checker lock matches its locked digest. The
generator manifest's toolchain object exactly equals
`/reference/klean-toolchain.lock.json`.

The `klean_py_sha256` and `exporter_sha256` fields in the generator manifest
identify the historical generator-image sources; those historical source files
are not mounted. They are preserved inside the selected Stage 4 artifact hash
and were not substituted for the separately locked current audit tools.

Evidence:

- `evidence/12_hash_reconstruction.txt`
- `evidence/15_checker_lock_verification.txt`
- `evidence/16_remaining_resolution_hashes.txt`
- `evidence/21_manifest_hash_crosschecks.txt`

## Inventory reconstruction and bijection

I invoked the locked
`tools.k_rule_inventory.inventory_verification(Path("/reference/k-proof"))`.
`prove.sh` selects `VERIFICATION` as the main module. Within
`verification.k`, the local import closure contains only `VERIFICATION`;
`MPY-SEMANTICS` is defined in the separately required `semantic.k`, so its
rules are operational context but are not members of this local inventory.

The trusted scanner found 18 rules in source order. For each rule it removed
comments only as specified by the scanner, collapsed whitespace for the
normalized text, computed the normalized SHA-256, and assigned
`source_rule_id = "rule-" + normalized_sha256`. The canonical JSON hash of the
ordered rule documents is:

`abf9ccdcfd0a77de4c492e722b24752b8311ffec102ba6cf608a1e6708bf4541`

The protected Stage 3 manifest has exactly 18 entries and 18 unique IDs. Its ID
sequence exactly equals the reconstructed source sequence. Thus there is no
omission, duplicate, extra entry, reorder, span change, normalized-hash change,
or unaccounted classification.

The full reconstructed record, including exact rule text and attributes, is in
`evidence/reconstructed-inventory.json`. The source with physical line numbers
is in `evidence/19_numbered_verification_source.txt`.

## Independent rule classification

In the table below, each source ID is `rule-<normalized SHA-256>`.

| Lines | Normalized SHA-256 | Classification | Independent judgment |
|---|---|---|---|
| 9–14 | `db9420e8fd1c4626595b79b7ea2e6307a53b03fc99d9a63570388395764ad474` | `DEFINITION` | Expands the named `longestLoopBody` macro to the exact translated loop body. |
| 17–27 | `79576cfe9c9b959c7fa701acac35d9e135e225f3fdeb54b5effd615e4a16a951` | `DEFINITION` | Expands the named `longestProgram` macro to the translated source AST. |
| 33 | `cf8b57d453a6eeb1d815ece37d5946c5fead470f5c67daf85939a3638bd36896` | `DEFINITION` | Defines the `stringList` conversion wrapper. |
| 34 | `7f473637b44742359337a6ea4b8811bbced9fc57f43365394878fa092f0337db` | `DEFINITION` | Base equation for the `stringValues` conversion. |
| 35–36 | `0eb9fd5516c5c09a4385fa1fb3ce068e72e602071ec62aa60e1aca23a6648342` | `DEFINITION` | Structurally recursive `stringValues` equation. |
| 43 | `d522a0d2a80d77bf23fff3789a4c9cc1dee3902e31f1443c813bc6cbc8bd5e20` | `DEFINITION` | Empty case of the named contract summary `expectedLongest`. |
| 44–45 | `0632983b57909c5400dca4ed74248b5d09a3914a9a277a31c21c50ec82e29e7f` | `DEFINITION` | Nonempty case of `expectedLongest`, seeding its fold with the head. |
| 47 | `bb0ed98a5e6ea08b1f41e028d4ab4f62da3a797dbe6f3b3a6b0fb0b0be94ec3b` | `DEFINITION` | Base case of the `firstLongest` recurrence. |
| 48–50 | `e2ea59e583e9aba4f56686bbb8c31703b58b4e536d869f118bf4f3f066a4c42b` | `DEFINITION` | Strictly-longer branch of `firstLongest`. |
| 51–53 | `41608496e24b276d61c515e55ec432cae88d14f9e1bdb34b9983811ac7afe643` | `DEFINITION` | Retain-current branch of `firstLongest`, including equal-length ties. |
| 60–61 | `b0f0333a8289ed42bf63f5f68911b09e710cd5d1f3945ffceead604fd31c6755` | `OPERATIONAL_RULE` | Runtime `isEmpty` observation for a zero-length `seqVal`. |
| 62–63 | `e69efc7581406d022b7856deb7b0903c7ce4f89a28c7ba8668b210fa8eeb1f44` | `OPERATIONAL_RULE` | Runtime `isEmpty` observation for a positive-length `seqVal`. |
| 64–65 | `b1717a1cb9f20abb2c92ed3d8bb9f5dfc66a3f417779b528e3fcddc52cf5e014` | `OPERATIONAL_RULE` | Runtime `head` observation for a nonempty `seqVal`. |
| 67–68 | `f224022b33a01068dbf84152f03ad2c24f192cea0b778266eb7958ce3e3c07ca` | `OPERATIONAL_RULE` | Terminates `forValues` execution when no symbolic elements remain. |
| 69–74 | `6217bfa50b953d6505f0f15ac2a66ceb8481b6397d4eea8a5ca19a91b3cef5da` | `OPERATIONAL_RULE` | Executes one loop body, updates the bound loop variable, increments the index, and decrements the remaining count. |
| 78–79 | `e4633a59660c5ec7ead77cb473c04e9f0d1cdbe206f021fdb481ce4081ba04f7` | `DEFINITION` | Base case of the named loop-summary recurrence `firstInSeq`. |
| 80–83 | `64119d60105d2cb544dd81225851d868a9c84ab75c122076ae4a088d7f4cf1ab` | `DEFINITION` | Strictly-longer branch of `firstInSeq`. |
| 84–87 | `2c6384deca5d2eff6d3d334e4b29720ab4673a16bc8a4f57ad4341881f7e6cc3` | `DEFINITION` | Retain-current branch of `firstInSeq`, including ties. |

This yields:

- `DEFINITION`: 13
- `OPERATIONAL_RULE`: 5
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The definitions meet the required definition test: they are macros, conversion
functions, contract summaries, or recursive fold equations. The five `seqVal`
rules act on the execution functions `isEmpty`, `head`, and `forValues`; the
last two also manipulate the live `<k>` and `<env>` cells. They are ordinary
observations/execution transitions, not algebraic facts used to simplify a
domain proposition.

The strict `>` branch and complementary `<=` branch agree with the Python
source's first-maximum tie behavior. Counterfactually replacing `>` with `>=`
would select a later equal-length string, so the current recurrences and loop
macro are sensitive to the source contract. For `N > 0`, the `seqVal` step
exposes `stringAt(ID,I)`, advances to `I+1`, and decreases `N`; for `N = 0`,
iteration stops. These guards are disjoint and match the operational role used
by the three symbolic claims in `spec.k`.

There is no claimed derived lemma whose prior proof would need checking. There
is also no `simplification` attribute on any inventory entry, so the
simplification-category restriction is satisfied. The declaration of
`stringAt` as a total function is not a rule and therefore is not an omitted
inventory entry.

This classification does not by itself certify a universal connection between
the proof-only `seqVal` representation and ordinary `listVal` inputs; that is a
Stage 1/2 soundness and adequacy question. It does not turn any of the five
execution rules into a domain lemma, and Stage 4 correctly does not present
them as mathematical Lean obligations.

Evidence:

- `evidence/02_reconstructed_inventory.txt`
- `evidence/17_inventory_bijection_and_class_counts.txt`
- `evidence/20_operational_context.txt`

## Deterministic Stage 4 generation

I ran the required trusted function with `PYTHONPATH=/reference` and the exact
three mounted inputs:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
)
```

The sandbox initially made Lean's `/proc/<getpid>/exe` lookup fail even though
`/proc/self/exe` was available. I recorded that failed attempt, then used a
narrow preload shim under `/tmp/audit-work` that redirects only this
self-executable lookup. It does not alter the checker or any mounted input.
Lean then identified the pinned version and commit, and the exact trusted
preflight returned:

- status: `KLEAN_NO_OBLIGATIONS`
- Stage 1/export hash:
  `5d3faa1a08c461fb4cca52e79b1ad7f41fe97e52b47b168058c034b075e9aef1`
- Stage 3 manifest hash:
  `d4be6d49dbe337b1abcdbf53e0d00d2494a7372008351466566552b3772b223d`
- generated tree hash:
  `a85c18ade04d80d50c836c27c215b6c58199dd2b4f14fae76d127c279b8cdb20`
- obligation count: 0
- target: null
- trust declarations: 49
- designated sorries: 0
- `lake clean`: exit 0, empty-output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output hash
  `f0bb4bb311ba839e514aa3f2cd269d5b84d65f9292e617992e53cfb029d6bcb8`

The successful returned document is byte-for-value equal to the stored
preflight facts in the signed audit input.

Evidence:

- `evidence/06_check_generation.txt` — initial environment failure
- `evidence/13_lean_proc_shim_validation.txt` — pinned Lean identity and clean build
- `evidence/14_check_generation_success.txt` — exact successful returned evidence

## Obligation bijection and fixed target

My independent classification has an empty ordered domain-rule ID list. This
matches all generation layers exactly:

- `input-manifest.json` `source_rules`: `[]`
- `obligation-map.json` `source_rules`: `[]`
- `obligation-map.json` `obligations`: `[]`
- `obligation-map.json` `trust_parameters`: `[]`
- generator obligation count: 0
- export-result obligation count: 0

Thus the source-rule/obligation relation is the exact empty bijection. There
can be no omitted, duplicated, reordered, irrelevant, weakened, or vacuous
conjunct because there is no true domain lemma and no generated conjunct.

The expected target definition computed from the obligation map is null.
`tools.klean_export.target_statement` independently returns null. The generator
manifest, stored preflight, signed audit resolution, and top-level signed target
all record null. `Klean12Longest/Lemmas.lean` contains imports, a namespace, and
no declaration. No generated target exists and there is no Stage 5 proof
candidate, exactly as required for a genuine `KLEAN_NO_OBLIGATIONS` result.

Evidence:

- `evidence/04_stage4_manifests.txt`
- `evidence/05_generated_sources.txt`
- `evidence/18_obligation_and_target_identity.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
