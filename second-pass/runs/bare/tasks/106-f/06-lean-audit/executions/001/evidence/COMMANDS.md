# Audit command index

All commands were run from `/audit-output`. The Python source adjacent to each
`.out` file is the complete command body; each `.out` file records the returned
result.

## Rule inventory and independent classification

```text
PYTHONPATH=/reference python3 /audit-output/evidence/reconstruct_inventory.py
```

Exit: `0`. Result: `reconstruct_inventory.out`.

## Producer and frozen-input authentication

```text
PYTHONPATH=/reference python3 /audit-output/evidence/authenticate_inputs.py
```

Exit: `0`. Result: `authenticate_inputs.out`.

Direct producer hashes were also checked with:

```text
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
```

Output:

```text
235473b1324d2b203cb2a49ab94e36fb7c300084d506a57fca2228381f1bdec0  /reference/generation-tools/klean_export.py
ddec66db87398459ff0c2b5aad7121fe1029b58b8d576db4203c68bf5b647d13  /reference/generation-tools/klean.py
```

## Required trusted preflight

The initial unadapted run and exact error, PID-namespace diagnosis, shim build,
shim hashes, and pinned Lean/Lake version outputs are in
`preflight-environment.txt`.

The narrow shim was compiled with:

```text
cc -shared -fPIC -O2 -Wall -Wextra -Werror -o /tmp/audit-work/lean-proc-self-shim.so /audit-output/evidence/lean-proc-self-shim.c -ldl
```

The successful rerun was:

```text
PYTHONPATH=/reference python3 /audit-output/evidence/run_preflight.py
```

Exit: `0`. Complete returned evidence: `run_preflight.out`.

## Independent Stage 4 manifest, bijection, and target check

```text
PYTHONPATH=/reference python3 /audit-output/evidence/verify_generation.py
```

Exit: `0`. Result: `verify_generation.out`.

## Fixed generated target and Stage 5 absence

The exact commands and outputs are in `target-scan.out`.
