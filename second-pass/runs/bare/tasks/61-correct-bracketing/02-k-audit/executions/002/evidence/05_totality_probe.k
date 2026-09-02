requires "/tmp/audit-work/61-correct-bracketing-audit/candidate/verification.k"

module TOTALITY-PROBE
  imports MPY-VERIFICATION

  // bracketSpec is declared [total], but its equations intentionally have no
  // non-"(" case when N < 0.  This probe asks whether the declaration alone
  // fabricates a fixed false result on that uncovered input.
  claim [uncovered-negative]:
    <mpy>
      <k> boolVal(bracketSpec(-1, ")")) => boolVal(false) </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </mpy>
endmodule
