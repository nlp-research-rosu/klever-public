# Audit commands

All mounted candidate and provenance content was treated as untrusted evidence.
Only the trusted tooling below `/reference/tools` was imported or executed.

## Producer authentication

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /audit-input.json
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
python3 -m json.tool /audit-input.json
```

## Canonical inventory

```sh
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))
PY
```

## Stage 3 contract and independent bijection

```sh
PYTHONPATH=/reference python3 - <<'PY'
# See evidence/inventory-comparison.json for the full structured result.
PY
```

## Deterministic generation preflight

```sh
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

The first invocation was preserved in `check-generation-output.txt`; Lake
failed before compilation because the audit PID namespace did not correspond
to the read-only `/proc` mount. The narrow compatibility shim
`/tmp/audit-work/proc-self-fix.so` was compiled from
`/tmp/audit-work/proc-self-fix.c`. It changes only `readlink`/`readlinkat`
requests of the form `/proc/<numeric-pid>/exe` to `/proc/self/exe`.
The unchanged trusted preflight was rerun as:

```sh
LD_PRELOAD=/tmp/audit-work/proc-self-fix.so \
PYTHONPATH=/reference \
python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

The complete returned result is in `check-generation-output-rerun.txt`.
The successful build output was short enough that `output_tail` contains it
in full; its SHA-256 is also recorded by the checker.

## Hash reconciliation

The trusted algorithms used were:

```sh
PYTHONPATH=/reference python3
```

- `tools.pipeline_contract.sha256_tree` for launcher artifact/tree hashes.
- `tools.klean_export.tree_digest` for frozen-export and generated-project
  hashes.
- `tools.pipeline_contract.sha256_file` for every one of the 770 Stage 1
  files.
- `tools.stage6_resolution_contract.verify_audit_input` for the signed
  resolution digest.

The structured command result is `hash-reconciliation.json`.

## Semantic cross-check

```sh
python3 - <<'PY'
# Two independently written functions modeled (1) direct execution of the
# source branches and (2) nextCurrent/nextResult/scanCurrent/scanResult.
# Exhaustive products used codes [111, 46, 124, 32, -1, 128], lengths 0..6.
# Guard partitions were checked for codes -5..130 and currents -2..6.
# The operational `o` assignment was then counterfactually changed 4 -> 5.
PY
```

The complete result is `semantic-crosscheck.txt`; the implementation used for
the check appears in the raw executed heredoc recorded by the audit runtime.
