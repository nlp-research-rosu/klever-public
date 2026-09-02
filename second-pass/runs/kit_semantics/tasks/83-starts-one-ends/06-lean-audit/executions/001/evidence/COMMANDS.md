# Audit command record

The corresponding complete terminal transcripts are the numbered `.txt` files
in this directory. The decisive commands were:

```sh
env | LC_ALL=C sort | sed -n '/^AUDIT_MODE=/p'

sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/lemma-discovery.json \
  /reference/k-proof/verification.k \
  /reference/klean-generation/generated/obligation-map.json

PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'

rg -n '^[[:space:]]*rule(?:[[:space:]]|$)|^[[:space:]]*module[[:space:]]|^[[:space:]]*imports[[:space:]]|^[[:space:]]*endmodule' \
  /reference/k-proof/verification.k

rg -n -C 3 'Call\(|Return\(|IfExp\(|Compare\(|BinOp\(|applyBin|applyCmp|pow|\*\*|\^Int' \
  /reference/k-proof/reference-semantics/semantics/call.k \
  /reference/k-proof/reference-semantics/semantics/controls.k \
  /reference/k-proof/reference-semantics/semantics/core.k \
  /reference/k-proof/reference-semantics/semantics/operators.k \
  /reference/k-proof/reference-semantics/semantics/int.k \
  /reference/k-proof/reference-semantics/semantics/functions.k

LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LEAN=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean \
LAKE=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake \
LD_PRELOAD=/audit-output/evidence/lean_proc_self_exe_interposer.so \
PYTHONPATH=/reference \
python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'

PYTHONPATH=/reference python3 /audit-output/evidence/audit_integrity.py

rg -n '\b(sorry|admit|unsafe|axiom|opaque|theorem|lemma)\b|KleanObligations|final' \
  /reference/klean-generation/generated --glob '*.lean'

test ! -e /candidate
```

The first unmodified preflight attempt is preserved in
`32-rerun-klean-preflight.txt`. It failed because the audit sandbox hides
`/proc/<pid>/exe`. The narrow executable-location interposer source, build,
probe, and hashes are preserved in `lean_proc_self_exe_interposer.c`,
`44-build-lean-interposer.txt`, `48-interposed-lean-version.txt`, and
`51-local-audit-helper-hashes.txt`. The successful unmodified trusted
`check_generation` result is `49-rerun-klean-preflight-success.txt`.
