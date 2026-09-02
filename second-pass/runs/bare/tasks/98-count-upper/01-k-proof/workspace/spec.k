requires "verification.k"

module COUNT-UPPER-SPEC
  imports COUNT-UPPER-VERIFICATION

  // Total functional correctness for every K String.
  claim <k> run(countUpperProgram, S:String)
          => intVal(countUpperSpec(S)) ... </k>

  // The examples from prompt.py.
  claim <k> run(countUpperProgram, "aBCdEf") => intVal(1) ... </k>
  claim <k> run(countUpperProgram, "abcdefg") => intVal(0) ... </k>
  claim <k> run(countUpperProgram, "dBBE") => intVal(0) ... </k>

endmodule
