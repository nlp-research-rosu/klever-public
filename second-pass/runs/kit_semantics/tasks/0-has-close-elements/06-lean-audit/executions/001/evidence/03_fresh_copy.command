audit_tmp=/tmp/audit-work/proof-audit.2wTFR1
cp -a /reference/klean-generation/generated "$audit_tmp/Base"
cp -a /candidate/. "$audit_tmp/"
find "$audit_tmp" -maxdepth 2 -type f -printf '%P\n' | sort
