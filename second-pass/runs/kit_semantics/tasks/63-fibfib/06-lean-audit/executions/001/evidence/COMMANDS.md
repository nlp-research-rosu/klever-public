# Audit command ledger

All paths below are the mounted read-only inputs or the fresh workspace
`/tmp/audit-work/63-fibfib-proof.zz70ap`.

The sandbox exposes a PID namespace whose numeric PIDs are absent from its
mounted `/proc`. Lean therefore initially failed while resolving
`/proc/<pid>/exe`. The initial failure is preserved in
`05a-preflight-initial-failure.log`. The small source-only compatibility shim
`proc-exe-readlink-shim.c` supplies only the pinned Lean executable path for
that readlink; it does not intercept file reads, proof checking, compilation,
or theorem output.

## Provenance and inventory

```sh
env PYTHONPATH=/reference \
  python3 /audit-output/evidence/01-provenance-and-hashes.py

env PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True, ensure_ascii=False))'

env PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; r=validate_trust_boundary(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json")); print(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False))'

env PYTHONPATH=/reference \
  python3 /audit-output/evidence/04-independent-bijection.py
```

Results are in `01-provenance-and-hashes.log`,
`02-reconstructed-inventory.json`, `03-stage3-contract.json`, and
`04-independent-bijection.log`.

## Deterministic generation

Initial environment-diagnostic invocation:

```sh
env PYTHONPATH=/reference python3 -c \
  'from pathlib import Path; from tools.klean_preflight import check_generation; check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json"))'
```

Pinned-toolchain rerun:

```sh
env \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/opt/elan/bin:/opt/runtimeverification-k/pyk/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  PYTHONPATH=/reference \
  LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  AUDIT_LEAN_APP_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake \
  python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; r=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False))'

env PYTHONPATH=/reference \
  python3 /audit-output/evidence/06-stage4-independent-audit.py
```

Results are in `05a-preflight-initial-failure.log`,
`05b-preflight-rerun.json`, and `06-stage4-independent-audit.log`.

## Fresh proof workspace and build

```sh
mktemp -d /tmp/audit-work/63-fibfib-proof.XXXXXX
cp -a /candidate/. /tmp/audit-work/63-fibfib-proof.zz70ap/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/63-fibfib-proof.zz70ap/Base/

env \
  LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  AUDIT_LEAN_APP_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/opt/elan/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  lake clean

env \
  LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  AUDIT_LEAN_APP_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/opt/elan/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  lake build
```

Complete terminal transcripts, including exit codes, are in
`07a-lake-clean.log` and `07b-lake-build.log`.

## Trusted gate, theorem identity, axioms, and bridges

```sh
env \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/opt/elan/bin:/opt/runtimeverification-k/pyk/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  PYTHONPATH=/reference \
  LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  AUDIT_LEAN_APP_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake \
  python3 -c \
  'import json; from pathlib import Path; from tools.klean_final_gate import check_final; r=check_final(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),Path("/candidate"),toolchain_lock=Path("/reference/klean-toolchain.lock.json"),audit_input=Path("/audit-input.json")); print(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False))'

lake env lean AxiomAudit.lean
lake env lean BridgeAudit.lean
lake env lean BridgeDefinitionProof.lean

env PYTHONPATH=/reference \
  python3 /audit-output/evidence/12-candidate-static-audit.py
python3 /audit-output/evidence/13-operational-bridge-audit.py
env PYTHONPATH=/reference \
  python3 /audit-output/evidence/14-axiom-accounting.py
```

The three `lake env lean` commands used the same pinned `PATH`,
`LD_PRELOAD`, and `AUDIT_LEAN_APP_PATH` values shown above. Their exact inputs
are stored beside this ledger. Passing outputs are in
`09-print-axioms.log`, `10d-bridge-adversarial.log`, and
`11b-bridge-definition-proof.log`. Earlier `10*` and `11-*` logs preserve
failed audit-harness formulations; they do not alter or test a different
candidate.
