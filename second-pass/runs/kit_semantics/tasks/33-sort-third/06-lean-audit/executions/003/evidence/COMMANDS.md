# Audit commands

The mounted inputs were treated as read-only evidence. These are the material
commands whose output is preserved in this directory.

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json
```

Output: `01-producer-hashes.txt`.

```sh
PYTHONPATH=/reference python3 /audit-output/inventory_audit.py
```

Output: `02-inventory-reconstruction.txt`.

The first required preflight attempt exposed the audit sandbox's mismatched PID
namespace and `/proc` mount:

```sh
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")), indent=2, sort_keys=True))'
```

Output: `03-stage4-preflight.txt`.

Lean 4.22 uses `/proc/<pid>/exe` for `IO.appPath`. In this sandbox, inner PIDs
are absent from the exposed outer `/proc`, while `/proc/self/exe` is valid. The
narrow preload shim in `proc_self_readlink_shim.c` redirects only executable
link lookups. It was built as follows:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /audit-output/evidence/proc_self_readlink_shim.so \
  /audit-output/evidence/proc_self_readlink_shim.c -ldl
```

The required preflight was then rerun unchanged apart from that process-path
compatibility environment:

```sh
LD_PRELOAD=/audit-output/evidence/proc_self_readlink_shim.so \
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")), indent=2, sort_keys=True))'
```

Output: `04-stage4-preflight-success.txt`.

```sh
PYTHONPATH=/reference python3 /audit-output/stage4_integrity_audit.py
```

Output: `05-stage4-integrity.txt`.

The fresh proof project was created at
`/tmp/audit-work/stage5-audit.GWhMbC`:

```sh
stage5_audit_dir=$(mktemp -d /tmp/audit-work/stage5-audit.XXXXXX)
cp -a /candidate/. "$stage5_audit_dir/"
cp -a /reference/klean-generation/generated/. "$stage5_audit_dir/Base/"
```

Its Base tree hash was checked as
`84df5ee8f24c175c97ad6b512ce5032869165c33cf62417caabb8dd73412c666`.

```sh
LD_PRELOAD=/audit-output/evidence/proc_self_readlink_shim.so lake clean
LD_PRELOAD=/audit-output/evidence/proc_self_readlink_shim.so lake build
```

Working directory: `/tmp/audit-work/stage5-audit.GWhMbC`. Complete outputs:
`06-stage5-lake-clean.txt` and `07-stage5-lake-build.txt`.

```sh
LD_PRELOAD=/audit-output/evidence/proc_self_readlink_shim.so \
  lake env lean PrintAxioms.lean
```

`PrintAxioms.lean` contains `#print axioms Proof.final`. Output:
`08-print-axioms.txt`.

```sh
PYTHONPATH=/reference python3 /audit-output/stage5_integrity_audit.py
```

Output: `09-stage5-static-trust.txt`.

```sh
LD_PRELOAD=/audit-output/evidence/proc_self_readlink_shim.so \
  lake env lean BridgeAudit.lean
```

Working directory: `/tmp/audit-work/stage5-audit.GWhMbC`. The audited source is
copied as `BridgeAudit.lean`; output is `10-lean-bridge-adversarial.txt`.

```sh
python3 -c 'sort_third=lambda l: [sorted(l[::3])[i//3] if i%3==0 else l[i] for i in range(len(l))]; values=([True,None,None,False],[5,6,3,4,8,9,2],[5,6,3,7,8,9,2]); [print(repr(value), "=>", repr(sort_third(list(value)))) for value in values]'
```

Output: `11-python-operational-oracle.txt`.

```sh
timeout 60 krun /tmp/audit-work/bool-operational-test.mpy \
  --definition /reference/k-proof/runtime-kompiled
```

The audited input is copied as `bool-operational-test.mpy`; output and exit 113
are in `12-k-bool-operational.txt`.

The source excerpts used for the operational comparison were captured with
numbered `nl -ba`/`sed` reads into `13-operational-source-excerpts.txt`.
