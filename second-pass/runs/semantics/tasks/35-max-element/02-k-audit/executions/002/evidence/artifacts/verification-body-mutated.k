requires "reference-semantics/semantics.k"

module MAX-ELEMENT-VERIFICATION-BODY-MUTATED
  imports MPY

  syntax Module ::= "maxElementProgramMutated" [function, total]
  rule maxElementProgramMutated
    => Module(
         FuncDef("max_element", Params("l"),
           Return(Int(0))))

  syntax ValSeq ::= intValsMutated(IntSeq)

  syntax Int ::= maxOfMutated(Int, IntSeq) [function, total]
  rule maxOfMutated(M:Int, .IntSeq)                => M
  rule maxOfMutated(M:Int, iCons(I:Int, R:IntSeq)) => maxOfMutated(maxInt(M, I), R)

  rule <k> #iterNext(list(intValsMutated(.IntSeq)))
        => #iterDone ... </k>
       [priority(40)]
  rule <k> #iterNext(list(intValsMutated(iCons(I:Int, R:IntSeq))))
        => #iterYield(I, list(intValsMutated(R))) ... </k>
       [priority(40)]
endmodule
