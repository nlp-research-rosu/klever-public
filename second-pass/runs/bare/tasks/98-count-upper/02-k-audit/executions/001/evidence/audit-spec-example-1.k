requires "verification.k"

module AUDIT-SPEC-EXAMPLE-1
  imports COUNT-UPPER-VERIFICATION

  claim <k> run(countUpperProgram, "aBCdEf") => intVal(1) ... </k>
endmodule
