# Audit command record

The numbered `.sh` and `.py` files in this directory are the exact command
and checker sources used. Their corresponding `.log` files contain stdout,
stderr, and exit status as captured by `script -q -e`.

The two principal trusted-tool invocations were:

```sh
env PYTHONPATH=/reference \
  LD_PRELOAD=/tmp/audit-work/proc_self_readlink_shim.so \
  LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
  python3 /audit-output/evidence/08_rerun_klean_preflight.py
```

```sh
env PYTHONPATH=/reference \
  LD_PRELOAD=/tmp/audit-work/proc_self_readlink_shim.so \
  LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
  python3 /audit-output/evidence/12_run_mechanical_final_gate.py
```

The `LD_PRELOAD` library is built from
`/audit-output/evidence/proc_self_readlink_shim.c`. It changes only a
`readlink("/proc/<current-pid>/exe", ...)` request into
`readlink("/proc/self/exe", ...)`, working around the audit sandbox's
numeric-PID `/proc` restriction. Every other `readlink` is delegated
unchanged. The source, build command, library hash, and Lean/Lake version
checks are in `11_build_and_test_proc_shim.sh` and its log.
