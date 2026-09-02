requires "reference-semantics/semantics.k"

module AUDIT-SLICE-GROUND-BAD
  imports MPY

  // Deliberately false opposite outcome: [97, 98][1:] is [98], not [].
  claim [wrong-two]:
    <k>
      buildIS(
        iCons(97, iCons(98, .IntSeq)),
        clampHi(1, isLen(iCons(97, iCons(98, .IntSeq))), 1),
        isLen(iCons(97, iCons(98, .IntSeq))),
        1)
      => .IntSeq
    </k>
endmodule
