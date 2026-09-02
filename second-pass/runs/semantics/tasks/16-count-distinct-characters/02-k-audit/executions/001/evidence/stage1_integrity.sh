#!/usr/bin/env bash
set -u

candidate=/candidate
reference=/reference

required_candidate_files=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  spec.k
  verification.k
)

echo "SEMANTICS MODE: SUPPLIED_SEMANTICS"
if [[ -d "$reference/reference-semantics" && ! -L "$reference/reference-semantics" ]]; then
  echo "trusted reference-semantics: PRESENT DIRECTORY"
else
  echo "trusted reference-semantics: MODE BREACH"
fi

for name in "${required_candidate_files[@]}"; do
  path="$candidate/$name"
  if [[ -L "$path" ]]; then
    echo "required $name: SYMLINK -> $(readlink "$path")"
  elif [[ -f "$path" ]]; then
    echo "required $name: REGULAR FILE"
  elif [[ -e "$path" ]]; then
    echo "required $name: MISTYPED ($(stat -c %F "$path"))"
  else
    echo "required $name: MISSING"
  fi
done

echo "candidate top-level entries:"
find "$candidate" -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort

for pair in \
  "prompt.py:$reference/prompt.py" \
  "py2mpy.py:$reference/py2mpy.py"
do
  name=${pair%%:*}
  trusted=${pair#*:}
  if [[ -f "$candidate/$name" && ! -L "$candidate/$name" ]]; then
    if cmp -s "$candidate/$name" "$trusted"; then
      echo "$name trusted-byte-comparison: IDENTICAL"
    else
      echo "$name trusted-byte-comparison: CHANGED"
      sha256sum "$candidate/$name" "$trusted"
    fi
  else
    echo "$name trusted-byte-comparison: NOT COMPARABLE"
  fi
done

echo "candidate symlinks anywhere:"
find "$candidate" -type l -printf '%p -> %l\n' | sort

echo "supplied-semantics recursive comparison:"
python3 - "$candidate/reference-semantics" "$reference/reference-semantics" <<'PY'
import hashlib
import os
import stat
import sys

left, right = sys.argv[1:]

def inventory(root):
    result = {}
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        entries = list(dirs) + list(files)
        for name in entries:
            path = os.path.join(base, name)
            rel = os.path.relpath(path, root)
            mode = os.lstat(path).st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", "")
            elif stat.S_ISREG(mode):
                with open(path, "rb") as stream:
                    digest = hashlib.sha256(stream.read()).hexdigest()
                result[rel] = ("file", digest)
            else:
                result[rel] = ("other", stat.S_IFMT(mode))
    return result

cand = inventory(left)
ref = inventory(right)
all_paths = sorted(set(cand) | set(ref))
failures = 0
for path in all_paths:
    if path not in cand:
        failures += 1
        print(f"MISSING {path}: expected {ref[path]}")
    elif path not in ref:
        failures += 1
        print(f"ADDITIONAL {path}: candidate {cand[path]}")
    elif cand[path][0] != ref[path][0]:
        failures += 1
        print(f"MISTYPED {path}: candidate {cand[path][0]}, expected {ref[path][0]}")
    elif cand[path][0] == "symlink":
        failures += 1
        print(f"SYMLINK {path}: candidate target {cand[path][1]!r}")
    elif cand[path] != ref[path]:
        failures += 1
        print(f"CHANGED {path}: candidate {cand[path][1]}, expected {ref[path][1]}")

print(f"candidate entries: {len(cand)}")
print(f"trusted entries: {len(ref)}")
print(f"integrity failures: {failures}")
sys.exit(1 if failures else 0)
PY
