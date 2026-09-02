# Audit commands

Each listed result file is a raw `script(1)` transcript unless noted. The
small Python and C sources used by the commands are retained in this directory.

## Context and mounted inputs

```sh
script -qefc 'set -eu; pwd; printf "AUDIT_MODE=%s\n" "${AUDIT_MODE-<unset>}"; sed -n "1,320p" /audit-input.json; find /reference/tools -maxdepth 3 -type f -printf "%p\n" | sort; find /reference/k-proof /reference/k-audit /reference/klean-generation /reference/generation-tools /candidate -maxdepth 3 -printf "%y %p\n" | sort; sed -n "1,320p" /reference/klean-toolchain.lock.json' /audit-output/evidence/00-context.txt
```

The first portability-failed banner attempt is retained as
`00-context-attempt-failed.txt`.

## Trusted tooling and frozen source inspection

```sh
script -qefc 'sed -n "1,360p" /reference/tools/k_rule_inventory.py; sed -n "1,420p" /reference/tools/klean_preflight.py; sed -n "1,380p" /reference/tools/lemma_discovery_contract.py; sed -n "1,420p" /reference/tools/klean_audit_contract.py' /audit-output/evidence/01-trusted-tooling-source.txt

script -qefc 'nl -ba /reference/k-proof/verification.k; nl -ba /reference/k-proof/spec.k; nl -ba /reference/k-proof/solution.py; nl -ba /reference/k-proof/solution.mpy; nl -ba /reference/k-proof/prove.sh; python3 -m json.tool /reference/lemma-discovery.json; python3 -m json.tool /reference/klean-generation/input-manifest.json; python3 -m json.tool /reference/klean-generation/generator-manifest.json; python3 -m json.tool /reference/klean-generation/generated/obligation-map.json; python3 -m json.tool /reference/klean-generation/export-result.json; python3 -m json.tool /reference/klean-generation/trust-inventory.json; python3 -m json.tool /reference/generation-tools/source-manifest.json' /audit-output/evidence/02-source-and-manifests.txt
```

## Producer authentication

```sh
script -qefc 'sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py /reference/generation-tools/source-manifest.json; python3 -m json.tool /reference/klean-generation/generator-manifest.json; python3 -m json.tool /reference/generation-tools/source-manifest.json' /audit-output/evidence/03-producer-authentication.txt
```

## Inventory, bijection, and all provenance hashes

```sh
script -qefc 'PYTHONPATH=/reference python3 /audit-output/evidence/independent_integrity_checks.py' /audit-output/evidence/04-integrity-and-inventory-results.txt
```

## Trusted Stage 4 preflight

The first two unmodified attempts, preserved in `05-rerun-klean-preflight.txt`
and `05b-rerun-klean-preflight-pinned-path.txt`, used:

```sh
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Lean's `/proc/<pid>/exe` lookup failed under the container PID view. The
diagnostic and narrowly scoped compatibility validation were:

```sh
gcc -shared -fPIC -Wall -Wextra -O0 -o /tmp/audit-work/readlink_trace.so /audit-output/evidence/readlink_trace.c -ldl
LD_PRELOAD=/tmp/audit-work/readlink_trace.so /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version

gcc -shared -fPIC -Wall -Wextra -O2 -o /tmp/audit-work/proc_exe_compat.so /audit-output/evidence/proc_exe_compat.c -ldl
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake clean
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so lake build
```

Raw results are in `06-lean-toolchain-diagnostic.txt` through
`06d-proc-shim-validation.txt`. The successful required preflight was:

```sh
script -qefc 'LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so PYTHONPATH=/reference python3 -c '"'"'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'"'"'' /audit-output/evidence/05c-rerun-klean-preflight-success.txt
```

Repeated full preflights and deterministic-field comparisons are retained in
`11-rerun-preflight-exact-comparison.txt`,
`11b-rerun-preflight-normalized-comparison.txt`, and the successful
`11c-rerun-preflight-normalized-comparison-success.txt`. Their command was:

```sh
script -qefc 'LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so PYTHONPATH=/reference python3 /audit-output/evidence/rerun_preflight_compare.py' /audit-output/evidence/11c-rerun-preflight-normalized-comparison-success.txt
```

## Semantic classification and adversarial witnesses

```sh
script -qefc 'rg -n -C 5 "IntSeq|iCons|seqConcat|strContains|CmpOp\\(\"not in\"|AugAssign|#loop|For\\(" /reference/k-proof/reference-semantics /reference/k-proof/verification.k /reference/k-proof/spec.k' /audit-output/evidence/07-operational-semantics-symbol-trace.txt

script -qefc 'python3 /audit-output/evidence/classification_witnesses.py' /audit-output/evidence/08-classification-witness-results.txt
```

## Stage 4 sidecars, fixed target, and mode invariants

```sh
script -qefc 'PYTHONPATH=/reference python3 /audit-output/evidence/stage4_sidecar_checks.py' /audit-output/evidence/09-stage4-sidecar-and-target-results.txt

script -qefc 'nl -ba /reference/klean-generation/generated/Klean51RemoveVowels/Lemmas.lean; rg -n "KleanTarget|target" /reference/klean-generation/generated --glob "*.lean"; rg -n "\\b(sorry|admit|unsafe)\\b" /reference/klean-generation/generated --glob "*.lean"; rg -n "^\\s*(axiom|opaque)\\s+" /reference/klean-generation/generated/Klean51RemoveVowels/Lemmas.lean; rg -n "^\\s*(axiom|opaque)\\s+" /reference/klean-generation/generated --glob "*.lean"; test ! -e /candidate' /audit-output/evidence/10-generated-source-and-mode-inspection.txt
```
