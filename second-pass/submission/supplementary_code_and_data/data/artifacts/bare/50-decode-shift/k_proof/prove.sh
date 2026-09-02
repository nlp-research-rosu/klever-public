#!/bin/sh
set -eu

python3 py2mpy.py solution.py > solution.mpy
PYTHONDONTWRITEBYTECODE=1 python3 -c 'compile(open("solution.py", encoding="utf-8").read(), "solution.py", "exec")'
PYTHONDONTWRITEBYTECODE=1 python3 -c 'from prompt import encode_shift; from solution import decode_shift; samples = ["", "abc", "xyz", "helloworld", "abcdefghijklmnopqrstuvwxyz"]; assert all(decode_shift(encode_shift(s)) == s for s in samples)'
python3 -c 'from pathlib import Path; mpy = "".join(Path("solution.mpy").read_text().split()); spec = "".join(Path("spec.k").read_text().split()); assert mpy in spec, "spec.k does not contain the translated solution term"'

kompile semantic.k --backend haskell --syntax-module MPY-SYNTAX --main-module SEMANTIC

krun solution.mpy -cINPUT='nil'
krun solution.mpy -cINPUT='cons(102, cons(103, cons(104, nil)))'
krun solution.mpy -cINPUT='cons(101, cons(97, cons(98, cons(122, nil))))'

kprove spec.k --definition semantic-kompiled --spec-module SPEC
