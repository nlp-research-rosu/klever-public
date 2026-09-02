requires "/tmp/audit-work/source/verification.k"

module BRIDGE-OPPOSITE
  imports VERIFICATION

  claim [count-wrong]:
    <k>
      digitOccurrences(strToCodes("1110"), 49)
      => 2
    </k>

  claim [int-string-wrong]:
    <k>
      intStringCodes(10)
      => strToCodes("11")
    </k>
endmodule
