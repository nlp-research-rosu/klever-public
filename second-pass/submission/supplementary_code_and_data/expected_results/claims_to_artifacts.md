# Claims to artifacts

How the paper's claims map to artifacts in this package. Statuses reflect
the snapshot recorded at packaging time (see `data/results/census.json`).

| Paper claim | Package artifact |
| --- | --- |
| Three-arm design (bare / semantics / kit_semantics) over the 164 HumanEval tasks | Arm conditions: `src/prompts/bare.md`, `with-semantics.md`, `kit-semantics.md` + skill bundle `src/data/skills/`; task inputs `src/data/questions/`; per-arm condition routing in `src/docker/codex/` |
| Headline per-arm comparison (LEGIT / PASS / CONCERNS / FAIL per arm) | `data/results/arms_summary.csv`; per-task detail in `data/results/results_bare.csv`, `results_semantics.csv`, `results_kit_semantics.csv`; aggregate `data/results/census.json` |
| Six-stage verification pipeline | Stage runners and entrypoints: `src/tools/`, `src/docker/`; stage prompts: `src/prompts/` |
| Per-task proof, classification, and audit artifacts | `data/artifacts/<arm>/<task>/` for all 164 tasks of every arm: `k_proof/` and `audits/` always; `classification/` for every legitimate task (kit_semantics 164, bare 64, semantics 73); `lean_proof/` + `Base/` exactly where the selected stage-4 generation exports a positive number of obligations (kit_semantics 72, bare 3, semantics 25), independent of the eventual stage-6 verdict |
| Stage 4 (K-to-Lean export of domain-lemma obligations) is deterministic and model-free | `src/docker/klean/` (Dockerfile, `generate_task.sh`, `check_task.sh`), exporter sources `src/tools/klean.py`, `src/tools/klean_export.py`; per-task export manifests at each `data/artifacts/<arm>/<task>/lean_proof/Base/` root |
| Shipped Lean proofs rebuild against their exact generated Base under the pinned toolchain | `cd data/artifacts/<arm>/<task>/lean_proof && lake build` (toolchain pinned by each `lean-toolchain`; verified on `kit_semantics/55-fib`) |
| Independent adversarial audit at stage 6 (fresh session plus a no-network mechanical gate) | `src/docker/klean-audit/` (launcher, `check_tool_bundle.py`), audit prompt `src/prompts/klean-audit.md`, checker lock `configs/klean-audit-tools.lock.json`, per-task reviews `data/artifacts/<arm>/<task>/audits/` |
| All tools, prompts, skills, and toolchains are version-pinned | Lock files in `configs/` (mirrored at `src/data/`); toolchain pins in `configs/klean-toolchain.lock.json` (K 7.1.293, Lean 4 v4.22.0, Codex CLI 0.144.6) |
| The reference semantics is frozen | `src/data/reference/src/` with scope and validation notes in `src/data/reference-semantics.md` |
| Per-arm outcome tallies are reproducible from the shipped tables | `python3 scripts/census.py --results data/results/results_<arm>.csv [--column stage2_status]`; expected outputs in `expected_results/census_*.txt` |
| The mechanical tool bundle shipped here matches the pinned hashes used by stage 6 | From `src/`: `python3 docker/klean-audit/check_tool_bundle.py --root . --lock data/klean-audit-tools.lock.json` |
