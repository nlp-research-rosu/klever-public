#!/usr/bin/env bash
set -u

status=0

reviewer_tree_hash() {
  root="$1"
  digest="$(
    cd "$root" || exit 1
    find . -mindepth 1 -printf '%y\t%P\0' |
      sort -z |
      while IFS= read -r -d '' entry; do
        entry_type="${entry%%$'\t'*}"
        relative="${entry#*$'\t'}"
        printf '%s\0' "$entry"
        if [[ "$entry_type" == "f" ]]; then
          sha256sum -- "$relative" | cut -d' ' -f1 | tr -d '\n'
          printf '\0'
        elif [[ "$entry_type" == "l" ]]; then
          readlink -- "$relative"
          printf '\0'
        fi
      done |
      sha256sum |
      cut -d' ' -f1
  )"
  printf 'REVIEWER_TREE_MANIFEST_SHA256 %s=%s\n' "$root" "$digest"
}

require_regular() {
  path="$1"
  if [[ -f "$path" && ! -L "$path" && -r "$path" ]]; then
    printf 'REGULAR_READABLE %s=true\n' "$path"
  else
    printf 'REGULAR_READABLE %s=false\n' "$path"
    status=1
  fi
}

for required in \
  /audit-input.json \
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
  /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T00-33-15-019f97c3-7059-7723-a2dd-413798611f73.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh \
  /candidate/PROOF.md
do
  require_regular "$required"
done

check_hash() {
  expected="$1"
  path="$2"
  actual="$(sha256sum "$path" | cut -d' ' -f1)"
  printf 'SHA256 %s\n  expected=%s\n  actual=%s\n' "$path" "$expected" "$actual"
  if [[ "$actual" != "$expected" ]]; then
    status=1
  fi
}

check_hash ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745 /audit-campaign-lock.json
check_hash 29ddcf16e9e8bd48ad7a6129ecd5fc1abbc3770d4ab87d0ab4a638e16a6e317a /reference/canonical.py
check_hash 4d14ffd571dae1770eb5e26636b128c8520cee2173f2f4a592277c6cd094e644 /reference/prompt.py
check_hash 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /reference/py2mpy.py
check_hash 3b99df09203880c9a59a6dcfed87c41b60e6057ebf8720421e156f1e7517bd73 /run.json
check_hash 433d8d31355547654937b3de2ed5df874af941dc0490d4d3a721691a2aaaa84c /task.json
check_hash 4b4319e539faca1903632a079b7f7129dc4205422de7ac9c14dedd675c78b62c /generation-result.json
check_hash 5e6cb690f0fdf7c950f3305308d686fcdacbb144baef82a795130788484767a0 /generation-evidence/invocation.json
check_hash 7ed68eb5ee5d737a439f76ff443d52ae4fc6b4e92d1b3cf931879bc290a0178b /generation-evidence/metrics.json
check_hash 679833233d8cffd6a7aaeeaad0ab33b20ad546dc3dfb6942f6ce20995cd24625 /generation-evidence/runtime-metrics.json
check_hash 1224ac8404e3e4344a02cc476e533da36abf53e5e5e290898b6194c538e6c6ce /generation-evidence/usage.json
check_hash 1e1821dc3ea6981a1ec115b457c12e405df50bf3dba769174bf673028a4c08c2 /generation-evidence/codex-last.txt
check_hash 5a025c922857bca90526d6df1020c47d2512d62b89bc0079f7c239bcd5bb2496 /generation-evidence/codex-output.log
check_hash c5f7af5f994f1d98d2cb3ab967f88f74a437a6548277cceaf24481aba1cf31e5 /generation-evidence/prompt.txt
check_hash ed8a9e0ad00a6879aa99b9a0ef771ab4616220ecf71edc443958be9cac4169f9 /generation-evidence/codex-trace/2026/07/25/rollout-2026-07-25T00-33-15-019f97c3-7059-7723-a2dd-413798611f73.jsonl

cmp /candidate/prompt.py /reference/prompt.py
printf 'CMP candidate prompt vs trusted exit=%s\n' "$?"
cmp /candidate/py2mpy.py /reference/py2mpy.py
printf 'CMP candidate translator vs trusted exit=%s\n' "$?"
diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics
diff_status=$?
printf 'DIFF candidate supplied semantics vs trusted tree exit=%s\n' "$diff_status"
if [[ "$diff_status" -ne 0 ]]; then
  status=1
fi

special_entries="$(find /candidate/reference-semantics /reference/reference-semantics ! -type d ! -type f -print)"
printf 'SPECIAL_OR_SYMLINK_ENTRIES=%s\n' "${special_entries:-none}"
if [[ -n "$special_entries" ]]; then
  status=1
fi

perl -MJSON::PP -e '
  local $/;
  open my $af, "<", "/audit-input.json" or die $!;
  my $a = decode_json(<$af>);
  open my $lf, "<", "/audit-campaign-lock.json" or die $!;
  my $l = decode_json(<$lf>);
  my $j = JSON::PP->new->canonical(1);
  die "campaign block mismatch\n"
    unless $j->encode($a->{audit_campaign}) eq $j->encode($l);
  print "CAMPAIGN_BLOCK_MATCH=true\n";
'
campaign_status=$?
if [[ "$campaign_status" -ne 0 ]]; then
  status=1
fi

reviewer_tree_hash /candidate
reviewer_tree_hash /candidate/reference-semantics
reviewer_tree_hash /reference/reference-semantics
reviewer_tree_hash /generation-evidence/codex-trace

printf 'FINAL_STATUS=%s\n' "$status"
exit "$status"
