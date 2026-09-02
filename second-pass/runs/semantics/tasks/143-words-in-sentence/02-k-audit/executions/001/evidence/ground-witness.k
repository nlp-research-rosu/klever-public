requires "verification.k"

module GROUND-WITNESS
  imports VERIFICATION

  claim [valid-example]:
    <k>
      validWords(
        wCons(
          iCons(84, iCons(104, iCons(105, iCons(115, .IntSeq)))),
          wCons(
            iCons(105, iCons(115, .IntSeq)),
            wCons(
              iCons(97, .IntSeq),
              wCons(
                iCons(116, iCons(101, iCons(115, iCons(116, .IntSeq)))),
                .WordSeq)))))
        => true
    </k>

  claim [length-example]:
    <k>
      sentenceLen(
        wCons(
          iCons(84, iCons(104, iCons(105, iCons(115, .IntSeq)))),
          wCons(
            iCons(105, iCons(115, .IntSeq)),
            wCons(
              iCons(97, .IntSeq),
              wCons(
                iCons(116, iCons(101, iCons(115, iCons(116, .IntSeq)))),
                .WordSeq)))))
        => 14
    </k>

  claim [result-example]:
    <k>
      filterWords(
        .IntSeq,
        wCons(
          iCons(84, iCons(104, iCons(105, iCons(115, .IntSeq)))),
          wCons(
            iCons(105, iCons(115, .IntSeq)),
            wCons(
              iCons(97, .IntSeq),
              wCons(
                iCons(116, iCons(101, iCons(115, iCons(116, .IntSeq)))),
                .WordSeq)))))
        => iCons(105, iCons(115, .IntSeq))
    </k>
endmodule
