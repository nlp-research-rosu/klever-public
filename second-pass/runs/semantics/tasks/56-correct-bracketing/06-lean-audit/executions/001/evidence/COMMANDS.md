# Audit command index

The `.txt` files in this directory are raw `script(1)` transcripts. The most
important exact commands were:

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
```

Output: `00_environment_and_files.txt`.

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2))'
```

Output: `02_reconstructed_rule_inventory.txt`.

```sh
PYTHONPATH=/reference python3 \
  /audit-output/evidence/recompute_integrity.py
```

Final output using the pipeline-record hash algorithm:
`04b_recomputed_integrity_pipeline_hashes.txt`.

```sh
PYTHONPATH=/reference python3 \
  /audit-output/evidence/check_inventory_bijection.py
```

Output: `10_inventory_bijection.txt`.

The first direct preflight command was:

```sh
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

Output: `06_fresh_check_generation.txt`. It reached the clean-build phase and
failed because the audit sandbox hides `/proc/<numeric-pid>/exe`.

The narrow sandbox compatibility shim was built and checked with:

```sh
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean_proc_exe_shim.so \
  /audit-output/evidence/lean_proc_exe_shim.c -ldl

LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
```

Output: `07b_lean_sandbox_workaround.txt`.

The successful mandated preflight rerun was the same
`tools.klean_preflight.check_generation` call shown above, with only this
process environment addition:

```sh
LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so \
PYTHONPATH=/reference \
python3 ...
```

Output: `06b_fresh_check_generation_with_sandbox_shim.txt`.

Relevant frozen semantics were printed with `nl -ba` and searched with `rg`;
the raw results are in `08_relevant_fixed_semantics_search.txt`,
`09_relevant_fixed_semantics_full.txt`, and
`12_core_semantics_and_trusted_tool_hashes.txt`.

The independent summary differential check and its complete output are in
`13_summary_differential_and_mutations.txt`; its executed source appears in
the transcript.

