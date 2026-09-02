#!/usr/bin/env bash
set -u

integrity_fail=0

report_failure() {
  printf 'INTEGRITY_FAILURE: %s\n' "$1"
  integrity_fail=1
}

printf '%s\n' '== Candidate top-level and nested inventory =='
find /candidate -xdev -printf '%y %p -> %l\n' | LC_ALL=C sort

printf '%s\n' '== Trusted reference inventory =='
find /reference -xdev -printf '%y %p -> %l\n' | LC_ALL=C sort

printf '%s\n' '== Required provenance records =='
for audit_name in run-input.json metrics.json codex-last.txt codex-output.log; do
  audit_path="/candidate/$audit_name"
  if [[ ! -e "$audit_path" && ! -L "$audit_path" ]]; then
    report_failure "missing /candidate/$audit_name"
  elif [[ -L "$audit_path" ]]; then
    report_failure "symlinked /candidate/$audit_name"
  elif [[ ! -f "$audit_path" ]]; then
    report_failure "mistyped /candidate/$audit_name (not a regular file)"
  else
    printf 'PRESENT regular file: %s\n' "$audit_path"
  fi
done

printf '%s\n' '== Structured trace candidates, when present =='
find /candidate -xdev \( -iname '*trace*' -o -iname '*.jsonl' \) \
  -printf '%y %p -> %l\n' | LC_ALL=C sort

printf '%s\n' '== Required source artifacts and types =='
for audit_name in prompt.py py2mpy.py solution.py solution.mpy spec.k verification.k; do
  audit_path="/candidate/$audit_name"
  if [[ ! -e "$audit_path" && ! -L "$audit_path" ]]; then
    report_failure "missing /candidate/$audit_name"
  elif [[ -L "$audit_path" ]]; then
    report_failure "symlinked /candidate/$audit_name"
  elif [[ ! -f "$audit_path" ]]; then
    report_failure "mistyped /candidate/$audit_name (not a regular file)"
  else
    printf 'PRESENT regular file: %s\n' "$audit_path"
  fi
done

if [[ ! -e /candidate/reference-semantics && ! -L /candidate/reference-semantics ]]; then
  report_failure 'missing /candidate/reference-semantics'
elif [[ -L /candidate/reference-semantics ]]; then
  report_failure 'symlinked /candidate/reference-semantics'
elif [[ ! -d /candidate/reference-semantics ]]; then
  report_failure 'mistyped /candidate/reference-semantics (not a directory)'
fi

if [[ ! -e /reference/reference-semantics && ! -L /reference/reference-semantics ]]; then
  printf '%s\n' 'INFRASTRUCTURE_BREACH: supplied-semantics trusted tree is absent'
  exit 70
elif [[ -L /reference/reference-semantics || ! -d /reference/reference-semantics ]]; then
  printf '%s\n' 'INFRASTRUCTURE_BREACH: trusted reference-semantics is symlinked or mistyped'
  exit 70
fi

printf '%s\n' '== Trusted prompt and translator byte comparisons =='
for audit_name in prompt.py py2mpy.py; do
  if cmp -s "/candidate/$audit_name" "/reference/$audit_name"; then
    printf 'BYTE_IDENTICAL: candidate/%s reference/%s\n' "$audit_name" "$audit_name"
  else
    report_failure "candidate/$audit_name differs from reference/$audit_name"
    cmp -l "/candidate/$audit_name" "/reference/$audit_name" | head -n 20
  fi
done

printf '%s\n' '== Candidate supplied-semantics recursive integrity =='
if [[ -d /candidate/reference-semantics && ! -L /candidate/reference-semantics ]]; then
  while IFS= read -r audit_rel; do
    audit_ref="/reference/reference-semantics/$audit_rel"
    audit_cand="/candidate/reference-semantics/$audit_rel"
    if [[ ! -e "$audit_cand" && ! -L "$audit_cand" ]]; then
      report_failure "missing candidate/reference-semantics/$audit_rel"
      continue
    fi
    audit_ref_type=$(stat -c '%F' "$audit_ref")
    audit_cand_type=$(stat -c '%F' "$audit_cand")
    if [[ "$audit_cand_type" == 'symbolic link' ]]; then
      report_failure "symlinked candidate/reference-semantics/$audit_rel"
      continue
    fi
    if [[ "$audit_ref_type" != "$audit_cand_type" ]]; then
      report_failure "mistyped candidate/reference-semantics/$audit_rel ($audit_cand_type versus $audit_ref_type)"
      continue
    fi
    if [[ -f "$audit_ref" ]] && ! cmp -s "$audit_ref" "$audit_cand"; then
      report_failure "changed candidate/reference-semantics/$audit_rel"
    else
      printf 'MATCH: candidate/reference-semantics/%s (%s)\n' "$audit_rel" "$audit_cand_type"
    fi
  done < <(cd /reference/reference-semantics && find . -mindepth 1 -printf '%P\n' | LC_ALL=C sort)

  while IFS= read -r audit_rel; do
    if [[ ! -e "/reference/reference-semantics/$audit_rel" && ! -L "/reference/reference-semantics/$audit_rel" ]]; then
      report_failure "additional candidate/reference-semantics/$audit_rel"
    fi
  done < <(cd /candidate/reference-semantics && find . -mindepth 1 -printf '%P\n' | LC_ALL=C sort)
fi

printf '%s\n' '== Candidate symlink prohibition =='
audit_symlink_count=$(find /candidate -xdev -type l -print | tee /dev/stderr | wc -l)
if (( audit_symlink_count > 0 )); then
  report_failure "candidate contains $audit_symlink_count symlink(s)"
else
  printf '%s\n' 'NO_CANDIDATE_SYMLINKS'
fi

printf 'INTEGRITY_FAILURE_COUNTED: %d\n' "$integrity_fail"
exit "$integrity_fail"
