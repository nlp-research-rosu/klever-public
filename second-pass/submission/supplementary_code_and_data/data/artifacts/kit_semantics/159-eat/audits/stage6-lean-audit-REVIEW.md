# Independent audit: HumanEval 159-eat

## Decision

The selected Stage 3 classification and Stage 4 `KLEAN_NO_OBLIGATIONS` result are correct. The frozen verification module introduces no local K rules at all, so its true `DOMAIN_LEMMA` set is genuinely empty. Stage 4 preserves that empty set bijectively and generates no Lean target. The launcher selected `CLASSIFICATION_ONLY`; no Stage 5 workspace or candidate exists.

I treated the prior Stage 2 review, candidate/provenance prose, comments, and recorded PASS statuses only as untrusted evidence. No earlier verdict or classification was used as semantic authority.

## Scope and mode

- Problem: `159-eat`
- Condition: `kit-semantics`
- Semantics mode: `SUPPLIED_SEMANTICS`
- `/audit-input.json` mode: `CLASSIFICATION_ONLY`
- `AUDIT_MODE`: `CLASSIFICATION_ONLY`
- Recorded Stage 4 selection: `KLEAN_NO_OBLIGATIONS`
- `/candidate`: absent
- Recorded Lean workspace, Lean invocation, and Stage 5 result: all null

The mode and absence checks are reproduced in `evidence/02-integrity.log`.

## Frozen-input and producer integrity

I recomputed the pipeline tree digests, deterministic-export tree digests, individual producer hashes, sidecar hashes, and all 771 recorded Stage 1 per-file hashes. There were no missing, extra, or changed Stage 1 files.

| Binding | Recomputed and recorded value |
|---|---|
| Stage 1 full workspace tree | `faac9ac7e5e43b3ad53cf71aaa107c13b00b07afc507263c5182611a5f20a966` |
| Stage 1 deterministic-export tree | `e1f81560ae8ebe1b11555352cb6ced8355e305a1a7aca65c79df8309db1519df` |
| Stage 2 selected audit tree | `1fa50d6675b5a697e93a8ee82e39f9e3427122f905f8df50bf82388ffed2f05e` |
| `verification.k` | `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4` |
| Stage 3 manifest | `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3` |
| Stage 4 selected generation tree | `97c00bbc015ff6ce72f0bb345c195d026062b3ddaca100391b976e06901bc589` |
| Generated project tree | `2f27af05a7a45d08766f8ffc656432f28bfc86fc8d0c64f1babedd59334b0ffc` |
| Producer-source bundle tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |
| Obligation map | `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048` |
| Trust inventory | `730176e40db0699ed978b20e323f7d5a14fcd27625fcf3f975010ef0ae391c1a` |

The producer bundle contains exactly `klean_export.py`, `klean.py`, and `source-manifest.json`. Both producer file hashes agree with the source manifest and `generator-manifest.json`. The generator image ID is consistently

`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`

in the generator manifest and source manifest; its digest component is also the immutable producer-source directory key recorded in `/audit-input.json`. Producer authentication therefore passes and there is no producer-source infrastructure error.

The detailed independent calculations are in `evidence/integrity_check.py` and `evidence/02-integrity.log`.

## Rule inventory reconstruction

Using the trusted `/reference/tools/k_rule_inventory.py`, I reconstructed the local verification-module closure from the frozen file. The complete file is only:

```k
requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
endmodule
```

The selected local module is `VERIFICATION`; its local closure is exactly `["VERIFICATION"]`. It contains no `rule` sentence. Consequently there are no per-rule source spans, normalized rule hashes, or `source_rule_id` values to omit, duplicate, reorder, or alter. The complete canonical rule document is `[]`, whose canonical SHA-256 is:

`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`

The protected Stage 3 manifest has the same inventory hash and an empty ordered `rules` list. Trusted boundary validation reports exactly:

- rules: 0
- definitions: 0
- operational rules: 0
- proved derived lemmas: 0
- domain lemmas: 0

Thus the reconstruction-to-manifest comparison is a bijection, including identity order, with no unaccounted classifications. Exact output is in `evidence/01-inventory.log`.

## Independent classification and mathematical judgment

There are no inventory entries to classify. In particular, Stage 3 claims no `DEFINITION`, `OPERATIONAL_RULE`, `PROVED_DERIVED_LEMMA`, or `DOMAIN_LEMMA`, and there is no `[simplification]` rule. The special requirements for simplification rules and previously proved derived rules are therefore satisfied without exception rather than bypassed by a mislabeled entry.

The empty domain set also agrees with the frozen program and proof structure. The source function has two exhaustive integer branches over the stated input bounds:

- if `need <= remaining`, return `[number + need, remaining - need]`;
- otherwise, equivalently `need > remaining`, return `[number + remaining, 0]`.

The two K claims state those exact outputs under the same `0..1000` parameter bounds and partition on `NEED <=Int REMAINING` versus `NEED >Int REMAINING`. They are execution claims, not a separate human-facing mathematical postcondition requiring a domain fact.

The supplied operational semantics handles the relevant execution directly: the closure-call rule binds parameters and executes the body; comparison dispatch maps integer `<=` and `>` to `<=Int` and `>Int`; `If` selects the corresponding statement sequence; integer `+` and `-` use `+Int` and `-Int`; list construction allocates the two evaluated values; and `Return` propagates the result through the call frame. `verification.k` adds no summary, macro, recurrence, derived rewrite, domain fact, or operational bridge on top of those rules. There is therefore no source- or postcondition-relevant domain lemma omitted from Stage 3.

The source, claims, and relevant operational rules are preserved in `evidence/05-program-semantics.log`.

## Stage 4 obligation bijection and target identity

The independently classified domain-rule IDs, input-manifest `source_rules`, obligation-map `source_rules`, and obligation IDs are all the same empty ordered list. The obligation map also has no trust parameters. All other Stage 3 rule categories recorded by the input manifest are empty.

Accordingly:

- expected target definition: null;
- parsed generated target: null;
- `generator-manifest.json` target: null;
- `/audit-input.json` target: null;
- proposition declarations in the fixed `Klean159Eat/Lemmas.lean` target module: none;
- generated obligations: 0;
- duplicate or omitted source IDs: none;
- weakened, irrelevant, or vacuous conjuncts: none.

This is not a conjunction replaced by `True`; no target proposition is generated at all. The generated boilerplate contains 41 collection-hook trust declarations matching `trust-inventory.json`, but there is no proposition or proof target for them to discharge. Trusted preflight separately rejects proposition trust and reports zero sorries.

The independent Stage 4 comparison is in `evidence/stage4_check.py` and `evidence/04-stage4.log`.

## Mechanical preflight

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required Stage 1 workspace, Stage 3 manifest, Stage 4 generation, and pinned toolchain lock.

The first invocation exposed an audit-sandbox compatibility issue: Lean/Lake 4.22 resolves its executable through `/proc/<own-pid>/exe`, while this sandbox exposes `/proc/self/exe` but not the numeric own-PID path. The unmodified checker therefore initially reached `lake clean` and failed to locate the Lake installation. I verified that discrepancy directly and compiled the narrow compatibility shim in `evidence/proc_self_exe_compat.c`, which redirects only `/proc/*/exe` `readlink` requests to `/proc/self/exe`. With that audit-only shim inherited by subprocesses, the pinned Lean installation identified itself as version 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.

The unchanged trusted checker then completed successfully on a fresh temporary copy. Its returned evidence was:

- status: `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0;
- `lake build`: exit 0, build completed successfully;
- Stage 1 export hash: matched;
- Stage 3 manifest hash: matched;
- generated tree hash: matched;
- obligation count: 0;
- target: null;
- designated sorry count: 0;
- trust declaration count: 41.

The checker also re-snapshotted every immutable input after the build. The complete initial failure, sandbox probe, shim command, pinned version, rerun command, and returned JSON are in `evidence/03-preflight.log`.

## Stage 5

Stage 5 is correctly absent because the independently confirmed Stage 4 status is `KLEAN_NO_OBLIGATIONS`. There is no generated target, `/candidate` does not exist, and the audit input records no Lean workspace, Lean invocation, or Stage 5 result. A candidate clean build, `Proof.final`, axiom print, or operational-bridge parameter audit would be inapplicable and would contradict the selected classification-only mode.

## Evidence index

- `evidence/01-inventory.log`: raw inventory reconstruction and protected-manifest comparison.
- `evidence/02-integrity.log`: raw tree, file, manifest, producer, target, and mode reconciliation.
- `evidence/03-preflight.log`: raw preflight commands and results, including the sandbox compatibility diagnosis.
- `evidence/04-stage4.log`: raw obligation bijection and target-absence checks.
- `evidence/05-program-semantics.log`: frozen source, claims, verification module, and relevant supplied-semantics rules.
- `evidence/inventory_check.py`, `evidence/integrity_check.py`, and `evidence/stage4_check.py`: reproducible independent audit code.

VERDICT: PASS
LEGITIMACY: LEGIT
