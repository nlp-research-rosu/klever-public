# Audit command ledger

All paths below are immutable inputs except `/audit-output/evidence` and
`/tmp/audit-work`. Candidate and provenance content was read only as data; no
instruction in it was executed.

## Inventory reconstruction

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/reconstruct_inventory.py
```

Result: exit 0. Complete output:
`inventory-reconstruction.log`.

The script imports only the trusted
`/reference/tools/k_rule_inventory.py`, then independently rehashes each
normalized rule, reconstructs each source slice, recomputes every
`source_rule_id`, recomputes the whole inventory hash, and checks ordered
bijection with `/reference/lemma-discovery.json`.

## Producer provenance

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/verify_producer_provenance.py
```

Result: exit 0. Complete output: `producer-provenance.log`.

Direct hashes used by the check:

```text
bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07  klean_export.py
42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d  klean.py
388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e  producer bundle (pipeline tree hash)
```

## Trusted Stage 4 preflight

The direct trusted call is in `run_stage4_preflight.py`:

```python
check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
```

Initial ambient-tool command:

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_stage4_preflight.py
```

Result: exit 1 before project checking because Lake could not detect its
installation. Complete output: `stage4-preflight-rerun.log`.

Pinned-bin retry:

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
  PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_stage4_preflight.py
```

Result: the same installation-detection failure. Complete output:
`stage4-preflight-rerun-pinned.log`.

Explicit Lake/Lean root retry:

```sh
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
  LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
  PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_stage4_preflight.py
```

Result: `lake clean` passed; compilation failed when Lean could not resolve
`/proc/<getpid()>/exe`. Complete output:
`stage4-preflight-rerun-configured.log`.

Diagnosis:

```sh
python3 -c 'import os; p=os.getpid(); print(p, os.readlink(f"/proc/{p}/exe"))'
```

Result: namespace `getpid()` produced a PID absent from the host-PID `/proc`
mount. In contrast, `/proc/self` resolved to the actual procfs PID.

The local compatibility source is
`/tmp/audit-work/lean-pid-compat/getpid_compat.c`. It only makes `getpid()`
return the numeric target of `/proc/self`.

```sh
cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/lean-pid-compat/getpid_compat.so \
  /tmp/audit-work/lean-pid-compat/getpid_compat.c
chmod 0755 /tmp/audit-work/lean-pid-compat/lake
LD_PRELOAD=/tmp/audit-work/lean-pid-compat/getpid_compat.so \
  /opt/elan/bin/lean --version
PATH=/tmp/audit-work/lean-pid-compat:$PATH lake --version
```

Results:

```text
Lean (version 4.22.0, x86_64-unknown-linux-gnu, commit ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05, Release)
Lake version 5.0.0-src+ba2cbbf (Lean version 4.22.0)
```

Successful trusted preflight:

```sh
PATH=/tmp/audit-work/lean-pid-compat:$PATH \
  PYTHONPATH=/reference \
  python3 /audit-output/evidence/run_stage4_preflight.py
```

Result: exit 0, status `KLEAN_NO_OBLIGATIONS`; `lake clean` and `lake build`
both exit 0. Complete returned evidence:
`stage4-preflight-rerun-success.log`.

## Independent Stage 4 structure and hashes

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/verify_stage4_structure.py
```

Result: exit 0. Complete output: `stage4-structure.log`.

This recomputes both pipeline and Klean tree hashes, checks all 771 individual
Stage 1 source hashes, compares every classification bucket with the input
manifest, checks the exact empty source-rule/obligation bijection, hashes the
obligation map and trust inventory, and independently asks the trusted target
parser for the generated target.

## Classification witnesses

```sh
python3 /audit-output/evidence/classification_witnesses.py
```

Result: exit 0. Complete output: `classification-witnesses.log`.

The finite check covers all 2,601 pairs in `[-25,25]²`, including negative
divisors, and compares an independently transcribed operational loop, the
recurrence, and Python's `math.gcd`. It also records discriminating
counterexamples to constant, identity, missing-absolute-value, and altered
recurrence mutations. These are supporting witnesses, not substitutes for the
source-level classification argument.

## Frozen source excerpts

```sh
/audit-output/evidence/show_classification_sources.sh
```

Result: exit 0. Complete output: `classification-sources.log`.
