# Audit command record

All commands were run from `/audit-output`. Complete outputs are in the named
evidence files.

1. `PYTHONPATH=/reference python evidence/check_integrity.py` →
   `01-integrity.json`.
2. `PYTHONPATH=/reference python evidence/reconstruct_inventory.py` →
   `02-inventory-reconstruction.json`.
3. `PYTHONPATH=/reference python -c '... tools.klean_preflight.check_generation(...) ...'`
   → initial sandbox path-discovery failure in `03-klean-preflight.json`.
4. `cc -shared -fPIC -O2 -o /tmp/audit-work/proc-self-exe-shim.so evidence/proc_self_exe_shim.c -ldl`.
5. `LD_PRELOAD=/tmp/audit-work/proc-self-exe-shim.so /usr/local/bin/assert-frozen-toolchain agent`
   → `00-frozen-toolchain.log`.
6. The exact `check_generation` call from step 3 with the path-resolution shim
   preloaded → `04-klean-preflight-rerun.json`.
7. `cp -a /candidate/. <fresh>/` and
   `cp -a /reference/klean-generation/generated/. <fresh>/Base/` → hashes and
   path in `05-proof-workdir*`.
8. `(cd <fresh> && lake clean)` and `(cd <fresh> && lake build)`, with the shim
   preloaded → `06-lake-clean.log` and `07-lake-build.log`.
9. `(cd <fresh> && lake env lean AxiomAudit.lean)` → `08-axiom-audit.log`.
10. Trusted `klean_final_gate.py` with all frozen inputs, `/candidate`, the
    toolchain lock, and `/audit-input.json` → `09-mechanical-final-gate.json`.
11. `(cd <fresh> && lake env lean Adversarial.lean)` →
    `10-adversarial-lean.log`.
12. `kompile --backend llvm /reference/k-proof/reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition <fresh-k>/runtime-kompiled`
    → `11-kompile-llvm.log`.
13. `krun /reference/k-proof/concrete_test.mpy --definition <fresh-k>/runtime-kompiled`
    → `12-krun-concrete.log`.
14. `(cd <fresh> && lake env lean Counterfactual.lean)` →
    `13-counterfactual-constant.log`.
15. `PYTHONPATH=/reference python evidence/check_stage4_target.py` →
    `14-stage4-target-checks.json`.
16. Candidate scans and generated-target source hash comparison →
    `15-candidate-static-scan.log`.
17. `PYTHONPATH=/reference python evidence/reconcile_axioms.py` →
    `16-axiom-reconciliation.json`.
18. `(cd /reference/k-proof && PYTHONDONTWRITEBYTECODE=1 python differential_test.py)`
    → `17-source-differential.log`.

The preload shim changes only failed reads of `/proc/<current-pid>/exe` to
`/proc/self/exe`. This audit sandbox exposes the latter but not the former.
Without the shim Lean cannot locate its own immutable installation; with it,
the trusted frozen-toolchain gate reports the pinned K, pyk/Klean, Lean, and
Codex versions.
