#!/usr/bin/env bash
set -uo pipefail

echo 'COMMAND: python3 campaign/container-path comparison'
python3 - <<'PY'
import json
import pathlib

audit_input = json.load(open("/audit-input.json", encoding="utf-8"))
campaign_lock = json.load(open("/audit-campaign-lock.json", encoding="utf-8"))
print("record_layout=" + str(audit_input.get("record_layout")))
print("semantics_mode=" + str(audit_input.get("semantics_mode")))
print("campaign_block_equal=" + str(audit_input.get("audit_campaign") == campaign_lock))
for name, raw_path in sorted(audit_input.get("container_paths", {}).items()):
    path = pathlib.Path(raw_path)
    print(
        f"container_path {name}: exists={path.exists()} "
        f"file={path.is_file()} dir={path.is_dir()} symlink={path.is_symlink()} path={path}"
    )
PY
echo "EXIT: $?"

echo 'COMMAND: independent typed tree digests for mounted directories'
python3 - <<'PY'
import hashlib
import os
import pathlib
import stat


def tree_digest(root: pathlib.Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    entries = 0
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        entries += 1
        rel = path.relative_to(root).as_posix().encode()
        info = path.lstat()
        digest.update(rel + b"\0" + oct(stat.S_IMODE(info.st_mode)).encode() + b"\0")
        if path.is_symlink():
            digest.update(b"L\0" + os.readlink(path).encode() + b"\0")
        elif path.is_dir():
            digest.update(b"D\0")
        elif path.is_file():
            digest.update(b"F\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            digest.update(b"\0")
        else:
            digest.update(b"O\0")
    return digest.hexdigest(), entries


for raw in (
    "/candidate",
    "/candidate/reference-semantics",
    "/reference/reference-semantics",
    "/generation-evidence/codex-trace",
):
    value, count = tree_digest(pathlib.Path(raw))
    print(f"reviewer_tree_sha256={value} entries={count} root={raw}")
PY
echo "EXIT: $?"

echo 'COMMAND: sha256sum launcher-declared and pipeline-v3 records'
sha256sum \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/29/*.jsonl
echo "EXIT: $?"

echo 'COMMAND: cmp trusted prompt and translator'
cmp /reference/prompt.py /candidate/prompt.py
prompt_status=$?
cmp /reference/py2mpy.py /candidate/py2mpy.py
translator_status=$?
echo "prompt_cmp_exit=$prompt_status translator_cmp_exit=$translator_status"

echo 'COMMAND: recursive supplied-semantics comparison'
diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
echo "semantics_diff_exit=$?"

echo 'COMMAND: reject symlinks in mounted evidence'
symlinks="$(
  find /candidate /reference /generation-evidence -type l -printf '%p -> %l\n'
)"
if [[ -n "$symlinks" ]]; then
  printf '%s\n' "$symlinks"
  echo 'symlink_check_exit=1'
else
  echo 'symlink_check_exit=0 symlinks=0'
fi

echo 'COMMAND: candidate proof-artifact presence and types'
for path in \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/PROOF.md
do
  stat -c '%F %a %s %n' "$path"
done
