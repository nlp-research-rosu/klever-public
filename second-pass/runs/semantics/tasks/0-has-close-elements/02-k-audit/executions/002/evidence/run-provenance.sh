#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/01-provenance.log
exec > >(tee "$LOG") 2>&1

run() {
  echo "\$ $*"
  "$@"
  local status=$?
  echo "[exit $status]"
  return 0
}

check_hash() {
  local expected=$1
  local path=$2
  local actual
  actual=$(sha256sum "$path" | cut -d' ' -f1)
  if [[ "$actual" == "$expected" ]]; then
    echo "HASH_OK $path $actual"
  else
    echo "HASH_MISMATCH $path expected=$expected actual=$actual"
  fi
}

echo "Declared layout: legacy-selected-stage1"
echo "Declared semantics mode: SUPPLIED_SEMANTICS"

required=(
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
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T20-31-25-019f8c99-51a5-7a12-811f-3c0052ef1541.jsonl
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
  /candidate
)
for path in "${required[@]}"; do
  run stat -c '%F %s %n' "$path"
done

echo '$ perl -MJSON::PP -e campaign comparison'
perl -MJSON::PP -0777 -e '
  my ($a,$l)=@ARGV;
  open my $af,"<",$a or die $!;
  open my $lf,"<",$l or die $!;
  my $aj=decode_json(do { local $/; <$af> });
  my $lj=decode_json(do { local $/; <$lf> });
  my $j=JSON::PP->new->canonical(1);
  my $same=$j->encode($aj->{audit_campaign}) eq $j->encode($lj);
  print "campaign_block_equal=",($same ? "yes" : "no"),"\n";
  exit($same ? 0 : 1);
' /audit-input.json /audit-campaign-lock.json
echo "[exit $?]"

check_hash ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745 /audit-campaign-lock.json
check_hash b19fa4b9ec23ba3f2deb06e3228d77cef75127023b2ef10b386b54df9da9c9d6 /reference/canonical.py
check_hash 00b2e074e127a6a9d1376278bef732933760ab706057ec755a8c2642217b557a /reference/prompt.py
check_hash 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /reference/py2mpy.py
check_hash 00b2e074e127a6a9d1376278bef732933760ab706057ec755a8c2642217b557a /candidate/prompt.py
check_hash 406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16 /candidate/py2mpy.py
check_hash 321818dc4f5c9795e25ea800ab12c1b1e5cf0bcc70b308443b9f08339a122db0 /run.json
check_hash d41d06bc9a209c7944d9421ac89d0799f2790a4b298118b3362db7f411e29d7d /task.json
check_hash a70aed06d8e32d7c529fa04685e65488a842c4050b2b4423581a06293848cb85 /generation-result.json
check_hash d8e7d34173ba1915874eef1afcbcf60984c2f8711334e27a2f798fe5e9fd8fb6 /generation-evidence/invocation.json
check_hash 525c6a986bdb3e8eb42efef449d04b3a7e396e8950b6104e611cb7ea0311eba3 /generation-evidence/metrics.json
check_hash dd41d25e7335ddeaf25f118cc8173208574672068107ee5ea46537b26785d45f /generation-evidence/usage.json
check_hash 0300ceb1c9a7a788e3349ec9a3210d22e65baacf5d732d41003dcdbfc440dd73 /generation-evidence/codex-last.txt
check_hash d0096d91ffffd02db5d9d9a7a9723ef38e95dc73022aaa845488d89f7b211600 /generation-evidence/codex-output.log
check_hash 3ccfe05a1e1620ec7e34cf354de6eeb973da0fe27a12a04f4ac62b0a78eeec09 /generation-evidence/prompt.txt
check_hash 24dbbf90cc78926b0af5c0015fd065ccab8805c77c448924d71aa9a009fa4377 /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T20-31-25-019f8c99-51a5-7a12-811f-3c0052ef1541.jsonl
check_hash fd71a796c2d98d069d6699aacd60575c8ebbc000874abb459887993d24efb659 /generation-evidence/legacy-metrics.json
check_hash de1adea23c39e1a8619475772a217f4814b16e0d09a0db7e571e8ff029c384ad /generation-evidence/legacy-run-input.json

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics

echo '$ find both semantics trees for non-regular entries'
find /candidate/reference-semantics /reference/reference-semantics \
  ! -type d ! -type f -printf '%y %p -> %l\n' | sort
echo "[exit ${PIPESTATUS[0]}]"

echo '$ diff sorted per-file SHA-256 manifests'
diff \
  <(cd /candidate/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum) \
  <(cd /reference/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum)
echo "[exit $?]"

echo '$ candidate/reference tree file manifests'
(cd /candidate/reference-semantics && find . -type f -print0 | sort -z | xargs -0 sha256sum)
echo "[exit ${PIPESTATUS[0]}]"

run perl /audit-output/evidence/inspect_generation.pl

echo '$ generation record excerpts'
sed -n '1,260p' /generation-evidence/invocation.json
sed -n '1,160p' /generation-evidence/metrics.json
sed -n '1,220p' /generation-evidence/usage.json
sed -n '1,160p' /generation-evidence/legacy-run-input.json
sed -n '1,160p' /generation-evidence/legacy-metrics.json
sed -n '1,160p' /generation-evidence/codex-last.txt
echo "[exit ${PIPESTATUS[0]}]"
