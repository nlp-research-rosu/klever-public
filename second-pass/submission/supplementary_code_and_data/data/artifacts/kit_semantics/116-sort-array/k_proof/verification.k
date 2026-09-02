requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The source contract is over arbitrary finite lists of integers.
  syntax Bool ::= allIntVS(ValSeq) [function, total]
  rule allIntVS(.ValSeq) => true
  rule allIntVS(vCons(V:Val, VS:ValSeq))
    => isInt(V) andBool allIntVS(VS)

  // Mathematical name for the value computed by
  // bin(value).count("1").  The fixed semantics defines binCodes and cntSub.
  syntax Int ::= popcountAbs(Int) [function, total]
  rule popcountAbs(I:Int)
    => cntSub(binCodes(I), iCons(49, .IntSeq))
    requires I >=Int 0
  rule popcountAbs(I:Int)
    => cntSub(binCodes(0 -Int I), iCons(49, .IntSeq))
    requires I <Int 0
endmodule
