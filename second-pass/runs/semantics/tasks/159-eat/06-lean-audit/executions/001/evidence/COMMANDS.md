# Commands executed

All mounted inputs were treated as read-only evidence. Audit-authored scripts
are in this directory.

## Inventory, provenance, and manifest checks

```sh
PYTHONPATH=/reference python3 evidence/audit_checks.py
```

The command was captured with `script` in
`integrity-and-inventory.log`. It invokes only trusted modules under
`/reference/tools`, recomputes both pipeline and export tree digests, hashes all
Stage 1 source files and producer files, reconstructs the canonical rule
inventory, performs an ordered/unique classification comparison, and checks the
empty obligation/target mapping.

```sh
bash evidence/semantic_source_slices.sh
```

The source and semantics slices are captured in
`semantic-source-slices.log`.

## Mandated Stage 4 preflight

Initial invocation:

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

This reached the temporary `lake clean` step but failed because Lean 4.22 could
not resolve `/proc/<inner-pid>/exe` in the command sandbox. The raw failure is
in `stage4-preflight-initial-failure.log`.

Environment diagnosis and correction:

```sh
bash evidence/lean_environment_check.sh
```

The raw PID-namespace diagnosis, compile result, and before/after Lean and Lake
versions are in `lean-environment.log`.

Successful mandated invocation:

```sh
LD_PRELOAD=/tmp/audit-work/outer_pid_preload.so \
PYTHONPATH=/reference \
python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

The exact returned evidence is in `stage4-preflight.log`. It exited zero. A
second successful rerun in `stage4-preflight-reconciliation.log` produced the
same structural result but Lake emitted the independent `Lemmas` and `Rewrite`
build lines in the opposite parallel order, so only the diagnostic output hash
differed. The first successful rerun reproduced the recorded diagnostic hash
exactly.
