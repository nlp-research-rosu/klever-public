requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports COUNT-UPPER-VERIFICATION

  // Deliberately false at the satisfying witness S = "".
  claim <k> run(countUpperProgram, S:String)
          => intVal(countUpperSpec(S) +Int 1) ... </k>
endmodule
