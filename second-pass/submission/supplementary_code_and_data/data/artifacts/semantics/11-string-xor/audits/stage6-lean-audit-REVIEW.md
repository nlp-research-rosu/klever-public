# Independent audit: HumanEval `11-string-xor`

## Outcome

The protected Stage 3 classification is correct, the selected deterministic
Stage 4 generation is structurally and mathematically faithful to that
classification, and `KLEAN_NO_OBLIGATIONS` is justified. The independently
classified `DOMAIN_LEMMA` set is genuinely empty. There is no generated target
and, consistently with `CLASSIFICATION_ONLY`, no Stage 5 proof candidate.

Audit scope:

- condition: `semantics`
- semantics mode: `SUPPLIED_SEMANTICS`
- launcher mode: `CLASSIFICATION_ONLY`
- frozen problem: `11-string-xor`

All mounted candidate/provenance content, including prior reviews and logs, was
treated as untrusted evidence. Conclusions below come from fresh hashing,
trusted inventory/preflight tooling, frozen-source inspection, operational
semantic witnesses, and a deterministic generator replay.

## Producer-source provenance gate

This gate passed before Stage 4 was judged.

| Item | Independently observed SHA-256 |
|---|---|
| `/reference/generation-tools/klean_export.py` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `/reference/generation-tools/klean.py` | `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1` |
| producer bundle, using the launcher’s trusted tree-hash algorithm | `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c` |

Both file hashes match `generator-manifest.json` and
`source-manifest.json`. The bundle hash matches `/audit-input.json`. The
generator image ID is consistently
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`
in the generator manifest, source manifest, and the image-key component of the
producer path recorded in `/audit-input.json`. The bundle contains exactly the
two producer files and `source-manifest.json`.

Other launcher-bound hashes also match:

| Artifact | Observed and expected SHA-256 |
|---|---|
| Stage 1 tree, launcher algorithm | `743a5166687956a5758e72be349e345ae88002ffab9e7b6c39d8b0d569539b63` |
| Stage 1 export tree, Klean algorithm | `1aba3c0e9d77a4d580993f6c6a3bbcfaa34e3eadad9fd7ba9f1e66b93b4bfcee` |
| `lemma-discovery.json` | `c524f5c42c97ca795b7fa77878a5dd7db118820d108e2f56c02d96f1d4c1807f` |
| selected Stage 2 tree | `0425bbcc91cadf84b731f77ab9fa5a0b39da1115a4df500c906cb4b52ab52e3c` |
| selected Stage 4 tree | `d49890923ce962cb9a9019e6441aa7c9197de5db97aa927b4f2219ada3df1e7c` |
| generated project tree | `3553ce22a41487aaabb785935fbee17b25ee50dc4836b9773d7f68cacd82aa6b` |

The complete Stage 1 regular-file set and every per-file source hash match
`stage1_source_hashes` in `/audit-input.json`.

## Stage 1 inventory reconstruction and Stage 3 bijection

I invoked `tools.k_rule_inventory.inventory_verification` from
`/reference/tools` on the frozen `/reference/k-proof` workspace. The local
verification-module closure is exactly one module:
`STRING-XOR-VERIFICATION`. It contains 19 rules.

The independently reconstructed inventory hash is:

`af05bd2b71be7a946c9ecf095978c233bf3e947a404302b7aeacf34399818916`

For every entry, the trusted reconstruction recomputed the source span,
normalized source, normalized SHA-256, and
`source_rule_id = "rule-" + normalized_sha256`. Comparison with the protected
Stage 3 manifest established all of the following:

- exactly 19 canonical entries and exactly 19 classifications;
- no canonical or classified duplicate ID;
- no omission or extra ID;
- identical ordered identities, so no reordering;
- exact inventory hash; and
- each recorded identity binds its freshly recomputed normalized hash.

The complete reconstructed text, spans, hashes, IDs, classifications, and
rationales are in
[03_inventory_reconstruction.log](/audit-output/evidence/03_inventory_reconstruction.log).

## Independent classification judgment

Every entry is a `DEFINITION`. This is not inferred from the protected
rationales: it follows from the frozen rule heads, their roles in `spec.k`, and
the supplied operational semantics.

| # | Source rule ID | Span | Classification and reason |
|---:|---|---:|---|
| 1 | `rule-199ce5880ece2ffb12808eff7fef493bd984e1a076cd0e8d4b343706610da6dd` | 9 | `DEFINITION`: introduces `binaryCode`, the ASCII 48/49 predicate. |
| 2 | `rule-a148568eb04c7f9b8870ff300eaedf75c27d7157f87329038363c581ba31e006` | 12–13 | `DEFINITION`: equal-input guarded equation for fresh summary `xorCode`, yielding 48. |
| 3 | `rule-fe604a49861f69b3d97a975621261928274be9ca20eacdb377de3f12c4cd20be` | 14–15 | `DEFINITION`: unequal-input guarded equation for `xorCode`, yielding 49. |
| 4 | `rule-62aca2024c4118a16e877ed708bc7768249c5c00041d1b722b67419785a42cb7` | 18 | `DEFINITION`: first-empty base equation for `xorAcc`. |
| 5 | `rule-3873758979b4fe1f32c7b6c9f3766c8a77b9e2692da5dd9a167d7ec6ed480a65` | 19 | `DEFINITION`: second-empty base equation for `xorAcc`. |
| 6 | `rule-5927925fd64b560eda4a130550ad28115a8190603ec3ef402ce86fd2e7f16246` | 20–21 | `DEFINITION`: structural recurrence for `xorAcc`, appending one summarized XOR code and descending on both tails. |
| 7 | `rule-b95fbff73db146c39988a02bbcbb098c77c0429f2871f9f6ce9412cd30eb2a41` | 25 | `DEFINITION`: empty base equation for `binaryCodes`. |
| 8 | `rule-0a4b0a280fe4a4a35fd65b3556363daab4e64279cb451ed33f6978a946f2f288` | 26–27 | `DEFINITION`: structural recurrence for `binaryCodes`. |
| 9 | `rule-51eed43ea34ea2b88fc0ee347ba2ce190ad10bf7d39e47c22ce25b918d176bd8` | 33 | `DEFINITION`: first-empty base equation for loop-state summary `xorLastX`. |
| 10 | `rule-a38734cd4f874be55b9ca33cb03b46d5c734929e291f977a284b556b320c7a24` | 34 | `DEFINITION`: second-empty base equation for `xorLastX`. |
| 11 | `rule-7fbbae800178ce2c9ba1863b427c2174c299cc3ade1339dce972aa9f67e5e909` | 35–36 | `DEFINITION`: recurrence recording the current first head in `xorLastX`. |
| 12 | `rule-7f5cb64a2e98293475868861131ad7741bf1e6a094fbf0ee0640e2a0798bb97b` | 37 | `DEFINITION`: first-empty base equation for loop-state summary `xorLastY`. |
| 13 | `rule-27fb8fe751825dffe32c8718d119f49236783d0d07bcd8a5db653b1dea712d16` | 38 | `DEFINITION`: second-empty base equation for `xorLastY`. |
| 14 | `rule-0c567126c3b88db4eaddf41bd503995b9c2bb3ac347550f17551712ad2763a7b` | 39–40 | `DEFINITION`: recurrence recording the current second head in `xorLastY`. |
| 15 | `rule-b29ef2baa281c5fa26870dd0bdec73534d8ce1dfb5f50b7530fc079eb66befb8` | 44 | `DEFINITION`: named proof term expanding to the exact tuple loop target. |
| 16 | `rule-fb6d7f05a768ed8021b86cfe5116ba4f3a3285bc89b5cb1b77d93545fe5b3e63` | 47–50 | `DEFINITION`: named proof term expanding to the exact loop body. |
| 17 | `rule-9038158948b425b3a65b4356422181488831c1971604f53f17abfdf852273664` | 53–60 | `DEFINITION`: named proof term expanding to the complete translated function body. |
| 18 | `rule-7ca33bffe28bd24537015e6017062942fea10d0e7b29d0e6493564505573088b` | 63–64 | `DEFINITION`: named closure value with exact parameters, body, and defining scope. |
| 19 | `rule-ddfff0b94e57e746b0fc84a9f6b2e7f71e126aed256bc39b9680c789117a7846` | 67–70 | `DEFINITION`: named module term expanding to the exact translated module. |

None is an `OPERATIONAL_RULE`: none matches or changes a K configuration,
execution continuation, store, or observation. The first 14 introduce fresh
predicates or structural summaries; the final five are named proof
terms/macros. None is a `PROVED_DERIVED_LEMMA`: `verification.k` contains no
local claims that first prove one of these exact rules in a module omitting it.
None states a mathematical property of an already-defined symbol, so none is a
`DOMAIN_LEMMA`. Every inventory attribute list is empty; in particular there is
no `[simplification]` rule.

### Mathematical and operational alignment

The classifications are also relevant and truthful for the frozen program:

- `binaryCode`/`binaryCodes` precisely express the claim’s binary-string
  precondition.
- The supplied `zip` semantics pairs one-character strings and stops at the
  shorter input (`builtins.k` 162–174).
- The supplied loop semantics binds the tuple target, evaluates the body, and
  recurs on the remaining zip object (`controls.k` 62–74 and `tuple.k` 30–57).
- Supplied string `==` compares code sequences and string `+` concatenates them
  (`str.k` 19–26); supplied `if` semantics selects the matching branch
  (`controls.k` 50–54).
- Therefore `xorAcc` exactly computes the result prefix through the shorter
  input. `xorLastX` and `xorLastY` exactly account for the observable loop-scope
  values needed by the invariant, including the initialized empty values when
  the loop never runs.
- The five named terms reproduce the translated `solution.mpy` loop target,
  body, closure, and module rather than replacing operational execution.

A fresh LLVM compilation of the supplied semantics succeeded. Independent
ground witnesses covered empty input, equal and unequal bits, both
unequal-length directions, longer inputs, and returned traces exposing final
`x`/`y`; they all ended with `<exit-code> 0`. A counterfactual that changed the
equal branch to append `"1"` was rejected on input `("0","0")` with
`AssertionError` and exit code 1. These tests are finite sensitivity evidence;
the classification judgment itself rests on the source recurrences and
operational rules above.

Thus the true independently classified domain set is empty.

## Deterministic Stage 4 generation

### Trusted preflight rerun

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required inputs:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`
- `/reference/klean-toolchain.lock.json`

The returned evidence is:

- status: `KLEAN_NO_OBLIGATIONS`
- Stage 1 hash:
  `1aba3c0e9d77a4d580993f6c6a3bbcfaa34e3eadad9fd7ba9f1e66b93b4bfcee`
- Stage 3 hash:
  `c524f5c42c97ca795b7fa77878a5dd7db118820d108e2f56c02d96f1d4c1807f`
- generated-tree hash:
  `3553ce22a41487aaabb785935fbee17b25ee50dc4836b9773d7f68cacd82aa6b`
- obligation count: `0`
- target: `null`
- designated sorry count: `0`
- trust declarations: `47`
- `lake clean`: exit 0, empty output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, complete output hash
  `04c822f766bc0e57d3332ffce19a0630b495c40882faf53e2c83152d3542e2f4`

The build output hash is identical to the immutable recorded preflight.

The first direct rerun exposed an audit-container path-detection issue: Lean’s
application-path routine consulted `/proc/<namespace-pid>/exe`, while this
container exposes the executable through `/proc/self/exe`. That failed before
compilation and is preserved in the evidence. A narrow, source-recorded
`readlink` compatibility shim mapped only that path form to `/proc/self/exe`;
with the pinned direct Lean 4.22.0 toolchain, the same trusted preflight then
passed. The shim did not alter or write any mounted input. Its source, failed
attempt, successful rerun, and complete build output are all preserved.

### Independent manifest and obligation audit

The protected discovery has no `DOMAIN_LEMMA` entry. Independently checking all
Stage 4 sidecars found:

- `input-manifest.json.source_rules = []`;
- `obligation-map.json.source_rules = []`;
- `obligation-map.json.obligations = []`;
- `obligation-map.json.trust_parameters = []`;
- generator and export obligation counts are both zero;
- obligation-map SHA-256 is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  exactly as recorded;
- the source-rule and obligation ID sequences are equal, unique, and empty;
- there is no `True`/vacuous conjunct; and
- all 19 definitions appear in the input manifest in canonical inventory order.

The fixed target identity is consistently absence of a target:

- generator manifest target: `null`;
- audit-input target: `null`;
- recorded and rerun preflight target: `null`;
- trusted `target_statement` parser result: `None`;
- trusted expected-target construction: `None`; and
- `Klean11StringXor/Lemmas.lean` contains an empty namespace with no target
  declaration.

There is therefore no omitted, duplicated, weakened, irrelevant, or vacuous
domain obligation and no changed generated target.

### Independent deterministic replay

I copied the hash-verified producer sources byte-for-byte to a scratch
`tools` directory and replayed export from the frozen Stage 1 workspace,
protected Stage 3 manifest, generator image ID, problem ID, and pinned
toolchain lock.

The replay returned `KLEAN_NO_OBLIGATIONS` and reproduced:

- the exact generated tree hash
  `3553ce22a41487aaabb785935fbee17b25ee50dc4836b9773d7f68cacd82aa6b`;
- a byte-for-byte identical generated project (`diff -r` empty);
- byte-identical `generator-manifest.json`;
- byte-identical `trust-inventory.json`; and
- byte-identical `export-result.json`.

The replayed input manifest differs only in the absolute mount prefix recorded
for `required_k_files` (`/reference/k-proof` in the audit replay versus
`/frozen-k` in the generator container). All source and tree hashes, inventory,
classes, source rules, generated files, and result sidecars agree.

## Stage 5

Stage 5 is correctly absent. `AUDIT_MODE` and `/audit-input.json` both select
`CLASSIFICATION_ONLY`; the Lean workspace/invocation and Stage 5 result fields
are null, `/candidate` is absent, and the generated target is null. Accordingly
there is no candidate target to rebuild, no `Proof.final`, no candidate
parameter bridge, and no candidate axiom list to audit. Running
`#print axioms Proof.final` or inventing a candidate in this mode would be
inconsistent with the selected zero-obligation status.

The 47 Stage 4 trust declarations are structurally checked and allowlisted
Klean executable-boundary declarations; preflight independently rejects
proposition trust and found no generated proof hole. With no target theorem,
they do not constitute a Stage 5 proof or an escape from one.

## Evidence index

- Exact core commands:
  [COMMANDS.md](/audit-output/evidence/COMMANDS.md)
- Producer hashes and image binding:
  [01_producer_provenance.log](/audit-output/evidence/01_producer_provenance.log)
- All launcher/source/tree hashes:
  [02_all_input_hashes.log](/audit-output/evidence/02_all_input_hashes.log)
- Full canonical inventory and bijection:
  [03_inventory_reconstruction.log](/audit-output/evidence/03_inventory_reconstruction.log)
- Per-rule independent classification:
  [04_independent_classification.md](/audit-output/evidence/04_independent_classification.md)
- Initial environment-level preflight failure:
  [05_preflight_rerun.log](/audit-output/evidence/05_preflight_rerun.log)
- Successful trusted preflight with complete output:
  [06_preflight_rerun_compat.log](/audit-output/evidence/06_preflight_rerun_compat.log)
  and [preflight-returned.json](/audit-output/evidence/preflight-returned.json)
- Deterministic export replay:
  [07_stage4_generation_replay.log](/audit-output/evidence/07_stage4_generation_replay.log)
- Byte/hash comparison of replay:
  [08_stage4_replay_comparison.log](/audit-output/evidence/08_stage4_replay_comparison.log)
- Operational witnesses and rejected mutation:
  [09_operational_semantics_witnesses.log](/audit-output/evidence/09_operational_semantics_witnesses.log)
- Independent obligation/target checks:
  [10_stage4_structure.log](/audit-output/evidence/10_stage4_structure.log)
- Replay-only absolute input-path difference:
  [11_replay_input_manifest_path_diff.log](/audit-output/evidence/11_replay_input_manifest_path_diff.log)

VERDICT: PASS
LEGITIMACY: LEGIT
