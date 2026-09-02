# Independent audit: HumanEval `69-search`

## Scope and decision

The launcher and signed resolution both select:

- condition: `bare`
- semantics mode: `GENERATED_SEMANTICS`
- audit mode: `CLASSIFICATION_ONLY`
- selected Stage 4 status: `KLEAN_NO_OBLIGATIONS`

I treated the mounted Stage 1–Stage 4 artifacts and the earlier Stage 2 review as untrusted evidence. I did not rely on any earlier verdict or classification. I used the trusted code under `/reference/tools` for canonical inventory reconstruction, deterministic-generation preflight, and the final mechanical gate, and separately made the semantic classification judgment described below.

The independent result is that the sole inventory rule is a legitimate `PROVED_DERIVED_LEMMA`. Therefore the true `DOMAIN_LEMMA` set is empty, the empty Stage 4 obligation set is correct, no generated target should exist, and no Stage 5 project should exist.

## Input and producer authentication

The signed audit-input envelope validated with canonical digest:

`6db674d8ed06dfc29093ae2137aea6e84a916a3452c01edaafb493ca793fb810`

I recomputed all signed resolution hashes with the corresponding trusted digest algorithm:

| Artifact | Recomputed digest |
|---|---|
| Stage 1 pipeline tree | `19fbe222eac441c9cc3d6beafe115b45a9d14ab9eed79e11c92d1e4bdd704966` |
| Stage 1 export tree | `e67e7eb440b2ce1bfdb25fcf94d947eadd3a16c6698a34f5fbc0cd3c1b07bfdb` |
| Stage 2 selected audit tree | `d8f0020287ff73018da84b6167258097b13af93f81dcea7777b0182915e2ec87` |
| Stage 3 manifest | `dc4c345764b8308f2131c6dcfaf2bb4227218908c361d9c628fa9af91639a2ef` |
| Stage 4 selected generation tree | `cef679436d34ef207624e5e100ee386e3c0c83766218ede1ca3e0a9064de8f4c` |
| Generated Lean project tree | `4effc42a6a6a820a371f4c844c84ce22c19dc902365b7245949bf1b4fe213baf` |
| Generation producer-source bundle | `363d98891cb09c42f1719e3632b09413274cb5603460fa8823003da0ffba11b0` |

The complete per-file Stage 1 hash map also equals `resolution.stage1_source_hashes`. The selected Stage 2 and Stage 4 artifact hashes equal their signed selection records. The signed copy of the Stage 4 preflight is JSON-equivalent to `/reference/klean-generation/preflight.json`.

Before judging Stage 4, I directly hashed the two mounted generation-time producers:

- `klean_export.py`: `235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0`
- `klean.py`: `ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13`

Both hashes equal the fields in `generator-manifest.json` and the exact file map in `source-manifest.json`. The source manifest contains only the required schema, image ID, and those two file hashes. Its image ID,
`sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda`,
equals the generator provenance and the immutable producer-bundle identifier recorded in `/audit-input.json`. The bundle has exactly the two producers plus `source-manifest.json`. There is no producer-source mismatch and therefore no infrastructure `AUDIT_ERROR`.

Raw results are in `evidence/08-provenance-and-producer-authentication.log`.

## Canonical inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` implementation and independently recomputed each returned span, normalized hash, source ID, and the canonical JSON inventory hash.

The reconstructed inventory is:

- verification file SHA-256: `d5265cb157801d669c5ee7e2174692b3d6a60dbe15fe7ae4391c5bf2cd3ea8a1`
- selected module: `VERIFICATION`
- local module closure in `verification.k`: `[VERIFICATION]`
- rule count: 1
- source span: lines 8–16
- normalized SHA-256: `9c0f13f3d959c4d25eeabaa331cdf4ff8c0471110b739b101cee0ce8e9d29e31`
- source rule ID: `rule-9c0f13f3d959c4d25eeabaa331cdf4ff8c0471110b739b101cee0ce8e9d29e31`
- attributes: `[priority(40)]`
- inventory SHA-256: `399877c7e577f85227443d33c6d781cbcbfaa3e241b6932903fc17814bf36314`

The reconstructed source text exactly equals the recorded physical span. The protected Stage 3 manifest has exactly one entry with the same ID in the same order and the same inventory hash. Both sides are duplicate-free and their ordered lists and identity sets are equal. Thus there are no omitted, extra, duplicated, reordered, changed, or unclassified rules. See `evidence/01-inventory-reconstruction.log`.

The sole rule has no `simplification` attribute, so the simplification-only restriction is not implicated.

## Independent classification judgment

### Rule meaning

The rule consumes the remaining `loop("value", IS, searchLoopBody)` followed by the function return. It clears the environment and returns `VInt(scan(L, IS, A))`, where `A` is the current answer and `L` is the original list.

It is not a `DEFINITION`: it does not introduce equations for a summary symbol or macro. Considered without its prior proof, it would be an execution-replacing bridge, not an ordinary small-step `OPERATIONAL_RULE`. It is nevertheless a valid `PROVED_DERIVED_LEMMA` because the exact reachability body is first proved without this rule and only then reused.

### Exact prior proof and exclusion

The body of the rule is whitespace-normalization-identical to the body of the `[loop-invariant]` claim in `loop-lemma-spec.k`; only the sentence header and the later rule priority differ.

That claim requires and imports `VERIFICATION-CORE`, not `verification.k` or `VERIFICATION`. Neither `verification-core.k` nor `semantic.k` contains the derived rule. The Stage 1 sequence places:

1. compilation of `VERIFICATION-CORE`;
2. `kprove loop-lemma-spec.k` against that core;
3. compilation of `verification.k`, which adds the proved rule; and
4. the later end-to-end proof.

I independently replayed this sequence in `/tmp/audit-work/stage1-recheck`:

- core compilation: exit 0;
- loop claim against the rule-free core: `#Top`, exit 0;
- later `VERIFICATION` compilation: exit 0;
- final `spec.k`: `#Top`, exit 0.

The exact outputs are in `evidence/04-compile-verification-core.log` through `evidence/07-prove-final-spec-with-derived-rule.log`.

The proof is discriminating. An independent off-by-one mutation changed the result to `scan(L, IS, A) +Int 1`; `kprove` rejected it with exit 1 and a stuck implication containing `A #Equals A +Int 1`. See `evidence/14-reject-false-derived-lemma.log`.

### Operational and mathematical correspondence

The frozen semantics executes each remaining element by:

1. binding `value` to the head element;
2. testing `count(value, L) >= value`;
3. testing `value > answer`;
4. updating `answer` only when both tests pass;
5. recurring over the remaining list; and
6. returning and clearing the environment.

`promote(L, I, A)` has exactly those two complementary guarded branches. `scan(L, .Ints, A) = A`, while `scan(L, cons(I, IS), A)` recurs with `promote(L, I, A)`. The recurrence decreases structurally on `IS`; its guards are exhaustive and disjoint. It therefore matches the source loop and the rule's complete result, binding, continuation, and environment effects. The prior bridge-free reachability proof establishes this universally.

As an additional adversarial sanity check, I compared the recurrence with an independently written imperative reading of the source over 121,680 states, including negative, zero, and positive values; there were no mismatches. All prompt examples matched. A strict-frequency counterfactual fails on `[2, 2]`, and a constant `-1` counterfactual fails on `[1]`. These finite checks support, but do not replace, the universal K proof.

The lemma is directly relevant: `searchSpec(L)` is `scan(L, L, -1)`, and the source/postcondition result depends on completing exactly this loop and return. It is not an unproved mathematical `DOMAIN_LEMMA` hidden under another label.

The independent classification is therefore:

- `DEFINITION`: 0
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 1
- `DOMAIN_LEMMA`: 0

Detailed semantic checks are in `evidence/15-stage3-stage4-semantic-audit.log`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required Stage 1, Stage 3, Stage 4, and toolchain-lock paths.

The audit container initially exposed a PID-namespace mismatch: Lean uses `/proc/<pid>/exe`, while this container's `/proc` exposes another PID namespace. The first attempts consequently failed before elaboration. I diagnosed this independently and used a narrow preload shim that redirects only `/proc/<pid>/exe` lookups to `/proc/self/exe`; it does not alter any input, Lean source, generated source, or theorem. Under the pinned Lean 4.22.0 installation, the unchanged trusted preflight returned:

- status: `KLEAN_NO_OBLIGATIONS`
- `lake clean`: exit 0, empty output
- `lake build`: exit 0
- build-output SHA-256: `4c6bf2303b1aa3be71a00246267c7e976a18a372fdfacd58195d7bd842e62271`
- obligation count: 0
- target: null
- designated sorry count: 0
- trust-declaration count: 44

The successful build output hash and text exactly match the signed Stage 4 preflight. The failed environmental attempts remain visible in `evidence/09-rerun-klean-preflight.log`, `evidence/11-lake-project-diagnostics.log`, and `evidence/12-rerun-klean-preflight-with-pinned-env.log`; the successful returned evidence is `evidence/13-rerun-klean-preflight-success.log`.

Because the independently classified domain set is genuinely empty:

- `input-manifest.json` has an empty domain `source_rules` list;
- `obligation-map.json` has empty `source_rules`, `obligations`, and `trust_parameters`;
- the empty source-rule/obligation bijection is exact and duplicate-free;
- the obligation-map hash is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`;
- every manifest count is zero;
- the expected-target generator returns no definition;
- the trusted target parser returns no target;
- the generator manifest, preflight, and signed audit input all record target `null`;
- there is no generated `Target`, `Proof.final`, weakened duplicate, or vacuous `Target := True`.

The 44 generated executable-boundary axioms exactly match `trust-inventory.json`; preflight rejects proposition trust and found no `sorry`, `admit`, or `unsafe`. Since no target or proof exists, none is used to prove a proposition.

Finally, the trusted Stage 6 mechanical gate passed in classification-only mode, rebound all signed inputs, reran preflight, returned target `null`, candidate `null`, and an empty used-axiom list. Its raw result is `evidence/16-final-mechanical-gate.log`. As the gate itself states, semantic classification is model-owned; that independent judgment is supplied above.

## Stage 5

Stage 5 is correctly absent. `/candidate` does not exist, all signed Lean workspace/invocation hashes are null, `stage5_result` is null, and there is no generated target to prove. A `Proof.final` build, axiom print, or operational-parameter bridge audit would be inappropriate in this `CLASSIFICATION_ONLY` case.

## Evidence index

The principal raw command/result records are:

- `evidence/01-inventory-reconstruction.log`
- `evidence/03-stage1-source-hashes.log`
- `evidence/04-compile-verification-core.log`
- `evidence/05-prove-loop-derived-lemma.log`
- `evidence/06-compile-verification-with-derived-rule.log`
- `evidence/07-prove-final-spec-with-derived-rule.log`
- `evidence/08-provenance-and-producer-authentication.log`
- `evidence/13-rerun-klean-preflight-success.log`
- `evidence/14-reject-false-derived-lemma.log`
- `evidence/15-stage3-stage4-semantic-audit.log`
- `evidence/16-final-mechanical-gate.log`

VERDICT: PASS
LEGITIMACY: LEGIT
