requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: for S = .PString and K = .K, the real call returns
  // pyStr(.PString), not pyStr(ch("!") .PString).
  claim
    <py>
      <k> call("fix_spaces", pyStr(S:PString)) ~> K:K
        => pyStr(ch("!") fixRef(S)) ~> K
      </k>
      <input> _INPUT:String </input>
      <env> _ENV:Env </env>
      <funs> solutionFuns </funs>
      <result> _RESULT:K </result>
    </py>

  claim
    <py>
      <k> call("_drop_spaces", pyStr(S:PString)) ~> K:K
        => pyStr(dropRef(S)) ~> K
      </k>
      <input> _INPUT:String </input>
      <env> _ENV:Env </env>
      <funs> solutionFuns </funs>
      <result> _RESULT:K </result>
    </py>
endmodule
