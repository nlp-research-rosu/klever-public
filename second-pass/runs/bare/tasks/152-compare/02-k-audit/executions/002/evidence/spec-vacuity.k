requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfying ground input GS = US = VNil:
  // the real program returns VNil, not a list with an extra leading 1.
  claim <k> execute(solutionProgram, VList(VNil), VList(VNil))
         => VList(VCons(VInt(1), VNil)) </k>
endmodule
