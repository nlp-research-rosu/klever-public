requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports MPY-VERIFICATION

  // Fresh false mutation of the submitted "abcdef" claim:
  // Python and the unmutated K semantics both return 3, never 4.
  claim <k> runProgram(solutionAST, "abcdef") => VInt(4) ... </k>
endmodule
