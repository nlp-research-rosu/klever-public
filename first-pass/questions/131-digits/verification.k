// verification.k — summary for the digits proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module DIGITS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // ---- digit-decomposition summaries = the spec (differential-tested vs CPython) ----
  // A digit char with code C has value (C - 48); it is ODD iff (C - 48) % 2 == 1, the
  // same floored-modInt parity test the body computes via `int(digit) % 2 == 1`.  Both
  // [function, total]: they thread through the loop-invariant scope (see ../NOTES.md on
  // scope-map values needing [total]).

  // allDigit(S) (every code is a digit 48..57) comes from the reference MPY-METHODS; it is
  // threaded through the loop invariant so `int(digit)`'s guard (48 <= C <= 57) fires on each
  // symbolic element. Echo its unfold as [simplification] so the head bound reaches the path.
  rule allDigit(iCons(C:Int, S:IntSeq)) => (C >=Int 48 andBool C <=Int 57) andBool allDigit(S) [simplification]

  // oddDigit(C): the digit code C is odd.
  syntax Bool ::= oddDigit(Int) [function, total]
  rule oddDigit(C:Int) => pyMod(C -Int 48, 2) ==Int 1 [simplification]

  // oddProd(S, P): running product P times the product of the ODD digit values in S.
  // Branch-split on oddDigit(C) — the same test the body's If branches on.
  syntax Int ::= oddProd(IntSeq, Int) [function, total]
  rule oddProd(.IntSeq, P:Int) => P [simplification]
  rule oddProd(iCons(C:Int, S:IntSeq), P:Int)
    => oddProd(S, P *Int (C -Int 48)) requires oddDigit(C)         [simplification]
  rule oddProd(iCons(C:Int, S:IntSeq), P:Int)
    => oddProd(S, P)                  requires notBool oddDigit(C) [simplification]

  // oddCnt(S, K): running count K plus the number of ODD digits in S.
  syntax Int ::= oddCnt(IntSeq, Int) [function, total]
  rule oddCnt(.IntSeq, K:Int) => K [simplification]
  rule oddCnt(iCons(C:Int, S:IntSeq), K:Int)
    => oddCnt(S, K +Int 1) requires oddDigit(C)         [simplification]
  rule oddCnt(iCons(C:Int, S:IntSeq), K:Int)
    => oddCnt(S, K)        requires notBool oddDigit(C) [simplification]
endmodule
