requires "verification.k"

module SPEC
  imports VERIFICATION

  // The pair of mutually circular claims is structural induction over the
  // finite PString argument.  Together they cover every string and establish
  // that execution of both recursive Python functions equals the independent
  // reference relation above.
  claim
    <py>
      <k> call("fix_spaces", pyStr(S:PString)) ~> K:K
        => pyStr(fixRef(S)) ~> K
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
