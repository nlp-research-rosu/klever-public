requires "verification.k"

module GROUND-RESULT-SPEC
  imports FIX-SPACES-BASE

  claim
    <k>
      appendPending(
        fixSpacesLoop(
          .IntSeq,
          iCons(97, iCons(32, iCons(32, .IntSeq))),
          0),
        trailingSpaces(
          iCons(97, iCons(32, iCons(32, .IntSeq))),
          0))
      =>
      iCons(97, iCons(95, iCons(95, .IntSeq)))
    </k>
endmodule
