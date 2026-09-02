requires "verification.k"

module FALSE-RESULT-SPEC
  imports MPY-VERIFICATION

  // Fresh audit mutation: the satisfying prompt-one input returns [5], not [6].
  claim
      <k> bootstrap ~> invoke("filter_integers",
            VList(VString("a"), VFloat("3.14"), VInt(5))) => .K </k>
      <program> solutionModule() </program>
      <return> noResult => result(VList(VInt(6))) </return>
endmodule
