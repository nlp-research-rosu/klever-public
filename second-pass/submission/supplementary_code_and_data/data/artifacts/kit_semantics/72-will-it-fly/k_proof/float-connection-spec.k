requires "verification.k"

module FLOAT-SUM-CONNECTION
  imports FLOAT-REST-VERIFICATION

  // The initial Int accumulator crosses to the float phase at the first
  // float. FLOAT-REST-VERIFICATION is justified independently.
  claim [float-sum-fold]:
    <k> #iterNext(list(VS:ValSeq)) ~> #sumCont(ACC:Int)
      => sumToFloat(ACC, VS) ... </k>
    requires allNumeric(VS) andBool hasFloat(VS)
endmodule
