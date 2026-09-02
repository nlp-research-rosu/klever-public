// verification.k — summary for the all_prefixes proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module ALL-PREFIXES-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // prefixList(A, CS) = for each growing prefix of CS, the string str(A ++ prefix)
  // (the scan's `result` when `acc` currently holds A).
  syntax ValSeq ::= prefixList(IntSeq, IntSeq) [function, total]
  rule prefixList(_:IntSeq, .IntSeq) => .ValSeq [simplification]
  rule prefixList(A:IntSeq, iCons(C:Int, S:IntSeq))
    => vCons(str(seqConcat(A, iCons(C, .IntSeq))), prefixList(seqConcat(A, iCons(C, .IntSeq)), S)) [simplification]

endmodule
