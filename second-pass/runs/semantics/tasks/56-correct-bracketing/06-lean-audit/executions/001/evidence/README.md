# Evidence notes

- `04_recomputed_integrity.txt` is a preserved diagnostic attempt using the
  newer `audit_contract.sha256_tree` framing. The launcher-recorded whole-tree
  fields use `pipeline_contract.sha256_tree`; the corrected, authoritative
  recomputation is `04b_recomputed_integrity_pipeline_hashes.txt`, where every
  comparison is true.
- `06_fresh_check_generation.txt` preserves the initial environment failure.
  `07_lean_environment_diagnostic.txt` and
  `07b_lean_sandbox_workaround.txt` isolate and resolve the audit sandbox's
  `/proc/<numeric-pid>/exe` limitation.
- `06b_fresh_check_generation_with_sandbox_shim.txt` is the authoritative
  successful fresh preflight result.
- `01_manifests_and_classification.txt` preserves the harmless discovery that
  `jq` is not installed. The complete JSON rendering is
  `01b_manifests_and_classification.txt`.

