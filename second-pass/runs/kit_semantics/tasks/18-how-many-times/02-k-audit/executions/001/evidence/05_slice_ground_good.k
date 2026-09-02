requires "reference-semantics/semantics.k"

module AUDIT-SLICE-GROUND-GOOD
  imports MPY

  claim [one]:
    <k>
      buildIS(
        iCons(97, .IntSeq),
        clampHi(1, isLen(iCons(97, .IntSeq)), 1),
        isLen(iCons(97, .IntSeq)),
        1)
      => .IntSeq
    </k>

  claim [two]:
    <k>
      buildIS(
        iCons(97, iCons(98, .IntSeq)),
        clampHi(1, isLen(iCons(97, iCons(98, .IntSeq))), 1),
        isLen(iCons(97, iCons(98, .IntSeq))),
        1)
      => iCons(98, .IntSeq)
    </k>

  claim [four]:
    <k>
      buildIS(
        iCons(97, iCons(98, iCons(99, iCons(100, .IntSeq)))),
        clampHi(
          1,
          isLen(iCons(97, iCons(98, iCons(99, iCons(100, .IntSeq))))),
          1),
        isLen(iCons(97, iCons(98, iCons(99, iCons(100, .IntSeq))))),
        1)
      => iCons(98, iCons(99, iCons(100, .IntSeq)))
    </k>
endmodule
