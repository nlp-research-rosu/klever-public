requires "verification.k"

module SPEC-VACUITY-GROUND
  imports VERIFICATION

  // False result mutation of the target claim at the satisfiable empty input.
  // The real call returns pyStr(.PString), while this demands "X".
  claim
    <py>
      <k> call("fix_spaces", pyStr(.PString))
        => pyStr(ch("X") .PString)
      </k>
      <input> "" </input>
      <env> .Env </env>
      <funs> solutionFuns </funs>
      <result> .K </result>
    </py>
endmodule
