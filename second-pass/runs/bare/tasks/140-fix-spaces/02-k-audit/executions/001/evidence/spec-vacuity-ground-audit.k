requires "verification.k"

module SPEC-VACUITY-GROUND-AUDIT
  imports VERIFICATION

  // Deliberately false at a concrete satisfying pre-state: fix_spaces("")
  // returns "", while this destination requires "!".
  claim
    <py>
      <k>
        call("fix_spaces", pyStr(.PString))
          => pyStr(ch("!") .PString)
      </k>
      <input> "" </input>
      <env> .Env </env>
      <funs> solutionFuns </funs>
      <result> .K </result>
    </py>
endmodule
