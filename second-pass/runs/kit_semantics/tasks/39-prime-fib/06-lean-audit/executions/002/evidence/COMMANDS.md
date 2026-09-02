# Audit commands

The raw results are the adjacent numbered `.log` files. The inspection scripts
invoked below are preserved verbatim in this directory.

```sh
env PYTHONPATH=/reference python3 /audit-output/evidence/01_integrity_inventory.py

env LD_PRELOAD=/tmp/audit-work/lean_app_path_fix.so \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/opt/elan/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  PYTHONPATH=/reference \
  python3 /audit-output/evidence/02_generation_preflight.py

env PYTHONPATH=/reference python3 /audit-output/evidence/03_stage4_bijection.py

test ! -e /tmp/audit-work/39-prime-fib-independent-audit
mkdir -p /tmp/audit-work/39-prime-fib-independent-audit
cp -a /reference/klean-generation/generated \
  /tmp/audit-work/39-prime-fib-independent-audit/Base
cp /candidate/Proof.lean /candidate/lake-manifest.json \
  /candidate/lakefile.lean /candidate/lean-toolchain \
  /tmp/audit-work/39-prime-fib-independent-audit/

cd /tmp/audit-work/39-prime-fib-independent-audit
env LD_PRELOAD=/tmp/audit-work/lean_app_path_fix.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake clean
env LD_PRELOAD=/tmp/audit-work/lean_app_path_fix.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake build
env LD_PRELOAD=/tmp/audit-work/lean_app_path_fix.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake env lean Axioms.lean
env LD_PRELOAD=/tmp/audit-work/lean_app_path_fix.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake env lean ProofIdentity.lean
env LD_PRELOAD=/tmp/audit-work/lean_app_path_fix.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake env lean Adversarial.lean
env LD_PRELOAD=/tmp/audit-work/lean_app_path_fix.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake env lean Counterfactual.lean

python3 /audit-output/evidence/09_operational_oracle.py

env LD_PRELOAD=/tmp/audit-work/lean_app_path_fix.so PYTHONPATH=/reference \
  python3 /reference/tools/stage5_mechanical_check.py \
  --generation /reference/klean-generation --candidate /candidate

env PYTHONPATH=/reference python3 /audit-output/evidence/11_candidate_static.py
env PYTHONPATH=/reference python3 /audit-output/evidence/12_audit_input_binding.py

cd /tmp/audit-work/39-prime-fib-independent-audit
env LD_PRELOAD=/tmp/audit-work/lean_app_path_fix.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake env lean Probe.lean
env PYTHONPATH=/reference python3 /audit-output/evidence/14_probe_identity.py
```

The first two preflight attempts, preserved as `02_generation_preflight.log`
and `02_generation_preflight_rerun.log`, failed before any source build because
the audit PID namespace exposes `/proc` from a different namespace. Lean 4.22's
`IO.appPath` asks for `/proc/<namespace-pid>/exe`, which is absent. The successful
attempt interposed only `readlink`, mapping that one path to `/proc/self/exe`.
The interposer source is preserved as `lean_app_path_fix.c`; it does not modify
Lean, Lake, generated source, candidate source, or compiler output.
