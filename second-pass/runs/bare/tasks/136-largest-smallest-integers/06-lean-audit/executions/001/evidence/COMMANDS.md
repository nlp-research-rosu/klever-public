# Audit command ledger

All paths below were read-only except `/audit-output` and `/tmp/audit-work`.
The corresponding complete transcripts are the numbered files in this
directory.

## Canonical rule reconstruction

```sh
PYTHONPATH=/reference python3 -c '
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(inventory_verification(Path("/reference/k-proof")),
                 indent=2, sort_keys=True))
'
```

Result: exit 0; see `10-reconstructed-rule-inventory.json`.

## Required Stage 4 preflight

The literal first attempt was:

```sh
PYTHONPATH=/reference python3 -c '
import json
from pathlib import Path
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

Result: the build environment failed before project elaboration because Lean
could not resolve `/proc/<namespace-pid>/exe`; see
`21-rerun-check-generation.txt` through `42-readlink-self-test.txt`.

After compiling the narrow `/proc/<pid>/exe` to `/proc/self/exe` `readlink`
shim recorded in `43-lean-path-shim-build-and-smoke.txt`, the successful
command was:

```sh
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0/src/lean/lake \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
PYTHONPATH=/reference \
python3 -c '
import json
from pathlib import Path
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

Result: exit 0; `KLEAN_NO_OBLIGATIONS`; see
`44-rerun-check-generation-success.txt`.

## Independent structural and hash checks

```sh
AUDIT_MODE="$AUDIT_MODE" PYTHONPATH=/reference \
python3 /audit-output/evidence/50-independent-structural-checks.py
```

Result: exit 0, 167 checks passed; see
`65-independent-structural-checks-success.txt`.

## Semantic/adversarial checks

```sh
python3 /audit-output/evidence/70-fold-semantics-tests.py
```

Result: exit 0, 3,906 cases and zero mismatches; see
`71-fold-semantics-tests.txt`.

## Independent Stage 4 regeneration probes

The trusted current exporter was run with the same frozen input, Stage 3
manifest, problem ID, generator image identifier, and toolchain lock:

```sh
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0/src/lean/lake \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
PYTHONPATH=/reference \
python3 /reference/tools/klean_export.py \
  --input /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --output /tmp/audit-work/regenerated-stage4 \
  --problem 136-largest-smallest-integers \
  --generator-image-id \
    sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda \
  --toolchain-lock /reference/klean-toolchain.lock.json
```

The same command was repeated at a second output path with
`PYTHONHASHSEED=random`; see `58-independent-stage4-regeneration.txt`,
`59-stage4-regeneration-diff.txt`, and
`60-second-stage4-regeneration.txt`.

Two further repetitions used `PYTHONHASHSEED=0`; see
`72-fixed-seed-stage4-regeneration.txt`.
