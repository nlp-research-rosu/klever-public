# Audit command transcript index

The evidence files named below contain the complete stdout/stderr and exit status captured for the material commands. Superseded setup attempts are retained rather than deleted.

```sh
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
# result: 02_producer_hashes.txt

PYTHONPATH=/reference python3 /audit-output/evidence/audit_structural.py
# result: 16_structural_reconstruction_v2.txt

PYTHONPATH=/reference LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so \
  python3 /audit-output/evidence/run_preflight.py
# result: 31_fresh_preflight_with_shim.txt

PYTHONPATH=/reference python3 /audit-output/evidence/audit_stage4.py
# result: 38_independent_stage4_hash_bijection.txt

cd /tmp/audit-work/lean-audit-DaSChT
LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake clean
# result: 40_proof_lake_clean.txt

LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake build
# result: 41_proof_lake_build.txt

LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake env lean AxiomAudit.lean
# result: 42_print_axioms.txt

LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake env lean OperationalAuditInternal.lean
# result: 44_operational_internal_tests.txt

LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so lake env lean OperationalAudit.lean
# result: 45_operational_counterfactual_tests.txt

PYTHONPATH=/reference python3 /audit-output/evidence/audit_candidate.py
# result: 48_candidate_identity_axioms.txt

PYTHONPATH=/reference LD_PRELOAD=/tmp/audit-work/proc_exe_shim.so \
  python3 /reference/tools/stage5_mechanical_check.py \
  --generation /reference/klean-generation --candidate /candidate
# result: 49_stage5_mechanical_check.txt

python3 /audit-output/evidence/audit_recorded_file_hashes.py
# result: 50_recorded_file_hashes.txt
```

The first unshimmed generation preflight is retained in `29_fresh_preflight.txt`; it reached and passed structural checks, then Lean could not resolve its executable through the sandbox's hidden numeric `/proc/<pid>/exe`. `30_lean_environment.txt` records that environment. The small `readlink` compatibility shim source and binary are `/tmp/audit-work/proc_exe_shim.c` and `/tmp/audit-work/proc_exe_shim.so`; it changes only `/proc/*/exe` resolution to `/proc/self/exe` and does not modify the candidate, generator, or toolchain. The first project-copy layout error is retained in `39_proof_lake_clean.txt`; the correctly laid-out fresh copy produced `40_proof_lake_clean.txt` and `41_proof_lake_build.txt`.
