// verification.k — summary for the check_if_last_char_is_a_letter proof, UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module CHECK-LAST-LETTER-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position (so str(CS) can be a Call arg).
  syntax Expr ::= Val

  // Width-2 window the loop leaves (scope-map VALUES in the invariant → must be [total]).
  // lastOf(CS, LAST) = code of the last char of CS (LAST if empty).
  syntax Int ::= lastOf(IntSeq, Int) [function, total]
  rule lastOf(.IntSeq, LAST:Int)                 => LAST          [simplification]
  rule lastOf(iCons(C:Int, S:IntSeq), _LAST:Int) => lastOf(S, C)  [simplification]

  // prevOf(CS, LAST, PREV) = code of the second-to-last char (threading the prior `last`).
  syntax Int ::= prevOf(IntSeq, Int, Int) [function, total]
  rule prevOf(.IntSeq, _LAST:Int, PREV:Int)                 => PREV               [simplification]
  rule prevOf(iCons(C:Int, S:IntSeq), LAST:Int, _PREV:Int)  => prevOf(S, C, LAST) [simplification]
  // (length uses the reference `isLen`.)
endmodule
