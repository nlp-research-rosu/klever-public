# AAAI-27 Supplementary Package — build report

Built 2026-07-31 (final revision: THREE-ARM coverage — bare / semantics /
kit_semantics). Deliverables (all confined to this scratchpad area; no
repo writes):

- ZIP: `supplementary_code_and_data.zip` (beside this report) —
  **15 MB** zipped (v8.2), ~48 MB unpacked. Hard limit 50 MB on the
  zipped upload: comfortable margin.
- Build tree kept at `aaai-package/supplementary_code_and_data/`.
- Single top-level directory confirmed; clean-directory unzip verified.

## Tree (2 levels)

```text
supplementary_code_and_data/
├── README.md                 three-arm design, pipeline, commands,
│                             artifact guide, lake recipe (tested)
├── requirements.txt          stdlib-only statement
├── src/                      runnable repository-root mirror
│   ├── tools/                23 .py (one-shot/migration scripts pruned)
│   ├── prompts/              12 stage prompts (all three arm conditions)
│   ├── docker/               audit/, codex/ (no secrets), klean/,
│   │                         klean-audit/, frozen-toolchain-check.sh
│   └── data/                 questions/ (164), skills/, audit-skills/,
│                             reference/ + reference-semantics.md,
│                             6 lock JSONs, selection.json, py2mpy.py
├── scripts/                  census.py (--column aware) + s6 drivers
├── configs/                  copies of the 6 lock files + README
├── data/artifacts/           per-arm, per-task result artifacts
│   ├── kit_semantics/<t>/    160 tasks (stage-6 green)
│   ├── bare/<t>/             64 tasks (stage-2 green)
│   └── semantics/<t>/        73 tasks (stage-2 green)
├── data/results/             results_{kit_semantics,bare,semantics}.csv,
│                             arms_summary.csv, census.json (all fresh)
└── expected_results/         census_{kit_semantics,bare,semantics}.txt,
                              claims_to_artifacts.md
```

## Census (live at final re-zip) and arms summary

- bare (primary verdict stage 2): 23 PASS + 41 CONCERNS = **64 LEGIT**,
  100 FAIL — matches the user's expected numbers.
- semantics (stage 2): 37 PASS + 36 CONCERNS = **73 LEGIT**, 91 FAIL —
  matches.
- kit_semantics (stage 6): 158 PASS + 2 CONCERNS = **160 LEGIT**, 3 FAIL,
  1 not reached.
- `arms_summary.csv` columns: arm, primary_verdict_stage, legit, pass,
  concerns, fail, not_reached, total (the two extra columns keep the
  164-task accounting honest).
- Control-arm tables include stage-4/stage-6 status and obligation-count
  columns — verified meaningfully populated (bare: 64 stage-4 selections,
  64 stage-6 selections incl. 1 FAIL; semantics: 73 and 72 incl. 8 FAIL).

## Artifact coverage (green-only, per arm)

| arm | tasks | s2 reviews | classifications | s6 reviews | lean_proof |
| --- | --- | --- | --- | --- | --- |
| kit_semantics | 160 | 160 | 160 | 160 | 68 |
| bare | 64 | 64 | 64 | 63 | 3 |
| semantics | 73 | 73 | 73 | 64 | 17 |

Rules applied: control-arm tasks ship on stage-2 PASS/CONCERNS; stage-6
reviews only where the selected stage-6 audit is green (bare has 1
stage-6 FAIL, semantics 8 — excluded); `lean_proof/` only where
additionally the selected stage-4 generation is PASS (semantics has 8
stage-4-PASS tasks with non-green/absent stage-6 — Base+proof excluded
for all 8, listed in the build log). k_proof rules identical to the kit
arm (root `.k` — including the bare arm's model-authored semantics —
prompt.py, prove.sh, root markdowns; no reference-semantics copies, no
kompiled dirs, no binaries — bare's `kore-exec.tar.gz` etc. excluded).

**Manifests verification (user question): all 88 shipped `lean_proof/`
trees (68+3+17) contain all four per-generation manifests at the `Base/`
root (obligation-map.json, generator-manifest.json, trust-inventory.json,
export-result.json) — verified in the build tree and re-verified in the
extracted ZIP.** The README's artifacts section now states this location
explicitly.

**[Superseded in v8.2: the ledger is re-packaged — the stage-6 mechanical
gate resolves recorded producer hashes there, and a reviewer's own fresh
run tree is itself "an existing run tree" by audit time; see the v8.2
section.]** Producer ledger REMOVED (final tidy): `src/data/stage4-producer-sources/`
(all bundles + the scoped README) is no longer in the package, per the
latest-version-only doctrine — the single final exporter in `src/tools`
plus `src/docker/klean` is what reviewers run. The README's stage-4 text
now states: exports are deterministic per exporter version; the shipped
Base trees are the campaign's selected outputs; re-running the included
exporter reproduces trees under the current, final version. Residual code
reference: `src/tools/klean_audit_contract.py` still names
`data/stage4-producer-sources` — a stage-6 audit-time mount path only
exercised when auditing an existing run tree (unmodified tool code;
noted, not an error).

## Lake-build recipe — TESTED

`cd data/artifacts/kit_semantics/55-fib/lean_proof && lake build`: Base +
Proof built in ~30 s under elan-selected leanprover/lean4:v4.22.0
(residue cleaned). Recipe and the `/tmp/klean-generated-build` buildDir
quirk documented in README.

## Double-blind scan (assembled tree AND extracted ZIP)

- Fixed list (yuqing, zhai, kevinzhai, zhaiyuqing, @gmail, @outlook,
  claude, anthropic, co-authored): **zero hits** both scans.
- `/home/`: sole residual `/home/agent` (generic container user,
  src/docker/codex/Dockerfile:71).
- New control-arm model-written texts (137 stage-2 reviews, 127 stage-6
  reviews, 137 DISCOVERY.md, trust boundaries, 2 k_proof markdowns)
  scanned hard: no emails, no institutions, no user paths, no
  scratchpad/runner-state/Documents leakage; a handful of benign
  technical phrases ("cells written by...", "acknowledged abstraction")
  inspected and cleared. URL inventory: only the upstream
  runtimeverification/haskell-backend citation in generated Prelude.lean
  files (now 88 copies) plus the previously logged toolchain URLs.
- Quarantines: none.

## Items for user judgment (carried + new)

1. `/home/agent` container path and third-party toolchain/citation URLs —
   kept (load-bearing/public, non-identifying).
2. Evaluated-model identifier `gpt-5.6-sol` appears throughout — subject,
   not authors.
3. `source_repository: ANONYMIZED` in kit lock files (historical-Kit
   resume path inert; fresh runs unaffected).
4. Control arms: the 8 semantics-arm and 1 bare-arm stage-6 FAILs are
   visible in the results tables (honest) but ship no artifacts; the
   arms' primary verdict remains stage 2 as directed.
5. Snapshot caveat: all three censuses are the 2026-07-31 live state;
   re-run before any re-upload if statuses move.

## Verification log

- ZIP extracts cleanly; full re-scan of extracted tree clean; all three
  per-arm censuses from the extracted copy match expected_results and
  the live runs trees; artifact counts re-verified post-extraction
  (table above); 88×4 manifests re-verified post-extraction.
- `bash -n` on shipped shell scripts; markdownlint on authored markdown;
  permissions normalized 644/755.

## v5 refresh (2026-07-31 evening)

Folded in the two endgame rescues, both validated by fresh adversarial
stage-6 audits:

- `73-smallest-change`: PASS (artifacts added — k_proof, audits,
  classification, lean_proof/Base from generations/004).
- `144-simplify`: PASS (artifacts added; lean_proof/Base from
  generations/006).
- kit_semantics census: 160 PASS + 2 CONCERNS = 162/164 rows LEGIT
  (1 FAIL, 1 NOT_REACHED); census.json, arms_summary.csv,
  results_kit_semantics.csv, expected_results updated.
- Double-blind scan re-run over the added artifacts: clean (Prelude
  upstream-attribution URLs retained, matching v4 precedent).

## v6 refresh (2026-08-01 morning)

- `129-minPath`: **PASS at stage 6** — the final rescue. Chain:
  honest-PARTIAL K derivation (all constituent claims #Top; composed
  replay blocked by a characterized frozen-backend limitation) →
  stage-2 CONDITIONAL CONCERNS/LEGIT under the registered, disclosed
  129-minPath provision → 7 domain lemmas honestly classified →
  deterministic export → all 7 obligations proven in Lean (axiom
  footprint: Lean core only) → independent stage-6 audit PASS.
  Artifacts added under data/artifacts/kit_semantics/129-minPath/.
- kit_semantics census: 161 PASS + 2 CONCERNS = 163/164 rows LEGIT
  (sole FAIL: 118-get-closest-vowel, whose explicit-derivation session
  remains in progress and is disclosed in the campaign ledger).
- Double-blind scan re-run over added artifacts: clean.

## v7 refresh (2026-08-01) — FAIL artifacts added for all arms

Per-task artifact folders now cover **all 164 tasks in every arm** (previously
only the LEGIT tasks were included):

- `bare`: +100 FAIL artifacts — each is the rejected `k_proof/` plus the
  decisive `audits/stage2-k-audit-REVIEW.md` (the independent K audit that
  returned FAIL).
- `semantics`: +91 FAIL artifacts, same structure.
- `kit_semantics`: +1 FAIL artifact (`118-get-closest-vowel`) — its K proof
  PASSED stage-2 (`audits/`), classification present; the exported Lean
  obligation was not machine-checked to completion, so it carries the
  in-progress `lean_proof/Proof.lean` and a `STATUS.md` stating it is the
  single kit_semantics FAIL and is not a verified proof.
Every k_proof folder also now includes the agent-written `solution.py` (the
solution the K proof verifies), added across all 492 task dirs with a
verification.k source-consistency check (0 mismatches).

Double-blind scan re-run over every added file: clean (only upstream
RuntimeVerification attribution URLs remain, as before). Verdicts unchanged;
this refresh adds artifacts only.

## v8 refresh (2026-08-01) — 118 PASS: 164/164 per-arm coverage complete

`118-get-closest-vowel` is now a stage-6 **PASS**, completing the
kit_semantics arm at **162 PASS + 2 CONCERNS = 164/164 LEGIT**. The rescue
chain, fully documented in the campaign ledger: Stage 1 had proven all three
operational summaries as reachability claims; the K compiler renders claims
vs installed rules differently in its own `<generatedCounter>` cell, which
under the strict compiled-form identity test demoted the three proven
summaries to unproved DOMAIN_LEMMAs and inflated the Lean export. A
registered provision (in both the Stage 3 instructions and the Stage 6 audit
criteria) credits the proven claim when the compiler's counter-cell
rendering is the sole compiled delta, with a mandatory recorded residual
caveat (counter preservation uncredited; structurally justified as the
summarized code performs no fresh allocation). Stages 3–6 re-ran cleanly:
honest reclassification (3 PROVED_DERIVED with the caveat, 2 DOMAIN_LEMMA),
deterministic export of exactly the two `#Ceil` obligations, first-invocation
Stage 5 proof, and an independent Stage 6 audit that verified the sole-delta
condition itself and returned PASS. The FAIL-era STATUS.md is removed; the
artifact now carries the full six-stage evidence including both audit
reviews and the classification with its recorded caveat.

### v8.1 consistency fix

Reconciled a fork-divergence artifact: the kit_semantics results CSV and arms
summary carried a stale interim verdict for 118; all four census record
sources now agree (162 PASS + 2 CONCERNS = 164/164). The `src/` mirror
(prompts, stage runners, contracts, locks) is refreshed to the exact
versions that produced the final verdicts, including the registered
generated-counter provision in both the Stage 3 and Stage 6 instructions
and the documented env-gated endgame continuation branches (inert without
their explicit environment flags, each chronicled in the campaign ledger).

## v8.2 refresh (2026-08-02) — four-agent integrity audit and batch fix

Four independent read-only audit agents (hygiene, artifact completeness,
anonymity, reproducibility) swept the assembled tree. Every finding was
fixed and the zip re-cut once:

- **Anonymity (2 blockers, fixed)**: the v8.1 `src/` mirror refresh had
  re-synced `src/data/kit-skills.lock.json` and
  `src/data/audit-kit-skills.lock.json` from the repo, clobbering the
  anonymization — `source_repository` again carried the absolute local
  path. Both now record `"ANONYMIZED"`, and `kit_lock_sha256` was
  re-frozen in **both** `audit-campaign.lock.json` copies (`configs/` and
  `src/data/`) to the digest of the sanitized audit-kit lock.
  `tools/check_audit_campaign.py` was then run against the shipped chain
  and passes (`audit campaign OK`), as does the stage-6 tool-bundle gate.
  configs/ and src/data lock copies verified byte-identical.
- **Completeness (fixed)**: 9 missing stage-6 FAIL reviews
  (bare/13-greatest-common-divisor; semantics 19, 24, 38, 44, 59, 79,
  94, 127) copied from each run's *selected* stage-6 execution, and 8
  missing `lean_proof/` sets (semantics 24, 38, 44, 59, 79, 85, 94, 127)
  assembled per the package convention (stage-5 workspace `Proof.lean`,
  `lakefile.lean`, `lean-toolchain` + the selected stage-4 generation's
  `generated/` tree and manifests as `Base/`). The packaging invariant is
  now exact in all three arms: `lean_proof/` exists ⟺ the selected
  stage-4 generation exports > 0 obligations (kit_semantics 72, bare 3,
  semantics 25), independent of the stage-6 verdict; every task that
  reached stage 6 ships its review regardless of verdict.
- **Reproducibility (fixed)**: packaged
  `src/data/reference-semantics-versions.json` plus the
  `reference-semantics-v1/` and `-v2/` trees (the stage-2 audit mounts
  the exact semantics version a candidate recorded),
  `src/data/stage4-producer-sources/` (content-addressed producer source
  bundles the stage-6 mechanical check resolves by hash), and
  `src/data/kit-archive/` (historic Kit bundles backing the provenance
  fallback so the anonymized `source_repository` is never consulted).
  README gained a "Re-pinning the stage-2 audit image gate" section with
  the exact one-field re-pin command, since Docker image IDs are not
  bit-reproducible across hosts.
- **Hygiene (fixed)**: 297 `prove.sh` exec bits normalized to 755; the
  stray `kit_semantics/69-search/lean_proof/.toolchain-lake.lean`
  residue removed; `claims_to_artifacts.md` lean_proof counts updated to
  the exact invariant above.

Re-verified after the re-cut: zip is byte-identical to the tree
(recursive diff of a clean extraction), full author/path/secret grep
clean over both the tree and the extracted zip, both mechanical gates
pass from the shipped `src/`, entry counts match (7,229 files + 2,429
directories). **This report stays outside the zip and must never be
uploaded** — it contains the de-anonymization grep patterns.

## v8.3 refresh (2026-08-02) — summary-number verification; semantics version archive

- **Summary numbers verified end-to-end** (user question after the v8.2
  gap fill): all 164 rows of `results_bare.csv` and
  `results_semantics.csv` recomputed against each run's per-stage
  `selected.json` — zero mismatches; `census.py` outputs match
  `expected_results/` for all three arms; `census.json` and
  `arms_summary.csv` agree (bare 64 LEGIT / semantics 73 / kit_semantics
  164). The v8.2 additions changed evidence only — the FAIL verdicts
  were already in every table.
- **Version-archive restructure (repo first, then mirrored)**:
  `data/reference-semantics-v1`, `-v2` moved to
  `data/semantic-archive/{v1,v2}` (named parallel to `kit-archive`,
  per user direction);
  `reference-semantics-versions.json` re-pointed; every registry entry
  re-verified by tree hash in both the repo and the package (the
  documented pre-v1 alias remains the sole, intended exception).
  `kit-archive/` and `stage4-producer-sources/` deliberately stay at
  their original paths: those are hardcoded in campaign contract code —
  `pipeline_contract.py` is hash-pinned in
  `klean-audit-tools.lock.json`, so relocating them would mean editing
  frozen campaign code and re-freezing the stage-6 gate, which would
  falsify the shipped-bundle-matches-campaign-hashes claim. README
  layout annotates both as path-fixed.
