requires "connection-verification.k"

module CONNECTION-OPPOSITE-SPEC
  imports CONNECTION-VERIFICATION

  // Deliberately wrong opposite interpretation of the middle element.
  claim [wrong-middle]:
    <k>
      valSeqAt(
        auditIntVals(iCons(7, iCons(-3, iCons(11, .IntSeq)))),
        1)
      => 99
    </k>
endmodule
