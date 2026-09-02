#!/usr/bin/env bash
set -u
echo '$ pwd'
pwd
echo '$ env | grep "^AUDIT_MODE="'
env | grep '^AUDIT_MODE='
echo '$ sed -n "1,260p" /audit-input.json'
sed -n '1,260p' /audit-input.json
echo '$ find /reference -maxdepth 3 -mindepth 1 -printf "%y %p\n" | sort'
find /reference -maxdepth 3 -mindepth 1 -printf '%y %p\n' | sort
echo '$ find /candidate -maxdepth 4 -printf "%y %p\n" | sort'
find /candidate -maxdepth 4 -printf '%y %p\n' 2>/dev/null | sort
