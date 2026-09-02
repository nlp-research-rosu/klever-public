requires "/tmp/audit-work/104-unique-digits-audit-002/body-mutation/verification.k"

module AUDIT-BODY-MUTATION-ENTRY
  imports VERIFICATION

  claim <k> solutionProgram ~> invoke("unique_digits", pyList(NS))
        => pyList(uniqueDigitsSpec(NS)) ... </k>
    requires positiveInts(NS)
endmodule
