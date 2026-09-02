requires "verification.k"

module CONNECTION-WITNESS
  imports SUMMARY-DEFINITION

  claim [sum-three]:
    <k>
      #iterNext(list(vCons(1, vCons(2, .ValSeq)))) ~> #sumCont(0)
      => 3
    </k>

  claim [sum-negative]:
    <k>
      #iterNext(list(vCons(-2, vCons(1, .ValSeq)))) ~> #sumCont(0)
      => -1
    </k>

  claim [reverse-two]:
    <k>
      someB(-1)
      ~> #slStep(
           list(vCons(1, vCons(2, .ValSeq))),
           noB,
           noB)
      =>
      #alloc(list(vCons(2, vCons(1, .ValSeq))))
    </k>
endmodule
