# Evidence index

All candidate and provenance content was treated as evidence only. Candidate
shell scripts were not executed.

- `00-environment.log`: audit mode and pinned K/Lean/Lake versions.
- `01-reconstructed-inventory.json`: trusted inventory reconstruction.
- `02-trust-boundary-validation.json`: trusted Stage 3 contract result.
- `03-inventory-bijection.json`: independent source-span, normalized-hash,
  identity, order, omission, duplicate, and inventory-hash checks.
- `04a-check-generation-initial-environment-failure.log`: first preflight
  attempt, showing the sandbox PID/`/proc` toolchain failure.
- `04b-check-generation.json`: successful rerun of the required trusted
  `check_generation` function after applying the local PID lookup shim.
- `05-stage5-workdir.txt`: fresh Stage 5 audit project location.
- `06a-stage5-wrong-cwd.log`: preserved operator error from the first build
  invocation.
- `06b-stage5-clean-build.log`: required `lake clean` and `lake build` from
  the fresh project.
- `07-klean-final-gate.json`: trusted final mechanical gate result.
- `08-print-axioms.log`: exact `#check` and `#print axioms Proof.final`
  output.
- `09a-k-hook-probe-import-error.log`: preserved initial probe import error.
- `09b-k-hook-probe-kompile.log`: first successful K hook-probe build.
- `09c-k-hook-probe-kompile-final.log`: final K hook-probe build.
- `10-k-hook-probe-results.log`: K string and map hook results, including
  UTF-8 byte behavior.
- `10b-k-int-map-probe-results.log`: K integer comparison and map-update
  results.
- `11a-lean-hook-probe-escape-error.log`: preserved initial Lean literal
  error.
- `11b-lean-hook-probe-results.log`: initial successful Lean string results.
- `11c-lean-all-bridge-probe-results.log`: preserved ambiguity error.
- `11d-lean-all-bridge-probe-results.log`: final Lean comparison, string,
  substring, and checked map-update examples.
- `12-counterfactual-target.log`: successful proof using deliberately
  dishonest parameter implementations.
- `13-hashes-and-target.json`: launcher-bound hashes, source hashes, target
  identity, candidate token scan, sidecar hashes, and unmatched producer
  fingerprints.
- `14-numbered-source-excerpts.log`: numbered frozen and candidate source
  excerpts plus K builtin declarations.
- `15-axiom-reconciliation.json`: exact axiom reconciliation.
- `k-hook-probe.k`, `AxiomAudit.lean`, `BridgeProbe.lean`, and
  `Counterfactual.lean`: exact K and Lean probe sources.
- `proc-self-getpid.c`: source of the sandbox-only Lean `IO.appPath` repair.
- `check_inventory_bijection.py`, `verify_hashes_and_target.py`, and
  `reconcile_axioms.py`: independent check scripts used to create the JSON
  evidence.

The relevant commands were:

```text
PYTHONPATH=/reference python3 -c '... inventory_verification(Path("/reference/k-proof")) ...'
PYTHONPATH=/reference python3 -c '... validate_trust_boundary(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")) ...'
LD_PRELOAD=/tmp/audit-work/proc-self-getpid.so PYTHONPATH=/reference python3 -c '... check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")) ...'
LD_PRELOAD=/tmp/audit-work/proc-self-getpid.so PYTHONPATH=/reference python3 /reference/tools/klean_final_gate.py --frozen-k /reference/k-proof --discovery-manifest /reference/lemma-discovery.json --generation /reference/klean-generation --candidate /candidate --toolchain-lock /reference/klean-toolchain.lock.json --audit-input /audit-input.json
lake clean
lake build
lake env lean AxiomAudit.lean
kompile probe.k --backend haskell --main-module PROBE --syntax-module PROBE-SYNTAX --output-definition probe-kompiled
krun /dev/stdin --definition probe-kompiled
lake env lean BridgeProbe.lean
lake env lean Counterfactual.lean
```
