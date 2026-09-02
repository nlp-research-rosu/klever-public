#!/usr/bin/env bash
set -uo pipefail

trace=/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T05-31-28-019f8961-631d-72a0-bc03-eab6305b691d.jsonl

echo '$ sha256sum <launcher-declared files>'
sha256sum \
  /audit-campaign-lock.json \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/legacy-metrics.json \
  /generation-evidence/legacy-run-input.json \
  "$trace"
echo "sha256sum exit=$?"

echo '$ cmp candidate prompt/translator against trusted mounts'
cmp -s /candidate/prompt.py /reference/prompt.py
echo "prompt cmp exit=$?"
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
echo "translator cmp exit=$?"

echo '$ require generated-semantics boundary'
test ! -e /reference/reference-semantics
echo "trusted reference-semantics absent exit=$?"
test ! -e /candidate/reference-semantics
echo "candidate reference-semantics absent exit=$?"

echo '$ require regular candidate and provenance entries (no symlinks)'
find -P /candidate /generation-evidence /reference -type l -print
test -z "$(find -P /candidate /generation-evidence /reference -type l -print -quit)"
echo "no symlinks exit=$?"

echo '$ validate all structured trace lines as JSON'
perl -MJSON::PP -ne '
  next unless /\S/;
  $lines++;
  eval { decode_json($_) };
  $bad++ if $@;
  END {
    print "trace_lines=$lines malformed=" . ($bad // 0) . "\n";
    exit(($bad // 0) == 0 ? 0 : 1);
  }
' "$trace"
echo "trace JSON validation exit=$?"

echo '$ compare audit_campaign block with campaign lock'
perl -MJSON::PP -0777 -e '
  sub loadj {
    my ($path) = @_;
    open my $stream, "<", $path or die "$path: $!";
    local $/;
    return decode_json(<$stream>);
  }
  my $audit = loadj("/audit-input.json");
  my $lock = loadj("/audit-campaign-lock.json");
  my $json = JSON::PP->new->canonical;
  my $same = $json->encode($audit->{audit_campaign}) eq $json->encode($lock);
  print $same ? "campaign lock MATCH\n" : "campaign lock MISMATCH\n";
  exit($same ? 0 : 1);
'
echo "campaign comparison exit=$?"

echo '$ pipeline_contract.sha256_tree on mounted candidate and trace trees'
PYTHONPATH=/opt/humaneval/tools python3 - <<'PY'
from pathlib import Path
from pipeline_contract import sha256_tree

print(f"candidate_pipeline_tree_sha256={sha256_tree(Path('/candidate'))}")
print(
    "trace_pipeline_tree_sha256="
    f"{sha256_tree(Path('/generation-evidence/codex-trace'))}"
)
PY
echo "pipeline tree hashing exit=$?"
