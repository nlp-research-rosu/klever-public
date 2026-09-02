// verification.k — summary for the string_xor proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module STRING-XOR-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // xorSeq(CA, CB) = per aligned pair, "0" (48) if the codes are equal, else "1" (49),
  // truncating to the shorter string.
  syntax IntSeq ::= xorSeq(IntSeq, IntSeq) [function, total]
  rule xorSeq(.IntSeq, _:IntSeq)              => .IntSeq [simplification]
  rule xorSeq(iCons(_:Int, _:IntSeq), .IntSeq) => .IntSeq [simplification]
  rule xorSeq(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))
    => iCons(48, xorSeq(As, Bs)) requires A  ==Int B [simplification]
  rule xorSeq(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq))
    => iCons(49, xorSeq(As, Bs)) requires A =/=Int B [simplification]

endmodule
