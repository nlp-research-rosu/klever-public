#!/usr/bin/env bash
set +e

echo '$ command -v kup'
command -v kup
echo "exit=$?"

echo '$ command -v kompile'
command -v kompile
echo "exit=$?"

echo '$ kompile --version'
kompile --version
echo "exit=$?"

echo '$ kprove --version'
kprove --version
echo "exit=$?"

echo '$ krun --version'
krun --version
echo "exit=$?"

echo '$ python3 --version'
python3 --version
echo "exit=$?"
