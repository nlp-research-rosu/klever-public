# Audit commands

All commands were run from `/audit-output` unless another working directory is
stated. Mounted inputs under `/reference` were treated as read-only.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/01_inventory_command.py \
  | tee /audit-output/evidence/01_inventory_result.json

PYTHONPATH=/reference python3 /audit-output/evidence/02_hashes_command.py \
  | tee /audit-output/evidence/02_hashes_result.json

python3 /audit-output/evidence/05_semantic_crosscheck_command.py \
  | tee /audit-output/evidence/05_semantic_crosscheck_result.json
```

The first required preflight attempt exposed the runner's PID/proc namespace
mismatch:

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/03_preflight_command.py
# Exit 1; exact output:
# /audit-output/evidence/03c_preflight_failed_attempt.txt
```

Lean 4.22 calls `readlink("/proc/<getpid()>/exe")`; this runner's `getpid()`
and mounted `/proc` use different PID namespaces. The compatibility shim was
built and tested only under writable audit paths:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/libpid_namespace_shim.so \
  /audit-output/evidence/pid_namespace_shim.c

LD_PRELOAD=/tmp/audit-work/libpid_namespace_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/libpid_namespace_shim.so lake --version
# Exact output:
# /audit-output/evidence/03b_pid_namespace_shim_build_and_test.txt
```

The unchanged trusted preflight was then rerun successfully:

```sh
LD_PRELOAD=/tmp/audit-work/libpid_namespace_shim.so \
PYTHONPATH=/reference \
python3 /audit-output/evidence/03_preflight_command.py \
  | tee /audit-output/evidence/03_preflight_result.json
```

The remaining structural, mode, and hash checks were:

```sh
PYTHONPATH=/reference \
python3 /audit-output/evidence/04_stage4_structure_command.py \
  | tee /audit-output/evidence/04_stage4_structure_result.json

printf 'AUDIT_MODE=%s\n' "$AUDIT_MODE"
python3 -c \
  'import json; print(json.load(open("/audit-input.json"))["resolution"]["mode"])'
stat -c '%F %n' /candidate
# Exact output:
# /audit-output/evidence/06_mode_and_candidate_presence.txt

PYTHONPATH=/reference \
python3 /audit-output/evidence/07_recorded_bindings_command.py \
  | tee /audit-output/evidence/07_recorded_bindings_result.json
```

Relevant frozen source and generated excerpts, including the negative
`targetStatement` scan, are in
`/audit-output/evidence/08_source_and_generated_excerpts.txt`.
