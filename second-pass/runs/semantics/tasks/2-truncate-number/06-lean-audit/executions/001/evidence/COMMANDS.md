# Audit command record

All paths below are the mounted audit paths. Output files named alongside each
command contain the captured stdout/stderr and, for gates, a separate exit-code
file.

## Launcher and producer hashes

```bash
env | rg '^AUDIT_MODE='
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
sed -n '1,260p' /audit-input.json
```

Results: `00-launcher-mode-and-producer-sha256.txt`,
`01-audit-input.json.txt`.

## Canonical Stage 1 rule inventory

```bash
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Result: `03-reconstructed-rule-inventory.json`.

```bash
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")),indent=2,sort_keys=True))'
```

Result: `23-validated-stage3-trust-boundary.json`.

The frozen source and relevant operational semantics were read with:

```bash
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/prompt.py
nl -ba /reference/k-proof/reference-semantics/semantics/float.k | sed -n '1,80p'
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k | sed -n '1,100p'
nl -ba /reference/k-proof/reference-semantics/semantics/call.k | sed -n '1,90p'
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k | sed -n '1,115p'
```

Results: `04-verification.k.txt`, `05-spec.k.txt`,
`06-solution.mpy.txt`, `07-solution.py.txt`, `11-float-semantics-core.txt`,
`12-operator-dispatch.txt`, `13-call-semantics.txt`,
`14-function-semantics.txt`, and `85-prompt.py.txt`.

## Hash reconstruction

```bash
PYTHONPATH=/reference python -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; paths=["/reference/k-proof","/reference/k-audit","/reference/klean-generation","/reference/generation-tools"]; [print(sha256_tree(Path(p)),p) for p in paths]'
```

Result: `19-pipeline-tree-digests.txt`.

```bash
PYTHONPATH=/reference python -c \
  'from pathlib import Path; from tools.klean_export import tree_digest; paths=["/reference/k-proof","/reference/klean-generation/generated"]; [print(tree_digest(Path(p)),p) for p in paths]'
```

The relevant values are included in
`84-independent-stage3-stage4-verification.json`.

```bash
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.stage6_resolution_contract import verify_audit_input; d=json.loads(Path("/audit-input.json").read_text()); r,h=verify_audit_input(d); print(json.dumps({"verified": True, "resolved_input_sha256": h, "mode": r["mode"]}, sort_keys=True))'
```

Result: `20-audit-input-envelope-verification.txt`.

```bash
sha256sum /reference/lemma-discovery.json \
  /reference/klean-generation/input-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/trust-inventory.json \
  /reference/klean-generation/export-result.json \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-toolchain.lock.json /audit-input.json
```

Result: `16-sidecar-file-sha256.txt`.

## Required generation preflight

The first exact invocation, before the sandbox compatibility diagnosis, was:

```bash
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; r=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(r,indent=2,sort_keys=True))'
```

It exited 1 because Lean 4.22 attempted `/proc/<namespace-pid>/exe`, which this
sandbox does not expose. Results:
`24-check-generation-output.txt`,
`24-check-generation-exit-code.txt`, and diagnostics `25` through `69`.

The narrow compatibility library in `proc_exe_compat.c` was built with:

```bash
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/libproc-exe-compat.so \
  /audit-output/evidence/proc_exe_compat.c -ldl
```

Results: `70-proc-exe-compat-build-output.txt` and
`70-proc-exe-compat-build-exit-code.txt`. Its effect was checked with:

```bash
LD_PRELOAD=/tmp/audit-work/libproc-exe-compat.so lean --version
LD_PRELOAD=/tmp/audit-work/libproc-exe-compat.so lake env
```

Results: `71-lean-version-with-proc-shim.txt`,
`72-lake-env-with-proc-shim.txt`.

The unchanged trusted checker was then rerun:

```bash
LD_PRELOAD=/tmp/audit-work/libproc-exe-compat.so \
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; r=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(r,indent=2,sort_keys=True))'
```

Results: `73-check-generation-rerun-output.txt` and
`73-check-generation-rerun-exit-code.txt`.

## Independent Stage 3/4 cross-check

```bash
PYTHONPATH=/reference python \
  /audit-output/evidence/verify_stage3_stage4.py
```

Results: `84-independent-stage3-stage4-verification.json` and
`84-independent-stage3-stage4-verification-exit-code.txt`.

The generated no-obligation artifacts and candidate absence were inspected
with:

```bash
cat /reference/klean-generation/generated/obligation-map.json
cat /reference/klean-generation/export-result.json
cat /reference/klean-generation/preflight.json
nl -ba /reference/klean-generation/generated/Klean2TruncateNumber/Lemmas.lean
find /candidate -maxdepth 1 -print
```

Results: `74-obligation-map.json.txt` through
`80-candidate-absence.txt`.
