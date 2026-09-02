#!/usr/bin/env bash
set -u
source /audit-output/evidence/run_logged.sh

run_cmd date --iso-8601=seconds
run_cmd pwd
run_shell 'command -v kup; command -v kompile; command -v kprove; command -v krun'
run_shell 'kompile --version; kprove --version; krun --version'

run_shell 'if test -d /reference/reference-semantics; then echo SUPPLIED_SEMANTICS_BASELINE_PRESENT; else echo SUPPLIED_SEMANTICS_BASELINE_MISSING; exit 1; fi'
run_shell 'find /candidate -mindepth 1 -maxdepth 3 -printf "%y %m %s %p -> %l\n" | LC_ALL=C sort'
run_shell 'find /reference -mindepth 1 -maxdepth 4 -printf "%y %m %s %p -> %l\n" | LC_ALL=C sort'
run_shell 'find /candidate -type l -printf "%p -> %l\n" | LC_ALL=C sort'
run_shell 'find /reference/reference-semantics -type l -printf "%p -> %l\n" | LC_ALL=C sort'

run_shell 'for f in run-input.json metrics.json codex-last.txt codex-output.log; do p=/candidate/$f; if test -f "$p" && ! test -L "$p"; then echo "===== $p ====="; sed -n "1,240p" "$p"; else echo "MISSING_OR_MISTYPED $p"; fi; done'
run_shell 'find /candidate -maxdepth 2 -type f \( -iname "*trace*" -o -iname "*.jsonl" \) -print | LC_ALL=C sort'
run_shell 'for p in $(find /candidate -maxdepth 2 -type f \( -iname "*trace*" -o -iname "*.jsonl" \) -print | LC_ALL=C sort); do echo "===== $p ====="; sed -n "1,320p" "$p"; done'

run_shell 'cmp -s /candidate/prompt.py /reference/prompt.py; rc=$?; if test "$rc" -eq 0; then echo PROMPT_BYTE_IDENTICAL; else echo PROMPT_DIFFERENT_OR_MISSING; fi; exit "$rc"'
run_shell 'cmp -s /candidate/py2mpy.py /reference/py2mpy.py; rc=$?; if test "$rc" -eq 0; then echo TRANSLATOR_BYTE_IDENTICAL; else echo TRANSLATOR_DIFFERENT_OR_MISSING; fi; exit "$rc"'
run_shell 'diff -ruN --no-dereference /reference/reference-semantics /candidate/reference-semantics'
run_shell 'python3 - <<'"'"'PY'"'"'\nimport os\nfrom pathlib import Path\nfor base in (Path(\"/reference/reference-semantics\"), Path(\"/candidate/reference-semantics\")):\n    print(f\"TREE_TYPES {base}\")\n    for root, dirs, files in os.walk(base, followlinks=False):\n        for name in sorted(dirs + files):\n            p = Path(root, name)\n            if p.is_symlink(): kind = \"symlink\"\n            elif p.is_dir(): kind = \"dir\"\n            elif p.is_file(): kind = \"file\"\n            else: kind = \"other\"\n            print(kind, p.relative_to(base))\nPY'

run_shell 'for f in /reference/prompt.py /reference/canonical.py /reference/py2mpy.py /candidate/solution.py /candidate/solution.mpy /candidate/semantic.k /candidate/semantics.k /candidate/verification.k /candidate/spec.k /candidate/PROOF.md; do if test -e "$f" || test -L "$f"; then stat -c "%F %a %s %n -> %N" "$f"; else echo "ABSENT $f"; fi; done'
