requires "bridge-base.k"

module BRIDGE-GROUND-SPEC
  imports BRIDGE-BASE

  // Bridge-free fixed-semantics witnesses for reverse slicing.
  claim
    <k>
      doSlice(list(.ValSeq), noB, noB, someB(-1))
      => list(.ValSeq)
    </k>

  claim
    <k>
      doSlice(list(vCons(7, .ValSeq)), noB, noB, someB(-1))
      => list(vCons(7, .ValSeq))
    </k>

  claim
    <k>
      doSlice(
        list(vCons(1, vCons(2, vCons(3, .ValSeq)))),
        noB, noB, someB(-1))
      => list(vCons(3, vCons(2, vCons(1, .ValSeq))))
    </k>

  claim
    <k>
      doSlice(
        list(vCons(true, vCons(noneV, .ValSeq))),
        noB, noB, someB(-1))
      => list(vCons(noneV, vCons(true, .ValSeq)))
    </k>

  // Bridge-free fixed-semantics witnesses for integer sum.
  claim
    <k> #sumAcc(list(.ValSeq), 0) => 0 </k>

  claim
    <k>
      #sumAcc(list(vCons(1, vCons(-2, vCons(3, .ValSeq)))), 0)
      => 2
    </k>
endmodule
