requires "verification.k"

module AUDIT-VACUITY-SPEC
  imports VALID-DATE-VERIFICATION

  // Fresh reviewer mutation: the unchanged submitted program returns true on
  // this satisfying input, so a false result obligation must be rejected.
  claim <k> runProgram(solutionProgram, "valid_date", vals(strVal("03-11-2000")))
          => boolVal(false) </k>
endmodule
