#!/usr/bin/env bash
set -u

work_dir=/tmp/audit-work/reconstruction
cd "$work_dir" || exit 90

echo '$ cp /audit-output/evidence/spec-post-discrimination.k /tmp/audit-work/reconstruction/spec-post-discrimination.k'
cp /audit-output/evidence/spec-post-discrimination.k \
  /tmp/audit-work/reconstruction/spec-post-discrimination.k
echo "exit=$?"

for module in \
  POST-CORRECT-CONCRETE-SPEC \
  POST-WRONG-CONCRETE-SPEC \
  POST-ABSTRACT-TAG-SPEC
do
  echo "\$ kprove spec-post-discrimination.k --definition verification-kompiled --spec-module $module --output pretty"
  kprove spec-post-discrimination.k \
    --definition verification-kompiled \
    --spec-module "$module" \
    --output pretty
  echo "module=$module exit=$?"
done

# Individual statuses are the experiment's output, not a wrapper failure.
exit 0
