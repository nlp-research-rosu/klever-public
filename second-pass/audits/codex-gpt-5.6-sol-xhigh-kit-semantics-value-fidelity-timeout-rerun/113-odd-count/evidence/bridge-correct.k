requires "/tmp/audit-work/source/verification.k"

module BRIDGE-CORRECT
  imports VERIFICATION

  claim [count-ground]:
    <k>
      digitOccurrences(strToCodes("1110"), 49)
      => 3
    </k>

  claim [int-string-ground]:
    <k>
      intStringCodes(10)
      => strToCodes("10")
    </k>
endmodule
