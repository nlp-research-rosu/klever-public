#!/usr/bin/env bash
set -u
set -o pipefail
set -x

printf '== candidate required metadata ==\n'
for path in \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log
do
  if [[ -e "$path" || -L "$path" ]]; then
    stat -c '%F %n -> %N' "$path"
  else
    printf 'MISSING %s\n' "$path"
  fi
done

printf '== candidate structured traces ==\n'
find /candidate -maxdepth 2 \
  \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*.json' \) \
  -printf '%y %p -> %l\n' | sort

printf '== other candidate proof claims (untrusted, bounded) ==\n'
for path in \
  /candidate/PROOF.md \
  /candidate/call-proof.out \
  /candidate/loop-proof.out \
  /candidate/concrete-krun.out
do
  if [[ -f "$path" && ! -L "$path" ]]; then
    stat -c '%F %s bytes %n' "$path"
    sha256sum "$path"
    sed -n '1,160p' "$path"
  elif [[ -e "$path" || -L "$path" ]]; then
    stat -c 'MISTYPED_OR_SYMLINKED %F %n -> %N' "$path"
  else
    printf 'MISSING %s\n' "$path"
  fi
done

printf '== trusted-mode boundary ==\n'
if [[ -d /reference/reference-semantics && ! -L /reference/reference-semantics ]]; then
  printf 'TRUSTED_SEMANTICS_PRESENT_DIRECTORY\n'
else
  printf 'TRUSTED_SEMANTICS_BOUNDARY_BREACH\n'
fi

printf '== candidate required source types ==\n'
for path in \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/reference-semantics
do
  if [[ -e "$path" || -L "$path" ]]; then
    stat -c '%F %n -> %N' "$path"
  else
    printf 'MISSING %s\n' "$path"
  fi
done

printf '== prompt identity ==\n'
cmp --silent /candidate/prompt.py /reference/prompt.py
prompt_status=$?
printf 'PROMPT_CMP_EXIT=%s\n' "$prompt_status"
sha256sum /candidate/prompt.py /reference/prompt.py

printf '== translator identity ==\n'
cmp --silent /candidate/py2mpy.py /reference/py2mpy.py
translator_status=$?
printf 'TRANSLATOR_CMP_EXIT=%s\n' "$translator_status"
sha256sum /candidate/py2mpy.py /reference/py2mpy.py

printf '== semantics recursive type/path/content comparison ==\n'
python3 - <<'PY'
import hashlib
import os
from pathlib import Path

trusted = Path("/reference/reference-semantics")
candidate = Path("/candidate/reference-semantics")

def inventory(root: Path):
    entries = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                entries[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                entries[rel] = ("directory", None)
            elif path.is_file():
                entries[rel] = (
                    "file",
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                )
            else:
                entries[rel] = ("other", None)
    return entries

t = inventory(trusted)
c = inventory(candidate)
all_paths = sorted(set(t) | set(c))
differences = 0
for rel in all_paths:
    if rel not in t:
        print(f"ADDITIONAL {rel}: {c[rel]}")
        differences += 1
    elif rel not in c:
        print(f"MISSING {rel}: expected {t[rel]}")
        differences += 1
    elif t[rel] != c[rel]:
        print(f"CHANGED_OR_MISTYPED {rel}: trusted={t[rel]} candidate={c[rel]}")
        differences += 1
    elif c[rel][0] == "symlink":
        print(f"SYMLINKED {rel}: candidate={c[rel]}")
        differences += 1
print(f"SEMANTICS_DIFFERENCE_COUNT={differences}")
raise SystemExit(0 if differences == 0 else 1)
PY
semantics_status=$?
printf 'SEMANTICS_COMPARE_EXIT=%s\n' "$semantics_status"

if (( prompt_status == 0 && translator_status == 0 && semantics_status == 0 )); then
  exit 0
fi
exit 1
