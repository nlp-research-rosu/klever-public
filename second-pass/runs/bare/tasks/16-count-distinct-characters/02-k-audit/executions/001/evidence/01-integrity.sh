#!/usr/bin/env bash
set +e

echo '$ test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics'
test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics
echo "exit=$?"

echo '$ find /reference -maxdepth 1 -mindepth 1 -printf "%f\t%y\t%l\n" | sort'
find /reference -maxdepth 1 -mindepth 1 -printf '%f\t%y\t%l\n' | sort
echo "exit=$?"

echo '$ find /candidate -maxdepth 1 -mindepth 1 -printf "%f\t%y\t%l\n" | sort'
find /candidate -maxdepth 1 -mindepth 1 -printf '%f\t%y\t%l\n' | sort
echo "exit=$?"

echo '$ cmp -s /reference/prompt.py /candidate/prompt.py'
cmp -s /reference/prompt.py /candidate/prompt.py
echo "exit=$?"

echo '$ cmp -s /reference/py2mpy.py /candidate/py2mpy.py'
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
echo "exit=$?"

echo '$ sha256sum trusted and candidate prompt/translator and candidate source artifacts'
sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
echo "exit=$?"

echo '$ find /candidate/codex-trace -type f -printf "%p\t%s bytes\n" | sort'
find /candidate/codex-trace -type f -printf '%p\t%s bytes\n' | sort
echo "exit=$?"

echo '$ command -v kompile; kompile --version; command -v kprove; kprove --version'
command -v kompile
kompile --version
command -v kprove
kprove --version
echo "exit=$?"
