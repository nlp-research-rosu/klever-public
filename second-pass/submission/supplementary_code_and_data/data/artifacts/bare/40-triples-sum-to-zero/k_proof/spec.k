requires "verification.k"

module SPEC
  imports VERIFICATION

  // Lemma 1: the helper exhaustively checks all pairs following FIRST.
  claim [pair-correct]:
    <mpy>
      <k> invoke2("_has_pair_sum", VInt(FIRST), VList(IS)) ~> RESTK
        => VBool(hasPairWith(FIRST, IS)) ~> RESTK </k>
      <funs> solutionFunctions </funs>
      <env> _ENV </env>
      <input> _INPUT </input>
      <result> _RESULT </result>
    </mpy>

  // Lemma 2: the entry point exhaustively checks every possible first
  // position, using pair-correct for the remaining two positions.
  claim [triples-correct]:
    <mpy>
      <k> invoke1("triples_sum_to_zero", VList(IS)) ~> RESTK
        => VBool(hasZeroTriple(IS)) ~> RESTK </k>
      <funs> solutionFunctions </funs>
      <env> _ENV </env>
      <input> _INPUT </input>
      <result> _RESULT </result>
    </mpy>

  // The exact solution.mpy tree, from a fresh semantics configuration, meets
  // the HumanEval contract for every finite list of mathematical integers.
  claim [program-correct]:
    <mpy>
      <k> solutionProgram => .K </k>
      <funs> .Map => solutionFunctions </funs>
      <env> .Map </env>
      <input> VList(IS) </input>
      <result> noResult => result(VBool(hasZeroTriple(IS))) </result>
    </mpy>
endmodule
