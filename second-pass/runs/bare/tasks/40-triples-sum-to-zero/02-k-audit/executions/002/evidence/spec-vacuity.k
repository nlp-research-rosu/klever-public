requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [pair-correct]:
    <mpy>
      <k> invoke2("_has_pair_sum", VInt(FIRST), VList(IS)) ~> RESTK
        => VBool(hasPairWith(FIRST, IS)) ~> RESTK </k>
      <funs> solutionFunctions </funs>
      <env> _ENV </env>
      <input> _INPUT </input>
      <result> _RESULT </result>
    </mpy>

  claim [triples-correct]:
    <mpy>
      <k> invoke1("triples_sum_to_zero", VList(IS)) ~> RESTK
        => VBool(hasZeroTriple(IS)) ~> RESTK </k>
      <funs> solutionFunctions </funs>
      <env> _ENV </env>
      <input> _INPUT </input>
      <result> _RESULT </result>
    </mpy>

  // Fresh false mutation: require the opposite Boolean result.  Empty input
  // is a satisfying witness: execution returns false, while this asks true.
  claim [program-false-opposite]:
    <mpy>
      <k> solutionProgram => .K </k>
      <funs> .Map => solutionFunctions </funs>
      <env> .Map </env>
      <input> VList(IS) </input>
      <result> noResult
        => result(VBool(notBool hasZeroTriple(IS))) </result>
    </mpy>
endmodule
