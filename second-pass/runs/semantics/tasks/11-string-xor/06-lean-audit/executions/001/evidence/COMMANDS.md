# Core audit commands

The helper sources named below are stored in this evidence directory. The
corresponding `.log` files contain complete combined standard output/error and
exit status.

## Environment and provenance

```sh
printenv AUDIT_MODE
python --version
kompile --version
kprove --version
lake --version
sha256sum /audit-input.json

PYTHONPATH=/reference python evidence/check_producer_provenance.py
PYTHONPATH=/reference python evidence/check_all_hashes.py
```

Results: `00_environment.log`, `01_producer_provenance.log`,
`02_all_input_hashes.log`.

## Canonical inventory reconstruction

```sh
PYTHONPATH=/reference python evidence/reconstruct_inventory.py
```

Result: `03_inventory_reconstruction.log`.

## Trusted preflight

The first direct attempt was:

```sh
PYTHONPATH=/reference python evidence/rerun_preflight.py
```

It stopped at `lake clean` because this audit container's PID namespace is not
represented in its mounted `/proc`. Lean's `lean_io_app_path` uses
`/proc/<getpid()>/exe`, so the Lake/Lean install could not be located.
`05_preflight_rerun.log` preserves the failure.

The narrow compatibility shim in `proc_exe_compat.c` changes only those
`readlink("/proc/<pid>/exe")` calls to `readlink("/proc/self/exe")`. It was
compiled and the same preflight was rerun with the pinned direct toolchain:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc_exe_compat.so \
  evidence/proc_exe_compat.c -ldl

env \
  LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
  PYTHONPATH=/reference \
  python evidence/rerun_preflight.py
```

Result: `06_preflight_rerun_compat.log`. The returned document is also
preserved verbatim as `preflight-returned.json`.

## Deterministic Stage 4 replay

The two producer sources were copied byte-for-byte to a scratch `tools`
directory together with the trusted inventory/contract dependencies. Their
hashes were checked before this command:

```sh
env \
  LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
  PYTHONPATH=/tmp/audit-work/generation-replay \
  python /tmp/audit-work/generation-replay/tools/klean_export.py \
    --input /reference/k-proof \
    --discovery-manifest /reference/lemma-discovery.json \
    --output /tmp/audit-work/generation-replay/replayed \
    --problem 11-string-xor \
    --generator-image-id \
      sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000 \
    --toolchain-lock /reference/klean-toolchain.lock.json
```

Then:

```sh
PYTHONPATH=/reference python - <<'PY'
from pathlib import Path
from tools.klean_export import tree_digest
for path in (
    Path("/reference/klean-generation/generated"),
    Path("/tmp/audit-work/generation-replay/replayed/generated"),
):
    print(path, tree_digest(path))
PY

diff -r --no-dereference \
  /reference/klean-generation/generated \
  /tmp/audit-work/generation-replay/replayed/generated
```

The generator manifest, trust inventory, and export result were also compared
with `sha256sum` and `diff -u`. Results:
`07_stage4_generation_replay.log`, `08_stage4_replay_comparison.log`,
`11_replay_input_manifest_path_diff.log`.

## Operational semantic witnesses and mutation

```sh
bash evidence/run_semantic_witnesses.sh
```

That script runs:

```sh
kompile /reference/k-proof/reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/semantic-runtime-kompiled

krun /audit-output/evidence/semantic_witnesses.mpy \
  --definition /tmp/audit-work/semantic-runtime-kompiled

krun /audit-output/evidence/semantic_counterfactual.mpy \
  --definition /tmp/audit-work/semantic-runtime-kompiled
```

Result: `09_operational_semantics_witnesses.log`.

## Independent obligation/target audit

```sh
PYTHONPATH=/reference python evidence/audit_stage4_structure.py
```

Result: `10_stage4_structure.log`.
