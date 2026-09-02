# Audit command record

All mounted evidence was treated as data.  Helper programs authored for the
audit are retained beside these logs.

## Audit mode

```sh
env | rg '^AUDIT_MODE='
python3 -c 'import json; d=json.load(open("/audit-input.json"))["resolution"]; print(d["mode"], d["problem_id"], d["condition"], d["semantics_mode"])'
```

The environment and audit input both report `CLASSIFICATION_AND_PROOF`;
the remaining fields are `44-change-base`, `semantics`, and
`SUPPLIED_SEMANTICS`.  Raw output is in `00-audit-mode.log`.

## Producer provenance and inventory

```sh
env PYTHONPATH=/reference /usr/bin/python3 /audit-output/evidence/check_provenance.py
```

Result: exit 0; full result in `01-producer-provenance.log`.

```sh
env PYTHONPATH=/reference /usr/bin/python3 /audit-output/evidence/reconstruct_inventory.py
```

Result: exit 0; full reconstructed inventory in
`02-inventory-reconstruction.log`.

The frozen verification and relevant supplied semantics were captured with
numbered source lines:

```sh
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/reference-semantics/semantics/core.k
nl -ba /reference/k-proof/reference-semantics/semantics/call.k
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k
```

Results: `03-verification-source.log`, `03-source-solution.log`,
`03-source-postcondition.log`, `03-operational-core.log`,
`03-operational-call.log`, and `03-operational-functions.log`.

## Mandated preflight and independent structural checks

```sh
env \
  PYTHONPATH=/reference \
  LD_PRELOAD=/tmp/audit-work/lean_app_path_shim.so \
  LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
  LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0/src/lean/lake \
  PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  /usr/bin/python3 /audit-output/evidence/run_preflight.py
```

`run_preflight.py` calls
`tools.klean_preflight.check_generation(Path("/reference/k-proof"),
Path("/reference/lemma-discovery.json"),
Path("/reference/klean-generation"), toolchain_lock=...)`.
Result: exit 0 and status `PASS`; complete returned evidence in
`04-preflight-rerun-success.log`.  The earlier `04-preflight-rerun*.log`
files retain failed environment-launch attempts before the pinned Lean
launcher workaround; none changed source or proof data.

```sh
env PYTHONPATH=/reference /usr/bin/python3 /audit-output/evidence/check_hashes_and_target.py
```

Result: exit 0, all checks true; full hashes, obligation map, bijection, and
target identity in `05-hashes-obligations-target.log`.

The sandbox exposes a PID-namespace mismatch to Lean's `/proc/<getpid()>/exe`
lookup.  The narrow launcher shim used only for tool discovery was built with:

```sh
/usr/bin/cc -shared -fPIC -O2 \
  -o /tmp/audit-work/lean_app_path_shim.so \
  /audit-output/evidence/lean_app_path_shim.c -ldl
```

Result: exit 0 in `00-lean-shim-build.log`.  It changes no generated or
candidate source.

## Fresh proof workspace and Lean checks

The candidate source/configuration and generated project were copied to the
fresh directory `/tmp/audit-work/proof-audit.QWcnih`, with the generated
project named `Base`.  From that workspace, using the same pinned environment:

```sh
lake clean
lake build
```

Both exited 0.  Complete results are `06-lake-clean.log` and
`07-lake-build.log`.

```sh
lake env lean AxiomAudit.lean
lake env lean ProofPrint.lean
lake env lean DefinitionsPrint.lean
lake env lean Adversarial.lean
```

All exited 0.  Results are respectively `08-print-axioms.log`,
`10-print-proof-final.log`, `11-print-parameter-definitions.log`, and
`09-adversarial-vacuity-and-bridge.log`.  The exact input files are preserved
as `AxiomAudit.lean`, `ProofPrint.lean`, `DefinitionsPrint.lean`, and
`Adversarial.lean`.

```sh
env PYTHONPATH=/reference /usr/bin/python3 /audit-output/evidence/check_fresh_copy.py
```

Result: exit 0, all checks true; `13-fresh-copy-integrity.log` shows that the
fresh `Base` tree remained the exact generated tree
`abc17ba024518dea8fc6aa8e9394a007440a5d2481d7ff0cb5a91c70af6b2d7f`
and that the fresh proof was byte-identical to the candidate.

Numbered generated and candidate sources are in
`12-generated-sorts.log`, `12-generated-target.log`, and
`12-candidate-proof-source.log`.
