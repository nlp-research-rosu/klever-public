requires "verification-connection.k"

module SPEC-ITERATOR-CONNECTION
  imports VERIFICATION-CONNECTION

  // Bridge-free fixed-semantics result corresponding to the candidate's
  // intVals(.IntSeq) iterator rule.
  claim [empty-iterator-connection]:
    <k>
      #iterNext(list(materializeInts(.IntSeq)))
      => #iterDone
      ...
    </k>

  // Bridge-free fixed-semantics result corresponding to the candidate's
  // intVals(iCons(I, IS)) iterator rule, universally in I and IS.
  claim [cons-iterator-connection]:
    <k>
      #iterNext(list(materializeInts(iCons(I, IS))))
      => #iterYield(I, list(materializeInts(IS)))
      ...
    </k>
endmodule
