requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfying input GS = US = VNil:
  // the real program returns VNil, not a list with an extra leading 1.
  claim <k> execute(solutionProgram, VList(GS), VList(US)) ~> REST
         => VList(VCons(VInt(1), expected(GS, US))) ~> REST </k>
endmodule
