requires "slice-fixed.k"

module SPEC-SLICE-FIXED-GROUND
  imports SLICE-FIXED

  claim <k>
          doSlice(str(iCons(65, iCons(66, .IntSeq))), someB(2), noB, noB) ~> #bang
        =>
          str(iCons(33, .IntSeq))
        </k>

  claim <k>
          doSlice(str(iCons(65, iCons(66, iCons(48, .IntSeq)))), someB(2), noB, noB) ~> #bang
        =>
          str(iCons(48, iCons(33, .IntSeq)))
        </k>

  claim <k>
          doSlice(str(iCons(65, iCons(66, iCons(49, iCons(48, .IntSeq))))), someB(2), noB, noB) ~> #bang
        =>
          str(iCons(49, iCons(48, iCons(33, .IntSeq))))
        </k>

  // Outside the bridge match (start 1): both definitions must retain the B.
  claim <k>
          doSlice(str(iCons(65, iCons(66, iCons(48, .IntSeq)))), someB(1), noB, noB) ~> #bang
        =>
          str(iCons(66, iCons(48, iCons(33, .IntSeq))))
        </k>
endmodule
