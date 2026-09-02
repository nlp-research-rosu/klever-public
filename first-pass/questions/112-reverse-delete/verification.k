// verification.k — summary for the reverse_delete proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module REVERSE-DELETE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // keptOf(CS, CC) = the chars of CS NOT in the delete-set CC (a filter). `C not in c` is
  // the reference substring `in`: notBool strContains(iCons(C,.IntSeq), CC).
  syntax IntSeq ::= keptOf(IntSeq, IntSeq) [function, total]
  rule keptOf(.IntSeq, _:IntSeq) => .IntSeq [simplification]
  rule keptOf(iCons(C:Int, S:IntSeq), CC:IntSeq) => iCons(C, keptOf(S, CC))
    requires notBool strContains(iCons(C, .IntSeq), CC) [simplification]
  rule keptOf(iCons(C:Int, S:IntSeq), CC:IntSeq) => keptOf(S, CC)
    requires strContains(iCons(C, .IntSeq), CC) [simplification]

  // revFilt(CS, CC, R) = reverse(keptOf(CS, CC)) prepended to R (the loop does rev = ch + rev).
  syntax IntSeq ::= revFilt(IntSeq, IntSeq, IntSeq) [function, total]
  rule revFilt(.IntSeq, _:IntSeq, R:IntSeq) => R [simplification]
  rule revFilt(iCons(C:Int, S:IntSeq), CC:IntSeq, R:IntSeq) => revFilt(S, CC, iCons(C, R))
    requires notBool strContains(iCons(C, .IntSeq), CC) [simplification]
  rule revFilt(iCons(C:Int, S:IntSeq), CC:IntSeq, R:IntSeq) => revFilt(S, CC, R)
    requires strContains(iCons(C, .IntSeq), CC) [simplification]

endmodule
