requires "verification.k"

module AUDIT-GROUND-SPEC
  imports VERIFICATION

  // No entry precondition exists. "A.dll" is a concrete satisfying witness,
  // and both Python implementations return "Yes" for it.
  claim <k> runProgram(solutionProgram, "A.dll")
          => VStr("Yes")
        </k>
endmodule
