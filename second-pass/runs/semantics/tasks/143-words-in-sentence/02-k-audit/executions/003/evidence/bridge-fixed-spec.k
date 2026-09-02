requires "verification.k"

module BRIDGE-FIXED-SPEC
  imports VERIFICATION

  claim [fixed-semantics-result]:
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
      0 |-> list(
        vCons(str(iCons(120, .IntSeq)), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
endmodule
