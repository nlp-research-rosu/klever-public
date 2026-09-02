requires "bridge-base.k"

module BRIDGE-GROUND-FALSE-SPEC
  imports BRIDGE-BASE

  // Deliberately wrong opposite interpretation: [1,2] reversed is not [1,2].
  claim
    <k>
      doSlice(
        list(vCons(1, vCons(2, .ValSeq))),
        noB, noB, someB(-1))
      => list(vCons(1, vCons(2, .ValSeq)))
    </k>
endmodule
