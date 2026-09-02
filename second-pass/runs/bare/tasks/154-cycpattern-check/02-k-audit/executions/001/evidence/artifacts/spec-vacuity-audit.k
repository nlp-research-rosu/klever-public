requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the submitted program returns true for ("hello", "ell").
  claim <mpy>
          <k> solutionProgram() ~> start => .K </k>
          <args> pyStr("hello") pyStr("ell") </args>
          <env> .Map => ?_RHO </env>
          <out> NoResult => Result(pyBool(false)) </out>
        </mpy>
endmodule
