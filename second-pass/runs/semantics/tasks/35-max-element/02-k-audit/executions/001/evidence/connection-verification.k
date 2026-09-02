requires "reference-semantics/semantics.k"

module MAX-ELEMENT-CONNECTION-VERIFICATION
  imports MPY

  syntax Module ::= "connectionProgram" [function, total]
  rule connectionProgram
    => Module(
         FuncDef("max_element", Params("l"),
           Return(Call(Name("max"), Name("l")))))

  // Pure expansion to the supplied semantics' ordinary vCons representation.
  // This adds no operational #iterNext rule.
  syntax ValSeq ::= expandIntVals(IntSeq) [function, total]
  rule expandIntVals(.IntSeq) => .ValSeq
  rule expandIntVals(iCons(I:Int, R:IntSeq))
    => vCons(I, expandIntVals(R))

  syntax Int ::= connectionMaxOf(Int, IntSeq) [function, total]
  rule connectionMaxOf(M:Int, .IntSeq) => M
  rule connectionMaxOf(M:Int, iCons(I:Int, R:IntSeq))
    => connectionMaxOf(maxInt(M, I), R)
endmodule
