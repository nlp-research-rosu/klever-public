# Independent Stage 3/4 Audit: `163-generate-integers`

## Scope and result

The launcher envelope validates under the trusted Stage 6 resolution contract.
Both `/audit-input.json` and `AUDIT_MODE` select `CLASSIFICATION_ONLY` for
condition `bare` and semantics mode `GENERATED_SEMANTICS`. Therefore this audit
covers the independent Stage 3 classification and deterministic Stage 4
generation. Stage 5 proof checks are not applicable.

I treated the mounted workspaces, manifests, logs, comments, and prior verdicts
as untrusted evidence. The classification below was reconstructed from the
frozen `verification.k`, frozen source program, and operational K semantics.

## Input and producer authentication

The signed resolution digest recomputed to
`c25950badfd47ee1081fb2e17333ecb2a879189bb394a3e9e6fce3c3caa0a2db`.
Every launcher-recorded source or tree hash recomputed exactly, including all
nine `stage1_source_hashes` entries. The principal bindings are:

| Artifact | Recomputed and recorded SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree format | `35de586b76ac3c2d70cb7974c836b1a5e6304e59ad246dadc6e42e4e766247e6` |
| Stage 1 export, Klean tree format | `de401a787892b0b3e367351d4cf078badce446f72bfcaa1a3cf0d532e5530868` |
| Frozen `verification.k` | `43cd3e9d248d5e3a77217deadcd67969728371a43150e7aafb2f1eee777f184a` |
| Stage 3 discovery manifest | `2bb9c613f66dc190c264604a5e5827eb21fe0f4082fdc93192e5c2fca1794b18` |
| Selected Stage 2 K audit tree | `222e63480cc50b8794ec72061397dc867e1f5f0276d402a64e8324a715e8e9fa` |
| Selected Stage 4 generation tree | `415187d3506a2df73d8a884dd38e2c53ae094624cb23bc42758be8138432173e` |
| Generated Lean project, Klean tree format | `c0a48c093a87734d7cfe56f73a617daec833a4f402807d1e381d571c74b97637` |
| Producer-source bundle tree | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |

Before evaluating Stage 4, I hashed the mounted producer sources:

| Producer | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` |
| `klean.py` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` |

Both values match `generator-manifest.json` and
`generation-tools/source-manifest.json`. The producer bundle contains exactly
those two sources plus the source manifest. The immutable generator image ID is
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`
in both manifests; `/audit-input.json` binds the producer directory with that
digest as its basename and binds the whole directory hash above. The generator
toolchain object also exactly matches `/reference/klean-toolchain.lock.json`.
No producer-source infrastructure error exists.

## Rule inventory reconstruction

Using the trusted `tools.k_rule_inventory.inventory_verification`, the main
module selected by the frozen `prove.sh` is `VERIFICATION`. Its local
verification-file closure is exactly `["VERIFICATION"]`. The imported `MPY`
module is frozen in `semantic.k`; its ordinary execution rules are operational
semantics, not extra local rules in the `verification.k` inventory.

For every reconstructed entry, I independently sliced the reported physical
lines, normalized whitespace, recomputed SHA-256, derived
`source_rule_id = "rule-" + normalized_sha256`, and recomputed the canonical
whole-inventory hash.

| Order | Span | Independent classification | Normalized SHA-256 |
|---:|---:|---|---|
| 1 | 9–11 | `DEFINITION` | `b067b43d5f947711d358527708712198f2c109323388e41a86efd408cfe7c3aa` |
| 2 | 12–15 | `DEFINITION` | `098526288db0b9357bcc0dfdb447cbb9838647572e7d85518b225581f438f785` |
| 3 | 17–21 | `DEFINITION` | `e5fd4b8a680c9837723a78964e7e9f5c5acbab3f9a323002561d8adfacf87cd4` |

All source slices and rule texts match byte-for-byte after line selection. All
three identities are unique. The manifest has the same three unique identities
in the same order, with no omission, duplicate, extra entry, or reordered
identity. The independently recomputed whole-inventory hash is
`1c4a93073f6781879b6ae9c5aff5efce4f9089c321e7b6bacc52db91656d0a28`,
matching both the trusted inventory and the Stage 3 manifest.

## Independent classification judgment

Let

`P(A,B,D) = (A <= D <= B) or (B <= D <= A)`.

The first rule is the positive defining equation for the declared K function
`expectedDigit`, returning `ListItem(D)` under `P`. The second is its negative
defining equation, returning `.List` under `notBool P`. These guards are exact
Boolean complements, so they are disjoint and exhaustive. Neither rule matches
an execution construct, a semantic cell, or a program invocation.

The third rule is the unguarded macro equation for the declared K function
`expected`. It concatenates `expectedDigit(A,B,D)` for `D = 2, 4, 6, 8` in
ascending order. It likewise names a summary and does not replace an
operational step.

This matches the frozen operational semantics and source program. If `A <= B`,
the program visits `2,4,6,8` in order and appends `D` exactly when
`A <= D <= B`. Otherwise it visits the same digits in the same order and
appends exactly when `B <= D <= A`. Thus both branches compute the list defined
by `expected`. The frozen postcondition places that same `expected(A,B)` in
both the result cell and the final `result` environment binding, so the
definitions are directly relevant to the program and postcondition.

As finite corroboration, an independently written direct operational model
matched the definitions on all 676 pairs in `[-5,20]^2`, including all 400
positive pairs in `[1,20]^2`. The guard partition had zero overlaps and zero
gaps on 17,576 tested triples. Reversed endpoints, singleton endpoints,
out-of-range intervals, and internal intervals were included. Strict-endpoint,
ordered-only, constant-full-list, and reverse-order counterfactuals were all
detected by concrete witnesses. The classification rests on the branch
argument above, not on finite testing alone.

Consequently:

- definitions: 3;
- ordinary operational rules in the local inventory: 0;
- proved derived lemmas: 0;
- domain lemmas: 0.

No entry is a mislabeled domain lemma. No `PROVED_DERIVED_LEMMA` is claimed, so
there is no unproved sequential-use claim to accept. None of the three rules
has a `simplification` attribute, so the simplification-class restriction is
also satisfied.

## Deterministic Stage 4 generation

After producer authentication, I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required frozen workspace, discovery manifest, generation, and trusted
toolchain lock.

The first invocation reached the clean-copy build but exposed a sandbox
toolchain issue: numeric `/proc/<pid>/exe` entries do not exist in this process
namespace, so Lean/Lake could not locate their installation. The failed output
is preserved. I reran with the recorded 26-line compatibility shim
`evidence/05_proc_exe_compat.c`, which only redirects `readlink` requests for
numeric `/proc/<pid>/exe` to the equivalent `/proc/self/exe`. It does not
intercept source reads, hashes, compilation, elaboration, or proof operations.

The mandated check then returned:

- `status: KLEAN_NO_OBLIGATIONS`;
- `obligation_count: 0`;
- `target: null`;
- `lake clean`: exit 0, empty output SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, output SHA-256
  `8d7c29846a650dd90ede9c061675453caf5381599bfe611617a1f9464b937de3`.

The build output hash and full returned diagnostic match the immutable recorded
preflight and `/audit-input.json`.

I also checked the Stage 4 mapping independently of that preflight:

- the independently classified domain set is empty;
- `input-manifest.json` has exactly that empty `source_rules` set;
- `obligation-map.json` has empty `source_rules`, `obligations`, and
  `trust_parameters`;
- the obligation-map SHA-256 is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  exactly as recorded by the generator;
- `generator-manifest.json` and `export-result.json` both record zero
  obligations and consistent hashes;
- the export trust-inventory SHA-256
  `034517e2bc53fe1f83a2ab8328661d724908eca12f7d3d68881f4511e0a2db85`
  matches the mounted file;
- the generator manifest, recorded preflight, audit input, trusted target
  parser, and expected-target reconstruction all yield `null`;
- scanning all seven generated Lean sources finds no `targetStatement`
  declaration.

There are therefore no omitted or duplicated domain rules, no extra,
irrelevant, weakened, or vacuous conjuncts, and no changed target. This is a
genuinely empty domain-lemma set, so `KLEAN_NO_OBLIGATIONS` is legitimate. The
absence of a target is the required representation of that empty set, not a
vacuous theorem.

## Stage 5 disposition

Stage 5 is correctly absent in `CLASSIFICATION_ONLY` mode:
`stage5_result`, `lean_workspace`, `lean_invocation`, and the target are all
null, and `/candidate` does not exist. There is no generated theorem to prove,
so no fresh `Base`, candidate build, `Proof.final`, axiom accounting, or
operational-bridge parameter audit applies.

## Evidence

Raw commands, complete results, and independent audit scripts are under
`/audit-output/evidence/`:

- `00_environment_*`: launcher mode, audit input, and mounted file inventory;
- `01_trusted_tool_inspection_*`: trusted inventory/preflight source used;
- `02_frozen_sources_and_manifests_*`: raw source, manifest, and file hashes;
- `03_inventory_and_hash_audit_*`: all recorded hashes and exact ordered rule
  reconstruction;
- `04_classification_semantics_audit_*`: classification, witnesses, exhaustive
  finite checks, and counterfactuals;
- `05_check_generation_*`, `05_toolchain_diagnostics_*`, and
  `05_proc_exe_compat.c`: failed and successful preflight evidence plus the
  narrow environment workaround;
- `06_stage4_structural_audit_*`: empty bijection, manifest bindings, target
  absence, and Stage 5 absence.

The Stage 3 classifications are complete and mathematically appropriate, and
the authenticated deterministic Stage 4 output exactly represents the genuine
empty domain-obligation set.

VERDICT: PASS
LEGITIMACY: LEGIT
