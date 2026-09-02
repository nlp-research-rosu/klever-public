# Independent audit: `1-separate-paren-groups` / `bare`

## Result

The protected Stage 3 classification is mathematically correct: the complete
local verification-module inventory contains 11 definitions and no operational
rules, proved-derived lemmas, or domain lemmas. The Stage 4
`KLEAN_NO_OBLIGATIONS` result is therefore legitimate. Its obligation map is
genuinely empty, its generated target is genuinely absent, and no Stage 5
candidate is present.

I report `CONCERNS` rather than `PASS` for one provenance limitation. The
generation manifest records generation-time hashes for `klean_export.py` and
`klean.py`, but the only mounted trusted copies have different hashes. The
mounted audit tools do exactly match the launcher-recorded mechanical-checker
lock, and all source, tree, sidecar, obligation-map, and target hashes that have
corresponding mounted objects match. No historical source object matching the
two generation-time hashes is mounted, so those two self-recorded provenance
fields cannot be independently reproduced. This does not create or suppress an
obligation in this case, because the independently classified domain set is
empty and the null target was independently established.

## Audit mode and trust handling

`AUDIT_MODE` and `/audit-input.json` both say `CLASSIFICATION_ONLY`; the
semantics mode is `GENERATED_SEMANTICS`. `/candidate` is absent. I treated the
Stage 1, Stage 2, Stage 3, Stage 4, and prior-log contents only as evidence and
did not execute their scripts or instructions.

The signed-resolution envelope validates with resolved-input digest
`a38afe56ac26419d201829047399dbfc48855676f4041f2fe4c5e34ea45e90ad`.
The launcher’s mechanical-checker lock hash,
`9cd22493bf7a2445bebb5c81b74bbe427a73a98d5c2a547db8b5c69b697ad56a`,
equals the SHA-256 of
`/opt/humaneval/data/klean-audit-tools.lock.json`. Every one of the eight
locked tool files matches its per-file hash under `/reference/tools`.

The two launcher copies of the audit input are byte-identical, with SHA-256
`a0c4e9a8c24082f7a2c88417984b88a6e73a1b8861c188358f3278cd03354217`.

## Inventory reconstruction and bijection

I invoked the trusted
`tools.k_rule_inventory.inventory_verification(Path("/reference/k-proof"))`
and separately imposed strict positional comparison, because the basic trust
boundary validates identities by key but does not itself reject reordering.

The selected main module is `MPY-VERIFICATION`. Its local closure inside
`verification.k` contains only `MPY-VERIFICATION`; `MPY` is defined in the
required `semantic.k`, not as another local module in `verification.k`.

Reconstruction results:

- `verification.k` SHA-256:
  `cf1dced488cadea0d91cd8c13684c691c2bbd9c891e0b717d0905146938e0f53`
- Canonical rule count: 11
- Canonical inventory SHA-256:
  `7110b556e2e2e5f7641769542e6db909889827d1e68749a448bdf5f51d38d241`
- Manifest rule count: 11
- Missing, extra, or duplicated IDs: none
- Positional identity: all 11 IDs occur in the exact canonical order
- Recomputed canonical inventory hash: exact match
- Discovery manifest SHA-256:
  `1d658f9f3f836cd96386a95bf89aa4d0ae7883a6c174f3fd3bb21487b68e0357`,
  exact match to the signed input and all Stage 4 bindings

Every rule has no attributes. Each `source_rule_id` is exactly `rule-` followed
by its independently recomputed normalized source hash:

| Span | Normalized SHA-256 / source-rule suffix | Head | Class |
|---:|---|---|---|
| 17 | `b29a7b1f61d027c75f5d54e6f778c4ffafe703f461096a1d08700bae9b5849da` | `runSpec(.Chars, ...)` | `DEFINITION` |
| 18 | `03d30c437cb7bd8a90fd37a82631921d6c5bd459ea8924300ffafa088b28240e` | `runSpec(SP CS, ...)` | `DEFINITION` |
| 19 | `ee28b1b89c45af68725d2c53c17fec71114155badb89a86ba1370ef263893c24` | `runSpec(LP CS, ...)` | `DEFINITION` |
| 20 | `ee734da296fe2d2d4070e9117fa1dc33181b3c52f7e9629c362ebe25fa07a852` | `runSpec(RP CS, zero, ...)` | `DEFINITION` |
| 21 | `a1305acd847b564566d980520b2960809147091b2fc541ba1b00bc3534001edd` | `runSpec(RP CS, succ(zero), ...)` | `DEFINITION` |
| 22 | `23aee5f25569cab008c78f770e7a68f475ee096ae14e72789cb7a87d5c7b6e26` | `runSpec(RP CS, succ(succ(D)), ...)` | `DEFINITION` |
| 24 | `6e9d63e72f1d96b8d7ba85bd3016f00960ddff320ccba1bd43d74b23295b5f90` | `stateDepth(scanState(...))` | `DEFINITION` |
| 25 | `5b065840a104280bdea14bf8cbfb96a45454e5d3f68448977ab8119c3521b55a` | `stateCurrent(scanState(...))` | `DEFINITION` |
| 26 | `4c968b2b2cfa45f88ae0c5dcf90432112081bb44e8a2471c9a987aa90bd17bfe` | `stateOutput(scanState(...))` | `DEFINITION` |
| 27 | `109874df159aa48ad8e1b3715b0ea513f28bc7bb9b410bf89eb790601fd826a4` | `stateLast(scanState(...))` | `DEFINITION` |
| 28 | `83fdf9d2c3bc8712363c660c4deb46f4e4be4ae1056e9f139ccca451b876e6df` | `separateSpec(CS)` | `DEFINITION` |

The protected manifest has the same classification for every exact ID. The
Stage 4 input manifest also reproduces all four ordered classification arrays
exactly.

## Independent classification judgment

The classifications follow from the frozen source, not from the manifest
rationales:

- Lines 17–22 are the base case and constructor-decreasing recurrence of the
  named mathematical scanner summary `runSpec`.
- Lines 24–27 are constructor projections from the named `scanState` summary.
- Line 28 defines the named top-level summary `separateSpec` by initializing
  `runSpec` and projecting the output.

All of these heads are declared `[function]` in `verification.k` lines 10–15.
They name summaries, recurrences, or projections, which meets the required
definition category.

By contrast, the operational semantics in `semantic.k` lines 128–199 rewrites
the `<k>`, `<env>`, `<functions>`, `<input>`, and `<result>` cells to load,
invoke, loop over, evaluate, mutate, append, and return from the translated
Python AST. None of the 11 inventoried rules matches an operational cell or
preempts an operational construct. `runSpec` is used as the mathematical
postcondition summary while the Stage 1 claims execute the AST; it is not an
operational bridge.

No entry can be `PROVED_DERIVED_LEMMA`. The inventoried entries are K rules,
not claims, and Stage 1 does not first prove any exact rule against a module
without it and later add it for a subsequent proof. The two reachability claims
reside in `spec.k` and are checked only after all 11 definitions are compiled.

No entry states an independent domain fact. Thus the independent counts are:

- `DEFINITION`: 11
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

There are no `simplification` attributes, so the special simplification
classification restriction is satisfied vacuously.

## Frozen-input and tree hashes

All launcher-recorded hashes with corresponding mounted inputs match:

| Object | Recomputed SHA-256 | Result |
|---|---|---|
| Stage 1 workspace, pipeline tree algorithm | `2912ea3c0e4486e103d25d57ade56084b7f5534d35b8782cb3fc9a08c479138b` | Match |
| Stage 1 workspace, deterministic-export tree algorithm | `f7198173f419636cacf3c009694d458c1c8113750de230e115a8bdfd24289f83` | Match |
| Selected Stage 2 audit tree | `3ab68ecc6de59b23c1b683246120c2713b070f395f90187f23b8b0039828af9c` | Match |
| Selected Stage 4 generation tree | `ed3e571d636bf69faabef69f98765174f72b54325fc602c91e65a752f466f35a` | Match |
| Generated Lean project tree | `ec2cabdd88613df091a482f8974a0b9be67d75d3d97827da8ff6ac78ae163e7a` | Match |
| Discovery manifest | `1d658f9f3f836cd96386a95bf89aa4d0ae7883a6c174f3fd3bb21487b68e0357` | Match |
| Generated obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` | Match |
| Trust inventory | `b52c40d9bb8196c1e9a497db5e90d91f26dd670ff21803ccf508394f3c3de2ea` | Match |

The complete 15-path `stage1_source_hashes` map matches exactly: no missing,
extra, or changed path. Both selected `artifact_sha256` values match their
recomputed Stage 2 and Stage 4 trees. The generator’s Stage 1, discovery,
inventory, generated-tree, toolchain-lock, obligation-map, and trust-inventory
bindings all match.

The two generation-code provenance fields are the exception:

| Manifest field | Recorded generation-time hash | Current trusted audit-tool hash |
|---|---|---|
| `exporter_sha256` | `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0` | `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0` |
| `klean_py_sha256` | `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13` | `92e9515ae1e4c5275b0cd366e5ff5c16ad35af1afdaf070ef1ae7c0980998964` |

The current hashes are exactly those pinned in the trusted mechanical-checker
lock. The manifest records a distinct generator image ID, but that image’s
source files are not among the mounted inputs. Therefore these fields are not
evidence that the current trusted source produced the artifact and cannot be
recomputed against their purported historical objects.

## Stage 4 preflight, obligation bijection, and target identity

I reran
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
`/reference/k-proof`, `/reference/lemma-discovery.json`,
`/reference/klean-generation`, and the pinned toolchain lock.

The first run reached the Lean build step but failed because this sandbox’s PID
namespace does not expose `/proc/<namespace-pid>/exe`, which Lean 4.22 uses to
locate its application. I compiled an audit-local compatibility shim that only
redirects numeric `/proc/<pid>/exe` `readlink` calls to `/proc/self/exe`.
With that recorded shim preloaded, `lean --version` reported Lean 4.22.0 at
commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock,
and the unchanged trusted checker completed.

The returned evidence exactly matches the selected recorded preflight:

- Status: `KLEAN_NO_OBLIGATIONS`
- Obligation count: 0
- Target: `null`
- Trust declaration count: 44
- Designated sorry count: 0
- `lake clean`: exit 0, empty output,
  SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `lake build`: exit 0, output SHA-256
  `669037f0d20098cd4e0488a046a50dee67e38e9994f982b51afd0bd6f01a0ee7`;
  all generated modules built successfully

I also ran the trusted final mechanical gate in classification-only mode. It
returned `status: PASS`, `target: null`, `candidate_sha256: null`,
`used_axioms: []`, and explicitly left semantic classification to this review
as `NOT_EVALUATED`.

The independently classified domain-source list is `[]`.
`obligation-map.json` has:

- `source_rules`: `[]`
- `obligations`: `[]`
- `trust_parameters`: `[]`

The lists are exactly equal and ordered, the obligation-ID list is unique, and
the generator manifest and export result both record count zero. There are no
conjuncts that could be weakened, irrelevant, duplicated, or vacuous.

The trusted target extractor returns `null`; the expected target definition is
also `null`; the generator manifest and audit input both record `null`; and an
independent scan finds no `def targetStatement` in any generated Lean file.
`Lemmas.lean` contains only its import and an empty namespace. Thus the fixed
generated target has not been changed—it is absent exactly as required for a
genuinely empty domain set.

The generated project has no `sorry`, `admit`, or `unsafe` token and no
symlink. Its 44 non-propositional generated trust declarations are exactly
accounted for by `trust-inventory.json` and were reconciled by the trusted
preflight. Because there is no target proposition, none supplies a proof of an
obligation.

## Stage 5

Proof-mode checks were intentionally not run. The launcher selected
`CLASSIFICATION_ONLY`, the fixed target is absent, `target.parameters` is
empty, `/candidate` does not exist, and both Stage 5 fields in the signed input
are null. This is the required state for `KLEAN_NO_OBLIGATIONS`, not a missing
proof candidate.

## Evidence

Key raw evidence:

- `evidence/00-provenance-snapshot.txt`
- `evidence/04-frozen-stage1-sources.txt`
- `evidence/05-inventory-reconstruction.json.txt`
- `evidence/14-stage4-check-generation.txt` (initial environment failure)
- `evidence/32-lean-compat-build-and-test.txt`
- `evidence/33-stage4-check-generation-success.txt`
- `evidence/37-mechanical-checker-lock.txt`
- `evidence/38-mechanical-tool-file-hashes.txt`
- `evidence/40-generated-target-and-token-scan.txt`
- `evidence/41-independent-classification.md`
- `evidence/42-hash-and-generation-audit-complete.txt`
- `evidence/45-trusted-final-mechanical-gate.txt`

VERDICT: CONCERNS
LEGITIMACY: LEGIT
