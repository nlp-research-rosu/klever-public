requires "verification.k"

module GROUND-WITNESS
  imports VERIFICATION

  // A concrete satisfier for the entry precondition.
  claim [valid-a]:
    <k>
      validHistogramInput(iCons(97, .IntSeq))
      =>
      true
    </k>

  claim [result-empty]:
    <k>
      histogramResult(.IntSeq)
      =>
      dictV(.ValSeq, .ValSeq)
    </k>

  claim [result-a]:
    <k>
      histogramResult(iCons(97, .IntSeq))
      =>
      dictV(
        vCons(str(iCons(97, .IntSeq)), .ValSeq),
        vCons(1, .ValSeq))
    </k>

  // "a b b a" has a two-way tie, with first-occurrence key order a,b.
  claim [result-tie]:
    <k>
      histogramResult(
        iCons(
          97,
          iCons(
            32,
            iCons(
              98,
              iCons(32, iCons(98, iCons(32, iCons(97, .IntSeq))))))))
      =>
      dictV(
        vCons(
          str(iCons(97, .IntSeq)),
          vCons(str(iCons(98, .IntSeq)), .ValSeq)),
        vCons(2, vCons(2, .ValSeq)))
    </k>
endmodule
