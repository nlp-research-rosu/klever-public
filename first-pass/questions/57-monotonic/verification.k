// verification.k — monotonic proof scaffolding + summaries, on the UNIFIED semantics.
// solution.py is the adjacent-compare fold (the canonical uses `l == sorted(l) or
// l == sorted(l, reverse=True)`; sort is not modelled — see ./PROOF.md). Symbolic input
// is the list `list(VS:ValSeq)`; the summaries fold VS, mirroring #135 can_arrange's
// projectIntTotal element compares.

requires "../../reference/src/lemmas.k"

module MONOTONIC-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position.
  syntax Expr ::= Val

  // ---- summary functions = the spec (differential-tested vs CPython: 0 / 300k) --------
  //
  // incFoldV(VS, IDX, PV, F) = the value of `inc` after folding VS from index IDX, previous
  // element PV (a raw Val), current flag F.  `inc` is a STICKY flag set False the first time
  // a DESCENT (x < prev) is seen at a valid position (i >= 1) — the program's nested If
  //   if i>=1: if x<prev: inc=False
  // The two vCons rules branch-split on (IDX>=1 andBool x<prev) so they line up one-to-one
  // with the loop (cf. ../NOTES.md sticky-flag rule; ../135-can-arrange for the ValSeq/
  // projectIntTotal fold shape).  [total]: exhaustive, lands in the scope map.
  syntax Bool ::= incFoldV(ValSeq, Int, Val, Bool) [function, total]
  rule incFoldV(.ValSeq, _:Int, _:Val, F:Bool) => F [simplification]
  rule incFoldV(vCons(V:Val, CS:ValSeq), IDX:Int, PV:Val, _F:Bool)
    => incFoldV(CS, IDX +Int 1, V, false)
    requires IDX >=Int 1 andBool projectIntTotal(V) <Int projectIntTotal(PV) [simplification]
  rule incFoldV(vCons(V:Val, CS:ValSeq), IDX:Int, PV:Val, F:Bool)
    => incFoldV(CS, IDX +Int 1, V, F)
    requires notBool (IDX >=Int 1 andBool projectIntTotal(V) <Int projectIntTotal(PV)) [simplification]

  // decFoldV(VS, IDX, PV, F) = the value of `dec`, the symmetric sticky flag set False the
  // first time an ASCENT (x > prev) is seen at a valid position (i >= 1) — the program's
  //   if i>=1: if x>prev: dec=False
  syntax Bool ::= decFoldV(ValSeq, Int, Val, Bool) [function, total]
  rule decFoldV(.ValSeq, _:Int, _:Val, F:Bool) => F [simplification]
  rule decFoldV(vCons(V:Val, CS:ValSeq), IDX:Int, PV:Val, _F:Bool)
    => decFoldV(CS, IDX +Int 1, V, false)
    requires IDX >=Int 1 andBool projectIntTotal(V) >Int projectIntTotal(PV) [simplification]
  rule decFoldV(vCons(V:Val, CS:ValSeq), IDX:Int, PV:Val, F:Bool)
    => decFoldV(CS, IDX +Int 1, V, F)
    requires notBool (IDX >=Int 1 andBool projectIntTotal(V) >Int projectIntTotal(PV)) [simplification]

  // prev accumulator: last element of VS (or PV if empty).
  syntax Val ::= lastOfV(ValSeq, Val) [function, total]
  rule lastOfV(.ValSeq, PV:Val)               => PV [simplification]
  rule lastOfV(vCons(V:Val, S:ValSeq), _:Val) => lastOfV(S, V) [simplification]

  // monotonicSpec(VS) = `inc or dec` = the function's result: VS is non-decreasing OR
  // non-increasing (i.e. l == sorted(l) or l == sorted(l, reverse=True)).  STRICT orBool of
  // the two sticky-flag summaries (evaluate both, combine — don't case-split).
  syntax Bool ::= monotonicSpec(ValSeq) [function, total]
  rule monotonicSpec(VS:ValSeq)
    => incFoldV(VS, 0, 0, true) orBool decFoldV(VS, 0, 0, true) [simplification]
endmodule
