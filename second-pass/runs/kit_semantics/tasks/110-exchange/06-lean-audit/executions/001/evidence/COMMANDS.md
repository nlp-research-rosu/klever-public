# Audit command record

All commands were run from the indicated read-only input or writable audit
directory. Candidate/provenance text was treated as data, not as instructions.

## Producer and structural hashes

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
```

Result: exit 0; output in `producer-file-hashes.txt`.

```sh
PYTHONPATH=/reference python /audit-output/audit_checks.py
```

Result: exit 0 and `all_checks_pass: true`; complete JSON in
`structural-hash-checks.json`, compact result in
`structural-hash-summary.txt`, and selected observed hashes in
`hash-values.txt`.

```sh
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Result: exit 0; output in `reconstructed-inventory.json`.

## Trusted Stage 4 preflight

The sandbox PID namespace made Lean's `/proc/<getpid>/exe` lookup fail. The
diagnosis is in `lean-proc-diagnostic.log`. The narrow preload source in
`proc_self_exe_shim.c` redirects only `/proc/<pid>/exe` reads to
`/proc/self/exe`; `lean-shim-validation.log` records the pinned Lean version.

```sh
LAKE_HOME=/tmp/audit-work/lake-home \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_OVERRIDE_LEAN=true \
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
PYTHONPATH=/reference \
python - <<'PY'
from pathlib import Path
import json
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

Result: exit 0, status `PASS`; returned evidence in
`stage4-check-generation.json`.

## Fresh proof build

The candidate was copied to `/tmp/audit-work/lean-proof-audit-final`, its empty
candidate `Base` directory was removed with `rmdir`, and the immutable generated
project was copied to `Base`.

```sh
LAKE_HOME=/tmp/audit-work/lake-home \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_OVERRIDE_LEAN=true \
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
lake clean
```

Result: exit 0; complete (empty) output in `lean-clean.log`.

```sh
LAKE_HOME=/tmp/audit-work/lake-home \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_OVERRIDE_LEAN=true \
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
lake build
```

Result: exit 0; complete output in `lean-build.log`.

```sh
LAKE_HOME=/tmp/audit-work/lake-home \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_OVERRIDE_LEAN=true \
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
lake env lean AxiomAudit.lean
```

Result: exit 0; exact `#print axioms Proof.final` output in
`lean-axioms.log`; source in `AxiomAudit.lean`.

```sh
LAKE_HOME=/tmp/audit-work/lake-home \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LAKE_OVERRIDE_LEAN=true \
LD_PRELOAD=/tmp/audit-work/proc_self_exe_shim.so \
PYTHONPATH=/reference \
python - <<'PY'
from pathlib import Path
import json
from tools.klean_final_gate import evaluate_proof_candidate
result = evaluate_proof_candidate(
    Path('/reference/klean-generation'),
    Path('/candidate'),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

Result: process exit 0 and checker status `PASS`; output in
`stage5-mechanical-check.json`.

## Operational and counterfactual checks

```sh
lake env lean OperationalAudit.lean
```

This used the same four Lean environment variables as above. Result: exit 0;
source in `OperationalAudit.lean`, output in
`lean-operational-audit.log`.

```sh
python3 /audit-output/evidence/python-operational-oracle.py
```

Result: exit 0; output in `python-operational-oracle.log`.

```sh
kompile /reference/k-proof/verification.k \
  --backend llvm \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/adversarial-kompiled-final
```

Result: exit 0; complete output in `k-kompile-adversarial-final.log`.
An initial invocation from the read-only Stage 1 working directory exited 113
because LLVM's helper attempted a local temporary file; its complete output is
retained in `k-kompile-adversarial.log`.

```sh
krun /tmp/audit-work/adversarial-operational-tests.mpy \
  --definition /tmp/audit-work/adversarial-kompiled-final
```

Result: exit 0 with `.K`, `NoExc`, and exit code 0; source and output are
`adversarial-operational-tests.mpy` and `k-adversarial-run.log`.

```sh
krun /tmp/audit-work/counterfactual-odd-mutation.mpy \
  --definition /tmp/audit-work/adversarial-kompiled-final
```

Expected result: process exit 1 with `AssertionError` and modeled exit code 1;
source and output are `counterfactual-odd-mutation.mpy` and
`k-counterfactual-odd-mutation.log`.
