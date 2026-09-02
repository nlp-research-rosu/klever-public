# Independent Stage 3–5 audit: `114-minSubArraySum`

## Scope and outcome

The launcher environment and the signed resolution both select
`CLASSIFICATION_ONLY`, condition `bare`, and semantics mode
`GENERATED_SEMANTICS`. The signed Stage 6 envelope independently verifies at
digest
`c5abac8cc28d611ed9fcd9625be1885f9c4163ce655aa8818e714680f2434992`.
There is no `/candidate`, the signed Stage 5 result is null, and the signed
target is null. Stage 5 proof checks are therefore correctly inapplicable.

The Stage 3 classification is complete and mathematically sound. Its true
domain-lemma set is genuinely empty. The deterministic Stage 4 artifact has an
empty, bijective obligation map and no generated theorem target. All producer,
source, tree, manifest, and target bindings reconcile, and a fresh trusted
preflight clean-build succeeds.

## Producer and input provenance

I hashed the two mounted generation-time producer sources before judging any
Stage 4 content:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

These values exactly match `source-manifest.json` and
`generator-manifest.json`. Both manifests identify immutable generator image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`;
the image digest is also the final component of the signed
`generation_producer_sources` path in `/audit-input.json`. The complete
producer-source tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
also exactly as signed. There is no producer-source mismatch and hence no
producer infrastructure error.

The independently recomputed principal hashes are:

| Artifact | Recomputed and signed SHA-256 |
|---|---|
| Stage 1 selected artifact tree | `2b26a23bfa05cd2cf81d2b8b1fc4fe517418751995a8cd0cb42e0e0a56eaa373` |
| Frozen Stage 1 export tree | `5874a425c50bb196d38c8288f66281e181404aab59ffc8f7ad279470f2d5fe5a` |
| Stage 2 selected artifact tree | `31058cd519df2853a5d81af972babeaf3facf6a3f44468be2a155c09ff46c1ce` |
| Stage 3 discovery file | `de606f4329c278a43290c6ade5019380eb09b271e19fce7dff7c4a140d5d322c` |
| Stage 4 selected artifact tree | `0c41bd8dcad6722285c258af2ef3f1e52c52871924625686a794cbaab21b5228` |
| Generated Lean project tree | `ac6f10afa71e19de8e85dfd28f7285f9836e799242ffd62742ee9b86f89a1a6d` |

Every individually signed Stage 1 source hash also matches, including
`semantic.k`, `verification.k`, `spec.k`, `solution.py`, `solution.mpy`,
`prompt.py`, `prove.sh`, `py2mpy.py`, and the retained bytecode file. The
complete comparison is in
[38_full_hash_and_target_identity_matrix.txt](evidence/38_full_hash_and_target_identity_matrix.txt);
all 29 independent checks report true.

## Canonical inventory reconstruction

I invoked the trusted `/reference/tools/k_rule_inventory.py` implementation on
the frozen `/reference/k-proof`, without using the prior Stage 2 review or
Stage 3 rationales as authority. `prove.sh` selects main module
`VERIFICATION`. Its local import closure inside `verification.k` contains only
that module, so the canonical local inventory has exactly these six rules, in
source order:

| Lines | `source_rule_id` | Independent class |
|---|---|---|
| 13 | `rule-3f798b6fd39a42a7d25fd8002e3066da3e8617d612075a0b0f57d6d6f522737d` | `DEFINITION` |
| 14–15 | `rule-364e97a48e25174f6f921fb2e22b84b37cec065992df06493163b98d8f09a1e9` | `DEFINITION` |
| 16 | `rule-fd5cdc2c6dc697f6e3f6b9c14f2667eaad0e92175bf0f4d2742cb42eea97c5a3` | `DEFINITION` |
| 17–19 | `rule-5f3cc33399429b30e31fad216187b4997f0ff34c2d707baddaeff6024a5d8dd4` | `DEFINITION` |
| 25–45 | `rule-0b8cd35a8b86672ed79c3b6fee35637ca272dac961db2be56821a1f452a6480c` | `DEFINITION` |
| 48–69 | `rule-05a73970c6cf8df50999bcb3c0f5f61c550a296cda23e9c2047ef21b92784859` | `DEFINITION` |

For each row, the suffix of `source_rule_id` equals the independently
recomputed normalized-source SHA-256. The frozen `verification.k` hash is
`392d58ec7915d7a4ff870cd23ac877211fa9de0ee0af1935cb98dfd41efdb93d`,
and the canonical whole-inventory hash is
`fe65530432cc62ff922aaf7349a6adbc4b22f2a3ef301790fa906c01b6e28d6e`.

The trusted Stage 3 boundary validator confirms an exact ordered bijection with
`/reference/lemma-discovery.json`: no omission, duplicate, extra identity,
reordering, changed hash, or unclassified rule exists. Every attributes list
is empty, so there is no hidden or misclassified `simplification` rule.
The raw reconstruction and boundary result are in
[04_reconstructed_inventory_and_bijection.txt](evidence/04_reconstructed_inventory_and_bijection.txt).

## Independent classification judgment

The first two equations define `minPrefix` by a disjoint,
constructor-recursive recurrence on non-empty integer lists. A non-empty prefix
of `H :: T` is either `[H]` or `H` followed by a non-empty prefix of `T`, which
gives exactly
`min(H, H + minPrefix(T))`. The next two equations similarly define
`minSubarray`: a non-empty contiguous subarray either begins at the current
head and is represented by `minPrefix`, or lies wholly in the tail. Singleton
and at-least-two-element patterns are disjoint and exhaustive over every
claimed non-empty input, and recursive calls strictly shorten the list.

These four rules introduce and define named mathematical summaries. They do
not assert facts about previously defined summaries, rewrite operational
`<k>` configurations, or bypass evaluation. They are therefore definitions,
not domain lemmas, operational rules, or derived lemmas. Both summaries are
directly relevant: `minSubarray` is the exact postcondition value, and
`minPrefix` is its recurrence and the source helper's result.

The remaining rules expand the zero-argument named terms
`solutionFunctions` and `solutionProgram` into, respectively, the exact two
function closures and the exact translated program AST. Their bodies agree
with frozen `solution.mpy` and `solution.py`. They name proof/program terms and
do not accelerate or replace program execution, so they are also definitions.

No rule qualifies as `PROVED_DERIVED_LEMMA`: there is no staged earlier proof
of a same rule followed by later use, and no inventory entry is classified
that way. No inventory entry is an ordinary operational or observation rule,
and none is a domain lemma. Thus the independent category counts are:

- definitions: 6;
- operational rules: 0;
- proved derived lemmas: 0;
- domain lemmas: 0.

This judgment was checked against actual behavior rather than comments. In a
fresh copy under `/tmp/audit-work`, K v7.1.293 rebuilt the semantics and proof,
the supplied exhaustive differential run passed all 19,607 lists, the three
symbolic claims finished with `#Top`, and concrete K executions returned 1,
-6, and 7 for the two prompt cases and a singleton. The complete replay is in
[42_fresh_stage1_replay.txt](evidence/42_fresh_stage1_replay.txt).

Separately, I compared the two recurrences, the frozen Python implementation,
and a direct enumeration of all non-empty contiguous subarrays over 137,256
lists of lengths 1–6 with entries in `[-3,3]`; there were zero mismatches.
Adversarial singleton, mixed-sign, all-zero, and all-negative cases also
agree. Constant-zero, identity/head-only, prompt-hard-coded, and
maximum-instead-of-minimum counterfactuals are each rejected by an explicit
witness. See
[43_adversarial_semantic_checks.txt](evidence/43_adversarial_semantic_checks.txt).
This operational and value-sensitivity work enforces the distinction between
an honest definition and an execution-bypassing convenience.

## Deterministic Stage 4 and target identity

The Stage 4 input manifest contains the same six definitions and no
operational or proved-derived entries. Its `source_rules` list—the list of
independently classified domain lemmas eligible for obligations—is empty.
`generated/obligation-map.json` has:

- `source_rules: []`;
- `obligations: []`;
- `trust_parameters: []`.

Its SHA-256 is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
exactly the generator-manifest value. The empty source/obligation order is an
exact bijection, the generator and export result both record obligation count
zero, and there are consequently no omitted, duplicated, irrelevant,
weakened, or vacuous conjuncts.

Independent calls to the trusted expected-target and observed-target routines
both return null. This agrees with `generator-manifest.json`,
`/audit-input.json`, and the empty `Lemmas.lean` namespace. There is no theorem
declaration elsewhere in the generated project. The generated recursive Lean
definitions in `Func.lean` preserve the singleton and recursive K equations;
they do not introduce a substitute target. The direct generated-source
inspection is in
[46_generated_definition_and_no_target_inspection.txt](evidence/46_generated_definition_and_no_target_inspection.txt).

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required frozen workspace, Stage 3 manifest, Stage 4 generation, and
trusted toolchain lock. The fresh result is:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0, empty-output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, output SHA-256
  `01533e71270efbf65bdb5becaf398cceef083386b4986c377ee2721805904f5d`;
- obligation count 0;
- target null;
- generated tree unchanged;
- designated sorry count 0;
- 47 generated base trust declarations, exactly reconciled with the Stage 4
  trust inventory.

The fresh returned document is byte-for-byte equal as a JSON value to the
signed preflight record. It is preserved in
[36_fresh_check_generation_pass.txt](evidence/36_fresh_check_generation_pass.txt),
with the explicit reconciliation in
[45_preflight_reconciliation_and_lean_scan.txt](evidence/45_preflight_reconciliation_and_lean_scan.txt).
The 47 base declarations cannot establish or weaken a Stage 5 result here:
there is no obligation theorem and no candidate proof.

The first two preflight attempts exposed an audit-sandbox runtime issue rather
than an artifact failure: Lean 4.22 reads `/proc/<numeric-pid>/exe`, while this
sandbox exposes only the equivalent `/proc/self/exe`. A narrowly scoped
preload shim redirected only that self-executable lookup. After the shim, Lean
reported the pinned 4.22.0 commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the unmodified trusted
checker passed. The failed attempts, diagnosis, exact shim source, and
successful version check remain in evidence files 09–36. Neither mounted
inputs nor generated sources were changed.

## Final judgment

The protected Stage 3 record accounts for the entire canonical local rule
inventory and classifies all six entries correctly. There is no true domain
lemma to export. The selected `KLEAN_NO_OBLIGATIONS` status, absence of a
generated target, and absence of Stage 5 are therefore substantively correct,
not merely self-consistent metadata. Producer provenance, deterministic
structure, hashes, clean build, obligation bijection, and target identity all
pass independent checks.

VERDICT: PASS
LEGITIMACY: LEGIT
