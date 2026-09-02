# Audit commands

This file records the independent audit commands. Command outputs are stored in the adjacent evidence files named below.

## Mode and frozen inputs

```sh
env | rg '^AUDIT_MODE='
python3 -m json.tool /reference/lemma-discovery.json
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/prove.sh
```

Results: `audit-mode-and-selection.txt`, `stage3-protected-classification.json`,
`frozen-verification-k.txt`, `frozen-spec-k.txt`, `frozen-solution-py.txt`, and
`frozen-prove-sh.txt`.

## Trusted Stage 3 inventory reconstruction and trust-boundary check

```sh
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(inventory_verification(Path('/reference/k-proof')),
                 indent=2, sort_keys=True))
PY

PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
workspace = Path('/reference/k-proof')
manifest = Path('/reference/lemma-discovery.json')
inventory = inventory_verification(workspace)
validated = validate_trust_boundary(workspace, manifest)
# Printed canonical hashes, modules, counts, ordering, uniqueness, spans,
# attributes, source text, classifications, and rationales.
PY
```

Results: `stage3-reconstructed-inventory.json` and
`stage3-bijection-check.txt`.

## Producer and immutable-input hashes

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json

PYTHONPATH=/reference python3 - <<'PY'
from tools import pipeline_contract, klean_export
# Recomputed every resolution.hashes tree/file digest with the matching trusted
# algorithm; checked both selected artifact hashes; hashed all 809 files in
# stage1_source_hashes; checked producer file hashes and image IDs across the
# source manifest, generator manifest, and audit-input producer-source path.
PY
```

Results: `generation-producer-file-sha256.txt`,
`recorded-hash-verification.txt`, `generation-source-manifest.json`,
`generator-manifest.json`, and `generation-manifest-hash-bijection.txt`.

## Trusted deterministic-generation preflight

The literal first call was:

```sh
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.klean_preflight import check_generation
check_generation(Path('/reference/k-proof'),
                 Path('/reference/lemma-discovery.json'),
                 Path('/reference/klean-generation'),
                 toolchain_lock=Path('/reference/klean-toolchain.lock.json'))
PY
```

It reached `lake clean` but exposed the container PID/proc mismatch recorded in
`stage4-check-generation-first-attempt.txt`. The independent C probe was built
and run with:

```sh
cc evidence/probe_app_path.c -o /tmp/audit-work/probe_app_path
/tmp/audit-work/probe_app_path
cc -shared -fPIC evidence/proc_exe_readlink_shim.c \
  -o /tmp/audit-work/proc_exe_readlink_shim.so -ldl
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
```

The successful exact trusted call was:

```sh
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so \
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'))
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

Result: `stage4-check-generation.json`. The shim changes only failed
`readlink("/proc/<pid>/exe", ...)` requests to `/proc/self/exe`; it does not
intercept file reads, writes, hashing, Lean elaboration, or input resolution.

## Independent Stage 4 identity checks

```sh
PYTHONPATH=/reference python3 - <<'PY'
# Loaded the protected discovery, input manifest, generator manifest,
# export result, recorded preflight, and obligation map. Compared independently
# reclassified domain IDs with every source-rule and obligation ID list;
# checked uniqueness, all obligation counts, map hash, expected/observed target,
# statuses, trust parameters, theorem/lemma declaration counts, and candidate
# absence.
PY

find /reference/klean-generation/generated -type f -maxdepth 4 | sort
rg -n '^\\s*(theorem|lemma|axiom|opaque|def|abbrev)\\b|\\bsorry\\b|\\badmit\\b|\\bunsafe\\b' \
  /reference/klean-generation/generated -g '*.lean'
nl -ba /reference/klean-generation/generated/Klean162StringToMd5/Lemmas.lean
```

Results: `stage4-independent-identity.txt`, `generated-file-list.txt`,
`generated-declarations-scan.txt`, and `generated-lemmas-lean.txt`.

## Operational semantics comparison

```sh
rg -n -C 6 'md5|hashlib|hexdigest|encode' \
  /reference/k-proof/reference-semantics /reference/k-proof/spec.k
sed -n '316,332p' \
  /reference/k-proof/reference-semantics/semantics/builtins.k
sed -n '50,62p' \
  /reference/k-proof/reference-semantics/semantics/methods.k
rg -n -C 3 'applyCmp\\("==", str|#branch\\(|truthy\\(B:Bool\\)' \
  /reference/k-proof/reference-semantics/semantics -g '*.k'
```

Results: `md5-semantics-search.txt`, `md5-operational-semantics.txt`,
`encode-operational-semantics.txt`, and
`branch-and-string-equality-rules.txt`.

## Trusted final mechanical gate

```sh
LD_PRELOAD=/tmp/audit-work/proc_exe_readlink_shim.so \
PYTHONPATH=/reference python3 /reference/tools/klean_final_gate.py \
  --frozen-k /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --generation /reference/klean-generation \
  --toolchain-lock /reference/klean-toolchain.lock.json \
  --audit-input /audit-input.json
```

Result: `mechanical-final-gate.json`.
