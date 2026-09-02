# Independent audit: HumanEval `93-encode`

## Outcome

The selected Stage 3 classification and deterministic Stage 4 result are legitimate. Both `/audit-input.json` and `AUDIT_MODE` select `CLASSIFICATION_ONLY`, so Stage 5 is not part of this audit. `/candidate` is absent, the Lean workspace and invocation hashes are null, and the recorded Stage 5 result is null, as this mode requires.

I treated all mounted candidate/provenance prose, logs, and earlier verdicts as untrusted evidence. The judgment below comes from the frozen sources, the locked verification tools, fresh hashing, independent rule classification, and a fresh preflight run.

## Producer provenance gate

I performed this gate before assessing Stage 4. The mounted producer files hash to:

- `klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Those values agree exactly with `generator-manifest.json` and `source-manifest.json`. The generator image is consistently bound as `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`: it appears in both manifests, and the protected producer-bundle path recorded by `/audit-input.json` ends in the same digest. The bundle contains exactly `klean_export.py`, `klean.py`, and `source-manifest.json`; its independently recomputed tree hash is `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, matching the audit input.

The trusted mechanical-checker lock itself hashes to `aadbd794398107ee2a918bf7c670ca8750bbbc246919a4aa6047cf597114828b`, matching the launcher record, and every one of its nine locked `/reference/tools` file hashes matches. There is no producer-source infrastructure error.

Evidence: [producer hashes and manifests](/audit-output/evidence/01-producer-provenance.results.txt), [independent producer comparison](/audit-output/evidence/04-producer-provenance-check.results.json), and [full locked-tool/hash audit](/audit-output/evidence/11-independent-hashes-and-bijection.results.json).

## Stage 3 inventory reconstruction

The frozen `verification.k` has SHA-256 `ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4`. `prove.sh` selects main module `VERIFICATION`. The trusted inventory implementation reconstructs the local verification-module closure as exactly `VERIFICATION`; the imported `MPY` module is supplied from a separate frozen semantics file and is not a local module in `verification.k`.

The local closure contains no rule sentences. Consequently there are no source spans, normalized rule hashes, or `source_rule_id` values to enumerate. The ordered reconstructed rule list is exactly `[]`, all uniqueness checks hold, and its canonical whole-inventory hash is `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`. `/reference/lemma-discovery.json` has exactly the same schema, ordered empty rule list, and inventory hash. This is an exact bijection: no omitted, duplicated, extra, reordered, changed, or unclassified rules exist.

Evidence: [frozen Stage 1 sources](/audit-output/evidence/02-stage1-sources.results.txt) and [fresh inventory reconstruction](/audit-output/evidence/03-inventory-reconstruction.results.json).

## Independent classification judgment

The independent classification counts are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 0 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

There are also zero local `simplification` rules. Thus the requirement that each simplification be a `DEFINITION` or `DOMAIN_LEMMA` holds without an unclassified case, and the true domain-lemma set is genuinely empty.

This empty result agrees with the frozen program and operational semantics, rather than merely with the protected manifest. `solution.py` computes `message.swapcase()` followed by ten ordered one-character replacements. The K claim executes the exact translated function body and states the result as those same ten nested `replaceC` applications over `mapSwap(CS)`, with the complete execution cells shown in the claim. The supplied semantics performs ordinary call, closure, parameter-binding, return, and method routing. In particular:

- `applyMethod(..., "swapcase", ...)` returns `str(mapSwap(CS))`; `mapSwap` recurses over the sequence and `swapC` implements the upper/lower/other cases.
- `applyMethod(..., "replace", ...)` returns `str(replaceC(CS,A,B))`; `replaceC` has exhaustive empty, equal-character, and unequal-character recursive equations.

These are frozen supplied-semantics rules, not proof-local rules added by Stage 1. Stage 1 contains no bridge, result oracle, postcondition lemma, or simplification shortcut to reclassify. There is therefore no relevant domain lemma that Stage 3 omitted or mislabeled.

Evidence: [operational semantics excerpts and simplification count](/audit-output/evidence/05-operational-semantics.results.txt) and [classification record](/audit-output/evidence/05-independent-classification.json).

## Stage 4 preflight and structural integrity

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` over exactly:

- `/reference/k-proof`
- `/reference/lemma-discovery.json`
- `/reference/klean-generation`
- toolchain lock `/reference/klean-toolchain.lock.json`

The first attempt exposed an audit-container PID-namespace defect: processes report an inner PID while `/proc` is mounted using the outer PID, causing Lean's executable-path lookup and then `lake clean` to fail. A small temporary `LD_PRELOAD` compatibility shim under `/tmp/audit-work` redirects only a `/proc/<numeric-pid>/exe` `readlink` to `/proc/self/exe`; it does not touch the generated tree, provenance inputs, or trusted checker. With that environment correction, Lean reports version 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, exactly matching the lock.

The rerun returned:

- status `KLEAN_NO_OBLIGATIONS`;
- `lake clean`: exit 0;
- `lake build`: exit 0, `Build completed successfully.`;
- Stage 1 export hash `3584a98a8fab06954382fdd706c280a04f86e17eabca5a4c3fc0e1610bf89728`;
- Stage 3 manifest hash `e13c01259eb807dd465c4db3e29a0727d9ce0eb8df88d145e8977e70f5b7fcf3`;
- generated tree hash `3b5ffce636adf98f384bb2327f23b74147104cec26152d372255f55acf382584`;
- obligation count 0;
- target null;
- designated sorry count 0; and
- 41 generated trust declarations, exactly reconciled by the preflight allowlist and rejected if proposition-like.

The failed environment attempt is retained rather than hidden. Evidence: [initial failure](/audit-output/evidence/06-preflight-rerun.results.json), [PID diagnosis and narrowly scoped shim](/audit-output/evidence/08-lean-pid-shim.results.txt), [successful returned preflight evidence](/audit-output/evidence/09-preflight-rerun-with-shim.results.json), and its [exact command](/audit-output/evidence/09-preflight-rerun-with-shim.commands.txt).

## Independent manifests, obligation bijection, and target identity

I independently recomputed and matched the Stage 1 pipeline tree hash, Stage 1 export hash, every Stage 1 file hash, selected Stage 2 tree hash, Stage 3 file hash, selected Stage 4 tree hash, producer tree hash, generated tree hash, obligation-map file hash, trust-inventory file hash, verification file hash, and signed audit-resolution hash. The result is recorded as 28 named checks, all true.

The exact ordered mapping is:

| Layer | Ordered entries |
|---|---|
| Independently reconstructed local rules | `[]` |
| Protected Stage 3 rules | `[]` |
| Stage 4 `input-manifest.source_rules` | `[]` |
| `obligation-map.source_rules` | `[]` |
| `obligation-map.obligations` | `[]` |
| `obligation-map.trust_parameters` | `[]` |

The obligation-map SHA-256 is `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`, matching the generator manifest. Counts are zero in the generator manifest, export result, recorded preflight, fresh preflight, and audit input. With a genuinely empty independent domain set, there are no obligations that can be omitted, duplicated, weakened, made irrelevant, or made vacuous.

The fixed generated target is correctly absent. The generated Lean tree contains zero `def targetStatement` declarations; the trusted target parser returns null; the expected target definition computed from the empty obligation map is null; and the generator manifest, recorded preflight, fresh preflight, and audit input all bind target to null. This is the only valid target state for `KLEAN_NO_OBLIGATIONS`.

Evidence: [complete Stage 4 sidecars and generated sources](/audit-output/evidence/10-stage4-sidecars.results.txt) and [independent hash/bijection/target audit](/audit-output/evidence/11-independent-hashes-and-bijection.results.json).

## Stage 5 applicability

Stage 5 is intentionally absent because the launcher selected `CLASSIFICATION_ONLY`. There is no generated theorem to prove, no target parameter or operational bridge to audit, no `/candidate`, and no `Proof.final` for an axiom print. Running proof-mode clean builds, candidate token scans, `#print axioms Proof.final`, or parameter-definition adversarial checks would invent a proof candidate outside the signed mode. Their absence is therefore correct, not missing evidence.

## Final judgment

The Stage 3 classification is an exact and mathematically appropriate empty classification. The deterministic Stage 4 artifacts are provenance-bound, hash-consistent, structurally valid, freshly buildable, bijective with that empty classification, and correctly contain neither obligations nor a target. The selected `KLEAN_NO_OBLIGATIONS` status is legitimate, and the classification-only run correctly has no Stage 5 candidate.

VERDICT: PASS
LEGITIMACY: LEGIT
