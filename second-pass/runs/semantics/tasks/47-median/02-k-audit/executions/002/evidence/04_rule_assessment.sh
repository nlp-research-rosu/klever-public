#!/usr/bin/env bash
set -uo pipefail

assessment=/audit-output/evidence/04_rule_assessment.txt
echo "COMMAND python3 /audit-output/evidence/04_rule_assessment.py > $assessment"
python3 /audit-output/evidence/04_rule_assessment.py > "$assessment"
assessment_status=$?
echo "ASSESSMENT_EXIT=$assessment_status"

echo "COMMAND sed -n '1,/ASSESSMENTS_BEGIN/p' $assessment"
sed -n '1,/ASSESSMENTS_BEGIN/p' "$assessment"
summary_status=$?
echo "SUMMARY_READ_EXIT=$summary_status"

echo "COMMAND sha256sum $assessment"
sha256sum "$assessment"
hash_status=$?
echo "SHA256_EXIT=$hash_status"

if [[ $assessment_status -eq 0 && $summary_status -eq 0 && $hash_status -eq 0 ]]; then
  exit 0
fi
exit 1
