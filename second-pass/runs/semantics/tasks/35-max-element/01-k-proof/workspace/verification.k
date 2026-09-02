requires "reference-semantics/semantics.k"

module MAX-ELEMENT-VERIFICATION
  imports MPY

  // The exact translated program, named so that the claims have one source of
  // truth for the implementation they execute.
  syntax Module ::= "maxElementProgram" [function, total]
  rule maxElementProgram
    => Module(
         FuncDef("max_element", Params("l"),
           Return(Call(Name("max"), Name("l")))))

  // A proof-side encoding of an arbitrary finite integer sequence, used as the
  // tail of a Python list, plus its mathematical left-fold maximum.
  syntax ValSeq ::= intVals(IntSeq)

  syntax Int ::= maxOf(Int, IntSeq) [function, total]
  rule maxOf(M:Int, .IntSeq)                => M
  rule maxOf(M:Int, iCons(I:Int, R:IntSeq)) => maxOf(maxInt(M, I), R)

  // These equations give intVals exactly the observable iteration behavior of
  // the corresponding vCons chain.  Their form lets symbolic narrowing happen
  // on IntSeq rather than on the untyped ValSeq.
  rule <k> #iterNext(list(intVals(.IntSeq)))
        => #iterDone ... </k>
       [priority(40)]
  rule <k> #iterNext(list(intVals(iCons(I:Int, R:IntSeq))))
        => #iterYield(I, list(intVals(R))) ... </k>
       [priority(40)]
endmodule
