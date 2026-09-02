#!/usr/bin/env bash
set -u
set -o pipefail

overall=0

check_file() {
  local path="$1"
  if [[ -f "$path" && -r "$path" && ! -L "$path" ]]; then
    printf 'OK regular-readable %s\n' "$path"
  else
    printf 'BAD required-file %s\n' "$path"
    overall=1
  fi
}

check_hash() {
  local expected="$1"
  local path="$2"
  local actual
  actual="$(sha256sum "$path" | awk '{print $1}')"
  if [[ "$actual" == "$expected" ]]; then
    printf 'OK sha256 %s %s\n' "$actual" "$path"
  else
    printf 'BAD sha256 expected=%s actual=%s %s\n' "$expected" "$actual" "$path"
    overall=1
  fi
}

printf 'Declared layout and mode\n'
python3 -c 'import json; d=json.load(open("/audit-input.json")); print(d["record_layout"]); print(d["semantics_mode"]); print(d["condition"]); print(d["problem_id"])'

required=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
)
for path in "${required[@]}"; do
  check_file "$path"
done

if [[ -d /generation-evidence/codex-trace && ! -L /generation-evidence/codex-trace ]]; then
  printf 'OK trace-directory /generation-evidence/codex-trace\n'
else
  printf 'BAD trace-directory /generation-evidence/codex-trace\n'
  overall=1
fi

if [[ -d /reference/reference-semantics && ! -L /reference/reference-semantics ]]; then
  printf 'OK supplied-semantics mount present\n'
else
  printf 'BAD supplied-semantics mount absent-or-symlinked\n'
  overall=1
fi

printf 'Campaign block comparison\n'
if python3 -c 'import json,sys; a=json.load(open("/audit-input.json"))["audit_campaign"]; b=json.load(open("/audit-campaign-lock.json")); sys.exit(0 if a == b else 1)'; then
  printf 'OK campaign block equals lock\n'
else
  printf 'BAD campaign block differs from lock\n'
  overall=1
fi

printf 'Declared individual hashes\n'
check_hash ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745 /audit-campaign-lock.json
check_hash 9690482d345e93d4b2789571770686de5547be7bba1ade3d325e6a1428923e15 /reference/canonical.py
check_hash 388474ac71e5b893802f5971102df2e4ea82ddf2f916a4a55361c19370f54012 /reference/prompt.py
check_hash 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /reference/py2mpy.py
check_hash 321818dc4f5c9795e25ea800ab12c1b1e5cf0bcc70b308443b9f08339a122db0 /run.json
check_hash 3bc98cf0ea750daf3178d3da4b74188232e76cc1a9dbb1bdd021c5b7e4932ecb /task.json
check_hash d577093b0aac2a47705def6d52fb26a770430dd819dd36a7bd2a592e00a5dec9 /generation-result.json
check_hash b645be834ea0aa4fdabdefde59dd96a0f1cd9380ac22df92e9ff720cf289014f /generation-evidence/invocation.json
check_hash e9c2f349ff9a8ef5dc550c3600aa75abcb8c2a8ea18563bd7b5022742cdb0d87 /generation-evidence/metrics.json
check_hash d81af044dfe2ec704f0e89313f2a222aed787f16175a55eb28d5fe23c888f21b /generation-evidence/usage.json
check_hash 52e3083c794a482aa9eb1c17c65d371cb938d873d4d03a143b079c5df1a3b101 /generation-evidence/codex-last.txt
check_hash d0153862576d4bfd638dea177f4697c785436de582aa525c047f5104078336bf /generation-evidence/codex-output.log
check_hash 3ccfe05a1e1620ec7e34cf354de6eeb973da0fe27a12a04f4ac62b0a78eeec09 /generation-evidence/prompt.txt

trace_file=/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T20-43-37-019f8ca4-7aa5-7871-bd85-ac5b2bfa206b.jsonl
check_file "$trace_file"
check_hash 3e160f9de83d5a1119a80b778ffa8ac54530516c956855bb2f725a3f274b4e14 "$trace_file"

printf 'Candidate trusted-artifact comparisons\n'
for pair in \
  '/candidate/prompt.py /reference/prompt.py' \
  '/candidate/py2mpy.py /reference/py2mpy.py'
do
  read -r left right <<<"$pair"
  if cmp -s "$left" "$right"; then
    printf 'OK byte-identical %s %s\n' "$left" "$right"
  else
    printf 'BAD content-difference %s %s\n' "$left" "$right"
    overall=1
  fi
done

if find /candidate/reference-semantics /reference/reference-semantics -type l -print -quit | grep -q .; then
  printf 'BAD symlink in semantics trees\n'
  find /candidate/reference-semantics /reference/reference-semantics -type l -printf '%p -> %l\n'
  overall=1
else
  printf 'OK no symlinks in semantics trees\n'
fi

if diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics; then
  printf 'OK candidate semantics recursively byte-identical to trusted semantics\n'
else
  printf 'BAD candidate semantics differs from trusted semantics\n'
  overall=1
fi

printf 'Required candidate proof artifacts\n'
for path in \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/spec.k \
  /candidate/verification.k \
  /candidate/prove.sh
do
  check_file "$path"
done

printf 'Structured trace validation and event counts\n'
if python3 -c 'import json,sys; [json.loads(line) for line in open(sys.argv[1], encoding="utf-8")]' "$trace_file"; then
  printf 'OK every trace line is valid JSON\n'
  python3 -c 'import collections,json,sys; counts=collections.Counter(json.loads(line)["type"] for line in open(sys.argv[1], encoding="utf-8")); [print(counts[key], key) for key in sorted(counts)]' "$trace_file"
else
  printf 'BAD malformed structured trace\n'
  overall=1
fi

printf 'Independent mounted-file SHA-256 inventory\n'
find /candidate /reference /generation-evidence -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum

printf 'Symlink inventory for all mounted input trees\n'
symlinks="$(find /candidate /reference /generation-evidence -type l -printf '%p -> %l\n')"
if [[ -n "$symlinks" ]]; then
  printf '%s\n' "$symlinks"
else
  printf 'NONE\n'
fi

printf 'INTEGRITY_SCRIPT_STATUS=%d\n' "$overall"
exit "$overall"
