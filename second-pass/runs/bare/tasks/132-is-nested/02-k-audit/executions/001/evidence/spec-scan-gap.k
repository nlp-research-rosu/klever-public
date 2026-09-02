requires "verification.k"

module SPEC-SCAN-GAP
  imports VERIFICATION

  claim
    <k> .K </k>
    <functions> .Map </functions>
    <env> .Map </env>
    <result>
      boolVal(scan(4, lbr .BString)) => boolVal(false)
    </result>
endmodule
