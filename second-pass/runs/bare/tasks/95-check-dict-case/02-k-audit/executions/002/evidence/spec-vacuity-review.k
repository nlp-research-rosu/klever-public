requires "verification.k"

module SPEC-VACUITY-REVIEW
  imports VERIFICATION

  // False for this satisfiable input: both keys are lowercase.
  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(StrVal("a") StrVal("b")) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(false) </result>
    </task>
endmodule
