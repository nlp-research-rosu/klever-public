# Independent Stage 3–5 Audit: `51-remove-vowels`

## Scope and result

The launcher records `AUDIT_MODE=CLASSIFICATION_ONLY`, condition `bare`, and
semantics mode `GENERATED_SEMANTICS`. I treated the mounted Stage 1–4
artifacts, the earlier Stage 2 review, and their comments and logs only as
untrusted evidence. The reconstruction and comparisons below use the trusted
modules under `/reference/tools`; no earlier verdict or classification was
accepted as authoritative.

The independent classification finds three definitions and no domain lemmas.
Consequently the selected Stage 4 status `KLEAN_NO_OBLIGATIONS`, empty
obligation map, absent target, and absent Stage 5 candidate are correct.

## Producer authentication

I authenticated the mounted generation-time producer sources before judging
the generated output.

| Producer file | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

These are exactly the `files` entries in
`/reference/generation-tools/source-manifest.json` and the
`exporter_sha256`/`klean_py_sha256` values in `generator-manifest.json`. The
producer bundle contains exactly those two files plus `source-manifest.json`.
Its recomputed signed-resolution tree hash is
`363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0`.

The source manifest and generator manifest both bind image
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`.
The basename of the producer-source path recorded in `/audit-input.json` is
the same digest. Producer lineage is therefore complete and consistent; no
infrastructure `AUDIT_ERROR` condition is present.

## Inventory reconstruction and Stage 3 bijection

Using `tools.k_rule_inventory.inventory_verification` on the frozen Stage 1
workspace, I reconstructed the local verification-module closure. The
selected module is `VERIFICATION`; its local closure contains only
`VERIFICATION`. The `MPY` module is required from `semantic.k`, not a module
locally declared in `verification.k`, so it is correctly outside this
particular inventory.

The frozen `verification.k` hash is
`38e8cf09eb29ca6f7e35b85eda0795a619c40a2b0ccdb6f6868a4b3f87ff4003`.
For each rule I independently sliced the recorded source lines, normalized
whitespace, recomputed SHA-256, and reconstructed `source_rule_id` as
`rule-<normalized-sha256>`.

| Span | Recomputed identity | Independent classification |
|---|---|---|
| 12–21 | `rule-d70a0aac3bb3b348786898ec6b394dbdace66562eea52f3eafc591f02cd22ab4` | `DEFINITION` |
| 23–32 | `rule-49a18c81258ea070950de54bb16d8b99c51a26b8c67538986c2c3b31a1fafa3f` | `DEFINITION` |
| 34–34 | `rule-cdf7c02d83c3928a7f8b88a45691a3681e2a79a579a8503bd2c19f81bb514a86` | `DEFINITION` |

The canonical inventory hash recomputes to
`db19c9fed28f7adfa8f59dfe04d16429d3bed749f02f49c42eb05bc32571c968`.
The protected Stage 3 manifest contains exactly these three identities in
this order, with no missing, extra, duplicated, or reordered entry. Its
inventory hash agrees. The trusted Stage 3 contract validation also passes.

## Independent classification judgment

The classifications are mathematically sound:

- `removeLowerVowels(S)` introduces and defines a named summary by a
  terminating composition of `deleteAll` at the five lowercase vowels.
- `removeUpperVowels(S)` does the same for the five uppercase vowels.
- `removeVowelsSpec(S)` is a macro-like definition composing the two named
  summaries.

These rules introduce the meanings of named proof terms. They do not assert
an algebraic property of an independently defined operation, do not replace
an operational program term, and are not claimed as derived lemmas. They
therefore satisfy the required `DEFINITION` category and are not hidden
`DOMAIN_LEMMA` entries.

All three definitions are relevant: `removeVowelsSpec(INPUT)` is the exact
postcondition term, and its two component summaries correspond to the source
program's replacement chain. There is no `[simplification]` attribute on any
inventory rule. The `deleteAll` simplification equation in `semantic.k` is
outside the local `verification.k` inventory; semantically it defines the
named helper by the fixed `replaceAll(S, NEEDLE, "")` hook.

I parsed, but did not execute, the frozen Python solution. Its nested
`.replace` calls delete exactly
`a,e,i,o,u,A,E,I,O,U`, in that order. The K rules for `eval`,
`replaceValue`, and `deleteAll` map those calls to the same deletion sequence.
Independent models agreed on empty, mixed-case, repeated-vowel, newline,
Unicode, emoji, and consonant-only inputs. Counterfactual identity,
constant-empty, omitted-`U`, and delete-`b`-instead-of-`a` mutations all
changed witness outputs. This supports both relevance and operational
alignment; it is not being used as a substitute for the rule classification.

The resulting independent inventory is:

- Definitions: 3
- Operational rules: 0
- Proved derived lemmas: 0
- Domain lemmas: 0

No rule meets the domain-lemma criterion, so the true domain set is genuinely
empty.

## Recorded hashes and Stage 4 manifest integrity

Every mounted content hash in the signed resolution and every Stage 4
sidecar binding was independently recomputed. Principal results are:

| Artifact | Recomputed hash |
|---|---|
| Stage 1 workspace, framed tree | `8494f5f7fe43be62e36bcc3df3c4c2177959ed878f1d7f8b1e29ca58b6c5c55b` |
| Stage 1 export tree | `bf65fba5049c765d85e8b9326a83a70a6e7ac690358db142a2a5a3ecfcf1d365` |
| Stage 3 manifest | `d19b4b795cd8b5316cd20bbbc4aee05a59ae724010c2bf3b223db53300ca04da` |
| Selected Stage 2 audit tree | `f291b299c4b76d7dd9d9114ec656e1fa2ceaea3d95e5846f8415f9df2a92775a` |
| Selected Stage 4 generation tree | `927da8d2caa8ec28179f455f51575eac79779de5bda0276f7914e41708f6b478` |
| Generated Lean tree | `536792747606a7f4f31ff11241239dcc768569dbcfe578b3c84b41215e595f91` |
| Producer-source bundle tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |

The per-file Stage 1 hashes exactly equal
`resolution.stage1_source_hashes`. The selected-artifact hashes, input
manifest hashes, generator provenance, export-result bindings, preflight
bindings, obligation-map hash, generated-tree hash, and trust-inventory hash
all agree with their recomputed subjects. The signed resolution digest also
verifies. The generator toolchain object exactly equals
`/reference/klean-toolchain.lock.json`.

The launcher-only audit-image and mechanical-checker-lock identifiers in the
unsigned `audit` metadata have no separately mounted comparison objects; they
were not used to infer artifact correctness. All hashes that bind mounted
candidate or provenance content were recomputed.

## Preflight rerun and obligation/target identity

I reran:

```text
PYTHONPATH=/reference python3 -c '... tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json
) ...'
```

The sandbox initially exposed a PID-namespace defect: Lean 4.22 calls
`readlink("/proc/<getpid()>/exe")`, while this container's `/proc` does not
expose the namespace-local numeric PID. A probe recorded `ENOENT`. I used the
recorded narrow preload shim in `evidence/proc_self_readlink_fix.c`, which
redirects only that exact self-executable lookup to `/proc/self/exe`; every
other `readlink` is passed through unchanged. With that environment repair,
Lean reports the pinned 4.22.0 commit and the trusted preflight succeeds.

The returned result exactly reproduces the stored preflight:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count 0;
- target `null`;
- trust declaration count 42;
- no designated `sorry`;
- `lake clean` exit 0 with empty output; and
- `lake build` exit 0 with output hash
  `f5d212bc8b07ec61bcddb12ebff16421752571bfdf4456cfaabec3853ffb6718`.

The exact source-rule/obligation relation is:

```text
source_rules = []
obligations = []
trust_parameters = []
```

This is a bijection because the independently classified domain set is also
empty. There can be no omitted, duplicated, irrelevant, weakened, or vacuous
conjunct. `generator-manifest.json`, `preflight.json`, `/audit-input.json`,
the obligation map, the computed expected target, and the actual generated
Lean sources all agree that the fixed target is absent. `Lemmas.lean`
contains an empty namespace and no substitute theorem. The 42 allowlisted
declarations are generated executable trust boundaries, not proposition
axioms or a hidden proof target; the trusted preflight validates their exact
allowlist and rejects proposition trust.

## Stage 5

Stage 5 proof checks are inapplicable in `CLASSIFICATION_ONLY`. The signed
resolution has null Lean workspace/invocation hashes and null Stage 5 result,
there is no generated target, and `/candidate` is absent. This is precisely
the required state for a legitimate no-obligation classification.

## Evidence

Raw commands and results are under `evidence/`. The principal records are:

- `01_producer_authentication.log` and `01b_manifests.log`
- `02_frozen_sources.log`
- `03b_extended_hash_checks.log`
- `04m_readlink_probe.log`, `04n_runtime_repair_validation.log`, and
  `04o_rerun_check_generation_pass.log`
- `05_generated_project_and_sidecars.log`
- `06_semantic_alignment_and_counterfactuals.log`

VERDICT: PASS
LEGITIMACY: LEGIT
