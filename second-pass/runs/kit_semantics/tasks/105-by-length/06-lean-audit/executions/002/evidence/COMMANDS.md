# Audit command index

This index records the substantive commands whose raw outputs are stored beside it. The sandbox required the recorded `LAKE_HOME`, `LEAN_SYSROOT`, and narrow `/proc` compatibility preload for Lake to locate the locked Lean 4.22.0 installation.

```bash
env | sort
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
```

Output: `00_environment_and_initial_hashes.txt`.

```bash
PYTHONPATH=/reference python3 /tmp/audit-work/audit_hash_inventory.py
```

Output: `03_hash_and_inventory_reconstruction.txt`. This invokes the trusted `tools.k_rule_inventory.inventory_verification` implementation and performs the launcher, tree, producer, and inventory comparisons.

```bash
PYTHONPATH=/reference \
LAKE_HOME=/tmp/audit-work/lake-install \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
python3 -c 'from pathlib import Path; import json; from tools.klean_preflight import check_generation; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")), indent=2, sort_keys=True))'
```

Successful output: `08_required_stage4_preflight_success.txt`. The same call without the Lake-location compatibility environment is preserved in `04_required_stage4_preflight.txt`.

```bash
PYTHONPATH=/reference python3 /tmp/audit-work/audit_stage4.py
```

Output: `09_stage4_bijection_and_target_hashes.txt`.

The fresh project was `/tmp/audit-work/lean-proof-audit`; candidate root files were copied there and `/reference/klean-generation/generated` was copied as `Base`. The required build commands were:

```bash
LAKE_HOME=/tmp/audit-work/lake-install \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
lake clean

LAKE_HOME=/tmp/audit-work/lake-install \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
lake build
```

Complete output: `10_fresh_candidate_clean_build.txt`.

```bash
LAKE_HOME=/tmp/audit-work/lake-install \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
lake env lean AxiomAudit.lean
```

Exact `#check`, `#print Proof.final`, and `#print axioms Proof.final` output: `12_axiom_audit_exact.txt`.

```bash
LAKE_HOME=/tmp/audit-work/lake-install \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
lake env lean BridgeAudit.lean
```

Successful adversarial evaluation output: `19_operational_bridge_evaluations_success.txt`; test source is printed in `14_operational_bridge_sources_and_tests.txt`.

```bash
PYTHONPATH=/reference \
LAKE_HOME=/tmp/audit-work/lake-install \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
python3 /reference/tools/klean_final_gate.py \
  --frozen-k /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --generation /reference/klean-generation \
  --candidate /candidate \
  --toolchain-lock /reference/klean-toolchain.lock.json \
  --audit-input /audit-input.json \
  --output /audit-output/evidence/15_trusted_final_gate.json
```

Output: `15_trusted_final_gate.json`; terminal transcript: `15_trusted_final_gate_command.txt`.
