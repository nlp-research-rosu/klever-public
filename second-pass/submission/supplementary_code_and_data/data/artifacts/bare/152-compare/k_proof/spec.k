requires "verification.k"

module SPEC
  imports VERIFICATION

  claim <k> execute(solutionProgram, VList(GS), VList(US)) ~> REST
         => VList(expected(GS, US)) ~> REST </k>
endmodule
