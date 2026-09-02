#!/usr/bin/env bash
set -u

status=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
}

printf 'Stage 1: independent provenance and integrity checks\n'
printf 'Rendered semantics mode: SUPPLIED_SEMANTICS\n'

required=(
  /candidate/run-input.json
  /candidate/metrics.json
  /candidate/codex-last.txt
  /candidate/codex-output.log
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/reference-semantics
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
  /candidate/PROOF.md
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
)

printf '\nRequired artifact types (symlinks are failures):\n'
for path in "${required[@]}"; do
  if [[ -L "$path" ]]; then
    printf 'FAIL symlink %s -> %s\n' "$path" "$(readlink "$path")"
    status=1
  elif [[ -f "$path" ]]; then
    printf 'OK regular-file %s\n' "$path"
  elif [[ -d "$path" ]]; then
    printf 'OK directory %s\n' "$path"
  elif [[ -e "$path" ]]; then
    printf 'FAIL mistyped %s (%s)\n' "$path" "$(stat -c %F "$path")"
    status=1
  else
    printf 'FAIL missing %s\n' "$path"
    status=1
  fi
done

printf '\nSymlinks anywhere in semantics trees:\n'
candidate_links="$(find /candidate/reference-semantics -type l -print 2>&1)"
reference_links="$(find /reference/reference-semantics -type l -print 2>&1)"
if [[ -n "$candidate_links" ]]; then
  printf 'FAIL candidate semantics symlinks:\n%s\n' "$candidate_links"
  status=1
else
  printf 'OK no candidate semantics symlinks\n'
fi
if [[ -n "$reference_links" ]]; then
  printf 'INFRASTRUCTURE candidate-independent trusted semantics symlinks:\n%s\n' "$reference_links"
  status=1
else
  printf 'OK no trusted semantics symlinks\n'
fi

run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run diff -r --no-dereference --brief /reference/reference-semantics /candidate/reference-semantics

printf '\nSemantics manifests (type, relative path, size, sha256 for files):\n'
for root in /reference/reference-semantics /candidate/reference-semantics; do
  printf -- '-- %s --\n' "$root"
  while IFS= read -r -d '' path; do
    rel="${path#"$root"/}"
    if [[ -f "$path" && ! -L "$path" ]]; then
      printf 'f %s %s ' "$rel" "$(stat -c %s "$path")"
      sha256sum "$path" | awk '{print $1}'
    elif [[ -d "$path" && ! -L "$path" ]]; then
      printf 'd %s\n' "$rel"
    elif [[ -L "$path" ]]; then
      printf 'l %s -> %s\n' "$rel" "$(readlink "$path")"
    else
      printf '? %s %s\n' "$rel" "$(stat -c %F "$path")"
    fi
  done < <(find "$root" -mindepth 1 -print0 | sort -z)
done

printf '\nTrusted/candidate provenance hashes:\n'
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/verification.k /candidate/spec.k

trace_count="$(find /candidate/codex-trace -type f -name '*.jsonl' | wc -l)"
printf '\nStructured generation trace JSONL files: %s\n' "$trace_count"
find /candidate/codex-trace -type f -name '*.jsonl' -printf '%p %s bytes\n' | sort

printf '\nFinal stage1_status=%d\n' "$status"
exit "$status"
