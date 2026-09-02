requires "verification.k"

module AUDIT-SPEC-VACUITY-CONCRETE
  imports COUNT-UPPER-VERIFICATION

  // Deliberately false: both Python implementations return 1 on this input.
  claim <k> run(countUpperProgram, "aBCdEf") => intVal(2) ... </k>
endmodule
