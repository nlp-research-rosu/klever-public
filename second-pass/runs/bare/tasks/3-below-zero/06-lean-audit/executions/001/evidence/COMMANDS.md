# Audit commands

The mounted candidate and provenance files were treated only as data. No
candidate-provided script was executed.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py
PYTHONPATH=/reference python3 /audit-output/evidence/verify_hashes.py
PYTHONPATH=/reference python3 /audit-output/evidence/check_generation.py
PYTHONPATH=/reference python3 /audit-output/evidence/inspect_stage4.py
python3 /audit-output/evidence/semantic_witnesses.py
```

The first preflight run exposed a PID-namespace incompatibility in Lean 4.22's
`IO.appPath`: the sandbox provides `/proc/self` but not the namespace-relative
`/proc/<getpid()>` path that Lean constructs. The failed run is retained as
`preflight.transcript`. The compatibility retry used:

```sh
cc -shared -fPIC -O2 \
  -o /tmp/audit-work/host_pid_shim.so \
  /audit-output/evidence/host_pid_shim.c
LD_PRELOAD=/tmp/audit-work/host_pid_shim.so \
  PYTHONPATH=/reference \
  python3 /audit-output/evidence/check_generation.py
```

The shim changes only `getpid()` for the audited command tree, reporting the
host PID obtained from `/proc/self` so that Lean can locate its own executable.
It does not modify or bypass the preflight or generated project.

To test deterministic payload reproduction with the currently mounted trusted
exporter revision:

```sh
LD_PRELOAD=/tmp/audit-work/host_pid_shim.so \
  PYTHONPATH=/reference \
  python3 -m tools.klean_export \
  --input /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --output /tmp/audit-work/regeneration-audit/generation \
  --problem 3-below-zero \
  --generator-image-id \
    sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda \
  --toolchain-lock /reference/klean-toolchain.lock.json

diff -ru \
  /reference/klean-generation/generated \
  /tmp/audit-work/regeneration-audit/generation/generated
```

Each command was run through:

```sh
script -q -e -c '<command>' /audit-output/evidence/<name>.transcript
```

The `script` transcript records the exact command, complete combined terminal
output, and exit status.
