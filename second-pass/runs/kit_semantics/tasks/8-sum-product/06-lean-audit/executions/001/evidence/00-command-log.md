# Audit command log

All commands were run with the launcher's inherited
`AUDIT_MODE=CLASSIFICATION_AND_PROOF`. `script -q -e -c ... FILE` was used
where shown to retain complete stdout/stderr and exit status.

## Producer and independent structural checks

```sh
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /audit-input.json

PYTHONPATH=/reference \
  script -q -e -c \
  'python3 /audit-output/evidence/independent_checks.py' \
  /audit-output/evidence/02-independent-structural-checks.txt
```

The first producer command also attempted to use unavailable `jq` and exited
127 after the hashes had printed; that preliminary output is preserved in
`01-producer-provenance.txt`. The Python check performs the completed JSON
comparisons without `jq`.

## Trusted preflight

```sh
PYTHONPATH=/reference \
  script -q -e -c \
  'python3 /audit-output/evidence/run_preflight.py' \
  /audit-output/evidence/03-preflight-rerun.txt

PYTHONPATH=/reference ELAN_HOME=/opt/elan \
  script -q -e -c \
  'python3 /audit-output/evidence/run_preflight.py' \
  /audit-output/evidence/04-preflight-rerun-configured.txt

cc -shared -fPIC -O2 -Wall -Wextra \
  -o /tmp/audit-work/proc_exe_compat.so \
  /audit-output/evidence/proc_exe_compat.c -ldl

ELAN_HOME=/opt/elan LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  script -q -e -c 'lean --version; lake --version' \
  /audit-output/evidence/05-lean-runner-compat.txt

PYTHONPATH=/reference ELAN_HOME=/opt/elan \
LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  script -q -e -c \
  'python3 /audit-output/evidence/run_preflight.py' \
  /audit-output/evidence/06-preflight-rerun-success.txt
```

The compatibility library only redirects `readlink`/`readlinkat` requests for
`/proc/<numeric-pid>/exe` to `/proc/self/exe`. The audit sandbox exposed the
latter but hid the former; the first two retained preflight attempts diagnose
that runner issue.

## Fresh Stage 5 workspace and clean build

The first copy attempt copied the candidate's empty `Base` directory and then
nested the generated project at `Base/generated`; its failed target check is
preserved in `08-fresh-workspace-copy.txt`. The corrected copy used:

```sh
mkdir -p /tmp/audit-work/stage5-fresh-002/Base
cp /candidate/Proof.lean \
   /candidate/lakefile.lean \
   /candidate/lean-toolchain \
   /tmp/audit-work/stage5-fresh-002/
cp -a /reference/klean-generation/generated/. \
   /tmp/audit-work/stage5-fresh-002/Base/

cd /tmp/audit-work/stage5-fresh-002
ELAN_HOME=/opt/elan LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  script -q -e -c 'lake clean' \
  /audit-output/evidence/10-stage5-lake-clean.txt
ELAN_HOME=/opt/elan LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  script -q -e -c 'lake build' \
  /audit-output/evidence/11-stage5-lake-build.txt
```

## Proof, target, trust, and bridge checks

```sh
cd /tmp/audit-work/stage5-fresh-002
ELAN_HOME=/opt/elan LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  script -q -e -c 'lake env lean PrintAxioms.lean' \
  /audit-output/evidence/12-print-axioms.txt

ELAN_HOME=/opt/elan LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  script -q -e -c 'lake env lean BridgeTests.lean' \
  /audit-output/evidence/13-operational-bridge-tests.txt

diff -qr --exclude=.lake \
  /tmp/audit-work/stage5-fresh-002/Base \
  /reference/klean-generation/generated
rg -n -i '\b(sorry|admit|unsafe|axiom|opaque)\b' \
  /candidate/Proof.lean /candidate/lakefile.lean
sha256sum \
  /tmp/audit-work/stage5-fresh-002/Base/Klean8SumProduct/Lemmas.lean \
  /reference/klean-generation/generated/Klean8SumProduct/Lemmas.lean

PYTHONPATH=/reference \
  script -q -e -c \
  'python3 /audit-output/evidence/postbuild_target_check.py' \
  /audit-output/evidence/15-postbuild-target-identity.txt

PYTHONPATH=/reference \
  script -q -e -c \
  'python3 /audit-output/evidence/axiom_reconcile.py' \
  /audit-output/evidence/16-axiom-reconciliation.txt

ELAN_HOME=/opt/elan LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  script -q -e -c 'lake env lean ProofIdentity.lean' \
  /audit-output/evidence/19-proof-identity-lean-success.txt

ELAN_HOME=/opt/elan LD_PRELOAD=/tmp/audit-work/proc_exe_compat.so \
  script -q -e -c 'lake env lean CounterfactualGuard.lean' \
  /audit-output/evidence/22-counterfactual-vacuous-and-hardcoded-bridges.txt
```

The initial theorem-print command accidentally replaced the actual toolchain
path with a nonexistent path and exited 127; it is preserved in
`18-proof-identity-lean.txt`. The corrected command and full theorem term are
in `19-proof-identity-lean-success.txt`.
