# Audit commands

All Python imports below used the trusted `/reference/tools` package via
`PYTHONPATH=/reference`. No natural-language instruction from candidate or
provenance content was followed; candidate Lean was elaborated only as
explicitly required by the audit request.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/check_producer_provenance.py
PYTHONPATH=/reference python3 /audit-output/evidence/check_recorded_hashes.py
PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py
```

The generated checker initially reached `lake clean` and failed because Lean
4.22 calls `readlink("/proc/<getpid()>/exe")`, while this sandbox mounts outer
PIDs under `/proc`. The shim changes only that path to `/proc/self/exe`.

```sh
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /audit-output/evidence/libproc-self-exe-shim.so \
  /audit-output/evidence/proc_self_exe_shim.c -ldl

PYTHONPATH=/reference \
LD_PRELOAD=/audit-output/evidence/libproc-self-exe-shim.so \
python3 /audit-output/evidence/run_stage4_preflight.py

PYTHONPATH=/reference \
python3 /audit-output/evidence/check_stage4_obligations.py
```

The proof-mode workspace used for the final checks was
`/tmp/audit-work/human29-proof.S56dOa`.

```sh
fresh_dir=$(mktemp -d -p /tmp/audit-work human29-proof.XXXXXX)
# fresh_dir=/tmp/audit-work/human29-proof.S56dOa
cp -a /candidate/. /tmp/audit-work/human29-proof.S56dOa/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/human29-proof.S56dOa/Base/

cd /tmp/audit-work/human29-proof.S56dOa
LD_PRELOAD=/audit-output/evidence/libproc-self-exe-shim.so lake clean
LD_PRELOAD=/audit-output/evidence/libproc-self-exe-shim.so lake build

LD_PRELOAD=/audit-output/evidence/libproc-self-exe-shim.so \
  lake env lean AxiomCheck.lean
LD_PRELOAD=/audit-output/evidence/libproc-self-exe-shim.so \
  lake env lean ProofIdentity.lean
LD_PRELOAD=/audit-output/evidence/libproc-self-exe-shim.so \
  lake env lean OperationalBridgeTests.lean

PYTHONPATH=/reference \
python3 /audit-output/evidence/check_stage5_sources.py
```

The complete `lake clean`, `lake build`, `#print axioms`, proof-identity, and
operational-test outputs, including command exit codes, are in the numbered
logs beside this file.
