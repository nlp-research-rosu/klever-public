# Audit commands

All commands ran from `/audit-output`. Mounted candidate and provenance inputs
were read-only. No script from those inputs was executed.

## Launcher and input presence

```bash
printf 'AUDIT_MODE=%s\n' "$AUDIT_MODE"
if test -e /candidate; then find /candidate -maxdepth 2 -type f -printf '%p\n' | sort; else printf '/candidate ABSENT\n'; fi
```

## Producer source authentication and launcher hash verification

```bash
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/lemma-discovery.json

PYTHONPATH=/reference python3 - <<'PY'
# Imported tools.pipeline_contract and tools.stage6_resolution_contract.
# Verified the signed audit envelope, recomputed pipeline sha256_tree for the
# four mounted trees, recomputed all 777 Stage 1 regular-file hashes, and
# compared producer file hashes/image IDs/file set across the source manifest,
# generator manifest, and launcher resolution.
PY
```

The complete result is in `01-producer-auth.json`.

## Canonical rule reconstruction

```bash
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
inventory = inventory_verification(Path('/reference/k-proof'))
# Compared its ordered IDs bijectively with lemma-discovery.json and printed
# the complete canonical inventory plus all counts/differences.
PY
```

The complete result is in `02-rule-inventory.json`.

## Required fresh Stage 4 preflight

The first literal invocation exposed the audit container's numeric `/proc` PID
namespace issue:

```bash
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.klean_preflight import check_generation
check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
PY
```

After compiling the narrowly scoped shim preserved as `proc-self-readlink.c`,
the successful invocation was:

```bash
gcc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/proc-self-readlink.so \
  /tmp/audit-work/proc-self-readlink.c -ldl

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

All attempts and the exact returned result are in `03-preflight.txt` and
`04-preflight-result.json`.

## Independent manifest, obligation, and target checks

```bash
PYTHONPATH=/reference python3 - <<'PY'
# Independently loaded every Stage 4 sidecar, recomputed sidecar/workspace/
# discovery/generated hashes, compared the canonical and classified rule
# sequences, checked the exact empty source-rule/obligation/trust-parameter
# bijection, invoked target_statement, and checked launcher/manifest target
# absence and /candidate absence.
PY
```

The complete result is in `05-manifest-bijection.json`.

## Independent semantic probes

```bash
python3 - <<'PY'
# Independent implementations of the frozen source control flow and the K
# summary recurrences were compared exhaustively for both strings of lengths
# 0..6, followed by boundary and counterfactual witnesses.
PY
```

The complete result is in `06-semantic-probes.txt`.
