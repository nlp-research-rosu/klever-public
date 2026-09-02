# Audit command ledger

All paths below are the immutable mounted inputs or fresh workspaces under
`/tmp/audit-work`. The numbered `.log` files contain the complete captured
stdout/stderr and exit status unless otherwise noted.

## Provenance and inventory

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json
```

The hashes and the relevant fields from `generator-manifest.json`,
`source-manifest.json`, and `/audit-input.json` are in
`01-producer-provenance.log`.

```sh
PYTHONPATH=/reference python -c \
  'from pathlib import Path; from tools.pipeline_contract import sha256_tree; print(sha256_tree(Path("/reference/generation-tools")))'
```

The result is in `02-producer-bundle-contract-hash.log`. The unrelated
`3535...` value visible in `01-producer-provenance.log` came from the export
tree-digest routine, not the launcher contract; the required
`pipeline_contract.sha256_tree` result is the matching `55e631...` value in
`02-producer-bundle-contract-hash.log`.

```sh
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'
```

The full reconstructed inventory is in
`03-reconstructed-rule-inventory.log`. Independent classification and the
bijection comparison with the protected manifest are in
`04-stage3-bijection-validation.log`.

## Deterministic Stage 4 checks

The trusted API was called with:

```sh
PYTHONPATH=/reference python -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation")), indent=2, sort_keys=True))'
```

The first run is `05-stage4-check-generation.log`. It exposed an audit
container PID-namespace incompatibility: Lean could not resolve its own
`/proc/<pid>/exe`. `06-lean-proc-namespace-diagnostic.log` records the
readlink diagnosis. The minimal compatibility source is
`lean-proc-readlink-compat.c`; it only maps an `ENOENT` read of
`/proc/<pid>/exe` to `/proc/self/exe`. It was built and the same trusted call
was rerun as:

```sh
cc -shared -fPIC -O2 -o /tmp/audit-work/lean-proc-readlink-compat.so \
  /audit-output/evidence/lean-proc-readlink-compat.c -ldl
PYTHONPATH=/reference \
LD_PRELOAD=/tmp/audit-work/lean-proc-readlink-compat.so \
python -c \
  'import json; from pathlib import Path; from tools.klean_preflight import check_generation; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation")), indent=2, sort_keys=True))'
```

The successful result is `07-stage4-check-generation-rerun.log`.

```sh
PYTHONPATH=/reference python /audit-output/evidence/verify_hashes_bijections.py
```

`09-hashes-bijections-target-corrected.log` is the authoritative result.
`08-hashes-bijections-target.log` was an earlier audit-helper attempt that
compared a pre-augmentation discovery record with a post-augmentation
generation record; it is superseded by the corrected script, which uses the
generator's trusted `_domain_source_rules` transformation.

## Fresh proof build and trust checks

The authoritative fresh project is `/tmp/audit-work/proof-audit-002`:

```sh
mkdir -p /tmp/audit-work/proof-audit-002/Base
cp -a /candidate/. /tmp/audit-work/proof-audit-002/
cp -a /reference/klean-generation/generated/. \
  /tmp/audit-work/proof-audit-002/Base/
LD_PRELOAD=/tmp/audit-work/lean-proc-readlink-compat.so lake clean
LD_PRELOAD=/tmp/audit-work/lean-proc-readlink-compat.so lake build
```

The copy, clean, and build results are `11-fresh-proof-copy-corrected.log`,
`13-stage5-lake-clean.log`, and `14-stage5-lake-build.log`. The earlier
`10-fresh-proof-copy.log` used an incorrect nested copy destination and is
superseded.

The lexical trust/shadow scan is in
`12-candidate-forbidden-shadow-scan.log`. The exact target comparison after
the build was:

```sh
PYTHONPATH=/reference python /audit-output/evidence/verify_hashes_bijections.py
```

with the fresh `Base` tree additionally compared to the selected generated
tree; the result is `23-postbuild-target-identity.log`.

Lean was run on a small import file containing:

```lean
import Proof
#check Proof.final
#print axioms Proof.final
```

The exact axiom line is `19-print-axioms-proof-final-exact.log`, the exact
type is `24-proof-final-identity.log`, and reconciliation was:

```sh
python /audit-output/evidence/reconcile_axioms.py
```

with result `25-axiom-reconciliation.log`. Logs `15` through `18` preserve
unsuccessful collection attempts affected by the same PID/PTY issue and are
superseded by `19`.

```sh
python /audit-output/evidence/locate_parameter_definitions.py
```

The exact definition, KORE binding, source-rule IDs, and source
classifications for all twelve target parameters are in
`27-parameter-definition-locations.log`.

## Adversarial bridge checks

Concrete sequence and map examples were checked by importing the candidate
definitions in Lean. The corrected results are in
`29-operational-bridge-examples-corrected.log`; `28` is an earlier
name-qualification error.

A separate Lean file proved that generated `SortScope` is empty and that the
two Scope-quantified target obligations hold for arbitrary operations:

```lean
#print axioms generatedSortScopeIsEmpty
#print axioms generatedMapUpdateObligationIsVacuous
#print axioms generatedMapDeleteObligationIsVacuous
```

The complete result is `22-generated-scope-vacuity-lean.log`.

A fresh counterfactual project replaced `_Map_`, `_|->_`,
`Map:update`, and `_[_<-undef]` with constant empty-map definitions, then ran:

```sh
LD_PRELOAD=/tmp/audit-work/lean-proc-readlink-compat.so lake clean
LD_PRELOAD=/tmp/audit-work/lean-proc-readlink-compat.so lake build
```

The mutation and successful build are
`20-vacuity-counterfactual-diff.log` and
`21-vacuity-counterfactual-build.log`.

Finally, another fresh project changed only:

```lean
inductive SortScope : Type where
  | auditWitness : SortScope
```

and ran the same clean build. `30-nonempty-scope-counterfactual-build.log`
records the expected failure at both candidate `nomatch` proofs.
