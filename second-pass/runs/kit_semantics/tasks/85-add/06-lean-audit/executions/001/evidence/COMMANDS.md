# Audit command record

The mounted inputs were only read. All writable work was staged under
`/tmp/audit-work/85-add-proof-audit`.

## Producer authentication

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/lemma-discovery.json \
  /audit-input.json
```

```sh
PYTHONPATH=/reference python3 -c '
import json
from pathlib import Path
from tools.pipeline_contract import sha256_tree
a = json.loads(Path("/audit-input.json").read_text())["resolution"]
print(a["hashes"]["generation_producer_sources_sha256"])
print(sha256_tree(Path("/reference/generation-tools")))
print("sha256:" + Path(a["generation_producer_sources"]).name)
'
```

Results: `01_manifests_and_producer_hashes.log`,
`06_producer_tree_and_audit_input_binding.log`.

## Stage 1 inventory and Stage 3 bijection

```sh
PYTHONPATH=/reference python3 -c '
from pathlib import Path
import json
from tools.k_rule_inventory import inventory_verification
print(json.dumps(
    inventory_verification(Path("/reference/k-proof")),
    indent=2,
    sort_keys=True,
))
'
```

```sh
PYTHONPATH=/reference python3 -c '
from pathlib import Path
import json
from tools.lemma_discovery_contract import validate_trust_boundary
print(json.dumps(
    validate_trust_boundary(
        Path("/reference/k-proof"),
        Path("/reference/lemma-discovery.json"),
    ),
    indent=2,
    sort_keys=True,
))
'
```

Results: `03_reconstructed_rule_inventory.log`,
`04_stage3_bijection_validation.log`,
`24_explicit_inventory_bijection_summary.log`,
`25_simplification_classification_gate.log`.

## Deterministic Stage 4 preflight

The first exact invocation exposed the sandbox PID/proc mismatch:

```sh
PYTHONPATH=/reference python3 -c '
from pathlib import Path
import json
from tools.klean_preflight import check_generation
r = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(r, indent=2, sort_keys=True))
'
```

Result: `07_rerun_klean_preflight.log`.

The narrowly scoped launcher workaround was built and checked:

```sh
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc_exe_readlink_shim.so \
  /audit-output/evidence/proc_exe_readlink_shim.c -ldl
sha256sum \
  /audit-output/evidence/proc_exe_readlink_shim.c \
  /tmp/audit-work/proc_exe_readlink_shim.so
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
```

Result: `10_proc_shim_build_and_lean_version.log`.

The same preflight was then rerun with the pinned Lean/Lake paths:

```sh
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake \
LEAN=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean \
PYTHONPATH=/reference \
python3 -c '
from pathlib import Path
import json
from tools.klean_preflight import check_generation
r = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(r, indent=2, sort_keys=True))
'
```

Result: `11_rerun_klean_preflight_pass.log`.

## Fresh Stage 5 build

```sh
mkdir /tmp/audit-work/85-add-proof-audit
cp -a /candidate/. /tmp/audit-work/85-add-proof-audit/
cp -a /reference/klean-generation/generated \
  /tmp/audit-work/85-add-proof-audit/Base
mv /tmp/audit-work/85-add-proof-audit/Base/generated \
  /tmp/audit-work/misplaced-generated-copy
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/85-add-proof-audit/Base/
```

`/candidate` contains an empty `Base` directory, so the first generated
copy nested one level too deeply. The nested copy was preserved outside
the project, and the exact generated contents were then copied into the
existing `Base`. The copied `Base` digest was checked with
`tools.klean_export.tree_digest`; result:
`14_corrected_base_copy_identity.log`.

In `/tmp/audit-work/85-add-proof-audit`, with the same
`LD_PRELOAD`, `LEAN_SYSROOT`, `LAKE_HOME`, `LAKE`, and `LEAN` values:

```sh
lake clean
lake build
lake env lean AxiomAudit.lean
lake env lean BridgeAudit.lean
```

Results: `15_fresh_candidate_lake_clean.log`,
`16_fresh_candidate_lake_build.log`,
`17_print_axioms_proof_final.log`,
`21_operational_bridge_adversarial_examples.log`.

## Trusted full mechanical binding gate

With the same pinned environment:

```sh
PYTHONPATH=/reference python3 -c '
from pathlib import Path
import json
from tools.klean_final_gate import check_final
r = check_final(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    Path("/candidate"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    audit_input=Path("/audit-input.json"),
)
print(json.dumps(r, indent=2, sort_keys=True))
'
```

Result: `20_full_mechanical_input_binding_gate.log`.
