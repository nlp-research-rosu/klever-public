requires "verification.k"

module SUMMARY-WITNESS-SPEC
  imports VERIFICATION-BASE

  claim [empty]:
    <k> str(antiFinish(.IntSeq, .IntSeq, .IntSeq))
        => str(.IntSeq) </k>

  claim [ba-ab]:
    <k>
      str(antiFinish(
        .IntSeq,
        .IntSeq,
        iCons(98, iCons(97, iCons(32, iCons(97, iCons(98, .IntSeq)))))))
      => str(iCons(97, iCons(98, iCons(32, iCons(97, iCons(98, .IntSeq))))))
    </k>

  claim [insert-ab]:
    <k> str(insertFinish(.IntSeq, 97, iCons(98, .IntSeq)))
        => str(iCons(97, iCons(98, .IntSeq))) </k>
endmodule
