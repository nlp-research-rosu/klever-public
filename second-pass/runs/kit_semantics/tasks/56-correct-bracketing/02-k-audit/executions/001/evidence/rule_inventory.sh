#!/usr/bin/env bash
set -u

roots=(
  /reference/reference-semantics/semantics.k
  /reference/reference-semantics/semantics
  /candidate/verification.k
  /candidate/spec.k
)

printf 'SOURCE FILES\n'
find "${roots[@]}" -type f -name '*.k' -print | sort

printf '\nDECLARATION COUNTS BY FILE\n'
for file in $(find "${roots[@]}" -type f -name '*.k' -print | sort); do
  modules="$(rg -c '^[[:space:]]*module[[:space:]]' "$file" || true)"
  syntax="$(rg -c '^[[:space:]]*syntax([[:space:]]|$)' "$file" || true)"
  rules="$(rg -c '^[[:space:]]*rule([[:space:]]|$)' "$file" || true)"
  claims="$(rg -c '^[[:space:]]*claim([[:space:]]|$)' "$file" || true)"
  configurations="$(rg -c '^[[:space:]]*configuration([[:space:]]|$)' "$file" || true)"
  contexts="$(rg -c '^[[:space:]]*context([[:space:]]|$)' "$file" || true)"
  printf '%s modules=%s syntax=%s rules=%s claims=%s configurations=%s contexts=%s\n' \
    "$file" "${modules:-0}" "${syntax:-0}" "${rules:-0}" "${claims:-0}" \
    "${configurations:-0}" "${contexts:-0}"
done

printf '\nEXHAUSTIVE DECLARATION STARTS\n'
rg -n \
  '^[[:space:]]*(module|endmodule|imports|requires|configuration|syntax|rule|claim|context|context alias|macro|alias)([[:space:]]|$)' \
  "${roots[@]}" | sort

printf '\nATTRIBUTES AND SPECIAL DECLARATIONS\n'
rg -n \
  '\[(function|total|functional|simplification|concrete|priority|priorities|owise|macro|alias|symbol|hook|anywhere|trusted)[^]]*\]|syntax priorities|syntax left|syntax right' \
  "${roots[@]}" | sort

printf '\nCANDIDATE PROOF-LOCAL INVENTORY\n'
rg -n \
  '^[[:space:]]*(syntax|rule|claim|configuration|context|macro|alias)([[:space:]]|$)|\[(function|total|functional|simplification|priority|owise|anywhere)[^]]*\]' \
  /candidate/verification.k /candidate/spec.k | sort
