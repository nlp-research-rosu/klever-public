#!/usr/bin/env bash
set -u

echo "== run-input.json (untrusted claim) =="
sed -n '1,220p' /candidate/run-input.json

echo "== metrics.json (untrusted claim) =="
sed -n '1,160p' /candidate/metrics.json

echo "== codex-last.txt (untrusted claim) =="
sed -n '1,160p' /candidate/codex-last.txt

echo "== codex-output.log bounded tail (untrusted claim) =="
wc -l -c /candidate/codex-output.log
tail -n 40 /candidate/codex-output.log

echo "== structured generation trace metadata and bounded tail (untrusted claim) =="
find /candidate/codex-trace -type f -printf '%F %s %p\n' | sort
wc -l -c /candidate/codex-trace/2026/07/23/*.jsonl
tail -n 3 /candidate/codex-trace/2026/07/23/*.jsonl

echo "== provenance artifact hashes =="
sha256sum /candidate/run-input.json /candidate/metrics.json \
          /candidate/codex-last.txt /candidate/codex-output.log \
          /candidate/codex-trace/2026/07/23/*.jsonl
