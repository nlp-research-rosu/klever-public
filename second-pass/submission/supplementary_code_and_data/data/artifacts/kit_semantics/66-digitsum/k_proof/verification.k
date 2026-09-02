requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical summary of the fixed semantics' ASCII string model.
  // The condition is exactly the one computed by one-character str.isupper().
  syntax Int ::= digitSumIS(IntSeq) [function, total]

  rule digitSumIS(.IntSeq) => 0
  rule digitSumIS(iCons(C:Int, REST:IntSeq))
    => (#if isUpperC(C) andBool notBool isLowerC(C)
        #then C
        #else 0
        #fi)
       +Int digitSumIS(REST)
endmodule
