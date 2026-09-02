requires "connection-verification.k"

module CONNECTION-SPEC
  imports CONNECTION-VERIFICATION

  claim
    <k> applyCmp("<", L:Val, R:Val)
      => auditIntValue(L) <Int auditIntValue(R)
    </k>
    requires isInt(L) andBool isInt(R)
    [label(int-compare-connection)]
endmodule
