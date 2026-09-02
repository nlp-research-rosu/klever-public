# Audit command index

The transcript files in this directory contain raw stdout/stderr and final
exit status. The two Python files and the C shim are preserved verbatim.

## Input and producer inspection

Result: `producer-provenance.log` (exit 0)

```sh
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
sha256sum /reference/generation-tools/source-manifest.json /reference/klean-generation/generator-manifest.json /reference/klean-generation/input-manifest.json /audit-input.json
sed -n '1,260p' /reference/generation-tools/source-manifest.json
sed -n '1,320p' /reference/klean-generation/generator-manifest.json
sed -n '1,320p' /reference/klean-generation/input-manifest.json
```

Result: `recorded-hash-verification-success.log` (exit 0)

```sh
PYTHONPATH=/reference python3 -c 'from pathlib import Path; from tools.pipeline_contract import sha256_tree; from tools.klean_export import tree_digest; roots=["/reference/k-proof","/reference/k-audit","/reference/klean-generation","/reference/generation-tools"]; [print("sha256_tree",p,sha256_tree(Path(p))) for p in roots]; print("tree_digest /reference/k-proof",tree_digest(Path("/reference/k-proof"))); print("tree_digest /reference/klean-generation/generated",tree_digest(Path("/reference/klean-generation/generated")))'
find /reference/k-proof -type f -print0 | sort -z | xargs -0 sha256sum
```

An earlier malformed Python one-liner is retained in
`recorded-hash-verification.log`; it exited nonzero with a syntax error before
the successful command above.

Result: `audit-input-verification.log` (exit 0)

```sh
PYTHONPATH=/reference python3 -c 'import json, os; from pathlib import Path; from tools.stage6_resolution_contract import verify_audit_input; r,d=verify_audit_input(json.loads(Path("/audit-input.json").read_text())); print("resolved_input_sha256",d); print("resolution.mode",r["mode"]); print("AUDIT_MODE",os.environ.get("AUDIT_MODE")); print("mode_match",r["mode"]==os.environ.get("AUDIT_MODE"))'
```

## Frozen source and canonical inventory

Results: `frozen-program-and-proof.log`, `frozen-semantics.log` (exit 0)

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/prompt.py
nl -ba /reference/k-proof/prove.sh
nl -ba /reference/k-proof/semantic.k
```

Results: `inventory-reconstruction.log`,
`inventory-reconstructed.json` (exit 0)

```sh
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

Result: `discovery-manifest.log` (exit 0)

```sh
sha256sum /reference/lemma-discovery.json /audit-output/evidence/inventory-reconstructed.json
sed -n '1,360p' /reference/lemma-discovery.json
```

## Stage 4 preflight

The first exact call reached the disposable `lake clean` and failed because
Lean's PID-based executable lookup is incompatible with the audit sandbox.
Result: `preflight-rerun.log` (exit 1).

```sh
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; r=check_generation(Path("/reference/k-proof"),Path("/reference/lemma-discovery.json"),Path("/reference/klean-generation"),toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(r,indent=2,sort_keys=True))'
```

Diagnostic result: `lean-toolchain-diagnostic.log`.

The compatibility shim was compiled and tested with:

```sh
gcc -shared -fPIC -O2 -Wall -Wextra -o /tmp/audit-work/libouterpid.so /audit-output/evidence/outerpid.c
LD_PRELOAD=/tmp/audit-work/libouterpid.so /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version
```

Result: `lean-pid-shim-build.log` (exit 0). The exact shim source is
`outerpid.c`.

The successful call uses `check_generation` directly. Its custom
`run_command` only sets the compatibility environment for the two Lake
subprocesses and records their complete output:

```sh
PYTHONPATH=/reference python3 /audit-output/evidence/run_preflight.py
```

Results: `preflight-rerun-success.log`, `preflight-rerun.json`, and
`preflight-build-full.log` (exit 0). The exact caller is
`run_preflight.py`.

## Independent structural checks

```sh
AUDIT_MODE=CLASSIFICATION_ONLY PYTHONPATH=/reference python3 /audit-output/evidence/independent_checks.py
```

Result: `independent-checks.log` (exit 0). The exact checks are preserved in
`independent_checks.py`.

## Independent live K corroboration

Tool versions are in `k-toolchain-versions.log`.

```sh
k_live_dir=$(mktemp -d /tmp/audit-work/k-live.XXXXXX)
cp /reference/k-proof/semantic.k /reference/k-proof/verification.k /reference/k-proof/spec.k /reference/k-proof/solution.mpy "$k_live_dir"
cd "$k_live_dir"
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled
for n in -3 0 5 12; do
  krun solution.mpy -cARG="$n" --definition verification-kompiled
done
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Result: `k-live-rebuild-and-proof.log` (exit 0). The four final values were
`""`, `"0"`, `"0 1 2 3 4 5"`, and
`"0 1 2 3 4 5 6 7 8 9 10 11 12"`; `kprove` returned `#Top`.
