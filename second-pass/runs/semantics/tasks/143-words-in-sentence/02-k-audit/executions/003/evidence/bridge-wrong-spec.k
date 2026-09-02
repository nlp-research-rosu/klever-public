requires "verification.k"

module BRIDGE-WRONG-SPEC
  imports VERIFICATION

  claim [bridge-admits-wrong-result]:
    <k>
      #applyK(
        toCall(
          boundMethodV(
            str(sentenceCodes(
              wCons(
                iCons(97, iCons(97, .IntSeq)),
                wCons(
                  iCons(98, iCons(98, iCons(98, .IntSeq))),
                  wCons(
                    iCons(99, iCons(99, iCons(99, iCons(99, .IntSeq)))),
                    .WordSeq))))),
            "split")),
        .Vals)
      => ref(0)
    </k>
    <heap>
      .Map
      =>
      0 |-> list(wordsVals(
        wCons(
          iCons(97, iCons(97, .IntSeq)),
          wCons(
            iCons(98, iCons(98, iCons(98, .IntSeq))),
            wCons(
              iCons(99, iCons(99, iCons(99, iCons(99, .IntSeq)))),
              .WordSeq)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
endmodule
