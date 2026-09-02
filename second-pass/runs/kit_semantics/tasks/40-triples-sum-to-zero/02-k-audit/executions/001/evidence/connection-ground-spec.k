requires "connection-verification.k"

module CONNECTION-GROUND-SPEC
  imports CONNECTION-VERIFICATION

  claim [length-empty]:
    <k> vsLen(auditIntVals(.IntSeq)) => 0 </k>

  claim [length-four]:
    <k>
      vsLen(auditIntVals(iCons(7, iCons(-3, iCons(11, iCons(5, .IntSeq))))))
      => 4
    </k>

  claim [index-first]:
    <k>
      valSeqAt(
        auditIntVals(iCons(7, iCons(-3, iCons(11, .IntSeq)))),
        0)
      => 7
    </k>

  claim [index-middle]:
    <k>
      valSeqAt(
        auditIntVals(iCons(7, iCons(-3, iCons(11, .IntSeq)))),
        1)
      => -3
    </k>

  claim [index-last]:
    <k>
      valSeqAt(
        auditIntVals(iCons(7, iCons(-3, iCons(11, .IntSeq)))),
        2)
      => 11
    </k>
endmodule
