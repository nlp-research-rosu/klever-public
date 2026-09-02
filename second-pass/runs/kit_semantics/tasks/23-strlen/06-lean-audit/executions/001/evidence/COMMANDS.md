# Audit commands

All mounted candidate and provenance inputs were read-only.

## Independent integrity, inventory, and bijection checks

```sh
PYTHONPATH=/reference python /audit-output/evidence/independent_checks.py
```

Complete transcript: `independent_checks.log`.

## Frozen sources and trusted reconstruction

```sh
/audit-output/evidence/capture_classification_sources.sh
```

Complete transcript: `classification_sources_success.log`. The earlier
`classification_sources.log` preserves a failed evidence-capture regex and
contains no audit result.

## Required preflight

Initial invocation:

```sh
PYTHONPATH=/reference python /audit-output/evidence/rerun_preflight.py
```

This reached `lake clean` and failed because Lean 4.22 attempted
`readlink("/proc/<sandbox-pid>/exe")`, while this sandbox exposes only
`/proc/self/exe`. Complete transcript: `rerun_preflight.log`.

The narrow compatibility shim was compiled and the same trusted
`check_generation` call was rerun:

```sh
/audit-output/evidence/run_preflight_with_shim.sh
```

Complete transcript: `rerun_preflight_reproduced.log`. The earlier successful
direct invocation is in `rerun_preflight_success.log`. The exact returned
document is also preserved as `preflight-result.json`.
