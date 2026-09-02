#!/usr/bin/env bash
set -u

EVIDENCE_DIR=/audit-output/evidence
WORK_DIR=/tmp/audit-work/audit-131-digits
LOG_FILE="$EVIDENCE_DIR/stage1_integrity.log"

: > "$LOG_FILE"

run() {
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } >> "$LOG_FILE"
  "$@" >> "$LOG_FILE" 2>&1
  status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status" >> "$LOG_FILE"
  return 0
}

manifest_tree() {
  root=$1
  destination=$2
  (
    cd "$root" || exit 125
    while IFS= read -r -d '' entry; do
      relative=${entry#./}
      if [[ -L "$entry" ]]; then
        printf 'l|%s|%s\n' "$relative" "$(readlink "$entry")"
      elif [[ -d "$entry" ]]; then
        printf 'd|%s|\n' "$relative"
      elif [[ -f "$entry" ]]; then
        printf 'f|%s|%s\n' "$relative" "$(sha256sum "$entry" | cut -d' ' -f1)"
      else
        printf 'o|%s|\n' "$relative"
      fi
    done < <(find -P . -mindepth 1 -print0 | sort -z)
  ) > "$destination"
}

printf 'Rendered mode: SUPPLIED_SEMANTICS\n' >> "$LOG_FILE"
if [[ -d /reference/reference-semantics && ! -L /reference/reference-semantics ]]; then
  printf 'Trusted semantics boundary: PRESENT_DIRECTORY\n\n' >> "$LOG_FILE"
else
  printf 'Trusted semantics boundary: INVALID_OR_MISSING\n\n' >> "$LOG_FILE"
fi

for artifact in \
  run-input.json \
  metrics.json \
  codex-last.txt \
  codex-output.log; do
  if [[ -e "/candidate/$artifact" || -L "/candidate/$artifact" ]]; then
    printf 'REQUIRED_CLAIM_ARTIFACT %s: PRESENT\n' "$artifact" >> "$LOG_FILE"
  else
    printf 'REQUIRED_CLAIM_ARTIFACT %s: MISSING\n' "$artifact" >> "$LOG_FILE"
  fi
done
printf '\n' >> "$LOG_FILE"

manifest_tree /candidate/reference-semantics \
  "$EVIDENCE_DIR/candidate-semantics.manifest"
manifest_tree /reference/reference-semantics \
  "$EVIDENCE_DIR/trusted-semantics.manifest"

run diff -u \
  "$EVIDENCE_DIR/trusted-semantics.manifest" \
  "$EVIDENCE_DIR/candidate-semantics.manifest"
run cmp -s /candidate/prompt.py /reference/prompt.py
run sha256sum /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum /candidate/py2mpy.py /reference/py2mpy.py
run find -P /candidate -type l -print

run mkdir -p "$WORK_DIR/candidate" "$WORK_DIR/trusted"
run cp -a \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/prove.sh \
  /candidate/concrete-tests.py \
  /candidate/concrete-tests.mpy \
  "$WORK_DIR/candidate/"
run cp -a /candidate/reference-semantics "$WORK_DIR/candidate/"
run cp -a \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  "$WORK_DIR/trusted/"

run find -P "$WORK_DIR" -maxdepth 3 -printf '%y %p -> %l\n'
