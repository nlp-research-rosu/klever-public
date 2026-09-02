#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: bash /audit-output/evidence/01-provenance-check.sh'

status=0
check() {
  description="$1"
  shift
  "$@"
  command_status=$?
  printf 'CHECK %-46s exit=%s\n' "$description" "$command_status"
  if [[ "$command_status" -ne 0 ]]; then
    status=1
  fi
}

printf 'record_layout='
perl -MJSON::PP -e '
  local $/;
  open my $fh, "<", "/audit-input.json" or die $!;
  my $a = decode_json(<$fh>);
  print $a->{record_layout}, "\n";
'

required_files=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
)
for artifact in "${required_files[@]}"; do
  check "regular, non-symlink: $artifact" test -f "$artifact"
  check "not symlink: $artifact" test ! -L "$artifact"
done
check "candidate is a real directory" test -d /candidate
check "candidate is not a symlink" test ! -L /candidate
check "trace is a real directory" test -d /generation-evidence/codex-trace
check "trace is not a symlink" test ! -L /generation-evidence/codex-trace
check "generated mode has no reference semantics" test ! -e /reference/reference-semantics
check "candidate prompt equals trusted prompt" cmp -s /candidate/prompt.py /reference/prompt.py
check "candidate translator equals trusted translator" cmp -s /candidate/py2mpy.py /reference/py2mpy.py

perl -MJSON::PP -e '
  local $/;
  open my $af, "<", "/audit-input.json" or die $!;
  my $a = decode_json(<$af>);
  open my $lf, "<", "/audit-campaign-lock.json" or die $!;
  my $l = decode_json(<$lf>);
  my $json = JSON::PP->new->canonical(1);
  exit($json->encode($a->{audit_campaign}) eq $json->encode($l) ? 0 : 1);
'
campaign_status=$?
printf 'CHECK %-46s exit=%s\n' "campaign block equals campaign lock" "$campaign_status"
if [[ "$campaign_status" -ne 0 ]]; then
  status=1
fi

printf 'SHA256_MOUNTED_FILES\n'
sha256sum \
  /audit-campaign-lock.json \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /reference/canonical.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/22/*.jsonl

printf 'CANDIDATE_ENTRY_TYPES_AND_HASHES\n'
find /candidate -mindepth 1 -maxdepth 1 -printf '%y %f -> %l\n' | sort
find /candidate -mindepth 1 -maxdepth 1 -type f -print0 |
  sort -z |
  xargs -0 sha256sum

printf 'TRACE_JSON_VALIDATION\n'
perl -MJSON::PP -ne 'decode_json($_); $count++; END { print "json_lines=$count\n" }' \
  /generation-evidence/codex-trace/2026/07/22/*.jsonl
trace_status=$?
printf 'CHECK %-46s exit=%s\n' "every structured trace line parses as JSON" "$trace_status"
if [[ "$trace_status" -ne 0 ]]; then
  status=1
fi

printf 'TRACE_AND_GENERATION_RECORD_COUNTS\n'
wc -l /generation-evidence/codex-trace/2026/07/22/*.jsonl \
  /generation-evidence/codex-output.log

printf 'PROVENANCE_STATUS=%s\n' "$status"
exit "$status"
