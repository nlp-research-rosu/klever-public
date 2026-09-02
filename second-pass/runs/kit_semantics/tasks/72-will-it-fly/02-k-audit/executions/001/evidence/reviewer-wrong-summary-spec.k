requires "reviewer-wrong-summary-verification.k"

module REVIEWER-WRONG-SUMMARY-SPEC
  imports REVIEWER-WRONG-SUMMARY

  claim [wrong-integer-sum]:
    <k>
      #iterNext(list(vCons(1, vCons(2, .ValSeq)))) ~> #sumCont(0)
      => sumInts(0, vCons(1, vCons(2, .ValSeq)))
    </k>

  claim [wrong-reverse]:
    <k>
      someB(-1)
      ~> #slStep(list(vCons(1, vCons(2, .ValSeq))), noB, noB)
      => #alloc(list(reverseSlice(vCons(1, vCons(2, .ValSeq)))))
    </k>

  claim [wrong-float-sum]:
    <k>
      #iterNext(list(vCons(F:Float, .ValSeq))) ~> #sumCont(ACC:Int)
      => sumToFloat(ACC, vCons(F, .ValSeq))
    </k>
endmodule
