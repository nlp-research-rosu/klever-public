#!/usr/bin/env bash
set -u

docs=/usr/include/kframework/builtin/domains.md
printf '%s\n' '$ sed -n 1678,1762p /usr/include/kframework/builtin/domains.md'
sed -n '1678,1762p' "$docs"
printf '[exit %d]\n' "$?"
