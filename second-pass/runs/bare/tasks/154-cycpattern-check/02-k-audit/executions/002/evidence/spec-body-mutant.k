requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  // The original program and contract both return true for this input.  The
  // translated mutated body returns false, so a body-sensitive proof must fail.
  claim [mutated-body-hello]:
        <mpy>
          <k> mutatedSolutionProgram() ~> start => .K </k>
          <args> pyStr("hello") pyStr("ell") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(cyclicContains("hello", "ell"))) </out>
        </mpy>
endmodule
