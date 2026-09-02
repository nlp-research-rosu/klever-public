# Audit command transcript

The helper programs named below are preserved in this directory. All commands
were run from `/audit-output` unless an explicit `cd` is shown.

```sh
python3 -c 'import json,os; d=json.load(open("/audit-input.json")); print("AUDIT_MODE="+os.environ.get("AUDIT_MODE", "")); print("audit_input_mode="+d["resolution"]["mode"]); print("condition="+d["resolution"]["condition"]); print("semantics_mode="+d["resolution"]["semantics_mode"])'

sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
PYTHONPATH=/reference python3 evidence/producer_provenance_check.py
PYTHONPATH=/reference python3 evidence/inventory_check.py

# Initial environment diagnostic (failed at Lake application-path discovery).
PYTHONPATH=/reference python3 evidence/run_generation_preflight.py

gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/app_path_shim.so \
  /tmp/audit-work/app_path_shim.c -ldl
LD_PRELOAD=/tmp/audit-work/app_path_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/app_path_shim.so \
  /usr/local/bin/assert-frozen-toolchain agent
LD_PRELOAD=/tmp/audit-work/app_path_shim.so PYTHONPATH=/reference \
  python3 evidence/run_generation_preflight.py

PYTHONPATH=/reference python3 evidence/all_recorded_hashes_check.py
PYTHONPATH=/reference python3 evidence/stage4_integrity_check.py

AUDIT_PROJECT=$(mktemp -d /tmp/audit-work/lean-audit.XXXXXX)
cp /candidate/Proof.lean "$AUDIT_PROJECT/Proof.lean"
cp /candidate/lakefile.lean "$AUDIT_PROJECT/lakefile.lean"
cp /candidate/lean-toolchain "$AUDIT_PROJECT/lean-toolchain"
cp /candidate/lake-manifest.json "$AUDIT_PROJECT/lake-manifest.json"
cp -a /reference/klean-generation/generated "$AUDIT_PROJECT/Base"

cd /tmp/audit-work/lean-audit.Bncwtt
LD_PRELOAD=/tmp/audit-work/app_path_shim.so lake clean
LD_PRELOAD=/tmp/audit-work/app_path_shim.so lake build

cd /audit-output
PYTHONPATH=/reference python3 evidence/candidate_source_check.py
cd /tmp/audit-work/lean-audit.Bncwtt
LD_PRELOAD=/tmp/audit-work/app_path_shim.so \
  lake env lean AxiomAudit.lean
LD_PRELOAD=/tmp/audit-work/app_path_shim.so \
  lake env lean BridgeChecks.lean

cd /audit-output
LD_PRELOAD=/tmp/audit-work/app_path_shim.so PYTHONPATH=/reference \
  python3 /reference/tools/klean_final_gate.py \
    --frozen-k /reference/k-proof \
    --discovery-manifest /reference/lemma-discovery.json \
    --generation /reference/klean-generation \
    --candidate /candidate \
    --toolchain-lock /reference/klean-toolchain.lock.json \
    --audit-input /audit-input.json

kompile --backend haskell \
  /reference/k-proof/reference-semantics/semantics.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/lemma-semantics-kompiled
kprove /reference/k-proof/lemma-spec.k \
  --definition /tmp/audit-work/lemma-semantics-kompiled \
  --spec-module LEMMA-SPEC

PYTHONPATH=/reference python3 evidence/axiom_reconciliation.py
sha256sum /reference/lemma-discovery.json \
  /reference/k-proof/verification.k \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-generation/generated/Klean141FileNameCheck/Lemmas.lean \
  /candidate/Proof.lean
```

Outputs, including exit codes for the clean build, proof audit, and fresh K
lemma proof, are in the correspondingly numbered files.
