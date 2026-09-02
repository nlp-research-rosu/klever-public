#!/usr/bin/env bash
set -euo pipefail

# Recreate the exact constructor term from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy
sha256sum solution.mpy | rg -q '^7d10644743b0d635231400e73ff58c5755e17dd09b7a73f64b79fd8fa0a12269  solution\.mpy$'

# Sanity-check the implementation under CPython.
python3 -c 'from solution import filter_by_prefix as f; assert f([], "a") == []; assert f(["abc", "bcd", "cde", "array"], "a") == ["abc", "array"]; assert f(["", "a", "aa", "b"], "") == ["", "a", "aa", "b"]; assert f(["a"], "aa") == []'

# Build the executable semantics together with its verification functions.
kompile semantic.k --backend haskell --main-module SEMANTIC --syntax-module VERIFICATION

# Exercise empty input, the prompt example, empty-prefix behavior, and a
# prefix longer than the candidate string.
krun solution.mpy --definition semantic-kompiled -cINPUT='nil' -cPREFIX='"a"'
krun solution.mpy --definition semantic-kompiled -cINPUT='cons("abc", cons("bcd", cons("cde", cons("array", nil))))' -cPREFIX='"a"'
krun solution.mpy --definition semantic-kompiled -cINPUT='cons("", cons("a", cons("aa", cons("b", nil))))' -cPREFIX='""'
krun solution.mpy --definition semantic-kompiled -cINPUT='cons("a", nil)' -cPREFIX='"aa"'

# Prove every claim in spec.k.  Success prints #Top and exits zero.
kprove spec.k --definition semantic-kompiled
