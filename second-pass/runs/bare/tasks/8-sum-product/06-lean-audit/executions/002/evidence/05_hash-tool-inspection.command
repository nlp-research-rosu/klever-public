rg -n 'def .*sha256|tree_sha256|artifact_sha256|resolved_input_sha256|source_hashes|generated_tree_sha256|workspace_sha256' /reference/tools/*.py
printf '\nKLEAN EXPORT HASHING\n'
rg -n -C 8 'def _tree_entries|def tree_sha256|def .*tree|canonical_json_sha256' /reference/tools/klean_export.py
printf '\nAUDIT CONTRACT HASHING\n'
rg -n -C 8 'resolved_input_sha256|artifact_sha256|tree_sha256|source_hashes' /reference/tools/audit_contract.py /reference/tools/klean_audit_contract.py /reference/tools/pipeline_contract.py
