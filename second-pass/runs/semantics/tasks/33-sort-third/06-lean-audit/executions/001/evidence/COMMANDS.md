# Audit command index

The transcript and JSON files in this directory were produced by these
top-level commands. The Python entry points import only trusted code from
`/reference/tools`; generation-time producer sources are hashed as data and
are never imported or executed.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/structural_checks.py
```

Full output:
`structural-checks.log`; machine-readable result:
`structural-checks.json`.

```sh
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean_app_path_shim.so \
  /tmp/audit-work/lean_app_path_shim.c -ldl
LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so lake --version
```

Full output: `lean-shim-validation.log`. The shim only maps Lean's failing
`/proc/<getpid>/exe` readlink to the equivalent `/proc/self/exe` path in this
PID-namespace environment.

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/run_preflight.py
```

This calls:

```python
tools.klean_preflight.check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_and_record,
)
```

Returned evidence: `preflight-result.json`; command transcript:
`preflight-command-rerun.log`; complete subprocess output:
`preflight-lake-clean.log` and `preflight-lake-build.log`. The initial
environmental failure before installing the narrowly scoped shim is retained
in `preflight-command.log`.

Additional raw source, hash, and target scans are in:

- `producer-provenance-hashes.log`
- `verification-source.log`
- `program-spec-proof-driver.log`
- `semantics-values.log`
- `semantics-execution.log`
- `generated-target-scan.log`
- `preflight-comparison.log`

The final trusted model-free gate was run as:

```sh
LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so \
PYTHONPATH=/reference \
python3 /reference/tools/klean_final_gate.py \
  --frozen-k /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --generation /reference/klean-generation \
  --toolchain-lock /reference/klean-toolchain.lock.json \
  --audit-input /audit-input.json \
  --output /audit-output/evidence/mechanical-final-gate.json
```

Result: `mechanical-final-gate.json`; transcript:
`mechanical-final-gate.log`.
