# Audit commands

The corresponding raw terminal transcripts are the numbered `.log` files in
this directory. The initial preflight attempts in `04_check_generation.log`
through `04j_lean_path_probe.log` record the sandbox-specific Lean launcher
failure. `04k_proc_exe_shim_and_probe.log` records the narrow compatibility
shim and successful pinned-toolchain probe.

## Producer identity and frozen inputs

```bash
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
python3 -m json.tool /audit-input.json
```

```bash
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
python3 -m json.tool /reference/lemma-discovery.json
```

## Lean sandbox compatibility

The audit sandbox exposes `/proc/self/exe` but not
`/proc/<current-pid>/exe`. Lean 4.22 uses the latter. The shim changes only
that readlink request.

```bash
gcc -shared -fPIC -Wall -Wextra -Werror -O2 \
  /tmp/audit-work/proc_exe_shim.c \
  -o /tmp/audit-work/proc_exe_shim.so -ldl
sha256sum /tmp/audit-work/proc_exe_shim.c \
  /tmp/audit-work/proc_exe_shim.so
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake --version
```

## Required Stage 4 preflight

```bash
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so \
PYTHONPATH=/reference \
python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

```bash
PYTHONPATH=/reference python3 /tmp/audit-work/structural_audit.py
```

## Fresh proof project and clean build

```bash
test ! -e /tmp/audit-work/humaneval-106-f-proof-audit
mkdir -p /tmp/audit-work/humaneval-106-f-proof-audit/Base
cp -a /candidate/Proof.lean /candidate/lakefile.lean \
  /candidate/lake-manifest.json /candidate/lean-toolchain \
  /tmp/audit-work/humaneval-106-f-proof-audit/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/humaneval-106-f-proof-audit/Base/
```

```bash
cd /tmp/audit-work/humaneval-106-f-proof-audit
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake build
```

## Proof identity, axioms, and operational bridge

```bash
cd /tmp/audit-work/humaneval-106-f-proof-audit
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so \
  lake env lean Axioms.lean
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so \
  lake env lean Identity.lean
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so \
  lake env lean AuditBridge.lean
```

```bash
PYTHONPATH=/reference python3 /tmp/audit-work/proof_integrity.py
```

```bash
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so \
PYTHONPATH=/reference \
python3 /reference/tools/stage5_mechanical_check.py \
  --generation /reference/klean-generation \
  --candidate /candidate
```
