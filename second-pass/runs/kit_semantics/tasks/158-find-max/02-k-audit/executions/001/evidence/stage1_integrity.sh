#!/usr/bin/env bash
set -u

status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
}

check_hash() {
  path=$1
  expected=$2
  actual=$(sha256sum "$path" | cut -d' ' -f1)
  printf '%s  %s\n' "$actual" "$path"
  if [[ "$actual" == "$expected" ]]; then
    printf '[recorded hash match]\n'
  else
    printf '[RECORDED HASH MISMATCH expected=%s]\n' "$expected"
    status=1
  fi
}

printf 'K toolchain\n'
run kompile --version
run kprove --version

printf '\nRequired pipeline-v3 records\n'
required=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/runtime-metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/codex-trace
  /candidate
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
)
for path in "${required[@]}"; do
  if [[ -r "$path" ]]; then
    stat -c '%F %s %n' "$path"
  else
    printf 'MISSING_OR_UNREADABLE %s\n' "$path"
    status=1
  fi
done

printf '\nRecorded singleton hashes\n'
check_hash /audit-campaign-lock.json ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745
check_hash /reference/canonical.py bd032dde583b287bd0fbefdc7c81e394436ab874fe20c50dbb1eb797e790b935
check_hash /reference/prompt.py c40e718aa330b51ea3bb37b1532061de990739b868af73c34faa3af0512626c3
check_hash /reference/py2mpy.py 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16
check_hash /candidate/prompt.py c40e718aa330b51ea3bb37b1532061de990739b868af73c34faa3af0512626c3
check_hash /candidate/py2mpy.py 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16
check_hash /run.json 57897a7c9ac278bb7e80d2bc5edb6c584ad49eca5b26e72b1c70cc396b108075
check_hash /task.json cb0658c40561c577cdd26bcbf65b8ff105ad9f4ee847e00df729633cac7ed4ce
check_hash /generation-result.json d9368c26bb429d1efce03720a33371473c9c283e3fdad1c8fbed7669c1a1f764
check_hash /generation-evidence/invocation.json 65d78911d0a4a1d104fe9c402a2443c0f0d6a24ff010235c99281eefdb05d9f0
check_hash /generation-evidence/metrics.json ad413372d791eca7b10386cb2c2db779303869ef95d9638ea27ed5b3d1292df9
check_hash /generation-evidence/runtime-metrics.json 28a92cd664c85870a823441d834cce75681e52dbf63603295ec29baf38b38ff0
check_hash /generation-evidence/usage.json e5264ef8d2d98c9e8a10bfb7c8492a6835692f08eb4178f6a8be0c66982e1dea
check_hash /generation-evidence/codex-last.txt 0a450edbb47d23a0c6e3c0bee71ec9dbb49dc745e939000dd98c74d3bd35707e
check_hash /generation-evidence/codex-output.log 1cc2608d33a6e93bbe49fe06160c197abb46f133f92606a2729562b523934d29
check_hash /generation-evidence/prompt.txt b6a26e02e06727577af0efab0b2bd22c3eb20fe397b069271f4eb05184d671cd
check_hash \
  /generation-evidence/codex-trace/2026/07/29/rollout-2026-07-29T12-51-19-019faf00-9931-70c1-8618-ad603f8355d4.jsonl \
  feb41cf46e8e9765363903d131982305b6a451bd898d517bcc50da7431cfb7fd

printf '\nTrusted/candidate source identity\n'
run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics

printf '\nSymlink checks in source/provenance mounts\n'
symlinks=$(
  find \
    /candidate/reference-semantics \
    /reference/reference-semantics \
    /generation-evidence \
    -type l -print
)
if [[ -z "$symlinks" ]]; then
  printf 'none\n'
else
  printf '%s\n' "$symlinks"
  status=1
fi

printf '\nStructured JSON and campaign-lock check\n'
run python3 /audit-output/evidence/stage1_json_check.py

printf '\nOverall integrity script status=%d\n' "$status"
exit "$status"
