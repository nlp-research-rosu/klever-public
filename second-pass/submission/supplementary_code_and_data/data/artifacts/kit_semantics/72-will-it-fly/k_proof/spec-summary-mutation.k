requires "mutation-verification.k"

module SPEC-SUMMARY-MUTATION
  imports SUMMARY-MUTATION

  claim [wrong-sum]:
    <k>
      #iterNext(list(vCons(1, vCons(2, .ValSeq)))) ~> #sumCont(0)
      =>
      sumInts(0, vCons(1, vCons(2, .ValSeq)))
    </k>

  claim [wrong-reverse]:
    <k>
      someB(-1)
      ~> #slStep(
           list(vCons(1, vCons(2, .ValSeq))),
           noB,
           noB)
      =>
      #alloc(
        list(
          reverseSlice(
            vCons(1, vCons(2, .ValSeq)))))
    </k>

  claim [wrong-float-sum]:
    <k>
      #iterNext(list(vCons(F:Float, .ValSeq))) ~> #sumCont(ACC:Int)
      =>
      sumToFloat(ACC, vCons(F, .ValSeq))
    </k>
endmodule
