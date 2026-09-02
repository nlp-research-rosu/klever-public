# Audit commands and result files

All commands were run from `/audit-output`. Candidate and provenance inputs
were read only. Helper scripts are retained beside their outputs.

## Recorded hashes and producer authentication

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/verify_recorded_hashes.py \
  > /audit-output/evidence/recorded-hash-verification.json
```

Exit 0. Result:
`recorded-hash-verification.json` (39 checks, zero mismatches, including all
765 launcher-recorded Stage 1 per-file hashes).

Direct producer file hashes used by that check:

```sh
sha256sum /reference/generation-tools/klean_export.py \
          /reference/generation-tools/klean.py
```

Result:

```text
0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0  /reference/generation-tools/klean_export.py
af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1  /reference/generation-tools/klean.py
```

## Canonical inventory reconstruction

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/reconstruct_inventory.py \
  > /audit-output/evidence/inventory-comparison.json
```

Exit 0. Results:
`reconstructed-inventory.json` and `inventory-comparison.json`.

## Independent classification and Stage 4 structure

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/verify_stage4_structure.py \
  > /audit-output/evidence/stage4-structure-verification.json
```

Exit 0. Result: `stage4-structure-verification.json` (20 checks, zero
mismatches). The human rule-by-rule judgment is
`classification-judgment.md`; exact frozen source excerpts are in
`source-semantic-cross-check.txt`.

## Required trusted preflight

The first unmodified invocation and its infrastructure error are preserved in
`preflight-first-attempt.txt`.

The compatibility shim was built and checked with:

```sh
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/libproc-self-readlink.so \
  /audit-output/evidence/proc-self-readlink.c -ldl
sha256sum /audit-output/evidence/proc-self-readlink.c \
          /tmp/audit-work/libproc-self-readlink.so
LD_PRELOAD=/tmp/audit-work/libproc-self-readlink.so lean --version
```

Result:

```text
3b5d191aa6e24fa136e6dd17313dd02d8dbcd9c63cb1a9f3ad15739e75288711  /audit-output/evidence/proc-self-readlink.c
cc5622d0821d04e586a996dabf0d2b3b4885b6182391ec8111b97f8f0a67b3b0  /tmp/audit-work/libproc-self-readlink.so
Lean (version 4.22.0, x86_64-unknown-linux-gnu, commit ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05, Release)
```

The required checker was then rerun, unchanged:

```sh
LD_PRELOAD=/tmp/audit-work/libproc-self-readlink.so \
PYTHONPATH=/reference \
python3 - <<'PY' > /audit-output/evidence/preflight-check-generation.json
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

Exit 0. Exact returned evidence is `preflight-check-generation.json`. It
records `lake clean` exit 0, `lake build` exit 0, status
`KLEAN_NO_OBLIGATIONS`, zero obligations, and target `null`.
