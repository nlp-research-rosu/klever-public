requires "verification-negative-model.k"

module SPEC-NEGATIVE-MODEL
  imports VERIFICATION-NEGATIVE-MODEL

  claim [permitted-wrong-negative-index-result]:
    <k>
      #applyK(
        toCall(#helperClosure),
        (ref(0), -1, 0, .Vals))
    =>
      1
    </k>
    <heap> 0 |-> list(vCons(5, .ValSeq)) </heap>
endmodule
