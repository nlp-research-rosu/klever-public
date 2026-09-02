requires "verification.k"

module AUDIT-FALSE-SPEC
  imports VERIFICATION

  // Fresh non-vacuity mutation: "A.dll" satisfies the entry precondition
  // (there is none) and both Python implementations return "Yes".
  claim <k> runProgram(solutionProgram, "A.dll")
          => VStr("No")
        </k>
endmodule
