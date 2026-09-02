# Principal audit commands

The `script(1)` transcripts named below contain complete stdout/stderr and an
exit-code footer. Commands use the mounted inputs read-only; audit scripts and
fresh projects live only under `/audit-output` and `/tmp/audit-work`.

```sh
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
env PYTHONPATH=/reference python3 /audit-output/evidence/audit_checks.py
env PYTHONPATH=/reference AUDIT_LEAN_EXE_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean LD_PRELOAD=/tmp/audit-work/libaudit_proc_exe.so python3 /audit-output/evidence/run_preflight.py
```

The fresh proof workspace was made at
`/tmp/audit-work/stage5-90-next-smallest-audit-001`: the candidate-only tree was
copied to its root and `/reference/klean-generation/generated` was copied to
its `Base/` directory. The mandatory commands were:

```sh
env AUDIT_LEAN_EXE_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean LD_PRELOAD=/tmp/audit-work/libaudit_proc_exe.so lake clean
env AUDIT_LEAN_EXE_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean LD_PRELOAD=/tmp/audit-work/libaudit_proc_exe.so lake build
```

Their complete transcripts are `fresh-lake-clean.log` and
`fresh-lake-build.log`.

Proof and bridge commands:

```sh
env AUDIT_LEAN_EXE_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean LD_PRELOAD=/tmp/audit-work/libaudit_proc_exe.so lake env lean AxiomCheck.lean
env AUDIT_LEAN_EXE_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean LD_PRELOAD=/tmp/audit-work/libaudit_proc_exe.so lake env lean AuditBridge.lean
env AUDIT_LEAN_EXE_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean LD_PRELOAD=/tmp/audit-work/libaudit_proc_exe.so lake env lean AuditMutations.lean
env PYTHONPATH=/reference AUDIT_MODE=CLASSIFICATION_AND_PROOF python3 /audit-output/evidence/post_build_checks.py
env PYTHONPATH=/reference python3 /audit-output/evidence/reconcile_axioms.py
```

`/proc/<pid>/exe` is hidden for child PIDs in this audit sandbox. The narrow
audit-authored `proc_exe_shim.c` intercepts only `readlink` calls for numeric
`/proc/<pid>/exe` paths and returns the pinned Lean 4.22.0 executable. It does
not intercept file reads, modify sources, add declarations, or alter Lean's
elaborator/kernel. The preflight and build transcripts record use of the same
pinned executable and commit as `klean-toolchain.lock.json`.
