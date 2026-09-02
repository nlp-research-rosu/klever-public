# Audit command index

All paths below were executed from `/audit-output`. The corresponding `.log` files contain raw combined output and exit status metadata from `script -q -e -c`.

## Producer and manifest authentication

Output: `01-producer-and-manifest-hashes.log`

```sh
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py /reference/generation-tools/source-manifest.json /reference/klean-generation/generator-manifest.json /reference/klean-generation/input-manifest.json /reference/lemma-discovery.json /reference/klean-generation/generated/obligation-map.json
```

Output: `02-manifests-and-launcher.log`

```sh
sed -n '1,260p' /reference/generation-tools/source-manifest.json
sed -n '1,320p' /reference/klean-generation/generator-manifest.json
sed -n '1,320p' /reference/klean-generation/input-manifest.json
sed -n '1,110p' /audit-input.json
```

Output: `18-launcher-style-tree-digests.log`

```sh
PYTHONPATH=/reference python -c 'from pathlib import Path; from tools.pipeline_contract import sha256_tree; paths=[Path("/reference/k-proof"),Path("/reference/k-audit"),Path("/reference/klean-generation"),Path("/reference/klean-generation/generated"),Path("/reference/generation-tools")]; [print(f"{sha256_tree(p)}  {p}") for p in paths]'
```

Output: `19-all-recorded-hash-verification.log`

```sh
PYTHONPATH=/reference python /audit-output/evidence/hash_verification.py
```

## Inventory reconstruction and Stage 3 bijection

Output: `06-reconstructed-rule-inventory.log`

```sh
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Output: `07-stage3-bijection-validation.log`

```sh
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
```

Output: `27-explicit-inventory-order-bijection.log`

```sh
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; inv=inventory_verification(Path("/reference/k-proof")); disc=json.loads(Path("/reference/lemma-discovery.json").read_text()); expected=[r["source_rule_id"] for r in inv["rules"]]; observed=[r["source_rule_id"] for r in disc["rules"]]; print("inventory_count=",len(expected)); print("classified_count=",len(observed)); print("ordered_identity_match=",observed==expected); print("inventory_unique=",len(expected)==len(set(expected))); print("classified_unique=",len(observed)==len(set(observed))); print("omitted=",sorted(set(expected)-set(observed))); print("extra=",sorted(set(observed)-set(expected))); print("expected_order=",expected); print("observed_order=",observed)'
```

Output: `28-source-id-and-inventory-hash-check.log`

```sh
PYTHONPATH=/reference python -c 'from pathlib import Path; from tools.k_rule_inventory import inventory_verification,canonical_json_sha256; inv=inventory_verification(Path("/reference/k-proof")); checks=[(r["start_line"],r["end_line"],r["source_rule_id"]=="rule-"+r["normalized_sha256"]) for r in inv["rules"]]; print("source_id_hash_checks=",checks); print("all_source_ids_bound_to_hash=",all(c[2] for c in checks)); print("recomputed_inventory_sha256=",canonical_json_sha256(inv["rules"])); print("reported_inventory_sha256=",inv["inventory_sha256"]); print("inventory_hash_match=",canonical_json_sha256(inv["rules"])==inv["inventory_sha256"])'
```

## Source and operational-semantic review

Output: `05-frozen-source-and-spec.log`

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/prompt.py
```

Output: `10-operational-semantics-trace.log`

```sh
rg -n 'triValue|triComplete|triResult|triLoopCondition|triLoopBody|triFunctionBody|triDefinition' /reference/k-proof --glob '*.k' --glob '!**/*-kompiled/**'
rg -n -C 3 '#while|While\(|append|pyMod|BinOp\("//"|BinOp\("%"|AugAssign|If\(' /reference/k-proof/reference-semantics --glob '*.k'
```

Output: `22-classification-witness.log`

```sh
python /audit-output/evidence/classification_witness.py
```

## Trusted Stage 4 preflight

Native output: `11-fresh-check-generation.log`

```sh
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Compatibility-shim test output: `23-app-path-compatibility.log`

```sh
cc -shared -fPIC -O2 -Wall -Wextra -o /tmp/audit-work/app_path_compat.so /audit-output/evidence/app_path_compat.c -ldl
sha256sum /audit-output/evidence/app_path_compat.c /tmp/audit-work/app_path_compat.so
lean --version
LD_PRELOAD=/tmp/audit-work/app_path_compat.so lean --version
```

Successful fresh preflight output: `15-fresh-check-generation-with-app-path-compat.log`

```sh
LD_PRELOAD=/tmp/audit-work/app_path_compat.so PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

## Obligation bijection and target

Output: `20-empty-bijection-and-target-check.log`

```sh
PYTHONPATH=/reference python -c 'import json; from pathlib import Path; from tools import klean_export, lemma_discovery_contract; validated=lemma_discovery_contract.validate_trust_boundary(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json")); source=[r for r in validated["rules"] if r.get("classification")=="DOMAIN_LEMMA"]; mapping=json.loads(Path("/reference/klean-generation/generated/obligation-map.json").read_text()); manifest=json.loads(Path("/reference/klean-generation/generator-manifest.json").read_text()); print("independent_domain_ids=",[r["source_rule_id"] for r in source]); print("mapped_source_ids=",[r["source_rule_id"] for r in mapping["source_rules"]]); print("obligation_source_ids=",[r["source_rule_id"] for r in mapping["obligations"]]); print("target_statement=",klean_export.target_statement(Path("/reference/klean-generation/generated"))); print("manifest_target=",manifest["target"]); print("manifest_obligation_count=",manifest["obligation_count"])'
rg -n '^[[:space:]]*(theorem|lemma|def[[:space:]]+target|axiom|opaque)[[:space:]]' /reference/klean-generation/generated --glob '*.lean'
test ! -e /candidate
printf 'AUDIT_MODE=%s\n' "$AUDIT_MODE"
```
