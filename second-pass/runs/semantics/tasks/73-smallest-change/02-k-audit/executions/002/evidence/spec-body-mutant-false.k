requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT-FALSE
  imports VERIFICATION

  // The mutated closure's fixed-semantics result is 999. The bridge-enabled
  // theory nevertheless proves 0 for the satisfying empty-list input.
  claim [mutated-body-wrong-result]:
    <k>
      #applyK(toCall(#mainClosure), (ref(0), .Vals))
    =>
      0
    </k>
    <heap> 0 |-> list(.ValSeq) </heap>
endmodule
