# Independent Stage 3–5 audit: `27-flip-case`, `bare`

## Result and scope

This audit confirms the Stage 3 classification and deterministic Stage 4
`KLEAN_NO_OBLIGATIONS` result. The launcher-recorded mode is
`CLASSIFICATION_ONLY`, both in `AUDIT_MODE` and `/audit-input.json`; therefore
Stage 5 Lean proof checks are not applicable. `/candidate` is absent, as
required for a no-obligation result.

I treated the mounted candidate/provenance artifacts, including prior reviews,
logs, comments, and classifications, only as untrusted evidence. The
classification below was reconstructed from frozen source and operational
semantics. Mechanical checks used only `/reference/tools` with
`PYTHONPATH=/reference`.

## Input and producer integrity

`stage6_resolution_contract.verify_audit_input` recomputed the canonical
resolved-input digest as
`a6ff3100626aeaecb229a77e44e645ed73b8ee9e510b7a6eb80757728bbb0b60`,
exactly matching `/audit-input.json`.

All launcher-recorded resolution hashes independently match their mounted
inputs:

| Input | Recomputed hash |
|---|---|
| Stage 1 workspace, pipeline tree hash | `f2b6d0dfd1ff9115f278a29e49d913f9705b0ba8d2d80772c5c33debacb4905e` |
| Stage 1 export, Klean tree digest | `d11693cdb57522ce42cef3abd21dd6e4d3fa3d6a3e154f0499875bd494d31b3f` |
| Stage 3 manifest | `68bba38c3652a276f6263235270b503ea84dc8cc760e8d560abf1ecbb15d1c6a` |
| Selected Stage 2 audit tree | `62b09107fac3255339870dcc566b5dd6ba43d364a331691581467db693cabfc8` |
| Selected Stage 4 generation tree | `02509f357d0a268b90dde58d9f31a67c195b1af16d816fead628fd0d2619c53c` |
| Producer-source bundle tree | `7b7fdfe618031c11f79bb3d7eec7df24bc64a9a480fc470c1176ce36a593286a` |
| Generated project tree | `dbecd54c61651fd55fa375403a6a0cbba4ec6d83cb5afa1e9404d05824a66e01` |

All ten Stage 1 per-file source hashes also match. The complete recomputation is
in [25_independent_recorded_hash_recomputation.txt](/audit-output/evidence/25_independent_recorded_hash_recomputation.txt).

The mandatory producer-source gate passes:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `4fa919ac98483620c7024ed7424c8b19f21406a2146feafad84ab4c813117881` |
| `klean.py` | `5d419b1cf907ab880eeb88a68e0d6da0bf59a92a56a0803b34d53698d91caabe` |

Those values agree exactly with both `source-manifest.json` and
`generator-manifest.json`. The immutable generator image ID is
`sha256:15baeb15b1ea8266bfad3dbc3a75ee531cf429f1b73e0e3ff478f279e6308f63`
in the source manifest, generator manifest, and audit-input producer-bundle
identity. The bundle contains exactly the two producer files plus its source
manifest. Thus there is no producer-provenance `AUDIT_ERROR`.

## Inventory reconstruction and Stage 3 bijection

The trusted `tools.k_rule_inventory.inventory_verification` selected
`VERIFICATION`, followed its local in-file module closure, and reconstructed
exactly one rule:

| Field | Reconstructed value |
|---|---|
| Module closure | `["VERIFICATION"]` |
| Source span | `verification.k:9–9` |
| Text | `rule flipSpec(S) => pySwapCase(S)` |
| Attributes | none |
| Normalized SHA-256 | `8457197f496be485d41f7599c86b9099304f92420061b607ba1a9f3e010a9ab0` |
| `source_rule_id` | `rule-8457197f496be485d41f7599c86b9099304f92420061b607ba1a9f3e010a9ab0` |
| Independent classification | `DEFINITION` |

The normalized hash was also recomputed directly from the normalized rule text.
The canonical whole-inventory hash is
`80c8724000a370da3d656bdbe33a27678acdb60fb6d00723589be7d2fabac9e2`.

`tools.lemma_discovery_contract.validate_trust_boundary` accepts the Stage 3
manifest against that reconstruction. There is one canonical identity and one
manifest entry, in the same only possible order. Consequently there are no
omissions, duplicates, extras, reordered identities, changed hashes, or
unaccounted classifications. See
[10_reconstructed_inventory.json](/audit-output/evidence/10_reconstructed_inventory.json)
and
[11_stage3_contract_validation.json](/audit-output/evidence/11_stage3_contract_validation.json).

## Independent classification judgment

The frozen source program is:

```python
def flip_case(string: str) -> str:
    return string.swapcase()
```

The operational K trace is direct:

1. The module rule installs and invokes `flip_case` on the supplied string.
2. Invocation binds the formal `string` to `strVal(S)`.
3. `Name("string")` evaluates to that value.
4. `Attribute(..., "swapcase")` produces
   `boundStringMethod("swapcase", S)`.
5. The no-argument call rule returns `strVal(pySwapCase(S))`.
6. `pySwapCase` has its own empty-string/base rule and per-character recurrence
   in the frozen semantics.

The specification's symbolic postcondition is `strVal(flipSpec(S))`.
`flipSpec` is introduced as a fresh function immediately before the inventory
rule. Its rule has no configuration cells, control term, state, guard, or
operational AST on the left-hand side. It merely gives the named contract term
the exact value already produced by the operational method-call semantics:
`pySwapCase(S)`.

This is precisely a named summary definition. It does not replace program
execution, assert a separate mathematical property, or rely on a
previously-proved lemma. It is therefore not an `OPERATIONAL_RULE`,
`PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`. It is relevant to both the source
operation and the postcondition. The rule has no `simplification` attribute, so
the simplification restriction is also satisfied.

The independently classified true domain-lemma set is therefore genuinely
empty.

## Deterministic Stage 4 generation

The generation-time producer logic takes exactly the validated
`domain_lemmas` list as `source_rules`, requires the generated obligation IDs
to equal those source IDs in order, enriches each obligation with the frozen
span and hashes, and emits a target only when the obligation list is nonempty.
The exact generation-time code used for this check is preserved in
[45_generation_time_obligation_logic.txt](/audit-output/evidence/45_generation_time_obligation_logic.txt).

For this case, every layer contains the same empty set:

- `input-manifest.json`: `source_rules = []`;
- `obligation-map.json`: `source_rules = []`, `obligations = []`,
  `trust_parameters = []`;
- `generator-manifest.json`: `obligation_count = 0`, `target = null`;
- `export-result.json`: `obligation_count = 0`,
  `status = KLEAN_NO_OBLIGATIONS`;
- `/audit-input.json`: `target = null`.

The obligation-map SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. Trusted `expected_target_definition` and
`target_statement` both return `None`. `Lemmas.lean` has an empty namespace and
there is no `targetStatement` declaration anywhere in the generated Lean
sources. There is therefore no omitted, duplicated, irrelevant, weakened, or
vacuous conjunct and no changed target; there is no target at all because the
mathematically correct domain set is empty.

The trusted sequential call to
`tools.klean_preflight.check_generation` returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- designated sorry count `0`;
- trust declaration count `51`;
- `lake clean` exit `0`;
- `lake build` exit `0`; and
- complete build through `Klean27FlipCase`, with output SHA-256
  `465a410d8644d436e51c299761123deef0247d0c2df985aaf7cacab5511c4b68`.

Its full returned document is
[47_check_generation_final_sequential.json](/audit-output/evidence/47_check_generation_final_sequential.json).
It is byte-for-byte identical to the stored Stage 4 `preflight.json` and
structurally identical to the preflight bound into `/audit-input.json`.

The generated project contains 51 allowlisted value-level hook/function axioms,
but the trusted preflight independently confirms that none is proposition
trust, the allowlist equals the declarations, and the generated project has no
`sorry`, `admit`, or `unsafe`. With no proposition target, these declarations
do not create a Stage 5 proof obligation.

### Toolchain environment note

The first preflight attempt failed before evaluation because the sandbox omits
numeric `/proc/<namespace-pid>/exe` entries that Lean 4.22 uses to locate
itself. `/proc/self/exe` remained available. I used an audit-local
`LD_PRELOAD` shim that redirects only numeric `/proc/<digits>/exe` `readlink`
requests to `/proc/self/exe`; its source and hashes are recorded in
[38_proc_self_shim_build_and_test.txt](/audit-output/evidence/38_proc_self_shim_build_and_test.txt).
The shim did not modify any frozen input, generated source, checker, or theorem.
After exploratory builds had drained, the authoritative preflight was rerun
alone. Its returned evidence exactly reproduces the immutable recorded result,
so this environment issue does not affect the verdict.

## Target identity and Stage 5

The fixed generated target is consistently absent. This is the only valid
target identity for the genuine empty domain set. `/candidate` is absent, and
the audit input has `lean_workspace = null`, `lean_invocation = null`, and
`stage5_result = null`.

Accordingly, clean candidate copying/building, `Proof.final`, `#print axioms`,
candidate forbidden-token checks, trust-dependency reconciliation, and
operational-bridge parameter testing are all not applicable in the
launcher-recorded `CLASSIFICATION_ONLY` mode. Running or inventing a Stage 5
proof here would contradict the no-obligation contract.

## Evidence

The exact principal commands are indexed in
[COMMANDS.md](/audit-output/evidence/COMMANDS.md). The strongest summary checks
are:

- [25_independent_recorded_hash_recomputation.txt](/audit-output/evidence/25_independent_recorded_hash_recomputation.txt);
- [26_producer_provenance_crosscheck.txt](/audit-output/evidence/26_producer_provenance_crosscheck.txt);
- [44_independent_zero_obligation_bijection.txt](/audit-output/evidence/44_independent_zero_obligation_bijection.txt);
- [47_check_generation_final_sequential.json](/audit-output/evidence/47_check_generation_final_sequential.json);
- [48_stage4_cross_manifest_hash_and_replay_check.txt](/audit-output/evidence/48_stage4_cross_manifest_hash_and_replay_check.txt); and
- [49_preflight_replay_file_hashes.txt](/audit-output/evidence/49_preflight_replay_file_hashes.txt).

All classification, provenance, bijection, target-identity, and applicable
mechanical gates pass. The selected Stage 4 status is legitimate only because
the independent classification found a genuinely empty domain set, which it
did.

VERDICT: PASS
LEGITIMACY: LEGIT
