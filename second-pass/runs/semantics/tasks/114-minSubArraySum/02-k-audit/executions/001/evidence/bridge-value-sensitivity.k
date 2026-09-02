requires "verification.k"

module ITERATOR-WRONG-SPEC
  imports VERIFICATION-BASE

  // Opposite interpretation witness: the actual head is 7, not 8.
  claim
    <k>
      #iterNext(list(intVals(iCons(7, .IntSeq))))
      => #iterYield(8, list(intVals(.IntSeq)))
      ...
    </k>
endmodule

module SUBSCRIPT-WRONG-SPEC
  imports VERIFICATION-BASE

  // Opposite interpretation witness for the proof-local head simplification.
  claim
    <k>
      valSeqAt(intVals(iCons(7, .IntSeq)), 0)
      => 8
      ...
    </k>
endmodule
