# Audit command transcript

All paths below are immutable inputs except the explicitly fresh workspace
under `/tmp/audit-work` and this evidence directory.

## Static provenance and inventory

```sh
PYTHONPATH=/reference \
  python3 /audit-output/evidence/static_checks.py
# exit 0; complete result: 05-static-checks.log

PYTHONPATH=/reference \
  python3 /audit-output/evidence/stage4_hash_and_bijection_checks.py
# exit 0; complete result: 22-stage4-hash-and-bijection-checks.log

PYTHONPATH=/reference \
  python3 /audit-output/evidence/proof_source_checks.py
# exit 0; complete result: 20-proof-source-and-target-checks.log
```

Producer files were hashed directly:

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json
# exit 0; complete result: 02-producer-provenance.log
```

## Lean PID-namespace compatibility

The container exposes host-PID `/proc` entries while Lean 4.22 asks for
`/proc/<namespace-pid>/exe`. The compatibility shim redirects only that
specific `readlink` shape to `/proc/self/exe`.

```sh
gcc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc-exe-readlink-shim.so \
  /audit-output/evidence/proc_exe_readlink_shim.c -ldl

LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean --version

LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  /opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake --version
# all exit 0; complete result: 10i-proc-shim-build-and-version.log
```

The initial unshimmed preflight reached `lake clean` and failed before any
build with “could not detect the configuration of the Lake installation”:
`10-rerun-preflight.log`. The successful rerun below is the result used for
the audit.

## Trusted Stage 4 preflight

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
PYTHONPATH=/reference \
  python3 /audit-output/evidence/rerun_preflight.py
# exit 0; complete nested commands, outputs, and returned evidence:
# 10j-rerun-preflight-success.log
```

The wrapper invokes the requested trusted function:

```python
tools.klean_preflight.check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
```

Its nested commands were `lake clean` and `lake build`, both exit 0.

## Fresh proof build

Fresh workspace:
`/tmp/audit-work/57-monotonic-proof.bNlsvL`.

```sh
cp -a /reference/klean-generation/generated \
  /tmp/audit-work/57-monotonic-proof.bNlsvL/Base
cp -a /candidate/. /tmp/audit-work/57-monotonic-proof.bNlsvL/
# exit 0; file inventory and pre-build hashes:
# 11-fresh-proof-workspace.log

cd /tmp/audit-work/57-monotonic-proof.bNlsvL
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  lake clean
# exit 0; 12-fresh-lake-clean.log

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  lake build
# exit 0; 13-fresh-lake-build.log
```

## Proof identity and axioms

`AxiomAudit.lean` contains exactly:

```lean
import Proof

#print axioms Proof.final
```

Command:

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  lake env lean AxiomAudit.lean
# exit 0; exact output: 14-print-axioms-proof-final.log
```

The exact output is:

```text
'Proof.final' does not depend on any axioms
```

A second complete trusted final-gate run used:

```sh
PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
PYTHONPATH=/reference \
  python3 /audit-output/evidence/rerun_final_gate.py
# exit 0; complete nested clean/build/axiom output and returned evidence:
# 15-rerun-final-gate.log
```

## Operational-bridge tests and mutations

```sh
cd /tmp/audit-work/57-monotonic-proof.bNlsvL

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  lake env lean BridgeAudit.lean
# exit 0; 17-bridge-truth-tables.log

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  lake env lean CounterfactualAccepted.lean
# exit 0; 18a-counterfactual-accepted.log

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  lake env lean CounterfactualRejected.lean
# exit 1 as expected; exact residual `⊢ False`:
# 19-counterfactual-rejected.log

PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH \
LD_PRELOAD=/tmp/audit-work/proc-exe-readlink-shim.so \
  lake env lean ParameterPrint.lean
# exit 0; compiled definitions and final theorem:
# 21-print-parameters-and-final.log
```
