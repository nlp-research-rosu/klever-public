requires "slice-fixed.k"

module SPEC-SLICE-FIXED-UNIVERSAL
  imports SLICE-FIXED

  claim <k>
          doSlice(str(iCons(A, iCons(B, REST))), someB(2), noB, noB) ~> #bang
        =>
          str(seqConcat(REST, iCons(33, .IntSeq)))
        </k>
endmodule
