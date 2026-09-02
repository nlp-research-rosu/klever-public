#!/usr/bin/env bash
set -u

fixed=/audit-output/evidence/stage3_krun_concrete.log
extended=/audit-output/evidence/stage5_krun_with_bridges.log

extract() {
  sed -n '/^<generatedTop>/,/^<\/generatedTop>/p' "$1"
}

echo '$ diff fixed-semantics-final-configuration bridge-enabled-final-configuration'
diff <(extract "$fixed") <(extract "$extended")
status=$?
echo "exit=$status"

echo '$ final-configuration hashes'
extract "$fixed" | sha256sum
extract "$extended" | sha256sum

exit "$status"
