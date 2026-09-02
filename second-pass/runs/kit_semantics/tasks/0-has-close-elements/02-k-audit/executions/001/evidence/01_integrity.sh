#!/usr/bin/env bash
set -u

status=0
finish() {
  local rc=$?
  echo "SCRIPT_EXIT=$rc"
}
trap finish EXIT

required=(
  /audit-input.json
  /run.json
  /task.json
  /generation-result.json
  /generation/invocation.json
  /generation/metrics.json
  /generation/runtime-metrics.json
  /generation/usage.json
  /generation/codex-last.txt
  /generation/codex-output.log
  /generation/prompt.txt
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
)

echo "COMMAND: bash /audit-output/evidence/01_integrity.sh"
echo "REQUIRED_ARTIFACT_TYPES"
for path in "${required[@]}"; do
  if [[ -f "$path" && ! -L "$path" && -r "$path" ]]; then
    stat -c '%F %a %s %n' "$path"
  else
    echo "INVALID_REQUIRED_ARTIFACT $path"
    status=1
  fi
done

echo "TRACE_ENTRIES"
find /generation/codex-trace -printf '%y %P -> %l\n' | LC_ALL=C sort
if find /generation/codex-trace -type l -print -quit | grep -q .; then
  echo "INVALID_TRACE_SYMLINK"
  status=1
fi
if ! find /generation/codex-trace -type f -name '*.jsonl' -print -quit | grep -q .; then
  echo "MISSING_TRACE_JSONL"
  status=1
fi

echo "DECLARED_INDIVIDUAL_HASH_CHECKS"
check_hash() {
  local expected=$1
  local path=$2
  local actual
  actual=$(sha256sum "$path" | awk '{print $1}')
  if [[ "$actual" == "$expected" ]]; then
    echo "MATCH $actual $path"
  else
    echo "MISMATCH expected=$expected actual=$actual path=$path"
    status=1
  fi
}

check_hash b19fa4b9ec23ba3f2deb06e3228d77cef75127023b2ef10b386b54df9da9c9d6 /reference/canonical.py
check_hash 00b2e074e127a6a9d1376278bef732933760ab706057ec755a8c2642217b557a /reference/prompt.py
check_hash 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /reference/py2mpy.py
check_hash 6081e7000c8636ede4cc88b731a31c76b1addb4060846e784e1559c0d59a5835 /run.json
check_hash 95bc32a8e5e760474590ee9868474992ab8c0568a115471c8744785b7f4d4046 /task.json
check_hash 6a135dc6169282dddb167d79b37692d06db062c9264f6650850859725da415e6 /generation-result.json
check_hash 1dc8b670dd8081937eb66b256a9d9301b8f69c9ca35c2059aa06d223ee58da78 /generation/invocation.json
check_hash 4b1cbc23a10b3a48fa2481b1bec6a2f5adab73127690f78637c9506657a81a1e /generation/metrics.json
check_hash 799420963df0d0fb0d4de9671d7bedd7e2959b71c31f562bcba81dae837420b1 /generation/runtime-metrics.json
check_hash cba0aa6feccd360dc376c930bba3b68d97b38aa8fb51a56af59eca09823a4066 /generation/usage.json
check_hash 5ae68978fcf419d9e04292450e771a6734983c902e0b0d1d47694a2f38c4a7df /generation/codex-last.txt
check_hash 280762517078d34ca0ee68665fbde1e7ff1221ea9a3840b20b14c6a77d3fe1d0 /generation/codex-output.log
check_hash b6a26e02e06727577af0efab0b2bd22c3eb20fe397b069271f4eb05184d671cd /generation/prompt.txt
check_hash 223987e90c3b178c05e5ac3910f085c082e15b5bf54d28956c9cf5a4f6b72519 /generation/codex-trace/2026/07/26/rollout-2026-07-26T00-57-01-019f9cff-8c9c-76e3-8d3b-1ccd3a1400fc.jsonl

echo "CANDIDATE_TRUSTED_FILE_COMPARISONS"
for pair in \
  "/candidate/prompt.py /reference/prompt.py" \
  "/candidate/py2mpy.py /reference/py2mpy.py"
do
  set -- $pair
  if [[ -f "$1" && ! -L "$1" ]] && cmp -s "$1" "$2"; then
    echo "IDENTICAL $1 $2"
  else
    echo "NOT_IDENTICAL_OR_INVALID $1 $2"
    status=1
  fi
done

echo "SUPPLIED_SEMANTICS_TYPE_MANIFESTS"
find /reference/reference-semantics -printf '%y\t%P\t%l\n' | LC_ALL=C sort
find /candidate/reference-semantics -printf '%y\t%P\t%l\n' | LC_ALL=C sort
find /reference/reference-semantics -printf '%y\t%P\t%l\n' | LC_ALL=C sort > /tmp/audit-work/reference-semantics.types
find /candidate/reference-semantics -printf '%y\t%P\t%l\n' | LC_ALL=C sort > /tmp/audit-work/candidate-semantics.types
if cmp -s /tmp/audit-work/reference-semantics.types /tmp/audit-work/candidate-semantics.types; then
  echo "SEMANTICS_TYPES_IDENTICAL"
else
  echo "SEMANTICS_TYPE_MISMATCH"
  diff -u /tmp/audit-work/reference-semantics.types /tmp/audit-work/candidate-semantics.types || true
  status=1
fi
if diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics; then
  echo "SEMANTICS_CONTENT_IDENTICAL"
else
  echo "SEMANTICS_CONTENT_MISMATCH"
  status=1
fi

echo "INDEPENDENT_SOURCE_HASHES"
find /candidate -maxdepth 1 -type f -print0 |
  LC_ALL=C sort -z |
  xargs -0 sha256sum
find /reference/reference-semantics -type f -print0 |
  LC_ALL=C sort -z |
  xargs -0 sha256sum

echo "REQUIRED_CANDIDATE_PROOF_ARTIFACTS"
for path in \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/PROOF.md
do
  if [[ -f "$path" && ! -L "$path" && -r "$path" ]]; then
    stat -c '%F %a %s %n' "$path"
  else
    echo "INVALID_CANDIDATE_ARTIFACT $path"
    status=1
  fi
done

exit "$status"
