# Audit command record

The mounted inputs were read only. Fresh K build artifacts were created under
`/tmp/audit-work/stage1-independent`; all persistent audit evidence is in this
directory.

## Audit context and producer authentication

```bash
printf 'AUDIT_MODE=%s\n' "$AUDIT_MODE"
kompile --version
kprove --version
LD_PRELOAD=/tmp/audit-work/proc_self_readlink_fix.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake --version
```

Result: `tool-versions.log`.

```bash
PYTHONPATH=/reference python3 \
  /audit-output/evidence/verify_generation_producer.py
```

Result: `generation-producer-authentication.json`.

```bash
PYTHONPATH=/reference python3 -c '
import json
from pathlib import Path
from tools.klean_audit_contract import verify_stage6_audit_input
d=json.loads(Path("/audit-input.json").read_text())
resolution,digest=verify_stage6_audit_input(d)
print(json.dumps({
  "verified": True,
  "resolved_input_sha256": digest,
  "mode": resolution["mode"],
  "problem_id": resolution["problem_id"],
  "semantics_mode": resolution["semantics_mode"],
}, indent=2, sort_keys=True))
'
```

Result: `audit-input-verification.json`.

## Canonical rule inventory and independent classification

```bash
PYTHONPATH=/reference python3 -c '
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(
  inventory_verification(Path("/reference/k-proof")),
  indent=2,
  sort_keys=True,
))
'
```

Result: `stage1-rule-inventory.json`.

```bash
mkdir -p /tmp/audit-work/stage1-independent
cp -a /reference/k-proof/reference-semantics \
  /tmp/audit-work/stage1-independent/reference-semantics
cp -a /reference/k-proof/domain.k \
  /reference/k-proof/verification-core.k \
  /reference/k-proof/loop-connection-spec.k \
  /tmp/audit-work/stage1-independent/
cd /tmp/audit-work/stage1-independent
kompile --backend haskell verification-core.k \
  --main-module VERIFICATION-CORE \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-connection-kompiled
kprove loop-connection-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-CONNECTION-SPEC
```

Results: `fresh-loop-connection-kompile.log` and
`fresh-loop-connection-kprove.log`.

The imported list-iterator bridge was also checked against a definition that
does not contain it:

```bash
cp -a /reference/k-proof/connection-spec.k \
  /tmp/audit-work/stage1-independent/
cd /tmp/audit-work/stage1-independent
kompile --backend haskell domain.k \
  --main-module STRING-SEQUENCE-DOMAIN \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
```

Results: `fresh-iterator-connection-kompile.log` and
`fresh-iterator-connection-kprove.log`.

```bash
cp -a /reference/k-proof/verification.k \
  /reference/k-proof/spec.k \
  /tmp/audit-work/stage1-independent/
cd /tmp/audit-work/stage1-independent
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Results: `fresh-final-kompile.log` and `fresh-final-kprove.log`.

The non-vacuity counterexample was rerun against that fresh final definition:

```bash
cp -a /reference/k-proof/spec-vacuity.k \
  /tmp/audit-work/stage1-independent/
cd /tmp/audit-work/stage1-independent
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Result: `fresh-vacuity-mutation-kprove.log`. It exits 1 with
`WarnStuckClaimState`, as required for the false result mutation.

```bash
PYTHONPATH=/reference python3 \
  /audit-output/evidence/verify_stage3_classification.py
```

Result: `stage3-classification-verification.json`.

## Deterministic Stage 4 preflight

The container exposes a host `/proc` that is not PID-namespace aligned. The
pinned Lean runtime therefore initially queried a wrong or absent
`/proc/<pid>/exe`. The raw failures and diagnosis are retained in the
`klean-preflight-rerun-*-failure.*` and
`lean-runtime-readlink-diagnostic.log` files.

The minimal environment shim was compiled with:

```bash
gcc -shared -fPIC \
  -o /tmp/audit-work/proc_self_readlink_fix.so \
  /audit-output/evidence/proc_self_readlink_fix.c \
  -ldl
```

It redirects only `/proc/<pid>/exe` reads to `/proc/self/exe`. The trusted
preflight was then invoked with its documented API:

```bash
PYTHONPATH=/reference python3 \
  /audit-output/evidence/run_klean_preflight.py
```

`run_klean_preflight.py` calls
`tools.klean_preflight.check_generation` with the three required inputs and
the pinned toolchain lock. Its runner only selects the pinned Lake executable
and injects the namespace shim. Result: `klean-preflight-rerun.json`;
exit status: `klean-preflight-rerun.exit`.

## Independent hash, bijection, and target checks

```bash
PYTHONPATH=/reference python3 \
  /audit-output/evidence/verify_recorded_hashes.py
```

Result: `recorded-hash-verification.json`; exit status:
`recorded-hash-verification.exit`.

No Stage 5 commands were run because both `AUDIT_MODE` and the verified audit
input say `CLASSIFICATION_ONLY`, the generated target is absent, and no
`/candidate` exists.
