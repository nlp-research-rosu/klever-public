#!/usr/bin/env bash
set -uo pipefail

for file in \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k
do
  echo "FILE $file"
  rg -n \
    '^[[:space:]]*(requires|module|imports|syntax|configuration|rule|claim|endmodule)' \
    "$file"
done

echo "ATTRIBUTE INVENTORY"
rg -n '\[[^]]*(function|total|functional|simplification|concrete|priority|macro|strict|seqstrict|symbol)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k || true

echo "OPAQUE/FRESH SYMBOL SEARCH"
rg -n -i 'opaque|fresh|oracle|summary|uninterpreted|\\?[_A-Za-z]' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k || true
