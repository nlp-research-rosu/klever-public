#!/usr/bin/env bash
set -uo pipefail

echo '$ find /candidate -type f -print0 | sort -z | xargs -0 sha256sum > /audit-output/evidence/candidate_file_sha256.txt'
find /candidate -type f -print0 | sort -z | xargs -0 sha256sum \
  > /audit-output/evidence/candidate_file_sha256.txt
candidate_status=$?
echo "EXIT_STATUS: ${candidate_status}"

echo '$ find /reference/reference-semantics -type f -print0 | sort -z | xargs -0 sha256sum > /audit-output/evidence/trusted_semantics_file_sha256.txt'
find /reference/reference-semantics -type f -print0 | sort -z | xargs -0 sha256sum \
  > /audit-output/evidence/trusted_semantics_file_sha256.txt
semantics_status=$?
echo "EXIT_STATUS: ${semantics_status}"

echo '$ sha256sum /audit-output/evidence/candidate_file_sha256.txt /audit-output/evidence/trusted_semantics_file_sha256.txt'
sha256sum /audit-output/evidence/candidate_file_sha256.txt \
  /audit-output/evidence/trusted_semantics_file_sha256.txt
manifest_status=$?
echo "EXIT_STATUS: ${manifest_status}"

echo '$ wc -l /audit-output/evidence/candidate_file_sha256.txt /audit-output/evidence/trusted_semantics_file_sha256.txt'
wc -l /audit-output/evidence/candidate_file_sha256.txt \
  /audit-output/evidence/trusted_semantics_file_sha256.txt
count_status=$?
echo "EXIT_STATUS: ${count_status}"

echo 'launcher_recorded_candidate_tree_sha256=b866f9ef45451e9d3eca906140abf701b73c487647dd7c9676cd38c3f020b9af'
echo 'launcher_recorded_candidate_reference_semantics_sha256=1de6d5f51876cf9d0f4449a78f077f8b127a14add0504d5060da680fc5a443de'
