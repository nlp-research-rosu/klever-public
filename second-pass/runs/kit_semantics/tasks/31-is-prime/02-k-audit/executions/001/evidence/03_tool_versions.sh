#!/usr/bin/env bash
set -u

for tool in kompile kprove krun kast; do
  echo "$ command -v $tool"
  command -v "$tool"
  echo "EXIT: $?"
  echo "$ $tool --version"
  "$tool" --version
  echo "EXIT: $?"
done
