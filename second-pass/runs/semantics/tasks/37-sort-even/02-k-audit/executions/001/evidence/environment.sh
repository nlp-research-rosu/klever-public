#!/usr/bin/env bash
set -u

echo '$ pwd'
pwd
echo "exit=$?"

echo '$ command -v kompile; kompile --version'
command -v kompile
kompile --version
echo "exit=$?"

echo '$ command -v kprove; kprove --version'
command -v kprove
kprove --version
echo "exit=$?"

echo '$ command -v krun; krun --version'
command -v krun
krun --version
echo "exit=$?"

echo '$ python3 --version'
python3 --version
echo "exit=$?"
