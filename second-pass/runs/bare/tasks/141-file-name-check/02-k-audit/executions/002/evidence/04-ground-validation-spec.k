requires "verification.k"

module GROUND-VALIDATION-SPEC
  imports VERIFICATION

  claim <k> runProgram(solutionProgram, "example.txt")
          => VStr("Yes")
        </k>

  claim <k> runProgram(solutionProgram, "")
          => VStr("No")
        </k>

  claim <k> runProgram(solutionProgram, "a123.txt")
          => VStr("Yes")
        </k>

  claim <k> runProgram(solutionProgram, "a1234.txt")
          => VStr("No")
        </k>

  claim <k> runProgram(solutionProgram, "é.txt")
          => VStr("No")
        </k>

  claim <k> runProgram(solutionProgram, "a١٢٣٤.txt")
          => VStr("Yes")
        </k>
endmodule
