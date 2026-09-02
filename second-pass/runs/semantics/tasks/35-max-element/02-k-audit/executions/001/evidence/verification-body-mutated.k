requires "reference-semantics/semantics.k"

module MAX-ELEMENT-VERIFICATION-BODY-MUTATED
  imports MPY

  // Reviewer mutation: return the first element instead of calling max.
  syntax Module ::= "mutatedMaxElementProgram" [function, total]
  rule mutatedMaxElementProgram
    => Module(
         FuncDef("max_element", Params("l"),
           Return(Subscript(Name("l"), Int(0)))))

  syntax ValSeq ::= mutatedIntVals(IntSeq)

  rule <k> #iterNext(list(mutatedIntVals(.IntSeq)))
        => #iterDone ... </k>
       [priority(40)]
  rule <k> #iterNext(list(mutatedIntVals(iCons(I:Int, R:IntSeq))))
        => #iterYield(I, list(mutatedIntVals(R))) ... </k>
       [priority(40)]
endmodule
