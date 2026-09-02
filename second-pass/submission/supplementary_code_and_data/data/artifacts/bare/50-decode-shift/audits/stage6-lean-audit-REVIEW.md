# Independent Stage 3–5 audit: `50-decode-shift`

## Result

The selected result is legitimate. The launcher mode is
`CLASSIFICATION_ONLY`, the independent Stage 3 classification has no domain
lemmas, and Stage 4 correctly records `KLEAN_NO_OBLIGATIONS`. The generated
source-rule set, obligation set, and target are respectively empty, empty, and
null. `/candidate` is absent as required. Stage 5 proof checks therefore do
not apply.

No earlier review, PASS marker, rationale, or log was used as authority. The
selected Stage 2 audit was used only as an opaque tree whose launcher-recorded
hash was recomputed.

## Mode and frozen-input identity

- `AUDIT_MODE` and `/audit-input.json` both say `CLASSIFICATION_ONLY`.
- Problem: `50-decode-shift`.
- Condition: `bare`.
- Semantics mode: `GENERATED_SEMANTICS`.
- The canonical hash of the launcher resolution is
  `036ddf27fab8808b5f5d9ff8016556bac36a028c5d270d5c1a6fe5491ed34a05`,
  exactly its recorded `resolved_input_sha256`.
- Every per-file Stage 1 source hash matches `/audit-input.json`.
- The Stage 1 pipeline tree hash is
  `17f0ad45c95027f149dc9b8d751e4fe248f5ac891094f4bc586f0ba4bc06ac21`;
  its Klean frozen-export digest is
  `c6b7befe51bd61e175ceec6b2c791fca2356d9e9747d993921b2d7a73e8c95b5`.
- The selected Stage 2 opaque tree hash is
  `c524c88108ad819a25946dc4d69300d352ca873d180b8f0b5f6da26184bf2f40`.

The recomputations and launcher equality checks are in
`evidence/09_recomputed_tree_hashes.txt` and
`evidence/33_independent_stage4_check.txt`.

## Generation-producer provenance gate

This gate passed before the Stage 4 judgment:

| Producer | Actual SHA-256 | Manifest SHA-256 |
|---|---|---|
| `klean_export.py` | `2f04f1bc0f49f9f8c6f009875e730866a61c76ac029663d2ed2ffaffeab4e773` | same in `source-manifest.json` and `generator-manifest.json` |
| `klean.py` | `308fb4d213034fc0c00cd37e9617f6b05f10bda7bc7e383994786911f8a04bcc` | same in `source-manifest.json` and `generator-manifest.json` |

The producer-source pipeline tree digest is
`305f865953323958cc46250998c0ae761309c7bc7c60d6a2206b72df280f8354`,
matching `/audit-input.json`. The immutable generator image ID is
`sha256:9b919795ce70e46b5f58b36984cd9be4f84d1b056135e41498da6390ff4c5fa2`.
It is identical in `source-manifest.json` and `generator-manifest.json`; the
same digest is the terminal component of the producer-source path recorded by
the launcher.

Exact evidence is in `evidence/10_producer_provenance_gate.txt`.

## Canonical inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` from the trusted
`/reference` package against `/reference/k-proof`. It selected
`VERIFICATION`, whose local verification-module closure contains only that
module. The reconstruction found exactly nine ordered rules.

- Frozen `verification.k` SHA-256:
  `643042ae13c80e6cca21a1fd85dc91df9e60020754ec2fe727991d8866c77c92`.
- Whole canonical inventory SHA-256:
  `3d01d1f5125fc451e01e2c1d535329fec6ae9582a016e32d5fc1455e7812226c`.

For every row below, the normalized source SHA-256 is the suffix of the
displayed `source_rule_id`. Each span was independently sliced from frozen
`verification.k`, whitespace-normalized, hashed, and compared with the trusted
inventory result.

| Span | Exact `source_rule_id` | Independent class |
|---|---|---|
| 11–11 | `rule-d4ef40fe9e72b4a01ee701f6d6971ab3c47b2cb15ab743e809966b320fa2025e` | `DEFINITION` |
| 14–14 | `rule-1ea18c24cdb3a1935f7d7f77f6fb4e066945fe3501b1b600338f893826670097` | `DEFINITION` |
| 15–15 | `rule-52973ed25e536e8d1b46be38eaf35edbdd02e2dd02c53d61ef885e05950035ac` | `DEFINITION` |
| 18–18 | `rule-bf869afd467d96c7f40ef972137daeb64051501927c30f112761f5bd7afa6625` | `DEFINITION` |
| 21–21 | `rule-f469c289252f391f79088f48b68022ee3475b8af3a4512cab3b85b8bd546dd25` | `DEFINITION` |
| 22–22 | `rule-98869a9efb7f8a08b961eb88933575887fe7cd8cdeda236cf56a7f98486d94b8` | `DEFINITION` |
| 25–25 | `rule-14730e10b61f875e28e467d4f0865be99395d197f927b3331e5dc6459521473c` | `DEFINITION` |
| 28–28 | `rule-a54b1751451da8cc52a08176b0c06449f46d52d2528695a22dc27bd2e131c092` | `DEFINITION` |
| 29–29 | `rule-88e0dd7c4b09699c6346cfbedbf81edeb318cc01d7c0826676cdb7529dabad2f` | `DEFINITION` |

The protected Stage 3 manifest contains these nine identities exactly once
and in this exact order. Its inventory hash is the reconstructed inventory
hash. There are no omitted, duplicated, extra, reordered, or changed
identities. The discovery-manifest file hash is
`28337803e7c132a91b1a71bb5a792741e8950d9d4ca2032b2b3b097ed8cf2f3b`,
matching every launcher and generator binding.

Raw reconstruction is in `evidence/06_reconstructed_rule_inventory.json.log`.
The exact ordered comparison and independent classification are in
`evidence/11_inventory_bijection_and_classification.txt`; the check source is
`evidence/independent_inventory_check.py`.

## Independent semantic classification

All nine entries are definitions, for the following source-semantic reasons:

- `decodeCode` and `encodeCode` are unconditional arithmetic equations naming
  the one-character decoder and encoder summaries.
- The two equations for `decodeSpec` and the two for `encodeSpec` are the
  exhaustive `nil`/`cons` structural recurrences over `Chars`.
- `isLowerCode` names the inclusive lowercase-code predicate.
- The two `allLower` equations are the exhaustive `nil`/`cons` structural
  recurrence for the sequence predicate.

Each symbol is declared `[function, total]`. The integer equations are
unconditional. The sequence equations cover the two constructors without
overlap and recurse strictly on the tail. None of the nine rules has a
`simplification` attribute, so there is no simplification-classification
violation.

These rules do not match `<k>` cells, configurations, evaluator terms,
translated program AST nodes, or any ordinary execution state. They therefore
do not preempt or replace operational execution. In the frozen semantics,
`Module` dispatches to the translated body; `eval`, `BinOp`, `ord`, `chr`,
`comp`, and `join` perform the actual computation. The solution body computes
`((ord(ch) - 5 - ord("a")) % 26) + ord("a")`, while `decodeCode` gives the
same integer expression with `ord("a") = 97`, and `decodeSpec` maps it over
the character sequence. Thus these are contract-side summaries, not
operational bridges.

No inventory entry is an independently asserted algebraic or domain fact.
The actual inverse property is a `claim` in `spec.k`, not a rule in this
inventory. No inventory entry is first proved against a module omitting it and
then installed for a later proof, so none qualifies as
`PROVED_DERIVED_LEMMA`. The independent counts are consequently:

- `DEFINITION`: 9
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The summaries and predicates are connected to the frozen task: the decode
summary is the program postcondition, the encoder summary comes from the
prompt and its inverse claim, and the lowercase predicates are the proof
preconditions. There is no irrelevant claimed domain lemma.

Frozen source, semantics, program, and claim text are preserved in
`evidence/08_frozen_stage1_sources.txt`.

## Deterministic Stage 4 integrity

The main Stage 4 bindings all recompute exactly:

| Binding | Recomputed value |
|---|---|
| Generated project digest | `e0fb1258cfb26bb0cb962306b5dbc94ab07b0f2c578bb5792afc9f0d03df05e0` |
| Full selected generation pipeline hash | `a91d8f989b317769ea109b82d892e71281bb31e1ec0ce7c1cf2bc8097ae0d048` |
| Obligation-map file hash | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust-inventory file hash | `b3335ac3a6c2688c622204e64ba200c8cf8b9da2ddb96c707b2703529a860411` |

`generator-manifest.json` has the exact pinned toolchain object from
`/reference/klean-toolchain.lock.json`. Its Stage 1, Stage 3, inventory,
producer, generated-tree, and obligation-map bindings all match the
recomputed values. `input-manifest.json` contains the same nine canonical
definitions and no operational rules, proved-derived lemmas, or domain source
rules.

The independently classified domain set is genuinely empty.
`generated/obligation-map.json` is exactly:

```json
{
  "obligations": [],
  "schema_version": 3,
  "source_rules": [],
  "trust_parameters": []
}
```

This is an exact empty-to-empty source-rule/obligation bijection: no omission,
duplicate, irrelevant obligation, weakened obligation, or vacuous conjunct
exists. The expected target definition is null,
`tools.klean_export.target_statement` returns null, and the generator,
recorded preflight, and launcher all record `target: null`. An independent
scan finds no Lean `theorem` or `lemma` declaration in the generated project.

The selected `KLEAN_NO_OBLIGATIONS` status is therefore the correct result of
the mathematical classification, not merely a self-consistent manifest
choice.

The complete independent hash/mapping/target assertions are in
`evidence/33_independent_stage4_check.txt`, with source in
`evidence/independent_stage4_check.py`. The raw map, target module, trust
inventory, and candidate-absence check are in
`evidence/31_stage4_mapping_target_and_candidate.txt`.

## Required preflight rerun

The required call to `tools.klean_preflight.check_generation`, with
`PYTHONPATH=/reference` and the specified Stage 1, Stage 3, and Stage 4 paths,
returned:

- status: `KLEAN_NO_OBLIGATIONS`
- obligation count: 0
- target: null
- designated sorry count: 0
- generated trust declaration count: 41
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output SHA-256
  `e07d26ec145e1d06f35a3ff1cc93b721254b01c25f2b1d8d1e1e20ad1e45c700`

The complete returned evidence is
`evidence/30_rerun_klean_preflight_with_proc_compat.txt`. These diagnostics
are byte-for-byte the hashes recorded by the launcher.

The first direct rerun exposed a sandbox-specific toolchain issue: this
sandbox denies Lean 4.22's `/proc/<getpid()>/exe` lookup, so Lake could not
locate its installation. That failed attempt is retained in
`evidence/12_rerun_klean_preflight.txt`, and the denial is demonstrated in
`evidence/28_proc_pid_exe_probe.txt`. I used the recorded compatibility shim
`evidence/proc_exe_compat.c`, SHA-256
`6b67f4a8861d0e5aab61e57f8f1e8673de2eb97b018c95fb0c7bc465f196eaef`.
It redirects only numeric `/proc/<pid>/exe` `readlink` calls to
`/proc/self/exe`; it does not modify the frozen inputs, generated project,
Lean executable, imports, declarations, or proof logic. With that path-only
repair, Lean reports the pinned 4.22.0 commit and the unchanged trusted
preflight succeeds.

The trusted final mechanical gate was also run with the same path-discovery
compatibility. It returned status `PASS`, mode `CLASSIFICATION_ONLY`, null
target, null candidate hash, no diagnostics, no used axioms, and the same
preflight/hash evidence. Its exact output is
`evidence/35_trusted_final_mechanical_gate.txt`. Its model-free
`semantic_classification: NOT_EVALUATED` is supplied by the independent
classification above.

## Stage 5 applicability and trust accounting

Stage 5 is inapplicable because the recorded and active mode is
`CLASSIFICATION_ONLY`. In addition:

- `/candidate` does not exist.
- There is no generated target declaration.
- There are no target parameters or operational bridges to audit.
- There is no `Proof.final`, so a `#print axioms Proof.final` run would not be
  meaningful.

The generated semantics contains 41 allowlisted executable hook declarations,
which the preflight reconciles with `trust-inventory.json` and checks are not
proposition trust. Because there is no generated proposition and no Stage 5
proof, these declarations do not establish or discharge a theorem in this
audit. The final mechanical gate accordingly reports `used_axioms: []`.

## Evidence summary

All raw commands and results are under `/audit-output/evidence/`. The primary
records are:

- `00_environment_and_files.txt`
- `06_reconstructed_rule_inventory.json.log`
- `08_frozen_stage1_sources.txt`
- `10_producer_provenance_gate.txt`
- `11_inventory_bijection_and_classification.txt`
- `30_rerun_klean_preflight_with_proc_compat.txt`
- `31_stage4_mapping_target_and_candidate.txt`
- `33_independent_stage4_check.txt`
- `35_trusted_final_mechanical_gate.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
