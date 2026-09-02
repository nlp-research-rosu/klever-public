requires "body-mutant-verification.k"

module BODY-SENSITIVITY-SPEC
  imports MPY-VERIFICATION

  // False after the executed solutionModule body is changed to return [].
  claim
      <k> bootstrap ~> invoke("filter_integers",
            VList(VString("a"), VFloat("3.14"), VInt(5))) => .K </k>
      <program> solutionModule() </program>
      <return> noResult => result(VList(VInt(5))) </return>
endmodule
