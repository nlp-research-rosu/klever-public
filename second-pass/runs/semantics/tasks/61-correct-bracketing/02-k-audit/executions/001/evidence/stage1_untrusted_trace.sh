#!/usr/bin/env bash
set +e

archive=/candidate/kore-exec.tar.gz
trace_dir=/tmp/audit-work/untrusted-trace

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS=%d\n' "$rc"
  return "$rc"
}

printf 'UNTRUSTED CANDIDATE TRACE INSPECTION (NEVER EXECUTED)\n'
run stat -c '%F %s bytes %n' "$archive"
run sha256sum "$archive"
run tar -tzf "$archive"
mkdir -p "$trace_dir"
run tar -xzf "$archive" -C "$trace_dir"
run wc -l -c \
  "$trace_dir/spec.kore" \
  "$trace_dir/kore-exec.sh" \
  "$trace_dir/vdefinition.kore" \
  "$trace_dir/kore-exec.log" \
  "$trace_dir/error.log"
run sed -n 1,120p "$trace_dir/kore-exec.sh"
run sed -n 1,160p "$trace_dir/kore-exec.log"
run sed -n 1,160p "$trace_dir/error.log"
run tail -n 80 "$trace_dir/kore-exec.log"
run tail -n 80 "$trace_dir/error.log"
run rg -n '#Top|WarnStuckClaimState|ErrorException|backend terminated' \
  "$trace_dir/kore-exec.log" "$trace_dir/error.log"
