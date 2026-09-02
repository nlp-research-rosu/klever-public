# Evidence index and principal commands

All input paths were read-only. Audit-authored scripts and logs are contained
in this directory. The commands below were run from `/audit-output`.

## Launcher and mounted inputs

```sh
printenv AUDIT_MODE
sha256sum /audit-input.json /audit-output/audit-input.json
sed -n '1,260p' /audit-input.json
find /reference -maxdepth 3 -printf '%y %s %p\n' | sort
find /candidate -maxdepth 3 -printf '%y %s %p\n'
```

Results: `02_audit_mode_env.txt` through `07_candidate_presence.txt`.

The trusted checker and toolchain locks were also verified:

```sh
sha256sum /opt/humaneval/data/klean-audit-tools.lock.json
python3 - <<'PY'
# For every lock["files"] entry, SHA-256 /reference/<entry>
# and require exact equality with the lock.
PY
LD_PRELOAD=/tmp/audit-work/libproc_exe_compat.so \
  /usr/local/bin/assert-frozen-toolchain agent
sha256sum \
  /opt/humaneval/data/klean-toolchain.lock.json \
  /reference/klean-toolchain.lock.json
```

Results: `112_mechanical_checker_lock_hash.txt` through
`114_mechanical_checker_bundle_verification.txt`,
`105_frozen_toolchain_checker_run_with_compat.txt`, and
`108_toolchain_lock_hashes.txt`.

## Producer provenance

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/lemma-discovery.json
PYTHONPATH=/reference \
  python3 /audit-output/evidence/recompute_integrity.py
```

Results: `08_critical_file_hashes.txt`, `09_generation_source_manifest.txt`,
`10_generator_manifest.txt`, and `34_recompute_integrity.log`.

## Inventory reconstruction and independent classification

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/semantic.k
nl -ba /reference/k-proof/spec.k
PYTHONPATH=/reference \
  python3 /audit-output/evidence/independent_stage3_stage4.py
```

Results: `15_verification_k_numbered.txt` through
`19_solution_mpy_numbered.txt`, `95_summary_symbol_usage.txt` through
`97_operational_correspondence_index.txt`, and
`98_independent_stage3_stage4_full.log`.

The audit script calls the trusted
`tools.k_rule_inventory.inventory_verification`, independently recomputes the
four source spans and normalized hashes, recomputes the canonical inventory
hash, checks ordered identity equality, and checks every Stage 3/Stage 4
mapping and status.

## Stage 4 preflight

The first unchanged preflight attempt was:

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_stage4_preflight.py
```

It reached the fresh Lake build and failed because Lean 4.22 attempted to
resolve `/proc/<namespace-pid>/exe`, while this container exposes that process
only through `/proc/self/exe`. The failure is preserved in
`38_stage4_preflight_rerun.log`.

The compatibility source in `proc_exe_compat.c` redirects only `readlink`
calls of the form `/proc/*/exe` to `/proc/self/exe`. It does not read or change
candidate, K, manifest, or generated-project data.

```sh
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/libproc_exe_compat.so \
  /audit-output/evidence/proc_exe_compat.c -ldl
LD_PRELOAD=/tmp/audit-work/libproc_exe_compat.so lean --version
LD_PRELOAD=/tmp/audit-work/libproc_exe_compat.so \
  PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_stage4_preflight.py
```

Results: `79_proc_exe_compat_build.log`,
`80_proc_exe_compat_smoke_test.log`, and
`81_stage4_preflight_rerun_with_compat.log`. The final command ran the
unmodified trusted `tools.klean_preflight.check_generation`; it returned exit
0 and `KLEAN_NO_OBLIGATIONS`, with successful `lake clean` and `lake build`.

## Stage 4 sources, mappings, and sidecars

```sh
sed -n '1,1200p' \
  /reference/klean-generation/export-result.json \
  /reference/klean-generation/preflight.json \
  /reference/klean-generation/trust-inventory.json \
  /reference/klean-generation/generated/obligation-map.json \
  /reference/klean-toolchain.lock.json
find /reference/klean-generation/generated -type f -name '*.lean' \
  -print0 | sort -z | xargs -0 -r -n1 sh -c \
  'printf "\nFILE %s\n" "$1"; nl -ba "$1"' sh
```

Results: `35_stage4_sidecars_and_lock.txt`,
`36_generated_lean_sources.txt`, `37_stage4_sidecar_hashes.txt`, and
`89_target_name_and_declaration_search.txt` through
`93_preflight_target_parser.txt`.

## Stage 5

No Stage 5 command was run. `AUDIT_MODE` and the launcher record both say
`CLASSIFICATION_ONLY`; the Lean invocation/workspace hashes and Stage 5 result
are null, and `/candidate` is absent.
