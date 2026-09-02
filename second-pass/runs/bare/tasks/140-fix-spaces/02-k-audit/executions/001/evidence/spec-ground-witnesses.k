requires "/tmp/audit-work/src/verification.k"

module SPEC-GROUND-WITNESSES
  imports VERIFICATION

  claim
    <py>
      <k>
        call("fix_spaces", pyStr(ch("a") sp sp .PString))
          => pyStr(ch("a") ch("_") ch("_") .PString)
      </k>
      <input> "" </input>
      <env> .Env </env>
      <funs> solutionFuns </funs>
      <result> .K </result>
    </py>

  claim
    <py>
      <k>
        call("_drop_spaces", pyStr(sp sp ch("a") sp sp .PString))
          => pyStr(ch("a") ch("_") ch("_") .PString)
      </k>
      <input> "" </input>
      <env> .Env </env>
      <funs> solutionFuns </funs>
      <result> .K </result>
    </py>
endmodule
