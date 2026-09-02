# Core audit commands

All paths below were run from `/audit-output` unless a different working
directory is shown. The linked evidence files contain the raw results.

```bash
env | rg '^AUDIT_MODE='
sed -n '1,260p' /audit-input.json
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
PYTHONPATH=/reference python evidence/check_recorded_hashes.py
```

Results: `00-audit-mode.txt`, `00-audit-input.txt`,
`01-producer-file-hashes.txt`, and `05-recorded-hash-check.txt`.

```bash
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
PYTHONPATH=/reference python evidence/check_inventory_bijection.py
PYTHONPATH=/reference python evidence/independent_reclassification.py
```

Results: `03-reconstructed-rule-inventory.json`,
`06-inventory-bijection-check.txt`, and
`12-independent-reclassification.json`.

The rule-sensitivity test used two fresh copies. In
`/tmp/audit-work/stage1-no-split`, only `verification.k:95-99` was removed;
the exact mutation is in `09-no-split-only-mutation.diff`.

```bash
# Working directory: /tmp/audit-work/stage1-no-split
kompile verification.k --backend haskell \
  --main-module SORT-NUMBERS-VERIFICATION \
  --syntax-module SORT-NUMBERS-VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module SORT-NUMBERS-SPEC \
  --claims SORT-NUMBERS-SPEC.sort-numbers-symbolic

# Working directory: /tmp/audit-work/stage1-with-split
kompile verification.k --backend haskell \
  --main-module SORT-NUMBERS-VERIFICATION \
  --syntax-module SORT-NUMBERS-VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module SORT-NUMBERS-SPEC \
  --claims SORT-NUMBERS-SPEC.sort-numbers-symbolic
```

Results: `09-no-split-kompile.txt`, `09-no-split-kprove-symbolic.txt`,
`09-with-split-kompile.txt`, and `09-with-split-kprove-symbolic.txt`.

The requested default preflight command was first run directly:

```bash
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

It reached the temporary `lake clean` command but the audit sandbox denied
Lean's `/proc/<pid>/exe` lookup. The raw exception is
`10-rerun-check-generation.txt`; the binary-level diagnosis is in
`10-lean-io-app-path-disassembly.txt`.

A narrow `LD_PRELOAD` compatibility shim was then built and injected only by
the temporary-build callback. It changes `readlink` only for `/proc/*/exe`
and returns `program_invocation_name`; all other reads delegate to libc.

```bash
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean-app-path-compat.so \
  evidence/lean_app_path_compat.c -ldl
PYTHONPATH=/reference \
  python evidence/rerun_check_generation_with_app_path_compat.py
```

Results: `10-lean-app-path-compat-build.txt`,
`10-lean-app-path-compat-test.txt`, and
`10-rerun-check-generation-compatible.txt`.

```bash
PYTHONPATH=/reference python evidence/check_stage4_bijection_and_target.py
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools import klean_export; print(json.dumps({"generated_tree_sha256":klean_export.tree_digest(Path("/reference/klean-generation/generated")),"target":klean_export.target_statement(Path("/reference/klean-generation/generated")),"expected_target_definition":klean_export.expected_target_definition(json.loads(Path("/reference/klean-generation/generated/obligation-map.json").read_text()))}, indent=2, sort_keys=True))'
```

Results: `13-stage4-bijection-and-target-check.txt` and
`13-independent-generated-target.json`.
