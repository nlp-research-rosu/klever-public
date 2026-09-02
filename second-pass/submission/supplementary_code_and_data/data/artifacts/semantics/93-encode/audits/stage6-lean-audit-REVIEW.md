# Independent audit: HumanEval `93-encode`

## Scope and result

This audit covers condition `semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. I treated all
mounted candidate and provenance content as untrusted evidence. I did not use
the selected Stage 2 verdict or any earlier classification as an authority.

The independent result is that the local verification-module closure contains
eight rules, all eight are genuine definitions, and the true
`DOMAIN_LEMMA` set is empty. The deterministic Stage 4 status
`KLEAN_NO_OBLIGATIONS` is therefore appropriate. There is no generated target
and no Stage 5 candidate.

## Launcher and immutable-input integrity

`AUDIT_MODE` and `/audit-input.json` both record `CLASSIFICATION_ONLY`.
The audit-input envelope and canonical resolution digest validate. The observed
digest is
`0c6d0d8ed2ab1f6c730caf12ba21afd1bf48a7ceb60978dc8157c0f16f31e717`,
exactly the recorded value.

I recomputed every non-null hash in `resolution.hashes` with the same trusted
hash algorithms used by the launcher:

| Artifact | Observed and recorded SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree digest | `5f3cc1e3a0b33b7a4b3e5af4915ee63dcf62f2a02b025c853f20661847519626` |
| Stage 1 exporter tree digest | `30810267a8bf6bd9243148c5a29db6923e3f732c3f2044a9fd71bbac25e719ec` |
| Stage 2 selected audit, pipeline tree digest | `6d4e48e328dc8c7392b764b4608aa6aa255250d85deb3856dfe585e46dd9886b` |
| Stage 3 discovery manifest | `d81d6f164607869f219eb2ab228546958e30d659cb1a533b75a567ea2915e8fd` |
| Stage 4 selected generation, pipeline tree digest | `4f3639619b866f8da8b88e814606be8bd105dc2dcad6d1ef2152cd8653c14c8d` |
| Stage 4 generated project, exporter tree digest | `bdb8401eef01e61db3ff4726737781cf76faddd4f83d6d90f156b69b30495802` |
| Generation producer-source bundle, pipeline tree digest | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

All 35 entries in `stage1_source_hashes` were also recomputed and matched
bijectively: there were no missing, extra, or changed files. Both selected
artifact hashes match their mounted trees. The nullable Lean workspace and
invocation hashes are both null, consistent with classification-only mode.
Full comparisons are in `evidence/07_all_recorded_hashes.json`.

## Generator-producer provenance

I performed this check before judging Stage 4.

| Producer | Observed SHA-256 | Generator manifest | Source manifest |
|---|---|---|---|
| `klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` | same | same |
| `klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` | same | same |

The producer bundle contains exactly those two files and
`source-manifest.json`. The generator image ID is
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the generator manifest and source manifest. The same ID is encoded as the
basename of the producer-source path signed into `/audit-input.json`. All three
bindings match, and the producer bundle's recomputed tree hash matches the
audit input. Thus there is no producer-source infrastructure error.

## Rule inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`. `prove.sh` selects `ENCODE-VERIFICATION`. The local
closure reconstructed by the inventory code is exactly
`["ENCODE-VERIFICATION"]`; `MPY` is supplied from the separately required
semantics and is not a module declared locally in `verification.k`.

The frozen `verification.k` hash is
`2de45a456ee357bbdb8dd8ffd5948dc04cce22fa521e7ce10d1fa7cf9c654b1e`.
The reconstructed canonical inventory hash is
`e3cb1460d02952d9116b4f977842c33b5a5399e664b221ce7f280b6e21020025`.

The complete source-ordered inventory is:

| Span | Normalized SHA-256 / source rule ID | Independent class |
|---|---|---|
| 9–45 | `4f1c1b8a406c0f6cf8b5d127a3dc79e4ddbab158f74aa40cbbd60e54aa68f543` | `DEFINITION` |
| 48–55 | `fe7cc44ef102427686a96c04572b5ba2207f321d0a51c6a392c8df26f885f857` | `DEFINITION` |
| 60–64 | `c967809d7c1f7190c8ad73e7c196724ba72b22ff8161f4b280ffeb5eec91a81e` | `DEFINITION` |
| 67–68 | `cff78f2fb920faa6ccb5cd7dc82e6fc6fef2f2b8add70a8501a76838d75b7bff` | `DEFINITION` |
| 69–70 | `e36d9423613e355c95d43fc7e640d283a0f29febbbaf355149ebefac14af8c37` | `DEFINITION` |
| 75 | `6f211f83fd1f1b067ef8044b1b3525bab51c6d295ab7ac66fe5024ea27fb9d59` | `DEFINITION` |
| 76–79 | `1a15858c13e575c194c98f523a18428daa99bf08a7d7f9756b8ffe6ea2e12371` | `DEFINITION` |
| 82 | `34c2691cb0a6fbd3e7ddcc90c14b933007085cabf3ad29d27766ad1f2943c4cf` | `DEFINITION` |

Each `source_rule_id` is `rule-` followed by the displayed normalized hash.
The full reconstructed text, spans, attributes, hashes, and IDs are saved in
`evidence/04_inventory_reconstruction.json`.

I separately compared the Stage 3 manifest's entry order rather than relying
only on its validator. Its eight IDs exactly equal the canonical IDs in source
order. Both lists contain eight unique identities. There are no omissions,
duplicates, extras, reorderings, span changes, hash changes, or unaccounted
classifications. No inventory rule has a `simplification` attribute.

## Independent classification judgment

The first two rules expand `encodeLoopBody` and `encodeFunctionBody`. They are
named AST proof terms and match the translated source body, statement order,
arguments, branches, and return exactly. They do not state mathematical facts
about pre-existing symbols and do not replace a configuration transition.

`isVowelCode` is a total Boolean definition listing the ten ASCII vowel codes.
The two `encodeCode` rules are the exhaustive, disjoint guarded cases of a
summary: swap case and add two when the swapped code is a vowel; otherwise
return the swapped code. The two `encodeAcc` rules are disjoint base and
structurally descending recurrence equations. `encodeCodes` is the empty-
accumulator wrapper.

This matches the supplied operational semantics:

- string iteration yields singleton strings from left to right;
- `For` binds each value, runs the body, and recurs on the remaining string;
- `swapcase` maps `swapC`, which uses ASCII `+32`, `-32`, or identity;
- `ord` extracts a singleton code and `chr` creates a singleton ASCII string;
- string `+` uses left-to-right `seqConcat`.

The vowel path always calls `chr` on one of the ten post-swap vowel codes plus
two, which remains inside the semantics' `0 <= I < 128` guard. Boundary cases
also discriminate the definitions: `a -> C`, `A -> c`, `y -> Y`, `Y -> y`,
and nonletters are unchanged; prepending rather than appending would reverse a
multi-character result.

Every rule is relevant to the source program or postcondition. The two named
terms are used by the end-to-end and loop claims; the summary chain
`encodeCodes -> encodeAcc -> encodeCode -> isVowelCode` defines the claimed
result. None is an ordinary execution/observation rule, none is a derived
lemma, and none is a domain lemma. Because no `PROVED_DERIVED_LEMMA` is
claimed, there is no unsupported two-phase derivation claim to accept. The
detailed per-rule rationale is in
`evidence/14_independent_classification.md`.

Independent classification counts:

- `DEFINITION`: 8
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

Therefore the true domain set is genuinely empty.

## Required Stage 4 preflight rerun

I invoked:

```text
LD_PRELOAD=/tmp/audit-work/lean_proc_self_shim.so PYTHONPATH=/reference \
  tools.klean_preflight.check_generation(
    /reference/k-proof,
    /reference/lemma-discovery.json,
    /reference/klean-generation,
    toolchain_lock=/reference/klean-toolchain.lock.json)
```

The first invocation without the preload reached `lake clean` but failed
because this audit container exposes `/proc/self/exe` while not exposing
`/proc/<getpid()>/exe`; Lean 4.22's `lean_io_app_path` hard-codes the latter.
The raw failure is in
`evidence/08a_initial_check_generation_failure.txt`, and the namespace
diagnosis is in `evidence/09p_proc_pid_exe_test.txt`.

I compiled a narrow shim under `/tmp/audit-work` that changes only the exact
`/proc/<own-pid>/exe` `readlink` request to `/proc/self/exe`; every other
`readlink` is passed through unchanged. Its source is preserved at
`/tmp/audit-work/lean_proc_self_shim.c` with SHA-256
`2850f1f7f2779b5f4f499fbdc4a299d2ff2029edfbedc706cb95a2ceb0146e56`.
It changes no mounted input. With the shim, Lean reports version 4.22.0 and
commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly the pinned toolchain.

The required checker then returned:

- status: `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty output;
- `lake build`: exit 0, all seven generated modules built;
- build-output SHA-256:
  `e10ff7b2117c427d89f22dc92e2ad5c7c3d3094b5aa5545914fa4603eaefcb85`;
- obligation count: 0;
- target: null;
- generated tree:
  `bdb8401eef01e61db3ff4726737781cf76faddd4f83d6d90f156b69b30495802`;
- designated sorry count: 0.

The complete returned object is in
`evidence/11_rerun_check_generation.json`. It is byte-for-byte equal as a JSON
value to both the immutable `preflight.json` and the preflight object signed
into `/audit-input.json`; see
`evidence/16_preflight_evidence_comparison.json`.

## Obligation bijection and target identity

I independently projected the validated inventory by classification and
compared it with all Stage 4 records:

- independently determined domain source rules: `[]`;
- `input-manifest.json.source_rules`: `[]`;
- `obligation-map.json.source_rules`: `[]`;
- `obligation-map.json.obligations`: `[]`;
- `obligation-map.json.trust_parameters`: `[]`.

Thus the ordered source-rule/obligation mapping is an exact empty bijection.
There can be no omitted, duplicated, reordered, irrelevant, weakened, or
vacuous conjunct: both sides have cardinality zero and no conjunct exists.
The obligation-map SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest.

The trusted producer's expected target definition is null for this map, and
its parser finds no generated target. The following are all null:

- expected target from the obligation map;
- observed target in the generated project;
- generator-manifest target;
- stored-preflight target;
- audit-input target.

No `targetStatement` or `Proof.final` occurs in the generated project. The
generator, export result, stored preflight, selected Stage 4 record, and
rerun preflight all agree on zero obligations and
`KLEAN_NO_OBLIGATIONS`. All Stage 1, Stage 3, inventory, generated-tree,
obligation-map, and trust-inventory hash bindings agree. The complete
independent comparison is in
`evidence/15_independent_stage4_integrity.json`.

The generated base contains 47 allowlisted executable K-hook axioms and no
proof holes. The preflight reconciled the declarations exactly with
`trust-inventory.json` and rejected proposition-shaped trust. With no target or
obligation, these declarations are not being used to claim a Stage 5 theorem.

## Stage 5 applicability

Stage 5 proof auditing is not applicable. The launcher mode is
`CLASSIFICATION_ONLY`, the independently justified Stage 4 status is
`KLEAN_NO_OBLIGATIONS`, `/candidate` is absent, and the audit input records
null Stage 5 result, workspace, invocation, and target. Creating a proof copy,
running `#print axioms Proof.final`, or auditing target parameters would invent
a target that the verified generation correctly does not contain.

## Evidence index

- `evidence/00_launcher_and_files.txt`: launcher mode, audit input, mounted file inventory
- `evidence/01_generator_provenance.txt` and `01b_generator_manifests.txt`: producer hashes and manifests
- `evidence/03_frozen_source_and_stage3.txt`: numbered source, specification, solution, and Stage 3 manifest
- `evidence/04_inventory_reconstruction.json`: canonical reconstruction and ordered bijection checks
- `evidence/07_all_recorded_hashes.json`: audit envelope, all tree/file hashes, all Stage 1 source hashes, image binding
- `evidence/08a_initial_check_generation_failure.txt` through `10_lean_proc_shim_test.txt`: preflight environment diagnosis and clean workaround validation
- `evidence/11_rerun_check_generation.json`: required preflight return value
- `evidence/12_generated_tree_and_empty_obligations.txt`: generated files, hashes, obligation map, and target search
- `evidence/13_operational_semantics_excerpts.txt`: relevant supplied operational rules
- `evidence/14_independent_classification.md`: detailed classification and counterfactual analysis
- `evidence/15_independent_stage4_integrity.json`: explicit mapping, target, status, and manifest checks
- `evidence/16_preflight_evidence_comparison.json`: rerun/stored/launcher preflight equality
- `evidence/17_trust_inventory_summary.json`: Stage 4 trust inventory summary

VERDICT: PASS
LEGITIMACY: LEGIT
