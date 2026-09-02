# Independent Stage 3/4 Audit: HumanEval `91-is-bored`

## Result and scope

The launcher records problem `91-is-bored`, condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, and audit mode `CLASSIFICATION_ONLY`. The environment variable `AUDIT_MODE` agrees. Consequently this review covers the Stage 3 rule classification and deterministic Stage 4 generation. Stage 5 is not applicable: `/candidate` is absent, the Stage 5 result and both Lean workspace/invocation hashes are null, and there is no generated target to prove.

I treated all mounted prose, logs, and prior conclusions as untrusted evidence. The conclusions below come from the frozen sources, trusted inventory/preflight code, independently recomputed hashes, and fresh K/preflight runs. Raw commands and complete captured results are in `evidence/`.

## Frozen input integrity

The trusted Stage 6 input verifier recomputed `resolved_input_sha256` as `66f4ca6f6bf9e00778f64c7fd087bed79399d51f1286c7519fb41dad873fdaa1`, exactly the value in `/audit-input.json`.

All nine top-level resolution hash fields match their mounted inputs, including the two null Stage 5 hashes. In particular:

- Stage 1 pipeline tree: `1b7903fd0e3dfc5041d94521e0b47680d242ae98330d5c3abffc331baa9cbd12`;
- frozen Stage 1 export tree: `814462a3d1fd64114185d9ec2123e2b97d1b707ae547ee8a9867dc53074055d5`;
- Stage 3 manifest: `6fb493d197604bf499e7beca779dc604d350a8ef3c8f9d38ee9a5466dea52a98`;
- generated project: `314fa5fffb99e54ce7c5738ad2422758eedb53d8076be863efdc35a0cdb89dd1`; and
- selected Stage 4 generation: `8244fa19acec0720f04cb150f1e938857a1b54376f2d5c2e82a9da1db59219e1`.

The independently rebuilt per-file Stage 1 source map has 870 entries, exactly the recorded 870 entries, with no missing paths, extra paths, or hash mismatches. See `evidence/04_audit_input_hashes.txt`.

## Rule inventory reconstruction and Stage 3 bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` on `/reference/k-proof`. `prove.sh` selects `VERIFICATION`; the local module closure inside `verification.k` is exactly `["VERIFICATION"]`. The reconstruction found exactly one rule:

| Field | Independently reconstructed value |
|---|---|
| source span | `verification.k:8-52` |
| module | `VERIFICATION` |
| attributes | `priority(40)` |
| normalized SHA-256 | `202b06d05541325e5aaf0e76d47ae510afce49eaa2aabb95863e7e1250b712ef` |
| source rule ID | `rule-202b06d05541325e5aaf0e76d47ae510afce49eaa2aabb95863e7e1250b712ef` |
| whole inventory SHA-256 | `c52fa2a5b96c79c46b9f6eea4cc8d3d034a6a20c005da213b247fb8b3b3d5577` |

The protected Stage 3 manifest has one classification record with that same ID and the same inventory hash. The ordered ID lists are equal and individually unique; there are no omissions, duplicates, extras, reordered identities, or unaccounted entries. The full reconstructed rule and comparison are in `evidence/01_inventory_reconstruction.txt` and `evidence/02_inventory_stage3_bijection.txt`.

## Independent classification judgment

Stage 3 labels the sole rule `PROVED_DERIVED_LEMMA`. That classification is correct.

The rule summarizes the exact `#loop(str(IS), Name("c"), BORED-LOOP-BODY)` configuration, exact post-loop `If`/`Return`/`#endcall` continuation, bindings, scopes, heap, stack, return, exception, and exit-code state as `scanResult(IS,N,A,P)`. It is not an ordinary source-language execution rule and it is not a definition of a new named summary. By behavior it accelerates operational execution, but it qualifies as a proved derived lemma because its entire reachability statement was proved before the rule was installed.

Specifically, `loop-spec.k` requires and imports only `VERIFICATION-BASE`, while the installed rule resides in the later `VERIFICATION` module. After removing the `rule` versus `claim [loop]:` header and the installed rule's operational priority attribute, the normalized logical cores are identical: both have SHA-256 `d3d6e3d6d75a51568c7927c2e6dab9de5d5f0f28007aa99d9256e3fecdd21fd` and length 809 characters. The priority attribute affects later rewrite selection, not the theorem statement.

The frozen `prove.sh` uses `set -e` and orders the proof correctly: it compiles `verification-base.k`, proves `loop-spec.k`, only then compiles `verification.k` containing the reusable rule, and finally proves `spec.k`. Fresh reruns independently produced:

- bridge-free loop claim against `verification-base-kompiled`: `#Top`, exit 0;
- later target against `verification-kompiled`: `#Top`, exit 0; and
- the four bridge-free `strip()` comparison connection claims: `#Top`, exit 0.

The operational meaning also matches the frozen source. Supplied MPY semantics lowers `For` to `#loop`, string iteration yields one-code-point strings, and the source body updates `(count, at_start, pending_i)` exactly as `scanStep`; `finishScan` performs the source's final pending-`I` increment. The rule therefore directly summarizes the source loop used by the public `is_bored` claim and is relevant to both the source program and its result. A counterfactual module replacing the loop body with `.Stmts` fails at exit 1 with `WarnStuckClaimState` and a residual inequality between the unchanged scanner state and the required one-step scanner transition. This rules out a body-insensitive or vacuous summary.

There is no `simplification` attribute on the inventory rule. Thus the requirement that every simplification rule be a `DEFINITION` or `DOMAIN_LEMMA` is satisfied vacuously. The only inventory entry is a genuinely proved execution lemma, not a human-facing fact about the returned count, so the independently classified `DOMAIN_LEMMA` set is genuinely empty. Source mapping and fresh proof/mutation logs are in `evidence/05_derived_lemma_identity_and_order.txt` through `evidence/09_kprove_later_target.txt`, with operational excerpts in `evidence/14_operational_semantics_mapping.txt`.

## Generation producer provenance

I hashed the mounted generation-time producer sources before accepting Stage 4:

- `klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`;
- `klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.

Both hashes match `generator-manifest.json` and `source-manifest.json`. The producer bundle contains exactly those two regular files plus `source-manifest.json`; it has no extra or linked entries. Its launcher-algorithm tree hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, matching `/audit-input.json`. The immutable image ID is consistently `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` in the generator manifest and source manifest, and the digest is the basename of the producer path recorded in `/audit-input.json`. There is no producer-provenance `AUDIT_ERROR`. See `evidence/03_producer_provenance.txt`.

## Deterministic Stage 4 preflight and target identity

I reran the unmodified trusted `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, the required frozen workspace, Stage 3 manifest, Stage 4 generation, and `/reference/klean-toolchain.lock.json`.

The sandbox blocks Lean's normal `/proc/<pid>/exe` lookup, so the first diagnostic attempt could not locate the Lean application; that failure is preserved in `evidence/10a_preflight_sandbox_failure.txt`. For the recorded successful rerun I used a narrow preload shim that intercepts only process-executable `readlink` calls and returns the explicitly pinned `/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean` path. The shim source and hashes are recorded in `evidence/11_lean_sandbox_path_shim.txt`. With it, Lean independently reports version 4.22.0 and commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly the lock. The shim does not alter source reads, elaboration, kernel checking, compilation, or any generated file.

The preflight returned `KLEAN_NO_OBLIGATIONS`, exit 0. Its private-copy `lake clean` exited 0 and its `lake build` exited 0 after building all generated modules. The returned evidence binds the same Stage 1, Stage 3, and generated-tree hashes listed above, reports zero designated sorries, 41 allowlisted generated trust declarations, zero obligations, and `target: null`. See `evidence/10_klean_preflight_rerun.txt`.

I also checked the structural result independently of preflight:

- independently classified domain source rules: `[]`;
- `input-manifest.json` source rules: `[]`;
- `obligation-map.json` source rules, obligations, and trust parameters: `[]`, `[]`, and `[]`;
- obligation-map SHA-256: `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, matching the generator manifest;
- generator obligation count: 0;
- expected target definition: null;
- trusted parser's observed generated target: null;
- generator manifest target and `/audit-input.json` target: null; and
- `/candidate`: absent.

Thus the source-rule/obligation mapping is the exact empty bijection. There is no omitted true domain lemma, duplicate or irrelevant obligation, weakened/vacuous conjunct, or changed target. For this genuinely empty domain set, the fixed generated target is correctly the absence of a target. Internal sidecar, trust-inventory, toolchain, verification-source, and generated-tree bindings also all match; see `evidence/12_stage4_zero_obligation_bijection.txt` and `evidence/13_stage4_internal_hash_bindings.txt`.

## Stage 5 applicability

No Stage 5 candidate or proof may exist for `KLEAN_NO_OBLIGATIONS`, and none exists. Because the launcher mode is `CLASSIFICATION_ONLY`, candidate clean-build, `Proof.final` identity, axiom accounting, and operational-parameter bridge checks are not applicable rather than skipped requirements.

VERDICT: PASS
LEGITIMACY: LEGIT
