requires "verification.k"

module SPEC
  imports VERIFICATION

  // Structural induction theorem for the recursive helper. After one
  // nonempty-list step, the remaining obligation is the same claim at the
  // tail and successor degree, so kprove closes it by circularity.
  claim
    <mpy>
      <k>
        #call("derivative_helper",
          (ListV(CS:Values), IntV(N:Int)),
          solutionFuns)
        ~> K:K
        => ListV(#differentiate(N, CS)) ~> K
      </k>
    </mpy>
    [label(helper-correct)]

  // [] and C0 :: CS exhaust all finite coefficient lists. The first
  // coefficient is discarded and the helper begins at degree one.
  claim
    <mpy>
      <k>
        #run(solutionProgram, ListV(.Values))
        => ListV(.Values)
      </k>
    </mpy>
    [label(derivative-empty), depends(helper-correct)]

  claim
    <mpy>
      <k>
        #run(solutionProgram,
          ListV((_C0:Value, CS:Values)))
        => ListV(#differentiate(1, CS))
      </k>
    </mpy>
    [label(derivative-nonempty), depends(helper-correct)]
endmodule
