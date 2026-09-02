requires "../../reference/src/lemmas.k"

module DIGITSUM-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  // proof convenience
  syntax Expr ::= Val

  // the contribution of code C: C when it is an uppercase letter (65..90), else 0
  syntax Int ::= contrib(Int) [function, total]
  rule contrib(C:Int) => C
    requires C >=Int 65 andBool C <=Int 90 [simplification]
  rule contrib(C:Int) => 0
    requires notBool (C >=Int 65 andBool C <=Int 90) [simplification]

  // the sum of contributions over the char codes
  syntax Int ::= digSum(IntSeq) [function, total]
  rule digSum(.IntSeq) => 0 [simplification]
  rule digSum(iCons(C:Int, S:IntSeq)) => contrib(C) +Int digSum(S) [simplification]
endmodule
