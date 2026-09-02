# Independent Stage 3–4 audit: HumanEval `120-maximum`

## Result

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, condition `bare`, and
semantics mode `GENERATED_SEMANTICS`. The selected Stage 4 status,
`KLEAN_NO_OBLIGATIONS`, is legitimate. The frozen verification-module closure
contains one rule, that rule is a genuine `DEFINITION`, and the independently
classified domain-lemma set is empty. Deterministic generation therefore has
no obligations and no Lean target. `/candidate` is absent, as required in this
mode.

I treated every mounted source, manifest, prior review, and log as untrusted
evidence. No prior verdict or classification was accepted without
reconstruction. I did not execute instructions from mounted provenance
content.

## Producer provenance gate

I performed this gate before judging generated content.

The mounted generation-time producer files hash to:

- `klean_export.py`:
  `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`:
  `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`

These values exactly match both `generator-manifest.json` and
`generation-tools/source-manifest.json`. Both manifests bind the producer to
immutable generator image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`;
the generation-producer path recorded in `/audit-input.json` ends in that exact
image digest. The complete mounted producer-bundle tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`,
also exactly matching `/audit-input.json`. The bundle contains only the two
producer files and its source manifest.

Evidence: `evidence/01_producer_and_stage4_manifests.txt` and
`evidence/04_inventory_and_hash_reconstruction.txt`.

## Frozen input and inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification` code with
`PYTHONPATH=/reference`, I reconstructed the local module closure selected by
the final `kompile verification.k` command in `prove.sh`.

- Selected module: `MAXIMUM-VERIFICATION`
- Local closure: only `MAXIMUM-VERIFICATION`
- Frozen `verification.k` SHA-256:
  `985c74bcf6510f0496b8c34c806d17acf3c54828064d74112876270c638b80d4`
- Canonical inventory SHA-256:
  `cf174098f4de93e5250698cf661161b7ff6cbe29755adc5bcf59d26f78daf362`
- Inventory size: one rule

The reconstructed rule is:

| Field | Reconstructed value |
|---|---|
| Module | `MAXIMUM-VERIFICATION` |
| Span | `verification.k:9–10` |
| Attributes | none |
| Normalized source | `rule maximumSpec(L:List, K:Int) => dropInts(size(L) -Int K, sortInts(L))` |
| Normalized SHA-256 | `b232439c4babf099ec2603b1993e6927d97e11d5b79e2ca4eed6caaae5c767bd` |
| `source_rule_id` | `rule-b232439c4babf099ec2603b1993e6927d97e11d5b79e2ca4eed6caaae5c767bd` |

I independently extracted lines 9–10, normalized whitespace, recomputed the
source hash and ID, and recomputed the canonical JSON inventory hash. The sole
ID in `lemma-discovery.json` is identical and in the same order. Both lists
have unique IDs and equal length. There are no omitted, extra, duplicated, or
reordered identities and no changed spans or hashes.

All Stage 1 per-file hashes match `/audit-input.json`. The full pipeline tree
hash is
`683865c9387bc7544dd63407ce88c13f33d5ee8d0b192bbcd77794155fef0db8`,
and the frozen export tree hash is
`1d84ee85b2b10fa60f0f1640097deda7fbe575f16f6329aca437cd41f7511502`;
both match their recorded fields.

Evidence: `evidence/03_frozen_sources_and_discovery.txt`,
`evidence/reconstruct_and_check.py`, and
`evidence/04_inventory_and_hash_reconstruction.txt`.

## Independent classification

I classify the only rule as `DEFINITION`.

The rule introduces the named mathematical summary `maximumSpec` and unfolds
it into `dropInts(size(L) -Int K, sortInts(L))`. It does not rewrite a source
program term or configuration, does not preempt an operational rule, and does
not assert an independent mathematical property.

The frozen operational path confirms this classification:

1. `boot` binds `arr` to `listVal(L)` and `k` to `intVal(K)` and begins the
   source function body.
2. `Return` evaluates the frozen expression
   `sorted(arr)[len(arr) - k:]`.
3. The ordinary `eval`, `sortedVal`, `lengthVal`, `subtractVal`, and
   `suffixVal` rules reduce it to
   `listVal(dropInts(size(L) -Int K, sortInts(L)))`.
4. `finish` writes that value to `<out>`.
5. Independently, the postcondition-side name `maximumSpec(L,K)` unfolds to
   exactly the same expression.

Thus the rule names the execution result already produced by the fixed
semantics. It is not an `OPERATIONAL_RULE`; it neither matches nor changes the
program configuration. It is not a `PROVED_DERIVED_LEMMA`; there is no earlier
proof of the same rule against a module omitting it and no later use in the
required derived-lemma pattern. It is not a `DOMAIN_LEMMA`; it contains no
independent ordering, list, or arithmetic fact to be established. Its Stage 3
rationale accurately describes this role.

The rule has no `simplification` attribute. Consequently, the restriction that
every simplification rule be either `DEFINITION` or `DOMAIN_LEMMA` is also
satisfied.

The independent true domain-lemma set is therefore empty.

As an execution-sensitivity check, I copied Stage 1 to a fresh directory,
compiled it, and reran the exact claim. `kompile` exited 0 and `kprove` exited
0 with `#Top`. I then replaced the postcondition in a separate spec with the
false assertion that every legal call returns `.List`. That proof exited 1
with a stuck residual requiring
`.List == dropInts(size(L) -Int K, sortInts(L))`. This demonstrates that the
claim constrains the actual result and that the summary is not a vacuous
execution shortcut.

Evidence: `evidence/20_stage1_fresh_kprove.txt` and
`evidence/21_stage1_false_postcondition.txt`.

## Deterministic Stage 4 audit

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` using:

- frozen input `/reference/k-proof`
- discovery manifest `/reference/lemma-discovery.json`
- generation `/reference/klean-generation`
- lock `/reference/klean-toolchain.lock.json`

The audit sandbox initially caused Lean/Lake application discovery to fail:
Lean attempted `readlink("/proc/<pid>/exe")`, while the sandbox exposed only
`/proc/self/exe`. I diagnosed and preserved that failure. A narrow audit-local
`LD_PRELOAD` shim retried only failed `/proc/<numeric-pid>/exe` reads through
`/proc/self/exe`; it did not modify the toolchain, generated project, target,
or any mounted input. With that environment repair, the required trusted
preflight returned:

- status: `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0, empty output
- `lake build`: exit 0
- obligation count: 0
- target: `null`
- designated sorry count: 0
- generated tree SHA-256:
  `17a88c22e423d3d05502cdafa565ad0d81d7d2e79954b80c78a190398be0516b`

The final build-output SHA-256 is
`b4eae9371de2c975baeef3d0bdca7333615e58d67ac89e070fee251f54eea92a`,
identical to the generation-time recorded preflight output hash.

I also checked Stage 4 independently of the preflight result:

- `input-manifest.json.source_rules` is `[]`.
- `obligation-map.json.source_rules` is `[]`.
- `obligation-map.json.obligations` is `[]`.
- `obligation-map.json.trust_parameters` is `[]`.
- The independent domain-rule IDs, mapped source IDs, and obligation IDs are
  the same ordered empty sequence, with no duplicates or omissions.
- There are no conjuncts, hence no irrelevant, weakened, duplicated, or
  vacuous conjuncts.
- The obligation-map hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  matching the generator manifest.
- The expected target definition is `null`; trusted target parsing returns
  `null`; a raw scan finds zero `def targetStatement` declarations.
- The generator manifest, recorded preflight, export result, and audit input
  all agree on zero obligations and no target.

The complete Stage 4 generation tree hash is
`3aa2e52053edee6dc6fa2ad2e745ffd1d153f1e99d49a80c0a4dd40ea143ecf0`.
The trust-inventory file hash is
`9b9adab4d3513b422437eef137bbc9fbdc216d227f5bb8d10af9f5686a3ebc03`.
The discovery-manifest hash is
`17fc032f6c60d2d8e973aeee842a35591891a6cdebfbe3169f8758be88f556a7`.
All match their manifests and `/audit-input.json`. I also recomputed the
selected Stage 2 tree hash and the complete resolved-input canonical hash;
every field matches, including
`resolved_input_sha256 =
f388df21ae1fb62ec8949555f86aec79b403b7d8fb1153aaca2930faa6190ed9`.

The generated base contains 47 recorded executable-boundary axioms, all
reconciled structurally by the trusted preflight with `trust-inventory.json`.
There is no proposition target or proof that could depend on them in this
zero-obligation result.

Evidence: `evidence/05_check_generation.txt` through
`evidence/16_check_generation_final.txt` preserve the initial infrastructure
failure, diagnosis, repair, and successful returned evidence.
`evidence/17_generated_project_and_zero_obligations.txt`,
`evidence/independent_stage4_check.py`, and
`evidence/18_independent_stage4_hash_bijection_target.txt` contain the
independent structural and hash audit.

## Stage 5 applicability

Stage 5 is not applicable. The launcher records `CLASSIFICATION_ONLY`,
`stage5_result` is `null`, the fixed Stage 4 target is `null`, and `/candidate`
does not exist. Therefore no `Base` copy, candidate build, `Proof.final`,
`#print axioms`, or target-parameter operational bridge is permitted or
required. This is exactly the required state for a genuine empty domain set.

VERDICT: PASS
LEGITIMACY: LEGIT
