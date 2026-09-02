# Auditor command manifest

All commands ran with working directory `/tmp/audit-work/fresh` unless stated
otherwise. `script -q -e -c ... LOG` captured terminal output and the exact
wrapped command's exit status in each named log footer.

| Purpose | Exact substantive command | Exit | Log |
|---|---|---:|---|
| Integrity | `python3 /audit-output/evidence/stage1_integrity.py` | 0 | `stage1_integrity.log` |
| Trace inspection | `python3 /audit-output/evidence/trace_summary.py` | 0 | `trace_summary.log` |
| Regenerate MPY | `python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy; cmp -l regenerated-solution.mpy solution.mpy` | 0 / 0 | `mpy_regeneration.log` |
| Python differential | `python3 /audit-output/evidence/differential_test.py` | 1 (detected mismatches) | `differential_test.log` |
| Toolchain | `command -v kup; command -v kompile; command -v krun; command -v kprove; kompile --version; krun --version; kprove --version` | 0 overall (`kup` absent, independently installed K present) | `toolchain.log` |
| Concrete build | `kompile --backend llvm semantic.k --main-module MODP-SEMANTIC --syntax-module MODP-SYNTAX --output-definition semantic-llvm-kompiled` | 0 | `build_semantic_llvm.log` |
| Proof build | `kompile --backend haskell verification.k --main-module MODP-VERIFICATION --syntax-module MODP-SYNTAX --output-definition verification-haskell-kompiled` | 0 | `build_verification_haskell.log` |
| Original + isolated positive claims | `bash /audit-output/evidence/run_positive_claims.sh` | 0 | `positive_claims.log` |
| Concrete semantics comparisons | `python3 /audit-output/evidence/concrete_semantics.py` | 0 (all in-domain generated-Python comparisons matched) | `concrete_semantics.log` |
| Constructor pinning | `python3 /audit-output/evidence/pinning_check.py` | 0 | `pinning_check.log` |
| Body sensitivity | `kprove spec-body-mutation.k --definition verification-haskell-kompiled --spec-module AUDIT-SPEC-BODY-MUTATION` | 1 (expected stuck result) | `body_mutation.log` |
| Local inventory check | `rg -n "^[[:space:]]*(syntax|configuration|rule|claim)" semantic.k verification.k spec.k` plus attribute-keyword scan | 0 | `static_inventory_check.log` |
| Mutation parse/build | `kprove --dry-run spec-vacuity-audit.k --definition verification-haskell-kompiled --spec-module AUDIT-SPEC-VACUITY --output none` | 0 | `nonvacuity_dry_run.log` |
| Mutation proof | `kprove spec-vacuity-audit.k --definition verification-haskell-kompiled --spec-module AUDIT-SPEC-VACUITY` | 1 (expected `WarnStuckClaimState`) | `nonvacuity_proof.log` |
| K primitive boundary | `sed -n '1218,1264p' /usr/include/kframework/builtin/domains.md; sha256sum /usr/include/kframework/builtin/domains.md` | 0 | `k_powmod_trust_boundary.log` |
