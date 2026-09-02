# Audit command ledger

All mounted reference and candidate paths were treated read-only. The scripts
named below perform only reads of those paths; temporary build output was
created under `/tmp/audit-work` or by the trusted preflight's temporary
directory.

## Producer and immutable-input hashes

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
```

Result: `06-producer-sha256.txt`.

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/20_verify_hashes.py
```

Result: `20-verify-hashes.txt`.

## Canonical K inventory and independent classification

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/21_reconstruct_inventory.py
```

Result: `21-reconstruct-inventory.txt`.

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/37_classification_checks.py
```

Result: `37-classification-checks.txt`. The frozen source and relevant
operational-semantics excerpts are in `17-verification-source.txt`,
`18-spec-source.txt`, `19-program-source.txt`, and `22` through `25`.

## Trusted Stage 4 preflight

The first two invocations failed before project evaluation because the audit
sandbox blocks `/proc/self/exe`, which the installed Lean/Lake launchers use
for installation discovery:

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/27_run_preflight.py
```

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
  PYTHONPATH=/reference \
  python3 /audit-output/evidence/27_run_preflight.py
```

Results: `27-preflight-rerun.txt` and `29-preflight-rerun-pinned.txt`.

The compatibility shim was built with:

```sh
cc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/proc-self-exe-shim.so \
  /audit-output/evidence/30_proc_self_exe_shim.c -ldl
```

The shim only maps `/proc/*/exe` reads to the same process's kernel-provided
`AT_EXECFN`. Its final source/binary hashes and the pinned Lean version are in
`39-shim-final-and-lean-version.txt`.

The successful required invocation was:

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
  LD_PRELOAD=/tmp/audit-work/proc-self-exe-shim.so \
  PYTHONPATH=/reference \
  python3 /audit-output/evidence/27_run_preflight.py
```

Complete `lake clean`, `lake build`, exit codes, command output, and returned
preflight evidence: `31-preflight-rerun-success.txt`.

## Obligation bijection and target identity

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/36_verify_bijection_and_target.py
```

Result: `36-verify-bijection-and-target.txt`. The raw obligation map and target
source scan are `32-obligation-map.txt`, `33-generated-declarations-scan.txt`,
and `34-generated-target-files.txt`.
