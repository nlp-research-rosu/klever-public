requires "/tmp/audit-work/candidate-src/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Preserve the two genuine recursive connection lemmas so the mutated
  // top-level claim reaches its deliberately false result obligation.
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

  // False mutation: force every list, including [], to return true.
  claim [program-always-true]:
    <mpy>
      <k> solutionProgram => .K </k>
      <funs> .Map => solutionFunctions </funs>
      <env> .Map </env>
      <input> VList(IS) </input>
      <result> noResult => result(VBool(true)) </result>
    </mpy>
endmodule
