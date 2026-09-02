requires "verification.k"

module SPEC-UNIVERSAL-PROBE
  imports VERIFICATION

  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal(KEYS:Values) </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(contract(DictVal(KEYS))) </result>
    </task>
endmodule
