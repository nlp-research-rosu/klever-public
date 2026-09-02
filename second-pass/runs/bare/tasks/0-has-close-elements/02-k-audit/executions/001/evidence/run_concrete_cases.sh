#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/source
definition=/tmp/audit-work/build/semantic-kompiled
status=0

labels=(
  example_false
  example_true
  empty
  singleton
  strict_equal
  strict_just_above
  negative_threshold
  negative_rational_strict
  negative_rational_above
  pair_only_at_end
)
arguments=(
  'VList(VRat(10,10),VRat(20,10),VRat(30,10)),VRat(5,10)'
  'VList(VRat(10,10),VRat(28,10),VRat(30,10),VRat(40,10),VRat(50,10),VRat(20,10)),VRat(3,10)'
  'VList(),VInt(1)'
  'VList(VInt(1)),VInt(1)'
  'VList(VRat(10,10),VRat(15,10)),VRat(5,10)'
  'VList(VRat(10,10),VRat(15,10)),VRat(5000001,10000000)'
  'VList(VInt(1),VInt(1)),VInt(-1)'
  'VList(VRat(-1,2),VInt(0)),VRat(1,2)'
  'VList(VRat(-1,2),VInt(0)),VRat(5000001,10000000)'
  'VList(VInt(100),VInt(-100),VInt(5),VRat(21,4)),VRat(3,10)'
)
expected=(false true false false false true false false true true)

for index in "${!labels[@]}"; do
  label=${labels[$index]}
  log="/audit-output/evidence/stage3-krun-${label}.log"
  if ! /audit-output/evidence/run_logged.sh "$log" \
      krun solution.mpy --definition "$definition" \
      "-cARGS=${arguments[$index]}"; then
    status=1
  elif ! rg -q "VBool \\( ${expected[$index]} \\)" "$log"; then
    printf 'WRONG RESULT for %s: expected %s\n' "$label" "${expected[$index]}"
    status=1
  fi
done

exit "$status"
