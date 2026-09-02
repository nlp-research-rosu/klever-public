#!/usr/bin/env bash
set +e

if (( $# != 2 )); then
  echo "usage: $0 DEFINITION SOLUTION_MPY" >&2
  exit 64
fi

probe_definition=$1
solution_mpy=$2
probe_root=$(cd -- "$(dirname -- "$0")/semantic-probes" && pwd)

printf '%s\n' 'PYTHON FLOOR-DIVISION REFERENCES'
python3 -c 'print("python(-3 // 2)=", -3 // 2); print("python(3 // -2)=", 3 // -2)'

for probe_name in \
  negative-dividend.mpy \
  negative-divisor.mpy \
  division-zero.mpy \
  unsupported-operator.mpy \
  unbound-name.mpy
do
  probe_path="$probe_root/$probe_name"
  printf 'COMMAND: krun %q --definition %q %q %q\n' \
    "$probe_path" "$probe_definition" '-cFUNCTION="probe"' '-cARG=0'
  krun "$probe_path" --definition "$probe_definition" \
    '-cFUNCTION="probe"' -cARG=0
  printf 'KRUN_EXIT_STATUS: %d\n' "$?"
done

printf 'COMMAND: krun %q --definition %q %q %q\n' \
  "$solution_mpy" "$probe_definition" '-cFUNCTION="other"' '-cARG=0'
krun "$solution_mpy" --definition "$probe_definition" \
  '-cFUNCTION="other"' -cARG=0
printf 'KRUN_EXIT_STATUS: %d\n' "$?"

exit 0
