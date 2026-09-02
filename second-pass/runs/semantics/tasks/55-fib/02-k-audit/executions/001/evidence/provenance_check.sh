#!/usr/bin/env bash
set -u

candidate=/candidate
trusted=/reference
issues=0

check_regular() {
  local path=$1
  if [[ ! -e "$path" ]]; then
    printf 'MISSING: %s\n' "$path"
    issues=$((issues + 1))
  elif [[ -L "$path" ]]; then
    printf 'SYMLINKED: %s -> %s\n' "$path" "$(readlink "$path")"
    issues=$((issues + 1))
  elif [[ ! -f "$path" ]]; then
    printf 'MISTYPED: %s is not a regular file\n' "$path"
    issues=$((issues + 1))
  else
    printf 'REGULAR: %s sha256=%s\n' "$path" "$(sha256sum "$path" | awk '{print $1}')"
  fi
}

printf '%s\n' '== Required candidate proof artifacts =='
for name in solution.py solution.mpy spec.k verification.k prompt.py py2mpy.py; do
  check_regular "$candidate/$name"
done

printf '%s\n' '== Requested untrusted generation records =='
for name in run-input.json metrics.json codex-last.txt codex-output.log; do
  check_regular "$candidate/$name"
done

printf '%s\n' '== Structured trace candidates, if any =='
find -P "$candidate" -maxdepth 1 -type f \
  \( -iname '*trace*' -o -iname '*.jsonl' \) -printf '%f\n' | sort

printf '%s\n' '== Candidate prompt and translator identity =='
for name in prompt.py py2mpy.py; do
  if cmp -s "$candidate/$name" "$trusted/$name"; then
    printf 'IDENTICAL: candidate/%s == reference/%s\n' "$name" "$name"
  else
    printf 'CHANGED: candidate/%s != reference/%s\n' "$name" "$name"
    diff -u "$trusted/$name" "$candidate/$name" || true
    issues=$((issues + 1))
  fi
done

printf '%s\n' '== Supplied-semantics tree entry types =='
candidate_types=$(mktemp /tmp/55-fib-candidate-types.XXXXXX)
trusted_types=$(mktemp /tmp/55-fib-trusted-types.XXXXXX)
find -P "$candidate/reference-semantics" -mindepth 1 -printf '%y %P\n' | sort >"$candidate_types"
find -P "$trusted/reference-semantics" -mindepth 1 -printf '%y %P\n' | sort >"$trusted_types"
if cmp -s "$candidate_types" "$trusted_types"; then
  printf '%s\n' 'IDENTICAL_ENTRY_TYPES'
else
  printf '%s\n' 'ENTRY_TYPE_OR_PATH_MISMATCH'
  diff -u "$trusted_types" "$candidate_types" || true
  issues=$((issues + 1))
fi

printf '%s\n' '== Candidate/reference semantics symlinks =='
candidate_symlinks=$(find -P "$candidate/reference-semantics" -type l -print)
trusted_symlinks=$(find -P "$trusted/reference-semantics" -type l -print)
printf 'candidate_symlinks=%s\n' "${candidate_symlinks:-NONE}"
printf 'trusted_symlinks=%s\n' "${trusted_symlinks:-NONE}"
if [[ -n "$candidate_symlinks" ]]; then
  issues=$((issues + 1))
fi

printf '%s\n' '== Supplied-semantics byte comparison =='
while IFS= read -r rel; do
  if cmp -s "$candidate/reference-semantics/$rel" "$trusted/reference-semantics/$rel"; then
    printf 'IDENTICAL: %s\n' "$rel"
  else
    printf 'CHANGED: %s\n' "$rel"
    issues=$((issues + 1))
  fi
done < <(find -P "$trusted/reference-semantics" -type f -printf '%P\n' | sort)

rm -f "$candidate_types" "$trusted_types"
printf 'ISSUE_COUNT: %d\n' "$issues"
if (( issues > 0 )); then
  exit 1
fi
