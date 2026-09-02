requires "verification.k"

module SUM-CONNECTION
  imports SUMMARY-DEFINITION

  // Bridge-free universal theorem for the exact sum-fold configuration used
  // by VERIFICATION's operational bridge.
  claim [sum-fold]:
    <k> #iterNext(list(VS:ValSeq)) ~> #sumCont(ACC:Int)
      => sumInts(ACC, VS) ... </k>
    requires allIntegral(VS)

  // Bridge-free connection for the float-accumulator phase.
  claim [float-rest-fold]:
    <k> #iterNext(list(VS:ValSeq)) ~> #sumContF(ACC:Float)
      => sumFloatRest(ACC, VS) ... </k>
    requires allNumeric(VS)

  // The target orientation is absent from this definition. The RHS reduces
  // solely by reverseSlice's exhaustive defining equation.
  claim [reverse-summary]:
    <k> buildVS(VS:ValSeq, vsLen(VS) +Int -1, -1, -1)
      => reverseSlice(VS) </k>

  // Exact fixed-semantics slice continuation, with an arbitrary k suffix.
  claim [reverse-slice]:
    <k> someB(-1) ~> #slStep(list(VS:ValSeq), noB, noB)
      => #alloc(list(reverseSlice(VS))) ... </k>
endmodule
