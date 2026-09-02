requires "verification.k"

module MPY-SPEC
  imports MPY-VERIFICATION

  // Inductive call lemma.  KREST makes the statement contextual, so the same
  // claim summarizes the recursive call under the caller's continuations.
  claim [sum-squares-call]:
    <k> invoke1("sum_squares", ListVal(IS:Ints)) ~> KREST:K
      => VInt(sumSquaresSpec(IS)) ~> KREST </k>
    <functions> solutionFunctions </functions>
    <env> ENV:Map => ENV </env>

  // End-to-end theorem: load precisely the Module emitted in solution.mpy,
  // invoke its required entry point, and obtain the mathematical contract.
  claim [sum-squares-program]:
    <k> solutionProgram ~> run(ListVal(IS:Ints))
      => VInt(sumSquaresSpec(IS)) </k>
    <functions> .Map => solutionFunctions </functions>
    <env> .Map </env>
endmodule
