requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  // This original multiplication summary is false for the mutated addition
  // body. Witness: N = 2 and CS = (IntV(5), .Values) gives 7, not 10.
  claim
    <mpy>
      <k>
        #call("derivative_helper",
          (ListV(CS:Values), IntV(N:Int)),
          bodyMutatedFuns)
        ~> K:K
        => ListV(#differentiate(N, CS)) ~> K
      </k>
    </mpy>
    [label(body-mutated-helper)]
endmodule
