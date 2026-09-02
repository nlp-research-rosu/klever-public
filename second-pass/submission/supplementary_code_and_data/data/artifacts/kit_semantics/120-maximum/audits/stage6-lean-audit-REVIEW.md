# Independent audit: HumanEval 120-maximum

## Scope and result

I independently audited Stage 3 classification and deterministic Stage 4 generation for condition `kit-semantics` in `SUPPLIED_SEMANTICS` mode. Both `AUDIT_MODE` and `/audit-input.json` say `CLASSIFICATION_ONLY`. The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, as required. Stage 5 proof checks therefore do not apply.

I treated every mounted candidate/provenance document, comment, log, and prior verdict as untrusted evidence. The conclusions below come from frozen source, trusted inventory/preflight code, independently recomputed hashes, and a fresh build.

## Producer-source gate

I performed the producer-source check before judging Stage 4.

- `/reference/generation-tools/klean_export.py` hashes to `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- `/reference/generation-tools/klean.py` hashes to `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.
- Both hashes exactly match `source-manifest.json` and `generator-manifest.json`.
- The generator image ID is `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` in both manifests. Its digest component also exactly matches the immutable producer-source directory named in `/audit-input.json`.
- The producer bundle tree hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, exactly matching `/audit-input.json`.

Thus the required producer source is present and provenance-consistent; there is no producer-source `AUDIT_ERROR`.

Primary raw evidence: `evidence/01-producer-and-generation-manifests.txt`, `evidence/16-producer-source-identity-and-generation-logic-index.txt`, `evidence/17-generation-time-producer-relevant-source.txt`, and `evidence/23-stage4-independent-manifest-bijection-checks.txt`.

## Inventory reconstruction

Using `/reference/tools/k_rule_inventory.py` directly with `PYTHONPATH=/reference`, I reconstructed the local closure of the verification main module selected by `prove.sh`.

- Main module: `VERIFICATION`.
- Local verification-module closure: only `VERIFICATION`. Its `MPY` import is supplied by the external frozen semantics, not another module locally declared in `verification.k`.
- Canonical inventory size: one rule.
- Canonical inventory hash: `a5c14e04fab2c20c7620b8979b4cc4b4eb2232e21babb1d076942b24e60bf083`.

The sole entry is:

- `source_rule_id`: `rule-fbc012b3ef8f9433c0af203532037974f8c0298dcbdd8c0b25f3729ff47074f9`
- Module and span: `VERIFICATION`, lines 9–14.
- Attributes: none.
- Independently normalized source hash: `fbc012b3ef8f9433c0af203532037974f8c0298dcbdd8c0b25f3729ff47074f9`.

I re-extracted lines 9–14, normalized them with the canonical whitespace rule, recomputed their SHA-256, recomputed the `rule-<hash>` identity, and recomputed the canonical JSON inventory hash. All match.

The comparison with `/reference/lemma-discovery.json` is bijective and ordered: one canonical entry, one classified entry, identical ordered identity, no duplicate in either set, no omission, no extra rule, and matching inventory hash. The trusted Stage 3 contract validator also accepts the manifest.

The full imported K file closure was independently recomputed as 25 ordered files (24 supplied-semantics files plus `verification.k`), exactly matching `input-manifest.json`.

Primary raw evidence: `evidence/02-trusted-tooling-and-inventory-code.txt`, `evidence/03-canonical-inventory-and-stage3-contract.txt`, `evidence/20-comprehensive-hash-and-inventory-reconciliation.txt`, and `evidence/27-recomputed-full-k-file-closure.txt`.

## Independent classification judgment

I agree with the sole classification: `DEFINITION`.

Line 8 introduces the fresh named summary `maximumResult(ValSeq, Int) : Val`. The rule at lines 9–14 expands that name to:

```text
doSlice(list(sortVS(VS)), someB(vsLen(VS) -Int K), noB, noB)
```

This is the exact supplied-K representation of the source expression `sorted(arr)[len(arr) - k:]`:

- `sorted(list(VS))` operationally allocates `list(sortVS(VS))` (`sort.k`, lines 34–37).
- `len(list(VS))` reduces through `seqLen` to `vsLen(VS)` (`builtins.k`, lines 19–24; `core.k`, lines 221–225).
- A slice with the computed lower bound and omitted upper/step bounds evaluates to `someB(vsLen(VS) -Int K), noB, noB`, then allocates `doSlice` (`subscript.k`, lines 43–65).
- The frozen source and the loaded function body in the claim contain precisely that `sorted`/length-minus-`k`/slice expression. The post-state names its value with `maximumResult`.

The rule contains no `<k>` cell or other configuration cell, does not replace execution, asserts no independent property (ordering, maximum membership, result length, or similar), and does not encode the requested human-facing correctness fact. It is an unconditional, nonrecursive name for the exact operational summary term. It is therefore a genuine definition, not an `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or disguised `DOMAIN_LEMMA`.

There are no local `simplification` rules, so the requirement that every such rule be a `DEFINITION` or `DOMAIN_LEMMA` is satisfied. There are no claimed derived lemmas requiring an earlier bridge-free proof. The independently classified true domain-lemma set is empty.

Primary raw evidence: `evidence/04-frozen-source-spec-and-relevant-semantics-index.txt` and `evidence/19-operational-semantics-trace.txt`.

## Hash and manifest accounting

I independently recomputed every resolution hash in `/audit-input.json`:

- Stage 1 workspace tree: `6bf4dee40257d41f6a5d955906c9b770bd6cca4b4a09cc9ea93a4fcd30d1d8a8`.
- Stage 1 export tree: `4298407d2a64117aa1d2d02cab660a96589c0c6a2da5866ce662138f135c86ad`.
- Stage 3 manifest: `7a81309cf2582854fa2e1aa76477e5f5aa44ce65b8cd69828f3213befde92f4a`.
- Selected Stage 2 tree: `5b523035db5d64e4d2e55c344919f92810f420e3b9cd1b1d87f855d915fadd43`.
- Selected Stage 4 tree: `53c8f614af8007e0fcc961368583725693c03506621e6383158e7f2e8cef51cf`.
- Producer-source tree: `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`.
- Generated-project tree: `b20055cd31d5ba00cfb242f232935570f3f5eacb66ac11ae3a81a6d885a1e966`.
- Lean workspace/invocation: both correctly recorded as null.

All match the launcher record. I also recomputed all 776 per-file Stage 1 source hashes: the key set, count, and every digest match exactly, with no missing, extra, or changed entry.

The sidecar bindings also match independently: the verification hash, inventory hash, Stage 1/Stage 3 provenance, generated tree, obligation-map hash `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, and trust-inventory hash `103b3709cba392fb7d0134c2ecbe3abc8b42e6f441702ee1c279536b0301152a` all reconcile across their actual files, input manifest, generator manifest, export result, and audit input.

Primary raw evidence: `evidence/20-comprehensive-hash-and-inventory-reconciliation.txt` and `evidence/23-stage4-independent-manifest-bijection-checks.txt`.

## Deterministic Stage 4 and target identity

Inspection of the exact generation-time producer confirms that Stage 4 selects only independently classified `DOMAIN_LEMMA` entries for export obligations and requires their ordered source IDs to equal the generated ordered obligation IDs. It generates `targetStatement` only when that obligation list is nonempty.

Here the independent domain set is genuinely empty. The generated `obligation-map.json` has exactly:

- `source_rules: []`
- `obligations: []`
- `trust_parameters: []`

The generator and export manifests both record obligation count zero. There is therefore no omitted, duplicated, irrelevant, weakened, or vacuous conjunct. The fixed generated target is correctly null: `generator-manifest.json` records `target: null`, trusted target reconstruction returns null, and a complete scan of generated Lean sources finds no `targetStatement` declaration. `Klean120Maximum/Lemmas.lean` contains only its imports and an empty namespace.

Consequently `KLEAN_NO_OBLIGATIONS` is the correct deterministic Stage 4 result. No generated target and no Stage 5 project are present.

Primary raw evidence: `evidence/17-generation-time-producer-relevant-source.txt`, `evidence/18-generated-tree-obligation-map-and-target-absence.txt`, `evidence/23-stage4-independent-manifest-bijection-checks.txt`, and `evidence/25-no-target-and-no-stage5-candidate.txt`.

## Required mechanical preflight

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` over the required three inputs and the pinned lock. It returned:

- Status: `KLEAN_NO_OBLIGATIONS`.
- Obligation count: 0.
- Target: null.
- `lake clean`: exit 0.
- `lake build`: exit 0; all generated modules built successfully, with only four unused-variable linter warnings in generated `Func.lean`.
- Returned frozen-input, discovery, and generated-tree hashes: exact matches.

The returned JSON is exactly equal as a JSON document to the recorded Stage 4 preflight, including the build-output hash `e2b1909bbfea34c177af0042561ed593741962583bc1149fe5200500b4ed0f9b`.

The first invocation exposed an audit-sandbox defect: the sandbox has a private PID namespace but a host `/proc` mount, so Lean 4.22 could not resolve `/proc/<inner-pid>/exe`. I documented the failure and repaired only executable-path discovery with a small audited `LD_PRELOAD` shim: a failed `readlink` for `/proc/*/exe` retries `/proc/self/exe`. The shim source hash is `5848507694e7c20d484cea5a13529f4e130c6d23bc3128e76279724b0315570b`. It does not modify the pinned Lean binary, generated project, or theorem content. With the shim, the pinned compiler identifies itself as Lean 4.22.0 commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the required preflight completed. This recovered environment issue does not leave an infrastructure error.

Complete fresh-build output is in `evidence/preflight-command-01.txt` and `evidence/preflight-command-02.txt`. The returned preflight is in `evidence/21-required-klean-preflight-result.txt`; diagnosis and shim construction are in `evidence/06-required-klean-preflight.txt`, `evidence/07-lean-toolchain-diagnosis.txt`, and `evidence/10-lean-proc-shim-build-and-test.txt`.

## Stage 5

Stage 5 is correctly absent because this is `CLASSIFICATION_ONLY` with a genuinely empty domain-obligation set. There is no target theorem, no `Proof.final`, no target parameter, and no candidate operational bridge to audit. Proof identity, `#print axioms Proof.final`, and parameter-definition adversarial checks are therefore inapplicable rather than skipped obligations.

## Conclusion

The protected Stage 3 manifest is complete and correctly classifies its only rule as a definition. Deterministic Stage 4 faithfully maps the independently empty domain-lemma set to an empty obligation set, generates no target, and correctly stops before Stage 5. All relevant provenance and content hashes match, and the trusted preflight succeeds on a fresh clean build.

VERDICT: PASS
LEGITIMACY: LEGIT
