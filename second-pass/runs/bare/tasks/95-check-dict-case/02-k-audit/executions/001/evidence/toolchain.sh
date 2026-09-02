#!/usr/bin/env bash
set -u

command -v kompile
command -v kprove
command -v krun
kompile --version
kprove --version
krun --version
