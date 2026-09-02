#!/usr/bin/env bash
set -u

candidate=/candidate
trusted=/reference
check_status=0

echo "SEMANTICS_MODE=SUPPLIED_SEMANTICS"
if [[ -d "$trusted/reference-semantics" && ! -L "$trusted/reference-semantics" ]]; then
  echo "MODE_MOUNT_CHECK=PASS trusted reference semantics is a real directory"
else
  echo "MODE_MOUNT_CHECK=FAIL trusted reference semantics missing, mistyped, or symlinked"
  check_status=1
fi

echo "CANDIDATE_TREE_BEGIN"
find -P "$candidate" -mindepth 1 -printf '%y\t%P\t%l\n' | LC_ALL=C sort
echo "CANDIDATE_TREE_END"

for rel in \
  run-input.json \
  metrics.json \
  codex-last.txt \
  codex-output.log \
  prompt.py \
  py2mpy.py \
  solution.py \
  solution.mpy \
  spec.k \
  verification.k
do
  path="$candidate/$rel"
  if [[ -L "$path" ]]; then
    echo "ARTIFACT_CHECK=FAIL symlink $rel"
    check_status=1
  elif [[ -f "$path" ]]; then
    echo "ARTIFACT_CHECK=PASS regular-file $rel"
  elif [[ -e "$path" ]]; then
    echo "ARTIFACT_CHECK=FAIL mistyped $rel"
    check_status=1
  else
    echo "ARTIFACT_CHECK=FAIL missing $rel"
    check_status=1
  fi
done

echo "TRACE_DISCOVERY_BEGIN"
find -P "$candidate" -maxdepth 2 \
  \( -iname '*trace*' -o -iname '*generation*' \) \
  -printf '%y\t%P\t%l\n' | LC_ALL=C sort
echo "TRACE_DISCOVERY_END"

for rel in prompt.py py2mpy.py; do
  if cmp -s "$candidate/$rel" "$trusted/$rel"; then
    echo "TRUSTED_FILE_COMPARE=PASS $rel byte-identical"
  else
    echo "TRUSTED_FILE_COMPARE=FAIL $rel differs"
    diff -u "$trusted/$rel" "$candidate/$rel" || true
    check_status=1
  fi
  sha256sum "$trusted/$rel" "$candidate/$rel"
done

candidate_sem="$candidate/reference-semantics"
trusted_sem="$trusted/reference-semantics"
if [[ -L "$candidate_sem" || ! -d "$candidate_sem" ]]; then
  echo "SEMANTICS_TREE_COMPARE=FAIL candidate tree root missing, mistyped, or symlinked"
  check_status=1
else
  candidate_manifest=$(mktemp)
  trusted_manifest=$(mktemp)
  find -P "$candidate_sem" -mindepth 1 -printf '%y\t%P\t%l\n' |
    LC_ALL=C sort >"$candidate_manifest"
  find -P "$trusted_sem" -mindepth 1 -printf '%y\t%P\t%l\n' |
    LC_ALL=C sort >"$trusted_manifest"
  echo "SEMANTICS_MANIFEST_DIFF_BEGIN"
  diff -u "$trusted_manifest" "$candidate_manifest" || check_status=1
  echo "SEMANTICS_MANIFEST_DIFF_END"

  while IFS= read -r trusted_file; do
    rel=${trusted_file#"$trusted_sem/"}
    candidate_file="$candidate_sem/$rel"
    if [[ ! -f "$candidate_file" || -L "$candidate_file" ]]; then
      echo "SEMANTICS_FILE_COMPARE=FAIL $rel missing, mistyped, or symlinked"
      check_status=1
    elif cmp -s "$trusted_file" "$candidate_file"; then
      echo "SEMANTICS_FILE_COMPARE=PASS $rel byte-identical"
    else
      echo "SEMANTICS_FILE_COMPARE=FAIL $rel content differs"
      check_status=1
    fi
  done < <(find -P "$trusted_sem" -type f | LC_ALL=C sort)

  while IFS= read -r candidate_file; do
    rel=${candidate_file#"$candidate_sem/"}
    trusted_file="$trusted_sem/$rel"
    if [[ ! -e "$trusted_file" && ! -L "$trusted_file" ]]; then
      echo "SEMANTICS_FILE_COMPARE=FAIL extra $rel"
      check_status=1
    fi
  done < <(find -P "$candidate_sem" -type f | LC_ALL=C sort)

  rm -f -- "$candidate_manifest" "$trusted_manifest"
fi

echo "INTEGRITY_SCRIPT_STATUS=$check_status"
exit "$check_status"
