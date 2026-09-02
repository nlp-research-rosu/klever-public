# Audit commands

All commands were run from `/audit-output` unless a command records another working directory. Exact stdout/stderr and exit codes are stored in the numbered log files beside this index.

1. `sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py /reference/generation-tools/source-manifest.json /reference/klean-generation/generator-manifest.json /audit-input.json`, followed by trusted `pipeline_contract.sha256_tree` and a JSON comparison of producer hashes/image IDs.
2. Trusted `tools.k_rule_inventory.inventory_verification(Path('/reference/k-proof'))`, followed by a bijective comparison with `/reference/lemma-discovery.json`.
3. Independent relevant-source inspection and classification of every reconstructed inventory entry.
4. `PYTHONPATH=/reference python3` calling `tools.klean_preflight.check_generation(...)` with the frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage 4 generation, and pinned lock.
5. Independent hash, obligation-map, target, generated-tree, and no-Stage-5 checks.
6. Audit-container workaround: compile `pidns_readlink_shim.c`, which maps only `/proc/<pid>/exe` to `/proc/self/exe`, then rerun the unchanged trusted preflight with `LD_PRELOAD`.
7. `PYTHONPATH=/reference python3 evidence/verify_stage4_integrity.py` to recompute every launcher resolution tree hash, all 769 Stage 1 per-file hashes, every Stage 4 sidecar binding, the producer/image bindings, the empty source-rule/obligation bijection, and target/candidate absence.
8. Raw inspection of `obligation-map.json`, generated `Lemmas.lean`, target-declaration scan, `/candidate` absence, and launcher Stage 5 fields.
