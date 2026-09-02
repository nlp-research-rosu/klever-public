requires "connection-verification.k"

module CONNECTION-SPEC
  imports CONNECTION-VERIFICATION

  claim
    <k> applyCmp("<", I:Int, J:Int)
      => auditIntValue(I) <Int auditIntValue(J)
    </k>
    [label(int-compare-connection)]
endmodule
