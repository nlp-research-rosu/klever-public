// verification.k — summary for the match_parens proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module MATCH-PARENS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof-only: let a Val sit in expression position (so list(...) can be a Call arg).
  syntax Expr ::= Val

  // Balance fold of one string: val (+1 on '(' = 40, -1 otherwise) and a STICKY ok
  // (cleared whenever val goes negative — the inlined early `return False`). Both land in
  // the loop-invariant's scope map, so both are [total].
  syntax Int ::= balVal(IntSeq, Int) [function, total]
  rule balVal(.IntSeq, V:Int) => V [simplification]
  rule balVal(iCons(C:Int, S:IntSeq), V:Int) => balVal(S, V +Int 1) requires C ==Int 40  [simplification]
  rule balVal(iCons(C:Int, S:IntSeq), V:Int) => balVal(S, V -Int 1) requires C =/=Int 40  [simplification]

  // Split on (newV < 0) exactly like `if val < 0: ok = False` (else nothing).
  syntax Bool ::= balOk(IntSeq, Int, Bool) [function, total]
  rule balOk(.IntSeq, _V:Int, OK:Bool) => OK [simplification]
  rule balOk(iCons(C:Int, S:IntSeq), V:Int, OK:Bool) => balOk(S, V +Int 1, OK)
    requires C ==Int 40 andBool V +Int 1 >=Int 0 [simplification]
  rule balOk(iCons(C:Int, S:IntSeq), V:Int, _OK:Bool) => balOk(S, V +Int 1, false)
    requires C ==Int 40 andBool V +Int 1 <Int 0 [simplification]
  rule balOk(iCons(C:Int, S:IntSeq), V:Int, OK:Bool) => balOk(S, V -Int 1, OK)
    requires C =/=Int 40 andBool V -Int 1 >=Int 0 [simplification]
  rule balOk(iCons(C:Int, S:IntSeq), V:Int, _OK:Bool) => balOk(S, V -Int 1, false)
    requires C =/=Int 40 andBool V -Int 1 <Int 0 [simplification]

  // a string is balanceable iff it never goes negative and ends at 0.
  syntax Bool ::= checkBalance(IntSeq) [function, total]
  rule checkBalance(CS:IntSeq) => balOk(CS, 0, true) andBool (balVal(CS, 0) ==Int 0) [simplification]
endmodule
