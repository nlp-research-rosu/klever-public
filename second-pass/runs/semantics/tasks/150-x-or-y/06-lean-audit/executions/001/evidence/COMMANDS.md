# Audit commands

All input paths below were read-only. Generated definitions and temporary build
artifacts were created only below `/tmp/audit-work`; audit evidence was written
below `/audit-output/evidence`.

## Launcher, producer, target, and mount checks

```bash
{
  printf 'AUDIT_MODE=%s\n' "$AUDIT_MODE"
  sha256sum /reference/generation-tools/klean_export.py \
    /reference/generation-tools/klean.py \
    /reference/generation-tools/source-manifest.json \
    /reference/klean-generation/generator-manifest.json \
    /reference/lemma-discovery.json
  sed -n '1,120p' /reference/generation-tools/source-manifest.json
  sed -n '1,200p' /reference/klean-generation/generator-manifest.json
  sed -n '1,200p' \
    /reference/klean-generation/generated/obligation-map.json
  find /reference/klean-generation/generated -type f \
    -printf '%P\t%s bytes\n' | sort
  rg -n '^\s*(def|theorem|lemma|axiom|opaque)\s+.*(?:Target|target|Obligation|obligation)|KleanTarget|targetProp' \
    /reference/klean-generation/generated --glob '*.lean' || true
  if test -e /candidate; then
    printf '/candidate EXISTS\n'
  else
    printf '/candidate ABSENT\n'
  fi
}
```

Complete output: `producer-and-target-check.txt` (exit 0).

## Trusted inventory reconstruction and all recorded hash checks

```bash
PYTHONPATH=/reference \
  python3 /audit-output/evidence/reconstruct_and_hash.py
```

Complete output: `reconstruction.json` (exit 0). The script source records each
asserted bijection, source hash, tree hash, producer binding, target identity,
and Stage 5 absence check.

## Independent classification checks

```bash
python3 /audit-output/evidence/verify_classification.py
```

Complete output: `classification-checks.json` (exit 0). The script compares the
proved claim and reused rule, checks module imports and proof order, tests the
summary recurrences against an independent source-loop oracle, and checks
discriminating counterfactuals.

## Required Stage 4 preflight

The literal first invocation was:

```bash
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

It exited 1 before project checking because Lean's runtime could not locate
`/proc/<getpid()>/exe` in the audit sandbox. Complete output:
`preflight-attempt-1.txt`.

The sandbox exposes `/proc/self/exe` but its virtual numeric PID is absent from
the read-only `/proc` mount. The narrowly scoped compatibility shim was built
and checked with:

```bash
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc-self-readlink.so \
  /tmp/audit-work/proc-self-readlink.c -ldl
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so lean --version
(cd /reference/klean-generation/generated &&
  LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so lake clean)
```

The shim source is preserved as `proc-self-readlink.c`; it redirects only
numeric `/proc/.../exe` `readlink` calls to `/proc/self/exe`.

The required preflight was then rerun, with no checker or input changes:

```bash
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so \
PYTHONPATH=/reference python3 -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Complete returned evidence: `preflight-return.json` (exit 0).

## Fresh K proof of the claimed derived lemma and its later use

```bash
mkdir /tmp/audit-work/k-derived-check
cp -a /reference/k-proof/. /tmp/audit-work/k-derived-check/
cd /tmp/audit-work/k-derived-check

kompile verification.k --backend haskell \
  --main-module X-OR-Y-VERIFICATION \
  --syntax-module X-OR-Y-VERIFICATION \
  --output-definition verification-kompiled

kprove spec.k --definition verification-kompiled \
  --spec-module X-OR-Y-LOOP-SPEC --claims loop_correct

kompile verification.k --backend haskell \
  --main-module X-OR-Y-SUMMARY \
  --syntax-module X-OR-Y-SUMMARY \
  --output-definition summary-kompiled

kprove spec.k --definition summary-kompiled \
  --spec-module X-OR-Y-MAIN-SPEC --claims main_correct

kprove spec.k --definition summary-kompiled \
  --spec-module X-OR-Y-MAIN-SPEC --claims main_correct \
  --haskell-backend-command \
  'kore-exec --trace-rewrites /audit-output/evidence/main-rewrites.yml'
```

All five commands exited 0. Complete outputs are `derived-kompile.log`,
`derived-kprove.log`, `summary-kompile.log`, `summary-main-kprove.log`, and
`summary-main-traced-kprove.log`. Both `kprove` goals printed `#Top`.
`main-rewrites.yml` is the complete later-proof rewrite trace.

The compiled source binding and later trace application were extracted with:

```bash
rg -n -m 2 \
  'ad2530f085eb20cb8a7faed8a7f49f7c300a4203bb31a69174dc2642975de222' \
  /tmp/audit-work/k-derived-check/summary-kompiled/definition.kore
rg -n -C 2 \
  'ad2530f085eb20cb8a7faed8a7f49f7c300a4203bb31a69174dc2642975de222' \
  /audit-output/evidence/main-rewrites.yml
```

Complete output: `summary-rule-use.txt` (exit 0).

## Tool versions

```bash
kompile --version
kprove --version
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so lean --version
LD_PRELOAD=/tmp/audit-work/proc-self-readlink.so lake --version
```

Complete output: `tool-versions.txt` (exit 0).
