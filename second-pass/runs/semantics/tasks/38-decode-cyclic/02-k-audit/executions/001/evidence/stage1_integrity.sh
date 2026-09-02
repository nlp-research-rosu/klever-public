#!/usr/bin/env bash
set -u

candidate=/candidate
trusted=/reference
failures=0

check_regular_file() {
  local path=$1
  if [[ -L "$path" ]]; then
    printf 'INTEGRITY_FAILURE symlink required file: %s -> %s\n' "$path" "$(readlink "$path")"
    failures=$((failures + 1))
  elif [[ ! -f "$path" ]]; then
    if [[ -e "$path" ]]; then
      printf 'INTEGRITY_FAILURE mistyped required file: %s\n' "$path"
    else
      printf 'INTEGRITY_FAILURE missing required file: %s\n' "$path"
    fi
    failures=$((failures + 1))
  else
    printf 'OK regular file: %s\n' "$path"
  fi
}

printf 'SEMANTICS_MODE: SUPPLIED_SEMANTICS\n'
if [[ -d "$trusted/reference-semantics" && ! -L "$trusted/reference-semantics" ]]; then
  printf 'OK trusted reference semantics present\n'
else
  printf 'INFRASTRUCTURE_BREACH trusted reference semantics missing or mistyped\n'
  exit 70
fi

for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  check_regular_file "$candidate/$name"
done

for name in prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k; do
  check_regular_file "$candidate/$name"
done

for pair in "prompt.py prompt.py" "py2mpy.py py2mpy.py"; do
  set -- $pair
  if cmp -s "$candidate/$1" "$trusted/$2"; then
    printf 'OK byte-identical trusted input: candidate/%s == reference/%s\n' "$1" "$2"
  else
    printf 'INTEGRITY_FAILURE changed trusted input: candidate/%s != reference/%s\n' "$1" "$2"
    failures=$((failures + 1))
  fi
done

if [[ -L "$candidate/reference-semantics" || ! -d "$candidate/reference-semantics" ]]; then
  printf 'INTEGRITY_FAILURE candidate reference-semantics root is missing, symlinked, or mistyped\n'
  failures=$((failures + 1))
else
  printf 'OK candidate reference-semantics root is a directory\n'
fi

tmp_listing=$(mktemp)
trap 'rm -f "$tmp_listing" "$tmp_listing.candidate" "$tmp_listing.trusted"' EXIT
(
  cd "$candidate/reference-semantics" || exit
  find . -mindepth 1 -printf '%P\t%y\t%l\n' | LC_ALL=C sort
) >"$tmp_listing.candidate"
(
  cd "$trusted/reference-semantics" || exit
  find . -mindepth 1 -printf '%P\t%y\t%l\n' | LC_ALL=C sort
) >"$tmp_listing.trusted"

if diff -u "$tmp_listing.trusted" "$tmp_listing.candidate"; then
  printf 'OK semantics tree entry names/types/link-targets identical\n'
else
  printf 'INTEGRITY_FAILURE semantics tree names/types/link-targets differ\n'
  failures=$((failures + 1))
fi

while IFS= read -r -d '' trusted_file; do
  rel=${trusted_file#"$trusted/reference-semantics/"}
  candidate_file="$candidate/reference-semantics/$rel"
  if [[ -f "$candidate_file" && ! -L "$candidate_file" ]]; then
    if ! cmp -s "$trusted_file" "$candidate_file"; then
      printf 'INTEGRITY_FAILURE changed semantics file: %s\n' "$rel"
      failures=$((failures + 1))
    fi
  fi
done < <(find "$trusted/reference-semantics" -type f -print0)

if find "$candidate" -maxdepth 2 -type f \
    \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*generation*' \) \
    -print -quit | grep -q .; then
  printf 'Structured generation trace candidates:\n'
  find "$candidate" -maxdepth 2 -type f \
    \( -iname '*trace*' -o -iname '*.jsonl' -o -iname '*generation*' \) -print | sort
else
  printf 'EVIDENCE_GAP no structured generation trace found\n'
fi

printf 'INTEGRITY_FAILURE_COUNT: %d\n' "$failures"
if (( failures > 0 )); then
  exit 1
fi
