requires "connection-verification.k"

module MAX-ELEMENT-CONNECTION-STEP-SPEC
  imports MAX-ELEMENT-CONNECTION-VERIFICATION

  // Bridge-free universal connection for intVals(.IntSeq): the supplied list
  // iterator on the corresponding ordinary list tail produces #iterDone.
  claim [expanded-empty-step]:
    <k> #iterNext(list(.ValSeq)) ~> CONT:K
      => #iterDone ~> CONT </k>

  // Bridge-free universal connection for intVals(iCons(I,R)): the supplied
  // list iterator on the corresponding ordinary vCons tail yields I and keeps
  // the expanded remainder. The arbitrary CONT and omitted cells are framed.
  claim [expanded-cons-step]:
    <k> #iterNext(list(vCons(I:Int, expandIntVals(R:IntSeq)))) ~> CONT:K
      => #iterYield(I, list(expandIntVals(R))) ~> CONT </k>
endmodule
