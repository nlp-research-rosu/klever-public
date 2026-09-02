requires "verification.k"

module AUDIT-SPEC-EXAMPLE-3
  imports COUNT-UPPER-VERIFICATION

  claim <k> run(countUpperProgram, "dBBE") => intVal(0) ... </k>
endmodule
