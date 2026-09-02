requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim
    <task>
      <k> solutionProgramMutated => .K </k>
      <input> DictVal(StrVal("a") StrVal("b")) </input>
      <env> .Map </env>
      <result>
        NoneVal => BoolVal(contract(DictVal(StrVal("a") StrVal("b"))))
      </result>
    </task>
endmodule
