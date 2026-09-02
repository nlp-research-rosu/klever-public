#!/usr/bin/env bash
set -u

program=/tmp/audit-work/candidate-src/solution.mpy
definition=/tmp/audit-work/candidate-src/proof-kompiled

run_case() {
  name=$1
  hex=$2
  karg=$3
  printf 'CASE=%s python_utf8_or_surrogatepass_hex=%s\n' "$name" "$hex"
  python3 - "$hex" <<'PY'
import sys
raw = bytes.fromhex(sys.argv[1])
value = raw.decode("utf-8", "surrogatepass")
result = value.swapcase()
print(f"python_input={value!r}")
print(f"python_output={result!r}")
print(
    "python_output_utf8_or_surrogatepass_hex="
    + result.encode("utf-8", "surrogatepass").hex()
)
PY
  printf '$ krun %q --definition %q %q\n' "$program" "$definition" "-cARG=$karg"
  krun "$program" --definition "$definition" "-cARG=$karg"
  rc=$?
  printf '[exit %d]\n' "$rc"
}

# U+00C3 followed by U+009F encodes as c3 83 c2 9f. This distinguishes the
# candidate's UTF-8 byte bridge from the two bytes c3 9f, which encode U+00DF.
run_case two-python-codepoints 'c383c29f' '"\xc3\x83\xc2\x9f"'

# Python permits lone surrogates in str. surrogatepass gives a reversible byte
# bridge; swapcase leaves this surrogate unchanged and the K semantics does too.
run_case lone-surrogate 'eda080' '"\xed\xa0\x80"'
