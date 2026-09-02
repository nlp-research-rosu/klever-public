requires "/tmp/audit-work/143/verification.k"

module GROUND-WITNESS
  imports VERIFICATION

  claim [witness-valid]:
    <k>
      validWords(
        wCons(
           iCons(97, iCons(97, .IntSeq)),
           wCons(
             iCons(98, iCons(98, iCons(98, .IntSeq))),
             wCons(
               iCons(99, iCons(99, iCons(99, iCons(99, .IntSeq)))),
               .WordSeq))))
      => true
    </k>

  claim [witness-length]:
    <k>
      sentenceLen(
        wCons(
          iCons(97, iCons(97, .IntSeq)),
          wCons(
            iCons(98, iCons(98, iCons(98, .IntSeq))),
            wCons(
              iCons(99, iCons(99, iCons(99, iCons(99, .IntSeq)))),
              .WordSeq))))
      => 11
    </k>

  claim [witness-result]:
    <k>
      filterWords(
        .IntSeq,
        wCons(
          iCons(97, iCons(97, .IntSeq)),
          wCons(
            iCons(98, iCons(98, iCons(98, .IntSeq))),
            wCons(
              iCons(99, iCons(99, iCons(99, iCons(99, .IntSeq)))),
              .WordSeq))))
      => iCons(
           97,
           iCons(
             97,
             iCons(
               32,
               iCons(98, iCons(98, iCons(98, .IntSeq))))))
    </k>
endmodule
