# Material audit commands

All paths below are absolute. Mounted candidate/provenance inputs were read
only. Locally authored audit scripts and the compatibility shim are preserved
beside their results.

## Producer hashes and manifests

```sh
sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py
python3 -m json.tool /audit-input.json
python3 -m json.tool /reference/generation-tools/source-manifest.json
python3 -m json.tool /reference/klean-generation/generator-manifest.json
```

Results:

- `producer-sha256.txt`
- `audit-input.pretty.json`
- `source-manifest.pretty.json`
- `generator-manifest.pretty.json`

## Canonical inventory reconstruction

```sh
PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
python3 -m json.tool /reference/lemma-discovery.json
```

Results:

- `reconstructed-rule-inventory.json`
- `lemma-discovery.pretty.json`

## Mandated generation preflight

Initial command and failure, the narrowly scoped compatibility diagnosis, and
the successful rerun command are recorded verbatim in
`preflight-infrastructure-note.txt`.

Successful command:

```sh
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
PYTHONPATH=/reference \
python3 -c 'import json; from pathlib import Path; from tools.klean_preflight import check_generation; result=check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")); print(json.dumps(result, indent=2, sort_keys=True))'
```

Exact returned evidence: `preflight-rerun.json`.

## Independent structural and hash checks

```sh
PYTHONPATH=/reference \
python3 /audit-output/evidence/independent_structural_check.py
```

Exact result: `independent-structural-check.json`.

## Adversarial summary checks

```sh
python3 /audit-output/evidence/summary_adversarial_check.py
```

Exact result: `summary-adversarial-check.json`.

## Target and Stage 5 absence

```sh
rg -n 'targetStatement' /reference/klean-generation/generated --glob '*.lean'
test -e /candidate
python3 -m json.tool /reference/klean-generation/generated/obligation-map.json
```

Exact exit codes and result: `target-and-stage5-check.txt`.

## Frozen source/semantics excerpts

The exact `nl`/`sed` commands and their outputs are in
`source-semantics-excerpts.txt`.
