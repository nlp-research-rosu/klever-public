# Independent Stage 3–5 Audit: `147-get-max-triples`

## Scope and result

The launcher and environment both record `AUDIT_MODE=CLASSIFICATION_ONLY` for condition `kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`. I independently audited the frozen Stage 1 verification-module rule inventory, the protected Stage 3 classifications, and the selected deterministic Stage 4 generation. Stage 5 proof checks are inapplicable in this mode and no Stage 5 candidate is mounted.

I treated the prior Stage 2 review, all logs, generated content, comments, and manifests as untrusted evidence. I did not adopt any earlier verdict or classification. Trusted `/reference/tools` code was used for canonical inventory reconstruction, tree/file hashing, trust-boundary validation, target extraction, and `check_generation`.

## Producer provenance gate

I hashed the two mounted generation-time producer sources before judging Stage 4:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b` |
| `klean.py` | `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4` |

Both hashes equal the values in `generator-manifest.json` and `source-manifest.json`. The image ID is consistently `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc` in the generator manifest, source manifest, and the image-keyed producer path recorded in `/audit-input.json`. The complete producer bundle, recomputed with the launcher's trusted tree-hash algorithm, is `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4`, exactly the launcher-recorded value.

An initial comparison used the exporter's different tree-digest serialization and therefore produced a different digest. Recomputing with the trusted launcher function `pipeline_contract.sha256_tree` resolved that format distinction and matched exactly; this was not a source mismatch. The full check is in `evidence/07-producer-provenance-launcher-format.log`.

Producer provenance passes. There is no producer-source infrastructure `AUDIT_ERROR`.

## Canonical rule-inventory reconstruction

Using `tools.k_rule_inventory.inventory_verification` with `PYTHONPATH=/reference`, I reconstructed the local module closure selected by `prove.sh`. The selected main module is `VERIFICATION`; the local closure, in frozen source order, is `VERIFICATION-SYNTAX`, `VERIFICATION`. The syntax module contains no rules. The complete closure has exactly these three rules:

| # | Span | Recomputed normalized SHA-256 / `source_rule_id` | Independent class |
|---:|---|---|---|
| 1 | `verification.k:18–19` | `7f4fda07af964878549fb6179e4214215094e6afdc0f799801aef078770bc8f4` / `rule-7f4fda07af964878549fb6179e4214215094e6afdc0f799801aef078770bc8f4` | `DEFINITION` |
| 2 | `verification.k:22–24` | `da6a4e2936c513bfd13e5a5dabe3f487b5f2fc80dad7975a6a8838c23f087590` / `rule-da6a4e2936c513bfd13e5a5dabe3f487b5f2fc80dad7975a6a8838c23f087590` | `DEFINITION` |
| 3 | `verification.k:26–28` | `f0b13856a8dad7aae0ba7cb74d4c557bf3d05dd316341f9923211e2c0e60ee6c` / `rule-f0b13856a8dad7aae0ba7cb74d4c557bf3d05dd316341f9923211e2c0e60ee6c` | `DEFINITION` |

For each entry I independently normalized the exact source text, recomputed its hash, reconstructed `rule-<hash>`, and checked the source span and module. The canonical whole-inventory hash is `97e6022f17f451a5f99cac62e3030189934e65106ea945ffd1d51f7a67b6ebf5`.

The protected Stage 3 manifest has exactly three unique entries. Its ordered identity sequence is identical to the reconstructed sequence, and its inventory hash is identical. There are no omissions, additions, duplicates, reordered identities, changed hashes, or unaccounted classifications. See `evidence/04-inventory-reconstruction.log`.

## Independent classification judgment

All three entries are genuinely definitions:

1. `zeroResidueCount(N)` introduces a fresh total summary function and defines it as the supplied semantics' exact integer-floor expression for `(N + 1) // 3`. It does not match a source AST term or a configuration cell and cannot preempt program execution.
2. `chooseThree(X)` introduces a fresh total summary function and defines it as the exact supplied-semantics normal form of `X * (X - 1) * (X - 2) // 6` using `pyMod` and `/Int`. It is an equation defining a named summary, not an asserted equality between previously meaningful terms.
3. `expectedTriples(N)` introduces the named postcondition term by composing the first two summaries. It defines the proof term used on the destination side of the reachability claim; it does not rewrite operational source code.

The supplied operational semantics dispatches integer `+`, `-`, and `*` to the corresponding K integer hooks, dispatches `I1 // I2` to `(I1 - pyMod(I1,I2)) /Int I2`, and defines `pyMod(I1,I2)` by `((I1 %Int I2) +Int I2) %Int I2`. The frozen program performs the same arithmetic assignments and return. Thus the rules name the values produced by ordinary execution and do not constitute operational bridges.

The definitions are relevant to the frozen source and postcondition. For `i = 1..n`, `i²-i+1` is residue `0 mod 3` exactly when `i ≡ 2 mod 3`, giving `floor((n+1)/3)` such indices; all other values have residue 1. A triple is divisible by 3 exactly when it takes three residue-0 values or three residue-1 values, giving `C(z,3)+C(n-z,3)`. Independent finite witnesses for every positive `n` from 1 through 80 had zero mismatches against direct triple enumeration. Counterfactual mutations to each definition produced observable mismatches. These tests support relevance and body sensitivity; the classification rests on the rule shapes and operational semantics, not finite testing alone. See `evidence/05-operational-semantics-excerpts.log` and `evidence/14-mathematical-relevance-and-mutations.log`.

No inventory rule has a `simplification` attribute, so the simplification-class restriction is satisfied vacuously. No rule is claimed as `PROVED_DERIVED_LEMMA`, and none has the shape of a derived fact requiring the special proof-history condition. Most importantly, no rule asserts a domain fact: every rule has a fresh defined head and a defining body. The independently classified true `DOMAIN_LEMMA` set is therefore genuinely empty.

## Stage 4 preflight and independent integrity checks

I invoked the requested API directly:

```text
PYTHONPATH=/reference python /audit-output/evidence/run_generation_preflight.py
```

The first invocation reached the build phase but the ambient Lean installation could not resolve its executable because the sandbox reports PID-namespace-local values from `getpid()` while its mounted `/proc` exposes host PIDs. This produced `lake clean failed (1): could not detect the configuration of the Lake installation`; it was an audit-environment failure, not a generation result.

I recorded the diagnostics and used the narrowly scoped preload shim in `evidence/host_getpid.c`, compiled under `/tmp/audit-work`, to return the host PID read from `/proc/self/status`. It changes no pinned Lean binary and no mounted evidence. With that environment-only correction, the same trusted API was rerun as:

```text
LD_PRELOAD=/tmp/audit-work/host_getpid.so \
PYTHONPATH=/reference \
python /audit-output/evidence/run_generation_preflight.py
```

The rerun returned:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- target `null`;
- `lake clean` exit `0`;
- `lake build` exit `0`, with `Build completed successfully`;
- designated sorry count `0`; and
- generated tree hash `ad1c18e7ac675dd92caaf22db54069a72390a7268ce19ddc2c5b08139ba36acf`.

The exact failure and successful returned evidence are preserved in `evidence/08-check-generation.log` and `evidence/11-check-generation-with-pid-shim.log`.

I then independently recomputed and reconciled all recorded bindings:

| Artifact/hash family | Recomputed value | Result |
|---|---|---|
| Stage 1 launcher tree | `636d84184b99baac2e1a44ed3c11d452a6bd4cb1891243cd25158875c7aa62fb` | matches audit input |
| Stage 1 exporter tree | `9ee695d2c6fdf5d819177929a289d8b739213fe6e2c956afce5dfdd5ca0d4d00` | matches input/export/generator/preflight/audit bindings |
| Stage 3 manifest file | `64690e24e05c54f03cfbfde7e426bfea0fea65f35f057044c323d58246bc7de4` | matches all bindings |
| Selected Stage 2 launcher tree | `8891530f07ade98706d3ea35234dcfd7b93fb7d9c4b2cf4abb7867d2823c6305` | matches selection; no earlier judgment trusted |
| Selected Stage 4 launcher tree | `1454872a228dca87a0ea1a6faba3b48b8503f87937296496eff2b429753a7bce` | matches selection and audit input |
| Generated project exporter tree | `ad1c18e7ac675dd92caaf22db54069a72390a7268ce19ddc2c5b08139ba36acf` | matches generator/export/preflight/audit input |
| Obligation map file | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` | matches generator manifest |
| Trust inventory file | `4bb3cc92649dba88ff7821d4fb38e47ac8352be6f63b016b292b4987afbc04b6` | matches export result |

All 774 per-file Stage 1 hashes match `/audit-input.json` exactly, including key set and values. The generator toolchain object exactly matches `/reference/klean-toolchain.lock.json`. The selected preflight document exactly matches the copy bound into `/audit-input.json`. Full results are in `evidence/13-independent-stage4-integrity.log`.

### Obligation bijection and fixed target

The independently classified domain source-rule list is `[]`. `input-manifest.json` records `source_rules: []`; `obligation-map.json` records `source_rules: []`, `obligations: []`, and `trust_parameters: []`; all count fields are zero. Thus the ordered source-rule/obligation map is exact and bijective. There can be no omission, duplicate, reordered obligation, weakened conjunct, irrelevant conjunct, or vacuous conjunct because there is no eligible domain rule and no obligation.

The trusted target extractor returns `null`. The generator manifest, selected preflight, and audit input all bind the target to `null`, and no generated target declaration exists. The generated definitions do preserve the three source definition bodies; excerpts are in `evidence/15-generated-definitions-no-target.log`. Consequently, `KLEAN_NO_OBLIGATIONS` is the correct deterministic Stage 4 result for the independently established empty domain set.

The generated prelude contains 41 recorded collection-hook value-level axioms. The trust inventory exactly matches those declarations, the trusted preflight rejects proposition trust, and there is no generated theorem or proof that could depend on them in this no-obligation result. They do not turn the empty target into a proof claim.

## Stage 5 disposition

This is not `CLASSIFICATION_AND_PROOF`. `/candidate` is absent; `lean_workspace`, `lean_invocation`, their hashes, and `stage5_result` are all `null` in the launcher input. That is exactly required for `KLEAN_NO_OBLIGATIONS`.

Accordingly, candidate `Base` copying, candidate `lake clean`/`lake build`, `#print axioms Proof.final`, proof identity, candidate trust-token scans, and `target.parameters` operational-bridge audits are not applicable and were not fabricated. There is no candidate target to shadow, weaken, duplicate, or prove vacuously.

## Evidence index

The main raw transcripts and auditor sources are under `/audit-output/evidence/`:

- `02-producer-provenance-comparison.log`, `06-producer-provenance-full-check.log`, `07-producer-provenance-launcher-format.log` — file/image provenance, the intentionally different exporter-format tree result, and the matching launcher-format tree result;
- `03-frozen-source-spec-and-classification.log`, `04-inventory-reconstruction.log` — frozen source and canonical inventory;
- `05-operational-semantics-excerpts.log`, `14-mathematical-relevance-and-mutations.log` — semantic classification evidence;
- `08-check-generation.log`, `09-lean-environment-diagnostics.log`, `10-elan-diagnostics.log`, `11-check-generation-with-pid-shim.log` — preflight failure diagnosis and successful rerun;
- `12-stage4-sidecars-and-target-search.log`, `13-independent-stage4-integrity.log`, `15-generated-definitions-no-target.log` — manifests, complete hash/bijection checks, and target absence; and
- `reconstruct_inventory.py`, `check_producer_provenance.py`, `run_generation_preflight.py`, `verify_stage4_integrity.py`, `check_mathematical_relevance.py`, `host_getpid.c` — exact auditor-authored commands/helpers.

VERDICT: PASS
LEGITIMACY: LEGIT
