# Audit command index

The numbered `.txt` files in this directory are raw `script(1)` transcripts.
Important commands and their primary result transcripts are listed below.

```sh
printenv AUDIT_MODE
# 00-audit-mode.txt

python3 -m json.tool /audit-input.json
# 01b-audit-input-json.txt

sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
# 06-generation-producer-sha256.txt

PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
# 16-reconstructed-rule-inventory.txt

PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'
# 128-trusted-stage3-contract-check.txt

PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
# 39-rerun-check-generation.txt (expected environment failure diagnosed below)

gcc -shared -fPIC -O2 -Wall -Wextra -Werror -o /audit-output/evidence/lean-proc-exe-shim.so /audit-output/evidence/lean-proc-exe-shim.c -ldl
# 106-build-lean-proc-shim-success.txt

LD_PRELOAD=/audit-output/evidence/lean-proc-exe-shim.so lean --version
# 108-lean-version-with-shim.txt

LD_PRELOAD=/audit-output/evidence/lean-proc-exe-shim.so PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
# 110-rerun-check-generation-success.txt

PYTHONPATH=/reference python3 /audit-output/evidence/independent_integrity_check.py
# 133-independent-integrity-check-final.txt

python3 /audit-output/evidence/summary_model_check.py
# 116-summary-model-check.txt

rg -n '^\s*(theorem|lemma)\b|KleanTarget|target' /reference/klean-generation/generated --glob '*.lean'
# 118-generated-target-search.txt (exit 1 means no match)

rg -n '\b(sorry|admit|unsafe)\b' /reference/klean-generation/generated --glob '*.lean'
# 119-generated-forbidden-search.txt (exit 1 means no match)

test ! -e /candidate
# 129-final-candidate-absence.txt
```

The original preflight failed because the Lean runtime uses
`/proc/<getpid()>/exe`, while the container's mounted `/proc` does not expose
the namespace PID. Evidence `100-app-path-disassembly.txt` and
`101-proc-pid-exe.txt` records that diagnosis. The source-recorded shim only
redirects matching `/proc/*/exe` `readlink` calls to `/proc/self/exe`; it does
not modify inputs, generated Lean, or proof semantics.
