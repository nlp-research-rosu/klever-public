# Principal audit commands

The numbered `.log` files in this directory contain the corresponding raw
stdout/stderr and exit codes. Commands that inspect candidate/provenance
content only read it as data.

## Signed inputs and hashes

```bash
env | rg '^AUDIT_MODE='
sed -n '1,260p' /audit-input.json
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /audit-input.json
```

Tree hashes were recomputed with the trusted
`tools.pipeline_contract.sha256_tree` and `tools.klean_export.tree_digest`
functions under `PYTHONPATH=/reference`. Every Stage 1 source file was hashed
directly with `hashlib.sha256`.

## Canonical rule inventory

```bash
PYTHONPATH=/reference python -c '
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(
    inventory_verification(Path("/reference/k-proof")),
    indent=2,
    sort_keys=True,
))
'
```

The protected-manifest structural validation additionally called:

```python
validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)
```

## Required Stage 4 preflight

The initial unmodified invocation was:

```python
from pathlib import Path
from tools.klean_preflight import check_generation

check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
```

After diagnosing the mismatched PID namespace exposed through `/proc`, the
same call was rerun under:

```bash
LD_PRELOAD=/tmp/audit-work/lean_pidns_fix.so
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0
PYTHONPATH=/reference
```

The shim changes only failed `readlink("/proc/<namespace-pid>/exe", ...)`
calls into `readlink("/proc/self/exe", ...)`. The failed call is shown in
`22_lean_pathtrace.log`; the successful toolchain/version probe is in
`23_lean_pid_namespace_workaround.log`; the complete returned preflight
document is in `24_check_generation_returned_evidence_rerun.log`.

## Independent Stage 4 checks

The script represented in `26_stage4_independent_crosschecks.log` directly:

- parsed every Stage 4 JSON sidecar;
- recomputed all file/tree hashes;
- independently supplied the audited empty domain set;
- compared ordered source-rule and obligation IDs;
- called `klean_export.target_statement` and
  `klean_export.expected_target_definition`;
- checked audit mode and Stage 5 absence; and
- compared the fresh preflight result with both recorded copies.

It reports `ALL_CHECKS_PASS True CHECK_COUNT 58`.

## Semantic checks

The data-only token comparison in `28_program_term_identity.log` used the
trusted reconstructed `validDateBody` rule and directly tokenized frozen
`solution.mpy`; it did not run a provenance script.

The independently encoded source-control and K-summary models in
`27_semantic_adversarial_checks.log` checked 1,265,625 representative
month/day/separator combinations, 60 year perturbations, 105 non-ten lengths,
targeted examples, and five counterfactual mutations.
