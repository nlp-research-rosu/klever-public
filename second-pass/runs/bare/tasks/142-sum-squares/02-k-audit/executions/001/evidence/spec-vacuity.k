requires "verification.k"

module MPY-SPEC-VACUITY
  imports MPY-VERIFICATION

  // Preserve the legitimate recursive-call lemma so the end-to-end target can
  // reach its result without unbounded unfolding.
  claim [sum-squares-call]:
    <k> invoke1("sum_squares", ListVal(IS:Ints)) ~> KREST:K
      => VInt(sumSquaresSpec(IS)) ~> KREST </k>
    <functions> solutionFunctions </functions>
    <env> ENV:Map => ENV </env>

  // Deliberately false: the returned integer is constrained to be one more
  // than the actual mathematical result. IS = .Ints is a satisfying witness:
  // fixed execution returns 0, while this destination requires 1.
  claim [false-sum-squares-program]:
    <k> solutionProgram ~> run(ListVal(IS:Ints))
      => VInt(sumSquaresSpec(IS) +Int 1) </k>
    <functions> .Map => solutionFunctions </functions>
    <env> .Map </env>
endmodule
