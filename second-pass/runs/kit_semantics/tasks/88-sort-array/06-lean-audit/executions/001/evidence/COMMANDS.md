# Audit command record

The numbered evidence files contain the corresponding raw stdout/stderr and
exit status. The commands below are the substantive audit commands, excluding
read-only exploratory source browsing.

## Producer and provenance

Output: `01-producer-hashes.txt`

```sh
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py /reference/generation-tools/source-manifest.json
```

Output: `03-generator-manifest.txt`

```sh
sed -n '1,300p' /reference/klean-generation/generator-manifest.json
```

Output: `04-source-manifest.txt`

```sh
sed -n '1,300p' /reference/generation-tools/source-manifest.json
```

Output: `05-audit-input-producer-fields.txt`

```sh
rg -n 'generator_image|producer|klean_export|klean.py|f884238|388cac' /audit-input.json
```

Output: `07-producer-tree-hash-pipeline.txt`

```sh
env PYTHONPATH=/reference python3 -c 'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
```

## Inventory and frozen-source inspection

Output: `08-reconstructed-inventory.json.txt`

```sh
env PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Output: `09-lemma-discovery.txt`

```sh
sed -n '1,360p' /reference/lemma-discovery.json
```

Outputs: `10-verification-k.txt`, `11-spec-k.txt`, `12-solution-py.txt`, and
`13-prompt-and-solution-mpy.txt`

```sh
sed -n '1,260p' /reference/k-proof/verification.k
sed -n '1,320p' /reference/k-proof/spec.k
sed -n '1,240p' /reference/k-proof/solution.py
sed -n '1,260p' /reference/k-proof/prompt.py
sed -n '1,300p' /reference/k-proof/solution.mpy
```

Output: `22-inventory-discovery-bijection.txt`

```sh
env PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; inv=inventory_verification(Path("/reference/k-proof")); disc=json.loads(Path("/reference/lemma-discovery.json").read_text()); ii=[r["source_rule_id"] for r in inv["rules"]]; di=[r["source_rule_id"] for r in disc["rules"]]; classes={r["source_rule_id"]:r["classification"] for r in disc["rules"]}; print(json.dumps({"inventory_hash_equal":inv["inventory_sha256"]==disc["inventory_sha256"],"inventory_rule_count":len(ii),"discovery_rule_count":len(di),"ordered_identities_equal":ii==di,"inventory_ids_unique":len(ii)==len(set(ii)),"discovery_ids_unique":len(di)==len(set(di)),"missing_from_discovery":sorted(set(ii)-set(di)),"extra_in_discovery":sorted(set(di)-set(ii)),"classifications_in_order":[classes[i] for i in ii],"simplification_rule_ids":[r["source_rule_id"] for r in inv["rules"] if "simplification" in r["attributes"]],"independently_true_domain_rule_ids":[]}, indent=2, sort_keys=True))'
```

Output: `23-relevant-operational-semantics.txt`

```sh
sed -n '1,120p' /reference/k-proof/reference-semantics/semantics/core.k
sed -n '190,245p' /reference/k-proof/reference-semantics/semantics/core.k
sed -n '1,95p' /reference/k-proof/reference-semantics/semantics/sort.k
sed -n '1,52p' /reference/k-proof/reference-semantics/semantics/subscript.k
sed -n '1,35p' /reference/k-proof/reference-semantics/semantics/int.k
sed -n '1,55p' /reference/k-proof/reference-semantics/semantics/bool.k
sed -n '45,110p' /reference/k-proof/reference-semantics/semantics/controls.k
```

## Preflight

Output: `14-rerun-preflight.txt` (the initial sandbox-environment failure)

```sh
env PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result = check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

The compatibility shim was compiled with:

```sh
gcc -shared -fPIC /tmp/audit-work/lean-proc-self-shim.c -o /tmp/audit-work/lean-proc-self-shim.so -ldl
```

Output: `15-rerun-preflight-with-sandbox-shim.txt`

```sh
env LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result = check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Output: `26-lean-sandbox-shim-diagnosis.txt`

```sh
python3 -c 'import os; p=f"/proc/{os.getpid()}/exe"; print("numeric_pid_path=", p); print("numeric_pid_exists=", os.path.exists(p)); print("proc_self_target=", os.readlink("/proc/self/exe"))'
env LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so lean --version
```

## Independent hash and Stage 4 checks

Output: `16-independent-high-level-hashes.txt`

```sh
env PYTHONPATH=/reference python3 -c 'import hashlib, json; from pathlib import Path; from tools import pipeline_contract, klean_export; values={"k_workspace_sha256":pipeline_contract.sha256_tree(Path("/reference/k-proof")),"stage1_export_sha256":klean_export.tree_digest(Path("/reference/k-proof")),"discovery_manifest_sha256":hashlib.sha256(Path("/reference/lemma-discovery.json").read_bytes()).hexdigest(),"k_audit_sha256":pipeline_contract.sha256_tree(Path("/reference/k-audit")),"klean_generation_sha256":pipeline_contract.sha256_tree(Path("/reference/klean-generation")),"generated_tree_sha256":klean_export.tree_digest(Path("/reference/klean-generation/generated")),"generation_producer_sources_sha256":pipeline_contract.sha256_tree(Path("/reference/generation-tools"))}; print(json.dumps(values, indent=2, sort_keys=True))'
```

Output: `17-stage1-source-hash-bijection-and-mode.txt`

```sh
env PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools import pipeline_contract; audit=json.loads(Path("/audit-input.json").read_text()); expected=audit["resolution"]["stage1_source_hashes"]; root=Path("/reference/k-proof"); observed={p.relative_to(root).as_posix():pipeline_contract.sha256_file(p) for p in pipeline_contract._walk_regular_files(root, "Stage 1 source workspace")}; print(json.dumps({"expected_count":len(expected),"observed_count":len(observed),"missing":sorted(set(expected)-set(observed)),"extra":sorted(set(observed)-set(expected)),"hash_mismatches":sorted(k for k in set(expected)&set(observed) if expected[k]!=observed[k]),"mode":audit["resolution"]["mode"],"semantics_mode":audit["resolution"]["semantics_mode"],"lean_workspace":audit["resolution"]["lean_workspace"],"lean_invocation":audit["resolution"]["lean_invocation"],"lean_workspace_sha256":audit["resolution"]["hashes"]["lean_workspace_sha256"],"lean_invocation_sha256":audit["resolution"]["hashes"]["lean_invocation_sha256"]}, indent=2, sort_keys=True))'
```

Output: `18-generation-maps-and-result.txt`

```sh
sed -n '1,360p' /reference/klean-generation/input-manifest.json
sed -n '1,360p' /reference/klean-generation/generated/obligation-map.json
sed -n '1,260p' /reference/klean-generation/export-result.json
```

Output: `19-generation-sidecar-file-hashes.txt`

```sh
sha256sum /reference/klean-generation/input-manifest.json /reference/klean-generation/generator-manifest.json /reference/klean-generation/generated/obligation-map.json /reference/klean-generation/trust-inventory.json /reference/klean-generation/export-result.json /reference/klean-generation/preflight.json
```

Output: `20-generated-tree-target-and-candidate-absence.txt`

```sh
find /reference/klean-generation/generated -maxdepth 3 -type f -printf '%P\n' | sort
test ! -e /candidate
rg -n '\b(?:theorem|axiom|opaque|sorry|admit|unsafe)\b|Proof\.final|target' /reference/klean-generation/generated || true
```

Output: `21-fixed-target-identity.txt`

```sh
env PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.klean_export import target_statement; audit=json.loads(Path("/audit-input.json").read_text()); generator=json.loads(Path("/reference/klean-generation/generator-manifest.json").read_text()); print(json.dumps({"scanned_generated_target":target_statement(Path("/reference/klean-generation/generated")),"generator_manifest_target":generator.get("target"),"audit_input_target_present":"target" in audit["resolution"],"audit_input_target":audit["resolution"].get("target"),"generator_obligation_count":generator.get("obligation_count")}, indent=2, sort_keys=True))'
```

Output: `24-candidate-absence.txt`

```sh
python3 -c 'from pathlib import Path; print({"candidate_exists": Path("/candidate").exists(), "candidate_is_symlink": Path("/candidate").is_symlink()})'
```

Output: `25-independent-manifest-bijection.txt`

```sh
env PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; inv=inventory_verification(Path("/reference/k-proof")); disc=json.loads(Path("/reference/lemma-discovery.json").read_text()); inp=json.loads(Path("/reference/klean-generation/input-manifest.json").read_text()); om=json.loads(Path("/reference/klean-generation/generated/obligation-map.json").read_text()); gm=json.loads(Path("/reference/klean-generation/generator-manifest.json").read_text()); joined=[]; bydisc={r["source_rule_id"]:r for r in disc["rules"]}; [joined.append({**r, **bydisc[r["source_rule_id"]]}) for r in inv["rules"]]; print(json.dumps({"input_definitions_exact_join":inp["definitions"]==joined,"input_source_rules":inp["source_rules"],"input_operational_rules":inp["operational_rules"],"input_proved_derived_lemmas":inp["proved_derived_lemmas"],"obligation_map_source_rules":om["source_rules"],"obligations":om["obligations"],"trust_parameters":om["trust_parameters"],"manifest_obligation_count":gm["obligation_count"],"manifest_target":gm["target"]}, indent=2, sort_keys=True))'
```
