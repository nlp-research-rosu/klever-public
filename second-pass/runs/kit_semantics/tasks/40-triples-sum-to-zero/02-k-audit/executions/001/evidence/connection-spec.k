requires "connection-verification.k"

module CONNECTION-SPEC
  imports CONNECTION-VERIFICATION

  // Universal structural connection for represented-list length.
  claim [length-connection]:
    <k>
      vsLen(auditIntVals(IS:IntSeq))
      =>
      isLen(IS)
    </k>

  // Every satisfying in-bounds access has a nonempty source sequence.
  claim [index-connection]:
    <k>
      valSeqAt(auditIntVals(iCons(H:Int, R:IntSeq)), I:Int)
      =>
      auditIntAt(iCons(H, R), I)
    </k>
    requires 0 <=Int I
      andBool I <Int isLen(iCons(H, R))
endmodule
