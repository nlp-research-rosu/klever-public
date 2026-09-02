#!/usr/bin/env bash
set -u

echo '$ python3 -m json.tool /audit-input.json'
python3 -m json.tool /audit-input.json
echo "EXIT: $?"

echo '$ python3 -m json.tool /audit-campaign-lock.json'
python3 -m json.tool /audit-campaign-lock.json
echo "EXIT: $?"

required=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/runtime-metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /candidate
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/reference-semantics
  /generation-evidence/codex-trace
)

echo '$ stat -c "%F|%n|%s" <pipeline-v3 required paths>'
for path in "${required[@]}"; do
  if [[ -e "$path" || -L "$path" ]]; then
    stat -c '%F|%n|%s' "$path"
  else
    echo "MISSING|$path"
  fi
done
echo 'EXIT: 0'

echo '$ sha256sum <launcher-declared regular files>'
sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py
echo "EXIT: $?"

echo '$ cmp -s /candidate/prompt.py /reference/prompt.py'
cmp -s /candidate/prompt.py /reference/prompt.py
echo "EXIT: $?"

echo '$ cmp -s /candidate/py2mpy.py /reference/py2mpy.py'
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
echo "EXIT: $?"

echo '$ find /candidate/reference-semantics /reference/reference-semantics -type l -print'
find /candidate/reference-semantics /reference/reference-semantics -type l -print
echo "EXIT: $?"

echo '$ diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics'
diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
echo "EXIT: $?"

echo '$ find /candidate/reference-semantics /reference/reference-semantics -printf "%y|%P\\n" | sort | sha256sum'
for root in /candidate/reference-semantics /reference/reference-semantics; do
  (
    cd "$root" &&
    find . -printf '%y|%P\n' | LC_ALL=C sort
  ) | sha256sum
done
echo "EXIT: $?"

echo '$ find /candidate -type l -print'
find /candidate -type l -print
echo "EXIT: $?"

echo '$ python3 <campaign/manifest/hash/trace integrity checks>'
python3 - <<'PY'
import collections
import hashlib
import json
import os
from pathlib import Path

audit = json.loads(Path('/audit-input.json').read_text())
lock_bytes = Path('/audit-campaign-lock.json').read_bytes()
lock = json.loads(lock_bytes)

print('record_layout:', audit.get('record_layout'))
print('semantics_mode:', audit.get('semantics_mode'))
print('reference_semantics_present:', Path('/reference/reference-semantics').is_dir())
print('campaign_json_equal:', lock == audit.get('audit_campaign'))
print('campaign_sha256:', hashlib.sha256(lock_bytes).hexdigest())
print('campaign_sha256_recorded:', audit['hashes']['audit_campaign_lock_sha256'])

checks = {
    'run_manifest_sha256': '/run.json',
    'task_manifest_sha256': '/task.json',
    'stage1_result_sha256': '/generation-result.json',
    'stage1_invocation_sha256': '/generation-evidence/invocation.json',
    'generation_metrics_sha256': '/generation-evidence/metrics.json',
    'generation_runtime_metrics_sha256': '/generation-evidence/runtime-metrics.json',
    'generation_usage_sha256': '/generation-evidence/usage.json',
    'generation_codex_last_sha256': '/generation-evidence/codex-last.txt',
    'generation_codex_output_sha256': '/generation-evidence/codex-output.log',
    'generation_prompt_sha256': '/generation-evidence/prompt.txt',
    'canonical_sha256': '/reference/canonical.py',
    'trusted_prompt_sha256': '/reference/prompt.py',
    'candidate_prompt_sha256': '/candidate/prompt.py',
    'trusted_translator_sha256': '/reference/py2mpy.py',
    'candidate_translator_sha256': '/candidate/py2mpy.py',
}
for key, name in checks.items():
    actual = hashlib.sha256(Path(name).read_bytes()).hexdigest()
    recorded = audit['hashes'].get(key)
    print(f'{key}: actual={actual} recorded={recorded} match={actual == recorded}')

run = json.loads(Path('/run.json').read_text())
task = json.loads(Path('/task.json').read_text())
result = json.loads(Path('/generation-result.json').read_text())
invocation = json.loads(Path('/generation-evidence/invocation.json').read_text())
print('task_equals_audit_manifest:', task == audit.get('manifest'))
print('run_config_matches:', run.get('config') == audit.get('config'))
print('run_condition_matches:', run.get('condition') == audit['manifest'].get('condition'))
print('run_contains_problem:', audit.get('problem_id') in run.get('tasks', []))
print('result_invocation_matches:', result.get('invocation') == invocation.get('name'))
print('result_stage_matches:', result.get('stage') == task.get('current_stage'))

def stable_tree_digest(root_name):
    root = Path(root_name)
    digest = hashlib.sha256()
    entries = sorted(root.rglob('*'), key=lambda p: p.relative_to(root).as_posix())
    for entry in entries:
        relative = entry.relative_to(root).as_posix()
        if entry.is_symlink():
            kind = b'L'
            payload = os.readlink(entry).encode()
        elif entry.is_dir():
            kind = b'D'
            payload = b''
        elif entry.is_file():
            kind = b'F'
            payload = entry.read_bytes()
        else:
            kind = b'O'
            payload = b''
        digest.update(kind + b'\0' + relative.encode() + b'\0')
        digest.update(len(payload).to_bytes(8, 'big'))
        digest.update(payload)
    return digest.hexdigest(), len(entries)

for root_name in [
    '/candidate',
    '/candidate/reference-semantics',
    '/reference/reference-semantics',
    '/generation-evidence/codex-trace',
]:
    tree_digest, entry_count = stable_tree_digest(root_name)
    print(f'independent_tree_sha256: root={root_name} entries={entry_count} sha256={tree_digest}')

trace_root = Path('/generation-evidence/codex-trace')
trace_files = sorted(p for p in trace_root.rglob('*') if p.is_file())
print('trace_file_count:', len(trace_files))
result_trace = result['outputs']['evidence']
for path in trace_files:
    rel = path.relative_to('/generation-evidence').as_posix()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f'trace: {rel} sha256={digest} recorded={result_trace.get(rel)} match={digest == result_trace.get(rel)}')
    counts = collections.Counter()
    records = 0
    with path.open(encoding='utf-8') as stream:
        for line_number, line in enumerate(stream, 1):
            obj = json.loads(line)
            records += 1
            counts[str(obj.get('type', '<missing>'))] += 1
    print(f'trace_jsonl_valid: records={records} top_level_types={dict(counts)}')
PY
echo "EXIT: $?"
