#!/usr/bin/env bash
set -euo pipefail

source=/tmp/audit-work/160-do-algebra/solution.mpy
output=/tmp/audit-work/160-do-algebra/audit-asserts.mpy

sed '$ s/)$//' "$source" >"$output"
printf '%s\n' \
  '  Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("+"), Str("*"), Str("-")), ListExpr(Int(2), Int(3), Int(4), Int(5))), CmpOp("==", Int(9))))' \
  '  Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("//"), Str("//")), ListExpr(Int(20), Int(3), Int(2))), CmpOp("==", Int(3))))' \
  '  Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("**"), Str("**")), ListExpr(Int(2), Int(3), Int(2))), CmpOp("==", Int(512))))' \
  '  Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("-"), Str("-")), ListExpr(Int(20), Int(6), Int(2))), CmpOp("==", Int(12))))' \
  '  Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("+")), ListExpr(Int(0), Int(0))), CmpOp("==", Int(0))))' \
  ')' >>"$output"

sha256sum "$output"
tail -n 9 "$output"
