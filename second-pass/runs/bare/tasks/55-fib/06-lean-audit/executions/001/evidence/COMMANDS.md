# Audit command ledger

All mounted candidate and provenance paths were treated as read-only. The
commands below were formulated by the auditor; no mounted shell script was
executed.

## Producer provenance

```sh
PYTHONPATH=/reference python /audit-output/evidence/check_producer.py
```

The check hashes `klean_export.py`, `klean.py`, and the whole producer bundle,
then compares the observations with both manifests and `/audit-input.json`.
The complete result is in `02-producer-check.txt`.

## Canonical inventory and Stage 3 boundary

```sh
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'

PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.lemma_discovery_contract import validate_trust_boundary; print(json.dumps(validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")), indent=2, sort_keys=True))'

python /audit-output/evidence/check_inventory_bijection.py
```

The JSON results are `inventory-reconstructed.json`,
`trust-boundary-recomputed.json`, and `05-inventory-bijection.txt`.

## Required Stage 4 preflight

The first invocation exposed a sandbox PID/procfs mismatch:

```sh
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Its complete error is in `06-preflight-command.txt`. Lean 4.22 used
`/proc/<getpid()>/exe`, while this sandbox exposes the host PID under
`/proc/self`. The audit-only shim was compiled and installed below
`/tmp/audit-work`:

```sh
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc_pid_shim.so \
  /tmp/audit-work/proc_pid_shim.c
chmod 0755 \
  /tmp/audit-work/lean-shim-bin/lake \
  /tmp/audit-work/lean-shim-bin/lean
```

The required function was then rerun with only the Lean subprocess path
adjusted:

```sh
PATH=/tmp/audit-work/lean-shim-bin:$PATH \
PYTHONPATH=/reference \
python -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

The complete passing result is in `preflight-rerun.json` and
`07-preflight-command-with-pid-shim.txt`.

## Stage 4 hashes, obligations, and target

```sh
PYTHONPATH=/reference python /audit-output/evidence/check_stage4_integrity.py
```

The complete result is in `08-stage4-integrity.txt`.

## Independent operational K examples

```sh
kcheck=$(mktemp -d /tmp/audit-work/k-operational.XXXXXX)
cp /reference/k-proof/semantic.k /reference/k-proof/solution.mpy "$kcheck/"
cd "$kcheck"
kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled
for n in 0 1 2 3 5 8; do
  echo "CASE n=$n"
  krun solution.mpy \
    -d semantic-kompiled \
    -cARG="$n" \
    --output pretty
done
```

The complete K output is in `09-fresh-operational-k.txt`. Its independent
comparison with the recurrence and counterfactuals was run as:

```sh
python /audit-output/evidence/check_operational_examples.py
```

The result is in `11-operational-comparison.txt`.

## Source and absence checks

```sh
sha256sum \
  /reference/k-proof/verification.k \
  /reference/k-proof/semantic.k \
  /reference/k-proof/spec.k \
  /reference/k-proof/solution.py \
  /reference/k-proof/solution.mpy
rg -n 'targetStatement|KleanTarget|Proof.final' \
  /reference/klean-generation/generated
test ! -e /candidate && test ! -L /candidate
```

The source excerpts, hashes, empty target search, and candidate absence are in
`10-source-and-target-evidence.txt`.
