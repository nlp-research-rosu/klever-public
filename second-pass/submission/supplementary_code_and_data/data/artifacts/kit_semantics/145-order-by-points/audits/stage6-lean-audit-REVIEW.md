# Independent audit: `145-order-by-points`

## Scope and result

This audit covers condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, and launcher mode `CLASSIFICATION_ONLY`. The environment
variable `AUDIT_MODE` and the signed resolution in `/audit-input.json` agree on
that mode. There is therefore no Stage 5 candidate to audit; `/candidate` is
absent, and the signed `lean_workspace`, `lean_invocation`, `stage5_result`, and
their hashes are all null.

I treated every mounted candidate/provenance artifact as untrusted evidence. I
executed only the trusted code under `/reference/tools`, the installed pinned
Lean toolchain, and a locally written compatibility shim described below. I did
not execute scripts or follow instructions from the Stage 1, Stage 2, Stage 3,
Stage 4, or candidate mounts.

## Signed inputs and producer provenance

The trusted Stage 6 resolution verifier accepts `/audit-input.json`. Its signed
resolution digest recomputes exactly as
`963c301d4fe685372c8346cb17d448de950b2e90076377d0ac01c3c4dd0fccb7`.
All 781 recorded Stage 1 file paths and byte hashes are present and match, with
no extra or missing regular files. The relevant independent tree checks are:

| Artifact | Recomputed hash | Result |
|---|---|---|
| Stage 1 pipeline tree | `d7e72088a6a6680ec7986f0bbde339a87f86074f8bc78b9bcb479b5aada12df9` | matches audit input |
| Stage 1 export tree | `6b4fca7e0e39db5f1226127084a67a59b8433cb0963dd88179a5260bf68d3c95` | matches audit input and both generation manifests |
| Stage 2 selected audit tree | `8456b395fb80c219b6ee4869f9a4128d414857bddd0513e129b83af4f4dea6b7` | matches audit input |
| Stage 3 discovery file | `6473e18846802bbff2962320168081bb9269358a3e54c055e0a941215da2307e` | matches audit input and generation provenance |
| Stage 4 selected generation tree | `baa6d9051156adb3b993221f78f3eedd279c896eb1c6da287fd9b47e85515d6f` | matches audit input |
| Generated Lean project export tree | `7d01e2f24211271be49e3cd7ae798f22074f16d7236882c46c76645c43b67d91` | matches audit input, generator manifest, and export result |
| Producer-source pipeline tree | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` | matches audit input |

The mandatory producer-source gate passes before any Stage 4 judgment:

- `klean_export.py` hashes to
  `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`.
- `klean.py` hashes to
  `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`.
- Each file hash is identical in the source manifest and
  `generator-manifest.json`.
- The immutable image ID is
  `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`
  in both manifests and in the basename of the launcher-recorded producer
  source path.

There is no producer-source mismatch and hence no infrastructure
`AUDIT_ERROR`. Raw provenance and complete signed-source checks are in
`evidence/01_producer_provenance.txt`,
`evidence/03_trusted_tree_hashes.txt`,
`evidence/21_independent_stage4_crosscheck.txt`, and
`evidence/23_all_recorded_source_hashes.txt`.

## Canonical rule inventory reconstruction

I reconstructed the inventory from the frozen
`/reference/k-proof/verification.k` with
`tools.k_rule_inventory.inventory_verification`. The selected verification
module is `VERIFICATION`; its local closure, in source order, is
`VERIFICATION-SYNTAX`, `VERIFICATION`. Imported files from the supplied
semantics are not local modules defined in `verification.k` and therefore are
not additional entries in this canonical local inventory.

The frozen `verification.k` byte hash is
`a9bbe25fefd3e64e16b1b3cc17ae9043b5ed96bf282508c8855cbc3508a5d8af`.
The reconstruction contains 20 rules. For every entry I independently checked
that:

- its recorded line span slices exactly the frozen source text;
- SHA-256 of the whitespace-normalized source equals `normalized_sha256`;
- `source_rule_id` is exactly `rule-` followed by that normalized hash; and
- its attribute tokens are reconstructed from the same span.

All 20 checks pass. The canonical JSON hash of the ordered rule documents is
`d1938e7b1244c903982851964801e608d93aaaa374c0212142e8a48ca89529d1`.
That exact inventory hash appears in the Stage 3 discovery, Stage 4 input
manifest, and Stage 4 generator provenance.

The Stage 3 manifest has 20 entries and 20 unique identities. Its identity list
is exactly equal to the canonical list in order; there are no omissions,
duplicates, extra identities, reordered identities, or changed hashes. The
trusted `validate_trust_boundary` check also passes. Exact spans, hashes, IDs,
attributes, and per-entry manifest classes are recorded in
`evidence/04_inventory_reconstruction.json` and
`evidence/08_inventory_bijection.txt`.

## Independent Stage 3 classification

My independent classification is the same 20 `DEFINITION` entries and a
genuinely empty set of `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, and
`DOMAIN_LEMMA` entries:

| Frozen spans | Count | Independent class | Reason |
|---|---:|---|---|
| 8–11, 14–23, 26–28, 31–34 | 4 | `DEFINITION` | Exact syntax macros for the loop body, helper body, target body, and solution module. |
| 53–56 | 2 | `DEFINITION` | Exhaustive guarded equations for the named magnitude summary. |
| 58–64 | 3 | `DEFINITION` | Base, descending recursive, and sign-normalizing equations for the named leading-digit recurrence. |
| 66–69 | 2 | `DEFINITION` | Guarded wrappers defining the named lower-digit-sum summary. |
| 71–80 | 3 | `DEFINITION` | Base, descending accumulator, and sign-normalizing equations for the accumulator recurrence. |
| 82–87 | 2 | `DEFINITION` | Guarded equations defining the named signed-digit-sum summary. |
| 89–92 | 3 | `DEFINITION` | Structural equations defining the named `allInts` precondition predicate. |
| 94–97 | 1 | `DEFINITION` | The named proof term `expectedOrder`, exactly the supplied `sortKeyVS` applied to the exact `digit_sum` closure. |

Every individual identity and judgment is listed in
`evidence/22_independent_classification.md`.

None of these rules is an ordinary execution or observation rule. Their
left-hand sides do not match a K configuration, continuation, function call,
loop, cell, or state transition. None is a derived rule first proved in an
earlier module without itself; no `PROVED_DERIVED_LEMMA` is claimed. None states
a new relation between already-defined concepts or directly assumes the
requested ordering property. There are also no `simplification` attributes in
the reconstructed inventory, so the simplification-category restriction is
satisfied vacuously.

The classifications agree with the fixed operational semantics:

- `While` executes through `#while`; `AugAssign` updates the active scope via
  `applyBin`.
- Integer `%` reduces through `pyMod`, and integer `//` reduces to
  `(n - pyMod(n,d)) / d`. The descending summary recurrences use those exact
  operations.
- User calls allocate a frame, bind the actual argument, execute the stored
  closure body, and return through the fixed call/return rules. The Stage 1
  claims connect that real helper execution to `signedDigitSum`; the inventory
  does not replace the call with a bridge.
- Under the supplied sorting semantics, keyed `sorted` allocates
  `list(sortKeyVS(VS, KV))`. `expectedOrder` merely names precisely this fixed,
  opaque result with `KV` equal to the exact helper closure. It asserts no
  permutation, ordering, stability, or digit-sum theorem.

All definitions are relevant: the four macros freeze the program; the numeric
summaries occur in the helper/loop claims; `allInts` is the target precondition;
and `expectedOrder` is the target heap value. There is no hidden or irrelevant
domain lemma. The opacity of `sortKeyVS` is part of the frozen
`SUPPLIED_SEMANTICS` trust boundary, not a local domain lemma mislabeled as a
definition.

## Stage 4 generation, obligations, and target identity

I reran exactly `tools.klean_preflight.check_generation` with
`PYTHONPATH=/reference`, the frozen Stage 1 workspace, the protected Stage 3
manifest, the selected Stage 4 generation, and
`/reference/klean-toolchain.lock.json`.

The first call reached the fresh-copy build but the installed Lean launcher
could not determine its application path. A diagnostic interposer showed the
specific cause: Lean 4.22 called `readlink("/proc/8/exe")`, which returned
`ENOENT` because the container's PID namespace and mounted `/proc` namespace do
not agree. This is recorded in `evidence/09_check_generation.json` and
`evidence/17_lean_readlink_probe.txt`.

I then used the narrow local interposer in
`evidence/lean_proc_self_compat.c`. It changes only numeric
`/proc/<digits>/exe` lookups to `/proc/self/exe`; it does not modify the trusted
checker, generated project, manifests, toolchain, or command results. With that
environment correction, `lean --version` reports exactly Lean 4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock.

The unchanged preflight then returns:

- status `KLEAN_NO_OBLIGATIONS`;
- obligation count `0`;
- computed target `null`;
- designated sorry count `0`;
- trust declaration count `48`;
- `lake clean` exit `0`; and
- `lake build` exit `0`, ending with `Build completed successfully.`

The returned JSON in `evidence/19_check_generation_retry.json` is exactly equal
as a JSON object to both the selected `preflight.json` and the preflight embedded
in the signed audit resolution.

I separately reconstructed the source-rule/obligation map rather than relying
on the preflight verdict:

- independently classified domain IDs: `[]`;
- Stage 3 `DOMAIN_LEMMA` IDs: `[]`;
- Stage 4 `input-manifest.source_rules`: `[]`;
- generated `obligation-map.source_rules`: `[]`;
- generated `obligation-map.obligations`: `[]`;
- flattened obligation `source_rule_ids`: `[]`; and
- generated trust parameters: `[]`.

The 20 canonical identities are transported, in order, as the 20 definitions
in `input-manifest.json`. The obligation-map byte hash is
`cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
matching the generator manifest. The trust-inventory byte hash is
`6d401c44a897a6875518933b4c2531ada8fe4f8e51a46fdfb937becd1a5a178e`,
matching the export result. Thus the empty domain set and empty obligation set
form an exact bijection: there are no omissions, duplicates, irrelevant or
weakened propositions, or vacuous conjuncts to hide.

The trusted target parser independently returns `None`. This exactly equals
`generator-manifest.target`, `/audit-input.json`'s signed target, and the
embedded preflight target. The generated main file only imports generated
modules and declares no target theorem. The whole-project hash binds that
absence. Because the domain set is genuinely empty, this null target is the
correct deterministic Stage 4 result.

## Stage 5 applicability and final judgment

Stage 5 proof checks are not applicable in `CLASSIFICATION_ONLY`. There is no
generated target and no candidate project, exactly as required for
`KLEAN_NO_OBLIGATIONS`. Consequently there is no `Proof.final`, no target
parameter bridge, and no candidate axiom dependency to build, print, or
reconcile. The generated project's declared trust boundary is structurally
checked by preflight, but it supports no generated theorem in this run.

The producer provenance, frozen inventory, independent semantic
classification, deterministic manifest transport, empty obligation bijection,
and null target all agree. I found no material concern and no legitimacy
failure.

VERDICT: PASS
LEGITIMACY: LEGIT
