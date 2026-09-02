#!/usr/bin/env bash
set -u -o pipefail

for root in /candidate /reference /generation-evidence/codex-trace; do
  printf '\n$ find %q -type f -print0 | sort -z | xargs -0 sha256sum\n' "$root"
  find "$root" -type f -print0 | sort -z | xargs -0 sha256sum
  status=$?
  printf '[exit %d]\n' "$status"
done

printf '\n$ independent deterministic candidate manifest digest\n'
python3 -c '
import hashlib
from pathlib import Path

root = Path("/candidate")
manifest = bytearray()
for path in sorted(p for p in root.rglob("*") if p.is_file()):
    relative = path.relative_to(root).as_posix()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest.extend(f"{relative}\0{digest}\n".encode())
print(hashlib.sha256(manifest).hexdigest(),
      "independent-path-NUL-content-sha256 manifest")
'
status=$?
printf '[exit %d]\n' "$status"
