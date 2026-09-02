requires "verification.k"

module AUDIT-SPEC-GENERAL
  imports COUNT-UPPER-VERIFICATION

  claim <k> run(countUpperProgram, S:String)
          => intVal(countUpperSpec(S)) ... </k>
endmodule
