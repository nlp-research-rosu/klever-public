# Audit command index

The corresponding `.log` files in this directory are complete `script(1)` captures and include command exit codes. The principal commands were:

```sh
PYTHONPATH=/reference python /audit-output/evidence/producer_auth.py
PYTHONPATH=/reference python /audit-output/evidence/reconstruct_inventory.py
PYTHONPATH=/reference python /audit-output/evidence/classification_judgment.py
```

Fresh K proof ordering was checked in `/tmp/audit-work/stage1-recheck` with:

```sh
kompile --backend haskell foundation.k --main-module FOUNDATION --syntax-module FOUNDATION-SYNTAX --output-definition connection-kompiled
kprove connection-spec.k --definition connection-kompiled --spec-module CONNECTION-SPEC
kompile --backend haskell helper-verification.k --main-module HELPER-VERIFICATION --syntax-module HELPER-VERIFICATION-SYNTAX --output-definition loop-connection-kompiled
kprove loop-connection-spec.k --definition loop-connection-kompiled --spec-module LOOP-CONNECTION-SPEC
kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module VERIFICATION-SYNTAX --output-definition verification-kompiled
kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module VERIFICATION-SYNTAX --output-definition verification-json-kompiled --emit-json
PYTHONPATH=/reference python /audit-output/evidence/derived_lemma_compare.py
```

The source program identity check used fresh `kast --expand-macros --output kore` invocations for `getClosestProgram` and `solution.mpy`, followed by `sha256sum` and `cmp`; see `fresh_kast_*`, `fresh_program_identity_hashes.log`, and `fresh_program_identity_cmp.log`.

Stage 4 was checked with:

```sh
PYTHONPATH=/reference python -c 'from pathlib import Path; from tools.klean_preflight import check_generation; print(check_generation(Path("/reference/k-proof"), Path("/reference/lemma-discovery.json"), Path("/reference/klean-generation"), toolchain_lock=Path("/reference/klean-toolchain.lock.json")))'
PYTHONPATH=/reference python /audit-output/evidence/stage4_integrity.py
```

Stage 5 was copied to `/tmp/audit-work/lean-proof-audit-2` with the immutable generated project at `Base`, then checked with:

```sh
lake clean
lake build
lake env lean AuditAxioms.lean
lake env lean AuditIdentity.lean
lake env lean /audit-output/evidence/stage5_operational_adversarial.lean
PYTHONPATH=/reference python /audit-output/evidence/stage5_static_integrity.py
PYTHONPATH=/reference python -c 'from pathlib import Path; from tools.klean_final_gate import check_proof_candidate; print(check_proof_candidate(Path("/reference/klean-generation"), Path("/candidate")))'
```

For the Lean commands, `PATH` began with `/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin` and `LD_PRELOAD=/tmp/audit-work/libprocself.so` supplied the narrowly scoped `/proc/<pid>/exe` compatibility fix documented in `proc_exe_compat.c` and `lean_launcher_compat_build_and_test.log`.
