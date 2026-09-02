requires "/tmp/audit-work/candidate-src/reference-semantics/semantics.k"

module SLICE-GROUND
  imports MPY

  claim
    <k>
      Subscript(
        str(iCons(48, iCons(98, .IntSeq))),
        Slice(Int(2), NoBound, NoBound)
      ) ~> CONT:K
      =>
      str(.IntSeq) ~> CONT
    </k>

  claim
    <k>
      Subscript(
        str(iCons(48, iCons(98, iCons(48, .IntSeq)))),
        Slice(Int(2), NoBound, NoBound)
      ) ~> CONT:K
      =>
      str(iCons(48, .IntSeq)) ~> CONT
    </k>

  claim
    <k>
      Subscript(
        str(iCons(48, iCons(98,
          iCons(49, iCons(48, iCons(49, .IntSeq)))))),
        Slice(Int(2), NoBound, NoBound)
      ) ~> CONT:K
      =>
      str(iCons(49, iCons(48, iCons(49, .IntSeq)))) ~> CONT
    </k>
endmodule
