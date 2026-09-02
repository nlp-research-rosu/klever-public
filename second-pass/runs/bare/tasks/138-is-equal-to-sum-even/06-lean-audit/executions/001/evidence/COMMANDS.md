# Audit commands

The command outputs are preserved in the adjacent `.log` files.

## Independent hashes, inventory, manifest bijection, and target absence

```bash
script -q -e \
  -c 'PYTHONPATH=/reference python3 /audit-output/evidence/independent_checks.py' \
  /audit-output/evidence/independent-checks.log
```

Exit: `0`.

## Lean sandbox diagnosis and narrow runtime workaround

```bash
script -q -e \
  -c 'bash /audit-output/evidence/lean-runtime-workaround.sh' \
  /audit-output/evidence/lean-runtime-workaround.log
```

Exit: `0`. The script intentionally records the unshimmed Lean startup failure,
compiles the narrow `/proc/<pid>/exe` to `/proc/self/exe` readlink shim, and
then records the pinned Lean 4.22 version successfully.

## Required trusted Stage 4 preflight rerun

```bash
script -q -e \
  -c 'LD_PRELOAD=/tmp/audit-work/proc-self-readlink-shim.so PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH PYTHONPATH=/reference python3 /audit-output/evidence/run_preflight.py' \
  /audit-output/evidence/preflight-rerun-success.log
```

Exit: `0`. Inside `tools.klean_preflight.check_generation`, the logged commands
were:

```text
lake clean
lake build
```

Both exited `0`; the complete output and returned evidence object are in
`preflight-rerun-success.log`.

The earlier environment-discovery attempts are retained in
`preflight-rerun.log`, `preflight-rerun-pinned.log`, and
`preflight-rerun-configured.log`. They failed before a Lean build could occur
because the sandbox does not expose `/proc/<getpid()>/exe`; the successful run
above is the completed required rerun.
