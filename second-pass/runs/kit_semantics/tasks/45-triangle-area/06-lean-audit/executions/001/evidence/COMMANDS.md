# Audit commands

The numbered `.log` files contain the corresponding raw results. Commands are
listed without the outer `script -q -e -c ... LOG` capture wrapper.

## 01–02 producer and manifest provenance

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /audit-input.json
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
python3 -m json.tool /reference/klean-generation/input-manifest.json
test -e /candidate && echo CANDIDATE_PRESENT || echo CANDIDATE_ABSENT
```

## 03 frozen sources and protected classification

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/prove.sh
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
python3 -m json.tool /reference/lemma-discovery.json
```

## 04 trusted rule-inventory reconstruction

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/inventory_check.py
```

## 05 Stage 4 sidecars

```sh
python3 -m json.tool /reference/klean-generation/export-result.json
python3 -m json.tool /reference/klean-generation/trust-inventory.json
python3 -m json.tool /reference/klean-generation/generated/obligation-map.json
python3 -m json.tool /reference/klean-generation/preflight.json
python3 -m json.tool /reference/klean-toolchain.lock.json
```

## 06 operational-semantics excerpts

```sh
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k | sed -n '1,55p'
nl -ba /reference/k-proof/reference-semantics/semantics/float.k | sed -n '1,40p;100,145p;185,210p'
nl -ba /reference/k-proof/reference-semantics/semantics/call.k | sed -n '1,105p'
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k | sed -n '35,90p'
nl -ba /reference/k-proof/reference-semantics/semantics/core.k | sed -n '115,145p'
```

## 07 independent hashes and bijection

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/hash_and_bijection_check.py
```

## 08 initial exact preflight rerun

```sh
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result = check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

This reached `lake clean` and exposed the container's PID/procfs mismatch. Logs
09–12 diagnose that mismatch. The compatibility library was built with:

```sh
gcc -shared -fPIC /tmp/audit-work/proc_exe_compat.c \
  -o /tmp/audit-work/proc_exe_compat.so -ldl
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lean --version
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake --version
```

## 13 successful exact preflight rerun

```sh
PYTHONPATH=/reference \
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result = check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

## 14 target and Stage 5 absence

```sh
nl -ba /reference/klean-generation/generated/Klean45TriangleArea/Lemmas.lean
rg -n '(^|[[:space:]])(theorem|lemma|example)[[:space:]]|Proof\.final|def[[:space:]]+target|KleanTarget' \
  /reference/klean-generation/generated -g '*.lean'
test -e /candidate && echo PRESENT || echo ABSENT
```

## 15 integer operator semantics

```sh
rg -n 'applyBin\("\*"|applyBin\("/"' \
  /reference/k-proof/reference-semantics/semantics/int.k
nl -ba /reference/k-proof/reference-semantics/semantics/int.k | sed -n '1,55p'
```

## 16 trusted mechanical final gate

```sh
PYTHONPATH=/reference \
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
python3 /reference/tools/klean_final_gate.py \
  --frozen-k /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --generation /reference/klean-generation \
  --toolchain-lock /reference/klean-toolchain.lock.json \
  --audit-input /audit-input.json \
  --output /audit-output/evidence/16-mechanical-final-gate.json
```
