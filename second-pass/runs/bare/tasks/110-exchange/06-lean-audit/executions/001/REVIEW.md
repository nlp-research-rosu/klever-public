# Independent Stage 3 / Stage 4 Audit: `110-exchange`

## Result and scope

The launcher records:

- condition: `bare`
- semantics mode: `GENERATED_SEMANTICS`
- audit mode: `CLASSIFICATION_ONLY`
- selected Stage 4 status: `KLEAN_NO_OBLIGATIONS`

I independently reconstructed and classified the Stage 1 rule inventory,
checked the Stage 3 manifest bijectively, verified the generation producer
provenance before judging Stage 4, reran the trusted Stage 4 preflight, and
independently checked the source-rule/obligation/target relationship.

The classification-only mode is correct. `/candidate` is absent, as required,
and there is no Stage 5 result or generated proof target to audit. I did not
rely on the selected Stage 2 verdict or any prior review.

## Frozen inputs and producer provenance

All hashes recorded in the signed resolution were independently recomputed
from the mounted inputs with the trusted hash implementations. They match:

- Stage 1 pipeline tree:
  `04bb1613d519ab57b1961080fe093a3beb1e213baea8f00744c80b649153d83e`
- Stage 1 export tree:
  `9a49aecaeece05fe3ea241df1f08949a341d6ddd2dbf80e4ad0a2e45b4aaef8b`
- Stage 3 manifest:
  `d95c59386f33947a3975de80e63804c5adf550cfbcad82f9f033e863249cc8da`
- selected Stage 2 tree:
  `961036a0f8ad8b519bdca2eeda2e745524908a50e444ecdbe0855fcff04133ac`
- selected Stage 4 tree:
  `7bbb469a996782c238caa03a6ae82269ec0d3f370746866051f467a91cfefc3a`
- producer-source tree:
  `7b7fdfe618031c11f79bb3d7eec7df24bc64a9a480fc470c1176ce36a593286a`
- generated project tree:
  `2fd779a4efd71d0e63e2877c0186009566f2940107d1849047b3da3d1d8253b0`

Every per-file Stage 1 source hash also matches `/audit-input.json`. The
selection hashes match the current Stage 2 and Stage 4 trees. The signed
resolution digest recomputes to
`66e8da1f7cda68afdc32a088f3a3468f7ed91b14743b16f1787ec29b9873217b`.

The required producer gate passes:

| Producer | Observed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` | same |
| `klean.py` | `5d419b1cf907ab880eeb88a68e0d6da0bf59a92a56a0803b34d53698d91caabe` | same |

Those values agree simultaneously with `source-manifest.json` and
`generator-manifest.json`. The source manifest and generator manifest both
record generator image
`sha256:15baeb15b1ea8266bfad3dbc3a75ee531cf429f1b73e0e3ff478f279e6308f63`;
the immutable producer-source path bound by `/audit-input.json` has the same
image digest as its final component. There is no producer-source
infrastructure error.

## Inventory reconstruction and bijection

I ran the trusted canonical inventory implementation on the frozen
`/reference/k-proof` workspace. `prove.sh` does not select a different
verification main module, so the unique local module is `VERIFICATION`.
Its local verification-module closure is exactly:

```text
["VERIFICATION"]
```

The reconstruction found eight rules. For every rule, the source slice at the
reported lines equals the inventory text, normalizing whitespace and hashing
the slice reproduces `normalized_sha256`, and `source_rule_id` is exactly
`rule-<normalized_sha256>`.

The canonical whole-inventory hash is:

```text
76c60c5d4bad411cf1086bae00f60ef87db52f0f9e6c79624a6c5b01245d8389
```

It matches the Stage 3 manifest and Stage 4 input manifest. The Stage 3 list
has exactly eight entries, all IDs are unique, its ID set is identical to the
canonical set, and its order is identical to canonical source order. Thus
there are no omissions, duplicates, extras, reordered identities, changed
spans, or changed hashes.

## Independent Stage 3 classification

The independent classifications are:

| Lines | Normalized hash | Rule role | Classification |
|---:|---|---|---|
| 7–10 | `3b0524b72be44f90dc539594c9435311735b97ca12e5744522207847efdf958f` | `countBody` expands a syntax symbol to the parity-counting statement body | `DEFINITION` |
| 13–22 | `79fb603017208f0260ce768393ce9fb05571d41100b73e0f56c39f20617e2d39` | `solutionProgram` expands a syntax symbol to the concrete translated program AST | `DEFINITION` |
| 25 | `88be6889f69f1872079523b2d7e52712728c0ade8da99f5cc8f1e208b15839ec` | even branch of the parity indicator | `DEFINITION` |
| 26 | `f261b5e7098649f4ee737cabca0e23ef363204ae35e929ff0aaeb927267eca1c` | complementary non-even branch of the parity indicator | `DEFINITION` |
| 29 | `0abfea958f5b272978425c2d6ebeb66d7f853b51b1cc98320b4d4f836eda2528` | empty-list base equation for `countEven` | `DEFINITION` |
| 30 | `e9f96e50aa51213c566f0e36b583257fd92bc4fb5a6a9ed4b83888d78d6b159f` | structurally decreasing recurrence for `countEven` | `DEFINITION` |
| 33 | `9b6c79e06a9018ca7b7a00e5e7de15c49eaa68710bdd4a950b891b2ee4e61050` | empty-list/default base equation for `lastValue` | `DEFINITION` |
| 34 | `00c9d163d151e306625b62553c8a82464be399ff77abca913944795d51bc75af` | structurally decreasing recurrence for `lastValue` | `DEFINITION` |

This agrees with all eight Stage 3 classifications.

The first two are macro definitions: their declared syntax symbols carry the
`[macro]` attribute, and their rules expose the exact statement body and
translated source program used by the operational semantics. They do not
assert mathematical consequences or skip a running configuration.

The `evenBit` pair defines the characteristic value of divisibility by two.
Its guards are a Boolean predicate and its negation, so they are exhaustive
and disjoint. `countEven` is a constructor-complete recursion on `PyList` and
decreases to the tail; it therefore defines the number of even elements.
`lastValue` is another constructor-complete tail recursion, returning the
provided default on `Nil` and the final list element otherwise. These are
summary definitions used by the loop and final-state claims, not algebraic
domain facts.

No inventory rule matches or advances a live K configuration, so none is an
`OPERATIONAL_RULE`. No inventory rule is presented as a consequence proved
first in an earlier bridge-free proof, so none is a
`PROVED_DERIVED_LEMMA`. Most importantly, none states an additional
mathematical fact about the helpers: the true `DOMAIN_LEMMA` set is empty.

All eight inventory rules have an empty rule-attribute list. In particular,
there is no `[simplification]` rule to reclassify, so the requirement that
every simplification rule be a definition or domain lemma is satisfied.

The classification is also faithful to the program and postcondition. The
source counts even values in both lists and returns `YES` precisely when that
count is at least the length of `lst1`. That criterion is exactly the
exchange feasibility condition: after unrestricted exchanges, `lst1` can be
all even iff the union of both lists supplies at least `len(lst1)` even
values. `countEven` and `evenBit` name this computation; `lastValue` accounts
for the operationally visible loop variable in the complete K final state.
No relevant mathematical theorem has been hidden under a definitional label.

## Stage 4 preflight and structural integrity

I reran exactly `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference` and these inputs:

```text
frozen input:       /reference/k-proof
discovery manifest: /reference/lemma-discovery.json
generation:         /reference/klean-generation
toolchain lock:     /reference/klean-toolchain.lock.json
```

The first attempt exposed a launcher-environment issue before any project
check: Lean 4.22 looks up `/proc/<getpid()>/exe`, while this audit sandbox
only exposes the equivalent `/proc/self/exe`. This made `lake clean` report
that it could not detect its installation. I diagnosed that mismatch and used
a local preload shim under `/tmp/audit-work` that redirects only that
executable-path lookup to `/proc/self/exe`. The shim does not alter or shadow
any mounted input, generated source, manifest, or theorem. With the real
pinned toolchain binaries first on `PATH`, both `lean --version` and a
separate clean test build succeeded.

I then reran the unchanged trusted checker. Its complete command output is in
`evidence/10_preflight_rerun_success.log`. The result was:

```text
lake clean: exit 0, empty output
lake build: exit 0
  Built Klean110Exchange.Prelude
  Built Klean110Exchange.Sorts
  Built Klean110Exchange.Inj
  Built Klean110Exchange.Lemmas
  Built Klean110Exchange.Func
  Built Klean110Exchange.Rewrite
  Built Klean110Exchange
  Build completed successfully.
```

The returned evidence is:

```text
status:                          KLEAN_NO_OBLIGATIONS
obligation_count:                0
target:                          null
frozen_input_sha256:             9a49aecaeece05fe3ea241df1f08949a341d6ddd2dbf80e4ad0a2e45b4aaef8b
stage3_discovery_manifest_sha256: d95c59386f33947a3975de80e63804c5adf550cfbcad82f9f033e863249cc8da
generated_tree_sha256:            2fd779a4efd71d0e63e2877c0186009566f2940107d1849047b3da3d1d8253b0
designated_sorry_count:           0
trust_declaration_count:          42
```

The clean/build output hashes exactly match the recorded preflight. The
trusted checker also established that the 42 generated trust declarations
exactly match `trust-inventory.json`, that there are no generated
proposition/proof assumptions, and that the immutable generated project
contains no `sorry`, `admit`, or `unsafe`. These declarations are generated
executable/data-model boundaries; there is no theorem target depending on
them in this mode.

## Obligation bijection and fixed target

The mathematical and structural views coincide:

```text
independently classified DOMAIN_LEMMA IDs: []
validated Stage 3 DOMAIN_LEMMA IDs:        []
Stage 4 input-manifest source rules:       []
generated obligation-map source rules:    []
generated obligations:                    []
generated trust parameters:               []
```

The source-rule and obligation ID sequences are identical and duplicate-free.
The obligation-map SHA-256 recomputes to
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching `generator-manifest.json`. With zero source rules, there can be no
omitted, weakened, duplicated, irrelevant, or vacuous conjunct.

The trusted target extractor independently returns `null`; the expected target
definition is also `null`; a raw scan finds no `def targetStatement`
declaration. The generator manifest, recorded preflight, export result, and
`/audit-input.json` all consistently record zero obligations and a null
target. Thus the fixed generated target is correctly absent rather than
changed or weakened.

Because the domain-lemma set is genuinely empty, `KLEAN_NO_OBLIGATIONS` is the
correct Stage 4 status. `/candidate` is absent and the launcher records null
Stage 5 workspace, invocation, target, and result fields, as required.
Consequently, Stage 5 clean-build, `Proof.final`, axiom reconciliation, and
operational-bridge parameter checks are not applicable.

## Evidence

- `evidence/01_producer_and_manifests.log`: raw producer hashes and Stage 4
  manifests.
- `evidence/02_hash_recomputation.log`: recomputation of every mounted tree,
  file, selection, and Stage 1 source hash.
- `evidence/02_hash_recomputation_NOTE.md`: explanation of a local wrapper's
  incorrectly typed Boolean in the preceding log.
- `evidence/03_inventory_reconstruction.log`: full canonical inventory,
  source spans, normalized hashes, IDs, order, manifest entries, and
  bijection checks.
- `evidence/04_preflight_rerun.log`: initial environment-level Lake failure.
- `evidence/05_toolchain_diagnosis.log` through
  `evidence/09_toolchain_shim_validation.log`: diagnosis and validation of the
  `/proc` compatibility shim.
- `evidence/10_preflight_rerun_success.log`: successful trusted preflight,
  complete clean/build output, and returned evidence.
- `evidence/11_stage4_bijection_and_target.log`: independent zero-domain,
  zero-obligation, and null-target checks.
- `evidence/12_audit_input_contract.log`: correct signed-resolution contract
  and digest check.
- `evidence/13_producer_provenance_gate.log`: explicit producer file/image
  equality checks.
- `evidence/14_rule_usage_and_target_scan.log`: rule uses across the frozen K
  sources and absence of a generated target declaration.

VERDICT: PASS
LEGITIMACY: LEGIT
