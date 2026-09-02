requires "verification.k"

module AUDIT-SPEC-EXAMPLE-2
  imports COUNT-UPPER-VERIFICATION

  claim <k> run(countUpperProgram, "abcdefg") => intVal(0) ... </k>
endmodule
