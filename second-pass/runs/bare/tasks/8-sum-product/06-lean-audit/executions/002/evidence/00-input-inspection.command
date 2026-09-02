pwd
printf 'AUDIT_MODE=%s\n' "${AUDIT_MODE-<unset>}"
sha256sum /audit-input.json /reference/lemma-discovery.json /reference/klean-toolchain.lock.json
python3 -m json.tool /audit-input.json
printf '\nTRUSTED TOOLS\n'
rg --files /reference/tools | sort
printf '\nSTAGE 1 FILES\n'
rg --files /reference/k-proof | sort
printf '\nSTAGE 2 FILES\n'
rg --files /reference/k-audit | sort
printf '\nSTAGE 3 FILES\n'
rg --files /reference | rg 'lemma-discovery\.json$'
printf '\nSTAGE 4 FILES\n'
rg --files /reference/klean-generation | sort
printf '\nSTAGE 5 FILES\n'
if test -d /candidate; then rg --files /candidate | sort; else printf '<absent>\n'; fi
