requires "reference-semantics/semantics.k"

module MAX-ELEMENT-VERIFICATION-BRIDGE-MUTATED
  imports MPY

  syntax Module ::= "maxElementProgramBridgeMutated" [function, total]
  rule maxElementProgramBridgeMutated
    => Module(
         FuncDef("max_element", Params("l"),
           Return(Call(Name("max"), Name("l")))))

  syntax ValSeq ::= intValsBridgeMutated(IntSeq)

  syntax Int ::= maxOfBridgeMutated(Int, IntSeq) [function, total]
  rule maxOfBridgeMutated(M:Int, .IntSeq) => M
  rule maxOfBridgeMutated(M:Int, iCons(I:Int, R:IntSeq))
    => maxOfBridgeMutated(maxInt(M, I), R)

  rule <k> #iterNext(list(intValsBridgeMutated(.IntSeq)))
        => #iterDone ... </k>
       [priority(40)]
  // Deliberate bridge-value mutation: yields I+1 instead of I.
  rule <k> #iterNext(list(intValsBridgeMutated(iCons(I:Int, R:IntSeq))))
        => #iterYield(I +Int 1, list(intValsBridgeMutated(R))) ... </k>
       [priority(40)]
endmodule
