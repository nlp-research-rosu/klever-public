requires "verification.k"

module BRIDGE-ENABLED-SPEC
  imports VERIFICATION

  claim [split-aa]:
    <k>
      #applyK(
        toCall(
          boundMethodV(
            str(sentenceCodes(wCons(iCons(97, iCons(97, .IntSeq)), .WordSeq))),
            "split")),
        .Vals)
      =>
      ref(0)
    </k>
    <heap>
      .Map
      =>
      0 |-> list(wordsVals(wCons(iCons(97, iCons(97, .IntSeq)), .WordSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>

  claim [iterate-aa]:
    <k>
      #iterNext(
        list(wordsVals(wCons(iCons(97, iCons(97, .IntSeq)), .WordSeq))))
      =>
      #iterYield(
        str(iCons(97, iCons(97, .IntSeq))),
        list(wordsVals(.WordSeq)))
    </k>
endmodule
