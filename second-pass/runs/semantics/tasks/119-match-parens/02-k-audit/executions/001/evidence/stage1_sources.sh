#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_shell 'for f in /reference/prompt.py /reference/canonical.py /reference/py2mpy.py /candidate/solution.py /candidate/solution.mpy /candidate/spec.k /candidate/verification.k /candidate/prove.sh /candidate/concrete-tests.mpy; do echo "===== $f ====="; nl -ba "$f"; done'
run_shell 'python3 -c '"'"'import os; from pathlib import Path; bases=[Path("/reference/reference-semantics"),Path("/candidate/reference-semantics")]; [(print("TREE_TYPES",b),[(print(("symlink" if p.is_symlink() else "dir" if p.is_dir() else "file" if p.is_file() else "other"),p.relative_to(b))) for root,dirs,files in os.walk(b,followlinks=False) for p in [Path(root,n) for n in sorted(dirs+files)]]) for b in bases]'"'"
run_shell 'if test -e /tmp/audit-work/audit-119-match-parens || test -L /tmp/audit-work/audit-119-match-parens; then find /tmp/audit-work/audit-119-match-parens -mindepth 1 -maxdepth 2 -printf "%y %p -> %l\n" | LC_ALL=C sort; else echo SCRATCH_TARGET_ABSENT; fi'
