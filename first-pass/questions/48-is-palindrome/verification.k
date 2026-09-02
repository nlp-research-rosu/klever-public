requires "../../reference/src/lemmas.k"

module IS-PALINDROME-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // the mirrored-index scan: true iff text[j] == text[len-1-j] for every j in [I, len).
  // Case-split rules (compare in the GUARDS): intSeqAt is partial, so it may not sit in a RHS.
  syntax Bool ::= palFrom(IntSeq, Int) [function, total]
  rule palFrom(CS:IntSeq, I:Int) => true requires I >=Int isLen(CS) [simplification]
  rule palFrom(CS:IntSeq, I:Int) => palFrom(CS, I +Int 1)
    requires 0 <=Int I andBool I <Int isLen(CS)
     andBool intSeqAt(CS, I) ==Int intSeqAt(CS, isLen(CS) -Int 1 -Int I)
    [simplification]
  rule palFrom(CS:IntSeq, I:Int) => false
    requires 0 <=Int I andBool I <Int isLen(CS)
     andBool notBool (intSeqAt(CS, I) ==Int intSeqAt(CS, isLen(CS) -Int 1 -Int I))
    [simplification]
endmodule
