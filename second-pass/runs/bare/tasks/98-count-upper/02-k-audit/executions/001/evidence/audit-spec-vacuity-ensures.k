requires "verification.k"

module AUDIT-SPEC-VACUITY-ENSURES
  imports COUNT-UPPER-VERIFICATION

  // Same reachable result, plus a deliberately false result obligation.
  claim <k> run(countUpperProgram, "aBCdEf") => intVal(1) ... </k>
    ensures 1 ==Int 2
endmodule
