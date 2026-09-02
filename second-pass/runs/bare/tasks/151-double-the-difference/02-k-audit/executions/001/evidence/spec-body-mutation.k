requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  // The original result for [1] is 1.  The mutated executed body returns 2.
  claim
    <py>
      <k> solutionProgramMutation => .K </k>
      <input> pyList(intCons(1, nil)) </input>
      <lst> noValue </lst>
      <total> pyInt(0) </total>
      <value> pyInt(0) </value>
      <function> noFunction </function>
      <result> noResult => pyInt(1) </result>
    </py>
endmodule
