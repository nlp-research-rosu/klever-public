requires "verification.k"

module MPY-SPEC-VACUITY-AUDIT
  imports MPY-VERIFICATION

  // Keep the genuine recursive call invariant available to the end-to-end
  // proof. This claim is unchanged from the candidate.
  claim [sum-squares-call]:
    <k> invoke1("sum_squares", ListVal(IS:Ints)) ~> KREST:K
      => VInt(sumSquaresSpec(IS)) ~> KREST </k>
    <functions> solutionFunctions </functions>
    <env> ENV:Map => ENV </env>

  // Deliberately false: for the satisfying witness IS = .Ints the real result
  // and sumSquaresSpec are 0, while this destination requires 1.
  claim [false-off-by-one-program]:
    <k> solutionProgram ~> run(ListVal(IS:Ints))
      => VInt(sumSquaresSpec(IS) +Int 1) </k>
    <functions> .Map => solutionFunctions </functions>
    <env> .Map </env>
endmodule
