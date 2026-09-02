# Audit commands

The mounted inputs were read-only. The persistent fresh proof project is
`/tmp/audit-work/proof-audit-112`, with the immutable generated project copied
to `Base`.

Lean 4.22 calls `readlink("/proc/<getpid()>/exe")`. This audit sandbox exposes
virtualized process IDs that are absent from the mounted `/proc`, so the first
preflight attempt failed before compiling Lean. The source of the narrow
`readlink` redirect used for subsequent Lean commands is
`proc-self-exe-fix.c`; it changes `/proc/<pid>/exe` lookups to
`/proc/self/exe` and changes no project input.

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /audit-input.json \
  /reference/lemma-discovery.json

PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_producer_provenance.py

PYTHONPATH=/reference \
  python3 /audit-output/evidence/reconstruct_inventory.py

PYTHONPATH=/reference \
LD_PRELOAD=/tmp/audit-work/proc-self-exe-fix.so \
  python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")), indent=2, sort_keys=True))'

PYTHONPATH=/reference \
  python3 /audit-output/evidence/verify_stage4_and_candidate_integrity.py

mkdir /tmp/audit-work/proof-audit-112
cp -a /candidate/. /tmp/audit-work/proof-audit-112/
mv /tmp/audit-work/proof-audit-112/Base \
  /tmp/audit-work/proof-audit-112-initial-empty-base-copy
cp -a /reference/klean-generation/generated \
  /tmp/audit-work/proof-audit-112/Base

cd /tmp/audit-work/proof-audit-112
LD_PRELOAD=/tmp/audit-work/proc-self-exe-fix.so lake clean
LD_PRELOAD=/tmp/audit-work/proc-self-exe-fix.so lake build
LD_PRELOAD=/tmp/audit-work/proc-self-exe-fix.so \
  lake env lean AxiomAudit.lean
LD_PRELOAD=/tmp/audit-work/proc-self-exe-fix.so \
  lake env lean OperationalBridgeAudit.lean

PYTHONPATH=/reference \
LD_PRELOAD=/tmp/audit-work/proc-self-exe-fix.so \
  python3 -c 'import json; from pathlib import Path; from tools.klean_final_gate import check_proof_candidate; print(json.dumps(check_proof_candidate(Path("/reference/klean-generation"), Path("/candidate")), indent=2, sort_keys=True))'

PYTHONPATH=/reference \
  python3 /audit-output/evidence/reconcile_proof_axioms.py
```

The exact output of each material command is in the correspondingly named
`.log` file in this directory. Failed first attempts are retained rather than
deleted; the accepted reruns have `fixed` or `final` in their names and exit
zero.
