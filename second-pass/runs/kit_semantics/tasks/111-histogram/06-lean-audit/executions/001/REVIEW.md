# Independent Stage 3/4 audit: HumanEval 111-histogram

## Result

The protected Stage 3 classification is complete and mathematically appropriate, and the selected deterministic Stage 4 generation is structurally and semantically consistent with it. The independently reconstructed domain-lemma set is genuinely empty. Therefore `KLEAN_NO_OBLIGATIONS`, a null generated target, and the absence of Stage 5 are correct.

This was a `CLASSIFICATION_ONLY` audit. Both `AUDIT_MODE` and the signed `/audit-input.json` resolution say `CLASSIFICATION_ONLY`; the condition is `kit-semantics` and the semantics mode is `SUPPLIED_SEMANTICS`. `/candidate` is absent, the Lean-workspace and Lean-invocation hashes are null, and the Stage 5 result is null. No Stage 5 proof or `#print axioms Proof.final` check is applicable.

I treated the mounted Stage 1/2/3/4 material, including prior reports and logs, only as evidence. I did not rely on any prior verdict or classification. Classification used the behavior-based proof-extension standard: a rule that merely names or recursively defines a value is a definition; a rule that replaces source execution is operational; and a theorem-shaped simplification is not accepted as a definition merely because it has a convenient name.

## Producer provenance gate

The required producer-source gate passed before any Stage 4 judgment:

- `/reference/generation-tools/klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `/reference/generation-tools/klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`
- generator image: `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
- complete producer-source tree: `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`

The two file hashes agree exactly with both `source-manifest.json` and `generator-manifest.json`. The image ID agrees between those two manifests, and its digest without the `sha256:` prefix is the final component of the producer-source path recorded in `/audit-input.json`. The producer bundle contains exactly `klean_export.py`, `klean.py`, and `source-manifest.json`. This is not an infrastructure-error case.

Raw evidence: `evidence/04-source-manifest-json.txt`, `evidence/05-generator-manifest-json.txt`, `evidence/06-generation-producer-sha256.txt`, and checks `producer_*` in `evidence/133-independent-integrity-check-final.txt`.

## Frozen-input and manifest integrity

An independent checker recomputed the signed resolution and every mounted artifact/source/tree binding used by this audit. It performed 68 comparisons with no failure, including all 770 individually recorded Stage 1 regular-file hashes. Important recomputed values are:

| Object | Recomputed SHA-256 |
|---|---|
| Signed resolution envelope | `92d6915db47a8f365f2adaeab4477330dc2666af297c019dbc53a7d0c7f1c3c6` |
| Stage 1 artifact tree | `6efc5bbf9dba1984bce4ba4acfd3dd2e56cddedf4189d59c6b9971881b4f4dad` |
| Stage 1 deterministic-export tree | `14635087931e3525361e58b70a8b501396d4e67e12d4fb77df93f78eaf897bba` |
| `verification.k` | `5c7548ae1a4b8a6f5e2386578f0950e62baed1b2b00a8a40d94e0ddaf54b6157` |
| Selected Stage 2 audit tree | `6ab85383855f069111bb1e35ad71a4a48bd4cbef23965cb63573b6327b9a2041` |
| Stage 3 discovery file | `4a2a92c11ecbd72497a0831af016ab197c44d4082ae34f4abf892b8b21eeec34` |
| Reconstructed rule inventory | `8355762f852bbf96edc58dc881c1320a840f84700bf8f961adeefc1e834f1d0d` |
| Selected Stage 4 generation tree | `54d4cd603db1ec17d32b367603b863354f1c11de0f9d3881ff50f0f0cbddc41a` |
| Generated project tree | `af62255565b2c58b02a03bd295f46f83b9b3acf90a4e9e9c8a73333202b62497` |
| Generated obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Generated trust inventory | `47d181c0cd3302889bb75f5c2b6bd41324d7f2f44f8d9e3f156aca1c8bbb9096` |

The Stage 4 toolchain manifest also equals `/reference/klean-toolchain.lock.json` exactly. The generator/input/export/preflight manifests bind the same Stage 1 tree, Stage 3 file, inventory, generated tree, obligation map, and trust inventory. The Stage 4 and Stage 2 selection hashes match the mounted trees, and the preflight embedded in `/audit-input.json` equals the mounted `preflight.json`.

Raw evidence: `evidence/133-independent-integrity-check-final.txt`; checker source: `evidence/independent_integrity_check.py`.

## Rule-inventory reconstruction

I ran the trusted `/reference/tools/k_rule_inventory.py` implementation directly on the frozen `/reference/k-proof`. It selected `VERIFICATION` from the frozen `prove.sh` and reconstructed the local module closure, in source order, as:

1. `COUNT-SUMMARY`
2. `VERIFICATION`

The closure contains exactly nine rules. For every row below, the exact `source_rule_id` is `rule-` followed by the displayed normalized SHA-256.

| # | Module and source span | Normalized SHA-256 | Independent classification | Semantic role |
|---:|---|---|---|---|
| 1 | `COUNT-SUMMARY:8` | `0e257a4ad15e0e26ec2d40a2bdb7104348f30fb607cec9c8268016c2df32ff5c` | `DEFINITION` | Empty-sequence base of `countHistogramCode`; returns its accumulator. |
| 2 | `COUNT-SUMMARY:9-16` | `e835c344071adb5cf8f06eb17d251a967ac9d5ae2edaa67d3f42ef596bfd8015` | `DEFINITION` | Constructor recurrence of `countHistogramCode`; increments exactly on a matching code and descends on the tail. |
| 3 | `COUNT-SUMMARY:20` | `d32dc5006d7e4ee002713099c087fb613bfad82730d2c2e21c54afd56d0a067b` | `DEFINITION` | Empty-sequence base of the named input-domain predicate. |
| 4 | `COUNT-SUMMARY:21-23` | `9ef0332db5a72b4f18503c215dfb40222289c5651ddbef6e2e7fad578292005c` | `DEFINITION` | Constructor recurrence of `validHistogramInput`; checks space or ASCII lowercase and descends. |
| 5 | `VERIFICATION:33` | `bcb3143ad88bf081cf786ab5158df364f6725bdc3a35484a2d7d5de476120b2f` | `DEFINITION` | Empty-suffix base of the maximum-count accumulator fold. |
| 6 | `VERIFICATION:34-46` | `16a917fc8d42da5cc2fc1a4a7bba75e65b7999838dbe9a9daa88ba945f4a6076` | `DEFINITION` | Constructor recurrence of `maxHistogramCount`; skips space, counts the current code, and performs the source's strict-maximum update. |
| 7 | `VERIFICATION:54-60` | `0547ef9d878306e0708cee9245a6b3126d85c893b76a24cf3d2ccc4522c9ba63` | `DEFINITION` | Empty-suffix base of `buildHistogram`; packages the accumulated parallel dictionary sequences. |
| 8 | `VERIFICATION:61-84` | `873fc726e8c4c1db886845f8ff0875b9c7bb782452d1d8f3d3e5667015b23e6b` | `DEFINITION` | Constructor recurrence of `buildHistogram`; skips space and uses the supplied dictionary update helpers exactly when the count equals the maximum. |
| 9 | `VERIFICATION:87-93` | `385829d23edb7fb14f9b963a8ed360edd5ebb107deade4c540203c41b439e4a4` | `DEFINITION` | Named result term composing the maximum and dictionary folds from their initial accumulators. |

The reconstructed identities are unique and occur in exactly the same order in `/reference/lemma-discovery.json`. The discovery inventory digest is the reconstructed digest `8355762f…`, so omitted, extra, duplicated, reordered, or changed rules would have been detected. Enriching the independently reconstructed records with Stage 3's classification/rationale yields the Stage 4 `input-manifest.json` `definitions` list byte-for-structure; there are no unaccounted classifications.

Raw evidence: `evidence/12-verification-k.txt`, `evidence/16-reconstructed-rule-inventory.txt`, `evidence/128-trusted-stage3-contract-check.txt`, and the `classified_*`/`enriched_definition_bijection` checks in `evidence/133-independent-integrity-check-final.txt`.

## Independent classification and operational judgment

All nine entries really are definitions, not disguised domain lemmas:

- Each left-hand side is headed by a named proof-local function. Eight rules are constructor base/step equations; the ninth defines a named result term by composition.
- None has a `<k>` cell, matches a source AST term, intercepts a call, or changes any operational cell. Thus none is an `OPERATIONAL_RULE` or operational bridge.
- None states a proposition about the returned histogram, asserts maximum-frequency correctness, or rewrites the desired postcondition. `histogramResult` only names a value; the separate `[histogram]` reachability claim is what connects complete source execution to that value.
- No inventory rule has a `simplification` attribute (indeed every reconstructed `attributes` list is empty), so there is no simplification rule hidden under an impermissible category.
- No entry claims `PROVED_DERIVED_LEMMA`; consequently there is no same-rule derivation claim to accept without the required proof-before-use sequence.

The definitions match the frozen source and supplied operational semantics:

- String iteration rewrites `str(iCons(C,R))` to a one-character string yield plus the remaining string. The `For` semantics consumes those yields through `#loop`, binds the target, executes the body, and resumes the remaining iterator.
- The source's inner loop increments `count` precisely when the candidate one-character string equals the current letter. `countHistogramCode` is exactly that accumulator recurrence.
- The first outer loop ignores space and updates `max_count` only under strict `>`. `maxHistogramCount` has the same branch order, original-input count, strict comparison, and suffix descent.
- The second outer loop ignores space and assigns `result[letter] = count` exactly under equality with `max_count`. `buildHistogram` performs that test and uses `dPutK`/`dPutV`, whose supplied semantics preserves first key position while updating the parallel value at that key. This agrees with the source dictionary behavior, including repeated maximum-frequency letters.
- `validHistogramInput` is not a theorem about histogram values. It is the recursive definition of the main claim's domain and matches the HumanEval contract, “space separated lowercase letters,” including the empty string.

Boundary cases agree: empty input and all-space input return the empty dictionary; a single letter returns count one; tied maxima retain every tied non-space letter; repeated keys update rather than duplicate. An independent executable model compared the direct nested-loop source algorithm with the five K summary recurrences on every string over `{space,a,b}` through length 6 (1,093 inputs) and found zero mismatches. It also distinguished counterfactual mutations that counted spaces in the maximum, changed the build equality to strict greater-than, or returned a constant empty dictionary. This finite check supports, but does not replace, the structural/inductive operational judgment above.

Raw evidence: source and claim in `evidence/17-stage1-spec-k.txt`, `evidence/17b-stage1-spec-k.txt`, `evidence/18-source-solution-py.txt`, and `evidence/127-human-eval-prompt.txt`; semantics in `evidence/21-semantics-dict-k.txt`, `evidence/23-semantics-str-k.txt`, `evidence/33-loop-semantics-detail.txt`, `evidence/37-function-semantics-detail.txt`, and `evidence/38-call-semantics-detail.txt`; model results in `evidence/116-summary-model-check.txt`.

### Domain-set conclusion

The independently reclassified domain-lemma set is empty. It is not empty because a mathematical postcondition lemma was mislabeled: there simply is no theorem-shaped or simplification rule in the local verification-module closure. The five named functions and their nine equations are computation/summary definitions. Therefore Stage 4 correctly has no lemma obligation to export.

## Stage 4 obligation bijection and target identity

The following independently observed sets are all exactly empty:

- `input-manifest.json.source_rules`
- `obligation-map.json.source_rules`
- `obligation-map.json.obligations`
- `obligation-map.json.trust_parameters`
- independently classified `DOMAIN_LEMMA` rules

The generator manifest, export result, mounted preflight, and fresh preflight all report obligation count zero and status `KLEAN_NO_OBLIGATIONS`. There can be no omission, duplicate, reordering, irrelevant obligation, weakened conjunct, or vacuous conjunct in a bijection of five independently confirmed empty sets.

Target identity is likewise exact:

- `generator-manifest.json.target`: null
- `/audit-input.json` signed `resolution.target`: null
- mounted `preflight.json.target`: null
- fresh `check_generation` result: null
- independent `klean_export.target_statement(generated)`: `None`

The generated root module contains only imports, and `Klean111Histogram/Lemmas.lean` contains an empty namespace. A source search found no theorem, lemma, target declaration, or target-like name in any generated Lean file. Thus Stage 4 did not replace the absent target with `True`, a vacuous conjunction, or another theorem. The fixed generated-project hash remains `af622555…` before and after preflight.

The generated project has 42 recorded non-propositional trust declarations for executable collection/equality hooks. The fresh preflight reconciled them exactly with `trust-inventory.json`, rejected proposition trust, and found zero `sorry` declarations. Because there is no generated proposition or Stage 5 proof, these executable hooks cannot be used to discharge a hidden theorem. A separate search found no `sorry`, `admit`, or `unsafe` token.

Raw evidence: `evidence/13-input-manifest-json.txt`, `evidence/14-obligation-map-json.txt`, `evidence/15-export-result-json.txt`, `evidence/117-generated-root-module.txt`, `evidence/118-generated-target-search.txt`, `evidence/119-generated-forbidden-search.txt`, `evidence/121-trust-inventory-json.txt`, and `evidence/122-generated-lemmas-lean.txt`.

## Required fresh preflight

Exact successful command:

```sh
LD_PRELOAD=/audit-output/evidence/lean-proc-exe-shim.so \
PYTHONPATH=/reference \
python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

The trusted checker copied the generated project into its own fresh temporary directory, ran `lake clean`, then `lake build`. Results:

- `lake clean`: exit 0, empty-output SHA-256 `e3b0c442…`
- `lake build`: exit 0, output SHA-256 `7a01980a…`
- built modules: Prelude, Sorts, Inj, Lemmas, Func, Rewrite, and root package
- returned status: `KLEAN_NO_OBLIGATIONS`
- returned obligation count: 0
- returned target: null
- returned generated tree: `af622555…`
- returned trust declaration count: 42
- returned designated sorry count: 0

The first attempt without the preload is preserved in `evidence/39-rerun-check-generation.txt`; it failed before compilation because this container's `/proc` mount does not expose the PID namespace value returned by `getpid()`. Lean 4.22 resolves its executable through `/proc/<pid>/exe`, confirmed in `evidence/100-app-path-disassembly.txt`, while `/proc/self/exe` remains available. The audit-local source-recorded shim redirects only matching `/proc/*/exe` `readlink` calls to `/proc/self/exe`. With it, the pinned binary reports Lean 4.22.0, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock and generator manifest. The shim changes neither mounted evidence nor generated source and has no effect on Lean elaboration or kernel checking.

Complete successful output: `evidence/110-rerun-check-generation-success.txt`. Shim source/build/version evidence: `evidence/lean-proc-exe-shim.c`, `evidence/106-build-lean-proc-shim-success.txt`, `evidence/107-lean-proc-shim-final-sha256.txt`, and `evidence/108-lean-version-with-shim.txt`.

## Stage 5 disposition

Stage 5 must not exist for a legitimate zero-domain-obligation result. It does not: `/candidate` is absent, all signed Lean paths/hashes and the Stage 5 result are null, and there is no generated target to prove. No candidate build, target-shadowing audit, `Proof.final`, axiom print, or operational-parameter bridge exists or is applicable.

## Evidence index

`evidence/COMMANDS.md` maps the principal exact commands to raw transcripts. All numbered evidence files are raw command transcripts; the two independent checker sources are preserved alongside their results.

VERDICT: PASS
LEGITIMACY: LEGIT
