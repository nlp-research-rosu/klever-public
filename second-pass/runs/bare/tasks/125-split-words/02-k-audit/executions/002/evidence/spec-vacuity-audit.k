requires "/tmp/audit-work/candidate/verification.k"

module AUDIT-SPEC-VACUITY
  imports MPY-VERIFICATION

  // Deliberately false: the satisfying input "abcdef" executes to VInt(3).
  claim <k> runProgram(solutionAST, "abcdef") => VInt(4) ... </k>
endmodule
