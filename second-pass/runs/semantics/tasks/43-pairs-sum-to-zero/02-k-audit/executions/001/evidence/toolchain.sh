#!/usr/bin/env bash
set +e

export PATH="$HOME/.nix-profile/bin:$PATH"
echo '$ command -v kup'
command -v kup
echo "exit=$?"
echo '$ command -v kompile'
command -v kompile
echo "exit=$?"
echo '$ command -v kprove'
command -v kprove
echo "exit=$?"
echo '$ command -v krun'
command -v krun
echo "exit=$?"
echo '$ kompile --version'
kompile --version
echo "exit=$?"
echo '$ kprove --version'
kprove --version
echo "exit=$?"
