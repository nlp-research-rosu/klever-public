requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh audit mutation.  This is deliberately false: both Python
  // implementations and fresh concrete K execution return true for this
  // satisfying input, while the postcondition below demands false.
  claim [false-result-hello]:
        <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("hello") pyStr("ell") </args>
          <env> .Map => ?RHO </env>
          <out> NoResult => Result(pyBool(false)) </out>
        </mpy>
endmodule
