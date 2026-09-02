requires "../../reference/src/lemmas.k"

module DECODE-SHIFT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // the decoded code: shift back 5 within the 26-letter alphabet at 97; decShift maps it
  syntax Int ::= dshift(Int) [function, total]
  rule dshift(C:Int) => (pyMod(C -Int 5 -Int 97, 26)) +Int 97 [simplification]

  syntax IntSeq ::= decShift(IntSeq) [function, total]
  rule decShift(.IntSeq) => .IntSeq [simplification]
  rule decShift(iCons(C:Int, S:IntSeq)) => iCons(dshift(C), decShift(S)) [simplification]

endmodule
