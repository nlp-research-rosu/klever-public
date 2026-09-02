# Audit command ledger

This ledger lists the read-only verification and clean-build commands whose full
captured outputs are stored alongside it. Mounted candidate and provenance files
were inspected as untrusted evidence; no candidate-provided script was executed.

All transcript-producing commands used `script -q -e -c '<command>' <log>` so
that exit status and complete stdout/stderr were retained. The principal command
bodies were:

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json

PYTHONPATH=/reference python3 -c 'import json; from pathlib import Path; from tools.k_rule_inventory import inventory_verification; print(json.dumps(inventory_verification(Path("/reference/k-proof")), indent=2, sort_keys=True))'

PYTHONPATH=/reference LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so \
  python3 -c 'from pathlib import Path; from tools.klean_preflight import check_generation; import json; print(json.dumps(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")), indent=2, sort_keys=True))'

LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so lake clean
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so lake build
LD_PRELOAD=/tmp/audit-work/lean-proc-self-shim.so \
  lake env lean AuditAxioms.lean

kompile /tmp/audit-work/tmod-check.k \
  --directory /tmp/audit-work/tmod-check-evidence-kompiled
krun /tmp/audit-work/k-tmod-neg3-2.kore \
  --definition /tmp/audit-work/tmod-check-evidence-kompiled
```

The per-result mapping is:

| Evidence file | Command/result |
|---|---|
| `00-launcher-input.log` | Mode, audit-input hashes, and raw launcher JSON |
| `01-producer-provenance.log` | Producer file hashes and manifest cross-check material |
| `01b-producer-bundle-pipeline-hash.log` | Trusted pipeline tree hash of the producer bundle |
| `02-reconstructed-inventory.json.log` | Trusted inventory reconstruction, including all rule texts/spans/hashes/IDs |
| `03-inventory-manifest-bijection.log` | Ordered uniqueness, completeness, and classification counts |
| `04-preflight-rerun.log` | First preflight attempt; sandbox `/proc/<pid>/exe` launcher failure, exit nonzero |
| `05-preflight-rerun-with-proc-shim.log` | Required preflight rerun with the narrow `/proc/self/exe` compatibility shim; `PASS` |
| `06-stage4-integrity.log` | Independent tree/file/sidecar/obligation/binding/target hash checks |
| `07-stage5-lake-clean.log` | Fresh candidate-project `lake clean`, exit 0 |
| `08-stage5-lake-build.log` | Fresh candidate-project `lake build`, exit 0 |
| `09-proof-final-axioms.log` | `lake env lean AuditAxioms.lean` with exact `#print axioms Proof.final` output |
| `10-trusted-final-mechanical-gate.log` | Trusted final mechanical gate, `PASS` |
| `11-lean-bridge-adversarial-examples.log` | Initial diagnostic used the wrong Lean runner mode and exited nonzero; superseded |
| `11b-lean-bridge-adversarial-examples.log` | Correct adversarial Lean evaluations, exit 0 |
| `12-k-tmod-harness-build.log` | Independent minimal K integer harness build, exit 0 |
| `13a-k-tmod-negative-dividend.log` | K evaluation of `-3 %Int 2`, result `-1` |
| `13b-k-tmod-negative-divisor.log` | K evaluation of `3 %Int -2`, result `1` |
| `13c-k-tdiv-negative-dividend.log` | K evaluation of `-3 /Int 2`, result `-1` |
| `14-operational-bridge-source-comparison.log` | Frozen K hooks, supplied Python arithmetic semantics, and exact candidate definitions |
| `15b-counterfactual-bridge-source.log` | Counterfactual `%Int` implementation with arbitrary negative-divisor result |
| `15-counterfactual-bridge-build.log` | Unchanged fixed-target proof clean-builds with that counterfactual, exit 0 |
| `16-candidate-structure.log` | Independent target-shadow, exact-final, definition-count, and forbidden-token scan |
| `17-axiom-reconciliation.log` | Used/core/generated/unrecorded axiom set reconciliation |
| `18-counterfactual-negative-dividend-build.log` | Extra exploratory mutation; the unchanged tactic script failed to normalize its branch, so this result is not used as evidence of theorem falsity or validity |

The fresh successful proof workspace was
`/tmp/audit-work/proof-audit.fWiTlY`. Its `Base` was populated from
`/reference/klean-generation/generated` before the logged clean build. The
counterfactual was performed only in the separate
`/tmp/audit-work/proof-counterfactual.6so7vB` copy.
