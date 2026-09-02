requires "verification.k"

module REPRESENTATION-GAP
  imports MAX-ELEMENT-VERIFICATION

  // These are the missing constructor-level connections between the abstract
  // intVals tail and the supplied semantics' real ValSeq constructors.
  claim [base-connection]:
    <k> intVals(.IntSeq) => .ValSeq </k>

  claim [step-connection]:
    <k> intVals(iCons(I:Int, R:IntSeq))
      => vCons(I, intVals(R)) </k>
endmodule
