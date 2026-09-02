requires "verification.k"

module AUDIT-GROUND-WITNESSES
  imports VERIFICATION

  claim [reverse-result]:
    <k>
      circularShiftResult(12, 3)
      => str(strToCodes("21"))
    </k>

  claim [negative-result]:
    <k>
      circularShiftResult(12, -1)
      => str(strToCodes("12"))
    </k>

  claim [rotate-result]:
    <k>
      circularShiftResult(12, 1)
      => str(strToCodes("21"))
    </k>
endmodule
