# Evidence index

All mounted candidate and provenance material was treated as untrusted data.
The executable audit code in `commands/` was authored for this audit and calls
only the trusted modules under `/reference/tools` (via `PYTHONPATH=/reference`)
or performs explicit read-only comparisons.

- `01-provenance-inventory-rerun.log`: successful producer provenance,
  launcher/tree/file hash, canonical inventory, order, span, normalized hash,
  and source-rule-ID reconstruction. The earlier
  `01-provenance-inventory.log` is a preserved superseded run whose audit
  script used the wrong export-result field name and exited with `KeyError`.
- `02-toolchain-environment.log`: exact PID-namespace diagnosis, compilation of
  the minimal `getpid` compatibility shim, and pinned Lean/Lake versions.
- `03-preflight.log`: preserved first preflight attempt, stopped when Lean could
  not resolve `/proc/<inner-pid>/exe`.
- `03-preflight-rerun.log`: successful exact return value from
  `tools.klean_preflight.check_generation`; includes the `lake clean` and
  `lake build` diagnostics.
- `04-stage4-bijection.log`: independent domain-rule/source-rule/obligation
  bijection, sidecar hash, null-target, status, and Stage 5 absence checks.
- `05-semantic-cases.log`: finite adversarial corroboration of the universal
  case analysis in `REVIEW.md`, including counterfactual mutations.

The scripts and compatibility-shim source are retained verbatim in
`evidence/commands/`.
