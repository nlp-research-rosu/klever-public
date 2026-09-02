# Audit command ledger

The mounted inputs were treated as read-only evidence. Temporary source and
build products were placed below `/tmp/audit-work`; audit results were placed
below `/audit-output/evidence`.

## Rule inventory and hash comparisons

The trusted inventory implementation was imported from
`/reference/tools/k_rule_inventory.py` and run against the frozen Stage 1
workspace:

```sh
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
from tools.k_rule_inventory import build_rule_inventory
# Build the local verification-module closure rooted at verification.k,
# serialize the canonical inventory, and compare every span/hash/id/order
# against /reference/lemma-discovery.json.
PY
```

Results:

- `01-reconstructed-inventory.json`
- `02-inventory-bijection.txt`
- `06-independent-classification.tsv`

The producer files and all recorded artifact trees/files were hashed with the
trusted repository hash routines and `hashlib.sha256`:

```sh
PYTHONPATH=/reference python3 - <<'PY'
from pathlib import Path
import hashlib
# Hash klean_export.py, klean.py, the producer bundle, all mounted artifacts,
# all 774 Stage 1 files, each obligation binding, and the fixed target.
PY
```

Results:

- `03-producer-provenance.txt`
- `05-hash-and-target-integrity.txt`

## Required Stage 4 preflight

Lean's launcher needed a narrow `/proc/<pid>/exe` compatibility shim because
the audit PID namespace is not reflected by the mounted `/proc`. The shim only
redirects `readlink("/proc/<digits>/exe")` to `/proc/self/exe`; it does not
modify Lean source, generated source, proof source, or proof checking.

```sh
cc -shared -fPIC -O2 -o /tmp/audit-work/proc-self-shim.so \
  /tmp/audit-work/proc-self-shim.c -ldl

LD_PRELOAD=/tmp/audit-work/proc-self-shim.so \
PYTHONPATH=/reference \
python3 - <<'PY'
from pathlib import Path
from tools.klean_preflight import check_generation
import json
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

Result: `04-preflight-return.json`.

## Fresh proof build and axiom audit

The successful fresh workspace was `/tmp/audit-work/lean-proof.GZJvxI`.
`/candidate` was copied there and the generated project was copied into its
`Base` directory.

```sh
cd /tmp/audit-work/lean-proof.GZJvxI
LD_PRELOAD=/tmp/audit-work/proc-self-shim.so lake clean
LD_PRELOAD=/tmp/audit-work/proc-self-shim.so lake build

LD_PRELOAD=/tmp/audit-work/proc-self-shim.so \
  lake env lean /tmp/audit-work/print-axioms-151.lean

LD_PRELOAD=/tmp/audit-work/proc-self-shim.so \
PYTHONPATH=/reference \
python3 /reference/tools/stage5_mechanical_check.py \
  --generation /reference/klean-generation \
  --candidate /candidate
```

Results:

- `08-lake-clean.log`
- `09-lake-build.log`
- `10-print-axioms.log`
- `11-candidate-source.txt`
- `12-candidate-integrity.txt`
- `17-stage5-mechanical-gate.json`

`07-lake-clean-setup-failure.log` records a discarded setup attempt in which
the generated project was copied one directory too deep. No audit conclusion
uses that attempt.

## Operational and counterfactual checks

The source-level adversarial program was converted with the trusted converter
and executed with the frozen Stage 1 runtime:

```sh
python3 /reference/tools/py2mpy.py \
  /tmp/audit-work/operational-checks-151.py
```

The converter's captured stdout was saved verbatim as
`/tmp/audit-work/operational-checks-151.mpy`, then executed:

```sh
krun /tmp/audit-work/operational-checks-151.mpy \
  --definition /reference/k-proof/runtime-kompiled
```

The actual Lean definitions and a deliberately degenerate counterfactual
parameterization were checked separately:

```sh
cd /tmp/audit-work/lean-proof.GZJvxI
LD_PRELOAD=/tmp/audit-work/proc-self-shim.so \
  lake env lean /tmp/audit-work/operational-checks-151.lean

LD_PRELOAD=/tmp/audit-work/proc-self-shim.so \
  lake env lean /tmp/audit-work/counterfactual-target-151.lean
```

Results:

- `13-k-operational-checks.log`
- `15-lean-operational-checks.log`
- `16-counterfactual-target.log`
- `18-operational-bridge.tsv`

`14-lean-operational-checks-harness-failure.log` preserves a discarded audit
harness syntax error; it is not a candidate or proof failure.
