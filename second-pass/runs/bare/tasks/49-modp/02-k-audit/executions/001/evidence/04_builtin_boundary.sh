#!/usr/bin/env bash
set -u

DOC=/usr/include/kframework/builtin/domains.md

printf '$ sha256sum %q\n' "$DOC"
sha256sum "$DOC"
printf '[exit %d]\n' "$?"

printf '\n$ sed -n 1193,1265p %q\n' "$DOC"
sed -n '1193,1265p' "$DOC"
printf '[exit %d]\n' "$?"

printf '\n$ rg -n %q %q\n' 'hook\\(INT\\.powmod\\)|INT\\.powmod' /usr/include/kframework
rg -n 'hook\(INT\.powmod\)|INT\.powmod' /usr/include/kframework
printf '[exit %d]\n' "$?"
