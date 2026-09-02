requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Ground mutation of the result obligation. The empty-input entry state is
  // reachable and returns VList(VNil), not the deliberately false [1].
  claim <k> execute(solutionProgram, VList(VNil), VList(VNil))
         => VList(VCons(VInt(1), VNil)) </k>
endmodule
