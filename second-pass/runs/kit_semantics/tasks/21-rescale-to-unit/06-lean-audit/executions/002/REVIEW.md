# Independent audit: `21-rescale-to-unit`

## Scope and result

- Condition: `kit-semantics`
- Semantics mode: `SUPPLIED_SEMANTICS`
- Audit mode: `CLASSIFICATION_AND_PROOF`
- Frozen Stage 1 workspace: `/reference/k-proof`
- Protected Stage 3 manifest: `/reference/lemma-discovery.json`
- Selected Stage 4 generation: `/reference/klean-generation`
- Stage 5 candidate: `/candidate`

I treated candidate files, prior reviews, logs, comments, and recorded conclusions
as untrusted evidence. I used the trusted inventory and gate implementations under
`/reference/tools` and independently checked the mathematical meaning of the
classification, obligations, and Lean parameter definitions.

The Stage 3 classification is complete and correct, Stage 4 is a deterministic
and faithful two-obligation generation, and `Proof.final` proves the exact fixed
target with operationally faithful definitions on every source-rule domain.

## Producer-source provenance gate

This gate passed before any Stage 4 judgment:

- `/reference/generation-tools/klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `/reference/generation-tools/klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`
- Producer tree:
  `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`
- Generator image:
  `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`

Both file hashes match `source-manifest.json` and `generator-manifest.json`.
The producer tree matches `/audit-input.json`. The same image ID is recorded by
the source manifest, generator manifest, and the basename of the launcher-bound
producer-source path in `/audit-input.json`. This is not an infrastructure
`AUDIT_ERROR`.

Raw result: `evidence/01_producer_provenance.log`.

## Stage 3 inventory reconstruction

I ran `tools.k_rule_inventory.inventory_verification` against the frozen
workspace, then separately recomputed every rule's normalized text hash and
`source_rule_id`.

Reconstruction result:

- Verification file SHA-256:
  `de602bdfc9d1ef6af603070a4a696107710fdd2c0125cf2beb4308060e27707c`
- Selected module: `VERIFICATION`
- Local verification-module closure: `[VERIFICATION]`
- Rule count: 27
- Inventory SHA-256:
  `92208488f5b3fbe4f881489dcbdba726ef2025162d4234a071210c0a94048c89`

For all 27 entries:

- the reconstructed start and end lines select the recorded source text;
- SHA-256 of whitespace-normalized text equals `normalized_sha256`;
- `source_rule_id` is exactly `rule-<normalized_sha256>`;
- the canonical JSON hash of the ordered rule list equals the inventory hash.

The protected manifest has exactly 27 distinct identities in the same order.
There are no omissions, extras, duplicates, reordered identities, or hash
changes. The trusted Stage 3 contract also validates the same inventory.

Complete reconstructed records and exact comparisons are in
`evidence/02_inventory_reconstruction.log`.

## Independent classification judgment

My classification is 25 `DEFINITION`, zero `OPERATIONAL_RULE`, zero
`PROVED_DERIVED_LEMMA`, and two `DOMAIN_LEMMA`. It agrees entry-for-entry with
the protected manifest.

| Frozen lines | Rules | Count | Classification and reason |
|---|---|---:|---|
| 8–10 | `allFloatVS` base/recurrence | 2 | `DEFINITION`: defines the homogeneous-float domain summary. |
| 15 | `definedProjectFloat` | 1 | `DEFINITION`: names the projection-domain predicate. |
| 20–22 | `#Ceil` of the Val-to-Float cast | 1 | `DOMAIN_LEMMA`: characterizes the domain of an existing partial cast. |
| 24–30 | `projectFloatTotal` and guarded cast equations | 3 | `DEFINITION`: defines a named total proof term and its guarded connection to the cast. |
| 34–37 | guarded dynamic-Val subtraction dispatch | 1 | `DOMAIN_LEMMA`: lifts the fixed static-Float dispatch across a dynamic Val under `isFloat`. |
| 46–49 | `minFOpaque`, `maxFOpaque` aliases | 2 | `DEFINITION`: names supplied opaque float primitives; these are proof terms, not derived facts. |
| 53–66 | `minTailF`, `maxTailF` | 6 | `DEFINITION`: base cases, structural recurrences, and off-domain totalization. |
| 69–82 | `minVF`, `maxVF` | 6 | `DEFINITION`: total summary functions seeded from the first value. |
| 89–108 | `scaleAcc` | 3 | `DEFINITION`: structural accumulator recurrence matching the source loop's append order. |
| 114–116 | `lastVal` | 2 | `DEFINITION`: structural summary of the loop-variable binding. |

The two true domain lemmas are:

1. `rule-57727b2acd45f64e74f4c2582f643b13345834dfbe7bf3fe97580d59dcd8ba43`
   at lines 20–22. It is relevant because `projectFloatTotal` and the float
   list summaries cast dynamically sorted `Val` elements to `Float`.
2. `rule-dc58f41e482527dda6d5bd7e29f533ee71f5356475fa5bfad6f9142925059957`
   at lines 34–37. It is relevant because the source loop computes
   `number - min_number`, while `number` is dynamically a `Val` and the fixed
   float dispatch is stated on the static `Float` subsort.

Neither statement is first proved as an exact rule-free K claim and only later
used. The frozen `spec.k` contains loop and end-to-end claims, not a prior proof
of either exact rule. They therefore cannot be `PROVED_DERIVED_LEMMA`.

Every simplification-bearing rule is either a definition or one of these two
domain lemmas. This includes the prioritized `simplification(10)` equation at
lines 25–27. No rule is an ordinary configuration execution/observation step,
so there is no `OPERATIONAL_RULE` in the local closure.

## Stage 4 deterministic generation

### Hashes and bijection

The independently recomputed hashes match every applicable manifest and
`/audit-input.json`:

- Stage 1 export tree:
  `4a72f06c9152fe5be324bf07c9d39c2b8e3b0512e8508cc1ac083eca0e5b401d`
- Stage 1 full tree:
  `c0f5def86533303d50ca94b9ab2dad260b772ca412ee0ab536b2378221e95c28`
- Stage 3 manifest:
  `17dfcbfeb2fef9ad417d580c8e46dfa4b276c24df468c869929775bde79531fc`
- Generated tree:
  `c2f18234a0070f4d668e48966f8394e9fc14c5e04ef63e2fb912a69d3e7127ae`
- Selected generation tree:
  `7ac40b581f4db71b93b7411df59fc4fc4de40392108d17c0412642a1248ed7a1`
- Obligation map:
  `8f2090c90132e4beb3eee2a1762aaffdb7cb31f4adf6369b646e43ff6d5a3629`

The input manifest and obligation map contain exactly the two independently
identified domain rules, in canonical source order. The two generated
obligations have exactly those IDs, source spans, normalized hashes, inventory
hashes, discovery hash, and independently checked conjunct hashes. There are
no omissions, extras, duplicates, or reordered obligations.

### Mathematical adequacy of the obligations

The first obligation is the exact definedness statement for the Val-to-Float
cast: the generated Float projector succeeds exactly when
`definedProjectFloat V` is true. Its displayed `∧ True` is accounted for by the
source rule's explicit `#Ceil(@V)`. A typed Lean `SortVal` is an already-defined
value, so translating that source subterm to `True` is exact; it neither drops
the cast-domain equivalence nor adds an unaccounted vacuous obligation.

The second obligation is the exact guarded subtraction rule: for a Float `F`
and dynamic `V` satisfying `isFloat`, dispatching `applyBin "-" V F` must equal
the injected result of `subF (projectFloatTotal V) F`. It retains the operator,
both operands, guard, result injection, and operand order used by the source
program.

Both obligations are relevant and nontrivial. The true domain set is nonempty,
so `KLEAN_NO_OBLIGATIONS` would be incorrect; the selected `OK`/two-obligation
generation is the required case.

### Fixed target identity

The generated target is the exact conjunction of those obligations:

- Declaration: `Klean21RescaleToUnit.Lemmas.targetStatement`
- Definition SHA-256:
  `5dfb019d3d98a8ac1b644aa237d8a022c95339d47bb6c998dff1b30f35c951e1`
- Applied-statement SHA-256:
  `38ec95d809391263646d8a1043da31394bf27f2f41522825b49ee36e0a136762`

The extracted target metadata equals `generator-manifest.json`, both target
records in `/audit-input.json`, and the target reconstructed from
`obligation-map.json`.

Raw independent checks are in
`evidence/03_stage4_hashes_bijection_target.log`.

### Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with:

```text
PYTHONPATH=/reference
frozen_input=/reference/k-proof
discovery_manifest=/reference/lemma-discovery.json
generation=/reference/klean-generation
toolchain_lock=/reference/klean-toolchain.lock.json
```

Final result: `PASS`, two obligations, 46 recorded generated trust
declarations, zero designated or other sorries, and successful `lake clean`
and `lake build`. See `evidence/04c_preflight_rerun_pinned_toolchain.log`.

The first two attempts exposed an ambient PID-namespace/tool launcher issue,
not an artifact failure: Lean looked up `/proc/<namespace-pid>/exe` while this
sandbox exposes host-indexed `/proc`. I used the pinned Lean 4.22.0 toolchain
and a narrow `readlink` shim that redirects only numeric
`/proc/<pid>/exe` lookups to `/proc/self/exe`. The shim source is preserved as
`evidence/proc_self_exe_shim.c`. The unchanged trusted checker then passed.
The failed environment attempts remain visible in
`evidence/04a_preflight_initial_environment_failure.log` and
`evidence/04b_preflight_rerun_pinned_environment.log`.

## Stage 5 Lean proof

### Fresh project and clean build

I created `/tmp/audit-work/lean-proof.6L7ByC`, copied the candidate into it,
and copied the immutable generated project into its `Base` directory. Before
and after the build, the source digest of `Base` is the fixed generated-tree
hash
`c2f18234a0070f4d668e48966f8394e9fc14c5e04ef63e2fb912a69d3e7127ae`.

Required commands:

```text
lake clean
lake build
```

Both exit 0. The complete non-interactive output and exit codes are in
`evidence/05d_stage5_fresh_clean_build_complete.log`. The only diagnostic is
the generated target's unused guard-variable linter warning.

The candidate full tree hash is
`541ed72b62cb8b6db379b350e068e699d34befb47f100c91771bc69fd56e433f`,
matching `/audit-input.json`. Candidate sources contain no `sorry`, `admit`,
`unsafe`, new `axiom`, or new `opaque`; all entries are regular files or
directories. The candidate neither defines `targetStatement` nor enters the
generated target namespace. Each of the six target parameters has exactly one
candidate `def`. See `evidence/05c_stage5_source_integrity.log`.

### Proof identity

`#check Proof.final` reports exactly:

```text
Klean21RescaleToUnit.Lemmas.targetStatement
  Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»
  Proof.«definedProjectFloat(_)_VERIFICATION_Bool_Val»
  Proof.isFloat Proof.projectFloatTotal Proof.subF
  Proof.«project:Float?»
```

This is the fixed manifest application, with the candidate's six definitions
and no duplicate or weakened theorem. The source declaration also matches the
manifest statement after whitespace normalization. Exact output:
`evidence/07_proof_target_identity.log`.

### Axiom accounting

Running Lean with `#print axioms Proof.final` produced:

```text
'Proof.final' depends on axioms: [propext, Classical.choice]
```

There is no `sorryAx`. `propext` and `Classical.choice` are Lean's standard
logical foundation entries accepted by the trusted gate's fixed logical
allowlist; neither is introduced by the candidate. The generated
`trust-inventory.json` contains 46 Klean boundary declarations, all
structurally reconciled by preflight, and none appears in the dependency set
of `Proof.final`. Thus there is no unrecorded candidate or generated proof
escape. Exact output is in `evidence/06_print_axioms_proof_final.log`; the
trusted Stage 5 mechanical gate independently reaches the same result in
`evidence/11_stage5_trusted_mechanical_gate.log`.

### Operational bridge audit

I compared each definition with its manifest `kore_symbol`, bound source-rule
IDs, frozen K rules, fixed operational semantics, and the source program.

| Parameter | Independent operational judgment |
|---|---|
| `applyBin` | On the complete load-bearing domain—operator `"-"`, Float right operand, and dynamic left operand satisfying `isFloat`—the candidate exposes the left Float and returns `inj_SortFloat (Float.sub left right)`. This matches fixed `applyBin("-", F1:Float, F2:Float) => subF(F1,F2)` and concrete `subF => _-Float_`. Other modeled Int/Float branches follow the frozen dispatch. The fallback totalization is outside the bound guarded rule domain and cannot discharge either obligation. |
| `definedProjectFloat` | Returns true exactly for `SortVal.inj_SortFloat`; this is the K sort test used by the cast-domain rule. |
| `isFloat` | Returns true exactly for a canonical single injected Float K item with `.K` suffix. Integer and nonterminal-continuation adversarial cases return false. |
| `projectFloatTotal` | Returns the underlying Float on the `isFloat` domain, matching the identity and guarded cast equations. Its off-domain total value is never used by the bound rule. |
| `subF` | Is `Float.sub`, matching the fixed concrete `F1 -Float F2` interpretation and preserving operand order. |
| `project:Float?` | Returns `some value` exactly for the canonical injected Float term and `none` for tested non-Float terms, matching cast definedness. |

`evidence/08_operational_parameter_tests.log` records successful Lean checks
for Float and integer witnesses, a nonempty K continuation, subtraction,
addition, and unmatched dispatch. The exact frozen and candidate definitions
are collected in `evidence/10_operational_bridge_sources.log`.

As a counterfactual sensitivity test, I changed the Float subtraction branch
of `applyBin` to return its left operand. The build then exited 1 at
`Proof.lean:115`; Lean showed that the mutated dispatch was not definitionally
equal to `subF (projectFloatTotal V) F`. The full failure is in
`evidence/09_counterfactual_wrong_subtraction_build.log`. This rejects the
identity/hard-coded mutation and confirms that the actual load-bearing bridge
is constrained.

## Final judgment

The reconstructed inventory is bijective with Stage 3, all classifications
meet their semantic categories, the true domain set is exactly the two relevant
lemmas, Stage 4 preserves them in an exact fixed target, and Stage 5 proves
that target with clean source, acceptable axiom dependencies, and faithful
operational definitions. No concern changes the proof claim or legitimacy.

VERDICT: PASS
LEGITIMACY: LEGIT
