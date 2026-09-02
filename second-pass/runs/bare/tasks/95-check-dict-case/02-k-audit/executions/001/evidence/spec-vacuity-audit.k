requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh auditor mutation. The precondition is the realizable initial state
  // for the empty dictionary, but the program must return false, not true.
  claim
    <task>
      <k> solutionProgram => .K </k>
      <input> DictVal() </input>
      <env> .Map </env>
      <result> NoneVal => BoolVal(true) </result>
    </task>
endmodule
