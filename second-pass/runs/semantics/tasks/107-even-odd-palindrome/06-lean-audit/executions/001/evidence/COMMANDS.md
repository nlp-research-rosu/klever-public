# Audit command record

All commands ran from `/audit-output` unless an explicit `cd` appears.
Candidate/provenance shell scripts were not executed.

## Canonical inventory, producer authentication, and hash checks

```bash
PYTHONPATH=/reference \
  python3 /audit-output/evidence/audit_checks.py
```

Exit: `0`. Raw stdout: `audit_checks.stdout.txt`. Structured results:
`inventory-reconstruction.json`, `inventory-comparison.json`,
`producer-authentication.json`, `hash-verification.json`, and
`stage4-structural-checks.json`.

The direct producer command and result are recorded verbatim in
`producer-authentication-raw.txt`; the command hashes
`/reference/generation-tools/klean_export.py` and `klean.py`, then prints and
compares the generator manifest, source manifest, signed audit-input image
identity, and bundle tree hash.

## Independent semantic cross-check

```bash
python3 /audit-output/evidence/semantic_crosscheck.py
```

Exit: `0`. Raw stdout: `semantic_crosscheck.stdout.txt`. Structured result:
`semantic-crosscheck.json`.

## Trusted Stage 4 preflight

The first unmodified environment attempt was:

```bash
PYTHONPATH=/reference python3 -c '
from pathlib import Path
from tools.klean_preflight import check_generation
check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)'
```

Exit: `1` before project evaluation because the Elan proxy could not detect
the Lake installation. Result: `preflight-initial-environment-failure.log`.

Activating the pinned direct toolchain exposed the sandbox PID-namespace
problem: Lean tried the absent path `/proc/<namespace-pid>/exe`. The diagnostic
source is `trace_paths.c`; the narrowly scoped workaround source is
`lean_proc_shim.c`. It was built with:

```bash
cc -shared -fPIC -ldl \
  /audit-output/evidence/lean_proc_shim.c \
  -o /tmp/audit-work/lean_proc_shim.so
```

The successful exact function rerun was:

```bash
TOOLROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0
PATH="$TOOLROOT/bin:$PATH" \
LAKE_HOME="$TOOLROOT/src/lean/lake" \
LEAN_SYSROOT="$TOOLROOT" \
LAKE_OVERRIDE_LEAN=true \
LD_PRELOAD=/tmp/audit-work/lean_proc_shim.so \
PYTHONPATH=/reference \
python3 -c '
import json
from pathlib import Path
from tools.klean_preflight import check_generation
print(json.dumps(check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
), indent=2, sort_keys=True))'
```

Exit: `0`. Exact returned evidence: `preflight-rerun-success.json`. The
intermediate direct-toolchain attempt before the PID workaround is retained as
`preflight-pinned-env-before-pid-shim-failure.log`.

The shim changes only a failed `readlink("/proc/<getpid()>/exe", ...)` into
`readlink("/proc/self/exe", ...)`; it does not intercept file reads, Lean
source, compilation, or theorem checking. With the shim, `lean --version`
reported `4.22.0`, commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, matching the lock.

## Fresh Stage 1 K rerun

A fresh directory was allocated below `/tmp/audit-work` and populated by
copying the frozen workspace. Its exact path is in `k-rerun-workspace.txt`.
No provenance script was executed.

```bash
cd "$KWORK"
PATH="$HOME/.nix-profile/bin:$PATH" \
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-kompiled
```

Exit: `0`. Complete output: `k-kompile.log`.

```bash
cd "$KWORK"
PATH="$HOME/.nix-profile/bin:$PATH" \
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module SPEC
```

Exit: `0`; result `#Top`. Complete output: `kprove-rerun.log`.

For the independent non-vacuity check, `spec.k` was copied to
`spec-vacuity.k` and only the satisfiable `N = 1000` destination was changed
from `evenPalindromes(1000)` (which reduces to `48`) to `47`:

```bash
cd "$KWORK"
PATH="$HOME/.nix-profile/bin:$PATH" \
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC
```

Exit: `1` as required, with `WarnStuckClaimState`; the residual shows the
executed source returned `(48, 60)` rather than `(47, 60)`. Complete output:
`kprove-vacuity.log`; exact mutation: `spec-vacuity.k`.

## Source/target inspections

`frozen-source-and-semantics.txt` records the source hashes, numbered
`verification.k`, `spec.k`, `solution.py`, prompt contract, and the relevant
fixed MPY rules for loading, name lookup, calls, parameter binding, assignment,
branching, returns, integer operations, and tuple construction.

`stage4-obligation-target-inspection.txt` records sidecar hashes, the complete
empty obligation map, the complete generated `Lemmas.lean`, target-token
search, and trusted producer computations of both the observed target
statement and expected target definition.
