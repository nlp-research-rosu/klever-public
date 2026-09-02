requires "verification.k"

module UNIVERSAL-ENTRY-SPEC
  imports MPY-VERIFICATION

  // The unrestricted modeled-list theorem absent from the submitted spec.k.
  claim
      <k> bootstrap ~> invoke("filter_integers", VList(VS:PyVals)) => .K </k>
      <program> solutionModule() </program>
      <return>
        noResult => result(VList(onlyIntegerInstances(VS)))
      </return>
endmodule
